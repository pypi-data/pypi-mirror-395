from __future__ import annotations

from wexample_helpers.classes.mixin.has_env_keys import HasEnvKeys
from wexample_helpers.decorator.base_class import base_class


@base_class
class HasEnvKeysFile(HasEnvKeys):
    """Mixin for classes that need to load env from files."""

    def _init_env_file(self, file_path: str) -> None:
        """
        Load environment variables from a file and validate them.

        Args:
            file_path: Path to the .env file
        """
        from dotenv import dotenv_values, load_dotenv

        load_dotenv(file_path)
        self.env_config.update(dotenv_values(file_path))
        self._validate_env_keys()
