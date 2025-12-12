from collections.abc import Collection

from greyhorse.app.abc.module import Module
from greyhorse.error import Error, ErrorCase
from greyhorse.logging import logger
from greyhorse.result import Err, Ok, Result

from ..component import Component
from ..fragment import Fragment
from ..module import Module as _Module
from ..schemas.component import ComponentConf, ModuleComponentConf, ModuleConf
from .loader import ModuleLoader


class ModuleBuildError(Error):
    namespace = 'greyhorse.app.builders.module'

    Disabled = ErrorCase(msg='Module is disabled: "{path}"', path=str)
    Factory = ErrorCase(
        msg='Module factory error: "{path}", details: "{details}"', path=str, details=str
    )
    LoadError = ErrorCase(
        msg='Load error in component: "{path}", details: "{details}"', path=str, details=str
    )
    UnloadError = ErrorCase(
        msg='Unload error in component: "{path}", details: "{details}"', path=str, details=str
    )
    ComponentError = ErrorCase(
        msg='Component error in module: "{path}" "{name}", details: "{details}"',
        path=str,
        name=str,
        details=str,
    )


class ComponentBuildError(Error):
    namespace = 'greyhorse.app.builders.component'

    Disabled = ErrorCase(msg='Component is disabled: "{path}" "{name}"', path=str, name=str)
    Factory = ErrorCase(
        msg='Component factory error: "{path}" "{name}", details: "{details}"',
        path=str,
        name=str,
        details=str,
    )
    Submodule = ErrorCase(
        msg='Component submodule error: "{path}" "{name}", details: "{details}"',
        path=str,
        name=str,
        details=str,
    )


