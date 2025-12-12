from __future__ import annotations


class FirstParent:
    def __init__(self, first_value="default_first") -> None:
        self.first_value = first_value

    def first_method(self):
        return f"First parent method with value: {self.first_value}"
