from __future__ import annotations

from abc import ABC, abstractmethod
from enum import IntEnum
from typing import Any

from greyhorse.app.contexts import SyncContext

from ..collections.selectors import Selector
from .resolver import Resolver


class OperationContext(SyncContext[Selector[type, Any]], ABC):
    @property
    @abstractmethod
    def scope[S: IntEnum](self) -> S | None: ...

    @abstractmethod
    def context[S: IntEnum](self, scope: S | None = None) -> OperationContext: ...

    @abstractmethod
    def context_resolver[S: IntEnum](self, scope: S | None = None) -> Resolver: ...

    @abstractmethod
    def advance(self) -> OperationContext: ...
