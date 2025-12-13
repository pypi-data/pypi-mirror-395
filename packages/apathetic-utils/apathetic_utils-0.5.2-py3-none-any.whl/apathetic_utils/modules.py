# src/apathetic_utils/modules.py
"""Module detection utilities."""

from __future__ import annotations

from pathlib import Path

from apathetic_logging import getLogger


class ApatheticUtils_Internal_Modules:  # noqa: N801  # pyright: ignore[reportUnusedClass]
    """Mixin class providing module detection utilities.

    These utilities help detect Python packages by scanning for __init__.py files.
    """

    @staticmethod
    def _find_package_root_for_file(
        file_path: Path,
        *,
        source_bases: list[str] | None = None,
        _config_dir: Path | None = None,
    ) -> Path | None:
        """Find the package root for a file.

        First checks for __init__.py files (definitive package marker).
        If no __init__.py found and file is under a source_bases directory,
        treats everything after the matching base prefix as a package structure.

        Args:
            file_path: Path to the Python file
            source_bases: Optional list of module base directories (absolute paths)
            _config_dir: Optional config directory (unused, kept for compatibility)

        Returns:
            Path to the package root directory, or None if not found
        """
        logger = getLogger()
        file_path_resolved = file_path.resolve()
        current_dir = file_path_resolved.parent
        last_package_dir: Path | None = None

        logger.trace(
            "[PKG_ROOT] Finding package root for %s, starting from %s",
            file_path.name,
            current_dir,
        )

        # First, walk up looking for __init__.py (definitive package marker)
        # __init__.py always takes precedence
        while True:
            # Check if current directory has __init__.py
            init_file = current_dir / "__init__.py"
            if init_file.exists():
                # This directory is part of a package
                last_package_dir = current_dir
                logger.trace(
                    "[PKG_ROOT] Found __init__.py at %s (package root so far: %s)",
                    current_dir,
                    last_package_dir,
                )
            # This directory doesn't have __init__.py
            # If we found a package via __init__.py, return it
            elif last_package_dir is not None:
                logger.trace(
                    "[PKG_ROOT] No __init__.py at %s, package root: %s",
                    current_dir,
                    last_package_dir,
                )
                return last_package_dir
                # No __init__.py found yet, continue walking up
                # (we'll check source_bases after this loop if needed)

            # Move up one level
            parent = current_dir.parent
            if parent == current_dir:
                # Reached filesystem root
                if last_package_dir is not None:
                    logger.trace(
                        "[PKG_ROOT] Reached filesystem root, package root: %s",
                        last_package_dir,
                    )
                    return last_package_dir
                # No __init__.py found, break to check source_bases
                break
            current_dir = parent

        # If no __init__.py found, check if file is under any source_bases directory
        if source_bases and last_package_dir is None:
            for base_str in source_bases:
                # base_str is already an absolute path
                base_path = Path(base_str).resolve()
                try:
                    # Check if file is under this base
                    rel_path = file_path_resolved.relative_to(base_path)
                    # If file is directly in base (e.g., src/mymodule.py), no package
                    if len(rel_path.parts) == 1:
                        # Single file in base - not a package
                        continue
                    # File is in a subdirectory of base (e.g., src/mypkg/submodule.py)
                    # The first part after base is the package
                    package_dir = base_path / rel_path.parts[0]
                    if package_dir.exists() and package_dir.is_dir():
                        logger.trace(
                            "[PKG_ROOT] Found package via source_bases: %s (base: %s)",
                            package_dir,
                            base_path,
                        )
                        return package_dir
                except ValueError:
                    # File is not under this base, continue to next base
                    continue

        # Return None if no package found
        return last_package_dir

    @staticmethod
    def detect_packages_from_files(  # noqa: C901, PLR0912, PLR0915
        file_paths: list[Path],
        package_name: str,
        *,
        source_bases: list[str] | None = None,
        _config_dir: Path | None = None,
    ) -> tuple[set[str], list[str]]:
        """Detect packages from file paths.

        If files are under source_bases directories, treats everything after the
        matching base prefix as a package structure (regardless of __init__.py).
        Otherwise, follows Python's import rules: only detects regular packages
        (with __init__.py files). Falls back to configured package_name if none
        detected.

        Args:
            file_paths: List of file paths to check
            package_name: Configured package name (used as fallback)
            source_bases: Optional list of module base directories (absolute paths)
            _config_dir: Optional config directory (unused, kept for compatibility)

        Returns:
            Tuple of (set of detected package names, list of parent directories).
            Package names always includes package_name. Parent directories are
            returned as absolute paths, deduplicated.
        """
        logger = getLogger()
        detected: set[str] = set()
        parent_dirs: list[Path] = []
        seen_parents: set[Path] = set()
        # Track which packages were detected via source_bases
        # (for namespace package detection)
        detected_via_source_bases: set[str] = set()

        # Detect packages from files
        for file_path in file_paths:
            file_path_resolved = file_path.resolve()
            pkg_root = ApatheticUtils_Internal_Modules._find_package_root_for_file(
                file_path, source_bases=source_bases
            )
            if pkg_root:
                # Check if this package was detected via source_bases
                # (by checking if file is under any source_base and no __init__.py)
                detected_via_sb = False
                if source_bases:
                    # Check if file is under a source_base
                    for base_str in source_bases:
                        base_path = Path(base_str).resolve()
                        try:
                            rel_path = file_path_resolved.relative_to(base_path)
                            # If file is in a subdirectory of base, check __init__.py
                            if (
                                len(rel_path.parts) > 1
                                and not (pkg_root / "__init__.py").exists()
                            ):
                                # No __init__.py, so detected via source_bases
                                detected_via_sb = True
                                break
                        except ValueError:
                            continue

                # Extract package name from directory name
                pkg_name = pkg_root.name
                detected.add(pkg_name)
                if detected_via_sb:
                    detected_via_source_bases.add(pkg_name)

                # For source_bases, also detect nested packages (all directory levels)
                if detected_via_sb and source_bases:
                    # Find which base this file is under
                    for base_str in source_bases:
                        base_path = Path(base_str).resolve()
                        try:
                            rel_path = file_path_resolved.relative_to(base_path)
                            # Detect all directory levels between base and file
                            # (excluding the file itself and the base)
                            # More than base + first level + file
                            min_nested_parts = 3
                            if len(rel_path.parts) >= min_nested_parts:
                                # Walk from base to file, detecting intermediate dirs
                                current = base_path
                                for part in rel_path.parts[:-1]:  # Exclude filename
                                    current = current / part
                                    if current.is_dir() and current != pkg_root:
                                        nested_pkg_name = current.name
                                        if (
                                            nested_pkg_name
                                            and nested_pkg_name != package_name
                                        ):
                                            detected.add(nested_pkg_name)
                                            detected_via_source_bases.add(
                                                nested_pkg_name
                                            )
                                            logger.trace(
                                                "[PKG_DETECT] Detected nested package "
                                                "%s from %s",
                                                nested_pkg_name,
                                                file_path,
                                            )
                        except ValueError:
                            continue

                # Extract parent directory (module base)
                parent_dir = pkg_root.parent.resolve()
                # Check if parent is filesystem root (parent of root equals root)
                is_root = parent_dir.parent == parent_dir
                if not is_root and parent_dir not in seen_parents:
                    seen_parents.add(parent_dir)
                    parent_dirs.append(parent_dir)

                logger.trace(
                    "[PKG_DETECT] Detected package %s from %s "
                    "(root: %s, parent: %s, via_sb=%s)",
                    pkg_name,
                    file_path,
                    pkg_root,
                    parent_dir,
                    detected_via_sb,
                )

        # Also detect directories as namespace packages if they contain
        # subdirectories that are packages (namespace packages)
        # This must happen BEFORE adding package_name to detected, so we can check
        # if base_name == package_name correctly
        # Compute common root of all files to avoid detecting it as a package
        common_root: Path | None = None
        if file_paths:
            common_root = file_paths[0].parent
            for file_path in file_paths[1:]:
                # Find common prefix of paths
                common_parts = [
                    p
                    for p, q in zip(
                        common_root.parts, file_path.parent.parts, strict=False
                    )
                    if p == q
                ]
                if common_parts:
                    common_root = Path(*common_parts)
                else:
                    # No common root, use first file's parent
                    common_root = file_paths[0].parent
                    break

        # Build set of source_bases paths for quick lookup
        source_bases_paths: set[Path] = set()
        if source_bases:
            for base_str in source_bases:
                base_path = Path(base_str).resolve()
                if base_path.exists() and base_path.is_dir():
                    source_bases_paths.add(base_path)

        # Check all detected packages' parent directories to see if they should
        # be detected as namespace packages
        # Only detect namespace packages when using source_bases
        if source_bases:
            checked_parents: set[Path] = set()
            for file_path in file_paths:
                file_path_resolved = file_path.resolve()
                pkg_root = ApatheticUtils_Internal_Modules._find_package_root_for_file(
                    file_path, source_bases=source_bases
                )
                if pkg_root:
                    pkg_name = pkg_root.name
                    # Only check parents if this package was detected via source_bases
                    if pkg_name not in detected_via_source_bases:
                        continue

                    pkg_parent = pkg_root.parent.resolve()
                    # Skip if we've already checked this parent
                    if pkg_parent in checked_parents:
                        continue
                    checked_parents.add(pkg_parent)

                    # Skip if parent is filesystem root
                    if pkg_parent == pkg_parent.parent:
                        continue

                    parent_name = pkg_parent.name
                    # Skip if empty name, already detected, is package_name,
                    # is the common root, or is in source_bases
                    if (
                        not parent_name
                        or parent_name in detected
                        or parent_name == package_name
                        or (common_root and pkg_parent == common_root.resolve())
                        or pkg_parent in source_bases_paths
                    ):
                        logger.trace(
                            "[PKG_DETECT] Skipping parent %s: name=%s, in_detected=%s, "
                            "is_package_name=%s, is_common_root=%s, in_source_bases=%s",
                            pkg_parent,
                            parent_name,
                            parent_name in detected,
                            parent_name == package_name,
                            common_root and pkg_parent == common_root.resolve(),
                            pkg_parent in source_bases_paths,
                        )
                        continue

                    # This parent contains a detected package, so it's also a package
                    detected.add(parent_name)
                    detected_via_source_bases.add(parent_name)
                    logger.trace(
                        "[PKG_DETECT] Detected parent directory as namespace package: "
                        "%s (contains package: %s)",
                        parent_name,
                        pkg_root.name,
                    )

        # Always include configured package (for fallback and multi-package scenarios)
        detected.add(package_name)

        # Return parent directories as absolute paths
        normalized_parents: list[str] = []
        seen_normalized: set[str] = set()

        for parent_dir in parent_dirs:
            base_str = str(parent_dir)
            if base_str not in seen_normalized:
                seen_normalized.add(base_str)
                normalized_parents.append(base_str)

        if len(detected) == 1 and package_name in detected:
            logger.debug(
                "Package detection: No packages found, using configured package '%s'",
                package_name,
            )
        else:
            logger.debug(
                "Package detection: Found %d package(s): %s",
                len(detected),
                sorted(detected),
            )

        return detected, normalized_parents

    @staticmethod
    def find_all_packages_under_path(root_path: Path) -> set[str]:
        """Find all package names under a directory by scanning for __init__.py files.

        Args:
            root_path: Path to the root directory to scan

        Returns:
            Set of package names found under the root directory
        """
        detected: set[str] = set()

        root_path = root_path.resolve()
        if not root_path.exists():
            return detected

        # Find all __init__.py files under root_path
        for init_file in root_path.rglob("__init__.py"):
            # Find the package root by walking up
            pkg_root = ApatheticUtils_Internal_Modules._find_package_root_for_file(
                init_file
            )
            if pkg_root:
                # Extract package name from root directory name
                # Relative to root_path to get the top-level package name
                try:
                    rel_path = pkg_root.relative_to(root_path)
                    # The first component is the top-level package name
                    top_level_pkg = rel_path.parts[0]
                    detected.add(top_level_pkg)
                except ValueError:
                    # If pkg_root is not under root_path, skip it
                    pass

        return detected
