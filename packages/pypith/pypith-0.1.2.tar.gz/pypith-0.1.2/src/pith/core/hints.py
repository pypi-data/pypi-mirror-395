from __future__ import annotations

from .schema import Command, PithSchema
from .types import TierLevel

HINT_PREFIX = "↳ "


def get_hint(schema: PithSchema, command: Command | None, level: TierLevel) -> str:
    if level == 0:
        return (
            f"{HINT_PREFIX}{schema.tool} pith [--json] <command> for details, "
            f"or --find <query> to search"
        )
    if command is None:
        return ""
    if level == 1:
        return f"{HINT_PREFIX}{schema.tool} pith {command.name} -v [--json] for options"
    if level == 2:
        return (
            f"{HINT_PREFIX}{schema.tool} pith {command.name} -vv [--json] for examples"
        )
    return ""


def get_error_hint(schema: PithSchema, command_name: str | None = None) -> str:
    """Generate a helpful hint when an error occurs.

    Args:
        schema: The PithSchema for the application
        command_name: Optional command name for context-specific hints

    Returns:
        A hint string suggesting how to get more information
    """
    if command_name:
        return f"{HINT_PREFIX}Run '{schema.tool} pith {command_name}' to see all options"
    return f"{HINT_PREFIX}Run '{schema.tool} pith <command>' to explore commands"


def get_success_hint(
    schema: PithSchema, command: Command, related_commands: list[str] | None = None
) -> str | None:
    """Generate an optional hint after successful command execution.

    Args:
        schema: The PithSchema for the application
        command: The command that was executed
        related_commands: Optional list of related command names to suggest

    Returns:
        A hint string or None if no contextual hint is available
    """
    # Use tier3.related if available and no explicit related_commands
    if related_commands is None and command.tier3 and command.tier3.related:
        related_commands = command.tier3.related

    if related_commands:
        # Suggest the first related command
        first_related = related_commands[0]
        return f"{HINT_PREFIX}Related: '{schema.tool} {first_related}'"

    return None
