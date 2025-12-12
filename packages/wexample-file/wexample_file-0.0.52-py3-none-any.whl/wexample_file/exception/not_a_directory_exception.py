from __future__ import annotations

from wexample_helpers.exception.undefined_exception import UndefinedException


class NotADirectoryException(UndefinedException):
    error_code: str = "DIRECTORY_EXPECTED"

    def __init__(self, path, message: str | None = None) -> None:
        msg = message or f"Path is not a directory: {path}"
        super().__init__(msg, data={"path": str(path)})
