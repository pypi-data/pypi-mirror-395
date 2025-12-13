from __future__ import annotations

import json
from typing import Any

from .hints import get_hint
from .run_line import build_run_line
from .schema import Command, Option, PithSchema
from .search import SearchResult
from .types import TierLevel


def render_tier0(schema: PithSchema) -> str:
    commands = ", ".join(schema.command_names())
    lines = [
        f"{schema.tool}: {schema.pith}",
        f"commands: {commands}",
        f"run: {build_run_line(schema, tier=0)}",
        get_hint(schema, None, 0),
    ]
    return "\n".join(line for line in lines if line)


def _format_option(option: Option) -> str:
    aliases = " / ".join(option.aliases) if option.aliases else f"--{option.name}"
    required = "required" if option.required else "optional"
    # Show default value when present and meaningful
    default_info = ""
    if not option.required and option.default is not None:
        default_info = f", default={option.default}"
    return (
        f"  {aliases}  {option.type}  {option.description} ({required}{default_info})"
    )


def _render_command_tier(schema: PithSchema, command: Command, level: TierLevel) -> str:
    lines: list[str] = [f"{command.name}: {command.pith}"]

    # Use tier-appropriate run-line: tier1.run override, or build dynamically
    run_line = command.tier1.run or build_run_line(schema, command, tier=level)
    lines.append(f"run: {run_line}")

    # Show intents at tier 1+ for semantic search/agent discoverability
    if command.intents:
        lines.append(f"intents: {', '.join(command.intents)}")

    if level >= 2 and command.tier2:
        if command.tier2.arguments:
            lines.append("arguments:")
            for arg in command.tier2.arguments:
                required = "required" if arg.required else "optional"
                lines.append(
                    f"  {arg.name}  {arg.type}  {arg.description} ({required})"
                )
        if command.tier2.options:
            lines.append("options:")
            for opt in command.tier2.options:
                lines.append(_format_option(opt))

    if level >= 3 and command.tier3:
        if command.tier3.examples:
            lines.append("examples:")
            for example in command.tier3.examples:
                lines.append(f"  - {example}")
        if command.tier3.related:
            lines.append("related:")
            lines.append("  " + ", ".join(command.tier3.related))

    hint = get_hint(schema, command, level)
    if hint:
        lines.append(hint)

    return "\n".join(lines)


def render_tier1(schema: PithSchema, command_name: str) -> str:
    command = schema.commands[command_name]
    return _render_command_tier(schema, command, 1)


def render_tier2(schema: PithSchema, command_name: str) -> str:
    command = schema.commands[command_name]
    return _render_command_tier(schema, command, 2)


def render_tier3(schema: PithSchema, command_name: str) -> str:
    command = schema.commands[command_name]
    return _render_command_tier(schema, command, 3)


# --- JSON Renderers (agent-optimized) ---


def _next_tier_hint(
    schema: PithSchema, command: Command | None, level: TierLevel
) -> str | None:
    """Return the command to get the next tier, or None if at tier 3."""
    if level >= 3:
        return None
    if command is None:
        return f"{schema.tool} pith <command>"
    if level == 1:
        return f"{schema.tool} pith {command.name} -v"
    return f"{schema.tool} pith {command.name} -vv"


def render_tier0_json(schema: PithSchema) -> str:
    """Render tier 0 (app overview) as JSON for agent consumption."""
    data: dict[str, Any] = {
        "tool": schema.tool,
        "pith": schema.pith,
        "tier": 0,
        "commands": [
            {"name": name, "pith": schema.commands[name].pith}
            for name in schema.command_names()
        ],
        "run": build_run_line(schema, tier=0),
        "next_tier": _next_tier_hint(schema, None, 0),
    }
    return json.dumps(data, indent=2)


def _argument_to_dict(arg: Any) -> dict[str, Any]:
    """Convert an Argument to a dict for JSON serialization."""
    return {
        "name": arg.name,
        "type": arg.type,
        "description": arg.description,
        "required": arg.required,
        "default": arg.default,
    }


