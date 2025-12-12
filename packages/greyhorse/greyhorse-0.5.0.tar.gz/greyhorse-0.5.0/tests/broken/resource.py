from __future__ import annotations

from collections.abc import Collection, MutableMapping
from dataclasses import dataclass
from typing import override

from greyhorse.app.abc.providers import BorrowError, BorrowMutError
from greyhorse.app.private.collections.registries import MutDictRegistry
from greyhorse.maybe import Just, Maybe, Nothing
from greyhorse.result import Ok, Result


@dataclass(slots=True, frozen=True, kw_only=True)
class ResourceProvisionPolicy:
    allow_borrow_when_acquired = False
    allow_acq_when_borrowed = False
    allow_multiple_acquisition = False


# type SharedFactory[T] = Factory[T] | Factory[Result[T, BorrowError]]
# type MutFactory[T] = Factory[T] | Factory[Result[T, BorrowMutError]]


class SharedStateImpl[S](ResourceState[S]):
    __slots__ = (
        '_conditions',
        '_next_status',
        '_policy',
        '_shared_counter',
        '_status',
        '_type',
        '_value',
    )

    def __init__(self, type: type[S], policy: ResourceProvisionPolicy | None = None) -> None:
        self._policy: ResourceProvisionPolicy = policy or ResourceProvisionPolicy()
        self._status: ResourceStatus = ResourceStatus.Idle
        self._conditions: MutableMapping[str, Condition] = {}
        self._next_status: ResourceStatus | None = None
        self._shared_counter: int = 0
        self._type = type
        self._value: Maybe[S] = Nothing

    def __repr__(self) -> str:
        return f'ResourceState <{self.shared_type.__name__}> status={self._status}'

    @property
    @override
    def shared_type(self) -> type[S]:
        return self._type

    @property
    @override
    def status(self) -> ResourceStatus:
        return self._status

    @property
    @override
    def transition_status(self) -> TransitionStatus:
        total = len(self._conditions)
        completed = 0
        permanent = False
        reasons = []
        messages = []

        for condition in self._conditions.values():
            if condition.status:
                completed += 1
            else:
                permanent |= condition.permanent
                reasons.append(condition.name)
                if condition.message:
                    messages.append(condition.message)

        if total == completed:
            return TransitionStatus.Complete
        if not permanent:
            if completed == 0:
                return TransitionStatus.Pending
            return TransitionStatus.Partial(total=total, completed=completed)
        return TransitionStatus.Failure(reasons=reasons, message='\n'.join(messages))

    @property
    @override
    def next_status(self) -> ResourceStatus | None:
        return self._next_status

    @override
    def borrow(self) -> Result[S, BorrowError]:
        match self._status:
            case ResourceStatus.Available(alive, _):
                self._status = ResourceStatus.Available(alive=alive, in_use=True)
            case ResourceStatus.Acquired(_):
                if not self._policy.allow_borrow_when_acquired:
                    return BorrowError.BorrowedAsMutable(
                        name=self.shared_type.__name__
                    ).to_result()
            case _:
                return BorrowError.Empty(name=self.shared_type.__name__).to_result()

        if self._value.is_nothing():
            return BorrowError.Empty(name=self.shared_type.__name__).to_result()

        self._shared_counter += 1
        return Ok(self._value.unwrap())

    @override
    def reclaim(self) -> None:
        match self._status:
            case ResourceStatus.Available(alive, _):
                self._status = ResourceStatus.Available(
                    alive=alive, in_use=self._shared_counter > 1
                )
            case ResourceStatus.Acquired(_):
                pass
            case _:
                return

        if self._shared_counter == 1:
            self._shared_counter = 0
            self.reset_value()
        else:
            self._shared_counter = max(0, self._shared_counter - 1)

    def set_condition(self, condition: Condition) -> None:
        self._conditions[condition.name] = condition

    def reset_condition(self, name: str) -> bool:
        return self._conditions.pop(name, None) is not None

    def set_status(self, status: ResourceStatus) -> None:
        self._status = status

    def set_value(self, value: S) -> S:
        self._value = Just(value)
        self._shared_counter = 1
        return value

    def reset_value(self) -> None:
        self._value = Nothing


