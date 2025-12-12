from typing import Any, ForwardRef

from pydantic import BaseModel, Field, PrivateAttr

from ..fragment import Fragment
from ..runtime.invoke import caller_path
from .ctrl import CtrlConf
from .svc import SvcConf


class ComponentConf(BaseModel, frozen=True):
    enabled: bool = Field(default=True)
    fragments: list[type[Fragment]] = Field(default_factory=list)
    exports: list[type] = Field(default_factory=list)


class ModuleComponentConf(ComponentConf, frozen=True):
    name: str
    path: str = Field(frozen=True)
    args: dict[str, Any] = Field(default_factory=dict, frozen=True)
    _init_path: list[str] = PrivateAttr(default_factory=lambda: caller_path(5))
    _conf: ForwardRef('ModuleConf') | None = PrivateAttr(default=None)


class ModuleConf(BaseModel, frozen=True):
    enabled: bool = Field(default=True)

    controllers: list[CtrlConf] = Field(default_factory=list)
    services: list[SvcConf] = Field(default_factory=list)

    fragments: list[type[Fragment]] = Field(default_factory=list)
    components: dict[str, ComponentConf] = Field(default_factory=dict)
