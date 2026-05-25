"""Certificate loading, JSON-schema validation, summaries, and CLI."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from jsonschema import ValidationError, validate

from .arithmetic_certificate import verify_add_mod_2n_transcript
from .gate_counts import load_gate_list, verify_circuit_against_certificate
from .modular_inversion import verify_modinv_transcript
from .toy_certificate import verify_toy_transcript
from .toy_functions import TOY_ARITHMETIC_FUNCTIONS

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
    public_circuit = cert.get("public_circuit", {})
    return {
        "certificate_id": cert.get("certificate_id"),
        "arithmetic_function": cert.get("arithmetic_function"),
        "modulus": params.get("modulus"),
        "bit_length": params.get("bit_length"),
        "test_count": tests.get("test_count"),
        "exhaustive": tests.get("exhaustive"),
        "proof_artifact": proof.get("type"),
        "public_circuit": public_circuit.get("circuit_id"),
    }


def verify_certificate(cert: dict, circuit_path: str | Path | None = None) -> tuple[bool, list[str]]:
    """Run semantic certificate checks beyond JSON-schema validation."""
    ok = True
    messages: list[str] = []
    arithmetic_function = cert.get("arithmetic_function")
    circuit = None

    if circuit_path is not None:
        circuit = load_gate_list(circuit_path)
        circuit_ok, circuit_messages = verify_circuit_against_certificate(cert, circuit)
        ok = ok and circuit_ok
        messages.extend(circuit_messages)

    if arithmetic_function == "modular_inversion":
        transcript_ok, transcript_messages = verify_modinv_transcript(cert)
        ok = ok and transcript_ok
        messages.extend(transcript_messages)
    elif arithmetic_function == "toy_add_mod_2n":
        if circuit is None:
            ok = False
            messages.append("toy_add_mod_2n certificates require --circuit")
        else:
            transcript_ok, transcript_messages = verify_add_mod_2n_transcript(cert, circuit)
            ok = ok and transcript_ok
            messages.extend(transcript_messages)
    elif arithmetic_function in TOY_ARITHMETIC_FUNCTIONS:
        if circuit is None:
            ok = False
            messages.append("toy arithmetic certificates require --circuit")
        else:
            transcript_ok, transcript_messages = verify_toy_transcript(cert, circuit)
            ok = ok and transcript_ok
            messages.extend(transcript_messages)
    else:
        ok = False
        messages.append(f"unsupported arithmetic_function: {arithmetic_function}")

    return ok, messages


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
    parser.add_argument("--circuit", help="Optional public gate-list circuit JSON to verify against resource counts")
    args = parser.parse_args(argv)

    try:
        cert = load_certificate(args.certificate)
        validate_certificate(cert, args.schema)
        ok, messages = verify_certificate(cert, args.circuit)
        _print_summary(certificate_summary(cert), messages)
        return 0 if ok else 1
    except Exception as exc:  # noqa: BLE001 - CLI should print a concise failure.
        print(f"certificate verification failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())