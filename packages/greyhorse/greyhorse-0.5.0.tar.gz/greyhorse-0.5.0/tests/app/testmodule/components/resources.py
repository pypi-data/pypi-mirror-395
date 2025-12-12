from copy import deepcopy
from functools import partial
from typing import override

from greyhorse.app.abc.resources.providers import provider
from greyhorse.app.abc.services import ServiceState
from greyhorse.app.contexts import MutCtxCallbacks, SyncContext, SyncMutCallbackContext
from greyhorse.app.entities.boxes import OwnerCtxRefBox
from greyhorse.app.entities.services import SyncService
from greyhorse.factory import CachePolicy

from ..common.resources import DictResContext, DictResource, MutDictResContext


class DictResourceBox(OwnerCtxRefBox[DictResource, DictResource]):
    allow_borrow_when_acquired = True
    allow_acq_when_borrowed = True
    allow_multiple_acquisition = False


class DictProviderService(SyncService):
    def __init__(self) -> None:
        super().__init__()
        self._value = {}
        self._box = DictResourceBox(
            SyncContext,
            SyncMutCallbackContext,
            partial(deepcopy, self._value),
            partial(deepcopy, self._value),
            mut_params=dict(callbacks=MutCtxCallbacks(on_apply=self._setter)),
        )

    def _setter(self, value: DictResource) -> None:
        self._value.clear()
        self._value.update(value)

    @override
    def setup(self) -> None:
        self._set_state(ServiceState.Ready(started=False))

    @override
    def teardown(self) -> None:
        self._set_state(ServiceState.Unready(started=False, message='stopped'))

    @provider(policy=CachePolicy.VOLATILE)
    def create_dict(self) -> DictResContext:
        value = self._box.borrow().unwrap()
        yield value
        self._box.reclaim(value)

    @provider()
    def create_mut_dict(self) -> MutDictResContext:
        value = self._box.acquire().unwrap()
        yield value
        self._box.release(value)
