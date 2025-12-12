from __future__ import annotations

import builtins
import contextlib
import enum
import inspect
from abc import ABC, abstractmethod
from collections.abc import AsyncGenerator, Awaitable, Callable, Generator, Mapping
from dataclasses import dataclass, replace
from functools import partial, reduce
from typing import Any, Optional, get_type_hints, override

from greyhorse.maybe import Maybe
from greyhorse.utils.types import (
    TypeWrapper,
    is_awaitable,
    is_maybe,
    is_optional,
    unwrap_maybe,
    unwrap_optional,
)


type FactoryFn[T] = (
    Callable[..., T]
    | Callable[..., Awaitable[T]]
    | type[T]
    | T
    | Callable[..., Generator[T, T, None]]
    | Callable[..., AsyncGenerator[T, T]]
)


class CachePolicy(enum.IntEnum):
    VOLATILE = enum.auto(0)
    GRAPH = enum.auto()
    ANY = enum.auto()


class ParamOpt(int, enum.Enum):
    NORMAL = 0
    OPTIONAL = 1
    MAYBE = 2


@dataclass(slots=True, frozen=True, kw_only=True)
class ParamData:
    type: type
    name: str
    optional: ParamOpt
    value: Any | None = None

    @property
    def is_required(self) -> bool:
        return self.optional == ParamOpt.NORMAL

    @property
    def raw_type(self) -> builtins.type:
        match self.optional:
            case ParamOpt.NORMAL:
                return self.type
            case ParamOpt.OPTIONAL:
                return Optional[self.type]  # noqa: UP045
            case ParamOpt.MAYBE:
                return Maybe[self.type]

    @classmethod
    def from_kv(cls, k: str, v: type, value: Any | None = None) -> ParamData:
        opt = (
            ParamOpt.OPTIONAL
            if is_optional(v)
            else ParamOpt.MAYBE
            if is_maybe(v)
            else ParamOpt.NORMAL
        )
        return cls(type=unwrap_maybe(unwrap_optional(v)), name=k, optional=opt, value=value)