class ModuleBuilder:
    __slots__ = ('_conf', '_name', '_path')

    def __init__(self, conf: ModuleConf, path: str, name: str) -> None:
        self._conf = conf
        self._path = path
        self._name = name

    def create_pass(self) -> Result[Module, ModuleBuildError]:
        if not self._conf.enabled:
            return ModuleBuildError.Disabled(path=self._path).to_result()

        logger.info('{path}: Module create'.format(path=self._path))

        fragments = [ft() for ft in self._conf.fragments]

        if not (res := self._create_components(fragments)):
            return res  # type: ignore

        components = res.unwrap()

        try:
            instance = _Module(name=self._name, fragments=fragments, components=components)

        except Exception as e:
            error = ModuleBuildError.Factory(path=self._path, details=str(e))
            logger.error(error.message)
            return error.to_result()

        for ctrl_conf in self._conf.controllers:
            if not ctrl_conf.enabled:
                continue
            if instance.add_controller(
                ctrl_conf.type_, ctrl_conf.name, init_path=ctrl_conf.init_path, **ctrl_conf.args
            ):
                logger.info(
                    '{path}: Module "{name}": Added controller "{ctrl}"'.format(
                        path=self._path, name=self._name, ctrl=ctrl_conf.name
                    )
                )

        for svc_conf in self._conf.services:
            if not svc_conf.enabled:
                continue
            if instance.add_service(
                svc_conf.type_, svc_conf.name, init_path=svc_conf.init_path, **svc_conf.args
            ):
                logger.info(
                    '{path}: Module "{name}": Added service "{svc}"'.format(
                        path=self._path, name=self._name, svc=svc_conf.name
                    )
                )

        logger.info('{path}: Module created successfully'.format(path=self._path))
        return Ok(instance)

    def destroy_pass(self, instance: Module) -> Result[None, ModuleBuildError]:
        if not self._conf.enabled:
            return ModuleBuildError.Disabled(path=self._path).to_result()

        logger.info('{path}: Module destroy'.format(path=self._path))

        for svc_conf in self._conf.services:
            if not svc_conf.enabled:
                continue
            if instance.remove_service(svc_conf.type_, svc_conf.name):
                logger.info(
                    '{path}: Module "{name}": Removed service "{svc}"'.format(
                        path=self._path, name=self._name, svc=svc_conf.name
                    )
                )

        for ctrl_conf in self._conf.controllers:
            if not ctrl_conf.enabled:
                continue
            if instance.remove_controller(ctrl_conf.type_, ctrl_conf.name):
                logger.info(
                    '{path}: Module "{name}": Removed controller "{ctrl}"'.format(
                        path=self._path, name=self._name, ctrl=ctrl_conf.name
                    )
                )

        if not (res := self._destroy_components()):
            return res

        logger.info('{path}: Module destroyed successfully'.format(path=self._path))
        return Ok()

    def _create_component(
        self, name: str, conf: ComponentConf, fragments: Collection[Fragment]
    ) -> Result[Component, ComponentBuildError]:
        if not conf.enabled:
            return ComponentBuildError.Disabled(path=self._path, name=name).to_result()

        logger.info('{path}: Component "{name}" creation'.format(path=self._path, name=name))

        filtered_fragments = tuple(f for f in fragments if type(f) in conf.fragments)

        try:
            instance = Component(name=name, fragments=filtered_fragments, exports=conf.exports)

        except Exception as e:
            error = ComponentBuildError.Factory(path=self._path, name=name, details=str(e))
            logger.error(error.message)
            return error.to_result()

        logger.info(
            '{path}: Component "{name}" created successfully'.format(path=self._path, name=name)
        )

        return Ok(instance)

    def _create_module_component(
        self, name: str, conf: ModuleComponentConf
    ) -> Result[Component, ComponentBuildError]:
        if not conf.enabled:
            return ComponentBuildError.Disabled(path=self._path, name=name).to_result()

        logger.info(
            '{path}: Module component "{name}" create'.format(path=self._path, name=name)
        )

        if not (
            res := load_module(f'{self._path}.{name}', conf).map_err(
                lambda err: ComponentBuildError.Submodule(
                    path=self._path, name=name, details=err.message
                )
            )
        ):
            return res  # type: ignore

        res.unwrap()

        try:
            # TODO
            instance = Component(name=name)

        except Exception as e:
            error = ComponentBuildError.Factory(path=self._path, name=name, details=str(e))
            logger.error(error.message)
            return error.to_result()

        logger.info(
            '{path}: Module component "{name}" created successfully'.format(
                path=self._path, name=name
            )
        )

        return Ok(instance)

    def _create_components(
        self, fragments: Collection[Fragment]
    ) -> Result[list[Component], ModuleBuildError]:
        result = []

        for name, conf in self._conf.components.items():
            match conf:
                case ModuleComponentConf() as conf:
                    match self._create_module_component(name, conf):
                        case Ok(component):
                            result.append(component)

                        case Err(e):
                            match e:
                                case ComponentBuildError.Disabled(_):
                                    logger.info(e.message)
                                case _:
                                    error = ModuleBuildError.ComponentError(
                                        path=self._path, name=name, details=e.message
                                    )
                                    logger.error(error.message)
                                    return error.to_result()

                case ComponentConf() as conf:
                    match self._create_component(name, conf, fragments):
                        case Ok(component):
                            result.append(component)

                        case Err(e):
                            match e:
                                case ComponentBuildError.Disabled(_):
                                    logger.info(e.message)
                                case _:
                                    error = ModuleBuildError.ComponentError(
                                        path=self._path, name=name, details=e.message
                                    )
                                    logger.error(error.message)
                                    return error.to_result()

        return Ok(result)

    def _destroy_components(self) -> Result[None, ModuleBuildError]:
        for name, conf in reversed(self._conf.components.items()):
            if not conf.enabled:
                return ComponentBuildError.Disabled(path=self._path, name=name).to_result()

            match conf:
                case ComponentConf():
                    pass

                case ModuleComponentConf() as conf:
                    logger.info(
                        '{path}: Module component "{name}" destroy'.format(
                            path=self._path, name=name
                        )
                    )

                    if not (
                        res := unload_module(f'{self._path}.{name}', conf).map_err(
                            lambda e: ModuleBuildError.UnloadError(
                                path=self._path, details=e.message
                            )
                        )
                    ):
                        return res

                    logger.info(
                        '{path}: Module component "{name}" destroyed successfully'.format(
                            path=self._path, name=name
                        )
                    )

        return Ok()


def load_module(path: str, conf: ModuleComponentConf) -> Result[Module, ModuleBuildError]:
    loader = ModuleLoader()

    if not (
        res := loader.load_pass(conf).map_err(
            lambda e: ModuleBuildError.LoadError(path=conf.path, details=e.message)
        )
    ):
        return res  # type: ignore

    module_conf = res.unwrap()
    builder = ModuleBuilder(module_conf, path, conf.name)

    if not (res := builder.create_pass()):
        return res

    module = res.unwrap()
    return Ok(module)


def unload_module(
    path: str, conf: ModuleComponentConf, instance: Module
) -> Result[None, ModuleBuildError]:
    builder = ModuleBuilder(conf._conf, path)  # noqa

    if not (res := builder.destroy_pass(instance)):
        return res

    loader = ModuleLoader()

    return loader.unload_pass(conf).map_err(  # type: ignore
        lambda e: ModuleBuildError.UnloadError(path=conf.path, details=e.message)
    )
