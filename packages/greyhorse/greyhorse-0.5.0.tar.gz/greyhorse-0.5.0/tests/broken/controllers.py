import asyncio
import inspect
import threading
from abc import ABC, abstractmethod
from collections.abc import Awaitable, Callable
from typing import Any

from greyhorse.enum import Enum, Struct, Unit
from greyhorse.error import Error, ErrorCase
from greyhorse.result import Result


class ControllerState(Enum):
    Idle = Unit()
    Initialization = Unit()
    Finalization = Unit()
    Initialized = Unit()
    Finalized = Unit()
    Running = Struct(alive=bool)
    Succeeded = Unit()
    Failed = Struct(message=str)


class ControllerWaiter(Enum):
    Sync = Struct(value=threading.Event)
    Async = Struct(value=asyncio.Event)


class ControllerRestartPolicy(Enum):
    Always = Unit()
    Never = Unit()
    OnFailure = Unit()


class ControllerError(Error):
    namespace = 'greyhorse.app'

    Factory = ErrorCase(msg='Controller factory error: "{details}"', details=str)
    NoSuchResource = ErrorCase(msg='Resource "{name}" is not set', name=str)


type ControllerFactoryFn = Callable[[...], Controller | Result[Controller, ControllerError]]
type ControllerFactories = dict[type[Controller], ControllerFactoryFn]


class ControllerVisitor:
    def visit_operator_listener(self, member: OperatorListenerData) -> None: ...

    def visit_provider_listener(self, member: ProviderListenerData) -> None: ...


class Controller(ABC):
    __slots__ = ('__conditions', '__op_listeners', '__prov_listeners', '__state', '__waiter')

    def __init__(self, waiter: ControllerWaiter) -> None:
        self.__state = ControllerState.Idle
        self.__conditions: dict[str, Condition] = {}
        self.__op_listeners: list[OperatorListenerData] = []
        self.__prov_listeners: list[ProviderListenerData] = []
        self.__waiter = waiter
        self._init_members()

    @property
    def state(self) -> ControllerState:
        return self.__state

    @property
    def waiter(self) -> ControllerWaiter:
        return self.__waiter

    @property
    def status(self) -> ReconciliationStatus:
        match self.__state:
            case ControllerState.Running(alive) if alive:
                return ReconciliationStatus.Live(
                    data=ConditionsData(conditions=self.__conditions)
                )
            case ControllerState.Succeeded:
                return ReconciliationStatus.Succeeded(
                    data=ConditionsData(conditions=self.__conditions)
                )
            case ControllerState.Failed:
                return ReconciliationStatus.Failed(
                    data=ConditionsData(conditions=self.__conditions)
                )
            case _:
                return ReconciliationStatus.Dead

    def inspect(self, visitor: ControllerVisitor) -> None:
        for item in self.__op_listeners:
            visitor.visit_operator_listener(item)
        for item in self.__prov_listeners:
            visitor.visit_provider_listener(item)

    @abstractmethod
    def setup(self, *args: Any, **kwargs: Any) -> None | Awaitable[None]: ...

    @abstractmethod
    def teardown(self, *args: Any, **kwargs: Any) -> None | Awaitable[None]: ...

    def _init_members(self) -> None:
        for _, member in inspect.getmembers(self, is_operator_listener_member):
            data = member.__op_list_data__
            member = OperatorListenerData(
                target=member, type=data.type, kind=data.kind, metadata=data.metadata
            )
            self.__op_listeners.append(member)

        for _, member in inspect.getmembers(self, is_provider_listener_member):
            data = member.__prov_list_data__
            member = ProviderListenerData(
                target=member, type=data.type, kind=data.kind, metadata=data.metadata
            )
            self.__prov_listeners.append(member)

    def _set_state(self, state: ControllerState) -> None:
        match state:
            case ControllerState.Running(alive):
                if alive:
                    self.__waiter.value.clear()
                else:
                    self.__waiter.value.set()
            case _:
                pass

        self.__state = state

    def _set_condition(self, condition: Condition) -> None:
        self.__conditions[condition.name] = condition

    def _reset_condition(self, name: str) -> bool:
        return self.__conditions.pop(name, None) is not None