class Factory[T](TypeWrapper[T], ABC):
    __slots__ = ('_cache_policy', '_name_map', '_params', '_type_map')

    scoped: bool = False
    is_async: bool = False

    def __init__(
        self,
        params: Mapping[str, type],
        args: Mapping[str, Any] | None = None,
        cache_policy: CachePolicy = CachePolicy.VOLATILE,
    ) -> None:
        args = args or {}
        params_data = [ParamData.from_kv(k, v, args.get(k)) for k, v in params.items()]
        self._params: list[ParamData] = params_data
        self._name_map = {pd.name: i for i, pd in enumerate(self._params)}
        self._type_map = {pd.type: i for i, pd in enumerate(self._params)}
        self._cache_policy = cache_policy

    @property
    def cache_policy(self) -> CachePolicy:
        return self._cache_policy

    @property
    def cacheable(self) -> bool:
        return self._cache_policy > 0

    @abstractmethod
    def create[**P](self, *args: P.args, **kwargs: P.kwargs) -> T | Awaitable[T]: ...

    @abstractmethod
    def destroy(self, instance: T) -> None | Awaitable[None]: ...

    def __call__[**P](self, *args: P.args, **kwargs: P.kwargs) -> T | Awaitable[T]:
        return self.create(*args, **kwargs)

    def clone(self) -> Factory[T]:
        instance = type(self)({})
        self._clone_into(instance)
        return instance

    @abstractmethod
    def __eq__(self, other: Factory[T]) -> bool: ...

    @abstractmethod
    def __hash__(self) -> int: ...

    @property
    def return_type(self) -> type[T]:
        return self.__wrapped_type__

    @property
    def params_count(self) -> int:
        return len(self._params)

    # @property
    # def params_types(self) -> tuple[type, ...]:
    #     return tuple(pd.raw_type for pd in self._params if pd.value is None)

    @property
    def args_count(self) -> int:
        return reduce(lambda a, pd: a + (1 if pd.value is not None else 0), self._params, 0)

    @property
    def all_params(self) -> Mapping[str, type]:
        res = {}
        for pd in self._params:
            res[pd.name] = pd.raw_type
        return res

    @property
    def actual_params(self) -> Mapping[str, type]:
        res = {}
        for pd in self._params:
            if pd.value is None:
                res[pd.name] = pd.raw_type
        return res

    def check_signature(self, signature: type[Callable]) -> bool:
        sig_ret_type = signature.__args__[-1]
        sig_params = signature.__args__[0 : len(signature.__args__) - 1]

        if not issubclass(self.return_type, sig_ret_type):
            return False

        sig_params_idx = 0

        for pd in self._params:
            if sig_params_idx < len(sig_params):
                sig_param_type = sig_params[sig_params_idx]
                fit = False

                match pd.optional:
                    case ParamOpt.NORMAL:
                        if inspect.isclass(sig_param_type):
                            fit = issubclass(sig_param_type, pd.type)
                        else:
                            fit = sig_param_type is pd.type
                    case ParamOpt.OPTIONAL:
                        fit = issubclass(unwrap_optional(sig_param_type), pd.type)
                    case ParamOpt.MAYBE:
                        fit = issubclass(unwrap_maybe(sig_param_type), pd.type)

                if fit:
                    sig_params_idx += 1
                    continue

            if pd.value is None and pd.optional == ParamOpt.NORMAL:
                return False

        return sig_params_idx == len(sig_params)

    def has_named_param(self, name: str) -> bool:
        return name in self._name_map

    def has_typed_param[U](self, key: type[U]) -> bool:
        return key in self._type_map

    def add_named_arg[U](self, name: str, value: U) -> bool:
        if name not in self._name_map:
            return False
        idx = self._name_map[name]
        if self._params[idx].value is value:
            return False
        # if self._params[idx].optional == _ParamOpt.MAYBE:
        #     value = Maybe(value)
        self._params[idx] = replace(self._params[idx], value=value)
        return True

    def remove_named_arg(self, name: str) -> bool:
        if name not in self._name_map:
            return False
        idx = self._name_map[name]
        self._params[idx] = replace(self._params[idx], value=None)
        return True

    def add_typed_arg[U](self, key: type[U], value: U) -> bool:
        if key not in self._type_map:
            return False
        idx = self._type_map[key]
        if self._params[idx].value is value:
            return False
        # if self._params[idx].optional == _ParamOpt.MAYBE:
        #     value = Maybe(value)
        self._params[idx] = replace(self._params[idx], value=value)
        return True

    def remove_typed_arg[U](self, key: type[U]) -> bool:
        if key not in self._type_map:
            return False
        idx = self._type_map[key]
        self._params[idx] = replace(self._params[idx], value=None)
        return True

    def _clone_into(self, other: Factory[T]) -> None:
        other._params = self._params.copy()
        other._name_map = self._name_map.copy()
        other._type_map = self._type_map.copy()
        other._cache_policy = self._cache_policy

    def _prepare_kwargs[**P](self, *args: P.args, **kwargs: P.kwargs) -> dict[str, Any]:
        prepared_kwargs = {}
        args_idx = 0

        for pd in self._params:
            if args_idx < len(args):
                arg_value = args[args_idx]
                arg_type = type(arg_value)
                fit = False

                match pd.optional:
                    case ParamOpt.NORMAL:
                        fit = issubclass(arg_type, pd.type)
                    case ParamOpt.OPTIONAL:
                        fit = issubclass(unwrap_optional(arg_type), pd.type)
                    case ParamOpt.MAYBE:
                        fit = issubclass(unwrap_maybe(arg_type), pd.type)
                        arg_value = Maybe(arg_value)

                if fit:
                    prepared_kwargs[pd.name] = arg_value
                    args_idx += 1
                    continue

            match pd.optional:
                case ParamOpt.NORMAL:
                    if pd.name in kwargs:
                        prepared_kwargs[pd.name] = kwargs[pd.name]
                    elif pd.value is not None:
                        prepared_kwargs[pd.name] = pd.value
                case ParamOpt.OPTIONAL:
                    prepared_kwargs[pd.name] = kwargs.get(pd.name, pd.value)
                case ParamOpt.MAYBE:
                    if pd.name in kwargs:
                        prepared_kwargs[pd.name] = Maybe(kwargs[pd.name])
                    else:
                        prepared_kwargs[pd.name] = Maybe(pd.value)

        return prepared_kwargs

    @classmethod
    def from_syncfn(
        cls,
        fn: Callable[..., T],
        cache_policy: CachePolicy | None = None,
        hints: Mapping[str, Any] | None = None,
    ) -> Factory[T]:
        if not hints:
            hints = get_type_hints(strip_partial(fn), localns={'T': cls.__wrapped_type__})
        return_type = hints.pop('return', cls.__wrapped_type__)
        kwargs = {'cache_policy': cache_policy} if cache_policy is not None else {}
        return _SyncFnFactory[return_type](fn, hints, **kwargs)

    @classmethod
    def from_asyncfn(
        cls,
        fn: Callable[..., Awaitable[T]],
        cache_policy: CachePolicy | None = None,
        hints: Mapping[str, Any] | None = None,
    ) -> Factory[T]:
        if not hints:
            hints = get_type_hints(strip_partial(fn), localns={'T': cls.__wrapped_type__})
        return_type = hints.pop('return', cls.__wrapped_type__)
        kwargs = {'cache_policy': cache_policy} if cache_policy is not None else {}
        return _AsyncFnFactory[return_type](fn, hints, **kwargs)

    @classmethod
    def from_class(
        cls,
        cls_: type[T],
        cache_policy: CachePolicy | None = None,
        hints: Mapping[str, Any] | None = None,
    ) -> Factory[T]:
        if not hints:
            hints = get_type_hints(cls_.__init__, localns={'T': cls.__wrapped_type__})
        hints.pop('return', None)
        kwargs = {'cache_policy': cache_policy} if cache_policy is not None else {}
        return _ClassFactory[cls_](cls_, hints, **kwargs)

    @classmethod
    def from_instance(cls, instance: T) -> Factory[T]:
        instance_type = type(instance)
        return _InstanceFactory[instance_type](instance)

    @classmethod
    def from_syncgen(
        cls,
        gen_fn: Callable[..., Generator[T, T, None]],
        cache_policy: CachePolicy | None = None,
        hints: Mapping[str, Any] | None = None,
    ) -> Factory[T]:
        if not hints:
            hints = get_type_hints(strip_partial(gen_fn), localns={'T': cls.__wrapped_type__})
        return_type = hints.pop('return', cls.__wrapped_type__)
        if hasattr(return_type, '__origin__') and hasattr(return_type, '__args__'):
            match return_type.__origin__.__name__:
                case 'Generator' | 'Iterator' | 'Iterable':
                    return_type = return_type.__args__[0]
        kwargs = {'cache_policy': cache_policy} if cache_policy is not None else {}
        return _SyncGenFactory[return_type](gen_fn, hints, **kwargs)

    @classmethod
    def from_asyncgen(
        cls,
        gen_fn: Callable[..., AsyncGenerator[T, T]],
        cache_policy: CachePolicy | None = None,
        hints: Mapping[str, Any] | None = None,
    ) -> Factory[T]:
        if not hints:
            hints = get_type_hints(strip_partial(gen_fn), localns={'T': cls.__wrapped_type__})
        return_type = hints.pop('return', cls.__wrapped_type__)
        if hasattr(return_type, '__origin__') and hasattr(return_type, '__args__'):
            match return_type.__origin__.__name__:
                case 'AsyncGenerator' | 'AsyncIterator' | 'AsyncIterable':
                    return_type = return_type.__args__[0]
        kwargs = {'cache_policy': cache_policy} if cache_policy is not None else {}
        return _AsyncGenFactory[return_type](gen_fn, hints, **kwargs)


