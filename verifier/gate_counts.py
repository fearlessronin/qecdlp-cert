"""Helpers for public toy gate-list resource-count metadata."""

from __future__ import annotations

import json
from pathlib import Path

from .hash_tests import canonical_json, sha256_hex


def load_gate_list(path: str | Path) -> dict:
    """Load a public gate-list JSON file."""
    with Path(path).open("r", encoding="utf-8-sig") as handle:
        return json.load(handle)


def circuit_hash_from_gate_list(circuit: dict) -> str:
    """Return SHA-256 of the canonical JSON gate-list object."""
    return sha256_hex(canonical_json(circuit))


def count_gate_basis(gates: list[dict]) -> dict[str, int]:
    """Count gate dictionaries by their ``type`` field."""
    counts: dict[str, int] = {}
    for gate in gates or []:
        gate_type = gate.get("type") if isinstance(gate, dict) else None
        if gate_type is None:
            continue
        gate_type = str(gate_type).upper()
        counts[gate_type] = counts.get(gate_type, 0) + 1
    return counts


def summarize_gate_counts(circuit: dict | list[dict]) -> dict:
    """Summarize resource metadata for a public toy gate list.

    The current depth convention is serial depth, so depth equals total gate count.
    """
    if isinstance(circuit, list):
        gates = circuit
        qubit_count = 0
    else:
        gates = circuit.get("gates", []) or []
        qubit_count = int(circuit.get("qubit_count", 0) or 0)
    basis_counts = count_gate_basis(gates)
    total_gates = sum(basis_counts.values())
    return {
        "logical_qubits": qubit_count,
        "gate_counts_by_type": basis_counts,
        "toffoli_count": basis_counts.get("TOFFOLI", 0),
        "cnot_count": basis_counts.get("CNOT", 0),
        "swap_count": basis_counts.get("SWAP", 0),
        "not_count": basis_counts.get("NOT", 0),
        "total_gates": total_gates,
        "depth": total_gates,
    }


def validate_gate_indices(circuit: dict) -> list[str]:
    """Return errors for any gate referencing qubits outside ``0..qubit_count-1``."""
    errors: list[str] = []
    qubit_count = circuit.get("qubit_count")
    if not isinstance(qubit_count, int) or qubit_count < 0:
        return ["qubit_count must be a nonnegative integer"]

    for gate_index, gate in enumerate(circuit.get("gates", []) or []):
        if not isinstance(gate, dict):
            errors.append(f"gate {gate_index}: gate must be an object")
            continue
        for field in ("controls", "targets"):
            values = gate.get(field, []) or []
            if not isinstance(values, list):
                errors.append(f"gate {gate_index}: {field} must be a list")
                continue
            for qubit in values:
                if not isinstance(qubit, int):
                    errors.append(f"gate {gate_index}: {field} contains non-integer qubit {qubit!r}")
                elif qubit < 0 or qubit >= qubit_count:
                    errors.append(f"gate {gate_index}: {field} qubit {qubit} outside 0..{qubit_count - 1}")
    return errors


def verify_circuit_against_certificate(cert: dict, circuit: dict) -> tuple[bool, list[str]]:
    """Verify public circuit hash and resource counts against a certificate."""
    messages: list[str] = []
    errors = validate_gate_indices(circuit)
    if errors:
        messages.extend(errors)

    public_circuit = cert.get("public_circuit")
    computed_hash = circuit_hash_from_gate_list(circuit)
    if public_circuit:
        if public_circuit.get("circuit_hash") != computed_hash:
            messages.append("public_circuit.circuit_hash does not match supplied gate list")
        if public_circuit.get("circuit_id") != circuit.get("circuit_id"):
            messages.append("public_circuit.circuit_id does not match supplied gate list")
    else:
        messages.append("certificate has no public_circuit metadata; checking resource counts only")

    if cert.get("circuit_hash") != computed_hash:
        messages.append("certificate circuit_hash does not match supplied gate list")

    summary = summarize_gate_counts(circuit)
    resource_counts = cert.get("resource_counts", {})
    comparisons = {
        "logical_qubits": summary["logical_qubits"],
        "toffoli_count": summary["toffoli_count"],
        "cnot_count": summary["cnot_count"],
        "depth": summary["depth"],
    }
    for key, expected in comparisons.items():
        if resource_counts.get(key) != expected:
            messages.append(f"resource_counts.{key}={resource_counts.get(key)!r} does not match gate-list value {expected!r}")

    ok = not messages or messages == ["certificate has no public_circuit metadata; checking resource counts only"]
    if ok:
        messages.insert(0, "public circuit hash and resource counts verified")
    return ok, messages