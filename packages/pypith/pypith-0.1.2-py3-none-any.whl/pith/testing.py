"""Testing utilities for Pith applications.

This module provides a CliRunner-like interface for testing Pith applications,
similar to Click's CliRunner but designed for Pith's execution model.
"""

from __future__ import annotations

import io
import sys
from contextlib import redirect_stderr, redirect_stdout
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .app import Pith


@dataclass
class Result:
    """Result of a CLI invocation.

    Attributes:
        exit_code: The exit code (0 for success, non-zero for failure)
        output: Combined stdout and stderr output
        exception: Any exception that was raised during execution
    """

    exit_code: int
    output: str
    exception: BaseException | None = None


class CliRunner:
    """Test runner for Pith applications.

    Provides a similar interface to Click's CliRunner for testing Pith CLIs.

    Example:
        ```python
        from pith.testing import CliRunner
        from myapp import app

        runner = CliRunner()
        result = runner.invoke(app, ["mycommand", "--flag"])
        assert result.exit_code == 0
        assert "Success" in result.output
        ```
    """

    def __init__(self, mix_stderr: bool = True) -> None:
        """Initialize the runner.

        Args:
            mix_stderr: If True, mix stderr into stdout output (default).
        """
        self.mix_stderr = mix_stderr

    def invoke(
        self,
        app: Pith,
        args: list[str] | None = None,
        input: str | None = None,
    ) -> Result:
        """Invoke a Pith application with the given arguments.

        Args:
            app: The Pith application to invoke.
            args: Command-line arguments (without the program name).
            input: Optional input to provide to stdin.

        Returns:
            A Result object with exit_code, output, and exception.
        """
        args = args or []

        # Capture stdout/stderr
        stdout_buffer = io.StringIO()
        stderr_buffer = io.StringIO()

        # Mock stdin if input provided
        original_stdin = sys.stdin
        if input is not None:
            sys.stdin = io.StringIO(input)

        exit_code = 0
        exception: BaseException | None = None

        try:
            with redirect_stdout(stdout_buffer):
                if self.mix_stderr:
                    with redirect_stderr(stdout_buffer):
                        app.run(args)
                else:
                    with redirect_stderr(stderr_buffer):
                        app.run(args)
        except SystemExit as e:
            exit_code = e.code if isinstance(e.code, int) else 1
        except Exception as e:
            exception = e
            exit_code = 1
        finally:
            sys.stdin = original_stdin

        output = stdout_buffer.getvalue()
        if not self.mix_stderr:
            output += stderr_buffer.getvalue()

        return Result(exit_code=exit_code, output=output, exception=exception)
