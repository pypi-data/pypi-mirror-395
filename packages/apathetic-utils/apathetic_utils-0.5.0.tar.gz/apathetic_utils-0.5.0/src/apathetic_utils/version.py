# src/apathetic_utils/version.py
"""Version utilities."""

from __future__ import annotations

import sys
from typing import Any, NamedTuple


class ApatheticUtils_Internal_Version:  # noqa: N801  # pyright: ignore[reportUnusedClass]
    """Mixin class that provides version utility functionality.

    This class contains utilities for version detection and manipulation.
    When mixed into apathetic_utils, it provides version utility methods.
    """

    @staticmethod
    def get_sys_version_info() -> tuple[int, int, int] | tuple[int, int, int, str, int]:
        return sys.version_info

    @staticmethod
    def create_version_info(major: int, minor: int, micro: int = 0) -> Any:
        """Create a mock sys.version_info object with major and minor attributes.

        This properly mocks sys.version_info so it can be used with attribute access
        (.major, .minor) and tuple comparison, matching the behavior of the real
        sys.version_info object (which is a named tuple).

        Useful for testing or when you need to simulate different Python versions.

        Args:
            major: Major version number (e.g., 3)
            minor: Minor version number (e.g., 11)
            micro: Micro version number (default: 0)

        Returns:
            A mock version_info object with .major, .minor, .micro attributes
            and tuple-like comparison support.

        Example:
            version = create_version_info(3, 11)
            assert version.major == 3
            assert version.minor == 11
            assert version >= (3, 10)
        """

        # Create a named tuple that matches sys.version_info structure
        class _VersionInfo(NamedTuple):
            """Mock sys.version_info named tuple."""

            major: int
            minor: int
            micro: int
            releaselevel: str
            serial: int

        return _VersionInfo(
            major=major, minor=minor, micro=micro, releaselevel="final", serial=0
        )
