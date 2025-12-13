# src/apathetic_utils/ci.py
"""CI environment detection utilities."""

from __future__ import annotations

import os
from typing import ClassVar, TypeVar


T = TypeVar("T")


class ApatheticUtils_Internal_CI:  # noqa: N801  # pyright: ignore[reportUnusedClass]
    """Mixin class that provides CI environment detection functionality.

    This class contains utilities for detecting CI environments.
    When mixed into apathetic_utils, it provides CI detection methods.
    """

    # CI environment variable names that indicate CI environment
    CI_ENV_VARS: ClassVar[tuple[str, ...]] = (
        "CI",
        "GITHUB_ACTIONS",
        "GIT_TAG",
        "GITHUB_REF",
    )

    @staticmethod
    def is_ci() -> bool:
        """Check if running in a CI environment.

        Returns True if any of the following environment variables are set:
        - CI: Generic CI indicator (set by most CI systems)
        - GITHUB_ACTIONS: GitHub Actions specific
        - GIT_TAG: Indicates a tagged build
        - GITHUB_REF: GitHub Actions ref (branch/tag)

        Returns:
            True if running in CI, False otherwise
        """
        return bool(
            any(os.getenv(var) for var in ApatheticUtils_Internal_CI.CI_ENV_VARS)
        )

    @staticmethod
    def if_ci(ci_value: T, local_value: T) -> T:
        r"""Return different values based on CI environment.

        Useful for tests that need different behavior or expectations
        in CI vs local development environments.

        Args:
            ci_value: Value to return when running in CI
            local_value: Value to return when running locally

        Returns:
            ci_value if running in CI, otherwise local_value

        Example:
            # Different regex patterns for commit hashes
            commit_pattern = if_ci(
                r"[0-9a-f]{4,}",  # CI: expect actual commit hash
                r"unknown \\(local build\\)"  # Local: expect placeholder
            )
        """
        return ci_value if ApatheticUtils_Internal_CI.is_ci() else local_value
