"""
Test the signal context class
"""


import random
import pytest
from pytest import local as l


@pytest.fixture(name="mock_register")
def mock_register_fixture():
    """
    Provides a mock register (a list of label/function pairs). Labels
    are the collection of hashable objects, functions are mock objects.
    Each mock object will return it's index in the register - mock
    function in first entry of the register will return 0, etc.
    """
    return [
        (h, l.mock.Mock(return_value=i))
        for i, h in enumerate(l.HASHABLE_OBJECTS)
    ]


def test_set(signal_context_class, hashable_objects):
    """
    Setter sanity test
    """
    obj = signal_context_class()
    for idx, hobj in enumerate(hashable_objects):
        obj[hobj] = idx


def test_set_and_get(signal_context_class, hashable_objects):
    """
    Ensure the value we get when we access a key is the one we set
    """
    obj = signal_context_class()
    for idx, hobj in enumerate(hashable_objects):
        obj[hobj] = idx
        assert obj[hobj] == idx

    for idx, hobj in enumerate(hashable_objects):
        assert obj[hobj] == idx


def test_get_nonexistant(signal_context_class, hashable_object):
    """
    Ensure a KeyError is thrown when a non-existant key is accessed
    """
    obj = signal_context_class()
    with pytest.raises(KeyError) as excinfo:
        obj[hashable_object] #pylint: disable=pointless-statement

    assert excinfo.value.args[0] == hashable_object


def test_constrict_get(signal_context_class, hashable_objects):
    """
    See what happens when constrict the keys available
    """
    obj = signal_context_class()
    for idx, hobj in enumerate(hashable_objects):
        obj[hobj] = idx

    random.seed('avocadoseed')
    permitted = random.sample(hashable_objects, len(hashable_objects) // 2 + 1)

    with obj.constrict(permitted):
        for idx, hobj in enumerate(hashable_objects):
            if hobj in permitted:
                assert obj[hobj] == hashable_objects.index(hobj)
            else:
                with pytest.raises(KeyError) as excinfo:
                    obj[hobj] #pylint: disable=pointless-statement

                assert excinfo.value.args[0] == hobj

    for idx, hobj in enumerate(hashable_objects):
        assert obj[hobj] == idx


def test_set_and_del(signal_context_class, hashable_objects):
    """
    Del santity check
    """
    obj = signal_context_class()
    for idx, hobj in enumerate(hashable_objects):
        obj[hobj] = idx
        del obj[hobj]


def test_set_and_del_and_get(signal_context_class, hashable_objects):
    """
    Make sure deleted values are gone
    """
    obj = signal_context_class()
    for idx, hobj in enumerate(hashable_objects):
        obj[hobj] = idx
        del obj[hobj]
        with pytest.raises(KeyError) as excinfo:
            obj[hobj] #pylint: disable=pointless-statement

        assert excinfo.value.args[0] == hobj


def test_set_and_interface_get(signal_context_class, hashable_objects):
    """
    Ensure the value we get when we access a key is the one we set
    """
    obj = signal_context_class()
    for idx, hobj in enumerate(hashable_objects):
        obj[hobj] = idx
        assert obj.interface[hobj] == idx

    for idx, hobj in enumerate(hashable_objects):
        assert obj.interface[hobj] == idx


def test_setitem_on_interface(signal_context_class, hashable_object):
    """
    Ensure we can't set any items on the interface
    """
    with pytest.raises(TypeError):
        signal_context_class().interface[hashable_object] = 'value'


def test_setattr_on_interface(signal_context_class):
    """
    Ensure we can't set any attributes on the interface
    """
    with pytest.raises(AttributeError):
        signal_context_class().interface.someattr = 'value'


def test_delattr_on_iterface(signal_context_class):
    """
    Ensure we can't delete any attributes on the interface
    """
    with pytest.raises(AttributeError):
        del signal_context_class().interface._ctx


def test_interface_get_nonexistant(signal_context_class, hashable_object):
    """
    Ensure a KeyError is thrown when a non-existant key is accessed on
    the interface
    """
    obj = signal_context_class()
    with pytest.raises(KeyError) as excinfo:
        obj.interface[hashable_object]  #pylint: disable=pointless-statement

    assert excinfo.value.args[0] == hashable_object


def test_constricted_interface_get(signal_context_class, hashable_objects):
    """
    See what happens when we constrict the keys available
    and access items from the interface
    """
    obj = signal_context_class()
    for idx, hobj in enumerate(hashable_objects):
        obj[hobj] = idx

    random.seed('avocadoseed')
    permitted = random.sample(hashable_objects, len(hashable_objects) // 2 + 1)

    with obj.constrict(permitted):
        for idx, hobj in enumerate(hashable_objects):
            if hobj in permitted:
                assert obj.interface[hobj] == hashable_objects.index(hobj)
            else:
                with pytest.raises(KeyError) as excinfo:
                    obj.interface[hobj]  #pylint: disable=pointless-statement

                assert excinfo.value.args[0] == hobj

    for idx, hobj in enumerate(hashable_objects):
        assert obj.interface[hobj] == idx


def test_populate(signal_context_class, mock_register):
    """
    Test populate with a mock register
    """
    obj = signal_context_class()
    stage_context = object()

    obj.populate(mock_register, stage_context)

    for _, mock_func in mock_register:
        mock_func.called_once_with(stage_context)


def test_populate_and_get(signal_context_class, mock_register):
    """
    Test populate with a mock register
    """
    obj = signal_context_class()
    stage_context = object()

    obj.populate(mock_register, stage_context)

    for idx, entry in enumerate(mock_register):
        hobj, _ = entry
        assert obj[hobj] == idx
