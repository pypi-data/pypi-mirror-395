from __future__ import annotations

from wexample_helpers.classes.base_class import BaseClass
from wexample_helpers.decorator.base_class import base_class


@base_class
class HasTwoStepInit(BaseClass):
    is_setup: bool = False

    def setup(self) -> HasTwoStepInit:
        self.is_setup = True
        return self
