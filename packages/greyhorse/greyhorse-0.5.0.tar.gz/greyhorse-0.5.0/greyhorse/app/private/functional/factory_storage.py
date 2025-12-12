from collections.abc import Callable, Collection, Mapping
from dataclasses import dataclass, field
from typing import Any, override

from greyhorse.app.abc.functional.registries import MutFactoryRegistry
from greyhorse.factory import Factory
from greyhorse.maybe import Just, Maybe, Nothing

from ..collections.registries import MutDictRegistry


@dataclass(slots=True, frozen=True, kw_only=True)
class _CovariantFactoryFilter[T]:
    key: type[T]
    filters: Mapping[str, Any] = field(default_factory=dict)

    def __call__(self, t: type[T], metadata: dict[str, Any]) -> bool:
        if not issubclass(self.key, t):
            return False

        counter = 0

        for k, v in self.filters.items():
            if k in metadata and metadata[k] == v:
                counter += 1

        return counter >= len(metadata)


class FactoryStorage(MutFactoryRegistry):
    __slots__ = ('_registries',)

    def __init__(self) -> None:
        self._registries = MutDictRegistry[type, Factory[Any]](allow_many=True)

    @override
    def has_factory[T](
        self,
        target_type: type[T] | None = None,
        signature: type[Callable] | None = None,
        **filters: Any,
    ) -> bool:
        if target_type is None:
            target_type = signature.__args__[-1]

        filter = _CovariantFactoryFilter(key=target_type, filters=filters)

        for _, factory, __ in self._registries.filter(filter):
            if signature is None or factory.check_signature(signature):
                return True

        return False

    @override
    def get_factory[T](
        self,
        target_type: type[T] | None = None,
        signature: type[Callable] | None = None,
        **filters: Any,
    ) -> Maybe[Factory[T]]:
        if target_type is None:
            target_type = signature.__args__[-1]

        filter = _CovariantFactoryFilter(key=target_type, filters=filters)

        for _, factory, __ in self._registries.filter(filter):
            if signature is None or factory.check_signature(signature):
                return Just(factory)

        return Nothing

    @override
    def get_factory_with_metadata[T](
        self,
        target_type: type[T] | None = None,
        signature: type[Callable] | None = None,
        **filters: Any,
    ) -> Maybe[tuple[Factory[T], Mapping[str, Any]]]:
        if target_type is None:
            target_type = signature.__args__[-1]

        filter = _CovariantFactoryFilter(key=target_type, filters=filters)

        for _, factory, md in self._registries.filter(filter):
            if signature is None or factory.check_signature(signature):
                return Just((factory, md))

        return Nothing

    @override
    def add_factory[T](self, target_type: type[T], factory: Factory[T], **filters: Any) -> bool:
        # filter = _CovariantFactoryFilter(key=target_type, filters=filters)
        # for _ in self._registries.filter(filter):
        #     return False
        return self._registries.add(target_type, factory, **filters)

    @override
    def remove_factory[T](
        self, target_type: type[T], factory: Factory[T] | None = None, **filters: Any
    ) -> Collection[tuple[Factory[T], Mapping[str, Any]]]:
        to_remove: dict[int, tuple[Factory, dict[str, Any]]] = {}

        filter = _CovariantFactoryFilter(key=target_type, filters=filters)
        for _, orig_fn, md in self._registries.filter(filter):
            if factory is None or orig_fn == factory:
                to_remove[id(orig_fn)] = (orig_fn, md)

        res = []

        for orig_fn, md in to_remove.values():
            if self._registries.remove(target_type, orig_fn):
                res.append((orig_fn, md))

        return res
