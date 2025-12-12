from __future__ import annotations

from typing import TYPE_CHECKING

from wexample_helpers.enums.debug_path_style import DebugPathStyle

if TYPE_CHECKING:
    from frame import ExceptionFrame

    from wexample_helpers.common.exception.formatter import TraceFormatter


class ExceptionHandler:
    """High-level API to format exceptions with truncation rules and path handling."""

    def __init__(self, formatter: TraceFormatter | None = None) -> None:
        from wexample_helpers.common.exception.formatter import TraceFormatter

        self.formatter = formatter or TraceFormatter()

    def format_current_trace(
        self,
        *,
        path_style: DebugPathStyle = DebugPathStyle.FULL,
        paths_map: dict[str, str] | None = None,
        skip_frames: int = 0,
    ) -> str:
        from wexample_helpers.common.exception.collector import TraceCollector

        frames = TraceCollector.from_stack(
            skip_frames=skip_frames,
            path_style=path_style,
            paths_map=paths_map,
        )
        return self.formatter.format(frames)

    def format_exception(
        self,
        error: Exception,
        *,
        path_style: DebugPathStyle = DebugPathStyle.FULL,
        paths_map: dict[str, str] | None = None,
        hide_magic_frames: bool = False,
    ) -> str:
        from wexample_helpers.common.exception.collector import TraceCollector

        frames = TraceCollector.from_traceback(
            error.__traceback__,
            path_style=path_style,
            paths_map=paths_map,
        )

        truncate_index = self._get_truncate_index(frames, error)
        if truncate_index != -1:
            frames = frames[:truncate_index]

        if hide_magic_frames and frames:
            # Trim trailing dunder frames (names starting and ending with '__') so the
            # last displayed frame points to user code call site rather than internals.
            def _is_dunder(name: str) -> bool:
                return len(name) >= 4 and name.startswith("__") and name.endswith("__")

            while frames and _is_dunder(frames[-1].function):
                frames = frames[:-1]

        return f"{self.formatter.format(frames)}\n{type(error).__name__}: {error}"

    def _get_truncate_index(
        self, frames: list[ExceptionFrame], error: Exception
    ) -> int:
        from wexample_helpers.enums.error_truncate_rule import ErrorTruncateRules

        error_module = error.__class__.__module__
        for rule_type in ErrorTruncateRules:
            if error_module.startswith(rule_type.module_prefix):
                rule = rule_type.rule

                if rule.truncate_stack_count is not None:
                    return min(rule.truncate_stack_count, len(frames))

                for i, frame in enumerate(frames):
                    filename = frame.filename

                    if (
                        rule.truncate_after_module
                        and rule.truncate_after_module in filename
                    ):
                        return i + 1

                    if rule.truncate_after_file and filename.endswith(
                        rule.truncate_after_file
                    ):
                        return i + 1
        return -1
