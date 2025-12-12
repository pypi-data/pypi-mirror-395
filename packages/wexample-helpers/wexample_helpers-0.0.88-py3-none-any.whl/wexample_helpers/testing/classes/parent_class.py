from __future__ import annotations


class ParentClass:
    def __init__(self, parent_value="parent_default") -> None:
        self.parent_value = parent_value
        self._protected_value = "protected"

    def parent_method(self):
        return self.parent_value
