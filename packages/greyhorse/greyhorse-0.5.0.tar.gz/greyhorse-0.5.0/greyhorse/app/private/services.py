import asyncio
import inspect
import threading
import types
from collections.abc import Callable, Iterable, Mapping
from dataclasses import dataclass, field
from typing import Any

from greyhorse.app.abc.resources.common import ResourceEventKind
from greyhorse.app.abc.resources.providers import ProviderListenerFn, ProviderSubscription
from greyhorse.app.abc.resources.reconciler import ReconcilerCollector
from greyhorse.enum import Enum, Struct, Unit


@dataclass(slots=True, frozen=True, kw_only=True)
class _ProviderListenerData:
    target: ProviderListenerFn
    for_type: type | types.UnionType
    kind: ResourceEventKind
    metadata: Mapping[str, Any] = field(default_factory=dict)


def _is_provider_listener_member(member: types.FunctionType) -> bool:
    return hasattr(member, '__prov_list_data__')


def provider_listener(
    for_type: type | types.UnionType,
    kind: ResourceEventKind = ResourceEventKind.ALL,
    **metadata: Any,
) -> Callable[[ProviderListenerFn], ProviderListenerFn]:
    def decorator(func: ProviderListenerFn) -> ProviderListenerFn:
        func.__prov_list_data__ = _ProviderListenerData(
            target=func, for_type=for_type, kind=kind, metadata=metadata
        )
        return func

    return decorator


class ServiceState(Enum):
    Idle = Unit()
    Initialization = Unit()
    Finalization = Unit()
    Initialized = Unit()
    Finalized = Unit()
    Ready = Struct(started=bool)
    Unready = Struct(started=bool, message=str)


class ServiceWaiter(Enum):
    Sync = Struct(value=threading.Event)
    Async = Struct(value=asyncio.Event)


class Service:
    __slots__ = ('__prov_listeners', '__state', '__waiter')

    def __init__(self, waiter: ServiceWaiter) -> None:
        self.__state = ServiceState.Idle
        self.__waiter = waiter
        self.__prov_listeners: list[_ProviderListenerData] = []
        self._init_members()

    @property
    def state(self) -> ServiceState:
        return self.__state

    @property
    def waiter(self) -> ServiceWaiter:
        return self.__waiter

    def setup(
        self, prov_subscription: ProviderSubscription, task_collector: ReconcilerCollector
    ) -> None:
        for data in self.__prov_listeners:
            target_types = self._get_target_types(data)
            for target_type in target_types:
                prov_subscription.add_provider_listener(target_type, data.target, data.kind)

    def teardown(self, prov_subscription: ProviderSubscription) -> None:
        for data in reversed(self.__prov_listeners):
            target_types = self._get_target_types(data)
            for target_type in target_types:
                prov_subscription.remove_provider_listener(target_type, data.target, data.kind)

    def _init_members(self) -> None:
        for _, member in inspect.getmembers(self):
            if _is_provider_listener_member(member):
                data = member.__prov_list_data__
                # data = replace(data, target=into_factory(member))
                self.__prov_listeners.append(data)

    def _get_target_types(self, data: _ProviderListenerData) -> Iterable[type]:
        if isinstance(data.for_type, types.UnionType):
            target_types = data.for_type.__args__
        else:
            target_types = [data.for_type]
        return target_types

    def _set_state(self, state: ServiceState) -> None:
        match state:
            case ServiceState.Ready(started) | ServiceState.Unready(started):
                if started:
                    self.__waiter.value.clear()
                else:
                    self.__waiter.value.set()
            case _:
                pass

        self.__state = state
