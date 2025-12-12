from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, get_args, get_origin

REQUIRED = object()


def _is_required(default: Any) -> bool:
    """Check if a default value indicates a required parameter."""
    return default is REQUIRED or default is ...


def infer_pith_type(annotation: Any) -> str:
    """Infer pith type string from Python type annotation.

    Args:
        annotation: A Python type annotation (e.g., bool, Path, int)

    Returns:
        A pith type string: 'flag', 'path', 'integer', 'number', or 'text'
    """
    if annotation is None:
        return "text"

    # Handle Optional types (Union[X, None]) by extracting the non-None type
    origin = get_origin(annotation)
    if origin is not None:
        args = get_args(annotation)
        # For Union types, find the non-None arg
        non_none_args = [a for a in args if a is not type(None)]
        if non_none_args:
            annotation = non_none_args[0]

    # Map Python types to pith types
    if annotation is bool:
        return "flag"
    if annotation is Path or (
        isinstance(annotation, type) and issubclass(annotation, Path)
    ):
        return "path"
    if annotation is int:
        return "integer"
    if annotation is float:
        return "number"

    return "text"


@dataclass
class Argument:
    default: Any = REQUIRED
    pith: str = ""
    type: str = "text"

    @property
    def required(self) -> bool:
        return _is_required(self.default)


@dataclass
class Option:
    default: Any
    aliases: list[str]
    pith: str = ""
    type: str = "text"

    def __init__(self, default: Any, *aliases: str, pith: str = "", type: str = "text"):
        self.default = default
        self.aliases = list(aliases)
        self.pith = pith
        self.type = type

    @property
    def required(self) -> bool:
        return _is_required(self.default)
