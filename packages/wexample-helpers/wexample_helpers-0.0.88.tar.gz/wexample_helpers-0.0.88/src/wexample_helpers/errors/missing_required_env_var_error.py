from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from wexample_helpers.const.types import StringsList


class MissingRequiredEnvVarError(Exception):
    """Custom exception raised when required environment variables are missing."""

    def __init__(self, missing_keys: StringsList) -> None:
        self.missing_keys = missing_keys
        message = f"Missing required environment variables: {', '.join(missing_keys)}"
        super().__init__(message)
