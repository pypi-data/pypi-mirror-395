from __future__ import annotations

from typing import TYPE_CHECKING

from .abstract_local_item_path import AbstractLocalItemPath

if TYPE_CHECKING:
    from enum.local_path_type import LocalPathType

    from wexample_file.exception.directory_not_found_exception import (
        DirectoryNotFoundException,
    )


class LocalDirectory(AbstractLocalItemPath):
    """Represents a local directory path.

    The path is stored as a resolved absolute Path. If the path exists, it must
    be a directory.
    """

    def create(self, parents: bool = True, exist_ok: bool = True) -> None:
        if self.path.exists() and self.path.is_file():
            return None

        self.path.mkdir(parents=parents, exist_ok=exist_ok)

    def item_type(self) -> LocalPathType:
        from enum.local_path_type import LocalPathType

        return LocalPathType.DIRECTORY

    def remove(self) -> None:
        """Delete the directory recursively if it exists; no-op if it doesn't.

        This method is idempotent and will not raise if the directory is missing.
        """
        if not self.path.exists():
            return
        if self.path.is_dir():
            # Remove contents recursively
            import shutil

            shutil.rmtree(self.path)
        else:
            # If for some reason it's not a dir anymore, best-effort unlink
            try:
                self.path.unlink()
            except FileNotFoundError:
                pass

    def _check_exists(self):
        from wexample_file.exception.not_a_directory_exception import (
            NotADirectoryException,
        )

        super()._check_exists()

        if self.path.exists() and not self.path.is_dir():
            raise NotADirectoryException(self.path)
        return self.path

    def _not_found_exc(self) -> DirectoryNotFoundException:
        from wexample_file.exception.directory_not_found_exception import (
            DirectoryNotFoundException,
        )

        return DirectoryNotFoundException(self.path)
