import asyncio
from abc import ABC, abstractmethod
from collections.abc import Awaitable, Callable


class Runtime(ABC):
    __slots__ = ('_loop',)

    _instance: 'Runtime' = None

    def __init__(self, loop: asyncio.AbstractEventLoop) -> None:
        self._loop = loop

    @property
    def loop(self) -> asyncio.AbstractEventLoop:
        return self._loop

    @property
    @abstractmethod
    def active(self) -> bool: ...

    @abstractmethod
    def start(self) -> None | Awaitable[None]: ...

    @abstractmethod
    def stop(self) -> None | Awaitable[None]: ...

    @abstractmethod
    def invoke_sync[T, **P](
        self, func: Callable[P, T], /, *args: P.args, **kwargs: P.kwargs
    ) -> T: ...

    @abstractmethod
    async def invoke_async[T, **P](
        self, func: Callable[P, T], /, *args: P.args, **kwargs: P.kwargs
    ) -> T: ...
