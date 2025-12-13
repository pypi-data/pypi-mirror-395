# src/apathetic_utils/subprocess_utils.py
"""Subprocess utilities for testing."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
from collections.abc import Iterator
from contextlib import contextmanager, suppress
from dataclasses import dataclass
from io import StringIO
from pathlib import Path
from typing import Any


class SubprocessResult:
    """Result from run_with_output() that includes all output in error messages."""

    def __init__(
        self,
        result: subprocess.CompletedProcess[str],
    ) -> None:
        self.result = result

    @property
    def stdout(self) -> str:
        """Captured stdout (includes info messages)."""
        return self.result.stdout

    @property
    def stderr(self) -> str:
        """Captured stderr."""
        return self.result.stderr

    @property
    def returncode(self) -> int:
        """Return code from subprocess."""
        return self.result.returncode

    @property
    def all_output(self) -> str:
        """All output combined: stdout + stderr."""
        parts: list[str] = []
        if self.stdout:
            parts.append(f"=== STDOUT ===\n{self.stdout}")
        if self.stderr:
            parts.append(f"=== STDERR ===\n{self.stderr}")
        return "\n\n".join(parts) if parts else ""


class SubprocessResultWithBypass:
    """Result from run_with_separated_output() with separate bypass output."""

    def __init__(
        self,
        result: subprocess.CompletedProcess[str],
        bypass_output: str,
    ) -> None:
        self.result = result
        self._bypass_output = bypass_output

    @property
    def stdout(self) -> str:
        """Captured stdout (normal output, excluding bypass)."""
        return self.result.stdout

    @property
    def stderr(self) -> str:
        """Captured stderr."""
        return self.result.stderr

    @property
    def bypass_output(self) -> str:
        """Bypass output (written to sys.__stdout__)."""
        return self._bypass_output

    @property
    def returncode(self) -> int:
        """Return code from subprocess."""
        return self.result.returncode

    @property
    def all_output(self) -> str:
        """All output combined: stdout + stderr + bypass."""
        parts: list[str] = []
        if self.stdout:
            parts.append(f"=== STDOUT ===\n{self.stdout}")
        if self.stderr:
            parts.append(f"=== STDERR ===\n{self.stderr}")
        if self.bypass_output:
            parts.append(f"=== BYPASS (__stdout__) ===\n{self.bypass_output}")
        return "\n\n".join(parts) if parts else ""


class ApatheticUtils_Internal_Subprocess:  # noqa: N801  # pyright: ignore[reportUnusedClass]
    """Mixin class providing subprocess utilities for testing."""

    @staticmethod
    def _find_venv_paths() -> list[Path]:
        """Find paths to common virtual environment providers.

        Returns:
            List of venv paths found (Poetry, pipenv, virtualenv/venv, conda)
        """
        venv_paths: list[Path] = []

        # 1. Poetry
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
                if venv_path.exists():
                    venv_paths.append(venv_path)
            except Exception:  # noqa: BLE001, S110
                pass

        # 2. pipenv
        pipenv_cmd = shutil.which("pipenv")
        if pipenv_cmd:
            try:
                venv_path_result = subprocess.run(  # noqa: S603
                    [pipenv_cmd, "--venv"],
                    capture_output=True,
                    text=True,
                    check=True,
                )
                venv_path = Path(venv_path_result.stdout.strip())
                if venv_path.exists():
                    venv_paths.append(venv_path)
            except Exception:  # noqa: BLE001, S110
                pass

        # 3. virtualenv/venv (via VIRTUAL_ENV)
        virtual_env = os.getenv("VIRTUAL_ENV")
        if virtual_env:
            venv_path = Path(virtual_env)
            if venv_path.exists():
                venv_paths.append(venv_path)

        # 4. conda (via CONDA_PREFIX)
        conda_prefix = os.getenv("CONDA_PREFIX")
        if conda_prefix:
            venv_path = Path(conda_prefix)
            if venv_path.exists():
                venv_paths.append(venv_path)

        return venv_paths

    @staticmethod
    def find_python_command(
        command: str,
        *,
        error_hint: str | None = None,
    ) -> list[str]:
        """Find a Python command (module or executable).

        Returns a command list suitable for subprocess.run().
        Tries `python -m <command>` first, then the command directly.

        Also searches in common virtual environment providers:
        - Poetry (via `poetry env info --path`)
        - pipenv (via `pipenv --venv`)
        - virtualenv/venv (via `VIRTUAL_ENV` environment variable)
        - conda (via `CONDA_PREFIX` environment variable)

        Args:
            command: Name of the command to find (e.g., "zipbundler", "serger")
            error_hint: Optional hint message to include in error if command not found.
                If None, generates a default message.

        Returns:
            Command list (e.g., ["python", "-m", "zipbundler"] or ["zipbundler"])

        Raises:
            RuntimeError: If the command is not found

        Example:
            # Find zipbundler
            zipbundler_cmd = find_python_command("zipbundler")
            # Returns: ["python", "-m", "zipbundler"] or ["zipbundler"] or
            # ["/path/to/venv/bin/zipbundler"]

            # Find serger
            serger_cmd = find_python_command("serger")
            # Returns: ["python", "-m", "serger"] or ["serger"] or
            # ["/path/to/venv/bin/serger"]
        """
        # Try python -m <command> first (most reliable)
        try:
            result = subprocess.run(  # noqa: S603
                [sys.executable, "-m", command, "--help"],
                capture_output=True,
                text=True,
                check=False,
            )
            if result.returncode == 0:
                return [sys.executable, "-m", command]
        except Exception:  # noqa: BLE001, S110
            pass

        # Fall back to command directly in PATH
        cmd_path = shutil.which(command)
        if cmd_path:
            return [cmd_path]

        # Try to find in common virtual environment providers
        venv_paths = ApatheticUtils_Internal_Subprocess._find_venv_paths()

        # Check each venv for the command
        for venv_path in venv_paths:
            # Try both bin/ and Scripts/ (Windows)
            for bin_dir_name in ("bin", "Scripts"):
                bin_dir = venv_path / bin_dir_name
                cmd_in_venv = bin_dir / command
                if cmd_in_venv.exists():
                    return [str(cmd_in_venv)]

        # Command not found
        if error_hint is None:
            error_hint = (
                f"{command} not found. "
                f"Ensure {command} is installed in your virtual environment."
            )
        raise RuntimeError(error_hint)

    @dataclass
    class CapturedOutput:
        """Captured stdout, stderr, and merged streams."""

        stdout: StringIO
        stderr: StringIO
        merged: StringIO

        def __str__(self) -> str:
            """Human-friendly representation (merged output)."""
            return self.merged.getvalue()

        def as_dict(self) -> dict[str, str]:
            """Return contents as plain strings for serialization."""
            return {
                "stdout": self.stdout.getvalue(),
                "stderr": self.stderr.getvalue(),
                "merged": self.merged.getvalue(),
            }

    @staticmethod
    @contextmanager
    def capture_output() -> Iterator[ApatheticUtils_Internal_Subprocess.CapturedOutput]:
        """Temporarily capture stdout and stderr.

        Any exception raised inside the block is re-raised with
        the captured output attached as `exc.captured_output`.

        Example:
        from apathetic_utils import apathetic_utils
        from serger.cli import main

        with apathetic_utils.capture_output() as cap:
            exit_code = main(["--config", "my.cfg", "--dry-run"])

        result = {
            "exit_code": exit_code,
            "stdout": cap.stdout.getvalue(),
            "stderr": cap.stderr.getvalue(),
            "merged": cap.merged.getvalue(),
        }

        """
        merged = StringIO()

        class TeeStream(StringIO):
            def write(self, s: str) -> int:
                merged.write(s)
                return super().write(s)

        buf_out, buf_err = TeeStream(), TeeStream()
        old_out, old_err = sys.stdout, sys.stderr
        sys.stdout, sys.stderr = buf_out, buf_err

        cap = ApatheticUtils_Internal_Subprocess.CapturedOutput(
            stdout=buf_out, stderr=buf_err, merged=merged
        )
        try:
            yield cap
        except Exception as e:
            # Attach captured output to the raised exception for API introspection
            e.captured_output = cap  # type: ignore[attr-defined]
            raise
        finally:
            sys.stdout, sys.stderr = old_out, old_err

    @staticmethod
    def run_with_output(
        args: list[str],
        *,
        cwd: Path | str | None = None,
        initial_env: dict[str, str] | None = None,
        env: dict[str, str] | None = None,
        forward_to: str | None = "normal",
        check: bool = False,
        **kwargs: Any,
    ) -> SubprocessResult:
        """Run subprocess and capture all output with optional forwarding.

        This helper captures subprocess output and can optionally forward it to
        different destinations. It ensures captured output is available for error
        messages and can be displayed in real-time if desired.

        Args:
            args: Command and arguments to run
            cwd: Working directory
            initial_env: Initial environment state. If None, uses os.environ.copy().
                If provided, starts with this environment (can be empty dict for
                blank environment).
            env: Additional environment variables to add/override
            forward_to: Where to forward captured output. Options:
                - "bypass": Forward to sys.__stdout__/sys.__stderr__
                  (bypasses capsys) (default)
                - "normal": Forward to sys.stdout/sys.stderr (normal streams)
                - None: Don't forward
            check: If True, raise CalledProcessError on non-zero exit
            **kwargs: Additional arguments passed to subprocess.run()

        Returns:
            SubprocessResult with all captured output

        Example:
            # Use current environment with additional vars
            result = run_with_output(
                [sys.executable, "-m", "serger", "--config", "config.json"],
                cwd=tmp_path,
                env={"LOG_LEVEL": "test"},
            )

            # Forward output to bypass (visible in real-time, bypasses capsys)
            result = run_with_output(
                [sys.executable, "-m", "serger", "--config", "config.json"],
                cwd=tmp_path,
                env={"LOG_LEVEL": "test"},
                forward_to="bypass",
            )

            # On test failure, output will be included
            assert result.returncode == 0, f"Failed: {result.all_output}"
        """
        # Set up environment
        proc_env = os.environ.copy() if initial_env is None else initial_env.copy()

        if env:
            proc_env.update(env)

        # Run subprocess with normal capture
        result = subprocess.run(  # noqa: S603
            args,
            cwd=cwd,
            env=proc_env,
            capture_output=True,
            text=True,
            check=check,
            **kwargs,
        )

        # Forward captured output to specified destination
        if forward_to == "bypass":
            if result.stdout and sys.__stdout__ is not None:
                print(result.stdout, file=sys.__stdout__, end="")
                sys.__stdout__.flush()
            if result.stderr and sys.__stderr__ is not None:
                print(result.stderr, file=sys.__stderr__, end="")
                sys.__stderr__.flush()
        elif forward_to == "normal":
            if result.stdout:
                print(result.stdout, end="")  # noqa: T201
                sys.stdout.flush()
            if result.stderr:
                print(result.stderr, file=sys.stderr, end="")  # noqa: T201
                sys.stderr.flush()

        return SubprocessResult(result=result)

    @staticmethod
    def run_with_separated_output(
        args: list[str],
        *,
        cwd: Path | str | None = None,
        initial_env: dict[str, str] | None = None,
        env: dict[str, str] | None = None,
        check: bool = False,
        **kwargs: Any,
    ) -> SubprocessResultWithBypass:
        """Run subprocess with stdout and __stdout__ captured separately.

        This uses a Python wrapper to modify sys.__stdout__ before the command runs,
        allowing code to write to stdout and __stdout__ normally without any
        changes. Normal output (stdout) is captured, while bypass output
        (__stdout__) goes to the parent's stdout.

        Args:
            args: Command and arguments to run (must be a Python command)
            cwd: Working directory
            initial_env: Initial environment state. If None, uses os.environ.copy().
                If provided, starts with this environment (can be empty dict for
                blank environment).
            env: Additional environment variables to add/override
            check: If True, raise CalledProcessError on non-zero exit
            **kwargs: Additional arguments passed to subprocess.run()

        Returns:
            SubprocessResultWithBypass with separate stdout and bypass_output

        Example:
            result = run_with_separated_output(
                [sys.executable, "-m", "serger", "--config", "config.json"],
                cwd=tmp_path,
                env={"LOG_LEVEL": "test"},
            )
            # stdout contains normal output (captured)
            # bypass_output contains output written to __stdout__
            assert result.returncode == 0, f"Failed: {result.all_output}"
        """
        # Set up environment
        proc_env = os.environ.copy() if initial_env is None else initial_env.copy()

        if env:
            proc_env.update(env)

        # Create Python wrapper script that modifies sys.__stdout__ and runs command
        # For Python commands, we exec the script code in this process
        # Use __import__ to avoid namespace collisions in stitched mode
        wrapper_script = """import sys
