from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Mapping
from dataclasses import dataclass, field
from enum import IntEnum
from types import TracebackType
from typing import Self

from greyhorse.factory import Factory
from greyhorse.maybe import Maybe


@dataclass(slots=True, frozen=True, kw_only=True)
class ResolvedData[T]:
    type: type[T]
    factory: Factory[T]
    deps: dict[str, type] = field(default_factory=dict)


@dataclass(slots=True, frozen=True, kw_only=True)
class ResolveResult:
    resolved: dict[type, ResolvedData] = field(default_factory=dict)
    unresolved: list[type] = field(default_factory=list)


class Resolver(ABC):
    @abstractmethod
    def can_resolve[T](self, key: type[T]) -> bool: ...

    @abstractmethod
    def resolve_factories[T](
        self, key: type[T], from_scope: IntEnum | None = None
    ) -> ResolveResult: ...

    @abstractmethod
    def resolve_value[T](
        self,
        resolved: Mapping[type, ResolvedData],
        key: type[T],
        from_scope: IntEnum | None = None,
    ) -> Maybe[T]: ...

    @abstractmethod
    def resolve[T](self, key: type[T], from_scope: IntEnum | None = None) -> Maybe[T]: ...

    @abstractmethod
    def __enter__(self) -> Self: ...

    @abstractmethod
    def __exit__(
        self,
        exc_type: type[BaseException] | None = None,
        exc_value: BaseException | None = None,
        traceback: TracebackType | None = None,
    ) -> None: ...
