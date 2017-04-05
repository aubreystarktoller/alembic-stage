"""
Test the signal context register
"""


import random
import pytest


def test_empty_iter(signal_registry_class):
    """
    See what happens when iterate over a registry with noting
    registered
    """
    assert list(signal_registry_class()) == []


def test_register(signal_registry_class, contexts):
    """
    Ensure that callables are being assigned to the correct labels
    """
    reg = signal_registry_class()
    contexts.run(reg.register_context)
    assert list(reg) == contexts


def test_repeat_register(signal_registry_class, exceptions, hashable_object):
    """
    Ensure we get an error if we try and reuse a label
    """
    reg = signal_registry_class()

    func1 = lambda c: 1
    func2 = lambda c: 2

    reg.register_context(hashable_object, func1)
    with pytest.raises(exceptions.AlreadyRegistered) as excinfo:
        reg.register_context(hashable_object, func2)

    assert excinfo.value.name == hashable_object
    assert list(reg) == [(hashable_object, func1)]


def test_total_unregister(signal_registry_class, contexts):
    """
    See what happens after register all contexts we register
    """
    reg = signal_registry_class()
    contexts.run(reg.register_context)
    for label in contexts.labels:
        reg.unregister_context(label)
    assert list(reg) == []


def test_unregister(signal_registry_class, contexts):
    """
    See what happens after register some contexts
    """
    reg = signal_registry_class()
    contexts.run(reg.register_context)

    random.seed('mangoseed')
    labels = random.sample(contexts.labels, len(contexts.labels) // 2 + 1)

    for label in labels:
        reg.unregister_context(label)

    assert list(reg) == [e for e in contexts if e[0] not in labels]


def test_unregister_non_existant_context(
        signal_registry_class, exceptions, hashable_object):
    """
    What happens if unregister and context that has not been
    registered
    """
    reg = signal_registry_class()
    with pytest.raises(exceptions.NotRegistered) as excinfo:
        reg.unregister_context(hashable_object)

    assert excinfo.value.name == hashable_object
    assert list(reg) == []
