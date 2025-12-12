from typing import Protocol, Any, runtime_checkable

@runtime_checkable
class Memoable(Protocol):
    """
    Interface for objects that can capture and restore their internal state.
    """
    def copy(self) -> 'Memoable':
        """Produce a copy of this object with its current state."""
        ...

    def reset_from_memoable(self, other: 'Memoable') -> None:
        """Restore the state of this object from another object of the same type."""
        ...
