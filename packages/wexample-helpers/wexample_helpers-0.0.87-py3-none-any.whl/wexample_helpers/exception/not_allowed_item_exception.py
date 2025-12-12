from __future__ import annotations

from wexample_helpers.exception.mixin.not_allowed_item_mixin import NotAllowedItemMixin
from wexample_helpers.exception.undefined_exception import UndefinedException


class NotAllowedItemException(UndefinedException, NotAllowedItemMixin):
    """Base exception for cases where an item is not allowed or not provided.

    This exception should be used when:
    1. A specific item value is not in a list of allowed values
    2. A required item was not provided at all
    """

    error_code: str = "NOT_ALLOWED_ITEM"

    def __init__(
        self,
        item_type: str,
        item_value: str | None = None,
        allowed_values: list[str] | None = None,
        cause: Exception | None = None,
        previous: Exception | None = None,
        message: str | None = None,
    ) -> None:
        from wexample_helpers.exception.model.not_allowed_item_data import (
            NotAllowedItemData,
        )

        if allowed_values is None:
            allowed_values = []

        # Create structured data using TypedDict
        data: NotAllowedItemData = {
            "item_type": item_type,
            "item_value": item_value,
            "allowed_values": allowed_values,
            "is_missing": item_value is None,
        }

        # Generate message using the mixin method
        message = message or self.format_not_allowed_item_message(
            item_type=item_type, item_value=item_value, allowed_values=allowed_values
        )

        super().__init__(
            message=message,
            data=data,
            cause=cause,
            previous=previous,
        )
