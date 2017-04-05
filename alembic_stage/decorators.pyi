from typing import Any, Callable, Iterator, Hashable, Tuple, Optional
from .type_definitions import Decorator, SignalContext, T


def signal_context(name: Optional[Hashable]) -> Decorator[SignalContext]:
    ...
