from typing import Any

from pydantic import AliasChoices, BaseModel, Field, PrivateAttr, model_validator

from ..runtime.invoke import caller_path
from ..services import Service


class SvcConf(BaseModel, frozen=True):
    type_: type[Service] = Field(validation_alias=AliasChoices('type'))
    name: str | None = None
    args: dict[str, Any] = Field(default_factory=dict)
    enabled: bool = Field(default=True)
    _init_path: list[str] = PrivateAttr(default_factory=lambda: caller_path(5))

    @model_validator(mode='before')
    def _setup_name(self: dict[str, Any]) -> dict:
        if 'name' not in self:
            self['name'] = self['type'].__name__
        return self

    @property
    def init_path(self) -> list[str]:
        return self._init_path.copy()
