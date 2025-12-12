from abc import abstractmethod
from collections.abc import Awaitable
from typing import Protocol

from greyhorse.error import Error, ErrorCase
from greyhorse.result import Result

from .resources.borrow import BorrowError, BorrowMutError


class Provider[T](Protocol):
    @abstractmethod
    def borrow(self) -> Result[T, BorrowError] | Awaitable[Result[T, BorrowError]]: ...

    @abstractmethod
    def reclaim(self) -> None | Awaitable[None]: ...


class MutProvider[T](Protocol):
    @abstractmethod
    def acquire(self) -> Result[T, BorrowMutError] | Awaitable[Result[T, BorrowMutError]]: ...

    @abstractmethod
    def release(self) -> None | Awaitable[None]: ...


class ForwardError(Error):
    namespace = 'greyhorse.app'

    Empty = ErrorCase(
        msg='Cannot forward "{name}" because the value is not available', name=str
    )

    MovedOut = ErrorCase(
        msg='Cannot forward "{name}" because the value was moved out', name=str
    )

    Unexpected = ErrorCase(
        msg='Cannot forward "{name}" because an unexpected error occurred: "{details}"',
        name=str,
        details=str,
    )

    # InsufficientDeps = ErrorCase(
    #     msg='Cannot forward "{name}" because dependencies are not enough to satisfy', name=str
    # )


class ForwardProvider[T](Protocol):
    @abstractmethod
    def take(self) -> Result[T, ForwardError] | Awaitable[Result[T, ForwardError]]: ...

    @abstractmethod
    def drop(self, instance: T) -> None | Awaitable[None]: ...

    @abstractmethod
    def __bool__(self) -> bool | Awaitable[bool]: ...


AnyProvider = Provider | MutProvider | ForwardProvider
