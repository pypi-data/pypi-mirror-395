import asyncio
import time

import pytest

from greyhorse.app.private.runtime.runtime import Runtime, get_runtime


def sync_fn(runtime: Runtime, counter: int) -> list[int]:
    if counter == 0:
        return [0]

    res = runtime.invoke_sync(async_fn, runtime, counter - 1)
    return [*res, counter]


async def async_fn(runtime: Runtime, counter: int) -> list[int]:
    if counter == 0:
        return [0]

    res = await runtime.invoke_async(sync_fn, runtime, counter - 1)
    return [*res, counter]


def test_runtime_sync() -> None:
    runtime = get_runtime()
    counter = 250

    res = runtime.invoke_sync(async_fn, runtime, counter)
    assert list(range(0, counter + 1)) == res


@pytest.mark.asyncio
async def test_runtime_async() -> None:
    runtime = get_runtime()
    counter = 250

    res = await runtime.invoke_async(async_fn, runtime, counter)
    assert list(range(0, counter + 1)) == res


if __name__ == '__main__':
    t1 = time.perf_counter()
    test_runtime_sync()
    t2 = time.perf_counter()
    print(f'Sync runtime takes {t2 - t1:.03} secs')

    t1 = time.perf_counter()
    asyncio.run(test_runtime_async())
    t2 = time.perf_counter()
    print(f'Async runtime takes {t2 - t1:.03} secs')
