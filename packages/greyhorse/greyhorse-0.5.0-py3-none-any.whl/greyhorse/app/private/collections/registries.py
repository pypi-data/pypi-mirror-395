from collections import defaultdict
from collections.abc import Callable, Iterable, Mapping
from typing import Any, override

from greyhorse.app.abc.collections.registries import ListRegistry, MutListRegistry
from greyhorse.maybe import Just, Maybe, Nothing


class DictRegistry[K, T](ListRegistry[K, T]):
    __slots__ = ('_allow_many', '_storage')

    def __init__(self, allow_many: bool = False) -> None:
        self._storage: dict[K, list[tuple[T, dict[str, Any]]]] = defaultdict(list)
        self._allow_many = allow_many

    def __len__(self) -> int:
        return len(self._storage)

    @override
    def add(self, key: K, instance: T, /, **metadata: Any) -> bool:
        if key in self._storage:
            variants = self._storage[key]
            if not self._allow_many and len(variants) > 0:
                return instance == variants[0]
            if instance in variants:
                return False
            variants.append((instance, metadata))
        else:
            self._storage[key].append((instance, metadata))
        return True

    @override
    def has(self, key: K) -> bool:
        return key in self._storage

    @override
    def get(self, key: K) -> Maybe[T]:
        if variants := self._storage.get(key):
            item = variants[0]
            return Just(item[0])

        return Nothing

    @override
    def get_with_metadata(self, key: K) -> Maybe[tuple[T, Mapping[str, Any]]]:
        if variants := self._storage.get(key):
            item = variants[0]
            return Just(item)

        return Nothing

    @override
    def list(self, key: K | None = None) -> Iterable[tuple[K, T] | T]:
        if key is None:
            for k, v in self._storage.items():
                for item in v:
                    yield k, item[0]
        else:
            if key not in self._storage:
                return

            for item in self._storage[key]:
                yield item[0]

    @override
    def list_with_metadata(
        self, key: K | None = None
    ) -> Iterable[tuple[K, T, Mapping[str, Any]] | tuple[T, Mapping[str, Any]]]:
        if key is None:
            for k, v in self._storage.items():
                for item in v:
                    yield k, *item
        else:
            if key not in self._storage:
                return

            yield from self._storage[key]

    @override
    def filter(
        self, filter_fn: Callable[[K, Mapping[str, Any]], bool] | None = None
    ) -> Iterable[tuple[K, T, Mapping[str, Any]]]:
        for k, v in self._storage.items():
            for item in v:
                if not filter_fn or filter_fn(k, item[1]):
                    yield k, *item


class MutDictRegistry[K, T](DictRegistry[K, T], MutListRegistry[K, T]):
    @override
    def remove(self, key: K, instance: T | None = None) -> bool:
        if key not in self._storage:
            return False

        result = False

        if instance is None:
            del self._storage[key]
            result = True

        else:
            i = 0
            items = self._storage[key]
            while i < len(items):
                v, _ = items[i]
                if v == instance:
                    result = True
                    self._storage[key].pop(i)
                else:
                    i += 1

            if len(self._storage[key]) == 0:
                del self._storage[key]

        return result

    @override
    def clear(self) -> None:
        while key := next(iter(self._storage), None):
            del self._storage[key]


class ScopedDictRegistry[K, T](ListRegistry[K, T]):
    __slots__ = ('_scope_func', '_storage')

    def __init__(
        self, factory: Callable[[], DictRegistry[K, T]], scope_func: Callable[[], str]
    ) -> None:
        super().__init__()
        self._scope_func = scope_func
        self._storage: dict[str, DictRegistry[K, T]] = defaultdict(factory)

    def _get_registry(self) -> DictRegistry[K, T]:
        key = self._scope_func()
        return self._storage[key]

    def __len__(self) -> int:
        registry = self._get_registry()
        return registry.__len__()

    @override
    def add(self, key: K, instance: T, /, **metadata: Any) -> bool:
        registry = self._get_registry()
        return registry.add(key, instance, **metadata)

    @override
    def has(self, key: K) -> bool:
        registry = self._get_registry()
        return registry.has(key)

    @override
    def get(self, key: K) -> Maybe[T]:
        registry = self._get_registry()
        return registry.get(key)

    @override
    def get_with_metadata(self, key: K) -> Maybe[tuple[T, Mapping[str, Any]]]:
        registry = self._get_registry()
        return registry.get_with_metadata(key)

    @override
    def list(self, key: K | None = None) -> Iterable[tuple[K, T] | T]:
        registry = self._get_registry()
        return registry.list(key)

    @override
    def list_with_metadata(
        self, key: K | None = None
    ) -> Iterable[tuple[K, T, Mapping[str, Any]] | tuple[T, Mapping[str, Any]]]:
        registry = self._get_registry()
        return registry.list_with_metadata(key)

    @override
    def filter(
        self, filter_fn: Callable[[K, Mapping[str, Any]], bool] | None = None
    ) -> Iterable[tuple[K, T, Mapping[str, Any]]]:
        registry = self._get_registry()
        yield from registry.filter(filter_fn)


class ScopedMutDictRegistry[K, T](ScopedDictRegistry[K, T], MutListRegistry[K, T]):
    __slots__ = ('_storage',)

    def __init__(
        self, factory: Callable[[], MutDictRegistry[K, T]], scope_func: Callable[[], str]
    ) -> None:
        super().__init__(factory, scope_func)
        self._storage: dict[str, MutDictRegistry[K, T]] = defaultdict(factory)

    def _get_registry(self) -> MutDictRegistry[K, T]:
        key = self._scope_func()
        return self._storage[key]

    @override
    def remove(self, key: K, instance: T | None = None) -> bool:
        registry = self._get_registry()
        return registry.remove(key, instance)

    @override
    def clear(self) -> None:
        registry = self._get_registry()
        registry.clear()
        del self._storage[self._scope_func()]
