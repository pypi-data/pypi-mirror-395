from __future__ import annotations

import os
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path

    from wexample_helpers.const.types import FileStringOrPath, PathOrString


def file_change_mode(path: PathOrString, mode: int) -> None:
    """
    Change file permissions for a path, ignoring symlinks and missing files.
    """
    try:
        if not os.path.islink(str(path)):
            os.chmod(str(path), mode)
    except FileNotFoundError:
        pass


def file_change_mode_recursive(
    path: PathOrString, mode: int, follow_symlinks: bool = True
) -> None:
    """
    Recursively change mode for files and directories under path.

    :param path: Root path to change mode.
    :param mode: Permission bits to apply.
    :param follow_symlinks: If False, skip symlinked directories.
    """
    file_change_mode(path, mode)
    if os.path.isdir(str(path)) and (follow_symlinks or not os.path.islink(str(path))):
        for item in os.listdir(str(path)):
            file_change_mode_recursive(
                os.path.join(str(path), item), mode, follow_symlinks
            )


def file_get_directories(path: PathOrString, recursive: bool = False) -> list[str]:
    """Get directories under path, optionally recursively."""
    from pathlib import Path

    base = Path(path)
    if not recursive:
        return [str(p) for p in base.iterdir() if p.is_dir()]
    return [str(p) for p in base.rglob("*") if p.is_dir()]


def file_list_subdirectories(path: PathOrString) -> list[str]:
    """
    List immediate subdirectory names (excluding hidden) under a given path.
    """
    from pathlib import Path

    base = Path(path)
    subdirs = [
        p.name for p in base.iterdir() if p.is_dir() and not p.name.startswith(".")
    ]
    return sorted(subdirs)


def file_mode_num_to_octal(num: int) -> str:
    """Convert numeric mode (e.g. st_mode) to a three-digit octal string."""
    return oct(num & 0o777)[-3:]


def file_mode_octal_to_num(mode: str | int) -> int:
    """Convert octal mode string (e.g. '755') to its numeric value."""
    return int(str(mode), 8)


def file_path_get_mode_num(path: Path) -> int:
    """Get the numeric permission bits for a Path object."""
    return path.stat().st_mode & 0o777


def file_path_get_octal_mode(path: Path) -> str:
    """Get the octal permission string for a Path object."""
    return file_mode_num_to_octal(path.stat().st_mode)


def file_read(file_path: PathOrString) -> str:
    """Read file content as UTF-8 text."""
    from pathlib import Path

    return Path(file_path).read_text(encoding="utf-8")


def file_read_or_default(
    file_path: PathOrString, default: str | None = ""
) -> str | None:
    """Read file content or return default on any error."""
    try:
        return file_read(file_path)
    except Exception:
        return default


def file_remove_if_exists(path: PathOrString) -> None:
    """Remove a file or symlink if it exists."""
    from pathlib import Path

    p = Path(path)
    if p.is_file() or p.is_symlink():
        p.unlink()


def file_resolve_path(path: FileStringOrPath) -> Path:
    """Resolve a FileStringOrPath to a pathlib.Path object."""
    from pathlib import Path

    return path if isinstance(path, Path) else Path(path)


def file_touch(path: PathOrString, times: tuple[int, int] | None = None) -> None:
    """Create file if missing and update its access and modification times."""
    from pathlib import Path

    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("a"):
        os.utime(p, times)


def file_validate_mode_octal(mode: str | int) -> bool:
    """Validate that mode is a three-digit octal string or int."""
    m = str(mode)
    return len(m) == 3 and all(ch in "01234567" for ch in m)


def file_validate_mode_octal_or_fail(mode: str | int) -> bool:
    """Validate octal mode or raise Exception."""
    if not file_validate_mode_octal(mode):
        raise ValueError(f"Bad mode format {mode!r}")
    return True


def file_write(file_path: PathOrString, content: str, encoding: str = "utf-8") -> None:
    """Write content to file, overwriting if it exists."""
    from pathlib import Path

    p = Path(file_path)
    p.write_text(content, encoding=encoding)


def file_write_ensure(
    file_path: FileStringOrPath, content: str, encoding: str = "utf-8"
) -> None:
    """
    Write content to file, creating parent directories if needed.

    :param file_path: Destination file path.
    :param content: Text content to write.
    :param encoding: Text encoding.
    """
    p = file_resolve_path(file_path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding=encoding)
