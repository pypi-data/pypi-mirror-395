from __future__ import annotations

from typing import TYPE_CHECKING

from .abstract_local_item_path import AbstractLocalItemPath

if TYPE_CHECKING:
    from enum.local_path_type import LocalPathType

    from wexample_file.exception.file_not_found_exception import FileNotFoundException


class LocalFile(AbstractLocalItemPath):
    """Represents a local file path.

    The path is stored as a resolved absolute Path. If the path exists, it must
    be a file.
    """

    def change_extension(self, new_extension: str) -> None:
        # Normalize extension: allow callers to pass with or without dot
        ext = new_extension.lstrip(".")
        suffix = f".{ext}" if ext else ""
        target = self.path.with_suffix(suffix)

        self.path.replace(target)

    def get_extension(self) -> str:
        """Return the last suffix without the leading dot.

        Examples:
            "archive.tar.gz" -> "gz"
            "report.pdf" -> "pdf"
            "README" -> ""
            Dotfiles without other dots (e.g. ".env") -> "env"
        """
        # Primary: use pathlib suffix when present
        suf = self.path.suffix
        if suf.startswith("."):
            return suf[1:]

        # Special-case: dotfiles like ".env" (no formal suffix)
        name = self.path.name
        if name.startswith(".") and len(name) > 1 and "." not in name[1:]:
            return name[1:]

        return ""

    def is_empty(self) -> bool:
        from pathlib import Path

        return Path(self.path).stat().st_size == 0

    def item_type(self) -> LocalPathType:
        from enum.local_path_type import LocalPathType

        return LocalPathType.FILE

    def read(self, encoding: str = "utf-8") -> str | None:
        """Read and return the file content as text, or None if it doesn't exist.

        Parameters:
            encoding: Text encoding used to decode file content. Defaults to 'utf-8'.
        """
        if not self.path.exists() or not self.path.is_file():
            return None

        return self.path.read_text(encoding=encoding)

    def remove(self) -> None:
        """Delete the file if it exists; no-op if it doesn't.

        This method is idempotent and will not raise if the file is missing.
        """
        try:
            # unlink(missing_ok=True) is available in Python 3.8+
            self.path.unlink(missing_ok=True)
        except TypeError:
            # Fallback for older Python: check existence first
            if self.path.exists():
                self.path.unlink()

    def touch(self, parents: bool = True, exist_ok: bool = True) -> bool:
        if parents:
            self.path.parent.mkdir(parents=True, exist_ok=True)
        if self.path.exists() or self.path.is_dir():
            return False

        self.path.touch(exist_ok=exist_ok)
        return True

    def write(
        self, content: str, encoding: str = "utf-8", make_parents: bool = True
    ) -> None:
        """Write text content to the file, creating it if necessary."""
        from wexample_file.exception.not_a_file_exception import NotAFileException

        if make_parents:
            self.path.parent.mkdir(parents=True, exist_ok=True)
        if self.path.exists() and self.path.is_dir():
            raise NotAFileException(self.path)
        self.path.write_text(content, encoding=encoding)

    def _check_exists(self) -> None:
        from wexample_file.exception.not_a_file_exception import NotAFileException

        super()._check_exists()

        # Only validate type when it exists; creation workflows may pass a non-existent path
        if self.path.exists() and not self.path.is_file():
            raise NotAFileException(self.path)

    def _not_found_exc(self) -> FileNotFoundException:
        from wexample_file.exception.file_not_found_exception import (
            FileNotFoundException,
        )

        return FileNotFoundException(self.path)
