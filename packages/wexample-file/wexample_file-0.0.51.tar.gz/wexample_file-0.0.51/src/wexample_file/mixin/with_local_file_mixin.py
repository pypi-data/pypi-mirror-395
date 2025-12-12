from __future__ import annotations

from typing import TYPE_CHECKING

from wexample_helpers.mixin.with_path_mixin import WithPathMixin

if TYPE_CHECKING:
    from wexample_file.common.local_file import LocalFile


class WithLocalFileMixin(WithPathMixin):
    def get_local_file(self) -> LocalFile:
        from wexample_file.common.local_file import LocalFile

        return LocalFile(path=self.get_path())
