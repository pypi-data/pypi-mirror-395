from __future__ import annotations

from wexample_helpers.classes.mixin.has_short_class_name_class_mixin import (
    HasShortClassNameClassMixin,
)


class HasSnakeShortClassNameClassMixin(HasShortClassNameClassMixin):
    @classmethod
    def get_name(cls) -> str:
        return cls.get_snake_short_class_name()

    @classmethod
    def get_snake_class_name_suffix(cls) -> str | None:
        from wexample_helpers.helpers.string import string_to_snake_case

        suffix = cls.get_class_name_suffix()
        return string_to_snake_case(suffix) if suffix is not None else None

    @classmethod
    def get_snake_short_class_name(cls) -> str:
        from wexample_helpers.helpers.string import string_to_snake_case

        return string_to_snake_case(cls.get_short_class_name())
