from __future__ import annotations

from pathlib import Path

from wexample_helpers.const.types import PathOrString

STATE_FILE = Path(".last_git_state")


def repo_get_state(cwd: PathOrString | None = None) -> str:
    """Return a unique hash representing the current git state (HEAD + changes).

    Args:
        cwd: Optional path to the git repository. If None, uses current directory.
    """
    from wexample_helpers.helpers.shell import shell_run

    head_result = shell_run(["git", "rev-parse", "HEAD"], cwd=cwd)
    head_hash = head_result.stdout.strip() if head_result.stdout else ""

    diff_result = shell_run(["git", "diff"], cwd=cwd)
    diff_hash = diff_result.stdout if diff_result.stdout else ""

    return f"{head_hash}-{hash(diff_hash)}"


def repo_has_changed(
    cwd: PathOrString | None = None,
    state_file: Path | None = None,
) -> bool:
    """Check if code has changed since last run.

    Args:
        cwd: Optional path to the git repository. If None, uses current directory.
        state_file: Optional custom state file path. If None, uses STATE_FILE.
    """
    current_state = repo_get_state(cwd=cwd)
    file_to_use = state_file if state_file is not None else STATE_FILE
    previous_state = file_to_use.read_text().strip() if file_to_use.exists() else None
    if current_state != previous_state:
        file_to_use.write_text(current_state)
        return True
    return False


def repo_has_changed_since(
    previous_state: str,
    cwd: PathOrString | None = None,
) -> bool:
    """Return True if the repo state has changed compared to a provided hash.

    Args:
        previous_state: The previous git state hash to compare against.
        cwd: Optional path to the git repository. If None, uses current directory.
    """
    current_state = repo_get_state(cwd=cwd)
    return current_state != previous_state
