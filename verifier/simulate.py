"""Classical simulator for small public reversible Boolean gate lists."""

from __future__ import annotations


def _validate_bit(value: int) -> None:
    if value not in (0, 1):
        raise ValueError(f"bit values must be 0 or 1, got {value!r}")


def _validate_index(state: list[int], index: int) -> None:
    if not isinstance(index, int):
        raise ValueError(f"qubit index must be an integer, got {index!r}")
    if index < 0 or index >= len(state):
        raise ValueError(f"qubit index {index} outside 0..{len(state) - 1}")


def _one_target(gate: dict) -> int:
    targets = gate.get("targets")
    if not isinstance(targets, list) or len(targets) != 1:
        raise ValueError(f"{gate.get('type')} gate requires exactly one target")
    return targets[0]


def _two_targets(gate: dict) -> tuple[int, int]:
    targets = gate.get("targets")
    if not isinstance(targets, list) or len(targets) != 2:
        raise ValueError(f"{gate.get('type')} gate requires exactly two targets")
    return targets[0], targets[1]


def _controls(gate: dict, count: int) -> list[int]:
    controls = gate.get("controls")
    if not isinstance(controls, list) or len(controls) != count:
        raise ValueError(f"{gate.get('type')} gate requires exactly {count} controls")
    return controls


def apply_not(state: list[int], target: int) -> None:
    """Apply a NOT gate in place."""
    _validate_index(state, target)
    state[target] ^= 1


def apply_cnot(state: list[int], control: int, target: int) -> None:
    """Apply a CNOT gate in place."""
    _validate_index(state, control)
    _validate_index(state, target)
    if state[control] == 1:
        state[target] ^= 1


def apply_toffoli(state: list[int], control1: int, control2: int, target: int) -> None:
    """Apply a Toffoli gate in place."""
    _validate_index(state, control1)
    _validate_index(state, control2)
    _validate_index(state, target)
    if state[control1] == 1 and state[control2] == 1:
        state[target] ^= 1


def apply_swap(state: list[int], q1: int, q2: int) -> None:
    """Apply a SWAP gate in place."""
    _validate_index(state, q1)
    _validate_index(state, q2)
    state[q1], state[q2] = state[q2], state[q1]


def _apply_gate(state: list[int], gate: dict) -> None:
    gate_type = str(gate.get("type", "")).upper()
    if gate_type == "NOT":
        apply_not(state, _one_target(gate))
    elif gate_type == "CNOT":
        control = _controls(gate, 1)[0]
        apply_cnot(state, control, _one_target(gate))
    elif gate_type == "TOFFOLI":
        control1, control2 = _controls(gate, 2)
        apply_toffoli(state, control1, control2, _one_target(gate))
    elif gate_type == "SWAP":
        q1, q2 = _two_targets(gate)
        apply_swap(state, q1, q2)
    else:
        raise ValueError(f"unsupported gate type: {gate.get('type')!r}")


def simulate_gate_list(circuit: dict, input_bits: list[int]) -> list[int]:
    """Simulate a small reversible gate list on computational-basis bits."""
    qubit_count = circuit.get("qubit_count")
    if not isinstance(qubit_count, int) or qubit_count < 0:
        raise ValueError("circuit.qubit_count must be a nonnegative integer")
    if len(input_bits) != qubit_count:
        raise ValueError("input length must equal circuit.qubit_count")
    state = list(input_bits)
    for bit in state:
        _validate_bit(bit)
    for gate in circuit.get("gates", []) or []:
        if not isinstance(gate, dict):
            raise ValueError("each gate must be an object")
        _apply_gate(state, gate)
    return state


def all_bitstrings(n: int) -> list[list[int]]:
    """Return all bitstrings of length ``n`` in lexicographic integer order."""
    if n < 0:
        raise ValueError("n must be nonnegative")
    return [[(value >> shift) & 1 for shift in reversed(range(n))] for value in range(2**n)]


def truth_table(circuit: dict) -> list[dict]:
    """Return the full truth table for a small reversible circuit."""
    qubit_count = circuit.get("qubit_count")
    if not isinstance(qubit_count, int) or qubit_count < 0:
        raise ValueError("circuit.qubit_count must be a nonnegative integer")
    return [
        {"input": bits, "output": simulate_gate_list(circuit, bits)}
        for bits in all_bitstrings(qubit_count)
    ]