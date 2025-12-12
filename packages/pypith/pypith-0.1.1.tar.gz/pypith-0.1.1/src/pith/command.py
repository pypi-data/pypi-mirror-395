from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any


@dataclass
class CommandDefinition:
    name: str
    callback: Callable[..., Any]
    summary: str
    intents: list[str] = field(default_factory=lambda: [])
    hints: list[str] = field(default_factory=lambda: [])
    examples: list[str] = field(default_factory=lambda: [])
    priority: int = 50  # 1-100, lower = more important (shown first)
