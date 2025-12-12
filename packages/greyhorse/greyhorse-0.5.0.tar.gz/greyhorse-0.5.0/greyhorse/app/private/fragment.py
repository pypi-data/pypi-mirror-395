import inspect
import types
from collections.abc import Callable, Collection, Iterable, Mapping
from dataclasses import dataclass, field, replace
from enum import IntEnum
from typing import Any, ClassVar

from greyhorse.app.abc.functional.registries import MutFactoryRegistry
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
from greyhorse.factory import CachePolicy, Factory, FactoryFn, into_factory


@dataclass(slots=True, frozen=True, kw_only=True)
class _MemberData:
    target: Factory[Any] | types.FunctionType
    for_type: type | types.UnionType | None = None
    policy: CachePolicy = CachePolicy.ANY
    scope: IntEnum | None = None
    metadata: Mapping[str, Any] = field(default_factory=dict)


@dataclass(slots=True, frozen=True, kw_only=True)
class _OperatorMemberData:
    target: Factory[Any] | types.FunctionType
    for_type: type | types.UnionType | None = None
    external: Collection[type] | None = None
    scope: IntEnum | None = None
    metadata: Mapping[str, Any] = field(default_factory=dict)


def _is_factory_member(member: types.FunctionType) -> bool:
    return hasattr(member, '__factory_data__')


def _is_operator_member(member: types.FunctionType) -> bool:
    return hasattr(member, '__operator_data__')


def _is_provider_member(member: types.FunctionType) -> bool:
    return hasattr(member, '__provider_data__')


def factory(
    for_type: type | types.UnionType | None = None,
    scope: IntEnum | None = None,
    policy: CachePolicy = CachePolicy.ANY,
    **metadata: Any,
) -> Callable[[FactoryFn[Any]], FactoryFn[Any]]:
    def decorator(func: FactoryFn[Any]) -> FactoryFn[Any]:
        func.__factory_data__ = _MemberData(
            target=func, for_type=for_type, policy=policy, scope=scope, metadata=metadata
        )
        return func

    return decorator


def operator(
    for_type: type | types.UnionType | None = None,
    scope: IntEnum | None = None,
    external: Collection[type] | None = None,
    **metadata: Any,
) -> Callable[[FactoryFn[Any]], FactoryFn[Any]]:
    def decorator(func: FactoryFn[Any]) -> FactoryFn[Any]:
        func.__operator_data__ = _OperatorMemberData(
            target=func, for_type=for_type, external=external, scope=scope, metadata=metadata
        )
        return func

    return decorator


def provider(
    for_type: type | types.UnionType | None = None,
    scope: IntEnum | None = None,
    policy: CachePolicy = CachePolicy.ANY,
    **metadata: Any,
) -> Callable[[FactoryFn[Any]], FactoryFn[Any]]:
    def decorator(func: FactoryFn[Any]) -> FactoryFn[Any]:
        func.__provider_data__ = _MemberData(
            target=func, for_type=for_type, policy=policy, scope=scope, metadata=metadata
        )
        return func

    return decorator


