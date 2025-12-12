from __future__ import annotations

from typing import TYPE_CHECKING

from wexample_helpers.classes.base_class import BaseClass
from wexample_helpers.classes.field import public_field
from wexample_helpers.decorator.base_class import base_class
from wexample_helpers.mixin.with_path_mixin import WithPathMixin

if TYPE_CHECKING:
    from wexample_helpers.classes.example.executor import Executor


@base_class
class Example(WithPathMixin, BaseClass):
    executor: Executor | None = public_field(
        default=None,
        description="Reference to the Executor managing this example instance.",
    )

    def execute(self) -> None:
        pass
