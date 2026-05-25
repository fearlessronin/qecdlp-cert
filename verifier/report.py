"""Markdown and CSV report helpers."""

from __future__ import annotations

import csv
from pathlib import Path


def markdown_table(headers, rows) -> str:
    """Render a simple GitHub-flavored Markdown table."""
    header_line = "| " + " | ".join(str(header) for header in headers) + " |"
    rule_line = "| " + " | ".join("---" for _ in headers) + " |"
    body = ["| " + " | ".join(str(cell) for cell in row) + " |" for row in rows]
    return "\n".join([header_line, rule_line, *body]) + "\n"


def status_to_markdown_table(rows: list[dict]) -> str:
    """Render report status dictionaries as a Markdown table."""
    if not rows:
        return "| status |\n| --- |\n| no rows |\n"
    headers = list(rows[0].keys())
    table_rows = [[row.get(header, "") for header in headers] for row in rows]
    return markdown_table(headers, table_rows)


def write_csv(path, headers, rows) -> None:
    """Write dictionaries or row sequences to a CSV file."""
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(headers)
        for row in rows:
            if isinstance(row, dict):
                writer.writerow([row.get(header, "") for header in headers])
            else:
                writer.writerow(row)


def write_text(path, text: str) -> None:
    """Write text to disk, creating parent directories if needed."""
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text, encoding="utf-8")