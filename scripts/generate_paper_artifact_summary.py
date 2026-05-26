"""Generate paper-ready artifact summary tables from verifier outputs."""

from __future__ import annotations

import csv
from pathlib import Path

from verifier.report import markdown_table, write_text

CERTIFICATE_CSV = Path("outputs/certificate_report.csv")
TOY_CIRCUIT_CSV = Path("outputs/toy_circuit_report.csv")
SUMMARY_MD = Path("outputs/paper_artifact_summary.md")
SUMMARY_TEX = Path("outputs/paper_artifact_summary.tex")

DISPLAY_NAMES = {
    "inv-8bit-toy-transcript": "inv_8bit",
    "inv-16bit-toy-transcript": "inv_16bit",
    "toy_cnot_copy-truth-table-cert": "CNOT-copy",
    "toy_toffoli_and-truth-table-cert": "Toffoli-AND",
    "toy_swap-truth-table-cert": "SWAP",
    "toy_add_mod_2n_n2-truth-table-cert": "add-mod-4",
}

FUNCTION_NAMES = {
    "modular_inversion": "modular inversion",
    "toy_cnot_copy": "CNOT copy",
    "toy_toffoli_and": "Toffoli AND",
    "toy_swap": "SWAP",
    "toy_add_mod_2n": "add mod 4",
}


def read_csv_dicts(path: Path) -> list[dict]:
    with path.open("r", newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def display_name(row: dict) -> str:
    cert_id = row["certificate_id"]
    if cert_id == "inv-8bit-toy-transcript" and row.get("public_circuit_attached") == "true":
        return "inv_8bit+circuit"
    return DISPLAY_NAMES.get(cert_id, cert_id)


def latex_escape(value) -> str:
    text = str(value)
    replacements = {
        "\\": r"\textbackslash{}",
        "_": r"\_",
        "%": r"\%",
        "&": r"\&",
        "#": r"\#",
        "$": r"\$",
        "{": r"\{",
        "}": r"\}",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text


def transcript_status(row: dict) -> str:
    return "hash verified" if row["transcript_hash_verified"] == "true" else "hash failed"


def circuit_status(row: dict) -> str:
    if row["public_circuit_attached"] != "true":
        return "not attached"
    if row["circuit_hash_verified"] == "true" and row["resource_counts_verified"] == "true":
        return "hash/counts verified"
    return "mismatch"


def modular_rows(certificate_rows: list[dict]) -> list[dict]:
    return [row for row in certificate_rows if row["arithmetic_function"] == "modular_inversion"]


def toy_rows(certificate_rows: list[dict]) -> list[dict]:
    return [row for row in certificate_rows if row["arithmetic_function"] != "modular_inversion"]


def markdown_certificate_rows(rows: list[dict]) -> list[list[str]]:
    return [
        [
            display_name(row),
            FUNCTION_NAMES.get(row["arithmetic_function"], row["arithmetic_function"]),
            row["bit_length"],
            row["test_count"],
            transcript_status(row),
            circuit_status(row),
            row["status"],
        ]
        for row in rows
    ]


def markdown_resource_rows(certificate_rows: list[dict], circuit_rows: list[dict]) -> list[list[str]]:
    resource_fields = [
        ["transcript_hash_verified", "certificate report", "hash verified"],
        ["public_circuit_attached", "certificate report", "attached / not attached"],
        ["circuit_hash_verified", "certificate report", "hash verified / not applicable"],
        ["resource_counts_verified", "certificate report", "counts verified / not applicable"],
        ["total_gates", "toy circuit report", "serial gate count"],
        ["serial_depth", "toy circuit report", "serial gate-count depth; not architecture-aware"],
    ]
    # Touch both inputs so stale/empty reports fail naturally in callers/tests.
    if not certificate_rows or not circuit_rows:
        resource_fields.append(["warning", "reports", "one or more source reports were empty"])
    return resource_fields


def tex_certificate_rows(rows: list[dict]) -> list[str]:
    tex_rows = []
    for row in rows:
        values = [
            display_name(row),
            FUNCTION_NAMES.get(row["arithmetic_function"], row["arithmetic_function"]),
            row["bit_length"],
            row["test_count"],
            transcript_status(row),
            circuit_status(row),
            row["status"],
        ]
        tex_rows.append(" & ".join(latex_escape(value) for value in values) + r" \\")
    return tex_rows


def tex_resource_rows() -> list[str]:
    rows = [
        ["Transcript hash", "SHA-256 over canonical transcript JSON", "hash verified"],
        ["Public circuit", "canonical gate-list hash", "hash/counts verified"],
        ["Resource counts", "logical qubits, CNOT, Toffoli, serial_depth", "hash/counts verified"],
        ["Unattached certificates", "transcript-only examples", "not attached"],
    ]
    return [" & ".join(latex_escape(value) for value in row) + r" \\" for row in rows]


def generate_markdown(certificate_rows: list[dict], circuit_rows: list[dict]) -> str:
    headers = ["Artifact", "Function", "Bits", "Tests", "Transcript", "Circuit/resources", "Status"]
    resource_headers = ["Field", "Source", "Paper wording"]
    text = "# Paper Artifact Summary\n\n"
    text += "Generated from `outputs/certificate_report.csv` and `outputs/toy_circuit_report.csv`.\n\n"
    text += "## Modular inversion certificates\n\n"
    text += markdown_table(headers, markdown_certificate_rows(modular_rows(certificate_rows)))
    text += "\n## Toy exhaustive certificates\n\n"
    text += markdown_table(headers, markdown_certificate_rows(toy_rows(certificate_rows)))
    text += "\n## Resource-count verification fields\n\n"
    text += markdown_table(resource_headers, markdown_resource_rows(certificate_rows, circuit_rows))
    text += "\n## Notes on limitations\n\n"
    text += "These artifacts certify public toy transcripts, public toy gate-list hashes, and resource-count metadata. "
    text += "They do not implement a quantum attack, recover private keys, verify withheld circuits, or implement a production modular-inversion circuit.\n"
    return text


def generate_tex(certificate_rows: list[dict]) -> str:
    lines = [
        "% Generated by scripts/generate_paper_artifact_summary.py",
        "% Table-row snippets only; wrap these rows in paper-side table environments.",
        "",
        "% Modular inversion certificate rows",
        *tex_certificate_rows(modular_rows(certificate_rows)),
        "",
        "% Toy exhaustive certificate rows",
        *tex_certificate_rows(toy_rows(certificate_rows)),
        "",
        "% Resource field rows",
        *tex_resource_rows(),
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    certificate_rows = read_csv_dicts(CERTIFICATE_CSV)
    circuit_rows = read_csv_dicts(TOY_CIRCUIT_CSV)
    write_text(SUMMARY_MD, generate_markdown(certificate_rows, circuit_rows))
    write_text(SUMMARY_TEX, generate_tex(certificate_rows))
    print(f"wrote {SUMMARY_MD}")
    print(f"wrote {SUMMARY_TEX}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())