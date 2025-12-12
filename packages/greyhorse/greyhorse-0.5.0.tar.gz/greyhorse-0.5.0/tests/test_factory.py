from collections.abc import AsyncGenerator, Callable, Generator
from decimal import Decimal
from unittest.mock import Mock

import pytest
from faker import Faker

from greyhorse.factory import into_factory
from greyhorse.maybe import Maybe


def sync_simple_fn() -> int:
    return 123


async def async_simple_fn() -> int:
    return 123


def sync_complex_fn(a1: int, a2: str) -> Decimal:
    return Decimal(a1) + Decimal(a2)


async def async_complex_fn(a1: int, a2: str) -> Decimal:
    return Decimal(a1) + Decimal(a2)


def sync_ctx_fn(a1: int, a2: str) -> Generator[Decimal, Decimal, None]:
    res = Decimal(a1) + Decimal(a2)
    yield res
    assert res == Decimal(a1) + Decimal(a2)


async def async_ctx_fn(a1: int, a2: str) -> AsyncGenerator[Decimal, Decimal]:
    res = Decimal(a1) + Decimal(a2)
    yield res
    assert res == Decimal(a1) + Decimal(a2)


class A:
    pass


class B:
    def __init__(self, a: A) -> None:
        self.a = a


class C:
    def __init__(self, conf: str) -> None:
        self.conf = conf


class D:
    def __init__(self, a: A, b: Maybe[B], c: C | None) -> None:
        self.a = a
        self.b = b
        self.c = c


def test_instance() -> None:
    factory = into_factory('test')

    assert not factory.scoped
    assert factory.cacheable
    assert not factory.is_async

    assert factory.return_type is str
    assert factory.params_count == 0
    assert factory.args_count == 0
    assert factory.actual_params == {}

    assert factory.check_signature(Callable[[], str])
    assert factory.check_signature(Callable[[], object])

    res = factory.create()
    assert isinstance(res, str)
    assert res == 'test'


