from __future__ import annotations

from typing import Any

from wexample_helpers.enums.debug_path_style import DebugPathStyle


def dd(*args, **kwargs) -> None:
    debug_dump_and_die(*args, **kwargs)


def debug_breakpoint(message: str = None) -> None:
    from wexample_helpers.common.debug.debug_breakpoint import DebugBreakpoint

    DebugBreakpoint(message).execute()


def debug_class_info(cls_or_obj, title: str = None) -> None:
    """
    Print detailed information about a class or object with improved hierarchy visualization.
    """
    from wexample_helpers.common.debug.debug_dump_class import DebugDumpClass

    target_class = cls_or_obj if isinstance(cls_or_obj, type) else type(cls_or_obj)
    dumper = DebugDumpClass(target_class)

    if title:
        print(f"\n=== {title} ===")

    dumper.execute()


def debug_dump(obj: Any, max_depth: int = 100) -> None:
    from wexample_helpers.common.debug.debug_dump import DebugDump

    DebugDump(obj, max_depth).execute()


def debug_dump_and_die(*args, **kwargs) -> None:
    debug_dump(*args, **kwargs)
    exit()


def debug_timer_end(name: str, precision: int = 2):
    if name not in _DEBUG_TIMERS:
        return None

    return time.perf_counter() - _DEBUG_TIMERS.pop(name)


def debug_timer_start(name: str) -> None:
    _DEBUG_TIMERS[name] = time.perf_counter()


def debug_trace(
    data: Any = None,
    path_style: DebugPathStyle = DebugPathStyle.FULL,
    paths_map: dict | None = None,
    skip_frames: int | None = 1,
) -> None:
    """Print a debug trace of the current stack.

    Args:
        path_style: How to display file paths
        paths_map: Optional path mappings for display
        skip_frames: If an int, skip this many frames from the top and filter internal frames.
                    If None, show all frames including internals.
    """
    from wexample_helpers.helpers.trace import trace_print

    if data is not None:
        debug_dump(data)

    # trace_print will handle incrementing skip_frames for its own frame
    trace_print(
        path_style=path_style,
        paths_map=paths_map,
        skip_frames=skip_frames,
    )


def debug_trace_and_die(
    message: str = None,
    path_style: DebugPathStyle = DebugPathStyle.FULL,
    paths_map: dict | None = None,
    skip_frames: int | None = 1,
) -> None:
    """Print a debug trace and exit.

    Args:
        message: Optional message to print before the trace
        path_style: How to display file paths
        paths_map: Optional path mappings for display
        skip_frames: If an int, skip this many frames from the top and filter internal frames.
                    If None, show all frames including internals.
    """
    # debug_trace will handle the skip_frames logic
    debug_trace(
        path_style=path_style,
        paths_map=paths_map,
        skip_frames=skip_frames,
    )

    if message:
        debug_dump(message)
    exit(1)


def dt(*args, **kwargs) -> None:
    debug_trace_and_die(*args, **kwargs)


import time

_DEBUG_TIMERS = {}
