from __future__ import annotations

from collections.abc import Callable
from typing import TYPE_CHECKING, Any

import attrs

from wexample_helpers.classes.base_field import BaseField

if TYPE_CHECKING:
    from collections.abc import Callable

    from wexample_helpers.enums.field_visibility import FieldVisibility


def public_field(
    description: str,
    validator: None | Callable | list[Callable] = None,
    default: Any = attrs.NOTHING,
    **kwargs,
) -> Any:
    """Create a public field."""
    return Field(
        description, validator=validator, default=default, **kwargs
    ).to_attrs_field()


class Field(BaseField):
    """Standard public field."""

    @property
    def visibility(self) -> FieldVisibility:
        from wexample_helpers.enums.field_visibility import FieldVisibility

        return FieldVisibility.PUBLIC
