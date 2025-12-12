from __future__ import annotations

from collections.abc import Iterable


def alias_from_click(option_strings: Iterable[str]) -> list[str]:
    """Lightweight helper for migrating Click/Typer options to Pith aliases."""
    return list(option_strings)
