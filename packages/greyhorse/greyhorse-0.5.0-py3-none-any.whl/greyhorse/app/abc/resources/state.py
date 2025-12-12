from abc import ABC, abstractmethod
from collections.abc import Awaitable

from greyhorse.result import Result

from ..collections.selectors import ListSelector
from .borrow import BorrowError, BorrowMutError
from .common import ResourceStatus, TransitionStatus


class BaseResource(ABC):
    @property
    @abstractmethod
    def status(self) -> ResourceStatus: ...

    @property
    @abstractmethod
    def transition_status(self) -> TransitionStatus: ...


class ResourceState[S](BaseResource, ABC):
    @property
    @abstractmethod
    def shared_type(self) -> type[S]: ...

    @property
    @abstractmethod
    def next_status(self) -> ResourceStatus | None: ...

    @abstractmethod
    def borrow(self) -> Result[S, BorrowError] | Awaitable[Result[S, BorrowError]]: ...

    @abstractmethod
    def reclaim(self) -> None | Awaitable[None]: ...


class MutResourceState[S, M](BaseResource, ABC):
    @property
    @abstractmethod
    def mut_type(self) -> type[M]: ...

    @property
    @abstractmethod
    def next_status(self) -> ResourceStatus | None: ...

    @abstractmethod
    def acquire(self) -> Result[M, BorrowMutError] | Awaitable[Result[M, BorrowMutError]]: ...

    @abstractmethod
    def release(self) -> None | Awaitable[None]: ...


ResourceSelector = ListSelector[type, ResourceState]
MutResourceSelector = ListSelector[type, MutResourceState]
