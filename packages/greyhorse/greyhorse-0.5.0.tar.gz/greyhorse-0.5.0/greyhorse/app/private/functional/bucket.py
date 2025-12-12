from __future__ import annotations

from collections import defaultdict
from collections.abc import Mapping
from dataclasses import dataclass, field
from enum import IntEnum
from typing import Any, override

from greyhorse.app.abc.collections.registries import MutRegistry
from greyhorse.app.abc.collections.selectors import Selector
from greyhorse.factory import Factory
from greyhorse.maybe import Maybe, Nothing

from ..collections.registries import MutDictRegistry
from ..runtime.invoke import invoke_sync


@dataclass(slots=True, kw_only=True)
class Bucket(Selector[type, Any]):
    cache: MutRegistry[type, Any] = field(
        default_factory=MutDictRegistry[type, Any], repr=False
    )
    finalizers: dict[type, list[tuple[Factory[Any], Any]]] = field(
        default_factory=lambda: defaultdict(list), repr=False
    )
    prev: Bucket | None = field(default=None, repr=False)
    scope: IntEnum | None = field(default=None, repr=True)
    num_children: int = field(default=0, repr=True)
    _counter: int = field(default=0, init=False, repr=True)

    @override
    def has[T](self, key: type[T]) -> bool:
        bucket = self

        while bucket is not None:
            if bucket.cache.has(key):
                return True
            bucket = bucket.prev
        return False

    @override
    def get[T](self, key: type[T]) -> Maybe[T]:
        bucket = self

        while bucket is not None:
            if (v := bucket.cache.get(key)).is_just():
                return v
            bucket = bucket.prev
        return Nothing

    @override
    def get_with_metadata[T](self, key: type[T]) -> Maybe[tuple[T, Mapping[str, Any]]]:
        bucket = self

        while bucket is not None:
            if (v := bucket.cache.get_with_metadata(key)).is_just():
                return v
            bucket = bucket.prev
        return Nothing

    def incr(self) -> None:
        bucket = self

        while bucket is not None:
            bucket._counter += 1  # noqa: SLF001
            bucket = bucket.prev

    def decr(self) -> None:
        bucket = self

        while bucket is not None:
            bucket._counter -= 1  # noqa: SLF001
            if bucket._counter == 0:  # noqa: SLF001
                bucket._finalize()  # noqa: SLF001
            bucket = bucket.prev

    def _finalize(self) -> None:
        while key := next(reversed(self.finalizers), None):
            for factory, instance in reversed(self.finalizers[key]):
                invoke_sync(factory.destroy, instance)
            del self.finalizers[key]

        self.cache.clear()
