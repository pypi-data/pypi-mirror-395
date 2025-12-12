from __future__ import annotations

from pathlib import Path

from wexample_helpers.classes.base_class import BaseClass
from wexample_helpers.classes.field import public_field
from wexample_helpers.const.types import PathOrString
from wexample_helpers.decorator.base_class import base_class


@base_class
class WithEntrypointPathMixin(BaseClass):
    entrypoint_path: PathOrString = public_field(
        description="The main file placed at application root directory"
    )

    def __attrs_post_init__(self) -> None:
        # Ensure this is always a path
        self.entrypoint_path = Path(self.entrypoint_path)
