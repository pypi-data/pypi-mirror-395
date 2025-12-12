import inspect
import types
from collections.abc import Callable, Iterable, Mapping
from dataclasses import dataclass, field
from typing import Any

from greyhorse.app.abc.resources.common import ResourceEventKind
from greyhorse.app.abc.resources.operators import OperatorListenerFn, OperatorSubscription
from greyhorse.app.abc.resources.reconciler import ReconcilerCollector


@dataclass(slots=True, frozen=True, kw_only=True)
class _OperatorListenerData:
    target: OperatorListenerFn
    for_type: type | types.UnionType
    kind: ResourceEventKind
    metadata: Mapping[str, Any] = field(default_factory=dict)


def _is_operator_listener_member(member: types.FunctionType) -> bool:
    return hasattr(member, '__op_list_data__')


def operator_listener(
    for_type: type | types.UnionType,
    kind: ResourceEventKind = ResourceEventKind.ALL,
    **metadata: Any,
) -> Callable[[OperatorListenerFn], OperatorListenerFn]:
    def decorator(func: OperatorListenerFn) -> OperatorListenerFn:
        func.__op_list_data__ = _OperatorListenerData(
            target=func, for_type=for_type, kind=kind, metadata=metadata
        )
        return func

    return decorator


class Controller:
    __slots__ = ('__op_listeners',)

    def __init__(self) -> None:
        self.__op_listeners: list[_OperatorListenerData] = []
        self._init_members()

    def setup(
        self, op_subscription: OperatorSubscription, task_collector: ReconcilerCollector
    ) -> None:
        for data in self.__op_listeners:
            target_types = self._get_target_types(data)
            for target_type in target_types:
                op_subscription.add_operator_listener(target_type, data.target, data.kind)

    def teardown(self, op_subscription: OperatorSubscription) -> None:
        for data in reversed(self.__op_listeners):
            target_types = self._get_target_types(data)
            for target_type in target_types:
                op_subscription.remove_operator_listener(target_type, data.target, data.kind)

    def _init_members(self) -> None:
        for _, member in inspect.getmembers(self):
            if _is_operator_listener_member(member):
                data = member.__op_list_data__
                # data = replace(data, target=into_factory(member))
                self.__op_listeners.append(data)

    def _get_target_types(self, data: _OperatorListenerData) -> Iterable[type]:
        if isinstance(data.for_type, types.UnionType):
            target_types = data.for_type.__args__
        else:
            target_types = [data.for_type]
        return target_types
