from __future__ import annotations

from wexample_helpers.testing.classes.first_parent import FirstParent
from wexample_helpers.testing.classes.second_parent import SecondParent


class MultipleChild(FirstParent, SecondParent):
    def __init__(
        self,
        child_value="default_child",
        first_value="inherited_first",
        second_value="inherited_second",
    ) -> None:
        FirstParent.__init__(self, first_value)
        SecondParent.__init__(self, second_value)
        self.child_value = child_value

    def child_method(self):
        return (
            f"Child method with value: {self.child_value}, "
            f"using {self.first_method()} and {self.second_method()}"
        )
