from __future__ import annotations

from typing import Any

from .attrs_inheritance_config import AttrsInheritanceConfig
from .attrs_inheritance_model import AttrsInheritanceModel


class AttrsInheritanceMain(AttrsInheritanceConfig, AttrsInheritanceModel):
    """Main class demonstrating multiple inheritance with attrs and mixins."""

    def __init__(self, **data) -> None:
        # Initialize attrs model first (it expects fields as kwargs)
        AttrsInheritanceModel.__init__(
            self,
            name=data.get("name", ""),
            tags=data.get("tags", []),
            description=data.get("description"),
            version=data.get("version", "1.0.0"),
            enabled=data.get("enabled", True),
            priority=data.get("priority", 0),
        )
        # Then initialize config
        AttrsInheritanceConfig.__init__(
            self, environment=data.get("environment", "development")
        )

    def get_full_state(self) -> dict[str, Any]:
        return {
            "environment": self.environment,
            "name": self.name,
            "version": self.version,
            "tags": self.tags,
            "description": self.description,
            "enabled": self.enabled,
            "priority": self.priority,
            "created_at": self.created_at,
            "metadata": self.get_metadata(),
        }
