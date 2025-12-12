from typing import Protocol, runtime_checkable

@runtime_checkable
class Stringable(Protocol):
    def __str__(self) -> str: ...