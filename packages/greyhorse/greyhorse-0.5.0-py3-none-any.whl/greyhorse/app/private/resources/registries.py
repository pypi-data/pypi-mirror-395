import weakref
from dataclasses import dataclass
from typing import Any, override

from greyhorse.app.abc.collections.collectors import MutCollector
from greyhorse.app.abc.resources.common import ResourceEventKind
from greyhorse.app.abc.resources.operators import (
    OperatorData,
    OperatorEvent,
    OperatorListenerFn,
    OperatorSubscription,
)
from greyhorse.app.abc.resources.providers import (
    ProviderData,
    ProviderEvent,
    ProviderListenerFn,
    ProviderSubscription,
)

from ..collections.registries import MutDictRegistry
from ..runtime.invoke import invoke_sync


@dataclass(slots=True, frozen=True, kw_only=True)
class _CovariantListenersFilter[T]:
    kind: ResourceEventKind
    key: type[T]

    def __call__(self, t: type[T], metadata: dict[str, Any]) -> bool:
        return t is Any or (
            issubclass(self.key, t) and metadata['kind'] & self.kind != ResourceEventKind(0)
        )


@dataclass(slots=True, frozen=True, kw_only=True)
class _ContravariantListenersFilter[T]:
    kind: ResourceEventKind
    key: type[T]

    def __call__(self, t: type[T], metadata: dict[str, Any]) -> bool:
        return t is Any or (
            issubclass(t, self.key) and metadata['kind'] & self.kind != ResourceEventKind(0)
        )


def _is_bound_method(cb: Any) -> bool:
    return (
        hasattr(cb, '__self__')
        and hasattr(cb, '__func__')
        and cb.__self__ is not None
        and not isinstance(cb.__self__, type)
        and getattr(cb.__func__, '__self__', None) is None
    )


class OperatorRegistry(MutCollector[type, OperatorData], OperatorSubscription):
    __slots__ = ('_metadata', '_op_listeners')

    def __init__(self) -> None:
        super().__init__()
        self._metadata = MutDictRegistry[type, OperatorData](allow_many=True)
        self._op_listeners = MutDictRegistry[type, OperatorListenerFn](allow_many=True)

    @override
    def add[U](self, target_type: type[U], instance: OperatorData, /, **metadata: Any) -> bool:
        filter = _CovariantListenersFilter(kind=ResourceEventKind.SETUP, key=target_type)

        event = OperatorEvent(kind=ResourceEventKind.SETUP, type=target_type, data=instance)
        self._notify(event, filter)
        return self._metadata.add(target_type, instance, **metadata)

    @override
    def remove[U](self, target_type: type[U], instance: OperatorData | None = None) -> bool:
        filter = _CovariantListenersFilter(kind=ResourceEventKind.TEARDOWN, key=target_type)

        if instance is None:
            for data, _md in self._metadata.list_with_metadata(target_type):
                event = OperatorEvent(
                    kind=ResourceEventKind.TEARDOWN, type=target_type, data=data
                )
                self._notify(event, filter)
        else:
            event = OperatorEvent(
                kind=ResourceEventKind.TEARDOWN, type=target_type, data=instance
            )
            self._notify(event, filter)

        return self._metadata.remove(target_type, instance)

    @override
    def add_operator_listener[T](
        self,
        key: type[T],
        fn: OperatorListenerFn,
        kind: ResourceEventKind = ResourceEventKind.ALL,
    ) -> bool:
        if _is_bound_method(fn):
            fn = weakref.WeakMethod(fn)
            md = {'weak': True}
        else:
            md = {'weak': False}
        return self._op_listeners.add(key, fn, kind=kind, **md)

    @override
    def remove_operator_listener[T](
        self,
        key: type[T],
        fn: OperatorListenerFn | None = None,
        kind: ResourceEventKind = ResourceEventKind.ALL,
    ) -> bool:
        filter = _CovariantListenersFilter(kind=kind, key=key)
        to_remove = []

        for t, orig_fn, metadata in self._op_listeners.filter(filter):
            if metadata['weak'] and (orig_fn := orig_fn()) is None:
                to_remove.append((t, orig_fn, metadata['kind']))
                continue
            if fn is None or fn == orig_fn:
                to_remove.append((t, orig_fn, metadata['kind']))

        res = False

        for orig_key, orig_fn, orig_kind in to_remove:
            new_kind = orig_kind & ~kind
            res |= self._op_listeners.remove(orig_key, orig_fn)
            if new_kind != ResourceEventKind(0):
                self._op_listeners.add(orig_key, orig_fn, kind=new_kind)

        return res

    def _notify(self, event: OperatorEvent, filter: _CovariantListenersFilter) -> None:
        callbacks = []
        to_remove = []

        for t, listener, metadata in self._op_listeners.filter(filter):
            if metadata['weak']:
                if listener._alive:  # noqa: SLF001
                    listener = listener()
                else:
                    to_remove.append((t, listener, metadata['kind']))
                    continue
            callbacks.append(listener)

        for orig_key, orig_fn, _orig_kind in to_remove:
            self._op_listeners.remove(orig_key, orig_fn)

        for listener in callbacks:
            invoke_sync(listener, event)


