from __future__ import annotations

from collections.abc import Collection
from typing import Any, override

from greyhorse.app.abc.component import Component
from greyhorse.app.abc.module import Module as BaseModule
from greyhorse.app.abc.resources.reconciler import (
    ReconcilerCollector,
    ReconcilerRunPhase,
    ReconcilerTaskFn,
    RestartPolicy,
)
from greyhorse.app.abc.resources.state import (
    MutResourceSelector,
    ResourceSelector,
    ResourceState,
)
from greyhorse.logging import logger
from greyhorse.maybe import Maybe
from greyhorse.utils.injectors import ParamsInjector

from .collections.registries import MutDictRegistry
from .controllers import Controller
from .fragment import Fragment
from .resources.registries import OperatorRegistry, ProviderRegistry
from .services import Service


class _ReconcilerCollector(ReconcilerCollector):
    def __init__(self) -> None: ...

    @override
    def add_task[T](
        self,
        key: type[T],
        function: ReconcilerTaskFn[T],
        phase: ReconcilerRunPhase = ReconcilerRunPhase.Setup,
        restart_policy: RestartPolicy = RestartPolicy.Never,
        conditions: list[str] | None = None,
    ) -> bool: ...

    @override
    def remove_task[T](
        self,
        key: type[T],
        function: ReconcilerTaskFn[T],
        phase: ReconcilerRunPhase = ReconcilerRunPhase.Setup,
    ) -> bool: ...


class Module(BaseModule):
    __slots__ = (
        '_components',
        '_controllers',
        '_fragments',
        '_injector',
        '_name',
        '_op_registry',
        '_parent',
        '_prov_registry',
        '_resources',
        '_services',
    )

    def __init__(
        self,
        name: str,
        parent: Module | None = None,
        fragments: Collection[Fragment] | None = None,
        components: Collection[Component] | None = None,
    ) -> None:
        self._name = name
        self._parent = parent
        self._services = MutDictRegistry[str, Service]()
        self._controllers = MutDictRegistry[str, Controller]()
        self._resources = MutDictRegistry[str, ResourceState]()
        self._injector = ParamsInjector()
        self._prov_registry = ProviderRegistry()
        self._op_registry = OperatorRegistry()
        self._fragments = {f.name: f for f in fragments} if fragments else {}
        self._components = {c.name: c for c in components} if components else {}

    @property
    @override
    def name(self) -> str:
        return self._name

    @property
    @override
    def full_path(self) -> str:
        if self._parent is None:
            return self._name
        return f'{self._parent.full_path}.{self._name}'

    def __repr__(self) -> str:
        return f'Module "{self.full_path}"'

    @override
    def get_component(self, name: str) -> Maybe[Component]:
        return Maybe(self._components.get(name))

    @override
    def setup(self) -> None:
        for _name, ctrl in self._controllers.list():
            ctrl.setup(self._op_registry, None)  # TODO
        for _name, svc in self._services.list():
            svc.setup(self._prov_registry, None)  # TODO
        for comp in self._components.values():
            comp.setup(self._op_registry, self._prov_registry)

    @override
    def teardown(self) -> None:
        for comp in reversed(self._components.values()):
            comp.teardown(self._op_registry, self._prov_registry)
        for _name, svc in reversed(list(self._services.list())):
            svc.teardown(self._prov_registry)
        for _name, ctrl in reversed(list(self._controllers.list())):
            ctrl.teardown(self._op_registry)

    def add_service(
        self,
        type_: type[Service],
        name: str | None = None,
        init_path: list[str] | None = None,
        **kwargs: Any,
    ) -> bool:
        if not name:
            name = type_.__name__

        if self._services.has(name):
            return False

        logger.info('{path}: Service "{name}" create'.format(path=self.full_path, name=name))

        factory = type_
        values = kwargs.copy()
        values['name'] = name

        if init_path:
            values['init_path'] = init_path

        types = {ResourceSelector: self._resources}
        injected = self._injector(factory, values, types)
        instance = factory(*injected.args, **injected.kwargs)

        logger.info('{path}: Service "{name}" created'.format(path=self.full_path, name=name))
        return self._services.add(name, instance)

    def add_controller(
        self,
        type_: type[Controller],
        name: str | None = None,
        init_path: list[str] | None = None,
        **kwargs: Any,
    ) -> bool:
        if not name:
            name = type_.__name__

        if self._controllers.has(name):
            return False

        logger.info('{path}: Controller "{name}" create'.format(path=self.full_path, name=name))

        factory = type_
        values = kwargs.copy()
        values['name'] = name

        if init_path:
            values['init_path'] = init_path

        types = {MutResourceSelector: self._resources}
        injected = self._injector(factory, values, types)
        instance = factory(*injected.args, **injected.kwargs)

        logger.info(
            '{path}: Controller "{name}" created'.format(path=self.full_path, name=name)
        )

        return self._controllers.add(name, instance)

    def remove_service(self, type_: type[Service], name: str | None = None) -> bool:
        if not name:
            name = type_.__name__

        if not self._services.has(name):
            return False

        instance = self._services.get(name).unwrap()
        return self._services.remove(name, instance)

    def remove_controller(self, type_: type[Controller], name: str | None = None) -> bool:
        if not name:
            name = type_.__name__

        if not self._controllers.has(name):
            return False

        instance = self._controllers.get(name).unwrap()
        return self._controllers.remove(name, instance)
