"""Pith library public API.

pypith is an agent-native CLI ecosystem for building discoverable command-line tools.
"""

from .app import Pith, SubcommandGroup

# Re-export core schema types for convenience
from .core import (
    Command,
    PithSchema,
    SchemaMetadata,
    SearchResult,
    Tier1,
    Tier2,
    Tier3,
    build_run_line,
    get_error_hint,
    get_hint,
    get_success_hint,
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
    search_all_schemas,
    search_commands,
)
from .parameters import Argument, Option
from .testing import CliRunner, Result
from .utils import PithException, confirm, echo, prompt

# Note: core.Argument and core.Option are schema dataclasses (different from
# pith.Argument/pith.Option which are decorator-style parameter definitions).
# Access them via pith.core.Argument / pith.core.Option if needed.

__all__ = [
    # Pith library API
    "Argument",
    "CliRunner",
    # Core schema types
    "Command",
    "Option",
    "Pith",
    "PithException",
    "PithSchema",
    "Result",
    "SchemaMetadata",
    "SearchResult",
    "SubcommandGroup",
    "Tier1",
    "Tier2",
    "Tier3",
    # Core functions
    "build_run_line",
    "confirm",
    "echo",
    "get_error_hint",
    "get_hint",
    "get_success_hint",
    "prompt",
    "render_search_results",
    "render_search_results_json",
    "render_tier0",
    "render_tier0_json",
    "render_tier1",
    "render_tier1_json",
    "render_tier2",
    "render_tier2_json",
    "render_tier3",
    "render_tier3_json",
    "search_all_schemas",
    "search_commands",
]
