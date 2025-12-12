from __future__ import annotations

import asyncio
import threading
from abc import ABC, abstractmethod
from collections.abc import Awaitable, Callable, Mapping
from contextlib import (
    AbstractAsyncContextManager,
    AbstractContextManager,
    AsyncExitStack,
    ExitStack,
    suppress,
)
from dataclasses import dataclass, field
from types import TracebackType
from typing import Any, override
from uuid import uuid4

from greyhorse.app.private.runtime.invoke import (
    invoke_async,
    invoke_sync,
    is_like_async_context_manager,
    is_like_sync_context_manager,
)
from greyhorse.enum import Enum, Struct, Unit
from greyhorse.factory import Factory, FactoryFn, into_factory
from greyhorse.utils.types import TypeWrapper


type FieldFactory[T] = (
    T
    | Callable[[], Awaitable[T] | T]
    | AbstractContextManager[T]
    | AbstractAsyncContextManager[T]
    | Callable[[], AbstractContextManager[T]]
    | Callable[[], AbstractAsyncContextManager[T]]
)


type ContextManagerLike[T] = (
    AbstractContextManager[T]
    | AbstractAsyncContextManager[T]
    | Callable[[], AbstractContextManager[T]]
    | Callable[[], AbstractAsyncContextManager[T]]
)


class ContextState[T](Enum):
    Idle = Unit()
    InUse = Struct(count=int, value=T)
    Applied = Struct(count=int, value=T)
    Cancelled = Struct(count=int, value=T)


@dataclass(slots=True, frozen=True, kw_only=True)
class ContextData[T]:
    factory: Factory[T]
    ident: str = field(default_factory=lambda: str(uuid4()))
    field_factories: dict[str, FieldFactory[Any]] = field(default_factory=dict)
    finalizers: list[Callable[[], Awaitable[None] | None]] = field(default_factory=list)


class InvalidContextStateError(RuntimeError):
    pass


class Context:
    __slots__ = ('_data', '_state')

    def __init__(
        self,
        factory: Factory[Any] | FactoryFn[Any],
        fields: Mapping[str, FieldFactory[Any]] | None = None,
        finalizers: list[Callable[[], Awaitable[None] | None]] | None = None,
    ) -> None:
        self._state = ContextState[Any].Idle
        if not isinstance(factory, Factory):
            factory = into_factory(factory)
        self._data = ContextData(
            factory=factory, field_factories=fields or {}, finalizers=finalizers or []
        )

    @property
    def ident(self) -> str:
        return self._data.ident

    @property
    def state(self) -> ContextState:
        return self._state

    def __enter__(self) -> object:
        raise NotImplementedError

    def __exit__(
        self,
        exc_type: type[BaseException] | None = None,
        exc_value: BaseException | None = None,
        traceback: TracebackType | None = None,
    ) -> None:
        raise NotImplementedError

    async def __aenter__(self) -> object:
        raise NotImplementedError

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None = None,
        exc_value: BaseException | None = None,
        traceback: TracebackType | None = None,
    ) -> None:
        raise NotImplementedError

    def children(self) -> list[Context]:
        raise NotImplementedError


class MutContext(Context, ABC):
    @abstractmethod
    def apply(self) -> Awaitable[None] | None: ...

    @abstractmethod
    def cancel(self) -> Awaitable[None] | None: ...

    @abstractmethod
    def mut_children(self) -> list[MutContext]: ...


