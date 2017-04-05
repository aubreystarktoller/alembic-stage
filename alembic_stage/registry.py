"""
Implements the SignalContextRegistry that is used to register signal
contexts
"""


import collections
import threading

from . import exceptions


class SignalContextRegistry(object):
    """
    Used to register and access signal contexts
    """
    def __init__(self):
        self._register = collections.OrderedDict()
        self.lock = threading.Lock()

    def register_context(self, label, callable_obj):
        """
        Register a signal context.

        :param label:
            a hashable object that will be used to reference the
            context. AlreadyRegistered is raised if the label has
            already been used.
        :param callable_obj:
            a callable that will be called whenever a new stage is
            created. This callable will be passed the stage context
            and it's return value will be exposed to the appropriate
            receivers.
        :return: Returns nothing
        """
        with self.lock:
            if label in self._register:
                raise exceptions.AlreadyRegistered(label)
            else:
                self._register[label] = callable_obj

    def unregister_context(self, label):
        """
        Unregister a signal context

        :param label:
            the hashable object that the context was registered
            under. NotRegisteredis raised is the label does not
            currently refer to any context.
        :return: Returns nothing
        """
        with self.lock:
            if label in self._register:
                del self._register[label]
            else:
                raise exceptions.NotRegistered(label)

    def __iter__(self):
        return iter(self._register.copy().items())
