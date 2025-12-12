from __future__ import annotations

from collections.abc import Callable, Iterable
from typing import Any


def _merge_meta(
    func: Callable[..., Any], key: str, values: Iterable[str]
) -> Callable[..., Any]:
    meta: dict[str, list[str]] = getattr(func, "_pith_meta", {})
    existing = list(meta.get(key, []))
    existing.extend(values)
    meta[key] = existing
    func._pith_meta = meta  # type: ignore[attr-defined]
    return func


def intents(*intents_values: str) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        return _merge_meta(func, "intents", intents_values)

    return decorator


def hints(*hints_values: str) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        return _merge_meta(func, "hints", hints_values)

    return decorator