class SyncContext[T](Context, TypeWrapper[T], AbstractContextManager):
    __slots__ = ('_children', '_lock', '_stack', '_sub_contexts')

    def __init__(
        self,
        factory: Factory[T] | FactoryFn[T],
        fields: dict[str, FieldFactory[T]] | None = None,
        finalizers: list[Callable[[], Awaitable[None] | None]] | None = None,
        sub_contexts: list[ContextManagerLike[T]] | None = None,
    ) -> None:
        fields = fields.copy() if fields else {}
        self._stack = ExitStack()
        self._lock = threading.Lock()
        self._children: list[SyncContext] = []
        self._sub_contexts: list[tuple[ContextManagerLike, str | None]] = []

        if sub_contexts:
            for ctx in sub_contexts:
                if isinstance(ctx, SyncContext):
                    self._children.append(ctx)
                if is_like_sync_context_manager(ctx):
                    self._sub_contexts.append((ctx, None))

        names_to_remove = set()

        for name, value in fields.items():
            if isinstance(value, SyncContext):
                self._children.append(value)
                names_to_remove.add(name)
            if is_like_sync_context_manager(value):
                self._sub_contexts.append((value, name))
                names_to_remove.add(name)
            elif is_like_async_context_manager(value):
                names_to_remove.add(name)

        for name in names_to_remove:
            fields.pop(name)

        super().__init__(factory, fields, finalizers)

    @override
    def children(self) -> list[Context]:
        return self._children.copy()

    def _switch_to_use(self) -> T:
        self._stack.__enter__()
        kwargs: dict[str, Any] = {}

        for ctx, field in self._sub_contexts:
            if callable(ctx):
                ctx = ctx()
            if (value := self._stack.enter_context(ctx)) and field is not None:
                kwargs[field] = value

        for name, value in self._data.field_factories.items():
            if callable(value):
                value = invoke_sync(value)
            kwargs[name] = value

        return self._create(**kwargs)

    def _switch_to_idle(
        self,
        instance: T,
        exc_type: type[BaseException] | None = None,
        exc_value: BaseException | None = None,
        traceback: TracebackType | None = None,
    ) -> None:
        with suppress(Exception):
            self._destroy(instance)

        for finalizer in self._data.finalizers:
            with suppress(Exception):
                invoke_sync(finalizer)

        # with suppress(Exception):
        self._stack.__exit__(exc_type, exc_value, traceback)

    def _create(self, **kwargs: Any) -> T:
        return invoke_sync(self._data.factory, **kwargs)

    def _destroy(self, instance: T) -> None:
        invoke_sync(self._data.factory.destroy, instance)

    def _enter(self, instance: T) -> T:
        return instance

    def _exit(
        self,
        instance: T,
        exc_type: type[BaseException] | None = None,
        exc_value: BaseException | None = None,
        traceback: TracebackType | None = None,
    ) -> None:
        pass

    def _nested_enter(self, instance: T) -> T:
        return instance

    def _nested_exit(
        self,
        instance: T,
        exc_type: type[BaseException] | None = None,
        exc_value: BaseException | None = None,
        traceback: TracebackType | None = None,
    ) -> None:
        pass

    @override
    def __enter__(self) -> T:
        with self._lock:
            match self._state:
                case ContextState.Idle:
                    value = self._switch_to_use()
                    self._state = ContextState[self.wrapped_type].InUse(count=1, value=value)
                    return self._enter(value)

                case (
                    ContextState.InUse(count, value)
                    | ContextState.Applied(count, value)
                    | ContextState.Cancelled(count, value)
                ):
                    self._state = self._state.__class__(count=count + 1, value=value)
                    return self._nested_enter(value)

    @override
    def __exit__(
        self,
        exc_type: type[BaseException] | None = None,
        exc_value: BaseException | None = None,
        traceback: TracebackType | None = None,
    ) -> None:
        with self._lock:
            match self._state:
                case ContextState.Idle:
                    raise InvalidContextStateError('Context exit on idle state')

                case (
                    ContextState.InUse(count, value)
                    | ContextState.Applied(count, value)
                    | ContextState.Cancelled(count, value)
                ):
                    if count > 1:
                        self._nested_exit(value, exc_type, exc_value, traceback)
                        self._state = self._state.__class__(count=count - 1, value=value)
                    else:
                        self._exit(value, exc_type, exc_value, traceback)
                        self._switch_to_idle(value, exc_type, exc_value, traceback)
                        self._state = ContextState[self.wrapped_type].Idle