import os
import json

# Modify __stdout__ to point to fd 3 (preserved original stdout)
try:
    original_stdout = os.fdopen(3, 'w')
    sys.__stdout__ = original_stdout
except (OSError, ValueError):
    # FD 3 not available, __stdout__ remains unchanged
    pass

# Execute the actual command
# Reconstruct the original command from environment (using JSON for safety)
cmd_json = os.environ.get('_WRAPPED_CMD')
if cmd_json:
    cmd = json.loads(cmd_json)
    if cmd and len(cmd) > 0:
        # If it's a Python command with a script file, exec in this process
        is_python = (
            cmd[0] == sys.executable
            or cmd[0].endswith('python')
            or 'python' in cmd[0]
        )
        if is_python and len(cmd) > 1:
            # Execute the script file in this process (after __stdout__ mod)
            script_path = cmd[1]
            with open(script_path, 'r') as f:
                script_code = f.read()
            # Execute in current namespace so __stdout__ modification applies
            exec(
                compile(script_code, script_path, 'exec'),
                {'__name__': '__main__', '__file__': script_path},
            )
            sys.exit(0)
        else:
            # For other commands, exec directly
            os.execvpe(cmd[0], cmd, os.environ)
    else:
        sys.exit(1)
else:
    sys.exit(1)
