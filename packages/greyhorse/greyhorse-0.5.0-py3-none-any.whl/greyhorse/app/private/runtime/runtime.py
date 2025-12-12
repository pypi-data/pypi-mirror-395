import asyncio
import sys
from asyncio import iscoroutine
from collections.abc import Callable
from typing import override

import greenback
from greenlet import getcurrent, greenlet

from greyhorse.app.abc.runtime.runtime import Runtime
from greyhorse.utils.types import is_awaitable


class _Greenlet(greenlet):
    __slots__ = ('main_context',)

    def __init__[T, **P](self, func: Callable[P, T], async_context: greenlet) -> None:
        greenlet.__init__(self, func, async_context)
        self.main_context = async_context


class SyncRuntime(Runtime):
    __slots__ = ('_counter', '_executor')

    def __init__(self) -> None:
        super().__init__(asyncio.new_event_loop())
        self._executor = _Greenlet(self._loop.run_forever, getcurrent())
        self._counter = 0

    @property
    @override
    def active(self) -> bool:
        return not self._executor.dead

    async def _loop_fn(self) -> None:
        result = self._executor.main_context.switch()

        while result != ():
            try:
                value = await result
            except BaseException:
                result = self._executor.main_context.throw(*sys.exc_info())
            else:
                result = self._executor.main_context.switch(value)

    @override
    def start(self) -> None:
        if self._counter == 0:
            self._loop.create_task(self._loop_fn())
            self._executor.switch()
        self._counter += 1

    @override
    def stop(self) -> None:
        if self._counter == 1:
            if not self._loop.is_closed():
                self._loop.call_soon_threadsafe(self._loop.stop)
            self._executor.switch()
            if not self._loop.is_closed():
                self._loop.close()

        self._counter = max(self._counter - 1, 0)

    @override
    def invoke_sync[T, **P](
        self, func: Callable[P, T], /, *args: P.args, **kwargs: P.kwargs
    ) -> T:
        if is_awaitable(func):
            if not self.active:
                return asyncio.run(func(*args, **kwargs))
            return self._executor.switch(func(*args, **kwargs))

        return func(*args, **kwargs)

    @override
    async def invoke_async[T, **P](
        self, func: Callable[P, T], /, *args: P.args, **kwargs: P.kwargs
    ) -> T:
        if is_awaitable(func):
            if iscoroutine(func):
                return await func  # type: ignore
            return await func(*args, **kwargs)

        context = _Greenlet(func, getcurrent())
        try:
            result = context.switch(*args, **kwargs)

            while not context.dead:
                try:
                    value = await result

                except BaseException:
                    result = context.throw(*sys.exc_info())
                else:
                    result = context.switch(value)
        finally:
            # clean up to avoid cycle resolution by gc
            del context.main_context

        return result


class AsyncRuntime(Runtime):
    __slots__ = ('_counter',)

    def __init__(self) -> None:
        super().__init__(asyncio.get_running_loop())
        self._counter = 0

    @property
    @override
    def active(self) -> bool:
        return self._loop.is_running()

    @override
    async def start(self) -> None:
        if self._counter == 0:
            await greenback.ensure_portal()
        self._counter += 1

    @override
    async def stop(self) -> None:
        self._counter = max(self._counter - 1, 0)

    @override
    def invoke_sync[T, **P](
        self, func: Callable[P, T], /, *args: P.args, **kwargs: P.kwargs
    ) -> T:
        if is_awaitable(func):
            return greenback.await_(func(*args, **kwargs))
        return func(*args, **kwargs)

    @override
    async def invoke_async[T, **P](
        self, func: Callable[P, T], /, *args: P.args, **kwargs: P.kwargs
    ) -> T:
        if is_awaitable(func):
            if iscoroutine(func):
                return await func  # type: ignore
            return await greenback.with_portal_run(func, *args, **kwargs)
        return await greenback.with_portal_run_sync(func, *args, **kwargs)


def get_runtime() -> Runtime:
    if Runtime._instance is not None:  # noqa: SLF001
        return Runtime._instance  # noqa: SLF001

    try:
        asyncio.get_running_loop()
        instance = AsyncRuntime()
    except RuntimeError:
        instance = SyncRuntime()

    Runtime._instance = instance  # noqa: SLF001
    return instance
