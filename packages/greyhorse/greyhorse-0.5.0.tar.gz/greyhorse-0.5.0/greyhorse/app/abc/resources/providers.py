from abc import ABC, abstractmethod
from collections.abc import Callable, Mapping
from dataclasses import dataclass, field
from enum import IntEnum
from typing import Any

from ..collections.collectors import Collector, MutCollector
from .common import ResourceEventKind


@dataclass(slots=True, frozen=True, kw_only=True)
class ProviderData:
    component: str
    fragment: str
    signature: type[Callable]
    scope: IntEnum | None = None
    metadata: Mapping[str, Any] = field(default_factory=dict, compare=False)


ProviderCollector = Collector[type, ProviderData]
MutProviderCollector = MutCollector[type, ProviderData]


@dataclass(slots=True, frozen=True, kw_only=True)
class ProviderEvent:
    kind: ResourceEventKind
    type: type
    data: ProviderData


type ProviderListenerFn = Callable[[ProviderEvent], ...]


class ProviderSubscription(ABC):
    @abstractmethod
    def add_provider_listener[T](
        self,
        key: type[T],
        fn: ProviderListenerFn,
        kind: ResourceEventKind = ResourceEventKind.ALL,
    ) -> bool: ...

    @abstractmethod
    def remove_provider_listener[T](
        self,
        key: type[T],
        fn: ProviderListenerFn | None = None,
        kind: ResourceEventKind = ResourceEventKind.ALL,
    ) -> bool: ...
