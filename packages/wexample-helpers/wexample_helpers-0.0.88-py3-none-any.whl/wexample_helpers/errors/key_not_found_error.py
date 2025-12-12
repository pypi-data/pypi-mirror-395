from __future__ import annotations


class KeyNotFoundError(Exception):
    """Exception raised when a key is not found in a list of available keys."""

    def __init__(self, message: str, key: str, available_keys: list[str]) -> None:
        """
        Initialize the exception with the missing key and available keys.

        :param key: The key that was not found
        :param available_keys: List of keys that are available
        """
        self.message = message
        self.key = key
        self.available_keys = available_keys
        super().__init__(self._build_message())

    def _build_message(self) -> str:
        """Build the error message including the missing key and available keys."""
        return f"{self.message}: '{self.key}'. Available keys: {self.available_keys}"
