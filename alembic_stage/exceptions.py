"""
Exceptions for alembic-stage
"""

class AlembicStageException(Exception):
    """
    Base class for all exceptions thrown by alebmic-stage
    """
    pass


class RegistryException(AlembicStageException):
    """
    Base class for all exceptions thrown by the context registry
    """
    def __init__(self, name):
        self.name = name
        super(RegistryException, self).__init__()


class AlreadyRegistered(RegistryException):
    """
    Raised when a context is registered using a label that has already
    been used
    """


class NotRegistered(RegistryException):
    """
    Raised when at attempt to retrieve to access a context is made, but
    the label used does not exist in the registry
    """

class ImmutableContext(AlembicStageException):
    """
    Raised by the context classes when forbidden operations are
    attempted
    """
