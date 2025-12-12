from __future__ import annotations

from abc import abstractmethod
from typing import Any

from wexample_helpers.classes.base_class import BaseClass
from wexample_helpers.classes.field import public_field
from wexample_helpers.decorator.base_class import base_class


@base_class
class AbstractValidator(BaseClass):
    error_message: str | None = public_field(
        default=None,
        description="Custom error message to display when validation fails",
    )

    def get_error_message(self, value: Any) -> str:
        """
        Get the error message for a failed validation.

        Args:
            value: The value that failed validation

        Returns:
            Error message string
        """
        if self.error_message:
            return self.error_message
        return self._get_default_error_message(value)

    @abstractmethod
    def validate(self, value: Any) -> bool:
        """
        Validate the given value.

        Args:
            value: The value to validate

        Returns:
            True if validation passes, False otherwise
        """

    @abstractmethod
    def _get_default_error_message(self, value: Any) -> str:
        """
        Get the default error message when no custom message is provided.

        Args:
            value: The value that failed validation

        Returns:
            Default error message string
        """
