"""Certificate loading, JSON-schema validation, summaries, and CLI."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from jsonschema import ValidationError, validate

from .modular_inversion import verify_modinv_transcript

DEFAULT_SCHEMA = Path("schema/reversible_arithmetic_certificate.schema.json")


def load_certificate(path: str | Path) -> dict:
    """Load a certificate JSON file from disk."""
    with Path(path).open("r", encoding="utf-8-sig") as handle:
        return json.load(handle)


def load_schema(path: str | Path) -> dict:
    """Load a JSON schema file from disk."""
    with Path(path).open("r", encoding="utf-8-sig") as handle:
        return json.load(handle)


def validate_certificate(cert: dict, schema_path: str | Path = DEFAULT_SCHEMA) -> None:
    """Validate ``cert`` against the certificate schema.

    Raises ``ValueError`` with a compact path-aware message when validation fails.
    """
    try:
        validate(instance=cert, schema=load_schema(schema_path))
    except ValidationError as exc:
        path = ".".join(str(part) for part in exc.absolute_path) or "<root>"
        raise ValueError(f"certificate schema validation failed at {path}: {exc.message}") from exc


def certificate_summary(cert: dict) -> dict:
    """Return a compact summary of the certificate."""
    params = cert.get("arithmetic_parameters", {})
    tests = cert.get("test_generation", {})
    proof = cert.get("proof_artifact", {})
    return {
        "certificate_id": cert.get("certificate_id"),
        "arithmetic_function": cert.get("arithmetic_function"),
        "modulus": params.get("modulus"),
        "bit_length": params.get("bit_length"),
        "test_count": tests.get("test_count"),
        "exhaustive": tests.get("exhaustive"),
        "proof_artifact": proof.get("type"),
    }


def _print_summary(summary: dict, messages: list[str]) -> None:
    print("Certificate verification summary")
    for key, value in summary.items():
        print(f"  {key}: {value}")
    print("Messages:")
    for message in messages:
        print(f"  - {message}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate and verify a reversible arithmetic certificate.")
    parser.add_argument("certificate", help="Path to certificate JSON")
    parser.add_argument("--schema", default=str(DEFAULT_SCHEMA), help="Path to certificate JSON schema")
    args = parser.parse_args(argv)

    try:
        cert = load_certificate(args.certificate)
        validate_certificate(cert, args.schema)
        if cert.get("arithmetic_function") == "modular_inversion":
            ok, messages = verify_modinv_transcript(cert)
        else:
            ok, messages = False, [f"unsupported arithmetic_function: {cert.get('arithmetic_function')}"]
        _print_summary(certificate_summary(cert), messages)
        return 0 if ok else 1
    except Exception as exc:  # noqa: BLE001 - CLI should print a concise failure.
        print(f"certificate verification failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())