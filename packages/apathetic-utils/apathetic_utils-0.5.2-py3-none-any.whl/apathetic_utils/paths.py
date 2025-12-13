# src/apathetic_utils/paths.py
"""Path manipulation utilities."""

from __future__ import annotations

import re
from itertools import zip_longest
from pathlib import Path

from apathetic_logging import getLogger


class ApatheticUtils_Internal_Paths:  # noqa: N801  # pyright: ignore[reportUnusedClass]
    """Mixin class that provides path manipulation functionality.

    This class contains utilities for path normalization and glob handling.
    When mixed into apathetic_utils, it provides path manipulation methods.
    """

    @staticmethod
    def normalize_path_string(raw: str) -> str:
        r"""Normalize a user-supplied path string for cross-platform use.

        Industry-standard (Git/Node/Python) rules:
          - Treat both '/' and '\\' as valid separators and normalize all to '/'.
          - Replace escaped spaces ('\\ ') with real spaces.
          - Collapse redundant slashes (preserve protocol prefixes like 'file://').
          - Never resolve '.' or '..' or touch the filesystem.
          - Never raise for syntax; normalization is always possible.

        This is the pragmatic cross-platform normalization strategy used by
        Git, Node.js, and Python build tools.
        This function is purely lexical — it normalizes syntax, not filesystem state.
        """
        logger = getLogger()
        if not raw:
            return ""

        path = raw.strip()

        # Handle escaped spaces (common shell copy-paste)
        if "\\ " in path:
            fixed = path.replace("\\ ", " ")
            logger.warning("Normalizing escaped spaces in path: %r → %s", path, fixed)
            path = fixed

        # Normalize all backslashes to forward slashes
        path = path.replace("\\", "/")

        # Collapse redundant slashes (keep protocol //)
        collapsed_slashes = re.sub(r"(?<!:)//+", "/", path)
        if collapsed_slashes != path:
            logger.trace(
                "Collapsed redundant slashes: %r → %r", path, collapsed_slashes
            )
            path = collapsed_slashes

        return path

    @staticmethod
    def has_glob_chars(s: str) -> bool:
        return any(c in s for c in "*?[]")

    @staticmethod
    def get_glob_root(pattern: str) -> Path:
        """Return the non-glob portion of a path like 'src/**/*.txt'.

        Normalizes paths to cross-platform.
        """
        if not pattern:
            return Path()

        # Normalize backslashes to forward slashes
        normalized = ApatheticUtils_Internal_Paths.normalize_path_string(pattern)

        parts: list[str] = []
        for part in Path(normalized).parts:
            if re.search(r"[*?\[\]]", part):
                break
            parts.append(part)
        return Path(*parts) if parts else Path()

    @staticmethod
    def shorten_path(
        path: str | Path,
        bases: str | Path | list[str | Path],
    ) -> str:
        """Return the shortest path relative to any base's common prefix.

        Finds the longest shared prefix between `path` and each base path by
        comparing their path parts, and returns the shortest remaining portion
        of `path`. This works with any paths (files, directories, etc.) and does
        not require one path to be under the other.

        When the common prefix is only root ("/"), returns the absolute path
        since a relative path from root is not useful.

        Example:
            shorten_path(
                "/home/user/code/serger/src/logs.py",
                ["/home/user/code/serger/tests/utils/patch.py",
                 "/home/user/code/serger/src"]
            )
            → "logs.py" (shortest: common prefix with src/)

            shorten_path(
                "/home/user/code/serger/src/logs.py",
                "/home/user/code/serger/tests/utils/patch.py"
            )
            → "src/logs.py"

        Args:
            path: Path to make relative
            bases: Single base path or list of base paths to find common prefix with

        Returns:
            Shortest path relative to common prefix, or absolute path if common
            prefix is only root
        """
        p = Path(path).resolve()

        # Normalize bases to a list
        if isinstance(bases, (str, Path)):
            bases_list: list[str | Path] = [bases]
        else:
            bases_list = bases

        candidates: list[str] = []

        for base in bases_list:
            b = Path(base).resolve()

            # Split both into parts and find the longest shared prefix
            common_len = 0
            for a, c in zip_longest(p.parts, b.parts):
                if a != c:
                    break
                common_len += 1

            # Slice off the shared prefix
            remaining = Path(*p.parts[common_len:])
            result = str(remaining) or "."

            # If common prefix is only root (common_len <= 1), return absolute path
            if common_len <= 1:
                # Common prefix is only root, return absolute path
                candidates.append(str(p))
            else:
                candidates.append(result)

        if candidates:
            # Return shortest result
            return min(candidates, key=len)

        # No bases provided, return absolute path
        return str(p)
