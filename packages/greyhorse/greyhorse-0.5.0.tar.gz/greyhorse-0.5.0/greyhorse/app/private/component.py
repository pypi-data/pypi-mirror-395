from collections import defaultdict
from collections.abc import Callable, Collection, Mapping
from dataclasses import dataclass, field
from functools import partial
from typing import Any, override

from greyhorse.app.abc.component import Component as BaseComponent
from greyhorse.app.abc.functional.context import OperationContext
from greyhorse.app.abc.resources.operators import (
    MutOperatorCollector,
    OperatorCollector,
    OperatorData,
)
from greyhorse.app.abc.resources.providers import (
    MutProviderCollector,
    ProviderCollector,
    ProviderData,
)
from greyhorse.factory import Factory

from .fragment import Fragment
from .functional.context import BucketOperationContext
from .functional.factory_storage import FactoryStorage
from .functional.operators import ContextOperator


@dataclass(frozen=True, slots=True, kw_only=True)
class _ComponentOperatorCollector(MutOperatorCollector):
    data: dict[str, list[tuple[type, OperatorData]]] = field(
        default_factory=partial(defaultdict, list)
    )

    @override
    def add[U](self, target_type: type[U], instance: OperatorData, /, **metadata: Any) -> bool:
        self.data[instance.fragment].append((target_type, instance))
        return True

    @override
    def remove[U](self, target_type: type[U], instance: OperatorData | None = None) -> bool:
        self.data[instance.fragment].remove((target_type, instance))
        return True


@dataclass(frozen=True, slots=True, kw_only=True)
class _ComponentProviderCollector(MutProviderCollector):
    data: dict[str, list[tuple[type, ProviderData]]] = field(
        default_factory=partial(defaultdict, list)
    )

    @override
    def add[U](self, target_type: type[U], instance: ProviderData, /, **metadata: Any) -> bool:
        self.data[instance.fragment].append((target_type, instance))
        return True

    @override
    def remove[U](self, target_type: type[U], instance: ProviderData | None = None) -> bool:
        self.data[instance.fragment].remove((target_type, instance))
        return True


class Component(BaseComponent):
    __slots__ = (
        '_contexts',
        '_exports',
        '_factories',
        '_fragments',
        '_name',
        '_op_registry',
        '_operators',
        '_prov_registry',
    )

    def __init__(
        self,
        name: str,
        fragments: Collection[Fragment],
        exports: Collection[type] | None = None,
    ) -> None:
        self._name = name
        self._fragments = list(fragments)
        self._factories = FactoryStorage()
        self._operators = FactoryStorage()
        self._contexts = {
            f.name: BucketOperationContext(self._factories, f.scope, fragment=f.name)
            for f in self._fragments
        }
        self._exports = set(exports) if exports else set()
        self._prov_registry = _ComponentProviderCollector()
        self._op_registry = _ComponentOperatorCollector()

    def __repr__(self) -> str:
        return f'Component "{self._name}"'

    @property
    @override
    def name(self) -> str:
        return self._name

    @override
    def context(self) -> OperationContext:
        return BucketOperationContext(self._operators)

    @override
    def add_factory[T](self, target_type: type[T], factory: Factory[T], **filters: Any) -> bool:
        return self._factories.add_factory(target_type, factory, **filters)

    @override
    def remove_factory[T](
        self, target_type: type[T], factory: Factory[T] | None = None, **filters: Any
    ) -> Collection[tuple[Factory[T], Mapping[str, Any]]]:
        return self._factories.remove_factory(target_type, factory, **filters)

    @override
    def setup(
        self,
        op_collector: OperatorCollector | None = None,
        prov_collector: ProviderCollector | None = None,
    ) -> None:
        for fragment in self._fragments:
            fragment.setup(self._name, self._factories, self._op_registry, self._prov_registry)

        for fragment in self._fragments:
            for target_type, prov_data in self._prov_registry.data[fragment.name]:
                if res := self._operators.get_factory(signature=prov_data.signature):
                    self._factories.add_factory(
                        target_type,
                        res.unwrap(),
                        fragment=prov_data.fragment,
                        scope=prov_data.scope,
                        **prov_data.metadata,
                    )
                elif prov_collector is not None:
                    prov_collector.add(target_type, prov_data)

            for target_type, op_data in self._op_registry.data[fragment.name]:
                fragment_context = self._contexts[fragment.name]
                ctx_operator = ContextOperator.from_context(
                    fragment_context, op_data.target, op_data.scope, op_data.external_params
                )
                ctx_operator.compile()
                target = ctx_operator.get_functor()
                self._operators.add_factory(target_type, target)
                if op_collector is not None and target_type in self._exports:
                    signature = Callable[[*target.actual_params.values()], target_type]
                    op_data = OperatorData(
                        component=self._name,
                        fragment=fragment.name,
                        target=target,
                        signature=signature,
                    )
                    op_collector.add(target_type, op_data)

    @override
    def teardown(
        self,
        op_collector: MutOperatorCollector | None = None,
        prov_collector: MutProviderCollector | None = None,
    ) -> None:
        for fragment in reversed(self._fragments):
            for target_type, prov_data in reversed(self._prov_registry.data[fragment.name]):
                if res := self._operators.get_factory(signature=prov_data.signature):
                    self._factories.remove_factory(
                        target_type,
                        res.unwrap(),
                        fragment=prov_data.fragment,
                        scope=prov_data.scope,
                        **prov_data.metadata,
                    )
                elif prov_collector is not None:
                    prov_collector.remove(target_type, prov_data)

            for target_type, op_data in reversed(self._op_registry.data[fragment.name]):
                for target, _md in self._operators.remove_factory(target_type):
                    if op_collector is not None and target_type in self._exports:
                        signature = Callable[[*target.actual_params.values()], target_type]
                        op_data = OperatorData(
                            component=self._name,
                            fragment=fragment.name,
                            target=target,
                            signature=signature,
                        )
                        op_collector.remove(target_type, op_data)

        for fragment in reversed(self._fragments):
            fragment.teardown(
                self._name, self._factories, self._op_registry, self._prov_registry
            )
