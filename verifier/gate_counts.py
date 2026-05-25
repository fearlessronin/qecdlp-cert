"""Small helpers for toy gate-count metadata."""

from __future__ import annotations


def count_gate_basis(gates: list[dict]) -> dict[str, int]:
    """Count gate dictionaries by their ``type`` field."""
    counts: dict[str, int] = {}
    for gate in gates or []:
        gate_type = gate.get("type") if isinstance(gate, dict) else None
        if gate_type is None:
            continue
        counts[str(gate_type)] = counts.get(str(gate_type), 0) + 1
    return counts


def summarize_gate_counts(gates: list[dict]) -> dict:
    """Return total gate count and basis counts for a toy gate list."""
    basis_counts = count_gate_basis(gates or [])
    return {
        "total_gates": sum(basis_counts.values()),
        "basis_counts": basis_counts,
    }