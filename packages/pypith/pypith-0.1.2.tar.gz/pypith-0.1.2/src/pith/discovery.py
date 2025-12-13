from __future__ import annotations

import json
from pathlib import Path
from typing import cast

from .command import CommandDefinition
from .core import (
    PithSchema,
    render_search_results,
    render_search_results_json,
    render_tier0,
    render_tier0_json,
    render_tier1,
    render_tier1_json,
    render_tier2,
    render_tier2_json,
    render_tier3,
    render_tier3_json,
    search_commands,
)
from .core.types import TierLevel


def render_overview(schema: PithSchema, *, use_json: bool = False) -> str:
    """Render tier 0 app overview in text or JSON format."""
    if use_json:
        return render_tier0_json(schema)
    return render_tier0(schema)


def render_command(
    schema: PithSchema,
    command: CommandDefinition,
    level: int,
    *,
    use_json: bool = False,
) -> str:
    """Render command at specified tier level in text or JSON format."""
    tier_level = cast("TierLevel", max(1, min(level, 3)))
    if use_json:
        if tier_level == 1:
            return render_tier1_json(schema, command.name)
        if tier_level == 2:
            return render_tier2_json(schema, command.name)
        return render_tier3_json(schema, command.name)
    if tier_level == 1:
        return render_tier1(schema, command.name)
    if tier_level == 2:
        return render_tier2(schema, command.name)
    return render_tier3(schema, command.name)


def render_search(
    schema: PithSchema,
    query: str,
    *,
    use_json: bool = False,
    limit: int = 5,
    min_score: float = 0.1,
) -> str:
    """Search commands by query and render results.

    Args:
        schema: The PithSchema to search
        query: Natural language search query
        use_json: Output as JSON if True
        limit: Maximum results to return
        min_score: Minimum score threshold (0.0-1.0)

    Returns:
        Formatted search results
    """
    results = search_commands(
        schema, query, limit=limit, min_score=min_score, use_semantic=True
    )
    if use_json:
        return render_search_results_json(schema, results, query)
    return render_search_results(schema, results, query)


def export_schema(schema: PithSchema, path: str | None = None) -> str:
    content = json.dumps(schema.to_dict(), indent=2)
    if path:
        Path(path).write_text(content, encoding="utf-8")
    return content
