from __future__ import annotations

from typing import TYPE_CHECKING, Any

from wexample_helpers.classes.base_class import BaseClass
from wexample_helpers.decorator.base_class import base_class

if TYPE_CHECKING:
    from wexample_helpers.service.registry import Registry


@base_class
class RegistryContainerMixin(BaseClass):
    """Abstract container for managing multiple registries of any type."""

    _registries: dict[str, Registry] = {}

    def get_item(self, registry_name: str, key: str, **kwargs) -> Any | None:
        """Retrieve an item from a specific registry by its key."""
        registry = self.get_registry(registry_name)
        return registry.get(key, **kwargs)

    def get_registry(
        self, name: str, registry_class_type: type[Registry] | None = None
    ) -> Registry:
        """Get a registry by its name."""
        registry_name = f"_{name}_registry"
        if registry_name not in self._registries:
            return self.set_registry(registry_name, registry_class_type)
        return self._registries[registry_name]

    def register_item(self, registry_name: str, key: str, item: Any) -> Registry:
        """Register an item in a specific registry."""
        registry = self.get_registry(registry_name)
        registry.register(key, item)
        return registry

    def register_items(self, registry_name: str, items: list[Any]) -> Registry:
        """Register multiple items at once in a specific registry."""
        registry = self.get_registry(registry_name)
        for item in items:
            if hasattr(item, "get_snake_short_class_name"):
                key = item.get_snake_short_class_name()
            else:
                key = item.__name__
            registry.register(key, item)
        return registry

    def set_registry(
        self, name: str, registry_class_type: type[Registry] | None = None
    ) -> Registry:
        self._registries[name] = (
            registry_class_type or self._get_registry_class_type()
        )(container=self)
        return self._registries[name]

    def _get_registry_class_type(self) -> type[Registry]:
        """Get the type of registry to use. Must be overridden by child classes."""
        from wexample_helpers.service.registry import Registry

        return Registry
