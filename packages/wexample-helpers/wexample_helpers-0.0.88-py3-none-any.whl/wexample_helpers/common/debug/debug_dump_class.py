from __future__ import annotations

import inspect
from typing import Any

from wexample_helpers.common.debug.abstract_debug import AbstractDebug


class DebugDumpClass(AbstractDebug):
    def __init__(self, cls: Any, depth: int = 0) -> None:
        self.cls = cls
        self.depth = depth
        super().__init__()

    def collect_data(self) -> None:
        self.data = self._collect_hierarchy(self.cls)

    def print(self, silent: bool = False):
        return super().print(silent=silent)

    def _collect_hierarchy(self, cls: Any, seen: set[int] | None = None) -> dict:
        if seen is None:
            seen = set()

        # Normalize input to a class object if an instance is provided
        cls_obj = cls if inspect.isclass(cls) else cls.__class__

        # Use id-based tracking to avoid hash issues
        key = id(cls_obj)
        if key in seen:
            return {
                "type": "circular",
                "name": getattr(cls_obj, "__name__", str(cls_obj)),
            }
        seen.add(key)

        # Safely resolve source file
        try:
            source_file = inspect.getfile(cls_obj)
        except Exception:
            source_file = None

        result = {
            "type": "class",
            "name": getattr(cls_obj, "__name__", str(cls_obj)),
            "module": getattr(cls_obj, "__module__", "<unknown>"),
            "depth": self.depth,
            "source_file": source_file,
        }

        # Collect attributes in a schema compatible with AbstractDebug._format_attribute_value
        attrs = {}
        for name, value in cls_obj.__dict__.items():
            if name.startswith("__"):
                continue
            # Properties
            if isinstance(value, property):
                attrs[name] = {
                    "type": "property",
                    "has_getter": value.fget is not None,
                    "has_setter": value.fset is not None,
                    "has_deleter": value.fdel is not None,
                }
                continue
            # Skip callables (methods, functions); hierarchy here focuses on data attributes
            if callable(value):
                continue
            # Regular attributes: record their type and a readable value
            try:
                value_repr = repr(value)
            except Exception:
                value_repr = "<unrepr-able>"
            attrs[name] = {
                "type": type(value).__name__,
                "value": value_repr,
            }
        if attrs:
            result["attributes"] = attrs

        # Collect base classes
        bases = []
        for base in getattr(cls_obj, "__bases__", ()):
            if base is not object:
                bases.append(self._collect_hierarchy(base, seen.copy()))
        if bases:
            result["bases"] = bases

        return result