def test_classes() -> None:
    factory_a = into_factory(A)

    assert not factory_a.scoped
    assert factory_a.cacheable
    assert not factory_a.is_async

    assert factory_a.return_type is A
    assert factory_a.params_count == 0
    assert factory_a.args_count == 0
    assert factory_a.actual_params == {}

    assert factory_a.check_signature(Callable[[], A])
    assert factory_a.check_signature(Callable[[], object])

    res_a = factory_a.create()
    assert isinstance(res_a, A)

    factory_b = into_factory(B)

    assert not factory_b.scoped
    assert factory_b.cacheable
    assert not factory_b.is_async

    assert factory_b.return_type is B
    assert factory_b.params_count == 1
    assert factory_b.args_count == 0
    assert factory_b.actual_params == {'a': A}

    assert factory_b.has_named_param('a')
    assert factory_b.has_typed_param(A)

    assert factory_b.check_signature(Callable[[A], B])
    assert factory_b.check_signature(Callable[[A], object])

    res_b = factory_b.create(a=res_a)
    assert isinstance(res_b, B)
    assert res_b.a is res_a

    assert factory_b.add_typed_arg(A, res_a)

    assert factory_b.check_signature(Callable[[A], B])
    assert factory_b.check_signature(Callable[[A], object])
    assert factory_b.check_signature(Callable[[], B])
    assert factory_b.check_signature(Callable[[], object])

    res_b = factory_b.create()
    assert isinstance(res_b, B)
    assert res_b.a is res_a

    factory_c = into_factory(C)

    assert not factory_c.scoped
    assert factory_c.cacheable
    assert not factory_c.is_async

    assert factory_c.return_type is C
    assert factory_c.params_count == 1
    assert factory_c.args_count == 0
    assert factory_c.actual_params == {'conf': str}

    assert factory_c.has_named_param('conf')
    assert factory_c.has_typed_param(str)

    assert factory_c.check_signature(Callable[[str], C])
    assert not factory_c.check_signature(Callable[[], C])

    assert factory_c.add_named_arg('conf', 'test')
    assert factory_c.check_signature(Callable[[], C])

    res_c = factory_c.create()
    assert isinstance(res_c, C)
    assert res_c.conf == 'test'

    factory_d = into_factory(D)

    assert not factory_d.scoped
    assert factory_d.cacheable
    assert not factory_d.is_async

    assert factory_d.return_type is D
    assert factory_d.params_count == 3
    assert factory_d.args_count == 0
    assert factory_d.actual_params == {'a': A, 'b': Maybe[B], 'c': C | None}

    assert factory_d.has_named_param('a')
    assert factory_d.has_named_param('b')
    assert factory_d.has_named_param('c')
    assert factory_d.has_typed_param(A)
    assert factory_d.has_typed_param(B)
    assert factory_d.has_typed_param(C)

    assert factory_d.check_signature(Callable[[A, B, C], D])
    assert factory_d.check_signature(Callable[[A, B], D])
    assert factory_d.check_signature(Callable[[A, C], D])
    assert factory_d.check_signature(Callable[[A], D])
    assert factory_d.check_signature(Callable[[A, Maybe[B], C], D])
    assert factory_d.check_signature(Callable[[A, Maybe[B], C | None], D])
    assert factory_d.check_signature(Callable[[A, B, C | None], D])
    assert not factory_d.check_signature(Callable[[B, C | None], D])

    assert factory_d.add_named_arg('a', res_a)

    assert factory_d.check_signature(Callable[[B, C], D])
    assert factory_d.check_signature(Callable[[B], D])
    assert factory_d.check_signature(Callable[[C], D])
    assert factory_d.check_signature(Callable[[], D])
    assert factory_d.check_signature(Callable[[Maybe[B], C], D])
    assert factory_d.check_signature(Callable[[Maybe[B], C | None], D])
    assert factory_d.check_signature(Callable[[B, C | None], D])

    res_d = factory_d.create()
    assert isinstance(res_d, D)
    assert res_d.a is res_a
    assert res_d.b.is_nothing()
    assert res_d.c is None

    assert factory_d.add_typed_arg(B, res_b)

    assert factory_d.check_signature(Callable[[B, C], D])
    assert factory_d.check_signature(Callable[[B], D])
    assert factory_d.check_signature(Callable[[C], D])
    assert factory_d.check_signature(Callable[[], D])
    assert factory_d.check_signature(Callable[[Maybe[B], C], D])
    assert factory_d.check_signature(Callable[[Maybe[B], C | None], D])
    assert factory_d.check_signature(Callable[[B, C | None], D])

    res_d = factory_d.create()
    assert isinstance(res_d, D)
    assert res_d.a is res_a
    assert res_d.b.unwrap() is res_b
    assert res_d.c is None

    assert factory_d.add_typed_arg(C, res_c)

    assert factory_d.check_signature(Callable[[B, C], D])
    assert factory_d.check_signature(Callable[[B], D])
    assert factory_d.check_signature(Callable[[C], D])
    assert factory_d.check_signature(Callable[[], D])
    assert factory_d.check_signature(Callable[[Maybe[B], C], D])
    assert factory_d.check_signature(Callable[[Maybe[B], C | None], D])
    assert factory_d.check_signature(Callable[[B, C | None], D])

    res_d = factory_d.create()
    assert isinstance(res_d, D)
    assert res_d.a is res_a
    assert res_d.b.unwrap() is res_b
    assert res_d.c is res_c

    res_d = factory_d.create(res_b, res_c)
    assert isinstance(res_d, D)
    assert res_d.a is res_a
    assert res_d.b.unwrap() is res_b
    assert res_d.c is res_c

    res_d = factory_d.create(b=res_b, c=res_c)
    assert isinstance(res_d, D)
    assert res_d.a is res_a
    assert res_d.b.unwrap() is res_b
    assert res_d.c is res_c


@pytest.mark.parametrize(
    'param', ((sync_simple_fn, False), (async_simple_fn, True)), ids=('Sync', 'Async')
)
@pytest.mark.asyncio
async def test_simple_callable(param) -> None:  # noqa: ANN001
    orig_fn = param[0]
    is_async = param[1]

    factory = into_factory(orig_fn)

    assert not factory.scoped
    assert not factory.cacheable
    assert is_async == factory.is_async

    assert factory.return_type is int
    assert factory.params_count == 0
    assert factory.args_count == 0
    assert factory.actual_params == {}

    assert factory.check_signature(Callable[[], int])
    assert factory.check_signature(Callable[[], object])

    if not is_async:
        res = factory.create()
    else:
        res = await factory.create()

    assert isinstance(res, int)
    assert res == 123


