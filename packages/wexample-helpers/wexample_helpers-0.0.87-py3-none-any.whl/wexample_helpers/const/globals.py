from __future__ import annotations

from pathlib import Path

DIR_GIT: Path = Path(".git")

# filestate: python-constant-sort
FILE_EXTENSION_ENV: str = "env"
FILE_EXTENSION_PYTHON: str = "py"
FILE_EXTENSION_YAML: str = "yml"

# filestate: python-constant-sort
FILE_NAME_ENV: Path = Path(f".{FILE_EXTENSION_ENV}")
FILE_NAME_ENV_YAML: Path = Path(f".{FILE_EXTENSION_ENV}.{FILE_EXTENSION_YAML}")

PATH_NAME_PATH: str = "path"
UNSET = object()
