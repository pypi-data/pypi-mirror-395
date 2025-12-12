from abc import ABC, abstractmethod
from collections.abc import Callable, Collection, Mapping
from typing import Any, overload

from greyhorse.factory import Factory
from greyhorse.maybe import Maybe


class FactoryRegistry(ABC):
    @overload
    def has_factory[T](
        self, target_type: type[T] = ..., signature: None = None, **filters: Any
    ) -> bool: ...

    @overload
    def has_factory(
        self, target_type: None = None, signature: type[Callable] = ..., **filters: Any
    ) -> bool: ...

    @abstractmethod
    def has_factory[T](
        self,
        target_type: type[T] | None = None,
        signature: type[Callable] | None = None,
        **filters: Any,
    ) -> bool: ...

    @overload
    def get_factory[T](
        self, target_type: type[T] = ..., signature: None = None, **filters: Any
    ) -> Maybe[Factory[T]]: ...

    @overload
    def get_factory(
        self, target_type: None = None, signature: type[Callable] = ..., **filters: Any
    ) -> Maybe[Factory[Any]]: ...

    @abstractmethod
    def get_factory[T](
        self,
        target_type: type[T] | None = None,
        signature: type[Callable] | None = None,
        **filters: Any,
    ) -> Maybe[Factory[T]]: ...

    @overload
    def get_factory_with_metadata[T](
        self, target_type: type[T] = ..., signature: None = None, **filters: Any
    ) -> Maybe[tuple[Factory[T], Mapping[str, Any]]]: ...

    @overload
    def get_factory_with_metadata(
        self, target_type: None = None, signature: type[Callable] = ..., **filters: Any
    ) -> Maybe[tuple[Factory[Any], Mapping[str, Any]]]: ...

    @abstractmethod
    def get_factory_with_metadata[T](
        self,
        target_type: type[T] | None = None,
        signature: type[Callable] | None = None,
        **filters: Any,
    ) -> Maybe[tuple[Factory[T], Mapping[str, Any]]]: ...


class MutFactoryRegistry(FactoryRegistry, ABC):
    @abstractmethod
    def add_factory[T](
        self, target_type: type[T], factory: Factory[T], **filters: Any
    ) -> bool: ...

    @abstractmethod
    def remove_factory[T](
        self, target_type: type[T], factory: Factory[T] | None = None, **filters: Any
    ) -> Collection[tuple[Factory[T], Mapping[str, Any]]]: ...
