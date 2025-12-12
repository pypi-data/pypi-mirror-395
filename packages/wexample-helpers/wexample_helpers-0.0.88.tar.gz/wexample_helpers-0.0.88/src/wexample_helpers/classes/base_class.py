from __future__ import annotations

import inspect
from typing import TYPE_CHECKING, NoReturn

from wexample_helpers.decorator.base_class import base_class

if TYPE_CHECKING:
    pass


@base_class
class BaseClass:
    def __init_subclass__(cls, **kwargs) -> None:
        """Validate that all non-uppercase properties inherit from BaseField."""
        super().__init_subclass__(**kwargs)
        cls._validate_field_types()

    @classmethod
    def _raise_not_implemented_error(
        cls,
        method: str | None = None,
        message: str | None = None,
    ) -> NoReturn:
        """Convenience to raise a standardized NotImplementedError."""
        if method is None:
            try:
                method = inspect.stack()[1].function
            except Exception:
                method = "<unknown>"
        raise NotImplementedError(
            message or f"{cls.__name__}.{method} must be implemented by subclass"
        )

    @classmethod
    def _validate_field_types(cls) -> None:
        """Ensure all non-uppercase class attributes are BaseField instances."""
        # Import here to avoid circular imports
        from wexample_helpers.classes.base_field import BaseField

        # Get all class attributes (including inherited ones)
        for name, value in cls.__dict__.items():
            # Skip special attributes, methods, and uppercase constants
            if (
                name.startswith("_")
                or name.isupper()
                or callable(value)
                or isinstance(value, (classmethod, staticmethod, property))
            ):
                continue

            # Check if it's an attrs field
            if hasattr(value, "__class__") and hasattr(value.__class__, "__module__"):
                # Check if it's an attrs field by looking at its type
                if "attrs" in str(type(value)):
                    # For attrs fields, we need to check the metadata or factory
                    metadata = getattr(value, "metadata", {})
                    field_type = metadata.get("field_type")

                    # If it has field_type metadata, it should be a BaseField subclass
                    if field_type and not any(
                        field_type == base.__name__
                        for base in BaseField.__subclasses__() + [BaseField]
                    ):
                        raise TypeError(
                            f"Field '{name}' in class '{cls.__name__}' must use a BaseField subclass. "
                            f"Found field_type: {field_type}"
                        )
                    elif not field_type and not name.isupper():
                        # If no field_type metadata and not uppercase, it's likely a raw attrs field
                        raise TypeError(
                            f"Property '{name}' in class '{cls.__name__}' must inherit from BaseField. "
                            f"Use Field(), PrivateField(), or ProtectedField() instead of raw attrs.field()"
                        )
            elif not name.isupper() and not callable(value):
                # For non-attrs fields that aren't uppercase constants
                if not isinstance(value, BaseField):
                    raise TypeError(
                        f"Property '{name}' in class '{cls.__name__}' must inherit from BaseField. "
                        f"Current type: {type(value).__name__}"
                    )

    def _execute_super_attrs_post_init_if_exists(self) -> None:
        """Call parent's __attrs_post_init__ if it exists in MRO."""
        post_init = getattr(super(), "__attrs_post_init__", None)
        if callable(post_init):
            post_init()

    def _filter_kwargs(self, kwargs: dict, allowed_params: list[str]) -> dict:
        """Generic method to filter initialization parameters."""
        return {key: value for key, value in kwargs.items() if key in allowed_params}