@pytest.mark.parametrize(
    'param',
    (
        (sync_complex_fn, False, False),
        (async_complex_fn, True, False),
        (sync_ctx_fn, False, True),
        (async_ctx_fn, True, True),
    ),
    ids=('Sync', 'Async', 'SyncCtx', 'AsyncCtx'),
)
@pytest.mark.asyncio
async def test_complex_callable(param) -> None:  # noqa: ANN001
    orig_fn = param[0]
    is_async = param[1]
    is_scoped = param[2]

    factory = into_factory(orig_fn)

    assert not factory.cacheable
    assert is_scoped == factory.scoped
    assert is_async == factory.is_async

    assert factory.return_type is Decimal
    assert factory.params_count == 2
    assert factory.args_count == 0
    assert factory.actual_params == {'a1': int, 'a2': str}

    assert not factory.has_named_param('a0')
    assert factory.has_named_param('a1')
    assert factory.has_named_param('a2')

    assert not factory.has_typed_param(bool)
    assert factory.has_typed_param(int)
    assert factory.has_typed_param(str)

    assert factory.check_signature(Callable[[int, str], Decimal])

    if not is_async:
        res = factory.create(1, '2')
    else:
        res = await factory.create(1, '2')

    assert isinstance(res, Decimal)
    assert res == Decimal('3')

    if not is_async:
        factory.destroy(res)
    else:
        await factory.destroy(res)


@pytest.mark.parametrize(
    'param',
    (
        (sync_complex_fn, False, False),
        (async_complex_fn, True, False),
        (sync_ctx_fn, False, True),
        (async_ctx_fn, True, True),
    ),
    ids=('Sync', 'Async', 'SyncCtx', 'AsyncCtx'),
)
@pytest.mark.asyncio
async def test_complex_override(param) -> None:  # noqa: ANN001
    orig_fn = param[0]
    is_async = param[1]

    factory = into_factory(orig_fn)

    assert not factory.check_signature(Callable[[], int])
    assert not factory.check_signature(Callable[[], Decimal])
    assert not factory.check_signature(Callable[[int], Decimal])
    assert not factory.check_signature(Callable[[str], Decimal])
    assert factory.check_signature(Callable[[int, str], Decimal])

    assert factory.args_count == 0
    assert factory.actual_params == {'a1': int, 'a2': str}

    assert not factory.add_named_arg('a0', 123)
    assert not factory.add_typed_arg(bool, True)

    assert factory.add_named_arg('a1', 123)
    assert factory.args_count == 1
    assert factory.actual_params == {'a2': str}

    assert not factory.check_signature(Callable[[], Decimal])
    assert not factory.check_signature(Callable[[int], Decimal])
    assert factory.check_signature(Callable[[str], Decimal])
    assert factory.check_signature(Callable[[int, str], Decimal])

    assert factory.add_typed_arg(str, '456')
    assert factory.args_count == 2
    assert factory.actual_params == {}

    assert factory.check_signature(Callable[[], Decimal])
    assert factory.check_signature(Callable[[int], Decimal])
    assert factory.check_signature(Callable[[str], Decimal])
    assert factory.check_signature(Callable[[int, str], Decimal])

    if not is_async:
        res = factory.create()
    else:
        res = await factory.create()

    assert isinstance(res, Decimal)
    assert res == Decimal('579')

    if not is_async:
        factory.destroy(res)
    else:
        await factory.destroy(res)

    if not is_async:
        res = factory.create(a2='789')
    else:
        res = await factory.create(a2='789')

    assert isinstance(res, Decimal)
    assert res == Decimal('912')

    if not is_async:
        factory.destroy(res)
    else:
        await factory.destroy(res)

    assert factory.remove_typed_arg(int)
    assert factory.args_count == 1
    assert factory.actual_params == {'a1': int}

    assert not factory.check_signature(Callable[[], Decimal])
    assert factory.check_signature(Callable[[int], Decimal])
    assert not factory.check_signature(Callable[[str], Decimal])
    assert factory.check_signature(Callable[[int, str], Decimal])

    assert factory.remove_named_arg('a2')
    assert factory.args_count == 0
    assert factory.actual_params == {'a1': int, 'a2': str}

    assert not factory.check_signature(Callable[[], Decimal])
    assert not factory.check_signature(Callable[[int], Decimal])
    assert not factory.check_signature(Callable[[str], Decimal])
    assert factory.check_signature(Callable[[int, str], Decimal])

    assert not factory.remove_named_arg('a0')
    assert not factory.remove_typed_arg(bool)


def test_sync_scope(faker: Faker) -> None:
    gen_mock = Mock()

    def gen() -> Generator[str, str, None]:
        gen_mock()
        yield faker.pystr()
        gen_mock()

    factory = into_factory(gen)
    assert factory.scoped
    assert factory.return_type is str
    assert not factory.is_async

    factory.destroy(factory.create())

    assert gen_mock.call_count == 2


@pytest.mark.asyncio
async def test_async_scope(faker: Faker) -> None:
    gen_mock = Mock()

    async def gen() -> AsyncGenerator[str, str, None]:
        gen_mock()
        yield faker.pystr()
        gen_mock()

    factory = into_factory(gen)
    assert factory.scoped
    assert factory.return_type is str
    assert factory.is_async

    await factory.destroy(await factory.create())

    assert gen_mock.call_count == 2
