from __future__ import annotations

import re
from typing import Any

from wexample_helpers.classes.field import public_field
from wexample_helpers.classes.private_field import private_field
from wexample_helpers.decorator.base_class import base_class
from wexample_helpers.validator.abstract_validator import AbstractValidator


@base_class
class RegexValidator(AbstractValidator):
    flags: int = public_field(
        default=0,
        description="Regular expression flags (e.g., re.IGNORECASE)",
    )
    pattern: list[str] | str = public_field(
        description="Regular expression pattern or list of regular expressions pattern to match against (OR logic)",
    )
    _patterns: list[str] = private_field(
        factory=list,
        description="List of regular expression patterns to match against (OR logic)",
    )

    def __attrs_post_init__(self) -> None:
        if isinstance(self.pattern, str):
            self._patterns = [self.pattern]
        else:
            self._patterns = self.pattern

        self._compiled_patterns = [
            re.compile(pattern, self.flags) for pattern in self._patterns
        ]

    def validate(self, value: Any) -> bool:
        """
        Validate that the value matches at least one of the regex patterns.

        Args:
            value: The value to validate (must be a string)

        Returns:
            True if the value matches at least one pattern, False otherwise
        """
        if not isinstance(value, str):
            return False

        return any(
            compiled_pattern.match(value) is not None
            for compiled_pattern in self._compiled_patterns
        )

    def _get_default_error_message(self, value: Any) -> str:
        if len(self._patterns) == 1:
            return f"Value '{value}' does not match pattern '{self._patterns[0]}'"
        else:
            patterns_str = "', '".join(self._patterns)
            return (
                f"Value '{value}' does not match any of the patterns: '{patterns_str}'"
            )