def into_factory[T](
    fn: FactoryFn[T],
    return_hint: type[T] | None = None,
    cache_policy: CachePolicy | None = None,
) -> Factory[T]:
    orig_fn = strip_partial(fn)
    return_hint = return_hint if return_hint is not None else type

    if callable(fn):
        unwrapped_fn = inspect.unwrap(orig_fn)

        if inspect.isgeneratorfunction(unwrapped_fn):
            return Factory[return_hint].from_syncgen(fn, cache_policy)
        if inspect.isasyncgenfunction(unwrapped_fn):
            return Factory[return_hint].from_asyncgen(fn, cache_policy)
        if inspect.isfunction(orig_fn) or inspect.ismethod(orig_fn):
            if is_awaitable(orig_fn):
                return Factory[return_hint].from_asyncfn(fn, cache_policy)
            return Factory[return_hint].from_syncfn(fn, cache_policy)
    if inspect.isclass(orig_fn):
        return Factory[return_hint].from_class(fn, cache_policy)
    return Factory[return_hint].from_instance(fn)


def strip_partial[T](fn: FactoryFn[T]) -> FactoryFn[T]:
    orig_fn = fn
    while isinstance(orig_fn, partial):
        orig_fn = orig_fn.func
    return orig_fn


class _SyncFnFactory[T](Factory[T]):
    __slots__ = ('_fn',)

    def __init__(
        self,
        fn: Callable[..., T],
        params: Mapping[str, type],
        args: Mapping[str, Any] | None = None,
        cache_policy: CachePolicy = CachePolicy.VOLATILE,
    ) -> None:
        super().__init__(params, args, cache_policy)
        self._fn = fn

    @override
    def create[**P](self, *args: P.args, **kwargs: P.kwargs) -> T:
        prepared_kwargs = self._prepare_kwargs(*args, **kwargs)
        return self._fn(**prepared_kwargs)

    @override
    def destroy(self, instance: T) -> None:
        del instance

    @override
    def clone(self) -> Factory[T]:
        instance = type(self)(self._fn, {})
        self._clone_into(instance)
        return instance

    @override
    def __eq__(self, other: Factory[T]) -> bool:
        return isinstance(other, _SyncFnFactory) and self._fn == other._fn

    @override
    def __hash__(self) -> int:
        return hash(self._fn)


