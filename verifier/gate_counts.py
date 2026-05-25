"""Placeholder-safe gate-count metadata helpers."""

from collections import Counter


def count_gate_basis(gates):
    """Count gate dictionaries by their type field."""
    return dict(Counter(gate.get("type", "UNKNOWN") for gate in gates))


def summarize_gate_counts(gates):
    """Summarize a toy gate list."""
    by_type = count_gate_basis(gates)
    return {
        "total_gates": len(gates),
        "by_type": by_type,
    }
