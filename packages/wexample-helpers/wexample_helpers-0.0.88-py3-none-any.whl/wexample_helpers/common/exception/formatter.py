from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Iterable

    from frame import ExceptionFrame


class TraceFormatter:
    """Formats a sequence of ExceptionFrame objects into a human-readable string."""

    def format(
        self, frames: Iterable[ExceptionFrame], skip_frames: int | None = 1
    ) -> str:
        """Format frames, optionally filtering internal frames.

        Args:
            frames: The frames to format
            skip_frames: If an int, filter internal frames and show count.
                        If None, show all frames including internals.
        """
        frames_list = list(frames)

        if skip_frames is None:
            # Show all frames including internals
            result = "\n".join(str(frame) for frame in frames_list)
            # Add note about trace collector being excluded
            result += "\n\n" + "=" * 50 + "\n"
            result += "Note: TraceCollector.from_stack() excluded from trace"
            return result

        # Filter out internal frames
        filtered_frames = [frame for frame in frames_list if not frame.is_internal]
        skipped_count = len(frames_list) - len(filtered_frames)

        result = "\n".join(str(frame) for frame in filtered_frames)

        if skipped_count > 0:
            result += f"\n\n+ {skipped_count} internal frame{'s' if skipped_count > 1 else ''} skipped"

        return result
