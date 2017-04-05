"""
Decorators used to register signal contexts and signals
"""


from . import registry


def signal_context(label=None):
    """
    Decorator that regsiters a callable as signal context
    """
    generate_label = label is None

    def _decorator(func):
        if generate_label:
            label = func.__module__ + '.' + func.__name__
        registry.register.register_context(label, func)
        return func
    return _decorator
