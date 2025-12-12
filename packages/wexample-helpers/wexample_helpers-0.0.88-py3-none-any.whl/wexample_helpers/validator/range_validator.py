from __future__ import annotations

from typing import Any

from wexample_helpers.classes.field import public_field
from wexample_helpers.decorator.base_class import base_class
from wexample_helpers.validator.abstract_validator import AbstractValidator


@base_class
class RangeValidator(AbstractValidator):
    max_value: int | float | None = public_field(
        default=None,
        description="Maximum allowed value (inclusive)",
    )
    min_value: int | float | None = public_field(
        default=None,
        description="Minimum allowed value (inclusive)",
    )

    def validate(self, value: Any) -> bool:
        """
        Validate that the value is within the specified range.

        Args:
            value: The value to validate (must be numeric)

        Returns:
            True if the value is within range, False otherwise
        """
        if not isinstance(value, (int, float)):
            return False

        if self.min_value is not None and value < self.min_value:
            return False

        if self.max_value is not None and value > self.max_value:
            return False

        return True

    def _get_default_error_message(self, value: Any) -> str:
        if self.min_value is not None and self.max_value is not None:
            return (
                f"Value {value} must be between {self.min_value} and {self.max_value}"
            )
        elif self.min_value is not None:
            return f"Value {value} must be at least {self.min_value}"
        elif self.max_value is not None:
            return f"Value {value} must be at most {self.max_value}"
        else:
            return f"Value {value} is invalid"