class SyncMutContext[T](SyncContext[T], MutContext):
    __slots__ = ('_auto_apply', '_force_rollback', '_mut_children')

    def __init__(
        self,
        factory: Factory[T] | FactoryFn[T],
        fields: dict[str, FieldFactory[T]] | None = None,
        finalizers: list[Callable[[], Awaitable[None] | None]] | None = None,
        sub_contexts: list[ContextManagerLike[T]] | None = None,
        force_rollback: bool = False,
        auto_apply: bool = False,
    ) -> None:
        super().__init__(factory, fields, finalizers, sub_contexts)
        self._mut_children = []
        self._force_rollback = force_rollback
        self._auto_apply = auto_apply

        for child in self._children:
            if isinstance(child, SyncMutContext):
                self._mut_children.append(child)

    @override
    def mut_children(self) -> list[MutContext]:
        return self._mut_children.copy()

    def _apply(self, instance: T) -> None:
        pass

    def _cancel(self, instance: T) -> None:
        pass

    @override
    def apply(self) -> None:
        with self._lock:
            self._do_apply()

    @override
    def cancel(self) -> None:
        with self._lock:
            self._do_cancel()

    @override
    def _exit(
        self,
        instance: T,
        exc_type: type[BaseException] | None = None,
        exc_value: BaseException | None = None,
        traceback: TracebackType | None = None,
    ) -> None:
        if self._force_rollback or exc_type is not None:
            self._do_cancel()
        elif self._auto_apply:
            self._do_apply()

    def _do_apply(self) -> None:
        match self._state:
            case ContextState.Idle:
                raise InvalidContextStateError('MutContext apply on idle state')

            case ContextState.InUse(count, value):
                for child in self._mut_children:
                    child.apply()
                self._apply(value)
                self._state = ContextState[self.wrapped_type].Applied(count=count, value=value)

            case ContextState.Applied(_, _):
                pass

            case ContextState.Cancelled(_, _):
                raise InvalidContextStateError('MutContext apply on cancelled state')

    def _do_cancel(self) -> None:
        match self._state:
            case ContextState.Idle:
                raise InvalidContextStateError('MutContext cancel on idle state')

            case ContextState.InUse(count, value):
                for child in self._mut_children:
                    child.cancel()
                self._cancel(value)
                self._state = ContextState[self.wrapped_type].Cancelled(
                    count=count, value=value
                )

            case ContextState.Applied(_, _):
                raise InvalidContextStateError('MutContext cancel on applied state')

            case ContextState.Cancelled(_, _):
                pass


