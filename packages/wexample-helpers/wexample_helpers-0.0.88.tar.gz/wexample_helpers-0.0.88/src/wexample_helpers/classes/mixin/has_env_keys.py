from __future__ import annotations

from typing import TYPE_CHECKING, Any

from wexample_helpers.classes.base_class import BaseClass
from wexample_helpers.classes.field import public_field
from wexample_helpers.const.globals import UNSET
from wexample_helpers.decorator.base_class import base_class

if TYPE_CHECKING:
    from pathlib import Path

    from wexample_helpers.const.types import StringsList


@base_class
class HasEnvKeys(BaseClass):
    """Base mixin for environment variable validation."""

    env_config: dict[str, str | None] = public_field(
        factory=dict, description="The loaded environment configuration"
    )
    env_files_directory: None | str = public_field(
        description="The location of env files, may be different from the entrypoint",
        default=None,
    )

    def get_env_parameter(self, key: str, default: str | None = UNSET) -> Any:
        from wexample_helpers.errors.key_not_found_error import KeyNotFoundError

        if not key in self.env_config:
            if default is not UNSET:
                return default

            raise KeyNotFoundError(
                message=f"Environment variable is not defined",
                key=key,
                available_keys=list(self.env_config.keys()),
            )
        return self.env_config[key]

    def get_expected_env_keys(self) -> list[str]:
        """
        Returns a list of required environment variable keys.
        Should be overridden by child classes.
        """
        return []

    def set_env_parameter(self, key: str, value: str) -> None:
        """
        Set a single environment parameter in env_config.

        Args:
            key: The environment variable key
            value: The value to set
        """
        self.env_config[key] = value

    def set_env_parameters(self, parameters: dict[str, str]) -> None:
        """
        Set multiple environment parameters in env_config in batch.

        Args:
            parameters: Dictionary of key-value pairs to set
        """
        self.env_config.update(parameters)

    def _get_env_files_directory(self) -> Path:
        from pathlib import Path

        assert self.env_files_directory is not None
        return Path(self.env_files_directory)

    def _get_missing_env_keys(self, required_keys: StringsList) -> StringsList:
        """Check for missing environment variables in both os.environ and _env_values."""
        import os

        missing = []
        for key in required_keys:
            if not os.environ.get(key) and key not in self.env_config:
                missing.append(key)
        return missing

    def _init_env(self, env_dict: dict[str, str]) -> None:
        """
        Initialize environment values from an external source.

        Args:
            env_dict: Dictionary of environment variables
        """
        self.env_config = env_dict
        self._validate_env_keys()

    def _validate_env_keys(self) -> None:
        """
        Validates that all required environment variables are set.
        Raises MissingRequiredEnvVarError if any required variable is missing.
        """
        from wexample_helpers.errors.missing_required_env_var_error import (
            MissingRequiredEnvVarError,
        )

        missing_keys = self._get_missing_env_keys(self.get_expected_env_keys())

        if missing_keys:
            raise MissingRequiredEnvVarError(missing_keys)
