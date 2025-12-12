from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .schema import Command, PithSchema

# Lazy-loaded sentence-transformers model
_semantic_model: Any = None
_semantic_available: bool | None = None


def _get_semantic_model() -> Any:
    """Lazy-load sentence-transformers model if available."""
    global _semantic_model, _semantic_available

    if _semantic_available is False:
        return None

    if _semantic_model is not None:
        return _semantic_model

    try:
        from sentence_transformers import (
            SentenceTransformer,  # type: ignore[import-not-found]
        )

        _semantic_model = SentenceTransformer("all-MiniLM-L6-v2")
        _semantic_available = True
        return _semantic_model
    except ImportError:
        _semantic_available = False
        return None


@dataclass
class SearchResult:
    """Result from semantic search."""

    command: str
    score: float
    summary: str


# Keep backward compatibility alias
SemanticResult = SearchResult


def _build_haystack(command: Command) -> str:
    """Build searchable content from command, including tier3."""
    parts = [
        command.name,
        command.pith,
        command.tier1.summary,
        " ".join(command.intents),
    ]

    # Include tier3 content for richer search
    if command.tier3:
        parts.extend(command.tier3.examples)
        parts.extend(command.tier3.related)

    return " ".join(parts).lower()


def _keyword_score(command: Command, tokens: list[str], query: str) -> float:
    """Score command using keyword matching with boosting.

    Scoring strategy:
    - Exact command name match: +0.5 boost
    - Exact intent match: +0.3 boost per intent
    - Token hits in haystack: base score
    """
    haystack = _build_haystack(command)
    query_lower = query.lower()

    # Base score: token hits
    hits = sum(1 for token in tokens if token in haystack)
    base_score = hits / max(len(tokens), 1)

    boost = 0.0

    # Exact command name match
    if command.name.lower() == query_lower or command.name.lower() in tokens:
        boost += 0.5

    # Exact intent match
    for intent in command.intents:
        intent_lower = intent.lower()
        if intent_lower == query_lower:
            boost += 0.3
        elif all(token in intent_lower for token in tokens):
            boost += 0.15

    # Cap total score at 1.0
    return min(base_score + boost, 1.0)


def _semantic_score(command: Command, query: str, model: Any) -> float:
    """Score command using sentence-transformers embeddings."""
    try:
        from sentence_transformers import (
            SentenceTransformer,  # type: ignore[import-not-found]
        )
        from sentence_transformers.util import cos_sim  # type: ignore[import-not-found]

        if not isinstance(model, SentenceTransformer):
            return 0.0

        haystack = _build_haystack(command)

        # Encode query and haystack
        query_embedding = model.encode(query, convert_to_tensor=True)
        haystack_embedding = model.encode(haystack, convert_to_tensor=True)

        # Compute cosine similarity
        similarity = cos_sim(query_embedding, haystack_embedding)
        return float(similarity[0][0])
    except Exception:
        return 0.0


def search_commands(
    schema: PithSchema,
    query: str,
    limit: int = 5,
    min_score: float = 0.1,
    use_semantic: bool = True,
) -> list[SearchResult]:
    """Search commands by natural language query.

    Args:
        schema: The PithSchema to search
        query: Natural language search query
        limit: Maximum number of results to return
        min_score: Minimum score threshold (0.0-1.0), results below are filtered
        use_semantic: Whether to use sentence-transformers if available

    Returns:
        List of SearchResult ordered by descending score
    """
    if not query.strip():
        return []

    tokens = [part.lower() for part in query.split() if part]
    scored: list[SearchResult] = []

    # Try semantic search if enabled
    model = _get_semantic_model() if use_semantic else None

    for name, command in schema.commands.items():
        if model is not None:
            # Use semantic scoring with keyword boost
            semantic = _semantic_score(command, query, model)
            keyword = _keyword_score(command, tokens, query)
            # Blend: 70% semantic, 30% keyword for best of both
            score = 0.7 * semantic + 0.3 * keyword
        else:
            # Fallback to keyword-only scoring
            score = _keyword_score(command, tokens, query)

        if score >= min_score:
            scored.append(
                SearchResult(command=name, score=round(score, 2), summary=command.pith)
            )

    scored.sort(key=lambda result: result.score, reverse=True)
    return scored[:limit]


def search_all_schemas(
    schemas: list[PithSchema],
    query: str,
    limit: int = 10,
    min_score: float = 0.1,
    use_semantic: bool = True,
) -> list[tuple[str, SearchResult]]:
    """Search across multiple schemas (e.g., all wrapped tools).

    Args:
        schemas: List of PithSchema to search
        query: Natural language search query
        limit: Maximum total results
        min_score: Minimum score threshold
        use_semantic: Whether to use sentence-transformers if available

    Returns:
        List of (tool_name, SearchResult) tuples ordered by descending score
    """
    all_results: list[tuple[str, SearchResult]] = []

    for schema in schemas:
        results = search_commands(
            schema, query, limit=limit, min_score=min_score, use_semantic=use_semantic
        )
        for result in results:
            all_results.append((schema.tool, result))

    # Sort by score and limit
    all_results.sort(key=lambda x: x[1].score, reverse=True)
    return all_results[:limit]