class AsyncContext[T](Context, TypeWrapper[T], AbstractAsyncContextManager):
    __slots__ = ('_children', '_lock', '_stack', '_sub_contexts')

    def __init__(
        self,
        factory: Factory[T] | FactoryFn[T],
        fields: dict[str, FieldFactory[T]] | None = None,
        finalizers: list[Callable[[], Awaitable[None] | None]] | None = None,
        sub_contexts: list[ContextManagerLike[T]] | None = None,
    ) -> None:
        fields = fields.copy() if fields else {}
        self._stack = AsyncExitStack()
        self._lock = asyncio.Lock()
        self._children: list[Context] = []
        self._sub_contexts: list[tuple[ContextManagerLike[T], bool, str | None]] = []

        if sub_contexts:
            for ctx in sub_contexts:
                if isinstance(ctx, SyncContext):
                    self._children.append(ctx)
                    self._sub_contexts.append((ctx, False, None))
                elif isinstance(ctx, AsyncContext):
                    self._children.append(ctx)
                    self._sub_contexts.append((ctx, True, None))
                elif is_like_sync_context_manager(ctx):
                    self._sub_contexts.append((ctx, False, None))
                elif is_like_async_context_manager(ctx):
                    self._sub_contexts.append((ctx, True, None))

        names_to_remove = set()

        for name, value in fields.items():
            if isinstance(value, SyncContext):
                self._children.append(value)
                self._sub_contexts.append((value, False, name))
                names_to_remove.add(name)
            elif isinstance(value, AsyncContext):
                self._children.append(value)
                self._sub_contexts.append((value, True, name))
                names_to_remove.add(name)
            elif is_like_sync_context_manager(value):
                self._sub_contexts.append((value, False, name))
                names_to_remove.add(name)
            elif is_like_async_context_manager(value):
                self._sub_contexts.append((value, True, name))
                names_to_remove.add(name)

        for name in names_to_remove:
            fields.pop(name)

        super().__init__(factory, fields, finalizers)

    @override
    def children(self) -> list[Context]:
        return self._children.copy()

    async def _switch_to_use(self) -> T:
        await self._stack.__aenter__()
        kwargs: dict[str, Any] = {}

        for ctx, is_async, field in self._sub_contexts:
            if callable(ctx):
                ctx = ctx()
            if is_async:
                value = await self._stack.enter_async_context(ctx)
            else:
                value = self._stack.enter_context(ctx)

            if value is not None and field is not None:
                kwargs[field] = value

        for name, value in self._data.field_factories.items():
            if callable(value):
                value = await invoke_async(value)
            kwargs[name] = value

        return await self._create(**kwargs)

    async def _switch_to_idle(
        self,
        instance: T,
        exc_type: type[BaseException] | None = None,
        exc_value: BaseException | None = None,
        traceback: TracebackType | None = None,
    ) -> None:
        with suppress(Exception):
            await self._destroy(instance)

        for finalizer in self._data.finalizers:
            with suppress(Exception):
                await invoke_async(finalizer)

        # with suppress(Exception):
        await self._stack.__aexit__(exc_type, exc_value, traceback)

    async def _create(self, **kwargs: Any) -> T:
        return await invoke_async(self._data.factory, **kwargs)

    async def _destroy(self, instance: T) -> None:
        await invoke_async(self._data.factory.destroy, instance)

    async def _enter(self, instance: T) -> T:
        return instance

    async def _exit(
        self,
        instance: T,
        exc_type: type[BaseException] | None = None,
        exc_value: BaseException | None = None,
        traceback: TracebackType | None = None,
    ) -> None:
        pass

    async def _nested_enter(self, instance: T) -> T:
        return instance

    async def _nested_exit(
        self,
        instance: T,
        exc_type: type[BaseException] | None = None,
        exc_value: BaseException | None = None,
        traceback: TracebackType | None = None,
    ) -> None:
        pass

    @override
    async def __aenter__(self) -> T:
        async with self._lock:
            match self._state:
                case ContextState.Idle:
                    value = await self._switch_to_use()
                    self._state = ContextState[self.wrapped_type].InUse(count=1, value=value)
                    return await self._enter(value)

                case (
                    ContextState.InUse(count, value)
                    | ContextState.Applied(count, value)
                    | ContextState.Cancelled(count, value)
                ):
                    self._state = self._state.__class__(count=count + 1, value=value)
                    return await self._nested_enter(value)

    @override
    async def __aexit__(
        self,
        exc_type: type[BaseException] | None = None,
        exc_value: BaseException | None = None,
        traceback: TracebackType | None = None,
    ) -> None:
        async with self._lock:
            match self._state:
                case ContextState.Idle:
                    raise InvalidContextStateError('Context exit on idle state')

                case (
                    ContextState.InUse(count, value)
                    | ContextState.Applied(count, value)
                    | ContextState.Cancelled(count, value)
                ):
                    if count > 1:
                        await self._nested_exit(value, exc_type, exc_value, traceback)
                        self._state = self._state.__class__(count=count - 1, value=value)
                    else:
                        await self._exit(value, exc_type, exc_value, traceback)
                        await self._switch_to_idle(value, exc_type, exc_value, traceback)
                        self._state = ContextState[self.wrapped_type].Idle


class AsyncMutContext[T](AsyncContext[T], MutContext):
    __slots__ = ('_auto_apply', '_force_rollback', '_mut_children')

    def __init__(
        self,
        factory: Factory[T] | FactoryFn[T],
        fields: dict[str, FieldFactory[T]] | None = None,
        finalizers: list[Callable[[], Awaitable[None] | None]] | None = None,
        sub_contexts: list[ContextManagerLike[T]] | None = None,
        force_rollback: bool = False,
        auto_apply: bool = False,
    ) -> None:
        super().__init__(factory, fields, finalizers, sub_contexts)
        self._mut_children: list[MutContext] = []
        self._force_rollback = force_rollback
        self._auto_apply = auto_apply

        for child in self._children:
            if isinstance(child, (SyncMutContext, AsyncMutContext)):
                self._mut_children.append(child)

    @override
    def mut_children(self) -> list[MutContext]:
        return self._mut_children.copy()

    async def _apply(self, instance: T) -> None:
        pass

    async def _cancel(self, instance: T) -> None:
        pass

    @override
    async def apply(self) -> None:
        async with self._lock:
            await self._do_apply()

    @override
    async def cancel(self) -> None:
        async with self._lock:
            await self._do_cancel()

    @override
    async def _exit(
        self,
        instance: T,
        exc_type: type[BaseException] | None = None,
        exc_value: BaseException | None = None,
        traceback: TracebackType | None = None,
    ) -> None:
        if self._force_rollback or exc_type is not None:
            await self._do_cancel()
        elif self._auto_apply:
            await self._do_apply()

    async def _do_apply(self) -> None:
        match self._state:
            case ContextState.Idle:
                raise InvalidContextStateError('MutContext apply on idle state')

            case ContextState.InUse(count, value):
                for child in self._mut_children:
                    await invoke_async(child.apply)

                await self._apply(value)
                self._state = ContextState[self.wrapped_type].Applied(count=count, value=value)

            case ContextState.Applied(_, _):
                pass

            case ContextState.Cancelled(_, _):
                raise InvalidContextStateError('MutContext apply on cancelled state')

    async def _do_cancel(self) -> None:
        match self._state:
            case ContextState.Idle:
                raise InvalidContextStateError('MutContext cancel on idle state')

            case ContextState.InUse(count, value):
                for child in self._mut_children:
                    await invoke_async(child.cancel)

                await self._cancel(value)
                self._state = ContextState[self.wrapped_type].Cancelled(
                    count=count, value=value
                )

            case ContextState.Applied(_, _):
                raise InvalidContextStateError('MutContext cancel on applied state')

            case ContextState.Cancelled(_, _):
                pass