class _AsyncFnFactory[T](Factory[T]):
    __slots__ = ('_fn',)

    is_async = True

    def __init__(
        self,
        fn: Callable[..., Awaitable[T]],
        params: Mapping[str, type],
        args: Mapping[str, Any] | None = None,
        cache_policy: CachePolicy = CachePolicy.VOLATILE,
    ) -> None:
        super().__init__(params, args, cache_policy)
        self._fn = fn

    @override
    async def create[**P](self, *args: P.args, **kwargs: P.kwargs) -> T:
        prepared_kwargs = self._prepare_kwargs(*args, **kwargs)
        return await self._fn(**prepared_kwargs)

    @override
    async def destroy(self, instance: T) -> None:
        del instance

    @override
    async def __call__[**P](self, *args: P.args, **kwargs: P.kwargs) -> T:
        return await self.create(*args, **kwargs)

    @override
    def clone(self) -> Factory[T]:
        instance = type(self)(self._fn, {})
        self._clone_into(instance)
        return instance

    @override
    def __eq__(self, other: Factory[T]) -> bool:
        return isinstance(other, _AsyncFnFactory) and self._fn == other._fn

    @override
    def __hash__(self) -> int:
        return hash(self._fn)


class _ClassFactory[T](Factory[T]):
    __slots__ = ('_cls',)

    def __init__(
        self,
        cls: type[T],
        params: Mapping[str, type],
        args: Mapping[str, Any] | None = None,
        cache_policy: CachePolicy = CachePolicy.GRAPH,
    ) -> None:
        super().__init__(params, args, cache_policy)
        self._cls = cls

    @override
    def create[**P](self, *args: P.args, **kwargs: P.kwargs) -> T:
        prepared_kwargs = self._prepare_kwargs(*args, **kwargs)
        return self._cls(**prepared_kwargs)

    @override
    def destroy(self, instance: T) -> None:
        del instance

    @override
    def clone(self) -> Factory[T]:
        instance = type(self)(self._cls, {})
        self._clone_into(instance)
        return instance

    @override
    def __eq__(self, other: Factory[T]) -> bool:
        return isinstance(other, _ClassFactory) and self._cls == other._cls

    @override
    def __hash__(self) -> int:
        return hash(self._cls)


