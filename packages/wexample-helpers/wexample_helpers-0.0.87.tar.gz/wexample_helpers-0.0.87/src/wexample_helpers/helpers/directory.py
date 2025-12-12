from __future__ import annotations

import os
import shutil
from collections.abc import Callable
from contextlib import contextmanager
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from pathlib import Path

    from wexample_helpers.const.types import PathOrString

AnyCallable = Callable[..., Any]


def directory_aggregate_all_files(file_paths: list[PathOrString]) -> str:
    """Aggregate contents of the given list of file paths."""
    from pathlib import Path

    from wexample_helpers.helpers.file import file_read

    return os.linesep.join(file_read(os.fspath(Path(fp))) for fp in file_paths)


def directory_aggregate_all_files_from_dir(dir_path: PathOrString) -> str:
    """Aggregate contents of all files in a directory and its subdirectories."""
    return directory_aggregate_all_files(directory_list_files(dir_path))


def directory_empty_dir(dir_path: PathOrString) -> None:
    """Remove all contents within a directory, but keep the directory itself."""
    from pathlib import Path

    p = Path(dir_path)
    if not p.is_dir():
        raise NotADirectoryError(f"{p!r} is not a directory.")
    for item in os.listdir(p):
        item_path = os.path.join(p, item)
        if os.path.isdir(item_path) and not os.path.islink(item_path):
            shutil.rmtree(item_path)
        else:
            os.remove(item_path)


@contextmanager
def directory_execute_inside(target_dir: PathOrString) -> None:
    """
    Context manager to execute code inside a specific directory.

    Usage:
        with directory_execute_inside('path/to/dir'):
            # code here
    """
    from pathlib import Path

    original_dir = os.getcwd()
    p = Path(target_dir)
    os.chdir(p)
    try:
        yield
    finally:
        os.chdir(original_dir)


def directory_execute_inside_fn(target_dir: PathOrString, callback: AnyCallable) -> Any:
    """Execute a callback inside the target directory and return its result."""
    with directory_execute_inside(target_dir):
        return callback()


def directory_get_base_name(path: PathOrString) -> str:
    """Return the base name of a path (last component)."""
    from pathlib import Path

    p = Path(path)
    return os.path.basename(os.path.normpath(os.fspath(p)))


def directory_get_parent_path(path: PathOrString) -> str:
    """Return the parent directory path with trailing separator."""
    from pathlib import Path

    p = Path(path)
    parent = os.path.dirname(os.path.normpath(os.fspath(p)))
    return parent + os.sep if parent else os.sep


def directory_iterate_parent_dirs(
    path: PathOrString,
    condition: Callable[[Path], bool],
) -> Path | None:
    """
    Iterate through parent directories until a condition is met.

    Args:
        path: The starting directory path
        condition: A callback function that takes a Path and returns True when the condition is met

    Returns:
        The Path where the condition was met, or None if no match was found
    """
    from pathlib import Path

    current_path = Path(path).resolve()

    # Iterate through parent directories
    while True:
        if condition(current_path):
            return current_path

        # Check if we've reached the root
        parent = current_path.parent
        if parent == current_path:
            # We've reached the root directory
            break

        current_path = parent

    return None


def directory_list_files(dir_path: PathOrString) -> list[str]:
    """List all files in directory and subdirectories, sorted alphabetically."""
    from pathlib import Path

    p = Path(dir_path)
    file_paths: list[str] = []
    for root, _, files in os.walk(p):
        for file in sorted(files):
            full_path = os.path.join(root, file)
            if os.path.isfile(full_path):
                file_paths.append(full_path)
    return file_paths


def directory_remove_tree_if_exists(directory: PathOrString) -> None:
    """Remove a directory and all its contents if it exists."""
    from pathlib import Path

    p = Path(directory)
    if p.exists():
        shutil.rmtree(p)