def _option_to_dict(opt: Option) -> dict[str, Any]:
    """Convert an Option to a dict for JSON serialization.

    Uses the primary CLI alias as the name for agent-friendly output.
    """
    # Use primary alias as CLI-friendly name (e.g., "--force" instead of "force")
    cli_name = opt.aliases[0] if opt.aliases else f"--{opt.name}"
    return {
        "name": cli_name,
        "aliases": opt.aliases,
        "type": opt.type,
        "description": opt.description,
        "required": opt.required,
        "default": opt.default,
    }


def render_tier1_json(schema: PithSchema, command_name: str) -> str:
    """Render tier 1 (command summary) as JSON for agent consumption."""
    command = schema.commands[command_name]
    run_line = command.tier1.run or build_run_line(schema, command, tier=1)
    data: dict[str, Any] = {
        "name": command.name,
        "pith": command.pith,
        "tier": 1,
        "run": run_line,
        "intents": command.intents,
        "next_tier": _next_tier_hint(schema, command, 1),
    }
    return json.dumps(data, indent=2)


def render_tier2_json(schema: PithSchema, command_name: str) -> str:
    """Render tier 2 (full signature) as JSON for agent consumption."""
    command = schema.commands[command_name]
    run_line = command.tier1.run or build_run_line(schema, command, tier=2)
    data: dict[str, Any] = {
        "name": command.name,
        "pith": command.pith,
        "tier": 2,
        "run": run_line,
        "intents": command.intents,
        "arguments": [],
        "options": [],
        "next_tier": _next_tier_hint(schema, command, 2),
    }
    if command.tier2:
        data["arguments"] = [_argument_to_dict(arg) for arg in command.tier2.arguments]
        data["options"] = [_option_to_dict(opt) for opt in command.tier2.options]
    return json.dumps(data, indent=2)


def render_tier3_json(schema: PithSchema, command_name: str) -> str:
    """Render tier 3 (examples/related) as JSON for agent consumption."""
    command = schema.commands[command_name]
    run_line = command.tier1.run or build_run_line(schema, command, tier=3)
    data: dict[str, Any] = {
        "name": command.name,
        "pith": command.pith,
        "tier": 3,
        "run": run_line,
        "intents": command.intents,
        "arguments": [],
        "options": [],
        "examples": [],
        "related": [],
        "next_tier": None,
    }
    if command.tier2:
        data["arguments"] = [_argument_to_dict(arg) for arg in command.tier2.arguments]
        data["options"] = [_option_to_dict(opt) for opt in command.tier2.options]
    if command.tier3:
        data["examples"] = command.tier3.examples
        data["related"] = command.tier3.related
    return json.dumps(data, indent=2)


# --- Search Result Renderers ---


def render_search_results(
    schema: PithSchema,
    results: list[SearchResult],
    query: str,
) -> str:
    """Render search results as human-readable text.

    Args:
        schema: The PithSchema that was searched
        results: List of SearchResult from search_commands()
        query: The original search query

    Returns:
        Formatted text output with matching commands
    """
    if not results:
        lines = [
            f"No commands matching '{query}'",
            f"run: {build_run_line(schema, tier=0)}",
            f"↳ {schema.tool} pith to see all commands",
        ]
        return "\n".join(lines)

    lines = ["Matching commands:"]
    for result in results:
        lines.append(f"  {result.command} ({result.score:.2f}) - {result.summary}")

    lines.append(f"run: {build_run_line(schema, tier=0)}")
    lines.append(f"↳ {schema.tool} pith <command> for details")

    return "\n".join(lines)


def render_search_results_json(
    schema: PithSchema,
    results: list[SearchResult],
    query: str,
) -> str:
    """Render search results as JSON for agent consumption.

    Args:
        schema: The PithSchema that was searched
        results: List of SearchResult from search_commands()
        query: The original search query

    Returns:
        JSON string with search results
    """
    data: dict[str, Any] = {
        "query": query,
        "results": [
            {
                "command": result.command,
                "score": result.score,
                "summary": result.summary,
            }
            for result in results
        ],
        "run": build_run_line(schema, tier=0),
    }
    return json.dumps(data, indent=2)
