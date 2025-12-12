from __future__ import annotations

from wexample_helpers.exception.undefined_exception import UndefinedException


class NotAFileException(UndefinedException):
    error_code: str = "FILE_EXPECTED"

    def __init__(self, path, message: str | None = None) -> None:
        msg = message or f"Path is not a file: {path}"
        super().__init__(msg, data={"path": str(path)})
