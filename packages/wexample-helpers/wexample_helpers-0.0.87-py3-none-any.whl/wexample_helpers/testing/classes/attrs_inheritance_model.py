from __future__ import annotations

from ...classes.base_class import BaseClass
from ...classes.field import public_field
from ...decorator.base_class import base_class
from ..mixins.private_fields_mixin import PrivateFieldsMixin
from ..mixins.public_fields_mixin import PublicFieldsMixin


@base_class
class AttrsInheritanceModel(PublicFieldsMixin, PrivateFieldsMixin, BaseClass):
    """attrs model combining both mixins with additional functionality."""

    description: str | None = public_field(
        default=None,
        description="Optional text description of the model",
    )
    enabled: bool = public_field(
        default=True,
        description="Indicates whether the model is enabled",
    )
    name: str = public_field(
        default="",
        description="Name of the model, required by PublicFieldsMixin",
    )
    priority: int = public_field(
        default=0,
        description="Priority value used for ordering or processing",
    )
    tags: list[str] = public_field(
        factory=list,
        description="List of tags associated with the model",
    )
    version: str = public_field(
        default="1.0.0",
        description="Version identifier of the model",
    )

    def __attrs_post_init__(self) -> None:
        # Initialize any mixin-specific stuff if needed
        self._metadata["initialized_at"] = self._created_at
