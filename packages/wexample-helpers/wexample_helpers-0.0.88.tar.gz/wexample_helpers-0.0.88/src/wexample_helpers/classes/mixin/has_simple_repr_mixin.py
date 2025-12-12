from __future__ import annotations

from wexample_helpers.classes.base_class import BaseClass
from wexample_helpers.decorator.base_class import base_class


@base_class
class HasSimpleReprMixin(BaseClass):
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}"

    def __str__(self) -> str:
        return self.__repr__()