class Fragment:
    __slots__ = ('__factories', '__operators', '__providers')
    name: ClassVar[str]
    scope: ClassVar[type[IntEnum] | None] = None

    def __init__(self) -> None:
        self.__factories: list[_MemberData] = []
        self.__operators: list[_OperatorMemberData] = []
        self.__providers: list[_MemberData] = []
        self._init_members()

    def __repr__(self) -> str:
        return f'Fragment "{self.name}"'

    def setup(
        self,
        component: str,
        factory_registry: MutFactoryRegistry,
        op_collector: OperatorCollector,
        prov_collector: ProviderCollector,
    ) -> None:
        for data in self.__factories:
            self._setup_factory(data, factory_registry)

        for data in self.__operators:
            self._setup_operator(data, factory_registry, op_collector, component)

        for data in self.__providers:
            self._setup_provider(data, prov_collector, component)

    def teardown(
        self,
        component: str,
        factory_registry: MutFactoryRegistry,
        op_collector: MutOperatorCollector,
        prov_collector: MutProviderCollector,
    ) -> None:
        for data in reversed(self.__providers):
            self._teardown_provider(data, prov_collector, component)

        for data in reversed(self.__operators):
            self._teardown_operator(data, factory_registry, op_collector, component)

        for data in reversed(self.__factories):
            self._teardown_factory(data, factory_registry)

    def _init_members(self) -> None:
        for _, member in inspect.getmembers(self):
            if _is_factory_member(member):
                data = member.__factory_data__
                data = replace(data, target=into_factory(member, cache_policy=data.policy))
                self.__factories.append(data)

            elif _is_operator_member(member):
                data = member.__operator_data__
                data = replace(data, target=into_factory(member, cache_policy=CachePolicy.ANY))
                self.__operators.append(data)

            elif _is_provider_member(member):
                data = member.__provider_data__
                data = replace(data, target=into_factory(member, cache_policy=data.policy))
                self.__providers.append(data)

    def _get_target_types(self, data: _MemberData) -> Iterable[type]:
        if data.for_type is None:
            target_types = [data.target.return_type]
        elif isinstance(data.for_type, types.UnionType):
            target_types = data.for_type.__args__
        else:
            target_types = [data.for_type]
        return target_types

    def _setup_factory(self, data: _MemberData, factory_registry: MutFactoryRegistry) -> None:
        target_types = self._get_target_types(data)
        scope = data.scope or (self.scope(0) if self.scope is not None else None)

        for target_type in target_types:
            filters = dict(fragment=self.name)
            if scope is not None:
                filters['scope'] = scope

            factory_registry.add_factory(target_type, data.target, **filters)

    def _teardown_factory(
        self, data: _MemberData, factory_registry: MutFactoryRegistry
    ) -> None:
        target_types = self._get_target_types(data)
        scope = data.scope or (self.scope(0) if self.scope is not None else None)

        for target_type in target_types:
            filters = dict(fragment=self.name)
            if scope is not None:
                filters['scope'] = scope

            factory_registry.remove_factory(target_type, data.target, **filters)

    def _setup_operator(
        self,
        data: _OperatorMemberData,
        factory_registry: MutFactoryRegistry,
        op_collector: OperatorCollector,
        component: str,
    ) -> None:
        scope = data.scope or (self.scope(0) if self.scope is not None else None)
        signature = Callable[[*data.target.actual_params.values()], data.target.return_type]

        op_data = OperatorData(
            component=component,
            fragment=self.name,
            target=data.target,
            signature=signature,
            scope=scope,
            external_params=data.external,
            metadata=data.metadata,
        )
        data = _MemberData(
            target=data.target, for_type=data.for_type, scope=data.scope, metadata=data.metadata
        )

        for target_type in self._get_target_types(data):
            op_collector.add(target_type, op_data)

        self._setup_factory(data, factory_registry)

    def _teardown_operator(
        self,
        data: _OperatorMemberData,
        factory_registry: MutFactoryRegistry,
        op_collector: MutOperatorCollector,
        component: str,
    ) -> None:
        scope = data.scope or (self.scope(0) if self.scope is not None else None)
        signature = Callable[[*data.target.actual_params.values()], data.target.return_type]

        op_data = OperatorData(
            component=component,
            fragment=self.name,
            target=data.target,
            signature=signature,
            scope=scope,
            external_params=data.external,
            metadata=data.metadata,
        )
        data = _MemberData(
            target=data.target, for_type=data.for_type, scope=data.scope, metadata=data.metadata
        )

        for target_type in self._get_target_types(data):
            op_collector.remove(target_type, op_data)

        self._teardown_factory(data, factory_registry)

    def _setup_provider(
        self, data: _MemberData, prov_collector: ProviderCollector, component: str
    ) -> None:
        scope = data.scope or (self.scope(0) if self.scope is not None else None)
        signature = Callable[[*data.target.actual_params.values()], data.target.return_type]

        prov_data = ProviderData(
            component=component,
            fragment=self.name,
            signature=signature,
            scope=scope,
            metadata=data.metadata,
        )

        for target_type in self._get_target_types(data):
            prov_collector.add(target_type, prov_data)

    def _teardown_provider(
        self, data: _MemberData, prov_collector: MutProviderCollector, component: str
    ) -> None:
        scope = data.scope or (self.scope(0) if self.scope is not None else None)
        signature = Callable[[*data.target.actual_params.values()], data.target.return_type]

        prov_data = ProviderData(
            component=component,
            fragment=self.name,
            signature=signature,
            scope=scope,
            metadata=data.metadata,
        )

        for target_type in self._get_target_types(data):
            prov_collector.remove(target_type, prov_data)
