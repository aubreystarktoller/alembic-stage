from typing import Any, Callable, Iterator, Hashable, Tuple
from .type_definitions import SignalContext


class Registry:
    def __init__(self) -> None:
        ...

    def register_context(self, label:Hashable, callable:SignalContext, weak:bool) -> None:
        ...

    def unregister_context(self, label:Hashable) -> None:
        ...

    def _clear_dead_references(self) -> None:
        ...

    def _broken_reference(self) -> None:
        ...

    def __iter__(self) -> Iterator[Tuple[Hashable, SignalContext]]:
        ...
