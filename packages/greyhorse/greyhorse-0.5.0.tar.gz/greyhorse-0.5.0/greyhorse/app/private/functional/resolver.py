from __future__ import annotations

from collections import deque
from collections.abc import Mapping
from dataclasses import dataclass, field
from enum import IntEnum
from types import TracebackType
from typing import Any, Self, override

from greyhorse.app.abc.functional.registries import FactoryRegistry
from greyhorse.app.abc.functional.resolver import ResolvedData, Resolver, ResolveResult
from greyhorse.factory import CachePolicy
from greyhorse.maybe import Just, Maybe, Nothing
from greyhorse.utils.types import is_maybe, is_optional, unwrap

from ..runtime.invoke import invoke_sync
from .bucket import Bucket


@dataclass(slots=True, kw_only=True)
class _FrameData[T]:
    type: type[T]
    values: dict[type, Any] = field(default_factory=dict)
    visited: bool = False


class BucketResolver(Resolver):
    __slots__ = ('_bucket', '_filters', '_registry')

    def __init__(
        self, registry: FactoryRegistry, prev_bucket: Bucket | None = None, /, **filters: Any
    ) -> None:
        self._registry = registry
        self._filters = filters
        self._bucket = Bucket(prev=prev_bucket)

    @override
    def can_resolve[T](self, key: type[T]) -> bool:
        resolving_type = unwrap(key)
        bucket = self._bucket
        filters = dict(**self._filters)

        while bucket is not None:
            if bucket.cache.has(resolving_type):
                return True
            if bucket.scope is not None:
                filters['scope'] = bucket.scope
            if self._registry.has_factory(target_type=resolving_type, **filters):
                return True
            bucket = bucket.prev

        return False

    @override
    def resolve[T](self, key: type[T], from_scope: IntEnum | None = None) -> Maybe[T]:
        resolving_type = unwrap(key)
        if res := self._bucket.get(resolving_type).map(
            lambda v: Just(v) if is_maybe(key) else v
        ):
            return res

        res = self.resolve_factories(key, from_scope)
        if res.unresolved:
            return Nothing

        return self.resolve_value(res.resolved, key, from_scope)

    @override
    def __enter__(self) -> Self:
        self._bucket.incr()
        return self

    @override
    def __exit__(
        self,
        exc_type: type[BaseException] | None = None,
        exc_value: BaseException | None = None,
        traceback: TracebackType | None = None,
    ) -> None:
        self._bucket.decr()

    @override
    def resolve_factories[T](
        self, key: type[T], from_scope: IntEnum | None = None
    ) -> ResolveResult:
        resolve_queue: deque[type] = deque([unwrap(key)])
        resolved: dict[type, ResolvedData] = {}
        unresolved = []

        while resolve_queue:
            resolving_type = resolve_queue[0]
            current_bucket = self._bucket

            while current_bucket is not None:
                if from_scope is None or (
                    current_bucket.scope is not None and current_bucket.scope <= from_scope
                ):
                    if current_bucket.scope is not None:
                        filters = {'scope': current_bucket.scope, **self._filters}
                    else:
                        filters = self._filters

                    if res := self._registry.get_factory(target_type=resolving_type, **filters):
                        resolved_data = ResolvedData(type=resolving_type, factory=res.unwrap())
                        resolved[resolving_type] = resolved_data
                        resolve_queue.popleft()

                        for (
                            param_name,
                            param_type,
                        ) in resolved_data.factory.actual_params.items():
                            stripped_param_type = unwrap(param_type)
                            resolved_data.deps[param_name] = param_type
                            if param_type not in resolved:
                                resolve_queue.append(stripped_param_type)
                        break

                current_bucket = current_bucket.prev
            else:
                unresolved.append(resolving_type)
                resolve_queue.popleft()

        return ResolveResult(resolved=resolved, unresolved=unresolved)

    @override
    def resolve_value[T](  # noqa: PLR0915
        self,
        resolved: Mapping[type, ResolvedData],
        key: type[T],
        from_scope: IntEnum | None = None,
    ) -> Maybe[T]:
        resolving_type = unwrap(key)

        if res := self._bucket.get(resolving_type).map(
            lambda v: Just(v) if is_maybe(key) else v
        ):
            return res

        if resolving_type not in resolved:
            return Nothing

        resolve_stack: list[ResolvedData] = [resolved[resolving_type]]
        frame_stack: list[_FrameData] = [_FrameData(type=resolving_type)]
        instance = None

        while resolve_stack:
            head = resolve_stack[-1]
            frame_head = frame_stack[-1]

            if res := self._bucket.get(head.type):
                frame_head.values[head.type] = res if is_maybe(head.type) else res.unwrap()
                resolve_stack.pop()
                continue

            if head.type is not frame_head.type:
                frame_head = _FrameData(type=head.type)
                frame_stack.append(frame_head)

            if head.deps and not frame_head.visited:
                need_continue = False
                for dep_type in reversed(head.deps.values()):
                    if dep_type not in frame_head.values:
                        stripped_dep_type = unwrap(dep_type)
                        if stripped_dep_type in resolved:
                            resolve_stack.append(resolved[stripped_dep_type])
                            need_continue = True
                        elif is_maybe(dep_type):
                            frame_head.values[dep_type] = Nothing
                        elif is_optional(dep_type):
                            frame_head.values[dep_type] = None
                frame_head.visited = True
                if need_continue:
                    continue

            kwargs = {k: frame_head.values[v] for k, v in head.deps.items()}
            instance = invoke_sync(head.factory.create, **kwargs)
            instance = Just(instance) if is_maybe(head.type) else instance
            if len(frame_stack) > 1:
                frame_stack[-2].values[head.type] = instance

            match head.factory.cache_policy:
                case CachePolicy.VOLATILE | CachePolicy.GRAPH:
                    self._bucket.cache.add(head.type, instance)
                    if head.factory.scoped:
                        self._bucket.finalizers[head.type].append((head.factory, instance))
                case CachePolicy.ANY:
                    bucket = prev_bucket = self._bucket
                    while bucket is not None:
                        if from_scope is None or (
                            bucket.scope is not None and bucket.scope >= from_scope
                        ):
                            bucket.cache.add(head.type, instance)
                            prev_bucket = bucket
                        bucket = bucket.prev
                    if head.factory.scoped:
                        prev_bucket.finalizers[head.type].append((head.factory, instance))

            frame_stack.pop()
            resolve_stack.pop()

        return Just(instance)