class MutStateImpl[S, M](SharedStateImpl[S], MutResourceState[S, M]):
    __slots__ = ('_acq_counter', '_mut_type', '_mut_value')

    def __init__(
        self,
        shared_type: type[S],
        mut_type: type[M],
        policy: ResourceProvisionPolicy | None = None,
    ) -> None:
        super().__init__(shared_type, policy)
        self._acq_counter: int = 0
        self._mut_type = mut_type
        self._mut_value: Maybe[M] = Nothing

    def __repr__(self) -> str:
        return f'MutResourceState <{self.shared_type.__name__}, {self.mut_type.__name__}> status={self._status}'

    @property
    @override
    def mut_type(self) -> type[M]:
        return self._mut_type

    @override
    def acquire(self) -> Result[M, BorrowMutError]:
        match self._status:
            case ResourceStatus.Available(alive, in_use):
                if in_use and not self._policy.allow_acq_when_borrowed:
                    return BorrowMutError.BorrowedAsImmutable(
                        name=self.mut_type.__name__
                    ).to_result()
                self._status = ResourceStatus.Acquired(alive=alive)
            case ResourceStatus.Acquired(_):
                if not self._policy.allow_multiple_acquisition:
                    return BorrowMutError.AlreadyBorrowed(
                        name=self.mut_type.__name__
                    ).to_result()
            case _:
                return BorrowMutError.Empty(name=self.mut_type.__name__).to_result()

        if self._mut_value.is_nothing():
            return BorrowMutError.Empty(name=self.mut_type.__name__).to_result()

        self._acq_counter += 1
        return Ok(self._mut_value.unwrap())

    @override
    def release(self) -> None:
        match self._status:
            case ResourceStatus.Acquired(alive):
                if self._acq_counter == 1:
                    self._acq_counter = 0
                    self._status = ResourceStatus.Available(
                        alive=alive, in_use=self._shared_counter > 1
                    )
                    self.reset_mut_value()
                else:
                    self._acq_counter = max(0, self._acq_counter - 1)
            case _:
                return

    def set_mut_value(self, value: M) -> M:
        self._mut_value = Just(value)
        self._acq_counter = 1
        return value

    def reset_mut_value(self) -> None:
        self._mut_value = Nothing


class _ReconcilerTaskHandler(TaskHandler):
    def __init__(
        self,
        task: ReconcilerTask,
        reconciler: ReconcilerImpl,
        allowed_conditions: list[str] | None = None,
    ) -> None:
        self._task = task
        self._reconciler = reconciler
        self._allowed_conditions = allowed_conditions

    @override
    def add_event(self, event: ReconcilerEvent) -> None:
        self._reconciler.add_event(event)

    @override
    def set_condition(self, condition: Condition) -> bool:
        if (
            self._allowed_conditions is not None
            and condition.name not in self._allowed_conditions
        ):
            return False
        self._reconciler.set_condition(condition)
        return True

    @override
    def cancel(self, reason: str | None = None) -> None:
        self._reconciler.on_task_cancel(self._task.name, reason=reason)

    @override
    def complete[T](self, value: T | None = None) -> None:
        self._reconciler.on_task_complete(self._task.name, value=value)

    @override
    def failure(self, message: str, exception: Exception | None = None) -> None:
        self._reconciler.on_task_failure(self._task.name, message=message, exception=exception)


class ReconcilerImpl[S](Reconciler[S]):
    __slots__ = ('_events', '_state', '_type')

    def __init__(
        self, state: SharedStateImpl[S], waiter: ReconcilerWaiter | None = None
    ) -> None:
        self._state = state
        self._waiter = waiter
        self._tasks = MutDictRegistry[str, ReconcilerTask]()
        self._setup_schedule = []
        self._teardown_schedule = []
        self._periodic_schedule = []
        self._permanent_schedule = []
        self._events = []

    def _schedule(self) -> None:
        for _, task, _md in self._tasks.filter(lambda n, md: md['pending'] is True):
            match task.phase:
                case ReconcilerRunPhase.Setup:
                    self._setup_schedule.append(task)
                case ReconcilerRunPhase.Teardown:
                    self._teardown_schedule.append(task)
                case ReconcilerRunPhase.Periodic(interval):
                    self._periodic_schedule.append(task)
                case ReconcilerRunPhase.Permanent(async_):
                    self._permanent_schedule.append(task)

    @property
    @override
    def status(self) -> ReconciliationStatus:
        match self._state.status:
            case ResourceStatus.Available(alive, _) | ResourceStatus.Acquired(alive):
                if alive:
                    return ReconciliationStatus.Live(status=self._state.transition_status)
                return ReconciliationStatus.Succeeded(status=self._state.transition_status)
            case ResourceStatus.Failed(message):
                return ReconciliationStatus.Failed(
                    status=self._state.transition_status, message=message
                )
            case _:
                return ReconciliationStatus.Dead

    @property
    @override
    def waiter(self) -> ReconcilerWaiter | None:
        return self._waiter

    @override
    def set_resource_status(self, status: ResourceStatus) -> None:
        match status:
            case ResourceStatus.Available(alive, _) | ResourceStatus.Acquired(alive):
                if alive:
                    self._waiter.value.clear()
                else:
                    self._waiter.value.set()
            case _:
                pass

        self._state._status = status

    @override
    def set_condition(self, condition: Condition) -> None:
        self._state.set_condition(condition)

    @override
    def reset_condition(self, name: str) -> bool:
        return self._state.reset_condition(name)

    @override
    def events(self) -> Collection[ReconcilerEvent]:
        return self._events

    @override
    def setup(self, task_collector: TaskCollector) -> None: ...

    @override
    def teardown(self) -> None: ...

    def add_event(self, event: ReconcilerEvent) -> None:
        self._events.append(event)

    def on_task_cancel(self, name: str, reason: str | None = None) -> None: ...

    def on_task_complete(self, name: str, value: T | None = None) -> None: ...

    def on_task_failure(
        self, name: str, message: str, exception: Exception | None = None
    ) -> None: ...
