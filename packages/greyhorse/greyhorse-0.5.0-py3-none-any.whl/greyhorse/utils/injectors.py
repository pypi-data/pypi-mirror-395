import inspect
from collections.abc import Callable, Mapping
from typing import Any

from greyhorse.app.abc.collections.selectors import Selector
from greyhorse.maybe import Nothing

from .types import is_maybe, is_optional, unwrap_maybe, unwrap_optional


TypeProviderFactory = Callable[[str, ...], Any]


class ParamsInjector:
    def __init__(self, type_selector: Selector[type, Any] | None = None) -> None:
        self._type_selector = type_selector

    def __call__(
        self,
        func: Callable[[...], ...],
        values: Mapping[str, Any] | None = None,
        types: Mapping[type, Any] | None = None,
    ) -> inspect.BoundArguments:
        values = values or {}
        types = types or {}

        sig = inspect.signature(func, eval_str=True)
        args = {}

        for k, v in sig.parameters.items():
            if k == 'values':
                args[k] = values
            elif v.annotation in types:
                args[k] = types[v.annotation]
            elif k in values:
                args[k] = values[k]
            elif self._type_selector:
                if value := self._type_selector.get(
                    unwrap_maybe(unwrap_optional(v.annotation))
                ):
                    args[k] = value if is_maybe(v.annotation) else value.unwrap()
                elif is_maybe(v):
                    args[k] = Nothing
                elif is_optional(v):
                    args[k] = None

        args = sig.bind_partial(**args)
        args.apply_defaults()
        return args
