from __future__ import annotations

from collections.abc import Callable
from typing import TYPE_CHECKING, Any

from wexample_helpers.classes.base_field import BaseField

if TYPE_CHECKING:
    from collections.abc import Callable

    from wexample_helpers.enums.field_visibility import FieldVisibility


def private_field(
    description: str, validator: Callable = None, init: bool = False, **kwargs
) -> Any:
    """Create a private field. Private fields have init=False by default."""
    return PrivateField(description, validator, init=init, **kwargs).to_attrs_field()


class PrivateField(BaseField):
    """Private field - must start with underscore."""

    @property
    def visibility(self) -> FieldVisibility:
        from wexample_helpers.enums.field_visibility import FieldVisibility

        return FieldVisibility.PRIVATE
