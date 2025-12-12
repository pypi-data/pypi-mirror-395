from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass
class ShellResult:
    """Structured result for shell command execution."""

    args: str | list[str]
    cwd: Path | None
    duration: float
    end_time: float
    returncode: int
    start_time: float
    stderr: str | None
    stdout: str | None
