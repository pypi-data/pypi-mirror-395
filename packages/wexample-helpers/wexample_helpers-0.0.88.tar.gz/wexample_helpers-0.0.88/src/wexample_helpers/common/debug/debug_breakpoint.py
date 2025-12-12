from __future__ import annotations

import pdb

from wexample_helpers.common.debug.abstract_debug import AbstractDebug


class DebugBreakpoint(AbstractDebug):
    def __init__(self, message: str | None = None) -> None:
        self.message = message
        super().__init__()

    def collect_data(self) -> None:
        # No data collection needed for breakpoint
        pass

    def print(self, silent: bool = False):
        lines = []
        if self.message:
            lines.append(f"\n Debug breakpoint: {self.message}")
        lines.extend(
            [
                "Commands:",
                "  p variable  : Print variable",
                "  n          : Next line",
                "  c          : Continue execution",
                "  q          : Quit",
                "  h          : Help (more commands)",
            ]
        )

        text = "\n".join(lines)

        if silent:
            # In silent mode, do not start pdb; return the helper text instead
            return text

        if text:
            print(text)
        pdb.set_trace()
        return ""
