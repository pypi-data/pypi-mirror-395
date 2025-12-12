from __future__ import annotations

from typing import Any


class MultipleBaseModelInheritanceError(Exception):
    """Exception raised when multiple inheritance of BaseModel is detected."""

    def __init__(self, class_instance: Any) -> None:
        super().__init__(
            f"Multiple inheritance of BaseModel is not allowed in class '{class_instance.__name__}'."
        )
