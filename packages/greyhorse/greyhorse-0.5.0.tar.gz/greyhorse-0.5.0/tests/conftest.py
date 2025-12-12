from functools import partial
from typing import Any

import pytest

from greyhorse.run import wrap_async, wrap_sync
from greyhorse.utils.types import is_awaitable


@pytest.fixture(scope='session', autouse=True)
def setup_runtime(request: Any) -> None:
    print('setup_runtime called')

    session = request.node

    for item in session.items:
        match item:
            case pytest.Function() as func:
                if is_awaitable(func.obj):
                    func.obj = partial(wrap_async, func.obj)
                else:
                    func.obj = partial(wrap_sync, func.obj)
