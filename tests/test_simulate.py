import pytest

from verifier.simulate import (
    all_bitstrings,
    apply_cnot,
    apply_not,
    apply_swap,
    apply_toffoli,
    simulate_gate_list,
    truth_table,
)
from verifier.toy_generators import generate_cnot_copy_circuit, generate_swap_circuit, generate_toffoli_and_circuit


def test_apply_not():
    state = [0]
    apply_not(state, 0)
    assert state == [1]


def test_apply_cnot():
    state = [1, 0]
    apply_cnot(state, 0, 1)
    assert state == [1, 1]


def test_apply_toffoli():
    state = [1, 1, 0]
    apply_toffoli(state, 0, 1, 2)
    assert state == [1, 1, 1]


def test_apply_swap():
    state = [0, 1]
    apply_swap(state, 0, 1)
    assert state == [1, 0]


def test_simulate_generated_cnot_copy():
    circuit = generate_cnot_copy_circuit()
    assert simulate_gate_list(circuit, [1, 0]) == [1, 1]
    assert simulate_gate_list(circuit, [1, 1]) == [1, 0]


def test_simulate_generated_toffoli_and():
    circuit = generate_toffoli_and_circuit()
    assert simulate_gate_list(circuit, [1, 1, 0]) == [1, 1, 1]
    assert simulate_gate_list(circuit, [1, 0, 0]) == [1, 0, 0]


def test_simulate_generated_swap():
    circuit = generate_swap_circuit()
    assert simulate_gate_list(circuit, [0, 1]) == [1, 0]


def test_truth_table_length_equals_two_to_n():
    circuit = generate_toffoli_and_circuit()
    assert len(truth_table(circuit)) == 2 ** circuit["qubit_count"]
    assert len(all_bitstrings(3)) == 8


def test_invalid_input_raises():
    circuit = generate_cnot_copy_circuit()
    with pytest.raises(ValueError):
        simulate_gate_list(circuit, [1, 2])
    with pytest.raises(ValueError):
        simulate_gate_list(circuit, [1])