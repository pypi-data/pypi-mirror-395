from __future__ import annotations

from collections.abc import Collection, Generator
from enum import IntEnum
from typing import Any, override

from greyhorse.app.abc.functional.context import OperationContext
from greyhorse.app.abc.functional.operators import CompilationResult, Operator
from greyhorse.app.abc.functional.resolver import ResolvedData, Resolver
from greyhorse.factory import Factory, into_factory


class ContextOperator[T](Operator[T]):
    __slots__ = (
        '_compiled',
        '_external_params',
        '_functor',
        '_resolved_types',
        '_resolver',
        '_scope',
    )

    def __init__(
        self,
        functor: Factory[T],
        resolver: Resolver,
        scope: IntEnum | None = None,
        external_params: Collection[type] | None = None,
    ) -> None:
        self._resolver = resolver
        self._scope = scope
        self._external_params = set(external_params or [])
        self._resolved_types: dict[type, ResolvedData] = {
            functor.return_type: ResolvedData(
                type=functor.return_type, factory=functor, deps=dict(functor.actual_params)
            )
        }
        self._compiled = False
        self._functor = functor

    @override
    @property
    def return_type(self) -> type[T]:
        return self._functor.return_type

    @override
    @property
    def compiled(self) -> bool:
        return self._compiled

    @classmethod
    def from_context(
        cls,
        context: OperationContext,
        functor: Factory[T],
        scope: IntEnum | None,
        external_params: Collection[type] | None = None,
    ) -> Operator[T]:
        resolver = context.context_resolver(scope)
        return cls(functor, resolver, scope, external_params)

    @override
    def compile(self) -> CompilationResult:
        if self.compiled:
            return CompilationResult(resolved=self._resolved_types.keys())

        res = self._resolver.resolve_factories(self.return_type, self._scope)
        self._resolved_types.update(res.resolved)
        self._compiled = not res.unresolved
        return CompilationResult(
            resolved=self._resolved_types.keys(), unresolved=res.unresolved
        )

    @override
    def get_functor(self) -> Factory[T]:
        compilation_result = self.compile()

        external_params = {
            param_name: param_type
            for param_name, param_type in self._functor.actual_params.items()
            if param_type in self._external_params
            or param_type in compilation_result.unresolved
            or not self._resolver.can_resolve(param_type)
        }

        external_params_size = len(external_params) if external_params else 0
        if external_params_size >= len(self._functor.actual_params):
            return self._functor

        return Factory[self.return_type].from_syncgen(
            self._entrypoint,
            cache_policy=self._functor.cache_policy,
            hints={
                'return': Generator[self.return_type, self.return_type, None],
                **external_params,
            },
        )

    def _entrypoint(self, *args: Any, **kwargs: Any) -> Generator[T, T, None]:
        resolved = self._resolved_types.copy()

        with self._resolver as resolver:
            for param_idx, (param_name, param_type) in enumerate(
                self._functor.actual_params.items()
            ):
                if param_idx < len(args) and issubclass(type(args[param_idx]), param_type):
                    resolved[param_type] = ResolvedData(
                        type=param_type, factory=into_factory(args[param_idx])
                    )
                    continue
                if param_name in kwargs and param_type in self._external_params:
                    resolved[param_type] = ResolvedData(
                        type=param_type, factory=into_factory(kwargs[param_name])
                    )
                    continue
            instance = resolver.resolve_value(resolved, self.return_type, self._scope)
            assert instance.is_just()
            yield instance.unwrap()
