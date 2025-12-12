from __future__ import annotations

from dataclasses import dataclass


@dataclass
class DocstringContent:
    """Extracted content from a docstring."""

    examples: list[str]
    related: list[str]


def _is_section_header(line: str, lower: str) -> str | None:
    """Check if line is a section header and return the section name."""
    if lower in ("examples:", "examples"):
        return "examples"
    if lower in ("related:", "related"):
        return "related"
    # Other section-like headers (lines ending with colon)
    if lower.endswith(":") and not line.startswith("$") and not line.startswith("-"):
        return "other"
    return None


def _parse_example_line(line: str) -> str:
    """Parse a single example line."""
    if line.startswith("-"):
        return line.lstrip("- ")
    return line


def _parse_related_lines(line: str) -> list[str]:
    """Parse related items from a line (may be comma-separated)."""
    if line.startswith("-"):
        return [line.lstrip("- ").strip()]
    # Split on comma for comma-separated related items
    return [item.strip() for item in line.split(",") if item.strip()]


def extract_docstring_content(docstring: str | None) -> DocstringContent:
    """Extract examples and related sections from a docstring.

    Args:
        docstring: The function docstring to parse

    Returns:
        DocstringContent with examples and related lists
    """
    if not docstring:
        return DocstringContent(examples=[], related=[])

    lines = [line.strip() for line in docstring.splitlines() if line.strip()]
    examples: list[str] = []
    related: list[str] = []
    current_section: str | None = None

    for line in lines:
        lower = line.lower()
        section = _is_section_header(line, lower)

        if section == "examples":
            current_section = "examples"
            continue
        if section == "related":
            current_section = "related"
            continue
        if section == "other":
            current_section = None
            continue

        if current_section == "examples":
            examples.append(_parse_example_line(line))
        elif current_section == "related":
            related.extend(_parse_related_lines(line))

    return DocstringContent(examples=examples, related=related)


def extract_examples(docstring: str | None) -> list[str]:
    """Extract examples from a docstring (legacy function).

    Args:
        docstring: The function docstring to parse

    Returns:
        List of example strings
    """
    return extract_docstring_content(docstring).examples


def extract_related(docstring: str | None) -> list[str]:
    """Extract related commands from a docstring.

    Args:
        docstring: The function docstring to parse

    Returns:
        List of related command strings
    """
    return extract_docstring_content(docstring).related
