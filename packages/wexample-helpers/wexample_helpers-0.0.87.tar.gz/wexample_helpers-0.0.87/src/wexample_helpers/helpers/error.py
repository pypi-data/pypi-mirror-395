from __future__ import annotations

from typing import TYPE_CHECKING

from wexample_helpers.enums.debug_path_style import DebugPathStyle

if TYPE_CHECKING:
    # Backward-compat type alias to new frame class
    from wexample_helpers.common.exception.frame import ExceptionFrame as TraceFrame
    from wexample_helpers.common.exception.frame import TraceFrame


def error_format(
    error: Exception | None = None,
    path_style: DebugPathStyle = DebugPathStyle.FULL,
    paths_map: dict | None = None,
) -> str:
    from wexample_helpers.common.exception.handler import ExceptionHandler

    handler = ExceptionHandler()
    # Then print the formatted traceback using the new handler
    return handler.format_exception(
        error,
        path_style=path_style,
        paths_map=paths_map,
    )


def error_get_truncate_index(frames: list[TraceFrame], error: Exception) -> int:
    """Returns the index where to truncate the trace based on error type. Returns -1 if no truncation needed."""
    from wexample_helpers.common.exception.handler import ExceptionHandler

    # Delegate to ExceptionHandler internals to avoid duplication, but keep public API.
    handler = ExceptionHandler()
    return handler._get_truncate_index(frames, error)  # type: ignore[attr-defined]
