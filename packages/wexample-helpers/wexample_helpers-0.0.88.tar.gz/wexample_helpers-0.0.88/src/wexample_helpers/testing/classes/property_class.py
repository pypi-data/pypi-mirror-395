from __future__ import annotations


class PropertyClass:
    def __init__(self) -> None:
        self._value = None

    @property
    def value(self) -> None:
        """Get the value."""
        return self._value

    @value.setter
    def value(self, new_value) -> None:
        """Set the value."""
        self._value = new_value
