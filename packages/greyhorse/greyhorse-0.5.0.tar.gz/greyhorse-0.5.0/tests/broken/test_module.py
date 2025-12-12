from __future__ import annotations

from app.testmodule.module import __init__

from greyhorse.app.contexts import SyncContext
from greyhorse.app.private.builders.module import ModuleBuilder


def test_module() -> None:
    module_conf = __init__()

    module_builder = ModuleBuilder(module_conf, 'tests', 'test')
    res = module_builder.create_pass()
    assert res.is_ok()
    module = res.unwrap()

    ctx = module.make_facade()

    assert isinstance(ctx, SyncContext)

    with ctx as facade:
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

    res = module_builder.destroy_pass()
    assert res.is_ok()
