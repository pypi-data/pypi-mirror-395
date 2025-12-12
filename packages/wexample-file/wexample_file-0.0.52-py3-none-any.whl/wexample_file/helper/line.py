from __future__ import annotations

from pathlib import Path


def line_count_recursive(path: Path, pattern: str = "*") -> int:
    """
    Recursively counts the total number of lines in all files matching a given pattern
    under the specified directory.

    The function opens each file safely using UTF-8 encoding, ignoring unreadable characters.
    If any file cannot be read for any reason, the function simply skips it and continues.
    Returns the total number of lines across all matching files.
    """
    total = 0
    for f in path.rglob(pattern):
        try:
            with f.open(encoding="utf-8", errors="ignore") as fh:
                total += sum(1 for _ in fh)
        except Exception:
            # Skip files that cannot be opened or read
            continue
    return total
