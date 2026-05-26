"""Generate certificates for public simulated toy reversible circuits."""

from __future__ import annotations

import json
from pathlib import Path

from verifier.gate_counts import circuit_hash_from_gate_list, load_gate_list, summarize_gate_counts
from verifier.hash_tests import transcript_hash
from verifier.toy_certificate import expected_toy_tests

TOY_CERTIFICATES = [
    ("toy_cnot_copy", Path("circuits/toy_cnot_copy.json"), Path("examples/toy_cnot_copy_cert.json")),
    ("toy_toffoli_and", Path("circuits/toy_toffoli_and.json"), Path("examples/toy_toffoli_and_cert.json")),
    ("toy_swap", Path("circuits/toy_swap.json"), Path("examples/toy_swap_cert.json")),
]


def build_toy_certificate(arithmetic_function: str, circuit_path: Path) -> dict:
    """Build a certificate for a public toy reversible Boolean circuit."""
    circuit = load_gate_list(circuit_path)
    circuit_hash = circuit_hash_from_gate_list(circuit)
    summary = summarize_gate_counts(circuit)
    tests = expected_toy_tests(circuit, arithmetic_function)
    qubit_count = int(circuit["qubit_count"])
    return {
        "certificate_version": "0.1.0",
        "certificate_id": f"{arithmetic_function}-truth-table-cert",
        "circuit_hash": circuit_hash,
        "public_circuit": {
            "circuit_file": str(circuit_path).replace("\\", "/"),
            "circuit_hash": circuit_hash,
            "circuit_id": circuit.get("circuit_id"),
        },
        "gate_basis": circuit.get("gate_basis", []),
        "arithmetic_function": arithmetic_function,
        "arithmetic_parameters": {
            "modulus": 2,
            "bit_length": qubit_count,
            "field": "boolean_bits",
        },
        "resource_counts": {
            "logical_qubits": summary["logical_qubits"],
            "ancilla_qubits": 0,
            "toffoli_count": summary["toffoli_count"],
            "cnot_count": summary["cnot_count"],
            "serial_depth": summary["serial_depth"],
            "depth": summary["depth"],
            "source": "public toy gate-list circuit with exhaustive classical truth-table simulation",
        },
        "io_spec": {
            "domain": "boolean_bitstrings",
            "input_register": "input_bits",
            "output_register": "output_bits",
            "relation": arithmetic_function,
        },
        "test_generation": {
            "method": "exhaustive_truth_table",
            "label": arithmetic_function,
            "test_count": len(tests),
            "exhaustive": True,
        },
        "correctness_transcript": {
            "tests": tests,
        },
        "transcript_hash": transcript_hash(tests),
        "proof_artifact": {"type": "none"},
    }


def main() -> int:
    for arithmetic_function, circuit_path, output_path in TOY_CERTIFICATES:
        cert = build_toy_certificate(arithmetic_function, circuit_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(cert, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(f"wrote {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())