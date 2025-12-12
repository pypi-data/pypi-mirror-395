from __future__ import annotations

import uuid
from typing import Any


class UndefinedException(Exception):
    """Base exception class for all application exceptions.

    Provides enhanced functionality including:
    - Unique error codes
    - Structured error data using TypedDict
    - Error chaining (cause/previous)
    - Serialization support
    """

    # Class-level error code, should be overridden by subclasses
    error_code: str = "UNDEFINED_ERROR"

    def __init__(
        self,
        message: str,
        data: dict[str, Any] | None = None,
        cause: Exception | None = None,
        previous: Exception | None = None,
    ) -> None:
        self.message = message
        self.data = data or {}
        self.cause = cause
        self.previous = previous
        self.exception_id = str(uuid.uuid4())
        super().__init__(self.message)

    def __repr__(self) -> str:
        """Return a detailed string representation of the exception."""
        parts = [
            f"{self.__class__.__name__}(",
            f"  error_code={self.error_code!r}",
            f"  message={self.message!r}",
            f"  exception_id={self.exception_id!r}",
        ]
        if self.data:
            parts.append(f"  data={self.data!r}")
        if self.cause:
            parts.append(f"  cause={self.cause!r}")
        if self.previous:
            parts.append(f"  previous={self.previous!r}")
        parts.append(")")
        return "\n".join(parts)

    def to_dict(self) -> dict[str, Any]:
        """Convert exception to dictionary for serialization."""
        result = {
            "error_code": self.error_code,
            "message": self.message,
            "exception_id": self.exception_id,
        }

        if self.data:
            result["data"] = self.data

        if self.cause:
            result["cause"] = str(self.cause)

        return result

    def with_data(self, **kwargs) -> UndefinedException:
        """Add additional data to the exception."""
        self.data.update(kwargs)
        return self
