# src/apathetic_utils/runtime.py
"""Build and runtime utilities for testing."""

from __future__ import annotations

import importlib
import importlib.util
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import TYPE_CHECKING, Any

import pytest
from apathetic_logging import makeSafeTrace

from .modules import ApatheticUtils_Internal_Modules


if TYPE_CHECKING:
    from types import ModuleType


class ApatheticUtils_Internal_Runtime:  # noqa: N801  # pyright: ignore[reportUnusedClass]
    """Mixin class providing build and runtime utilities for testing."""

    @staticmethod
    def detect_runtime_mode(package_name: str) -> str:  # noqa: PLR0911
        """Detect the current runtime mode.

        Args:
            package_name: Name of the package to check for standalone mode

        Returns:
            - "frozen" if running as a frozen executable
            - "zipapp" if running as a .pyz zipapp
            - "standalone" if running as a standalone single-file script
            - "installed" if running from installed package
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
        # Check for standalone mode in multiple locations
        # 1. Current module's globals (for when called from within standalone script)
        # This works when all files are stitched into a single namespace
        if "__STANDALONE__" in globals():
            return "standalone"
        # 2. Check package module's globals (when loaded via importlib)
        # The standalone script is loaded as the package
        pkg_mod = sys.modules.get(package_name)
        if pkg_mod is not None and hasattr(pkg_mod, "__STANDALONE__"):
            return "standalone"
        # 3. Check __main__ module's globals (for script execution)
        if "__main__" in sys.modules:
            main_mod = sys.modules["__main__"]
            if hasattr(main_mod, "__STANDALONE__"):
                return "standalone"
        return "installed"

    @staticmethod
    def find_zipbundler() -> list[str]:
        """Find the zipbundler command.

        Returns a command list suitable for subprocess.run().
        Tries python -m zipbundler first, then zipbundler directly.

        Returns:
            Command list (e.g., ["python", "-m", "zipbundler"] or ["zipbundler"])

        Raises:
            RuntimeError: If zipbundler is not found
        """
        # Try python -m zipbundler first (most reliable)
        try:
            result = subprocess.run(  # noqa: S603
                [sys.executable, "-m", "zipbundler", "--help"],
                capture_output=True,
                text=True,
                check=False,
            )
            if result.returncode == 0:
                return [sys.executable, "-m", "zipbundler"]
        except Exception:  # noqa: BLE001, S110
            pass

        # Fall back to zipbundler directly
        zipbundler_path = shutil.which("zipbundler")
        if zipbundler_path:
            return [zipbundler_path]

        # If not in PATH, try to find it in the poetry venv
        poetry_cmd = shutil.which("poetry")
        if poetry_cmd:
            try:
                venv_path_result = subprocess.run(  # noqa: S603
                    [poetry_cmd, "env", "info", "--path"],
                    capture_output=True,
                    text=True,
                    check=True,
                )
                venv_path = Path(venv_path_result.stdout.strip())
                zipbundler_in_venv = venv_path / "bin" / "zipbundler"
                if zipbundler_in_venv.exists():
                    return [str(zipbundler_in_venv)]
            except Exception:  # noqa: BLE001, S110
                # Poetry command failed or venv path invalid - continue to error
                pass
        msg = (
            "zipbundler not found. "
            "Ensure zipbundler is installed: poetry install --with dev"
        )
        raise RuntimeError(msg)

    @staticmethod
    def ensure_standalone_script_up_to_date(
        *,
        root: Path,
        script_name: str | None = None,
        package_name: str,
        bundler_script: str | None = None,
    ) -> Path:
        """Rebuild standalone script if missing or outdated.

        Args:
            root: Project root directory
            script_name: Optional name of the standalone script (without .py extension).
                If None, defaults to package_name.
            package_name: Name of the package (e.g., "apathetic_utils")
            bundler_script: Optional path to bundler script (relative to root).
                If provided and exists, uses `python {bundler_script}`.
                Otherwise, uses `python -m serger --config .serger.jsonc`.

        Returns:
            Path to the standalone script
        """
        # Use package_name as default if script_name not provided
        actual_script_name = package_name if script_name is None else script_name
        bin_path = root / "dist" / f"{actual_script_name}.py"
        src_dir = root / "src" / package_name

        # If the output file doesn't exist or is older than any source file → rebuild.
        needs_rebuild = not bin_path.exists()
        if not needs_rebuild:
            bin_mtime_ns = bin_path.stat().st_mtime_ns
            for src_file in src_dir.rglob("*.py"):
                if src_file.stat().st_mtime_ns > bin_mtime_ns:
                    needs_rebuild = True
                    break

        if needs_rebuild:
            # Check if bundler_script is provided and exists
            if bundler_script is not None:
                bundler_path = root / bundler_script
                if bundler_path.exists():
                    print(  # noqa: T201
                        f"⚙️  Rebuilding standalone bundle (python {bundler_script})..."
                    )
                    subprocess.run(  # noqa: S603
                        [sys.executable, str(bundler_path)],
                        check=True,
                        cwd=root,
                    )
                    # force mtime update in case contents identical
                    bin_path.touch()
                    if not bin_path.exists():
                        msg = "❌ Failed to generate standalone script."
                        raise RuntimeError(msg)
                    return bin_path

            # Fall back to python -m serger
            config_path = root / ".serger.jsonc"
            if not config_path.exists():
                msg = (
                    "❌ Failed to generate standalone script: "
                    f"serger config not found at {config_path}."
                )
                raise RuntimeError(msg)

            print("⚙️  Rebuilding standalone bundle (python -m serger)...")  # noqa: T201
            subprocess.run(  # noqa: S603
                [
                    sys.executable,
                    "-m",
                    "serger",
                    "--config",
                    str(config_path),
                ],
                check=True,
                cwd=root,
            )
            # force mtime update in case contents identical
            bin_path.touch()
            if not bin_path.exists():
                msg = "❌ Failed to generate standalone script."
                raise RuntimeError(msg)

        return bin_path

    @staticmethod
    def ensure_zipapp_up_to_date(
        *,
        root: Path,
        script_name: str | None = None,
        package_name: str,
    ) -> Path:
        """Rebuild zipapp if missing or outdated.

        Args:
            root: Project root directory
            script_name: Optional name of the zipapp (without .pyz extension).
                If None, defaults to package_name.
            package_name: Name of the package (e.g., "apathetic_utils")

        Returns:
            Path to the zipapp
        """
        # Use package_name as default if script_name not provided
        actual_script_name = package_name if script_name is None else script_name
        zipapp_path = root / "dist" / f"{actual_script_name}.pyz"
        src_dir = root / "src" / package_name

        # If the output file doesn't exist or is older than any source file → rebuild.
        needs_rebuild = not zipapp_path.exists()
        if not needs_rebuild:
            zipapp_mtime_ns = zipapp_path.stat().st_mtime_ns
            for src_file in src_dir.rglob("*.py"):
                if src_file.stat().st_mtime_ns > zipapp_mtime_ns:
                    needs_rebuild = True
                    break

        if needs_rebuild:
            zipbundler_cmd = ApatheticUtils_Internal_Runtime.find_zipbundler()
            print("⚙️  Rebuilding zipapp (zipbundler)...")  # noqa: T201
            subprocess.run(  # noqa: S603
                [
                    *zipbundler_cmd,
                    "-m",
                    package_name,
                    "-o",
                    str(zipapp_path),
                    "-q",
                    ".",
                ],
                cwd=root,
                check=True,
            )
            # force mtime update in case contents identical
            zipapp_path.touch()
            if not zipapp_path.exists():
                msg = "❌ Failed to generate zipapp."
                raise RuntimeError(msg)

        return zipapp_path

    @staticmethod
    def runtime_swap(
        *,
        root: Path,
        package_name: str,
        script_name: str | None = None,
        bundler_script: str | None = None,
        mode: str | None = None,
    ) -> bool:
        """Pre-import hook — runs before any tests or plugins are imported.

        Swaps in the appropriate runtime module based on RUNTIME_MODE:
        - installed (default): uses src/{package_name} (no swap needed)
        - singlefile: uses dist/{script_name}.py (serger-built single file)
        - zipapp: uses dist/{script_name}.pyz (zipbundler-built zipapp)

        This ensures all test imports work transparently regardless of runtime mode.

        Args:
            root: Project root directory
            package_name: Name of the package (e.g., "apathetic_utils")
            script_name: Optional name of the standalone script (without extension).
                If None, defaults to package_name.
            bundler_script: Optional path to bundler script (relative to root).
                If provided and exists, uses `python {bundler_script}`.
                Otherwise, uses `python -m serger --config .serger.jsonc`.
            mode: Runtime mode override. If None, reads from RUNTIME_MODE env var.

        Returns:
            True if swap was performed, False if in installed mode

        Raises:
            pytest.UsageError: If mode is invalid or build fails
        """
        safe_trace = makeSafeTrace("🧬")

        if mode is None:
            mode = os.getenv("RUNTIME_MODE", "installed")

        if mode == "installed":
            return False  # Normal installed mode; nothing to do.

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

        if mode == "singlefile":
            return ApatheticUtils_Internal_Runtime._load_singlefile_mode(
                root, package_name, script_name, bundler_script, safe_trace
            )
        if mode == "zipapp":
            return ApatheticUtils_Internal_Runtime._load_zipapp_mode(
                root, package_name, script_name, safe_trace
            )

        # Unknown mode
        xmsg = (
            f"Unknown RUNTIME_MODE={mode!r}. Valid modes: installed, singlefile, zipapp"
        )
        raise pytest.UsageError(xmsg)

    @staticmethod
    def _load_singlefile_mode(
        root: Path,
        package_name: str,
        script_name: str | None,
        bundler_script: str | None,
        safe_trace: Any,
    ) -> bool:
        """Load standalone single-file script mode."""
        bin_path = ApatheticUtils_Internal_Runtime.ensure_standalone_script_up_to_date(
            root=root,
            script_name=script_name,
            package_name=package_name,
            bundler_script=bundler_script,
        )

        if not bin_path.exists():
            if bundler_script is None:
                hint_msg = "Hint: run the bundler (e.g. `poetry run poe build:script`)."
            else:
                hint_msg = (
                    f"Hint: run the bundler (e.g. `python {bundler_script}` "
                    f"or `poetry run poe build:script`)."
                )
            xmsg = (
                f"RUNTIME_MODE=singlefile but standalone script not found "
                f"at {bin_path}.\n{hint_msg}"
            )
            raise pytest.UsageError(xmsg)

        # Load standalone script as the package.
        spec = importlib.util.spec_from_file_location(package_name, bin_path)
        if not spec or not spec.loader:
            xmsg = f"Could not create import spec for {bin_path}"
            raise pytest.UsageError(xmsg)

        try:
            mod: ModuleType = importlib.util.module_from_spec(spec)
            sys.modules[package_name] = mod
            spec.loader.exec_module(mod)
            safe_trace(f"Loaded standalone module from {bin_path}")
        except Exception as e:
            # Fail fast with context; this is a config/runtime problem.
            error_name = type(e).__name__
            xmsg = (
                f"Failed to import standalone module from {bin_path}.\n"
                f"Original error: {error_name}: {e}\n"
                f"Tip: rebuild the bundle and re-run."
            )
            raise pytest.UsageError(xmsg) from e

        safe_trace(f"✅ Loaded standalone runtime early from {bin_path}")
        return True

    @staticmethod
    def _load_zipapp_mode(
        root: Path,
        package_name: str,
        script_name: str | None,
        safe_trace: Any,
    ) -> bool:
        """Load zipapp mode.

        Handles zipbundler zipapps which store packages directly in the zip root.
        Python's standard zipimporter can handle this structure directly.
        """
        zipapp_path = ApatheticUtils_Internal_Runtime.ensure_zipapp_up_to_date(
            root=root,
            script_name=script_name,
            package_name=package_name,
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
