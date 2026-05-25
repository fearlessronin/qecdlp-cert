"""Generators for small public reversible toy circuits."""

from __future__ import annotations


def generate_cnot_copy_circuit() -> dict:
    """Return a CNOT copy/xor toy circuit mapping ``(x,y)`` to ``(x,y xor x)``."""
    return {
        "circuit_id": "toy-cnot-copy",
        "circuit_version": "0.1.0",
        "description": "Toy reversible CNOT copy/xor circuit: (x, y) -> (x, y xor x).",
        "gate_basis": ["CNOT"],
        "qubit_count": 2,
        "gates": [
            {"type": "CNOT", "controls": [0], "targets": [1]},
        ],
    }


def generate_toffoli_and_circuit() -> dict:
    """Return a Toffoli AND toy circuit mapping ``(x,y,z)`` to ``(x,y,z xor x*y)``."""
    return {
        "circuit_id": "toy-toffoli-and",
        "circuit_version": "0.1.0",
        "description": "Toy reversible Toffoli AND circuit: (x, y, z) -> (x, y, z xor (x and y)).",
        "gate_basis": ["TOFFOLI"],
        "qubit_count": 3,
        "gates": [
            {"type": "TOFFOLI", "controls": [0, 1], "targets": [2]},
        ],
    }


def generate_swap_circuit() -> dict:
    """Return a toy SWAP circuit mapping ``(x,y)`` to ``(y,x)``."""
    return {
        "circuit_id": "toy-swap",
        "circuit_version": "0.1.0",
        "description": "Toy reversible SWAP circuit: (x, y) -> (y, x).",
        "gate_basis": ["SWAP"],
        "qubit_count": 2,
        "gates": [
            {"type": "SWAP", "targets": [0, 1]},
        ],
    }