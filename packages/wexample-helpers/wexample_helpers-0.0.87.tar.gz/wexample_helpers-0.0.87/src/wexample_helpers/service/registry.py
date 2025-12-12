from __future__ import annotations

from typing import Any, Generic, TypeVar

from wexample_helpers.classes.field import public_field
from wexample_helpers.classes.private_field import private_field

RegistrableType = TypeVar("RegistrableType")

from wexample_helpers.decorator.base_class import base_class


@base_class
class Registry(Generic[RegistrableType]):
    """Generic registry for managing any type of data."""

    container: Any = public_field(description="The service container")
    _fail_if_missing: bool = private_field(
        description="Define if missing item is fatal or not", default=False
    )
    _items: dict[str, RegistrableType] | None = private_field(
        description="The items of the registry", factory=dict
    )

    def __init__(self, container: Any) -> None:
        self._items = {}
        self.container = container

    def all_keys(self) -> list[str]:
        return list(self._items.keys())

    def get(self, key: str, **kwargs) -> RegistrableType | None:
        """
        Retrieve an item by its key.
        Additional kwargs can be used by child classes.
        """
        item = self._items.get(key)
        self._raise_error_if_expected(key, item)

        return item

    def get_all(self) -> dict[str, RegistrableType]:
        """Get all items in the registry."""
        return self._items

    def has(self, key: str) -> bool:
        """Check if an item exists in the registry."""
        return key in self._items

    def register(self, key: str, item: RegistrableType) -> None:
        """Register an item in the registry."""
        self._items[key] = item

    def _raise_error_if_expected(self, key: str, item: Any) -> None:
        if item is None and self._fail_if_missing:
            available_keys = self.all_keys()
            raise KeyError(
                f"Item not found in registry: {key}. Available keys: {available_keys}"
            )
