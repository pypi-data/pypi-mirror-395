from __future__ import annotations

from collections import defaultdict
from collections.abc import AsyncGenerator, Generator, Mapping, Sequence
from dataclasses import dataclass, field
from decimal import Decimal
from enum import IntEnum, auto
from types import TracebackType
from typing import Any, Self, override

from greyhorse.app.abc.collections.selectors import Selector
from greyhorse.app.contexts import CtxCallbacks, SyncCallbackContext, SyncContext
from greyhorse.app.private.collections.registries import MutDictRegistry
from greyhorse.app.private.runtime.invoke import invoke_sync
from greyhorse.factory import Factory, into_factory
from greyhorse.maybe import Just, Maybe, Nothing
from greyhorse.utils.types import (
    TypeWrapper,
    is_maybe,
    is_optional,
    unwrap_maybe,
    unwrap_optional,
)


@dataclass(slots=True, frozen=True, kw_only=True)
class _Get[T]:
    instance: T
    cached: bool
    metadata: Mapping[str, Any] = field(default_factory=dict)


class Container[T: IntEnum](Selector[type, Any], TypeWrapper[T]):
    __slots__ = (
        '_cache',
        '_ctx',
        '_current_level',
        '_parent',
        '_resources',
        '_scoped_factories',
        '_selectors',
    )

    def __init__(
        self,
        selectors: Sequence[Selector[type, Factory[Any]]],
        current_level: T | None = None,
        parent: Container | None = None,
        resources: dict[type, Any] | None = None,
    ) -> None:
        self._selectors = selectors
        self._current_level = current_level if current_level else self.wrapped_type(0)
        self._parent = parent
        self._resources = MutDictRegistry[type, Any]()
        self._cache = MutDictRegistry[type, Any]()
        self._scoped_factories: dict[type, list[tuple[Factory[Any], Any]]] = defaultdict(list)

        if resources:
            for k, v in resources.items():
                self._resources.add(k, v)

        self._ctx = self._create_ctx()

    def __repr__(self) -> str:
        return f'Container <{self._current_level.name}>'

    @property
    def parent(self) -> Container | None:
        return self._parent

    @property
    def level(self) -> T:
        return self._current_level

    @property
    def context(self) -> SyncContext[Container]:
        return self._ctx

    @override
    def has[T](self, key: type[T]) -> bool:
        if self._cache.has(key) or self._get_registry().has(key):
            return True
        if self._parent is not None:
            return self._parent.has(key)
        return False

    @override
    def get[T](self, key: type[T]) -> Maybe[T]:
        return self._get(key).map(lambda x: x.instance)

    @override
    def get_with_metadata[T](self, key: type[T]) -> Maybe[tuple[T, Mapping[str, Any]]]:
        return self._get(key).map(lambda x: (x.instance, x.metadata))

    def __call__(
        self, resources: dict[type, Any] | None = None, scope: T | None = None
    ) -> SyncContext[Container]:
        if scope is not None:
            if scope <= self._current_level:
                return self.context
            if scope >= self._current_level + len(self._selectors):
                return self.context

        child = self

        if scope is None:
            for cur_level in range(self._current_level, len(self.wrapped_type) + 1):
                level_idx = cur_level - self._current_level
                if level_idx < 1:
                    continue
                if level_idx < len(self._selectors):
                    child = Container[self.wrapped_type](
                        self._selectors[level_idx:],
                        self.wrapped_type(cur_level),
                        parent=child,
                        resources=resources,
                    )
                    break
                # if not cur_level.autocreate:
                #     break
        else:
            for cur_level in range(self._current_level, len(self.wrapped_type) + 1):
                level_idx = cur_level - self._current_level
                if level_idx < 1:
                    continue
                if child.level >= scope:
                    break
                if level_idx < len(self._selectors):
                    child = Container[self.wrapped_type](
                        self._selectors[level_idx:],
                        self.wrapped_type(cur_level),
                        parent=child,
                        resources=resources,
                    )

        return child.context

    def _get_registry(self) -> Selector[type, Factory[Any]]:
        return self._selectors[0]

    def _get[T](self, key: type[T]) -> Maybe[_Get[T]]:
        if res := self._cache.get_with_metadata(key):
            instance, metadata = res.unwrap()
            return Just(_Get(instance=instance, cached=True, metadata=metadata))

        if res := self._get_registry().get_with_metadata(key):
            factory, metadata = res.unwrap()

            kwargs = {}
            for param_name, param_type in factory.actual_params.items():
                stripped_param_type = unwrap_maybe(unwrap_optional(param_type))

                if res := self._get(stripped_param_type):
                    res = res.unwrap()

                    kwargs[param_name] = (
                        Just(res.instance) if is_maybe(param_type) else res.instance
                    )
                elif is_maybe(param_type):
                    kwargs[param_name] = Nothing
                elif is_optional(param_type):
                    kwargs[param_name] = None

            instance = invoke_sync(factory.create, **kwargs)

            if factory.scoped:
                self._scoped_factories[key].append((factory, instance))
            if factory.cacheable:
                self._cache.add(key, instance, **metadata)

            return Just(_Get(instance=instance, cached=factory.cacheable, metadata=metadata))

        if not self._parent:
            return Nothing

        if not (res := self._parent._get(key)):  # noqa: SLF001
            return Nothing

        res = res.unwrap()
        if res.cached:
            self._cache.add(key, res.instance, **res.metadata)
        return Just(res)

    def _enter(self, _) -> Self:  # noqa: ANN001
        if self._parent:
            self._parent.context.__enter__()

        for k, v in self._resources.list():
            self._cache.add(k, v)

        return self

    def _exit(
        self,
        _,  # noqa: ANN001
        exc_type: type[BaseException] | None = None,
        exc_value: BaseException | None = None,
        traceback: TracebackType | None = None,
    ) -> None:
        while key := next(reversed(self._scoped_factories), None):
            for factory, instance in reversed(self._scoped_factories[key]):
                invoke_sync(factory.destroy, instance)
            del self._scoped_factories[key]

        self._cache.clear()

        if self._parent:
            self._parent.context.__exit__(exc_type, exc_value, traceback)

    def _create_ctx(self) -> SyncContext[Container]:
        return SyncCallbackContext[Container](
            callbacks=CtxCallbacks(on_enter=self._enter, on_exit=self._exit),
            factory=lambda *_: self,
        )


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


