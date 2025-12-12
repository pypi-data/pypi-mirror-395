import enum
from datetime import datetime
from typing import override

from broken.controllers import Condition, ControllerState

from greyhorse.app.abc.functional.factories import MutFactoryRegistry
from greyhorse.app.abc.resources.common import ResourceEventKind
from greyhorse.app.abc.resources.operators import operator
from greyhorse.app.abc.resources.providers import ProviderEvent, provider_listener
from greyhorse.app.abc.services import ServiceState
from greyhorse.app.entities.controllers import SyncController
from greyhorse.app.entities.services import SyncService
from greyhorse.maybe import Maybe
from greyhorse.result import Ok, Result

from ..common.functional import FunctionalOperator
from ..common.resources import DictResContext, MutDictResContext


class TestLifetime(enum.IntEnum):
    DOMAIN = enum.auto(0)
    OPERATION = enum.auto()


class FunctionalOperatorImpl(FunctionalOperator):
    def __init__(self, ctx: DictResContext, mut_ctx: MutDictResContext) -> None:
        self.ctx = ctx
        self.mut_ctx = mut_ctx

    @override
    def add_number(self, value: int) -> Result[None, str]:
        with self.mut_ctx as ctx:
            ctx['number'] = value
            self.mut_ctx.apply()

        return Ok()

    @override
    def get_number(self) -> Result[int, str]:
        with self.ctx as ctx:
            value = Maybe(ctx.get('number'))

        return value.ok_or('Number is not initialized')

    @override
    def remove_number(self) -> Result[bool, str]:
        with self.mut_ctx as ctx:
            value = Maybe(ctx.pop('number', None))
            self.mut_ctx.apply()

        return value.ok_or('Number is not initialized').map(lambda _: True)


class DictResourceCtrl(SyncController):
    def __init__(self, factories: MutFactoryRegistry) -> None:
        super().__init__()
        self._factories = factories

    @override
    def setup(self) -> None:
        cond = Condition(
            name='DictResContext',
            status=self._factories.has_factory(DictResContext),
            permanent=True,
            transition_dt=datetime.now(),
        )
        self._set_condition(cond)
        cond = Condition(
            name='MutDictResContext',
            status=self._factories.has_factory(MutDictResContext),
            permanent=True,
            transition_dt=datetime.now(),
        )
        self._set_condition(cond)
        self._set_state(ControllerState.Succeeded)

    @override
    def teardown(self) -> None:
        self._reset_condition('DictResContext')
        self._reset_condition('MutDictResContext')
        self._set_state(ControllerState.Finalized)

    @provider_listener(DictResContext, fragment='frag1')
    def listener_1(self, event: ProviderEvent) -> None:
        if event.kind == ResourceEventKind.SETUP:
            f = event.context.__enter__()
            self._factories.add_factory(DictResContext, f)
        elif event.kind == ResourceEventKind.TEARDOWN:
            self._factories.remove_factory(DictResContext)
            event.context.__exit__()

    @provider_listener(MutDictResContext, fragment='frag1')
    def listener_2(self, event: ProviderEvent) -> None:
        if event.kind == ResourceEventKind.SETUP:
            f = event.context.__enter__()
            self._factories.add_factory(MutDictResContext, f)
        elif event.kind == ResourceEventKind.TEARDOWN:
            self._factories.remove_factory(MutDictResContext)
            event.context.__exit__()


class FunctionalService(SyncService):
    def __init__(self) -> None:
        super().__init__()

    @override
    def setup(self) -> None:
        self._set_state(ServiceState.Ready(started=False))

    @override
    def teardown(self) -> None:
        self._set_state(ServiceState.Unready(started=False, message='stopped'))

    # @operator(scope=TestLifetime.OPERATION, fragment='frag1')
    # @operator(fragment='frag1')

    op_1 = operator(
        for_type=FunctionalOperator, scope=TestLifetime.OPERATION, fragment='frag1'
    )(FunctionalOperatorImpl)
