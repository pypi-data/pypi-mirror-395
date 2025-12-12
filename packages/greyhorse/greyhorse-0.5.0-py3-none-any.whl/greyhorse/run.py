import asyncio
from collections.abc import Awaitable, Callable
from functools import partial, wraps

from greyhorse.app.private.runtime.runtime import Runtime, get_runtime
from greyhorse.utils.types import is_awaitable


def wrap_sync[T, **P](
    func: Callable[P, Awaitable[T]], /, *args: P.args, **kwargs: P.kwargs
) -> T:
    runtime = get_runtime()
    runtime.start()
    try:
        return func(*args, **kwargs)
    finally:
        runtime.stop()
        Runtime._instance = None  # noqa: SLF001


async def wrap_async[T, **P](
    func: Callable[P, Awaitable[T]], /, *args: P.args, **kwargs: P.kwargs
) -> T:
    runtime = get_runtime()
    await runtime.start()
    try:
        return await func(*args, **kwargs)
    finally:
        await runtime.stop()
        Runtime._instance = None  # noqa: SLF001


def run[T, **P](func: Callable[P, T], /, *args: P.args, **kwargs: P.kwargs) -> T:
    if is_awaitable(func):
        asyncio.set_event_loop(asyncio.new_event_loop())
        return asyncio.run(wrap_async(func, *args, **kwargs))
    return wrap_sync(func, *args, **kwargs)


def main[T, **P](func: Callable[P, T] | None = None) -> Callable[P, T]:
    @wraps(func)
    def decorator[T, **P](func: Callable[P, T]) -> T:
        return partial(run, func)

    if func is None:
        return decorator

    return decorator(func)
