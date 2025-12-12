from abc import ABC, abstractmethod
from collections.abc import Callable, Collection, Mapping
from dataclasses import dataclass, field
from enum import IntEnum
from typing import Any

from greyhorse.factory import Factory

from ..collections.collectors import Collector, MutCollector
from .common import ResourceEventKind


@dataclass(slots=True, frozen=True, kw_only=True)
class OperatorData:
    component: str
    fragment: str
    target: Factory[Any]
    signature: type[Callable]
    scope: IntEnum | None = None
    external_params: Collection[type] | None = None
    metadata: Mapping[str, Any] = field(default_factory=dict, compare=False)


OperatorCollector = Collector[type, OperatorData]
MutOperatorCollector = MutCollector[type, OperatorData]


@dataclass(slots=True, frozen=True, kw_only=True)
class OperatorEvent:
    kind: ResourceEventKind
    type: type
    data: OperatorData


type OperatorListenerFn = Callable[[OperatorEvent], ...]


class OperatorSubscription(ABC):
    @abstractmethod
    def add_operator_listener[T](
        self,
        key: type[T],
        fn: OperatorListenerFn,
        kind: ResourceEventKind = ResourceEventKind.ALL,
    ) -> bool: ...

    @abstractmethod
    def remove_operator_listener[T](
        self,
        key: type[T],
        fn: OperatorListenerFn | None = None,
        kind: ResourceEventKind = ResourceEventKind.ALL,
    ) -> bool: ...
