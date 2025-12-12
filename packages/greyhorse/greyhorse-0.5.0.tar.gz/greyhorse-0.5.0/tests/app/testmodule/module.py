from greyhorse.app.schemas.components import ComponentConf, ModuleConf
from greyhorse.app.schemas.elements import CtrlConf, SvcConf

from .common.functional import FunctionalOperator
from .components.functional import DictResourceCtrl, FunctionalService, TestLifetime
from .components.resources import DictProviderService


def __init__() -> ModuleConf:  # noqa: N807
    return ModuleConf(
        enabled=True,
        provides=FunctionalOperator,
        fragments=['frag1'],
        components={
            'domain': ComponentConf(enabled=True, services=[SvcConf(type=DictProviderService)]),
            'functional': ComponentConf(
                enabled=True,
                scope_class=TestLifetime,
                controllers=[CtrlConf(type=DictResourceCtrl)],
                services=[SvcConf(type=FunctionalService)],
            ),
        },
    )
