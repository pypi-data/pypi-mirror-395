from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from datetime import datetime


class PrivateFieldsMixin:
    """Mixin providing private attributes template."""

    _created_at: datetime
    _metadata: dict[str, Any]
    _secret_key: str = "default-key"

    def __init__(self) -> None:
        from datetime import datetime

        self._created_at = datetime.now()
        self._metadata = {}

    @property
    def created_at(self) -> datetime:
        """Read-only access to creation time."""
        return self._created_at

    def get_metadata(self) -> dict[str, Any]:
        """Safe access to private metadata."""
        return self._metadata.copy()

    def set_metadata(self, key: str, value: Any) -> None:
        """Safely set metadata value."""
        self._metadata[key] = value
