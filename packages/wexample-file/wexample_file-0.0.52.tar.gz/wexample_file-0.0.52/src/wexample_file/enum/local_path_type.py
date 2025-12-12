from __future__ import annotations

from enum import Enum


class LocalPathType(Enum):
    """Types of local paths."""

    DIRECTORY = "directory"
    FILE = "file"
