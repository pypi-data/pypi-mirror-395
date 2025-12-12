from abc import ABC, abstractmethod
from collections.abc import Callable, Iterable, Mapping
from typing import Any, override

from greyhorse.maybe import Maybe, Nothing


class Selector[K, T](ABC):
    @abstractmethod
    def has(self, key: K) -> bool: ...

    @abstractmethod
    def get(self, key: K) -> Maybe[T]: ...

    @abstractmethod
    def get_with_metadata(self, key: K) -> Maybe[tuple[T, Mapping[str, Any]]]: ...


class ListSelector[K, T](Selector[K, T], ABC):
    @abstractmethod
    def list(self, key: K | None = None) -> Iterable[tuple[K, T] | T]: ...

    @abstractmethod
    def list_with_metadata(
        self, key: K | None = None
    ) -> Iterable[tuple[K, T, Mapping[str, Any]] | tuple[T, Mapping[str, Any]]]: ...

    @abstractmethod
    def filter(
        self, filter_fn: Callable[[K, Mapping[str, Any]], bool] | None = None
    ) -> Iterable[tuple[K, T, Mapping[str, Any]]]: ...


class SelectorCombiner[K, T](Selector[K, T]):
    __slots__ = ('_selectors',)

    def __init__(self, *selectors: Selector[K, T]) -> None:
        self._selectors = list(selectors)

    def __len__(self) -> int:
        return len(self._selectors)

    def add_selector(self, selector: Selector[K, T]) -> bool:
        if selector in self._selectors:
            return False
        self._selectors.append(selector)
        return True

    def remove_selector(self, selector: Selector[K, T]) -> bool:
        if selector not in self._selectors:
            return False
        self._selectors.remove(selector)
        return True

    @override
    def has(self, key: K) -> bool:
        for selector in self._selectors:
            if res := selector.has(key):
                return res
        return False

    @override
    def get(self, key: K) -> Maybe[T]:
        for selector in self._selectors:
            if res := selector.get(key):
                return res
        return Nothing

    @override
    def get_with_metadata(self, key: K) -> Maybe[tuple[T, Mapping[str, Any]]]:
        for selector in self._selectors:
            if res := selector.get_with_metadata(key):
                return res
        return Nothing
