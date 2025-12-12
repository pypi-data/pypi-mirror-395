from collections.abc import Generator
from copy import deepcopy
from functools import partial
from unittest.mock import Mock

from faker import Faker

from greyhorse.app.abc.providers import BorrowError, BorrowMutError, ForwardError
from greyhorse.app.contexts import (
    MutCtxCallbacks,
    SyncContext,
    SyncMutCallbackContext,
    SyncMutContext,
)
from greyhorse.app.entities.boxes import CombinedBox, ForwardBox, MutBox, SharedBox


def test_shared() -> None:
    instance = SharedBox[int](lambda: 123)

    res = instance.borrow()
    assert res.is_ok()

    res = instance.borrow()
    assert res.is_ok()

    unwrapped = res.unwrap()
    assert unwrapped == 123
    instance.reclaim()
    instance.reclaim()


def test_mut() -> None:
    instance = MutBox[int](lambda: 123)

    res = instance.acquire()
    assert res.is_ok()
    unwrapped = res.unwrap()

    res = instance.acquire()
    assert res.is_err()
    assert res.unwrap_err() == BorrowMutError.AlreadyBorrowed(name='int')

    instance.release()

    res = instance.acquire()
    assert res.is_ok()
    assert unwrapped is res.unwrap()

    assert res.unwrap() == 123


def test_combined() -> None:
    instance = CombinedBox[int, str](lambda: 123, lambda: '123')

    res = instance.borrow()
    assert res.is_ok()

    res = instance.borrow()
    assert res.is_ok()

    unwrapped = res.unwrap()
    assert unwrapped == 123

    res = instance.acquire()
    assert res.is_err()
    assert res.unwrap_err() == BorrowMutError.BorrowedAsImmutable(name='str')

    instance.reclaim()
    instance.reclaim()

    res = instance.acquire()
    assert res.is_ok()

    unwrapped = res.unwrap()
    assert unwrapped == '123'

    res = instance.borrow()
    assert res.is_err()
    assert res.unwrap_err() == BorrowError.BorrowedAsMutable(name='int')

    instance.release()

    res = instance.borrow()
    assert res.is_ok()

    unwrapped = res.unwrap()
    assert unwrapped == 123


def test_shared_context() -> None:
    instance = SharedBox[SyncContext[int]](SyncContext[int](123))

    res = instance.borrow()
    assert res.is_ok()

    res = instance.borrow()
    assert res.is_ok()

    ctx = res.unwrap()
    assert isinstance(ctx, SyncContext)

    with ctx as data:
        assert data == 123


def test_mut_context() -> None:
    instance = MutBox[SyncContext[int]](SyncContext[int](123))

    res = instance.acquire()
    assert res.is_ok()
    unwrapped = res.unwrap()

    res = instance.acquire()
    assert res.is_err()
    assert res.unwrap_err() == BorrowMutError.AlreadyBorrowed(name='IntSyncContext')

    instance.release()

    res = instance.acquire()
    assert res.is_ok()
    assert unwrapped is res.unwrap()

    ctx = res.unwrap()
    assert isinstance(ctx, SyncContext)

    with ctx as data:
        assert data == 123


def test_combined_context() -> None:
    instance = CombinedBox[SyncContext[int], SyncContext[str]](
        SyncContext[int](123), SyncContext[str]('123')
    )

    res = instance.borrow()
    assert res.is_ok()

    res = instance.borrow()
    assert res.is_ok()

    ctx = res.unwrap()
    assert isinstance(ctx, SyncContext)

    with ctx as data:
        assert data == 123

    res = instance.acquire()
    assert res.is_err()
    assert res.unwrap_err() == BorrowMutError.BorrowedAsImmutable(name='StrSyncContext')

    instance.reclaim()
    instance.reclaim()

    res = instance.acquire()
    assert res.is_ok()

    mut_ctx = res.unwrap()
    assert isinstance(mut_ctx, SyncContext)

    with mut_ctx as data:
        assert data == '123'

    res = instance.borrow()
    assert res.is_err()
    assert res.unwrap_err() == BorrowError.BorrowedAsMutable(name='IntSyncContext')

    instance.release()

    res = instance.borrow()
    assert res.is_ok()

    ctx = res.unwrap()
    assert isinstance(ctx, SyncContext)

    with ctx as data:
        assert data == 123


