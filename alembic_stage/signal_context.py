"""
Implements the signal context which is exposed to recievers when
signals are sent
"""

from contextlib import contextmanager
from . import exceptions


class Interface(object):
    """
    The interface exposed to recievers
    """
    _ctx = None

    def __init__(self, ctx):
        self._ctx = ctx

    def __getitem__(self, label):
        return self._ctx[label]

    def __setattr__(self, name, value):
        if self._ctx is None:
            super(Interface, self).__setattr__(name, value)
        else:
            raise AttributeError("Interface has no attribute '{}'".format(name))

    def __delattr__(self, name):
        raise AttributeError("Interface has no attribute '{}'".format(name))


class SignalContext(object):
    def __init__(self):
        self._constrict = None
        self._store = {}
        self._interface = Interface(self)

    @property
    def interface(self):
        """
        Read only accessor to the context's interface
        """
        return self._interface

    def populate(self, register, stage_context):
        """
        Populate the context using the provided register
        """
        for name, init_func in register:
            self[name] = init_func(stage_context)

    @contextmanager
    def constrict(self, names):
        """
        Within this context only the specified keys may be accessed

        :param keys:
        Any iterable object that yields the keys that are allowed to be
        accessed within the context
        """
        self._constrict = set(names)
        yield
        self._constrict = None

    def __setitem__(self, name, value):
        self._store[name] = value

    def __getitem__(self, name):
        if self._constrict is None or name in self._constrict:
            return self._store[name]
        else:
            raise KeyError(name)

    def __delitem__(self, name):
        del self._store[name]
