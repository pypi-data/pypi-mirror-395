import enum
from datetime import datetime
from decimal import Decimal
from typing import Any, override

import pytest
from broken.controllers import Condition, ControllerState

from greyhorse.app.abc.providers import ProviderSelector
from greyhorse.app.abc.resources.common import ResourceEventKind
from greyhorse.app.abc.resources.operators import OperatorEvent, operator, operator_listener
from greyhorse.app.abc.resources.providers import (
    ProviderEvent,
    mut_provider,
    provider,
    provider_listener,
)
from greyhorse.app.abc.services import ServiceState
from greyhorse.app.contexts import SyncContext, SyncMutContext
from greyhorse.app.entities.component import AsyncComponent, ComponentState, SyncComponent
from greyhorse.app.entities.controllers import AsyncController, SyncController
from greyhorse.app.entities.fragment import Fragment
from greyhorse.app.entities.module import Module
from greyhorse.app.entities.services import AsyncService, SyncService
from greyhorse.factory import into_factory
from greyhorse.maybe import Maybe
from greyhorse.result import Ok, Result


class TestLifetime(enum.IntEnum):
    DOMAIN = enum.auto(0)
    OPERATION = enum.auto()


DictResource = dict[str, Any]
DictResContext = SyncContext[DictResource]
MutDictResContext = SyncMutContext[DictResource]


class FunctionalOperator:
    def __init__(self, ctx: DictResContext, mut_ctx: MutDictResContext) -> None:
        self.ctx = ctx
        self.mut_ctx = mut_ctx

    def add_number(self, value: int) -> Result[None, str]:
        with self.mut_ctx as ctx:
            ctx['number'] = value
            self.mut_ctx.apply()

        return Ok()

    def get_number(self) -> Result[int, str]:
        with self.ctx as ctx:
            value = Maybe(ctx.get('number'))

        return value.ok_or('Number is not initialized')

    def remove_number(self) -> Result[bool, str]:
        with self.mut_ctx as ctx:
            value = Maybe(ctx.pop('number', None))
            self.mut_ctx.apply()

        return value.ok_or('Number is not initialized').map(lambda _: True)


class SyncTestService(SyncService):
    def __init__(self) -> None:
        super().__init__()
        self._res = {}
        self._ctx = SyncContext[DictResource](lambda: self._res)
        self._mut_ctx = SyncMutContext[DictResource](lambda: self._res)

    @override
    def setup(self) -> None:
        self._set_state(ServiceState.Ready(started=False))

    @override
    def teardown(self) -> None:
        self._set_state(ServiceState.Unready(started=False, message='stopped'))

    @provider()
    def p_1(self) -> DictResContext:
        return self._ctx

    @mut_provider()
    def p_2(self) -> MutDictResContext:
        return self._mut_ctx

    @provider(scope=TestLifetime.OPERATION)
    def prov_1(self, global_dict: dict) -> int:
        global_dict['SyncTestService'] = 123
        yield 123
        del global_dict['SyncTestService']

    @operator(scope=TestLifetime.DOMAIN, fragment='frag1')
    def op_1(self, global_dict: dict) -> float:
        global_dict['test'] = 123
        yield global_dict['res'] + 1000
        del global_dict['test']


class AsyncTestService(AsyncService):
    def __init__(self) -> None:
        super().__init__()

    @override
    async def setup(self) -> None:
        self._set_state(ServiceState.Ready(started=False))

    @override
    async def teardown(self) -> None:
        self._set_state(ServiceState.Unready(started=False, message='stopped'))

    f_2 = provider(scope=TestLifetime.OPERATION, fragment='frag1')(FunctionalOperator)
    o_1 = operator(scope=TestLifetime.OPERATION, fragment='frag1')(FunctionalOperator)

    @provider(scope=TestLifetime.OPERATION, fragment='frag1')
    async def prov_1(self, global_dict: dict) -> Decimal:
        global_dict['AsyncTestService'] = 123
        yield Decimal(123)
        del global_dict['AsyncTestService']

    @operator(scope=TestLifetime.DOMAIN)
    async def op_1(self, global_dict: dict, e: str) -> str:
        global_dict['test'] = 123
        yield str(global_dict['res'] + 1000)
        del global_dict['test']


