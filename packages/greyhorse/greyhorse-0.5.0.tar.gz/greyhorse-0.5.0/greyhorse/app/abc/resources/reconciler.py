from __future__ import annotations

import asyncio
import enum
import threading
from abc import ABC, abstractmethod
from collections.abc import Awaitable, Callable, Collection
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Any, Optional

from greyhorse.enum import Enum, Struct, Unit
from greyhorse.utils.types import TypeWrapper

from .common import Condition, ResourceStatus, TransitionStatus


class ReconcilerRunPhase(Enum):
    Setup = Unit()
    Teardown = Unit()
    Periodic = Struct(interval=timedelta)
    Permanent = Struct(async_=bool)


class RestartPolicy(Enum):
    Always = Unit()
    Never = Unit()
    OnFailure = Unit()


type ReconcilerTaskFn[T] = Callable[[TaskHandler], T | Awaitable[T]]


class ReconcilerCollector(ABC):
    @abstractmethod
    def add_task[T](
        self,
        key: type[T],
        function: ReconcilerTaskFn[T],
        phase: ReconcilerRunPhase = ReconcilerRunPhase.Setup,
        restart_policy: RestartPolicy = RestartPolicy.Never,
        conditions: list[str] | None = None,
    ) -> bool: ...

    @abstractmethod
    def remove_task[T](
        self,
        key: type[T],
        function: ReconcilerTaskFn[T],
        phase: ReconcilerRunPhase = ReconcilerRunPhase.Setup,
    ) -> bool: ...


class TaskStatus(Enum):
    Pending = Unit()
    Scheduled = Struct(at=datetime)
    Running = Unit()
    Canceled = Struct(reason=str)
    Completed = Struct(result=Any)
    Failed = Struct(message=str, exc=Optional[Exception])  # noqa: UP045


class ReconcilerEventType(enum.IntEnum):
    INFO = enum.auto()
    WARN = enum.auto()
    OK = enum.auto()
    ERR = enum.auto()


@dataclass(slots=True, frozen=True, kw_only=True)
class ReconcilerEvent:
    type: ReconcilerEventType
    phase: ReconcilerRunPhase
    regarding: str | None = None
    action: str | None = None
    reason: str | None = None
    message: str
    reporter: str
    timestamp: datetime = field(default_factory=datetime.now)


class Task(ABC):
    @property
    @abstractmethod
    def status(self) -> TaskStatus: ...

    @property
    @abstractmethod
    def restart_policy(self) -> RestartPolicy: ...

    @property
    @abstractmethod
    def phase(self) -> ReconcilerRunPhase: ...

    @abstractmethod
    def events(self) -> Collection[ReconcilerEvent]: ...


class TaskHandler(ABC):
    @abstractmethod
    def add_event(self, event: ReconcilerEvent) -> None: ...

    @abstractmethod
    def set_condition(self, condition: Condition) -> bool: ...

    @abstractmethod
    def cancel(self, reason: str | None = None) -> None: ...

    @abstractmethod
    def complete[T](self, value: T | None = None) -> None: ...

    @abstractmethod
    def failure(self, message: str, exception: Exception | None = None) -> None: ...


class ReconcilerStatus(Enum):
    Dead = Unit()
    Alive = Struct(status=TransitionStatus)
    Succeeded = Struct(status=TransitionStatus)
    Failed = Struct(status=TransitionStatus, message=str)


class ReconcilerWaiter(Enum):
    Sync = Struct(value=threading.Event)
    Async = Struct(value=asyncio.Event)


class Reconciler[S](TypeWrapper[S], ABC):
    @property
    @abstractmethod
    def status(self) -> ReconcilerStatus: ...

    @property
    @abstractmethod
    def waiter(self) -> ReconcilerWaiter | None: ...

    @abstractmethod
    def set_resource_status(self, status: ResourceStatus) -> None: ...

    @abstractmethod
    def set_condition(self, condition: Condition) -> None: ...

    @abstractmethod
    def reset_condition(self, name: str) -> bool: ...

    @abstractmethod
    def events(self) -> Collection[ReconcilerEvent]: ...

    @abstractmethod
    def setup(self, task_collector: ReconcilerCollector) -> None | Awaitable[None]: ...

    @abstractmethod
    def teardown(self) -> None | Awaitable[None]: ...
