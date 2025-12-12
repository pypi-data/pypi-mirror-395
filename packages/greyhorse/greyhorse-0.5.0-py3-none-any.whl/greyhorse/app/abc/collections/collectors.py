from abc import ABC, abstractmethod
from typing import Any, override


class Collector[K, T](ABC):
    @abstractmethod
    def add(self, key: K, instance: T, /, **metadata: Any) -> bool: ...


class MutCollector[K, T](Collector[K, T], ABC):
    @abstractmethod
    def remove(self, key: K, instance: T | None = None) -> bool: ...


class CollectorCombiner[K, T](MutCollector[K, T]):
    __slots__ = ('_collectors',)

    def __init__(self, *collectors: MutCollector[K, T]) -> None:
        self._collectors = list(collectors)

    def __len__(self) -> int:
        return len(self._collectors)

    def add_collector(self, collector: MutCollector[K, T]) -> bool:
        if collector in self._collectors:
            return False
        self._collectors.append(collector)
        return True

    def remove_collector(self, collector: MutCollector[K, T]) -> bool:
        if collector not in self._collectors:
            return False
        self._collectors.remove(collector)
        return True

    @override
    def add(self, key: K, instance: T, /, **metadata: Any) -> bool:
        res = False
        for collector in self._collectors:
            res |= collector.add(key, instance, **metadata)
        return res

    @override
    def remove(self, key: K, instance: T | None = None) -> bool:
        res = False
        for collector in self._collectors:
            res |= collector.remove(key, instance)
        return res
