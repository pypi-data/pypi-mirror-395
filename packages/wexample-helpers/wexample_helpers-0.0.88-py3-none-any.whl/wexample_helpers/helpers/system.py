from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path


def system_get_venv_bin_path() -> Path:
    import sys
    from pathlib import Path

    return Path(sys.executable).parent
