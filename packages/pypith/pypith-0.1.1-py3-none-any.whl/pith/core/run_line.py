from __future__ import annotations

from .schema import Argument, Command, Option, PithSchema, Tier2


def _format_argument(arg: Argument) -> str:
    """Format an argument for run-line display."""
    token = f"<{arg.name}>"
    return token if arg.required else f"[{token}]"


def _format_option(option: Option) -> str:
    """Format an option for run-line display with -short/--long format."""
    # Build alias display: prefer "-s/--long" format
    if option.aliases:
        short_aliases = [
            a for a in option.aliases if a.startswith("-") and not a.startswith("--")
        ]
        long_aliases = [a for a in option.aliases if a.startswith("--")]

        if short_aliases and long_aliases:
            alias = f"{short_aliases[0]}/{long_aliases[0]}"
        else:
            alias = option.aliases[0]
    else:
        alias = f"--{option.name}"

    # Use type for value placeholder (e.g., <path>, <integer>), empty for bool/flag
    is_flag = option.type in ("bool", "flag")
    placeholder = "" if is_flag else f" <{option.type}>"
    body = f"{alias}{placeholder}"
    return body if option.required else f"[{body}]"


def build_run_line(
    schema: PithSchema, command: Command | None = None, tier: int = 2
) -> str:
    """Build a run-line for a command at a specific tier level.

    Args:
        schema: The PithSchema containing tool info
        command: The command to build run-line for (None for tier 0)
        tier: Tier level controlling verbosity:
            - 0: Generic "tool <command> [args...]"
            - 1: Required arguments only "tool cmd <req_arg>"
            - 2+: Full syntax with all arguments and options

    Returns:
        A formatted run-line string
    """
    parts: list[str] = [schema.tool]
    tier2: Tier2 | None = None

    if command is not None:
        parts.append(command.name)
        tier2 = command.tier2

    # Tier 0: Generic syntax for tool overview
    if command is None or tier == 0:
        parts.append("<command>")
        parts.append("[args...]")
        return " ".join(parts)

    # Tier 1+: Include arguments and options based on tier
    if tier2:
        # Tier 1: Required arguments only
        # Tier 2+: All arguments
        for arg in tier2.arguments:
            if tier >= 2 or arg.required:
                parts.append(_format_argument(arg))

        # Tier 1: Show [options] hint if there are any options
        # Tier 2+: Include full options
        if tier == 1 and tier2.options:
            parts.append("[options]")
        elif tier >= 2:
            for opt in tier2.options:
                parts.append(_format_option(opt))

    return " ".join(parts)
