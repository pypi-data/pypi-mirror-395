from __future__ import annotations

from wexample_helpers.classes.base_class import BaseClass
from wexample_helpers.decorator.base_class import base_class


@base_class
class PrintableMixin(BaseClass):
    def __str__(self):
        from wexample_helpers.common.debug.debug_dump_class import DebugDumpClass

        return DebugDumpClass(self).print(silent=True)
