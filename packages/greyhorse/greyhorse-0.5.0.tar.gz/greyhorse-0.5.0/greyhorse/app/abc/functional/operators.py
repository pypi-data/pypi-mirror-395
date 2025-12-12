from abc import ABC, abstractmethod
from collections.abc import Collection
from dataclasses import dataclass, field

from greyhorse.factory import Factory


@dataclass(slots=True, frozen=True, kw_only=True)
class CompilationResult:
    resolved: Collection[type] = field(default_factory=list)
    unresolved: Collection[type] = field(default_factory=list)

    @property
    def success(self) -> bool:
        return self.resolved and not self.unresolved

    @property
    def partial(self) -> bool:
        return bool(self.resolved) and bool(self.unresolved)

    @property
    def failed(self) -> bool:
        return not self.resolved and self.unresolved


class Operator[T](ABC):
    @property
    @abstractmethod
    def return_type(self) -> type[T]: ...

    @property
    @abstractmethod
    def compiled(self) -> bool: ...

    @abstractmethod
    def compile(self) -> CompilationResult: ...

    @abstractmethod
    def get_functor(self) -> Factory[T]: ...
