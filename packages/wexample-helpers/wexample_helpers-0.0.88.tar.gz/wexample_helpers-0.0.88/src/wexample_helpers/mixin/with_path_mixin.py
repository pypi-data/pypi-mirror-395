from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Any

from wexample_helpers.classes.base_class import BaseClass
from wexample_helpers.classes.field import public_field
from wexample_helpers.decorator.base_class import base_class

if TYPE_CHECKING:
    from wexample_helpers.const.types import PathOrString


@base_class
class WithPathMixin(BaseClass):
    path: Path | str | None = public_field(
        description="The path of the file or directory", default=None
    )

    def get_path(self) -> Any:
        assert self.path is not None
        return self.path

    def set_path(self, path: PathOrString | None) -> None:
        from pathlib import Path

        self.path = None if path is None else Path(path)

    def _check_exists(self) -> None:
        """If check_exists is True, ensure the path exists."""
        from wexample_helpers.exception.local_path_not_found_exception import (
            LocalPathNotFoundException,
        )

        if not self.path.exists():
            # Defer to subclass to choose the most specific exception
            exc = self._not_found_exc()
            if exc is None:
                # Fallback to a generic not-found exception
                raise LocalPathNotFoundException(self.path)
            raise exc

    def _not_found_exc(self) -> Exception | None:
        """Return a specific 'not found' exception instance for this item type.

        Subclasses should return an instance of a custom exception that best
        represents the missing path for their type (e.g., FileNotFoundException
        or DirectoryNotFoundException). Returning None will make the base class
        fall back to LocalPathNotFoundException.
        """
