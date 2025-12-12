from abc import ABC, abstractmethod

from greyhorse.maybe import Maybe

from .component import Component


class Module(ABC):
    @property
    @abstractmethod
    def name(self) -> str: ...

    @property
    @abstractmethod
    def full_path(self) -> str: ...

    @abstractmethod
    def get_component(self, name: str) -> Maybe[Component]: ...

    @abstractmethod
    def setup(self) -> None: ...
    @abstractmethod
    def teardown(self) -> None: ...