"""

        # Create temporary wrapper script
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
            f.write(wrapper_script)
            wrapper_path = f.name

        # Initialize read_pipe before try block
        read_pipe = None
        try:
            # Create pipes for stdout capture
            read_pipe, write_pipe = os.pipe()

            # Set up command in environment (use JSON for safety)
            proc_env["_WRAPPED_CMD"] = json.dumps(args)

            # Create shell command that:
            # 1. Preserves original stdout to fd 3: exec 3>&1
            # 2. Redirects stdout to pipe: exec 1>&{write_pipe}
            # 3. Runs Python wrapper: exec python wrapper.py
            shell_cmd = f"""
exec 3>&1  # Preserve original stdout to fd 3
exec 1>&{write_pipe}  # Redirect stdout to pipe
exec {shutil.which("python3") or sys.executable} {wrapper_path}
"""

            # Run the shell command
            # Note: We can't use capture_output=True because we need pass_fds
            # which is incompatible with capture_output. We need manual PIPE setup.
            result = subprocess.run(  # noqa: S603, UP022
                ["/bin/bash", "-c", shell_cmd],
                cwd=cwd,
                env=proc_env,
                stdout=subprocess.PIPE,  # This captures fd 3 output (bypass)
                stderr=subprocess.PIPE,  # This captures stderr
                text=True,
                check=check,
                pass_fds=(write_pipe,),
                **kwargs,
            )

            # Close write end
            os.close(write_pipe)

            # Read captured stdout from pipe
            captured_stdout = ""
            try:
                with os.fdopen(read_pipe, "r") as f:
                    captured_stdout = f.read()
            except (OSError, ValueError):
                pass

            # Result structure:
            # - result.stdout contains bypass output (from fd 3)
            # - captured_stdout contains normal output (from pipe)
            # - result.stderr contains stderr

            # Create a modified CompletedProcess with swapped stdout
            modified_result = subprocess.CompletedProcess(
                args=args,
                returncode=result.returncode,
                stdout=captured_stdout,  # Normal output from pipe
                stderr=result.stderr,
            )

            return SubprocessResultWithBypass(
                result=modified_result,
                bypass_output=result.stdout,  # Bypass output from fd 3
            )

        finally:
            # Clean up wrapper script
            with suppress(OSError):
                Path(wrapper_path).unlink()
            if read_pipe is not None:
                with suppress(OSError):
                    os.close(read_pipe)
