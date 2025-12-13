from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import datetime
from typing import Any


@dataclass
class SchemaMetadata:
    """Optional metadata about schema generation."""

    original_path: str | None = None
    tool_version: str | None = None
    generated_at: str | None = None
    generator: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {k: v for k, v in asdict(self).items() if v is not None}

    @classmethod
    def create(
        cls,
        original_path: str | None = None,
        tool_version: str | None = None,
        generator: str = "pypith-cli",
    ) -> SchemaMetadata:
        return cls(
            original_path=original_path,
            tool_version=tool_version,
            generated_at=datetime.now().isoformat(),
            generator=generator,
        )


@dataclass
class Argument:
    name: str
    description: str
    type: str = "text"
    required: bool = True
    default: Any = None  # Native JSON types: bool, int, float, str, None


@dataclass
class Option:
    name: str
    aliases: list[str]
    description: str
    type: str = "text"
    required: bool = False
    default: Any = None  # Native JSON types: bool, int, float, str, None


@dataclass
class Tier1:
    summary: str
    run: str


@dataclass
class Tier2:
    arguments: list[Argument] = field(default_factory=lambda: [])
    options: list[Option] = field(default_factory=lambda: [])


@dataclass
class Tier3:
    examples: list[str] = field(default_factory=lambda: [])
    related: list[str] = field(default_factory=lambda: [])


@dataclass
class Command:
    name: str
    pith: str
    tier1: Tier1
    tier2: Tier2 | None = None
    tier3: Tier3 | None = None
    intents: list[str] = field(default_factory=lambda: [])
    priority: int = 50  # 1-100, lower = more important (shown first in tier 0)
    aliases: list[str] = field(default_factory=lambda: [])  # Command aliases
    subcommands: dict[str, "Command"] | None = None  # Nested subcommands

    def to_dict(self) -> dict[str, object]:
        result = asdict(self)
        # Convert subcommands dict properly
        if self.subcommands:
            result["subcommands"] = {
                name: cmd.to_dict() for name, cmd in self.subcommands.items()
            }
        return result

    def to_json(self, indent: int | None = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent)

    def subcommand_names(self) -> list[str]:
        """Return subcommand names ordered by priority, then alphabetically."""
        if not self.subcommands:
            return []
        return sorted(
            self.subcommands.keys(),
            key=lambda name: (self.subcommands[name].priority, name),  # type: ignore[union-attr]
        )


@dataclass
class PithSchema:
    tool: str
    pith: str
    commands: dict[str, Command]
    schema_version: str = "1.0"
    metadata: SchemaMetadata | None = None

    def to_dict(self) -> dict[str, object]:
        result: dict[str, object] = {
            "schema_version": self.schema_version,
            "tool": self.tool,
            "pith": self.pith,
            "commands": {name: cmd.to_dict() for name, cmd in self.commands.items()},
        }
        if self.metadata:
            result["metadata"] = self.metadata.to_dict()
        return result

    def to_json(self, indent: int | None = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent)

    def command_names(self) -> list[str]:
        """Return command names ordered by priority (lower first), then alphabetically."""
        return sorted(
            self.commands.keys(),
            key=lambda name: (self.commands[name].priority, name),
        )

    def add_command(self, command: Command) -> None:
        self.commands[command.name] = command
