from typing import override

from greyhorse.app.abc.providers import (
    BorrowError,
    BorrowMutError,
    ForwardError,
    ForwardProvider,
    MutProvider,
    Provider,
)
from greyhorse.app.private.runtime.invoke import invoke_sync
from greyhorse.factory import Factory, FactoryFn, into_factory
from greyhorse.maybe import Just, Maybe, Nothing
from greyhorse.result import Ok, Result
from greyhorse.utils.types import TypeWrapper


type SharedFactory[T] = Factory[T] | Factory[Result[T, BorrowError]]
type MutFactory[T] = Factory[T] | Factory[Result[T, BorrowMutError]]


class _BasicBox:
    __slots__ = ('_acq_counter', '_shared_counter')

    allow_borrow_when_acquired = False
    allow_acq_when_borrowed = False
    allow_multiple_acquisition = False

    def __init__(self) -> None:
        self._shared_counter = 0
        self._acq_counter = 0

    def _check_borrow[T](self, name: str) -> BorrowError | None:
        if not self.allow_borrow_when_acquired and self._acq_counter > 0:
            return BorrowError.BorrowedAsMutable(name=name)
        return None

    def _check_borrow_mut[T](self, name: str) -> BorrowMutError | None:
        if not self.allow_multiple_acquisition and self._acq_counter > 0:
            return BorrowMutError.AlreadyBorrowed(name=name)
        if not self.allow_acq_when_borrowed and self._shared_counter > 0:
            return BorrowMutError.BorrowedAsImmutable(name=name)
        return None

    @staticmethod
    def _ensure_result[T](value: object, name: str) -> Result[T, BorrowError]:
        if isinstance(value, Result):
            return value
        if value is None:
            return BorrowError.Empty(name=name).to_result()
        if isinstance(value, BorrowError):
            return value.to_result()
        return Ok(value)

    @staticmethod
    def _ensure_mut_result[T](value: object, name: str) -> Result[T, BorrowMutError]:
        if isinstance(value, Result):
            return value
        if value is None:
            return BorrowMutError.Empty(name=name).to_result()
        if isinstance(value, BorrowMutError):
            return value.to_result()
        return Ok(value)


class SharedBox[T](_BasicBox, Provider[T], TypeWrapper[T]):
    __slots__ = ('_factory', '_value')

    def __init__(self, factory: SharedFactory[T] | FactoryFn[T]) -> None:
        super().__init__()
        if not isinstance(factory, Factory):
            factory = into_factory(factory, self.wrapped_type)
        self._factory = factory
        self._value: Maybe[T] = Nothing

    @override
    def borrow(self) -> Result[T, BorrowError]:
        if (res := self._check_borrow(self.wrapped_type.__name__)) is not None:
            return res.to_result()

        if self._value.is_just():
            self._shared_counter += 1
            return Ok(self._value.unwrap())

        return self._ensure_result(invoke_sync(self._factory), self.wrapped_type.__name__).map(
            self._set_value
        )

    @override
    def reclaim(self) -> None:
        if self._value.is_nothing():
            return
        self._shared_counter = max(0, self._shared_counter - 1)
        if self._shared_counter == 0:
            self._value.map(self._reset_value)

    def _set_value(self, value: T) -> T:
        self._value = Just(value)
        self._shared_counter = 1
        return value

    def _reset_value(self, value: T) -> None:
        if self._factory.scoped:
            invoke_sync(self._factory.destroy, value)
        self._value = Nothing


class MutBox[T](_BasicBox, MutProvider[T], TypeWrapper[T]):
    __slots__ = ('_factory', '_value')

    def __init__(self, factory: MutFactory[T] | FactoryFn[T]) -> None:
        super().__init__()
        if not isinstance(factory, Factory):
            factory = into_factory(factory, self.wrapped_type)
        self._factory = factory
        self._value: Maybe[T] = Nothing

    @override
    def acquire(self) -> Result[T, BorrowMutError]:
        if (res := self._check_borrow_mut(self.wrapped_type.__name__)) is not None:
            return res.to_result()

        if self._value.is_just():
            self._acq_counter += 1
            return Ok(self._value.unwrap())

        return self._ensure_mut_result(
            invoke_sync(self._factory), self.wrapped_type.__name__
        ).map(self._set_value)

    @override
    def release(self) -> None:
        if self._value.is_nothing():
            return
        self._acq_counter = max(0, self._acq_counter - 1)
        if self._acq_counter == 0:
            self._value.map(self._reset_value)

    def _set_value(self, value: T) -> T:
        self._value = Just(value)
        self._acq_counter = 1
        return value

    def _reset_value(self, value: T) -> None:
        if self._factory.scoped:
            invoke_sync(self._factory.destroy, value)
        self._value = Nothing


