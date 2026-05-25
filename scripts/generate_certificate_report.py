"""Generate reproducible verifier reports for example certificates."""

from __future__ import annotations

from pathlib import Path

from verifier.certificate import certificate_summary, load_certificate, validate_certificate
from verifier.gate_counts import load_gate_list, verify_circuit_against_certificate
from verifier.modular_inversion import verify_modinv_transcript
from verifier.report import status_to_markdown_table, write_csv, write_text

REPORT_HEADERS = [
    "certificate_id",
    "arithmetic_function",
    "modulus",
    "bit_length",
    "test_count",
    "exhaustive",
    "transcript_hash_verified",
    "public_circuit_attached",
    "circuit_hash_verified",
    "resource_counts_verified",
    "proof_artifact_type",
    "status",
]

EXAMPLES = [
    (Path("examples/inv_8bit.json"), None),
    (Path("examples/inv_16bit.json"), None),
    (Path("examples/inv_8bit_with_circuit.json"), Path("circuits/toy_modinv_stub_8bit.json")),
]


def _message_present(messages: list[str], expected: str) -> bool:
    return any(expected in message for message in messages)


def report_row(cert_path: Path, circuit_path: Path | None = None) -> dict:
    """Build one report row for a certificate and optional public circuit."""
    cert = load_certificate(cert_path)
    schema_ok = True
    schema_message = ""
    try:
        validate_certificate(cert)
    except Exception as exc:  # noqa: BLE001 - report should capture failures.
        schema_ok = False
        schema_message = str(exc)

    transcript_ok, transcript_messages = verify_modinv_transcript(cert)
    public_circuit_attached = bool(cert.get("public_circuit"))
    circuit_hash_verified = "not_applicable"
    resource_counts_verified = "not_applicable"
    circuit_ok = True
    circuit_messages: list[str] = []

    if circuit_path is not None:
        circuit = load_gate_list(circuit_path)
        circuit_ok, circuit_messages = verify_circuit_against_certificate(cert, circuit)
        circuit_hash_verified = str(_message_present(circuit_messages, "public circuit hash and resource counts verified")).lower()
        resource_counts_verified = str(_message_present(circuit_messages, "public circuit hash and resource counts verified")).lower()
    elif public_circuit_attached:
        circuit_hash_verified = "not_checked"
        resource_counts_verified = "not_checked"

    summary = certificate_summary(cert)
    status = "pass" if schema_ok and transcript_ok and circuit_ok else "fail"
    if not schema_ok:
        transcript_messages.append(schema_message)

    return {
        "certificate_id": summary["certificate_id"],
        "arithmetic_function": summary["arithmetic_function"],
        "modulus": summary["modulus"],
        "bit_length": summary["bit_length"],
        "test_count": summary["test_count"],
        "exhaustive": str(summary["exhaustive"]).lower(),
        "transcript_hash_verified": str(_message_present(transcript_messages, "transcript hash verified")).lower(),
        "public_circuit_attached": str(public_circuit_attached).lower(),
        "circuit_hash_verified": circuit_hash_verified,
        "resource_counts_verified": resource_counts_verified,
        "proof_artifact_type": summary["proof_artifact"],
        "status": status,
    }


def generate_report(rows: list[dict], md_path: Path, csv_path: Path) -> None:
    """Write Markdown and CSV certificate report outputs."""
    markdown = "# Certificate Verification Report\n\n"
    markdown += "This report is generated from the public toy certificates in `examples/`. "
    markdown += "It summarizes schema validation, modular-inversion transcript checks, transcript hashes, and optional public toy gate-list verification.\n\n"
    markdown += status_to_markdown_table(rows)
    write_text(md_path, markdown)
    write_csv(csv_path, REPORT_HEADERS, rows)


def main() -> int:
    rows = [report_row(cert_path, circuit_path) for cert_path, circuit_path in EXAMPLES]
    generate_report(rows, Path("outputs/certificate_report.md"), Path("outputs/certificate_report.csv"))
    print("wrote outputs/certificate_report.md")
    print("wrote outputs/certificate_report.csv")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())