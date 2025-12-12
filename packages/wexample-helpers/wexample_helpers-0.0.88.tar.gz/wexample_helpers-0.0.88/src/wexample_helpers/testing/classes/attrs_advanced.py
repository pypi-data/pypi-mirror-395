from __future__ import annotations

from datetime import timedelta
from enum import Enum
from typing import TYPE_CHECKING

from attrs.validators import ge, le

from wexample_helpers.classes.base_class import BaseClass
from wexample_helpers.classes.field import public_field
from wexample_helpers.classes.private_field import private_field
from wexample_helpers.decorator.base_class import base_class

if TYPE_CHECKING:
    from datetime import datetime, timedelta


class Status(Enum):
    ACTIVE = "active"
    PENDING = "pending"
    INACTIVE = "inactive"


@base_class
class AttrsAdvanced(BaseClass):
    """An attrs-based equivalent of the former PydanticAdvanced."""

    # Public fields
    id: str = public_field(
        description="Unique identifier of the object",
    )
    metadata: dict[str, str | int | bool] = public_field(
        factory=dict,
        description="Arbitrary metadata attached to the object",
    )
    score: float = public_field(
        default=0.0,
        converter=lambda v: round(float(v), 2),
        validator=[ge(0), le(100)],
        description="Score value between 0 and 100, rounded to 2 decimals",
    )
    status: Status = public_field(
        default=Status.PENDING,
        description="Current status of the object",
    )
    _created_at: datetime = private_field(
        factory=datetime.now,
        description="Timestamp when the object was created",
    )
    _internal_notes: list[str] = private_field(
        factory=list,
        description="Internal list of notes not exposed publicly",
    )
    _secret_key: str = private_field(
        default="private",
        description="Internal secret key used for private state",
    )

    # Note: range validation is handled by attrs validators and rounding by the converter above.
    @property
    def age(self) -> timedelta:
        from datetime import datetime

        return datetime.now() - self._created_at

    @property
    def is_active(self) -> bool:
        return self.status == Status.ACTIVE

    @property
    def notes(self) -> list[str]:
        return list(self._internal_notes)

    @notes.setter
    def notes(self, value: list[str]) -> None:
        self._internal_notes = [note.strip() for note in value]
