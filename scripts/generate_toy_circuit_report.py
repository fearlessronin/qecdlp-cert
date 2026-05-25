"""Generate a report for public toy reversible circuit simulation."""

from __future__ import annotations

from pathlib import Path

from verifier.gate_counts import circuit_hash_from_gate_list, load_gate_list, summarize_gate_counts
from verifier.report import status_to_markdown_table, write_csv, write_text
from verifier.simulate import truth_table

CIRCUIT_PATHS = [
    Path("circuits/toy_cnot_copy.json"),
    Path("circuits/toy_toffoli_and.json"),
    Path("circuits/toy_swap.json"),
]

REPORT_HEADERS = [
    "circuit_id",
    "qubit_count",
    "total_inputs",
    "total_gates",
    "not_count",
    "cnot_count",
    "toffoli_count",
    "swap_count",
    "depth",
    "circuit_hash",
]


def report_row(path: Path) -> dict:
    circuit = load_gate_list(path)
    counts = summarize_gate_counts(circuit)
    table = truth_table(circuit)
    return {
        "circuit_id": circuit.get("circuit_id"),
        "qubit_count": circuit.get("qubit_count"),
        "total_inputs": len(table),
        "total_gates": counts["total_gates"],
        "not_count": counts["not_count"],
        "cnot_count": counts["cnot_count"],
        "toffoli_count": counts["toffoli_count"],
        "swap_count": counts["swap_count"],
        "depth": counts["depth"],
        "circuit_hash": circuit_hash_from_gate_list(circuit),
    }


def generate_report(rows: list[dict], md_path: Path, csv_path: Path) -> None:
    markdown = "# Toy Reversible Circuit Simulation Report\n\n"
    markdown += "This report summarizes generated public toy reversible Boolean circuits. "
    markdown += "Truth tables are computed by classical simulation on computational-basis bit inputs only.\n\n"
    markdown += status_to_markdown_table(rows)
    write_text(md_path, markdown)
    write_csv(csv_path, REPORT_HEADERS, rows)


def main() -> int:
    rows = [report_row(path) for path in CIRCUIT_PATHS]
    generate_report(rows, Path("outputs/toy_circuit_report.md"), Path("outputs/toy_circuit_report.csv"))
    print("wrote outputs/toy_circuit_report.md")
    print("wrote outputs/toy_circuit_report.csv")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())