@dataclass(frozen=True, slots=True, kw_only=True)
class CtxCallbacks:
    before_create: Callable[..., Any] | None = None
    after_create: Callable[[Any], Any] | None = None
    before_destroy: Callable[[Any], Any] | None = None
    after_destroy: Callable[[], Any] | None = None
    on_enter: Callable[[Any], Any] | None = None
    on_exit: (
        Callable[
            [Any, type[BaseException] | None, BaseException | None, TracebackType | None], Any
        ]
        | None
    ) = None
    on_nested_enter: Callable[[Any], Any] | None = None
    on_nested_exit: (
        Callable[
            [Any, type[BaseException] | None, BaseException | None, TracebackType | None], Any
        ]
        | None
    ) = None


@dataclass(frozen=True, slots=True, kw_only=True)
class MutCtxCallbacks(CtxCallbacks):
    on_apply: Callable[[Any], Any] | None = None
    on_cancel: Callable[[Any], Any] | None = None


class SyncCallbackContext[T](SyncContext[T]):
    __slots__ = ('_callbacks',)

    def __init__(
        self,
        callbacks: CtxCallbacks,
        factory: Factory[T] | FactoryFn[T],
        fields: dict[str, FieldFactory[T]] | None = None,
        finalizers: list[Callable[[], Awaitable[None] | None]] | None = None,
        sub_contexts: list[ContextManagerLike[T]] | None = None,
    ) -> None:
        super().__init__(factory, fields, finalizers, sub_contexts)
        self._callbacks = callbacks

    @override
    def _create(self, **kwargs: Any) -> T:
        if self._callbacks.before_create is not None:
            self._callbacks.before_create(**kwargs)
        instance = super()._create(**kwargs)
        if self._callbacks.after_create is not None:
            self._callbacks.after_create(instance)
        return instance

    @override
    def _destroy(self, instance: T) -> None:
        if self._callbacks.before_destroy is not None:
            self._callbacks.before_destroy(instance)
        super()._destroy(instance)
        if self._callbacks.after_destroy is not None:
            self._callbacks.after_destroy()

    @override
    def _enter(self, instance: T) -> T:
        if self._callbacks.on_enter is not None:
            return self._callbacks.on_enter(instance)
        return instance

    @override
    def _exit(
        self,
        instance: T,
        exc_type: type[BaseException] | None = None,
        exc_value: BaseException | None = None,
        traceback: TracebackType | None = None,
    ) -> None:
        if self._callbacks.on_exit is not None:
            self._callbacks.on_exit(instance, exc_type, exc_value, traceback)

    @override
    def _nested_enter(self, instance: T) -> T:
        if self._callbacks.on_nested_enter is not None:
            return self._callbacks.on_nested_enter(instance)
        return instance

    @override
    def _nested_exit(
        self,
        instance: T,
        exc_type: type[BaseException] | None = None,
        exc_value: BaseException | None = None,
        traceback: TracebackType | None = None,
    ) -> None:
        if self._callbacks.on_nested_exit is not None:
            self._callbacks.on_nested_exit(instance, exc_type, exc_value, traceback)


