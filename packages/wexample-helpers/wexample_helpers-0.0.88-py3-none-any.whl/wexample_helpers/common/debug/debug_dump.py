from __future__ import annotations

import inspect
from typing import Any

from wexample_helpers.common.debug.abstract_debug import AbstractDebug


class DebugDump(AbstractDebug):
    def __init__(self, obj: Any, max_depth: int = 100) -> None:
        self.obj = obj
        self.max_depth = max_depth
        self.current_depth = 0
        # Get caller frame info
        frame = inspect.currentframe()
        caller = frame.f_back if frame else None
        self.caller_info = inspect.getframeinfo(caller) if caller else None
        super().__init__()

    def collect_data(self) -> None:
        self.data = self._collect_data(self.obj)
        if self.caller_info:
            self.data["dump_location"] = {
                "file": self.caller_info.filename,
                "line": self.caller_info.lineno,
            }

    def _collect_data(
        self, obj: Any, depth: int = 0, seen: set[int] | None = None
    ) -> dict:
        from datetime import datetime

        if seen is None:
            seen = set()

        # Check for max depth
        if depth >= self.max_depth:
            return {"type": "max_depth"}

        # Get object id for circular reference detection
        obj_id = id(obj)
        if obj_id in seen:
            return {"type": "circular"}
        seen.add(obj_id)

        # Handle different types of objects
        if isinstance(obj, (str, int, float, bool)):
            return {"type": type(obj).__name__, "value": repr(obj)}
        elif isinstance(obj, datetime):
            return {"type": "datetime", "value": obj.isoformat()}
        elif isinstance(obj, (list, tuple, set)):
            return {
                "type": type(obj).__name__,
                "elements": [
                    self._collect_data(item, depth + 1, seen.copy()) for item in obj
                ],
            }
        elif isinstance(obj, dict):
            return {
                "type": "dict",
                "items": [
                    {
                        "key": self._collect_data(key, depth + 1, seen.copy()),
                        "value": self._collect_data(value, depth + 1, seen.copy()),
                    }
                    for key, value in obj.items()
                ],
            }
        else:
            try:
                # Handle class instance
                class_data = {
                    "type": "class",
                    "name": obj.__class__.__name__,
                    "module": obj.__class__.__module__,
                    "source_file": inspect.getfile(obj.__class__),
                }

                # Collect instance attributes and properties
                attrs = {}
                for name, value in obj.__class__.__dict__.items():
                    if isinstance(value, property):
                        attrs[name] = {
                            "type": "property",
                            "has_getter": value.fget is not None,
                            "has_setter": value.fset is not None,
                            "has_deleter": value.fdel is not None,
                        }

                # Collect regular attributes
                if hasattr(obj, "__dict__"):
                    for name, value in obj.__dict__.items():
                        if not name.startswith("__"):
                            attrs[name] = self._collect_data(
                                value, depth + 1, seen.copy()
                            )

                return {
                    "instance_of": obj.__class__.__name__,
                    "class_data": class_data,
                    "attributes": attrs,
                }
            except (AttributeError, TypeError):
                # Fallback for objects that can't be introspected
                return {"type": type(obj).__name__, "value": str(obj)}
