from abc import ABC, abstractmethod

from .collectors import Collector, MutCollector
from .selectors import ListSelector, Selector


class Registry[K, T](Collector[K, T], Selector[K, T], ABC): ...


class MutRegistry[K, T](Registry[K, T], MutCollector[K, T], ABC):
    @abstractmethod
    def clear(self) -> None: ...


class ListRegistry[K, T](Registry[K, T], ListSelector[K, T], ABC): ...


class MutListRegistry[K, T](MutRegistry[K, T], ListRegistry[K, T], ABC): ...
