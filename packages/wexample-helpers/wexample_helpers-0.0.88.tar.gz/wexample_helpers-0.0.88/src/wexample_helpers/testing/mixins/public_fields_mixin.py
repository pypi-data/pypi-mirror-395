from __future__ import annotations

from .base_mixin import BaseMixin


class PublicFieldsMixin(BaseMixin):
    """Mixin providing public fields template."""

    description: str | None
    name: str
    tags: list[str]
    version: str = "1.0.0"
