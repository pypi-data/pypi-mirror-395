from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from wexample_helpers.classes.base_class import BaseClass
from wexample_helpers.classes.field import public_field
from wexample_helpers.decorator.base_class import base_class

if TYPE_CHECKING:
    from datetime import datetime


@base_class
class AttrsClass(BaseClass):
    """An attrs-based class with various field types.

    Mirrors the structure of PydanticClass for testing cattrs/attrs flows.
    """

    count: int = public_field(
        default=0,
        description="Counter value associated with the class instance",
    )
    created_at: datetime = public_field(
        factory=datetime.now,
        description="Timestamp when the instance was created",
    )
    description: str | None = public_field(
        default=None,
        description="Optional text description of the instance",
    )
    name: str = public_field(
        description="Required name of the instance",
    )
    tags: list[str] = public_field(
        factory=list,
        description="List of tags associated with the instance",
    )
