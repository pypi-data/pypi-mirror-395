from __future__ import annotations

from typing import Any


class HasClassDependencies:
    @classmethod
    def get_class_dependencies(cls) -> list[Any]:
        """
        Return a list of class dependencies, basically the classes used by properties which are only defined for type checking, with quotes,
        this function can be used to import dependencies before rebuilding class
        """
        return []
