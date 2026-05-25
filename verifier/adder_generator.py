"""Generators for small public reversible arithmetic toy circuits."""

from __future__ import annotations


def generate_add_mod_2n_circuit(n: int = 2) -> dict:
    """Generate a toy circuit for ``(a,b) -> (a,b+a mod 2^n)``.

    The current implementation supports ``n=2`` with register layout
    ``[a0, a1, b0, b1]`` in little-endian order. The circuit is:
    Toffoli(a0,b0 -> b1), CNOT(a1 -> b1), CNOT(a0 -> b0).
    """
    if n != 2:
        raise ValueError("generate_add_mod_2n_circuit currently supports n=2 only")
    return {
        "circuit_id": "toy-add-mod-2n-n2",
        "circuit_version": "0.1.0",
        "arithmetic_function": "toy_add_mod_2n",
        "description": "Toy reversible circuit for (a,b)->(a,b+a mod 2^n), currently n=2.",
        "gate_basis": ["CNOT", "TOFFOLI"],
        "qubit_count": 4,
        "registers": {
            "a": [0, 1],
            "b": [2, 3],
            "work": [],
            "endianness": "little",
        },
        "gates": [
            {
                "type": "TOFFOLI",
                "controls": [0, 2],
                "targets": [3],
                "comment": "Add carry from a0+b0 into b1.",
            },
            {
                "type": "CNOT",
                "controls": [1],
                "targets": [3],
                "comment": "Add a1 into b1.",
            },
            {
                "type": "CNOT",
                "controls": [0],
                "targets": [2],
                "comment": "Add a0 into b0.",
            },
        ],
    }