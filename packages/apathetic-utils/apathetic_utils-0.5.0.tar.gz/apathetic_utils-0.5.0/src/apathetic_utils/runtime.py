# src/apathetic_utils/runtime.py
"""Build and runtime utilities for testing."""

from __future__ import annotations

import importlib
import importlib.util
import os
import subprocess
import sys
from pathlib import Path
from typing import TYPE_CHECKING, Any

import pytest
from apathetic_logging import makeSafeTrace

from .modules import ApatheticUtils_Internal_Modules
from .subprocess_utils import ApatheticUtils_Internal_Subprocess


if TYPE_CHECKING:
    from types import ModuleType


class ApatheticUtils_Internal_Runtime:  # noqa: N801  # pyright: ignore[reportUnusedClass]
    """Mixin class providing build and runtime utilities for testing."""

    @staticmethod
    def detect_runtime_mode(package_name: str) -> str:  # noqa: PLR0911
        """Detect the current runtime mode.

        Args:
            package_name: Name of the package to check for stitched mode

        Returns:
            - "frozen" if running as a frozen executable
            - "zipapp" if running as a .pyz zipapp
            - "stitched" if running as a stitched single-file script
                (detects both __STITCHED__ and __STANDALONE__ markers)
            - "package" if running from package
        """
        if getattr(sys, "frozen", False):
            return "frozen"
        # Check for zipapp mode by looking for an attribute on __main__
        # named after this module's __file__ path that ends with .pyz
        if "__main__" in sys.modules:
            main_mod = sys.modules["__main__"]
            # Get this module's __file__ path to use as attribute name
            runtime_file = __file__
            zipapp_path = getattr(main_mod, runtime_file, "")
            if isinstance(zipapp_path, str) and zipapp_path.endswith(".pyz"):
                return "zipapp"
        # Check for stitched mode in multiple locations
        # Supports both __STITCHED__ and __STANDALONE__ for backward compatibility
        # 1. Current module's globals (for when called from within stitched script)
        # This works when all files are stitched into a single namespace
        if "__STITCHED__" in globals() or "__STANDALONE__" in globals():
            return "stitched"
        # 2. Check package module's globals (when loaded via importlib)
        # The stitched script is loaded as the package
        pkg_mod = sys.modules.get(package_name)
        if pkg_mod is not None and (
            hasattr(pkg_mod, "__STITCHED__") or hasattr(pkg_mod, "__STANDALONE__")
        ):
            return "stitched"
        # 3. Check __main__ module's globals (for script execution)
        if "__main__" in sys.modules:
            main_mod = sys.modules["__main__"]
            if hasattr(main_mod, "__STITCHED__") or hasattr(main_mod, "__STANDALONE__"):
                return "stitched"
        return "package"

    @staticmethod
    def _check_needs_rebuild(output_path: Path, src_dir: Path) -> bool:
        """Check if output file needs to be rebuilt.

        Args:
            output_path: Path to the output file
            src_dir: Directory containing source files to check

        Returns:
            True if rebuild is needed, False otherwise
        """
        if not output_path.exists():
            return True
        output_mtime_ns = output_path.stat().st_mtime_ns
        for src_file in src_dir.rglob("*.py"):
            if src_file.stat().st_mtime_ns > output_mtime_ns:
                return True
        return False

    @staticmethod
    def _validate_build_output(output_path: Path, build_type: str) -> None:
        """Validate that build output was created successfully.

        Args:
            output_path: Path to the output file
            build_type: Type of build (e.g., "stitched script", "zipapp")

        Raises:
            RuntimeError: If output file doesn't exist after build
        """
        # Force mtime update in case contents identical
        output_path.touch()
        if not output_path.exists():
            msg = f"❌ Failed to generate {build_type}."
            raise RuntimeError(msg)

    @staticmethod
    def _run_bundler_script(
        root: Path,
        command_path: str | None,
        output_path: Path,
        build_type: str,
    ) -> bool:
        """Run a custom bundler script if provided and exists.

        Args:
            root: Project root directory
            command_path: Optional path to bundler script (relative to root)
            output_path: Path to the expected output file
            build_type: Type of build (e.g., "stitched script", "zipapp")

        Returns:
            True if bundler script was run successfully,
            False if not provided or doesn't exist
        """
        if command_path is None:
            return False

        bundler_path = root / command_path
        if not bundler_path.exists():
            return False

        print(  # noqa: T201
            f"⚙️  Rebuilding {build_type} (python {command_path})..."
        )
        subprocess.run(  # noqa: S603
            [sys.executable, str(bundler_path)],
            check=True,
            cwd=root,
        )
        ApatheticUtils_Internal_Runtime._validate_build_output(output_path, build_type)
        return True

    @staticmethod
    def ensure_stitched_script_up_to_date(
        *,
        root: Path,
        script_name: str | None = None,
        package_name: str,
        command_path: str | None = None,
        log_level: str | None = None,
    ) -> Path:
        """Rebuild stitched script if missing or outdated.

        Args:
            root: Project root directory
            script_name: Optional name of the stitched script (without .py extension).
                If None, defaults to package_name.
            package_name: Name of the package (e.g., "apathetic_utils")
            command_path: Optional path to bundler script (relative to root).
                If provided and exists, uses `python {command_path}`.
                Otherwise, uses `python -m serger --config .serger.jsonc`.
            log_level: Optional log level to pass to serger.
                If provided, adds `--log-level=<log_level>` to the serger command.

        Returns:
            Path to the stitched script
        """
        # Use package_name as default if script_name not provided
        actual_script_name = package_name if script_name is None else script_name
        bin_path = root / "dist" / f"{actual_script_name}.py"
        src_dir = root / "src" / package_name

        # Check if rebuild is needed
        needs_rebuild = ApatheticUtils_Internal_Runtime._check_needs_rebuild(
            bin_path, src_dir
        )

        if needs_rebuild:
            # Check if command_path is provided and exists
            if ApatheticUtils_Internal_Runtime._run_bundler_script(
                root, command_path, bin_path, "stitched script"
            ):
                return bin_path

            # Fall back to using serger (found via find_python_command)
            config_path = root / ".serger.jsonc"
            if not config_path.exists():
                msg = (
                    "❌ Failed to generate stitched script: "
                    f"serger config not found at {config_path}."
                )
                raise RuntimeError(msg)

            print("⚙️  Rebuilding stitched bundle (serger)...")  # noqa: T201
            serger_cmd = ApatheticUtils_Internal_Subprocess.find_python_command(
                "serger",
                error_hint=(
                    "serger not found. "
                    "Ensure serger is installed in your virtual environment."
                ),
            )
            serger_cmd.extend(["--config", str(config_path)])
            if log_level is not None:
                serger_cmd.extend(["--log-level", log_level])
            subprocess.run(  # noqa: S603
                serger_cmd,
                check=True,
                cwd=root,
            )
            ApatheticUtils_Internal_Runtime._validate_build_output(
                bin_path, "stitched script"
            )

        return bin_path

    @staticmethod
    def ensure_zipapp_up_to_date(
        *,
        root: Path,
        script_name: str | None = None,
        package_name: str,
        command_path: str | None = None,
        log_level: str | None = None,
    ) -> Path:
        """Rebuild zipapp if missing or outdated.

        Args:
            root: Project root directory
            script_name: Optional name of the zipapp (without .pyz extension).
                If None, defaults to package_name.
            package_name: Name of the package (e.g., "apathetic_utils")
            command_path: Optional path to bundler script (relative to root).
                If provided and exists, uses `python {command_path}`.
                Otherwise, uses zipbundler.
            log_level: Optional log level to pass to zipbundler.
                If provided, adds `--log-level=<log_level>` to the zipbundler command.

        Returns:
            Path to the zipapp
        """
        # Use package_name as default if script_name not provided
        actual_script_name = package_name if script_name is None else script_name
        zipapp_path = root / "dist" / f"{actual_script_name}.pyz"
        src_dir = root / "src" / package_name

        # Check if rebuild is needed
        needs_rebuild = ApatheticUtils_Internal_Runtime._check_needs_rebuild(
            zipapp_path, src_dir
        )

        if needs_rebuild:
            # Check if command_path is provided and exists
            if ApatheticUtils_Internal_Runtime._run_bundler_script(
                root, command_path, zipapp_path, "zipapp"
            ):
                return zipapp_path

            # Fall back to using zipbundler
            zipbundler_cmd = ApatheticUtils_Internal_Subprocess.find_python_command(
                "zipbundler",
                error_hint=(
                    "zipbundler not found. "
                    "Ensure zipbundler is installed: poetry install --with dev"
                ),
            )
            print("⚙️  Rebuilding zipapp (zipbundler)...")  # noqa: T201
            cmd = [
                *zipbundler_cmd,
                "-m",
                package_name,
                "-o",
                str(zipapp_path),
                "-q",
                ".",
            ]
            if log_level is not None:
                cmd.extend(["--log-level", log_level])
            subprocess.run(  # noqa: S603
                cmd,
                cwd=root,
                check=True,
            )
            ApatheticUtils_Internal_Runtime._validate_build_output(
                zipapp_path, "zipapp"
            )

        return zipapp_path

    @staticmethod
    def runtime_swap(
        *,
        root: Path,
        package_name: str,
        script_name: str | None = None,
        stitch_command: str | None = None,
        zipapp_command: str | None = None,
        mode: str | None = None,
        log_level: str | None = None,
    ) -> bool:
        """Pre-import hook — runs before any tests or plugins are imported.

        Swaps in the appropriate runtime module based on RUNTIME_MODE:
        - package (default): uses src/{package_name} (no swap needed)
        - stitched: uses dist/{script_name}.py (serger-built single file)
        - zipapp: uses dist/{script_name}.pyz (zipbundler-built zipapp)

        This ensures all test imports work transparently regardless of runtime mode.

        Args:
            root: Project root directory
            package_name: Name of the package (e.g., "apathetic_utils")
            script_name: Optional name of the distributed script (without extension).
                If None, defaults to package_name.
            stitch_command: Optional path to bundler script for stitched mode
                (relative to root). If provided and exists, uses
                `python {stitch_command}`. Otherwise, uses
                `python -m serger --config .serger.jsonc`.
            zipapp_command: Optional path to bundler script for zipapp mode
                (relative to root). If provided and exists, uses
                `python {zipapp_command}`. Otherwise, uses zipbundler.
            mode: Runtime mode override. If None, reads from RUNTIME_MODE env var.
            log_level: Optional log level to pass to serger and zipbundler.
                If provided, adds `--log-level=<log_level>` to their commands.

        Returns:
            True if swap was performed, False if in package mode

        Raises:
            pytest.UsageError: If mode is invalid or build fails
        """
        safe_trace = makeSafeTrace("🧬")

        if mode is None:
            mode = os.getenv("RUNTIME_MODE", "package")

        if mode == "package":
            return False  # Normal package mode; nothing to do.

        # Nuke any already-imported modules from src/ to avoid stale refs.
        # Dynamically detect all modules under src/ instead of hardcoding names.
        src_dir = root / "src"
        modules_to_nuke = ApatheticUtils_Internal_Modules.find_all_packages_under_path(
            src_dir
        )

        for name in list(sys.modules):
            # Check if module name matches any detected module or is a submodule
            for mod_name in modules_to_nuke:
                if name == mod_name or name.startswith(f"{mod_name}."):
                    del sys.modules[name]
                    break

        if mode == "stitched":
            return ApatheticUtils_Internal_Runtime._load_stitched_mode(
                root, package_name, script_name, stitch_command, safe_trace, log_level
            )
        if mode == "zipapp":
            return ApatheticUtils_Internal_Runtime._load_zipapp_mode(
                root, package_name, script_name, zipapp_command, safe_trace, log_level
            )

        # Unknown mode
        xmsg = f"Unknown RUNTIME_MODE={mode!r}. Valid modes: package, stitched, zipapp"
        raise pytest.UsageError(xmsg)

    @staticmethod
    def _load_stitched_mode(
        root: Path,
        package_name: str,
        script_name: str | None,
        command_path: str | None,
        safe_trace: Any,
        log_level: str | None = None,
    ) -> bool:
        """Load stitched single-file script mode."""
        bin_path = ApatheticUtils_Internal_Runtime.ensure_stitched_script_up_to_date(
            root=root,
            script_name=script_name,
            package_name=package_name,
            command_path=command_path,
            log_level=log_level,
        )

        if not bin_path.exists():
            if command_path is None:
                hint_msg = (
                    "Hint: run the bundler (e.g. `poetry run poe build:stitched`)."
                )
            else:
                hint_msg = (
                    f"Hint: run the bundler (e.g. `python {command_path}` "
                    f"or `poetry run poe build:stitched`)."
                )
            xmsg = (
                f"RUNTIME_MODE=stitched but stitched script not found "
                f"at {bin_path}.\n{hint_msg}"
            )
            raise pytest.UsageError(xmsg)

        # Load stitched script as the package.
        spec = importlib.util.spec_from_file_location(package_name, bin_path)
        if not spec or not spec.loader:
            xmsg = f"Could not create import spec for {bin_path}"
            raise pytest.UsageError(xmsg)

        try:
            mod: ModuleType = importlib.util.module_from_spec(spec)
            sys.modules[package_name] = mod
            spec.loader.exec_module(mod)
            safe_trace(f"Loaded stitched module from {bin_path}")
        except Exception as e:
            # Fail fast with context; this is a config/runtime problem.
            error_name = type(e).__name__
            xmsg = (
                f"Failed to import stitched module from {bin_path}.\n"
                f"Original error: {error_name}: {e}\n"
                f"Tip: rebuild the bundle and re-run."
            )
            raise pytest.UsageError(xmsg) from e

        safe_trace(f"✅ Loaded stitched runtime early from {bin_path}")
        return True

    @staticmethod
    def _load_zipapp_mode(
        root: Path,
        package_name: str,
        script_name: str | None,
        command_path: str | None,
        safe_trace: Any,
        log_level: str | None = None,
    ) -> bool:
        """Load zipapp mode.

        Handles zipbundler zipapps which store packages directly in the zip root.
        Python's standard zipimporter can handle this structure directly.
        """
        zipapp_path = ApatheticUtils_Internal_Runtime.ensure_zipapp_up_to_date(
            root=root,
            script_name=script_name,
            package_name=package_name,
            command_path=command_path,
            log_level=log_level,
        )

        if not zipapp_path.exists():
            xmsg = (
                f"RUNTIME_MODE=zipapp but zipapp not found at {zipapp_path}.\n"
                f"Hint: run `poetry run poe build:zipapp`."
            )
            raise pytest.UsageError(xmsg)

        # For zipbundler zipapps, use normal import
        zipapp_str = str(zipapp_path)
        if zipapp_str not in sys.path:
            sys.path.insert(0, zipapp_str)

        try:
            importlib.import_module(package_name)
            safe_trace(f"Loaded zipapp module from {zipapp_path}")
        except Exception as e:
            error_name = type(e).__name__
            xmsg = (
                f"Failed to import zipapp module from {zipapp_path}.\n"
                f"Original error: {error_name}: {e}\n"
                f"Tip: rebuild the zipapp and re-run."
            )
            raise pytest.UsageError(xmsg) from e

        safe_trace(f"✅ Loaded zipapp runtime early from {zipapp_path}")
        return True