class ProviderRegistry(MutCollector[type, ProviderData], ProviderSubscription):
    __slots__ = ('_metadata', '_prov_listeners')

    def __init__(self) -> None:
        super().__init__()
        self._metadata = MutDictRegistry[type, ProviderData](allow_many=True)
        self._prov_listeners = MutDictRegistry[type, ProviderListenerFn](allow_many=True)

    @override
    def add[U](self, target_type: type[U], instance: ProviderData, /, **metadata: Any) -> bool:
        filter = _CovariantListenersFilter(kind=ResourceEventKind.SETUP, key=target_type)

        event = ProviderEvent(kind=ResourceEventKind.SETUP, type=target_type, data=instance)
        self._notify(event, filter)
        return self._metadata.add(target_type, instance, **metadata)

    @override
    def remove[U](self, target_type: type[U], instance: ProviderData | None = None) -> bool:
        filter = _CovariantListenersFilter(kind=ResourceEventKind.TEARDOWN, key=target_type)

        if instance is None:
            for data, _md in self._metadata.list_with_metadata(target_type):
                event = ProviderEvent(
                    kind=ResourceEventKind.TEARDOWN, type=target_type, data=data
                )
                self._notify(event, filter)
        else:
            event = ProviderEvent(
                kind=ResourceEventKind.TEARDOWN, type=target_type, data=instance
            )
            self._notify(event, filter)

        return self._metadata.remove(target_type, instance)

    @override
    def add_provider_listener[T](
        self,
        key: type[T],
        fn: ProviderListenerFn,
        kind: ResourceEventKind = ResourceEventKind.ALL,
    ) -> bool:
        if _is_bound_method(fn):
            fn = weakref.WeakMethod(fn)
            md = {'weak': True}
        else:
            md = {'weak': False}
        return self._prov_listeners.add(key, fn, kind=kind, **md)

    @override
    def remove_provider_listener[T](
        self,
        key: type[T],
        fn: ProviderListenerFn | None = None,
        kind: ResourceEventKind = ResourceEventKind.ALL,
    ) -> bool:
        filter = _CovariantListenersFilter(kind=kind, key=key)
        to_remove = []

        for t, orig_fn, metadata in self._prov_listeners.filter(filter):
            if metadata['weak'] and (orig_fn := orig_fn()) is None:
                to_remove.append((t, orig_fn, metadata['kind']))
                continue
            if fn is None or fn == orig_fn:
                to_remove.append((t, orig_fn, metadata['kind']))

        res = False

        for orig_key, orig_fn, orig_kind in to_remove:
            new_kind = orig_kind & ~kind
            res |= self._prov_listeners.remove(orig_key, orig_fn)
            if new_kind != ResourceEventKind(0):
                self._prov_listeners.add(orig_key, orig_fn, kind=new_kind)

        return res

    def _notify(self, event: ProviderEvent, filter: _CovariantListenersFilter) -> None:
        callbacks = []
        to_remove = []

        for t, listener, metadata in self._prov_listeners.filter(filter):
            if metadata['weak']:
                if listener._alive:  # noqa: SLF001
                    listener = listener()
                else:
                    to_remove.append((t, listener, metadata['kind']))
                    continue
            callbacks.append(listener)

        for orig_key, orig_fn, _orig_kind in to_remove:
            self._prov_listeners.remove(orig_key, orig_fn)

        for listener in callbacks:
            invoke_sync(listener, event)