def test_combined_context_read_write() -> None:
    value = {'counter': 1}

    instance = CombinedBox[SyncContext[int], SyncContext[str]](
        SyncContext[dict](partial(deepcopy, value)),
        SyncMutCallbackContext[dict](
            MutCtxCallbacks(on_apply=value.update), partial(deepcopy, value)
        ),
    )

    res = instance.borrow()
    assert res.is_ok()

    ctx = res.unwrap()
    assert isinstance(ctx, SyncContext)

    with ctx as data:
        assert data == {'counter': 1}

    instance.reclaim()

    res = instance.acquire()
    assert res.is_ok()

    mut_ctx = res.unwrap()
    assert isinstance(mut_ctx, SyncMutContext)

    with mut_ctx as data:
        assert data == {'counter': 1}
        data['counter'] += 1

    instance.release()

    res = instance.borrow()
    assert res.is_ok()

    ctx = res.unwrap()
    assert isinstance(ctx, SyncContext)

    with ctx as data:
        assert data == {'counter': 1}

    instance.reclaim()

    res = instance.acquire()
    assert res.is_ok()

    mut_ctx = res.unwrap()
    assert isinstance(mut_ctx, SyncMutContext)

    with mut_ctx as data:
        assert data == {'counter': 1}
        data['counter'] += 1
        mut_ctx.apply()

    instance.release()

    res = instance.borrow()
    assert res.is_ok()

    ctx = res.unwrap()
    assert isinstance(ctx, SyncContext)

    with ctx as data:
        assert data == {'counter': 2}


def test_shared_gen(faker: Faker) -> None:
    gen_mock = Mock()

    def gen() -> Generator[str, str, None]:
        gen_mock()
        yield faker.pystr()
        gen_mock()

    instance = SharedBox[str](gen)

    res = instance.borrow()
    assert res.is_ok()

    gen_mock.assert_called_once()
    gen_mock.reset_mock()

    unwrapped = res.unwrap()
    assert isinstance(unwrapped, str)

    res = instance.borrow()
    assert res.is_ok()

    gen_mock.assert_not_called()
    gen_mock.reset_mock()

    instance.reclaim()
    instance.reclaim()

    assert gen_mock.call_count == 1


def test_mut_gen(faker: Faker) -> None:
    gen_mock = Mock()

    def gen() -> Generator[str, str, None]:
        gen_mock()
        yield faker.pystr()
        gen_mock()

    instance = MutBox[str](gen)

    res = instance.acquire()
    assert res.is_ok()

    gen_mock.assert_called_once()
    gen_mock.reset_mock()

    unwrapped = res.unwrap()
    assert isinstance(unwrapped, str)

    res = instance.acquire()
    assert res.unwrap_err() == BorrowMutError.AlreadyBorrowed(name='str')

    gen_mock.assert_not_called()
    gen_mock.reset_mock()

    instance.release()
    instance.release()

    assert gen_mock.call_count == 1


def test_forward() -> None:
    instance = ForwardBox[int]()

    assert not instance

    res = instance.take()
    assert res.is_err()
    assert res.unwrap_err() == ForwardError.Empty(name='int')

    instance.accept(123)

    assert instance

    res = instance.take()
    assert res.is_ok()

    assert not instance

    unwrapped = res.unwrap()
    assert unwrapped == 123

    res = instance.take()
    assert res.is_err()
    assert res.unwrap_err() == ForwardError.Empty(name='int')

    instance.drop(unwrapped)