class CombinedBox[TS, TM](_BasicBox, MutProvider[TM], Provider[TS], TypeWrapper[TS, TM]):
    __slots__ = ('_factory', '_mut_factory', '_mut_value', '_value')

    def __init__(
        self,
        factory: SharedFactory[TS] | FactoryFn[TS],
        mut_factory: MutFactory[TM] | FactoryFn[TM],
    ) -> None:
        super().__init__()
        if not isinstance(factory, Factory):
            factory = into_factory(factory, self.wrapped_type[0])
        if not isinstance(mut_factory, Factory):
            mut_factory = into_factory(mut_factory, self.wrapped_type[1])
        self._factory = factory
        self._mut_factory = mut_factory
        self._value: Maybe[TS] = Nothing
        self._mut_value: Maybe[TM] = Nothing

    @property
    def shared_type(self) -> type[TS]:
        return self._factory.return_type

    @property
    def mut_type(self) -> type[TM]:
        return self._mut_factory.return_type

    @override
    def borrow(self) -> Result[TS, BorrowError]:
        if (res := self._check_borrow(self.shared_type.__name__)) is not None:
            return res.to_result()

        if self._value.is_just():
            self._shared_counter += 1
            return Ok(self._value.unwrap())

        return self._ensure_result(invoke_sync(self._factory), self.shared_type.__name__).map(
            self._set_value
        )

    @override
    def reclaim(self) -> None:
        if self._value.is_nothing():
            return
        self._shared_counter = max(0, self._shared_counter - 1)
        if self._shared_counter == 0:
            self._value.map(self._reset_value)

    @override
    def acquire(self) -> Result[TM, BorrowMutError]:
        if (res := self._check_borrow_mut(self.mut_type.__name__)) is not None:
            return res.to_result()

        if self._mut_value.is_just():
            self._acq_counter += 1
            return Ok(self._mut_value.unwrap())

        return self._ensure_mut_result(
            invoke_sync(self._mut_factory), self.mut_type.__name__
        ).map(self._set_mut_value)

    @override
    def release(self) -> None:
        if self._mut_value.is_nothing():
            return
        self._acq_counter = max(0, self._acq_counter - 1)
        if self._acq_counter == 0:
            self._mut_value.map(self._reset_mut_value)

    def _set_value(self, value: TS) -> TS:
        self._value = Just(value)
        self._shared_counter = 1
        return value

    def _reset_value(self, value: TS) -> None:
        if self._factory.scoped:
            invoke_sync(self._factory.destroy, value)
        self._value = Nothing

    def _set_mut_value(self, value: TM) -> TM:
        self._mut_value = Just(value)
        self._acq_counter = 1
        return value

    def _reset_mut_value(self, value: TM) -> None:
        if self._mut_factory.scoped:
            invoke_sync(self._mut_factory.destroy, value)
        self._mut_value = Nothing


class ForwardBox[T](ForwardProvider[T], TypeWrapper[T]):
    __slots__ = ('_value',)

    def __init__(self, value: T | None = None) -> None:
        self._value = Maybe(value)

    def accept(self, value: T) -> bool:
        if self._value.is_just():
            return False
        self._value = Maybe(value)
        return True

    def revoke(self) -> Maybe[T]:
        value, self._value = self._value, Nothing
        return value

    @override
    def take(self) -> Result[T, ForwardError]:
        value, self._value = self._value, Nothing
        return value.map(Ok).unwrap_or(
            ForwardError.Empty(name=self.wrapped_type.__name__).to_result()
        )

    @override
    def drop(self, instance: T) -> None:
        del instance

    @override
    def __bool__(self) -> bool:
        return self._value.is_just()


class PermanentForwardBox[T](ForwardBox[T]):
    @override
    def take(self) -> Result[T, ForwardError]:
        return self._value.map(Ok).unwrap_or(
            ForwardError.Empty(name=self.wrapped_type.__name__).to_result()
        )

    @override
    def drop(self, instance: T) -> None:
        pass
