from __future__ import annotations


class HasShortClassNameClassMixin:
    @classmethod
    def get_class_name_suffix(cls) -> str | None:
        return None

    @classmethod
    def get_name(cls) -> str:
        return cls.get_short_class_name()

    @classmethod
    def get_short_class_name(cls) -> str:
        short_name = cls.__name__
        suffix = cls.get_class_name_suffix()

        if suffix is not None and short_name.endswith(suffix):
            return short_name[: -len(suffix)]

        return short_name
