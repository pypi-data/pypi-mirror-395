from __future__ import annotations

from typing import TYPE_CHECKING

from wexample_helpers.enums.debug_path_style import DebugPathStyle

if TYPE_CHECKING:
    # Backward-compat type alias to new frame class
    from types import TracebackType

    from wexample_helpers.common.exception.frame import ExceptionFrame as TraceFrame
    from wexample_helpers.common.exception.frame import TraceFrame


def trace_format(
    traceback_frames: list[TraceFrame], skip_frames: int | None = 1
) -> str:
    """Format a list of TraceFrame objects and optional exception information.

    Args:
        traceback_frames: The frames to format
        skip_frames: If an int, filter internal frames and show count.
                    If None, show all frames including internals.
    """
    from wexample_helpers.common.exception.formatter import TraceFormatter

    return TraceFormatter().format(traceback_frames, skip_frames=skip_frames)


def trace_get_frames(
    path_style: DebugPathStyle = DebugPathStyle.FULL,
    paths_map: dict | None = None,
) -> list[TraceFrame]:
    """Convert stack frames to TraceFrame objects."""
    from wexample_helpers.common.exception.collector import TraceCollector

    # Collect all frames, filtering happens in the formatter
    return TraceCollector.from_stack(
        path_style=path_style,
        paths_map=paths_map,
    )


def trace_get_traceback_frames(
    traceback: TracebackType,
    path_style: DebugPathStyle = DebugPathStyle.FULL,
    paths_map: dict | None = None,
) -> list[TraceFrame]:
    """Convert exception traceback frames to TraceFrame objects."""
    from wexample_helpers.common.exception.collector import TraceCollector

    return TraceCollector.from_traceback(
        traceback,
        path_style=path_style,
        paths_map=paths_map,
    )


def trace_inheritance_stack(obj) -> None:
    print("Class inheritance stack:")

    for cls in obj.__class__.mro():
        print(f"  ↳ {cls.__module__}.{cls.__name__}")


def trace_print(
    path_style: DebugPathStyle = DebugPathStyle.FULL,
    paths_map: dict | None = None,
    skip_frames: int | None = 1,
) -> None:
    """Print a formatted stack trace.

    Args:
        path_style: How to display file paths
        paths_map: Optional path mappings for display
        skip_frames: If an int, filter internal frames and show count.
                    If None, show all frames including internals.
    """
    print(
        trace_format(
            trace_get_frames(
                path_style=path_style,
                paths_map=paths_map,
            ),
            skip_frames=skip_frames,
        )
    )
