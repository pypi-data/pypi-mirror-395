"""Utility functions for Pith applications.

This module provides utilities for interactive prompts, error handling, and output,
enabling Pith-based CLIs to offer a rich command-line experience with agent-friendly
progressive discovery.
"""

from __future__ import annotations

import sys
from typing import TypeVar

T = TypeVar("T")


class PithException(Exception):
    """Base exception for Pith CLI errors.

    Provides clean error formatting similar to Click's ClickException.
    When raised, the CLI will display the error message and exit with code 1.
    """

    def __init__(
        self, message: str, exit_code: int = 1, hint: str | None = None
    ) -> None:
        super().__init__(message)
        self.message = message
        self.exit_code = exit_code
        self.hint = hint

    def show(self) -> None:
        """Display the error message to stderr."""
        sys.stderr.write(f"Error: {self.message}\n")
        if self.hint:
            sys.stderr.write(f"{self.hint}\n")


def prompt(
    text: str,
    default: T | None = None,
    type: type[T] | None = None,
    show_default: bool = True,
    choices: list[str] | None = None,
) -> T:
    """Prompt the user for input.

    Args:
        text: The prompt text to display.
        default: Default value if user presses Enter.
        type: Type to convert the input to.
        show_default: Whether to show the default value in the prompt.
        choices: Optional list of valid choices.

    Returns:
        The user's input, converted to the specified type.

    Raises:
        PithException: If input is invalid or user aborts.
    """
    prompt_text = text
    if choices:
        prompt_text = f"{text} [{'/'.join(choices)}]"
    if default is not None and show_default:
        prompt_text = f"{prompt_text} [{default}]"
    prompt_text = f"{prompt_text}: "

    while True:
        try:
            value = input(prompt_text).strip()
        except (EOFError, KeyboardInterrupt):
            sys.stderr.write("\nAborted.\n")
            raise PithException("Aborted by user", exit_code=1) from None

        # Use default if empty
        if not value:
            if default is not None:
                return default  # type: ignore[return-value]
            # No default, value required
            sys.stderr.write("Error: Value required.\n")
            continue

        # Validate choices
        if choices and value not in choices:
            sys.stderr.write(
                f"Error: Invalid choice. Choose from: {', '.join(choices)}\n"
            )
            continue

        # Convert type
        if type is not None:
            try:
                return type(value)  # type: ignore[return-value]
            except (ValueError, TypeError):
                sys.stderr.write(f"Error: Invalid value for type {type.__name__}.\n")
                continue

        return value  # type: ignore[return-value]


def confirm(text: str, default: bool = False) -> bool:
    """Prompt the user for yes/no confirmation.

    Args:
        text: The confirmation text to display.
        default: Default value if user presses Enter.

    Returns:
        True if user confirms, False otherwise.
    """
    suffix = " [Y/n]" if default else " [y/N]"
    prompt_text = f"{text}{suffix}: "

    try:
        value = input(prompt_text).strip().lower()
    except (EOFError, KeyboardInterrupt):
        sys.stderr.write("\nAborted.\n")
        return False

    if not value:
        return default
    return value in ("y", "yes", "true", "1")


def echo(message: str, *, err: bool = False, nl: bool = True) -> None:
    """Print a message to stdout or stderr.

    Args:
        message: The message to print.
        err: If True, print to stderr instead of stdout.
        nl: If True, append a newline.
    """
    stream = sys.stderr if err else sys.stdout
    stream.write(message)
    if nl:
        stream.write("\n")
    stream.flush()