class SyncResourceCtrl(SyncController):
    def __init__(self, providers: ProviderSelector) -> None:
        super().__init__()
        self._providers = providers

    @override
    def setup(self) -> None:
        cond = Condition(
            name='DictResContext',
            status=self._providers.has(DictResContext),
            permanent=True,
            transition_dt=datetime.now(),
        )
        self._set_condition(cond)
        cond = Condition(
            name='MutDictResContext',
            status=self._providers.has(MutDictResContext),
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

    @operator_listener(float | str, fragment='frag1')
    def listener_3(self, event: OperatorEvent) -> None:
        pass


class AsyncResourceCtrl(AsyncController):
    def __init__(self) -> None:
        super().__init__()

    @override
    async def setup(self, global_dict: dict) -> None:
        cond = Condition(name='dict', status=False, permanent=True, message='qwer')
        self._set_condition(cond)
        self._set_state(ControllerState.Running(alive=True))

    @override
    async def teardown(self, global_dict: dict) -> None:
        self._reset_condition('dict')
        self._set_state(ControllerState.Succeeded)

    @provider_listener(int | Decimal, fragment='frag1')
    async def listener_1(self, event: ProviderEvent) -> None:
        pass

    @operator_listener(float | str, fragment='frag1')
    async def listener_2(self, event: OperatorEvent) -> None:
        pass


def test_sync_component() -> None:
    state = ComponentState(name='test')
    component = SyncComponent(state)

    assert component.add_controller(SyncResourceCtrl)
    assert not component.add_controller(AsyncResourceCtrl)
    assert component.add_service(SyncTestService)
    assert not component.add_service(AsyncTestService)

    fragment = Fragment('test', 'frag1', scope_class=TestLifetime)

    global_dict = {'res': 345}
    assert fragment.add_operator(dict, into_factory(global_dict))

    component.register_controllers({fragment.name: fragment})
    component.register_services({fragment.name: fragment})

    with fragment.context as selector:
        assert selector.has(float)
        value = selector.get(float).unwrap()
        assert value == 1345
        assert global_dict == {'res': 345, 'test': 123}

    assert global_dict == {'res': 345}

    component.setup_providers()

    res = component.get_shared_provider(int)
    assert res.is_just()
    prov = res.unwrap()

    res = prov.borrow()
    assert res.is_ok()
    assert res.unwrap() == 123
    assert global_dict == {'res': 345, 'SyncTestService': 123}

    prov.reclaim()
    assert global_dict == {'res': 345}

    res = component.get_shared_provider(DictResContext)
    assert res.is_just()
    prov = res.unwrap()
    res = prov.borrow()
    assert res.is_ok()
    prov.reclaim()

    res = component.get_mut_provider(MutDictResContext)
    assert res.is_just()
    prov = res.unwrap()
    res = prov.acquire()
    assert res.is_ok()
    prov.release()

    component.teardown_providers()

    component.unregister_controllers({fragment.name: fragment})
    component.unregister_services({fragment.name: fragment})

    assert component.remove_service(SyncTestService)
    assert not component.remove_service(AsyncTestService)
    assert component.remove_controller(SyncResourceCtrl)
    assert not component.remove_controller(AsyncResourceCtrl)


@pytest.mark.asyncio
async def test_async_component() -> None:
    component = AsyncComponent('test', 'name', TestLifetime)

    assert component.add_controller(SyncResourceCtrl)
    assert component.add_controller(AsyncResourceCtrl)
    assert component.add_service(SyncTestService)
    assert component.add_service(AsyncTestService)

    fragment = Fragment('test', 'frag1')

    global_dict = {'res': 345}
    assert component.add_factory(dict, into_factory(global_dict))

    component.register_controllers({fragment.name: fragment})
    component.register_services({fragment.name: fragment})

    op = fragment._registry.get_factory(float).unwrap()
    value = op()
    assert value == 1345
    assert global_dict == {'res': 345, 'test': 123}

    op.destroy(value)
    assert global_dict == {'res': 345}

    op = fragment._registry.get_factory(str).unwrap()
    value = op()
    assert value == '1345'
    assert global_dict == {'res': 345, 'test': 123}

    op.destroy(value)
    assert global_dict == {'res': 345}

    prov_ctx = fragment._prov_contexts.get(int).unwrap()
    with prov_ctx as prov:
        value = prov()
        assert value == 123
        assert global_dict == {'res': 345, 'SyncTestService': 123}

        prov.destroy(value)
        assert global_dict == {'res': 345}

    prov_ctx = fragment._prov_contexts.get(Decimal).unwrap()
    with prov_ctx as prov:
        value = await prov()
        assert Decimal(123) == value
        assert global_dict == {'res': 345, 'AsyncTestService': 123}

        await prov.destroy(value)
        assert global_dict == {'res': 345}

    component.unregister_controllers({fragment.name: fragment})
    component.unregister_services({fragment.name: fragment})

    assert component.remove_service(SyncTestService)
    assert component.remove_service(AsyncTestService)
    assert component.remove_controller(SyncResourceCtrl)
    assert component.remove_controller(AsyncResourceCtrl)


@pytest.mark.asyncio
async def test_async_two_components() -> None:
    component1 = AsyncComponent('test', '1', TestLifetime)
    component2 = AsyncComponent('test', '2', TestLifetime)

    assert component2.add_controller(SyncResourceCtrl)
    # assert component2.add_controller(AsyncResourceCtrl)
    assert component1.add_service(SyncTestService)
    assert component2.add_service(AsyncTestService)

    fragment = Fragment('test', 'frag1')

    component1.register_controllers({fragment.name: fragment})
    component2.register_controllers({fragment.name: fragment})
    component1.register_services({fragment.name: fragment})
    component2.register_services({fragment.name: fragment})

    prov_ctx = fragment._prov_contexts.get(FunctionalOperator).unwrap()
    with prov_ctx as prov:
        oper = prov()

        res = oper.add_number(123)
        assert res.is_ok()

        res = oper.get_number()
        assert res.is_ok()
        assert res.unwrap() == 123

        res = oper.remove_number()
        assert res.is_ok()
        assert res.unwrap() is True

        res = oper.get_number()
        assert res.is_err()
        assert res.unwrap_err() == 'Number is not initialized'

        prov.destroy(oper)

    component2.unregister_services({fragment.name: fragment})
    component1.unregister_services({fragment.name: fragment})
    component2.unregister_controllers({fragment.name: fragment})
    component1.unregister_controllers({fragment.name: fragment})

    assert component1.remove_service(SyncTestService)
    assert component2.remove_service(AsyncTestService)
    assert component2.remove_controller(SyncResourceCtrl)
    # assert component2.remove_controller(AsyncResourceCtrl)


@pytest.mark.asyncio
async def test_async_module() -> None:
    component1 = AsyncComponent('test', '1', TestLifetime)
    component2 = AsyncComponent('test', '2', TestLifetime)

    assert component2.add_controller(SyncResourceCtrl)
    # assert component2.add_controller(AsyncResourceCtrl)
    assert component1.add_service(SyncTestService)
    assert component2.add_service(AsyncTestService)

    module = Module[FunctionalOperator](
        'test',
        'test',
        FunctionalOperator,
        components=[component1, component2],
        fragments=['frag1'],
    )

    ctx = module.make_facade()

    async with ctx as facade:
        res = facade.add_number(123)
        assert res.is_ok()

        res = facade.get_number()
        assert res.is_ok()
        assert res.unwrap() == 123

        res = facade.remove_number()
        assert res.is_ok()
        assert res.unwrap() is True

        res = facade.get_number()
        assert res.is_err()
        assert res.unwrap_err() == 'Number is not initialized'

    assert component1.remove_service(SyncTestService)
    assert component2.remove_service(AsyncTestService)
    assert component2.remove_controller(SyncResourceCtrl)
    # assert component2.remove_controller(AsyncResourceCtrl)
