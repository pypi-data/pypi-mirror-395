from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .app import SubcommandGroup


@dataclass
class CommandDefinition:
    name: str
    callback: Callable[..., Any]
    summary: str
    intents: list[str] = field(default_factory=lambda: [])
    hints: list[str] = field(default_factory=lambda: [])
    examples: list[str] = field(default_factory=lambda: [])
    priority: int = 50  # 1-100, lower = more important (shown first)
    aliases: list[str] = field(default_factory=lambda: [])  # Command aliases
    subcommands: dict[str, "CommandDefinition"] = field(
        default_factory=lambda: {}
    )  # Nested subcommands
    subcommand_aliases: dict[str, str] = field(
        default_factory=lambda: {}
    )  # Maps subcommand alias -> canonical name
    subcommand_group: "SubcommandGroup | None" = field(
        default=None, repr=False
    )  # Reference to subcommand group for decorator access
