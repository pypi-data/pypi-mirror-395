from __future__ import annotations

from pathlib import Path


def path_rebase(
    root_src: str | Path, path_src: str | Path, root_dest: str | Path
) -> str:
    """
    Rebase a path from one root to another.

    Example:
        root_src="/home/me/project"
        path_src="/home/me/project/src/test.php"
        root_dest="/var/www/html"

        → "/var/www/html/src/test.php"
    """
    root_src = str(Path(root_src).resolve())
    path_src = str(Path(path_src).resolve())
    root_dest = str(Path(root_dest).resolve())

    # Compute the relative path from the original root
    relative_path = Path(path_src).resolve().relative_to(root_src)

    # Append it to the new root
    return str(Path(root_dest) / relative_path)