class SyncMutCallbackContext[T](SyncMutContext[T]):
    __slots__ = ('_callbacks',)

    def __init__(
        self,
        callbacks: MutCtxCallbacks,
        factory: Factory[T] | FactoryFn[T],
        fields: dict[str, FieldFactory[T]] | None = None,
        finalizers: list[Callable[[], Awaitable[None] | None]] | None = None,
        sub_contexts: list[ContextManagerLike[T]] | None = None,
        force_rollback: bool = False,
        auto_apply: bool = False,
    ) -> None:
        super().__init__(factory, fields, finalizers, sub_contexts, force_rollback, auto_apply)
        self._callbacks = callbacks

    @override
    def _create(self, **kwargs: Any) -> T:
        if self._callbacks.before_create is not None:
            self._callbacks.before_create(**kwargs)
        instance = super()._create(**kwargs)
        if self._callbacks.after_create is not None:
            self._callbacks.after_create(instance)
        return instance

    @override
    def _destroy(self, instance: T) -> None:
        if self._callbacks.before_destroy is not None:
            self._callbacks.before_destroy(instance)
        super()._destroy(instance)
        if self._callbacks.after_destroy is not None:
            self._callbacks.after_destroy()

    @override
    def _enter(self, instance: T) -> T:
        if self._callbacks.on_enter is not None:
            return self._callbacks.on_enter(instance)
        return instance

    @override
    def _exit(
        self,
        instance: T,
        exc_type: type[BaseException] | None = None,
        exc_value: BaseException | None = None,
        traceback: TracebackType | None = None,
    ) -> None:
        if self._callbacks.on_exit is not None:
            self._callbacks.on_exit(instance, exc_type, exc_value, traceback)

    @override
    def _nested_enter(self, instance: T) -> T:
        if self._callbacks.on_nested_enter is not None:
            self._callbacks.on_nested_enter(instance)
        return instance

    @override
    def _nested_exit(
        self,
        instance: T,
        exc_type: type[BaseException] | None = None,
        exc_value: BaseException | None = None,
        traceback: TracebackType | None = None,
    ) -> None:
        if self._callbacks.on_nested_exit is not None:
            self._callbacks.on_nested_exit(instance, exc_type, exc_value, traceback)

    @override
    def _apply(self, instance: T) -> None:
        if self._callbacks.on_apply is not None:
            self._callbacks.on_apply(instance)

    @override
    def _cancel(self, instance: T) -> None:
        if self._callbacks.on_cancel is not None:
            self._callbacks.on_cancel(instance)


class AsyncCallbackContext[T](AsyncContext[T]):
    __slots__ = ('_callbacks',)

    def __init__(
        self,
        callbacks: CtxCallbacks,
        factory: Factory[T] | FactoryFn[T],
        fields: dict[str, FieldFactory[T]] | None = None,
        finalizers: list[Callable[[], Awaitable[None] | None]] | None = None,
        sub_contexts: list[ContextManagerLike[T]] | None = None,
    ) -> None:
        super().__init__(factory, fields, finalizers, sub_contexts)
        self._callbacks = callbacks

    @override
    async def _create(self, **kwargs: Any) -> T:
        if self._callbacks.before_create is not None:
            self._callbacks.before_create(**kwargs)
        instance = await super()._create(**kwargs)
        if self._callbacks.after_create is not None:
            self._callbacks.after_create(instance)
        return instance

    @override
    async def _destroy(self, instance: T) -> None:
        if self._callbacks.before_destroy is not None:
            self._callbacks.before_destroy(instance)
        await super()._destroy(instance)
        if self._callbacks.after_destroy is not None:
            self._callbacks.after_destroy()

    @override
    async def _enter(self, instance: T) -> T:
        if self._callbacks.on_enter is not None:
            return self._callbacks.on_enter(instance)
        return instance

    @override
    async def _exit(
        self,
        instance: T,
        exc_type: type[BaseException] | None = None,
        exc_value: BaseException | None = None,
        traceback: TracebackType | None = None,
    ) -> None:
        if self._callbacks.on_exit is not None:
            self._callbacks.on_exit(instance, exc_type, exc_value, traceback)

    @override
    async def _nested_enter(self, instance: T) -> T:
        if self._callbacks.on_nested_enter is not None:
            return self._callbacks.on_nested_enter(instance)
        return instance

    @override
    async def _nested_exit(
        self,
        instance: T,
        exc_type: type[BaseException] | None = None,
        exc_value: BaseException | None = None,
        traceback: TracebackType | None = None,
    ) -> None:
        if self._callbacks.on_nested_exit is not None:
            self._callbacks.on_nested_exit(instance, exc_type, exc_value, traceback)


