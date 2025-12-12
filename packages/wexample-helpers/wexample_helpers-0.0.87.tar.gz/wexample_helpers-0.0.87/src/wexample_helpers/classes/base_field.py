from __future__ import annotations

from collections.abc import Callable
from typing import TYPE_CHECKING, Any

import attrs

if TYPE_CHECKING:
    from collections.abc import Callable

    from wexample_helpers.enums.field_visibility import FieldVisibility


class BaseField:
    """Base class for all field types."""

    def __init__(
        self,
        description: str,
        validator: Callable | None = None,
        default: Any = attrs.NOTHING,
        **kwargs,
    ) -> None:
        self.description = description
        self.validator = validator
        self.default = default
        self.extra_kwargs = kwargs

    @property
    def visibility(self) -> FieldVisibility:
        from wexample_helpers.enums.field_visibility import FieldVisibility

        return FieldVisibility.PUBLIC  # Override in subclasses

    def to_attrs_field(self) -> Any:
        """Convert to attrs field with proper metadata and validation."""
        from attrs import field

        attrs_params = [
            "init",
            "repr",
            "eq",
            "order",
            "hash",
            "compare",
            "kw_only",
            "on_setattr",
            "alias",
            "type",
            "factory",
            "converter",
        ]

        metadata = {
            "description": self.description,
            "visibility": self.visibility.value,
            "field_type": self.__class__.__name__,
        }

        field_kwargs = {"metadata": metadata}

        if self.default is not attrs.NOTHING:
            field_kwargs["default"] = self.default

        for param in attrs_params:
            if param in self.extra_kwargs:
                field_kwargs[param] = self.extra_kwargs[param]

        remaining_kwargs = {
            k: v for k, v in self.extra_kwargs.items() if k not in attrs_params
        }
        metadata.update(remaining_kwargs)

        # Validators
        validators = self._build_validators()
        if validators:
            field_kwargs["validator"] = validators

        return field(**field_kwargs)

    def _build_validators(self) -> Callable | None:
        """Build combined validator function."""
        name_validator = self._create_name_validator()
        validators = self.validator

        # Normalize validators into a list
        if validators is None:
            validators = []
        elif not isinstance(validators, (list, tuple)):
            validators = [validators]

        if name_validator:
            validators.insert(0, name_validator)

        if not validators:
            return None

        def combined_validator(instance, attribute, value):
            for v in validators:
                v(instance, attribute, value)
            return value

        return combined_validator

    def _create_name_validator(self) -> Callable | None:
        """Create validator for field name conventions."""
        expected_prefix = self._get_expected_prefix()
        if not expected_prefix:
            return None

        def name_validator(instance, attribute, value) -> None:
            if not attribute.name.startswith(expected_prefix):
                raise ValueError(
                    f"{self.__class__.__name__} '{attribute.name}' must start with "
                    f"'{expected_prefix}' (current: {self.visibility.value})"
                )

        return name_validator

    def _get_expected_prefix(self) -> str | None:
        """Get expected prefix based on visibility."""
        from wexample_helpers.enums.field_visibility import FieldVisibility

        if self.visibility in [FieldVisibility.PRIVATE, FieldVisibility.PROTECTED]:
            return "_"
        return None
