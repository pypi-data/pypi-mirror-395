from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

if TYPE_CHECKING:
    from wexample_helpers.const.types import StringKeysDict

T = TypeVar("T", bound="SerializableMixin")


class SerializableMixin:
    def hydrate(self, data: StringKeysDict) -> None:
        pass

    def serialize(self) -> StringKeysDict:
        return {}
