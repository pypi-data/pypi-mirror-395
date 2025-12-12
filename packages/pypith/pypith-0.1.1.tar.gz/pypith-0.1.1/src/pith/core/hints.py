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
