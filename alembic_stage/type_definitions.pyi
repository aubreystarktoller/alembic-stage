from typing import Any, Callable, TypeVar
from . import stage_context

T = TypeVar('T')

SignalContext = Callable[[stage_context.StageContext], Any]

Decorator = Callable[[T], T]
