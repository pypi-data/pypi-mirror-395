from __future__ import annotations

from collections.abc import Mapping
from enum import IntEnum
from types import TracebackType
from typing import Any, override

from greyhorse.app.abc.collections.selectors import Selector
from greyhorse.app.abc.functional.context import OperationContext
from greyhorse.app.abc.functional.registries import FactoryRegistry
from greyhorse.app.abc.functional.resolver import Resolver
from greyhorse.maybe import Maybe

from .bucket import Bucket
from .resolver import BucketResolver


class _ResolverSelector(Selector[type, Any]):
    __slots__ = ('_resolver', '_scope')

    def __init__(
        self, bucket: Bucket, registry: FactoryRegistry, filters: Mapping[str, Any]
    ) -> None:
        self._resolver = BucketResolver(registry, bucket, **filters)
        self._scope = bucket.scope

    @property
    def resolver(self) -> BucketResolver:
        return self._resolver

    def __repr__(self) -> str:
        if self._scope is not None:
            return f'ResolverSelector <{self._scope.name.lower()}>'
        return 'ResolverSelector'

    @override
    def has[T](self, key: type[T]) -> bool:
        return self._resolver.can_resolve(key)

    @override
    def get[T](self, key: type[T]) -> Maybe[T]:
        return self._resolver.resolve(key, self._scope)

    @override
    def get_with_metadata[T](self, key: type[T]) -> Maybe[tuple[T, Mapping[str, Any]]]:
        return self._resolver.resolve(key, self._scope).map(lambda x: (x, {}))


class BucketOperationContext(OperationContext):
    __slots__ = ('_bucket', '_filters', '_registry', '_scope_class')

    def __init__[S: IntEnum](
        self,
        registry: FactoryRegistry,
        scope_class: type[S] | None = None,
        bucket: Bucket | None = None,
        /,
        **filters: Any,
    ) -> None:
        super().__init__(_ResolverSelector)
        self._registry = registry
        self._scope_class = scope_class
        self._filters = filters

        if bucket:
            self._bucket = bucket
        else:
            self._bucket = Bucket(scope=self._scope_class(0)) if self._scope_class else Bucket()

    @override
    @property
    def scope[S: IntEnum](self) -> S | None:
        return self._bucket.scope

    @override
    def context[S: IntEnum](self, scope: S | None = None) -> OperationContext:
        bucket = self._bucket

        if self._scope_class and scope is not None:
            if scope < bucket.scope:
                while scope < bucket.scope and bucket.prev is not None:
                    bucket = bucket.prev
            elif scope > self._bucket.scope:
                next_scope = self._scope_class(self._bucket.scope + 1)
                bucket = self._construct_chain(bucket, next_scope, scope)

        return BucketOperationContext(
            self._registry, self._scope_class, bucket, **self._filters
        )

    @override
    def context_resolver[S: IntEnum](self, scope: S | None = None) -> Resolver:
        bucket = self._bucket

        if self._scope_class and scope is not None:
            if scope < bucket.scope:
                while scope < bucket.scope and bucket.prev is not None:
                    bucket = bucket.prev
            elif scope > self._bucket.scope:
                next_scope = self._scope_class(self._bucket.scope + 1)
                bucket = self._construct_chain(bucket, next_scope, scope)

        return BucketResolver(self._registry, bucket, **self._filters)

    @override
    def advance(self) -> OperationContext:
        if self._bucket.scope is None:
            return self

        next_val = self._bucket.scope + 1
        if next_val >= len(self._scope_class):
            return self
        next_scope = self._scope_class(next_val)
        return self.context(next_scope)

    def __repr__(self) -> str:
        if self.scope is None:
            res = 'OperationContext'
        else:
            res = f'OperationContext <scope={self.scope.name.lower()}>'

        if self._filters:
            filters_repr = ','.join([f'{k}={v}' for k, v in self._filters.items()])
            res += f', filters={filters_repr}>'

        return res

    def __del__(self) -> None:
        if self._bucket.prev:
            self._bucket.prev.num_children -= 1
            self._bucket.prev = None
        del self._bucket

    @override
    def _create(self) -> Selector[type, Any]:
        return self._data.factory(
            bucket=self._bucket, registry=self._registry, filters=self._filters
        )

    @override
    def _enter(self, instance: _ResolverSelector) -> Selector[type, Any]:
        instance.resolver.__enter__()
        return instance

    @override
    def _exit(
        self,
        instance: _ResolverSelector,
        exc_type: type[BaseException] | None = None,
        exc_value: BaseException | None = None,
        traceback: TracebackType | None = None,
    ) -> None:
        instance.resolver.__exit__(exc_type, exc_value, traceback)

    def _construct_chain(
        self, bucket: Bucket, scope_from: IntEnum, scope_to: IntEnum
    ) -> Bucket:
        for next_val in range(scope_from, scope_to + 1):
            if next_val >= len(self._scope_class):
                break
            bucket.num_children += 1
            bucket = Bucket(prev=bucket, scope=self._scope_class(next_val))
        return bucket
