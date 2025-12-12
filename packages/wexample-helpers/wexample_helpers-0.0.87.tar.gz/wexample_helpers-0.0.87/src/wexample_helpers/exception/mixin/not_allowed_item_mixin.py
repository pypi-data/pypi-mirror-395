from __future__ import annotations


class NotAllowedItemMixin:
    """Mixin for exceptions related to items that are not allowed in a list of allowed items.

    This mixin provides utility methods to format error messages for cases where:
    1. A provided item is not found in a list of allowed items
    2. A required item was not provided at all
    """

    @staticmethod
    def format_not_allowed_item_message(
        item_type: str, item_value: str | None, allowed_values: list[str]
    ) -> str:
        """Format an error message for an item that is not allowed or not provided.

        Args:
            item_type: The type of item (e.g., 'format', 'option', 'value', 'addon')
            item_value: The value of the item that is not allowed, or None if not provided
            allowed_values: List of allowed values for this item type

        Returns:
            A formatted error message
        """
        if item_value is None:
            output = f"No {item_type} was provided."
        else:
            output = f"The {item_type} '{item_value}' is not allowed."

        if allowed_values:
            values_str = "', '".join(allowed_values)
            output += f" Allowed values are: '{values_str}'."
        else:
            output += " No suggested allowed values available."

        return output

    @staticmethod
    def get_not_allowed_item_data(
        item_type: str, item_value: str | None, allowed_values: list[str]
    ) -> dict:
        """Get structured data for a not allowed item exception.

        Args:
            item_type: The type of item (e.g., 'format', 'option', 'value', 'addon')
            item_value: The value of the item that is not allowed, or None if not provided
            allowed_values: List of allowed values for this item type

        Returns:
            A dictionary with structured data about the error
        """
        return {
            "item_type": item_type,
            "item_value": item_value,
            "allowed_values": allowed_values,
            "is_missing": item_value is None,
        }
