"""
Pytest test configuration file; implements hooks and common fixtures
"""


import importlib
import random
import collections
try:
    from unittest import mock
except ImportError:
    import mock
import pytest

HASHABLE_OBJECTS = (
    "test",
    frozenset(),
    True,
    5,
    (1, 2, 3)
)


@pytest.fixture()
def signal_registry_class():
    """
    Exposes the SignalContextRegistryClass
    """
    module = importlib.import_module('alembic_stage.registry')
    return module.SignalContextRegistry


@pytest.fixture()
def signal_context_class():
    """
    Exposes the SignalContextClass
    """
    module = importlib.import_module('alembic_stage.signal_context')
    return module.SignalContext


@pytest.fixture()
def exceptions():
    """
    Fixture that exposes the exceptions module
    """
    return importlib.import_module('alembic_stage.exceptions')


@pytest.fixture(params=HASHABLE_OBJECTS)
def hashable_object(request):
    """
    Fixture that provides a hashable object
    """
    return request.param


@pytest.fixture(params=[1, 2, 3, 4, 5])
def hashable_objects(request):
    """
    Fixture that provides lists of hashable objects of varying sizes
    """
    random.seed(request.param)
    return random.sample(HASHABLE_OBJECTS, request.param)


class ContextList(collections.UserList):
    """
    Helper class to handle context label/function pairs
    """
    def __init__(self):
        super(ContextList, self).__init__()

    def __repr__(self):
        return ', '.join(str(l) for l in self.labels)

    def strip_functions(self):
        """
        Derefence all functions
        """
        for item in self:
            del item[1]
            item.append(None)

    def append_context(self, label, func):
        """
        Add a context
        """
        self.data.append([label, func])

    @property
    def labels(self):
        """
        Returns a list of all current labels
        """
        return [l for l, _ in self]

    def __eq__(self, other):
        if isinstance(other, list):
            return [(k, v) for k, v in self.data] == other
        else:
            return self == other

    def __iter__(self):
        return iter([(k, v) for k, v in self.data])

    def run(self, func):
        """
        Call func for label/function pairs
        """
        for label, ctx_func in self:
            func(label, ctx_func)


@pytest.fixture(name='contexts')
def contexts_fixture(hashable_objects):
    """
    Fixture that provices a variable number of label/function
    pairs in a list
    """
    contexts = ContextList()
    for idx, hobj in enumerate(hashable_objects):
        contexts.append_context(hobj, lambda x, i=idx: i)
    return contexts


def pytest_namespace():
    """
    pytest hook
    """
    return {
        'local': type('LocalPytest', (object,), {
            'HASHABLE_OBJECTS': HASHABLE_OBJECTS,
            'mock': mock,
        })
    }
