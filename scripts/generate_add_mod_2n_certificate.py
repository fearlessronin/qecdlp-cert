"""Generate a certificate for a toy reversible add-mod-2^n circuit."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from verifier.arithmetic_certificate import expected_add_mod_2n_tests
from verifier.gate_counts import circuit_hash_from_gate_list, load_gate_list, summarize_gate_counts
from verifier.hash_tests import transcript_hash


def build_add_mod_2n_certificate(circuit: dict, circuit_path: Path) -> dict:
    """Build a toy add-mod-2^n certificate from a public gate-list circuit."""
    arithmetic_function = circuit.get("arithmetic_function", "toy_add_mod_2n")
    if arithmetic_function != "toy_add_mod_2n":
        raise ValueError("circuit arithmetic_function must be toy_add_mod_2n")
    registers = circuit.get("registers", {})
    n = len(registers.get("a", []))
    if n <= 0:
        raise ValueError("circuit registers.a must define n")

    circuit_hash = circuit_hash_from_gate_list(circuit)
    summary = summarize_gate_counts(circuit)
    tests = expected_add_mod_2n_tests(circuit, n)
    return {
        "certificate_version": "0.1.0",
        "certificate_id": f"toy_add_mod_2n_n{n}-truth-table-cert",
        "circuit_hash": circuit_hash,
        "public_circuit": {
            "circuit_file": str(circuit_path).replace("\\", "/"),
            "circuit_hash": circuit_hash,
            "circuit_id": circuit.get("circuit_id"),
        },
        "gate_basis": circuit.get("gate_basis", []),
        "arithmetic_function": "toy_add_mod_2n",
        "arithmetic_parameters": {
            "n": n,
            "modulus": 2**n,
            "bit_length": n,
            "field": "Z/(2^n)",
        },
        "resource_counts": {
            "logical_qubits": summary["logical_qubits"],
            "ancilla_qubits": len(registers.get("work", [])),
            "toffoli_count": summary["toffoli_count"],
            "cnot_count": summary["cnot_count"],
            "serial_depth": summary["serial_depth"],
            "depth": summary["depth"],
            "source": "public toy add-mod-2^n gate-list with exhaustive classical truth-table simulation",
        },
        "io_spec": {
            "domain": "boolean_bitstrings_clean_work",
            "input_register": "a,b,work",
            "output_register": "a,b+a mod 2^n,work",
            "relation": "toy_add_mod_2n",
        },
        "test_generation": {
            "method": "exhaustive_truth_table",
            "label": "toy_add_mod_2n",
            "test_count": len(tests),
            "exhaustive": True,
        },
        "correctness_transcript": {"tests": tests},
        "transcript_hash": transcript_hash(tests),
        "proof_artifact": {"type": "none"},
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate a toy add-mod-2^n certificate.")
    parser.add_argument("--circuit", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args(argv)

    circuit_path = Path(args.circuit)
    circuit = load_gate_list(circuit_path)
    cert = build_add_mod_2n_certificate(circuit, circuit_path)
    output = Path(args.out)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(cert, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"wrote {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())