# src/apathetic_utils/testing.py
"""Test utilities mixin for reusable test helpers."""

from __future__ import annotations

import os
import sys
from collections.abc import Callable, Sequence
from contextlib import suppress
from pathlib import Path
from types import ModuleType
from typing import Any
from unittest.mock import MagicMock

import pytest
from apathetic_logging import safeTrace


class ApatheticUtils_Internal_Testing:  # noqa: N801  # pyright: ignore[reportUnusedClass]
    """Mixin class providing reusable test utilities.

    Inherit from this mixin in your test classes to access shared test utilities
    that can be used across multiple projects.
    """

    @staticmethod
    def _short_path(path: str | None) -> str:
        """Return a shortened version of a path for logging."""
        if not path:
            return "n/a"
        # Use a simple approach: show last MAX_PATH_COMPONENTS or full path if shorter
        max_path_components = 3
        path_obj = Path(path)
        parts = path_obj.parts
        if len(parts) > max_path_components:
            return str(Path(*parts[-max_path_components:]))
        return path

    @staticmethod
    def is_running_under_pytest() -> bool:
        """Detect if code is running under pytest.

        Checks multiple indicators:
        - Environment variables set by pytest
        - Command-line arguments containing 'pytest'

        Returns:
            True if running under pytest, False otherwise
        """
        return (
            "pytest" in os.environ.get("_", "")
            or "PYTEST_CURRENT_TEST" in os.environ
            or any(
                "pytest" in arg
                for arg in sys.argv
                if isinstance(arg, str)  # pyright: ignore[reportUnnecessaryIsInstance]
            )
        )

    @staticmethod
    def create_mock_superclass_test(
        mixin_class: type,
        parent_class: type,
        method_name: str,
        camel_case_method_name: str,
        args: tuple[Any, ...],
        kwargs: dict[str, Any],
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """Test that a mixin's snake_case method calls parent's camelCase via super().

        Creates a test class with controlled MRO:
        - TestClass inherits from mixin_class, then MockBaseClass
        - MockBaseClass provides the camelCase method that super() resolves to
        - Mocks the camelCase method and verifies it's called

        Args:
            mixin_class: The mixin class containing the snake_case method
            parent_class: The parent class with the camelCase method
                (e.g., logging.Logger)
            method_name: Name of the snake_case method to test (e.g., "add_filter")
            camel_case_method_name: Name of the camelCase method to mock
                (e.g., "addFilter")
            args: Arguments to pass to the snake_case method
            kwargs: Keyword arguments to pass to the snake_case method
            monkeypatch: pytest.MonkeyPatch fixture for patching

        Raises:
            AssertionError: If the camelCase method was not called as expected
        """
        # Get the real camelCase method from parent class to use as the base
        # implementation. Check if the method exists first.
        if not hasattr(parent_class, camel_case_method_name):
            py_version = f"{sys.version_info[0]}.{sys.version_info[1]}"
            pytest.skip(
                f"{camel_case_method_name} does not exist on {parent_class.__name__} "
                f"(Python {py_version})"
            )
        camel_method_unbound = getattr(parent_class, camel_case_method_name)

        # Create a base class with the camelCase method (what super() resolves to)
        # We define it dynamically so we can use any method name
        # The method needs to exist on the class for patching to work
        def create_method(camel_method: Any) -> Any:
            """Create a method that wraps the parent class method."""

            def method(self: Any, *a: Any, **kw: Any) -> Any:
                return camel_method(self, *a, **kw)

            return method

        mock_base_class = type(
            "MockBaseClass",
            (),
            {camel_case_method_name: create_method(camel_method_unbound)},
        )

        # Create test class: mixin first, then base class
        # MRO: TestLogger -> Mixin -> MockBaseClass -> object
        # When super() is called from Mixin, it resolves to MockBaseClass
        class TestClass(mixin_class, mock_base_class):  # type: ignore[misc, valid-type]
            """Test class with controlled MRO for super() resolution."""

            def __init__(self) -> None:
                mock_base_class.__init__(self)  # type: ignore[misc]

        # Create an instance of our test class
        test_instance = TestClass()

        # Get the snake_case method from the test instance
        snake_method = getattr(test_instance, method_name)
        if snake_method is None:
            msg = f"Method {method_name} not found on {mixin_class.__name__}"
            raise AttributeError(msg)

        # Mock the base class method (what super() resolves to)
        mock_method = MagicMock(wraps=camel_method_unbound)
        monkeypatch.setattr(mock_base_class, camel_case_method_name, mock_method)
        # Call the snake_case method on our test instance
        # Some methods may raise (e.g., invalid arguments)
        # That's okay - we just want to verify the mock was called
        with suppress(Exception):
            snake_method(*args, **kwargs)

        # Verify the underlying method was called
        # For super() calls, this verifies the parent method was invoked
        # When called via super(), the method is bound, so self is implicit
        # The mock receives just the args (self is already bound)
        # This is a "happy path" test - we just verify the method was called
        # (exact argument matching is less important than verifying the call happened)
        if not mock_method.called:
            msg = f"{camel_case_method_name} was not called by {method_name}"
            raise AssertionError(msg)
        # If we have simple args/kwargs, try to verify them more precisely
        # But don't fail if the method has defaults that fill in extra args
        if args and not kwargs:
            # For positional-only calls, check the first few args match
            call_args = mock_method.call_args
            if call_args:
                call_args_pos, _ = call_args
                # Verify at least the first arg matches (if we have args)
                if (
                    call_args_pos
                    and len(call_args_pos) >= len(args)
                    and call_args_pos[: len(args)] != args
                ):
                    msg = (
                        f"Args don't match: expected {args}, "
                        f"got {call_args_pos[: len(args)]}"
                    )
                    raise AssertionError(msg)

    @staticmethod
    def detect_module_runtime_mode(
        mod: ModuleType,
        *,
        stitch_hints: set[str] | None = None,
    ) -> str:
        """Detect the runtime mode of a specific module.

        Determines whether a module was built as part of a stitched single-file
        script, zipapp archive, or standard package by checking for markers and
        file path attributes.

        This check prioritizes marker-based detection (most reliable) but falls
        back to path heuristics for edge cases. It works correctly in:
        - Stitched mode: Modules loaded from a .py stitched script
        - Zipapp mode: Modules loaded from a .pyz zipapp archive
        - Package mode: Regular package modules
        - Mixed scenarios: When testing a stitched module while running in package mode

        Args:
            mod: Module to check
            stitch_hints: Optional set of path hints to identify stitched modules.
                Defaults to {"/dist/", "stitched"}. Used as fallback when markers
                are not present.

        Returns:
            - "stitched" if module has __STITCHED__ or __STANDALONE__ marker,
              or __file__ path matches stitch_hints
            - "zipapp" if module __file__ indicates zipapp (contains .pyz)
            - "package" for regular package modules

        Raises:
            TypeError: If mod is not a ModuleType
        """
        if stitch_hints is None:
            stitch_hints = {"/dist/", "stitched"}

        if not isinstance(mod, ModuleType):  # pyright: ignore[reportUnnecessaryIsInstance]
            msg = f"Expected ModuleType, got {type(mod).__name__}"
            raise TypeError(msg)

        # Check for stitched markers first (most reliable)
        if hasattr(mod, "__STITCHED__") or hasattr(mod, "__STANDALONE__"):
            return "stitched"

        # Check for zipapp and stitched by looking at __file__ path
        file_path = getattr(mod, "__file__", "") or ""
        if ".pyz/" in file_path or file_path.endswith(".pyz"):
            return "zipapp"
        if any(h in file_path for h in stitch_hints):
            return "stitched"

        # Default to package mode
        return "package"

    @staticmethod
    def patch_everywhere(  # noqa: C901, PLR0912, PLR0915
        mp: pytest.MonkeyPatch,
        mod_env: ModuleType | Any,
        func_name: str,
        replacement_func: Callable[..., object],
        *,
        package_prefix: str | Sequence[str],
        stitch_hints: set[str] | None = None,
        create_if_missing: bool = False,
        caller_func_name: str | None = None,
    ) -> None:
        """Replace a function everywhere it was imported.

        Works in both package and stitched single-file runtimes.
        Walks sys.modules once and handles:
          • the defining module
          • any other module that imported the same function object
          • any freshly reloaded stitched modules (heuristic: path matches hints)

        Args:
            mp: pytest.MonkeyPatch instance to use for patching
            mod_env: Module or object containing the function to patch
            func_name: Name of the function to patch
            replacement_func: Function to replace the original with
            package_prefix: Package name prefix(es) to filter modules.
                Can be a single string (e.g., "apathetic_utils") or a sequence
                of strings (e.g., ["apathetic_utils", "my_package"]) to patch
                across multiple packages.
            stitch_hints: Set of path hints to identify stitched modules.
                Defaults to {"/dist/", "stitched"}. When providing custom
                hints, you must be certain of the path attributes of your
                stitched file, as this uses substring matching on the module's
                __file__ path. This is a heuristic fallback when identity
                checks fail (e.g., when modules are reloaded).
            create_if_missing: If True, create the attribute if it doesn't exist.
                If False (default), raise TypeError if the function doesn't exist.
            caller_func_name: If provided, only patch __globals__ for this specific
                function. If None (default), patch __globals__ for all functions in
                the module that reference the original function.
        """
        if stitch_hints is None:
            stitch_hints = {"/dist/", "stitched"}

        # --- Sanity checks ---
        func = getattr(mod_env, func_name, None)
        func_existed = func is not None

        if func is None:
            if create_if_missing:
                # Will create the function below, but don't set func to replacement_func
                # since we need to track that it didn't exist for search logic
                pass
            else:
                xmsg = f"Could not find {func_name!r} on {mod_env!r}"
                raise TypeError(xmsg)

        mod_name = getattr(mod_env, "__name__", type(mod_env).__name__)

        # Patch in the defining module
        # For modules, if the attribute doesn't exist and create_if_missing=True,
        # we need to create it manually first, then use monkeypatch to track it
        if not func_existed and isinstance(mod_env, ModuleType):
            # Manually create the attribute on the module's __dict__
            # This is necessary because monkeypatch.setattr may fail if the attribute
            # doesn't exist on a module
            mod_env.__dict__[func_name] = replacement_func
            # Now register with monkeypatch for cleanup on undo
            # Since the attribute now exists, setattr should work
            mp.setattr(mod_env, func_name, replacement_func)
            safeTrace(f"Patched {mod_name}.{func_name}")
        else:
            try:
                mp.setattr(mod_env, func_name, replacement_func)
            except AttributeError:
                # If setattr fails because attribute doesn't exist on a module,
                # create it manually and try again
                if isinstance(mod_env, ModuleType) and create_if_missing:
                    mod_env.__dict__[func_name] = replacement_func
                    mp.setattr(mod_env, func_name, replacement_func)
                    safeTrace(f"Created and patched {mod_name}.{func_name}")
                else:
                    raise
            if func_existed:
                safeTrace(f"Patched {mod_name}.{func_name}")
            else:
                safeTrace(f"Created and patched {mod_name}.{func_name}")

        # Patch direct function calls via __globals__
        # Module-level functions share the same __globals__ dict (the module's
        # __dict__). We need to patch functions' __globals__ to intercept direct
        # calls (e.g., func() vs mod.func()). This works in both stitched and
        # non-stitched modes.

        # However, for stitched modules, all functions share a single __globals__
        # dict because they're all defined in one file. Patching __globals__ for
        # stitched modules corrupts the shared namespace across multiple test runs.
        # Module-level setattr is sufficient for stitched builds.
        is_stitched_or_zipapp = False
        if isinstance(mod_env, ModuleType):
            # Check if module is stitched or zipapp
            mode = ApatheticUtils_Internal_Testing.detect_module_runtime_mode(
                mod_env,
                stitch_hints=stitch_hints,
            )
            is_stitched_or_zipapp = mode in ("stitched", "zipapp")

        if (
            func_existed
            and isinstance(mod_env, ModuleType)
            and func is not None
            and not is_stitched_or_zipapp
        ):
            _apathetic_testing_priv_patch_globals_for_direct_calls(
                mp=mp,
                mod=mod_env,
                func_name=func_name,
                original_func=func,
                replacement_func=replacement_func,
                safeTrace=safeTrace,
                caller_func_name=caller_func_name,
            )

        patched_ids: set[int] = set()

        for m in list(sys.modules.values()):
            if (
                m is mod_env
                or not isinstance(m, ModuleType)  # pyright: ignore[reportUnnecessaryIsInstance]
                or not hasattr(m, "__dict__")
            ):
                continue

            # skip irrelevant stdlib or third-party modules for performance
            name = getattr(m, "__name__", "")
            if isinstance(package_prefix, str):
                prefixes: Sequence[str] = (package_prefix,)
            else:
                prefixes = package_prefix
            if not any(name.startswith(prefix) for prefix in prefixes):
                continue

            did_patch = False

            # 1) Normal case: module imported the same object
            # Only search if the function actually existed (not created)
            if func_existed:
                for k, v in list(m.__dict__.items()):
                    if v is func:
                        mp.setattr(m, k, replacement_func)
                        did_patch = True

            # 2) Single-file/zipapp case: reloaded stitched modules or zipapp modules
            #    Check for __STITCHED__ marker first (most reliable), then fallback
            #    to path heuristics
            mode = ApatheticUtils_Internal_Testing.detect_module_runtime_mode(
                m,
                stitch_hints=stitch_hints,
            )
            is_stitched_or_zipapp = mode in ("stitched", "zipapp")
            if is_stitched_or_zipapp and hasattr(m, func_name):
                mp.setattr(m, func_name, replacement_func)

                # NOTE: Do NOT patch __globals__ for stitched modules.
                # Stitched modules have all their functions defined in one file,
                # so they share a single __globals__ dict. Patching __globals__
                # would corrupt the shared namespace and break test isolation.
                # The module-level setattr above is sufficient for stitched builds
                # because all direct calls (func()) and qualified calls (mod.func())
                # resolve through the same namespace.
                did_patch = True

            if did_patch and id(m) not in patched_ids:
                patched_ids.add(id(m))
                safeTrace(f"  also patched {name}")


def _apathetic_testing_priv_patch_globals_for_direct_calls(
    *,
    mp: pytest.MonkeyPatch,
    mod: ModuleType,
    func_name: str,
    original_func: Callable[..., object],
    replacement_func: Callable[..., object],
    safeTrace: Callable[..., None],  # noqa: N803
    caller_func_name: str | None = None,
) -> None:
    """Replace a function everywhere it was imported.

    Works in both package and stitched single-file runtimes.
    Walks sys.modules once and handles:
      • the defining module
      • any other module that imported the same function object
      • any freshly reloaded stitched modules (heuristic: path matches hints)

    Args:
        mp: pytest.MonkeyPatch instance to use for patching
        mod: Module containing the function to patch
        func_name: Name of the function to patch
        original_func: The original function object to replace
        replacement_func: Function to replace the original with
        safeTrace: Callable for safe tracing/logging operations
        caller_func_name: If provided, only patch __globals__ for this specific
            function. If None (default), patch __globals__ for all functions in
            the module that reference the original function.
    """
    patched_count = 0
    for name, obj in mod.__dict__.items():
        if not callable(obj):
            continue
        if caller_func_name and name != caller_func_name:
            continue
        if not hasattr(obj, "__globals__"):
            continue
        # Get __globals__ and check if it's actually a dict
        try:
            globals_dict = obj.__globals__
        except (TypeError, AttributeError):
            # __globals__ might be a descriptor or not accessible
            continue
        if not isinstance(globals_dict, dict):  # pyright: ignore[reportUnnecessaryIsInstance]
            # __globals__ is not a dict (could be a descriptor)
            continue
        # Check if this function's __globals__ references the original function
        if func_name in globals_dict:
            current_ref = globals_dict[func_name]
            if current_ref is original_func:
                # Use mp.setitem() to ensure proper restoration when test completes
                # This is critical for test isolation - without it, __globals__
                # modifications persist and affect subsequent tests
                mp.setitem(globals_dict, func_name, replacement_func)
                patched_count += 1
                safeTrace(
                    f"  patched __globals__ for {name}()",
                    f"original_id={id(original_func)}",
                    f"replacement_id={id(replacement_func)}",
                )
            else:
                safeTrace(
                    f"  ⏭️  skipped __globals__ for {name}()",
                    "reference mismatch",
                )
    if patched_count > 0:
        safeTrace(
            f"  patched __globals__ for {patched_count} function(s) in {mod.__name__}"
        )
