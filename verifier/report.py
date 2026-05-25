"""Markdown report helpers."""

from __future__ import annotations

from pathlib import Path


def markdown_table(headers, rows) -> str:
    """Render a simple GitHub-flavored Markdown table."""
    header_line = "| " + " | ".join(str(header) for header in headers) + " |"
    rule_line = "| " + " | ".join("---" for _ in headers) + " |"
    body = ["| " + " | ".join(str(cell) for cell in row) + " |" for row in rows]
    return "\n".join([header_line, rule_line, *body]) + "\n"


def write_text(path, text: str) -> None:
    """Write text to disk, creating parent directories if needed."""
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text, encoding="utf-8")