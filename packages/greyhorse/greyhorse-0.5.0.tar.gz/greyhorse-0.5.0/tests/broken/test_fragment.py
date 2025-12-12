from greyhorse.app.entities.fragment import Fragment
from greyhorse.factory import into_factory


def test_fragment_factory() -> None:
    fragment = Fragment('test', 'name')

    assert not fragment.has_factory(int)
    assert fragment.get_factory(int).is_nothing()

    assert fragment.add_factory(int, into_factory(lambda: 123, int))

    assert fragment.has_factory(int)
    assert fragment.get_factory(int).is_just()

    f = fragment.get_factory(int).unwrap()
    assert f() == 123

    assert fragment.remove_factory(int)

    assert not fragment.has_factory(int)
    assert fragment.get_factory(int).is_nothing()


def test_fragment_context() -> None:
    fragment = Fragment('test', 'name')

    assert not fragment.has_factory(int)
    assert fragment.get_factory(int).is_nothing()

    assert fragment.add_factory(int, into_factory(lambda: 123, int))

    assert fragment.has_factory(int)
    assert fragment.get_factory(int).is_just()

    with fragment.get_context() as selector:
        assert selector.has(int)
        assert selector.get(int).unwrap() == 123

    assert fragment.remove_factory(int)

    assert not fragment.has_factory(int)
    assert fragment.get_factory(int).is_nothing()
