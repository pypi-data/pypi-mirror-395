from __future__ import annotations

import os
from dataclasses import dataclass

from wexample_helpers.enums.debug_path_style import DebugPathStyle


@dataclass(frozen=True)
class ExceptionFrame:
    code: str | None
    filename: str
    function: str
    lineno: int

    is_internal: bool = False
    path_style: DebugPathStyle = DebugPathStyle.FULL
    paths_map: dict[str, str] | None = None

    def __str__(self) -> str:  # pragma: no cover – str delegates to format
        return self.format()

    def format(self) -> str:
        from wexample_helpers.helpers.cli import cli_make_clickable_path

        formatted_path = self.get_formatted_path()
        path_with_line = f"{formatted_path}:{self.lineno}"

        base = (
            f"\n{'-' * 50}\n"
            f"File     : {cli_make_clickable_path(path_with_line)}\n"
            f"Line     : {self.lineno}\n"
            f"Function : {self.function}"
        )

        if self.code:
            code_section = f"\nCode     : {self.code.strip()}"
            return f"{base}{code_section}"
        return base

    def get_formatted_path(self) -> str:
        from wexample_helpers.enums.debug_path_style import DebugPathStyle

        path = self.filename

        if self.paths_map:
            for prod_path, local_path in self.paths_map.items():
                if path.startswith(prod_path):
                    path = path.replace(prod_path, local_path, 1)
                    break

        if self.path_style == DebugPathStyle.FULL:
            return path
        elif self.path_style == DebugPathStyle.RELATIVE:
            try:
                return os.path.relpath(path)
            except ValueError:
                return path
        else:
            return os.path.basename(path)
