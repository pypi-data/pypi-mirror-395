from abc import ABC, abstractmethod
from collections.abc import Collection, Mapping
from typing import Any

from greyhorse.factory import Factory

from .functional.context import OperationContext
from .resources.operators import MutOperatorCollector, OperatorCollector
from .resources.providers import MutProviderCollector, ProviderCollector


class Component(ABC):
    @property
    @abstractmethod
    def name(self) -> str: ...

    @property
    @abstractmethod
    def context(self) -> OperationContext: ...

    @abstractmethod
    def add_factory[T](
        self, target_type: type[T], factory: Factory[T], **filters: Any
    ) -> bool: ...

    @abstractmethod
    def remove_factory[T](
        self, target_type: type[T], factory: Factory[T] | None = None, **filters: Any
    ) -> Collection[tuple[Factory[T], Mapping[str, Any]]]: ...

    @abstractmethod
    def setup(
        self,
        op_collector: OperatorCollector | None = None,
        prov_collector: ProviderCollector | None = None,
    ) -> None: ...

    @abstractmethod
    def teardown(
        self,
        op_collector: MutOperatorCollector | None = None,
        prov_collector: MutProviderCollector | None = None,
    ) -> None: ...
