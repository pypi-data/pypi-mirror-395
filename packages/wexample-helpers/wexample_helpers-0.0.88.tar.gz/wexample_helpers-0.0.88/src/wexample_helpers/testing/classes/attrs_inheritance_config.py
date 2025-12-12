from __future__ import annotations


class AttrsInheritanceConfig:
    """Simple configuration class with a basic property (attrs-neutral)."""

    def __init__(self, environment: str = "development") -> None:
        self._environment = environment

    @property
    def environment(self) -> str:
        return self._environment

    @environment.setter
    def environment(self, value: str) -> None:
        self._environment = value.lower()