class _InstanceFactory[T](Factory[T]):
    __slots__ = ('_instance',)

    def __init__(self, instance: T) -> None:
        super().__init__({}, None, CachePolicy.ANY)
        self._instance = instance

    @override
    def create[**P](self, *args: P.args, **kwargs: P.kwargs) -> T:
        return self._instance

    @override
    def destroy(self, instance: T) -> None: ...

    @override
    def clone(self) -> Factory[T]:
        instance = type(self)(self._instance)
        self._clone_into(instance)
        return instance

    @override
    def __eq__(self, other: Factory[T]) -> bool:
        return isinstance(other, _InstanceFactory) and self._instance == other._instance

    @override
    def __hash__(self) -> int:
        return hash(self._instance)


class _SyncGenFactory[T](Factory[T]):
    __slots__ = ('_gen_fn', '_gens')

    scoped = True

    def __init__(
        self,
        generator_fn: Callable[..., Generator[T, T, None]],
        params: Mapping[str, type],
        args: Mapping[str, Any] | None = None,
        cache_policy: CachePolicy = CachePolicy.VOLATILE,
    ) -> None:
        super().__init__(params, args, cache_policy)
        self._gen_fn = generator_fn
        self._gens: dict[int, Generator[T, T, None]] = {}

    @override
    def create[**P](self, *args: P.args, **kwargs: P.kwargs) -> T:
        prepared_kwargs = self._prepare_kwargs(*args, **kwargs)
        gen = self._gen_fn(**prepared_kwargs)

        try:
            instance = next(gen)

        except StopIteration as e:
            instance = e.value

        self._gens[id(instance)] = gen
        return instance

    @override
    def destroy(self, instance: T) -> None:
        key = id(instance)
        if not (gen := self._gens.pop(key, None)):
            return

        with contextlib.suppress(StopIteration):
            gen.send(instance)

    @override
    def clone(self) -> Factory[T]:
        instance = type(self)(self._gen_fn, {})
        self._clone_into(instance)
        return instance

    @override
    def __eq__(self, other: Factory[T]) -> bool:
        return isinstance(other, _SyncGenFactory) and self._gen_fn == other._gen_fn

    @override
    def __hash__(self) -> int:
        return hash(self._gen_fn)


class _AsyncGenFactory[T](Factory[T]):
    __slots__ = ('_gen_fn', '_gens')

    scoped = True
    is_async = True

    def __init__(
        self,
        generator_fn: Callable[..., AsyncGenerator[T, T]],
        params: Mapping[str, type],
        args: Mapping[str, Any] | None = None,
        cache_policy: CachePolicy = CachePolicy.VOLATILE,
    ) -> None:
        super().__init__(params, args, cache_policy)
        self._gen_fn = generator_fn
        self._gens: dict[int, AsyncGenerator[T, T]] = {}

    @override
    async def create[**P](self, *args: P.args, **kwargs: P.kwargs) -> T:
        prepared_kwargs = self._prepare_kwargs(*args, **kwargs)
        gen = self._gen_fn(**prepared_kwargs)

        try:
            instance = await anext(gen)

        except StopAsyncIteration:
            instance = None

        self._gens[id(instance)] = gen
        return instance

    @override
    async def destroy(self, instance: T) -> None:
        key = id(instance)
        if not (gen := self._gens.pop(key, None)):
            return

        with contextlib.suppress(StopAsyncIteration):
            await gen.asend(instance)

    @override
    async def __call__[**P](self, *args: P.args, **kwargs: P.kwargs) -> T:
        return await self.create(*args, **kwargs)

    @override
    def clone(self) -> Factory[T]:
        instance = type(self)(self._gen_fn, {})
        self._clone_into(instance)
        return instance

    @override
    def __eq__(self, other: Factory[T]) -> bool:
        return isinstance(other, _AsyncGenFactory) and self._gen_fn == other._gen_fn

    @override
    def __hash__(self) -> int:
        return hash(self._gen_fn)
