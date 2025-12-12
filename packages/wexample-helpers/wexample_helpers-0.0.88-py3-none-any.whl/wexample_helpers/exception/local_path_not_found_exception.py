from __future__ import annotations

from wexample_helpers.exception.undefined_exception import UndefinedException


class LocalPathNotFoundException(UndefinedException):
    error_code: str = "LOCAL_PATH_NOT_FOUND"

    def __init__(self, path, message: str | None = None) -> None:
        msg = message or f"Path does not exist: {path}"
        super().__init__(msg, data={"path": str(path)})