class AsyncMutCallbackContext[T](AsyncMutContext[T]):
    __slots__ = ('_callbacks',)

    def __init__(
        self,
        callbacks: MutCtxCallbacks,
        factory: Factory[T] | FactoryFn[T],
        fields: dict[str, FieldFactory[T]] | None = None,
        finalizers: list[Callable[[], Awaitable[None] | None]] | None = None,
        sub_contexts: list[ContextManagerLike[T]] | None = None,
        force_rollback: bool = False,
        auto_apply: bool = False,
    ) -> None:
        super().__init__(factory, fields, finalizers, sub_contexts, force_rollback, auto_apply)
        self._callbacks = callbacks

    @override
    async def _create(self, **kwargs: Any) -> T:
        if self._callbacks.before_create is not None:
            self._callbacks.before_create(**kwargs)
        instance = await super()._create(**kwargs)
        if self._callbacks.after_create is not None:
            self._callbacks.after_create(instance)
        return instance

    @override
    async def _destroy(self, instance: T) -> None:
        if self._callbacks.before_destroy is not None:
            self._callbacks.before_destroy(instance)
        await super()._destroy(instance)
        if self._callbacks.after_destroy is not None:
            self._callbacks.after_destroy()

    @override
    async def _enter(self, instance: T) -> T:
        if self._callbacks.on_enter is not None:
            return self._callbacks.on_enter(instance)
        return instance

    @override
    async def _exit(
        self,
        instance: T,
        exc_type: type[BaseException] | None = None,
        exc_value: BaseException | None = None,
        traceback: TracebackType | None = None,
    ) -> None:
        if self._callbacks.on_exit is not None:
            self._callbacks.on_exit(instance, exc_type, exc_value, traceback)

    @override
    async def _nested_enter(self, instance: T) -> T:
        if self._callbacks.on_nested_enter is not None:
            self._callbacks.on_nested_enter(instance)
        return instance

    @override
    async def _nested_exit(
        self,
        instance: T,
        exc_type: type[BaseException] | None = None,
        exc_value: BaseException | None = None,
        traceback: TracebackType | None = None,
    ) -> None:
        if self._callbacks.on_nested_exit is not None:
            self._callbacks.on_nested_exit(instance, exc_type, exc_value, traceback)

    @override
    async def _apply(self, instance: T) -> None:
        if self._callbacks.on_apply is not None:
            self._callbacks.on_apply(instance)

    @override
    async def _cancel(self, instance: T) -> None:
        if self._callbacks.on_cancel is not None:
            self._callbacks.on_cancel(instance)


class ContextBuilder[T](TypeWrapper[T]):
    def __init__[**P](
        self,
        factory: Factory[T] | FactoryFn[T],
        fields: dict[str, FieldFactory[T]] | None = None,
        finalizers: list[Callable[[], Awaitable[None] | None]] | None = None,
        sub_contexts: list[ContextManagerLike[T]] | None = None,
        **kwargs: dict[str, Any],
    ) -> None:
        self._factory = factory
        self._fields = fields or {}
        self._finalizers = finalizers or []
        self._sub_contexts = sub_contexts or []
        self._kwargs = kwargs

    def add_param(self, name: str, value: FieldFactory[T]) -> None:
        self._fields[name] = value

    def add_sub_context(self, context: ContextManagerLike[T]) -> None:
        self._sub_contexts.append(context)

    def add_finalizer(self, finalizer: Callable[[], Awaitable[None] | None]) -> None:
        self._finalizers.append(finalizer)

    def build(self) -> T:
        return self.wrapped_type(
            factory=self._factory,
            fields=self._fields,
            finalizers=self._finalizers,
            sub_contexts=self._sub_contexts,
            **self._kwargs,
        )

    def __class_getitem__[C: SyncContext | AsyncContext | SyncMutContext | AsyncMutContext](
        cls, args: tuple[type[C], type[T]]
    ) -> ContextBuilder:
        class_, type_ = args
        return super().__class_getitem__(class_[type_])