def test_container() -> None:
    registries = [MutDictRegistry[type, Any]() for _ in range(0, len(Level))]

    container = Container[Level](registries)
    assert container.level == Level.ROOT

    assert not container.has(int)
    assert not container.has(str)
    assert not container.has(Decimal)

    assert registries[Level.ROOT].add(int, into_factory(lambda: 123))
    assert registries[Level.ROOT].add(str, into_factory(sync_ctx_manager))

    assert container.has(int)
    assert container.has(str)
    assert not container.has(Decimal)

    assert container.get(int).unwrap() == 123

    with container.context:
        assert container.level == Level.ROOT

        with container() as c1:
            assert c1.level == Level.FUNCTION
            assert registries[Level.FUNCTION].add(Decimal, into_factory(async_ctx_manager))

            assert c1.has(int)
            assert c1.has(str)
            assert c1.has(Decimal)

            assert registries[Level.LOCAL].add(int, into_factory(lambda: 456))

            with c1() as c2:
                assert c2.level == Level.LOCAL
                assert c2.get(int).unwrap() == 456
                assert c2.get(str).unwrap() == '123'
                assert Decimal(789) == c2.get(Decimal).unwrap()

                assert registries[Level.LOCAL].add(Decimal, into_factory(complex_fn))
                assert Decimal(579) == c2.get(Decimal).unwrap()

        assert container.get(int).unwrap() == 123
        assert registries[Level.FUNCTION].remove(Decimal)

    assert registries[Level.ROOT].remove(int)

    assert not container.has(int)
    assert container.has(str)
    assert not container.has(Decimal)
