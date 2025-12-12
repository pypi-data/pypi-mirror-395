from __future__ import annotations

from collections.abc import AsyncGenerator, Generator
from decimal import Decimal
from enum import IntEnum, auto

from greyhorse.app.private.functional.context import BucketOperationContext
from greyhorse.app.private.functional.factory_storage import FactoryStorage
from greyhorse.factory import into_factory


def sync_ctx_manager() -> Generator[str, str, None]:
    res = '123'
    yield res
    assert res == '123'


async def async_ctx_manager() -> AsyncGenerator[Decimal, Decimal]:
    res = Decimal(789)
    yield res
    assert res == Decimal(789)


def complex_fn(a: int, b: str) -> Decimal:
    return Decimal(a) + Decimal(b)


class Level(IntEnum):
    ROOT = auto(0)
    FUNCTION = auto()
    LOCAL = auto()


def test_simple() -> None:
    registry = FactoryStorage()

    context = BucketOperationContext(registry)
    assert context.scope is None

    with context as selector:
        assert not selector.has(int)
        assert not selector.has(str)
        assert not selector.has(Decimal)

        assert registry.add_factory(int, into_factory(lambda: 123, int))
        assert registry.add_factory(str, into_factory(sync_ctx_manager))

        assert selector.has(int)
        assert selector.has(str)
        assert not selector.has(Decimal)

        assert selector.get(int).unwrap() == 123

        inner_context = context.advance()
        assert context is inner_context


def test_scoped() -> None:
    registry = FactoryStorage()

    context = BucketOperationContext(registry, Level)
    assert context.scope == Level.ROOT

    with context as selector:
        assert not selector.has(int)
        assert not selector.has(str)
        assert not selector.has(Decimal)

        assert registry.add_factory(int, into_factory(lambda: 123, int), scope=Level.ROOT)
        assert registry.add_factory(str, into_factory(sync_ctx_manager), scope=Level.ROOT)

        assert selector.has(int)
        assert selector.has(str)
        assert not selector.has(Decimal)

        assert selector.get(int).unwrap() == 123

        inner_context = context.advance()
        assert context is not inner_context

        with inner_context as inner_selector:
            assert inner_context.scope == Level.FUNCTION
            assert registry.add_factory(
                Decimal, into_factory(async_ctx_manager), scope=Level.FUNCTION
            )

            assert inner_selector.has(int)
            assert inner_selector.has(str)
            assert inner_selector.has(Decimal)

            assert registry.add_factory(int, into_factory(lambda: 456, int), scope=Level.LOCAL)

            inner_context2 = inner_context.advance()
            assert inner_context is not inner_context2

            with inner_context2 as inner_selector2:
                assert inner_context2.scope == Level.LOCAL
                assert inner_selector2.get(int).unwrap() == 456
                assert inner_selector2.get(str).unwrap() == '123'
                assert Decimal(789) == inner_selector2.get(Decimal).unwrap()

            with inner_context2 as inner_selector2:
                assert registry.add_factory(
                    Decimal, into_factory(complex_fn), scope=Level.LOCAL
                )
                assert Decimal(579) == inner_selector2.get(Decimal).unwrap()

        assert inner_selector.get(int).unwrap() == 123
        assert registry.remove_factory(Decimal, scope=Level.FUNCTION)

        assert registry.remove_factory(int, scope=Level.ROOT)

    with context as selector:
        assert not selector.has(int)
        assert selector.has(str)
        assert not selector.has(Decimal)
