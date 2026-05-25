"""Certificate loading and JSON-schema validation helpers."""

import json
from pathlib import Path

from jsonschema import validate


def load_certificate(path):
    """Load a certificate JSON file from disk."""
    with Path(path).open("r", encoding="utf-8-sig") as handle:
        return json.load(handle)


def validate_certificate(cert, schema_path):
    """Validate a certificate dictionary against a JSON schema file."""
    with Path(schema_path).open("r", encoding="utf-8-sig") as handle:
        schema = json.load(handle)
    validate(instance=cert, schema=schema)
    return True