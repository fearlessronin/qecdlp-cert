"""Small report helpers for markdown outputs."""

from pathlib import Path


def markdown_table(headers, rows):
    """Render a markdown table from headers and row iterables."""
    lines = ["| " + " | ".join(headers) + " |"]
    lines.append("| " + " | ".join(["---"] * len(headers)) + " |")
    for row in rows:
        lines.append("| " + " | ".join(str(item) for item in row) + " |")
    return "\n".join(lines)


def write_text(path, text):
    """Write text to path, creating parent directories if needed."""
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(text, encoding="utf-8")
