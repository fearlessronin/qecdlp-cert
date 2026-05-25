from verifier.simulate import simulate_gate_list
from verifier.toy_generators import generate_cnot_copy_circuit, generate_swap_circuit, generate_toffoli_and_circuit


def test_generated_circuits_have_expected_ids():
    assert generate_cnot_copy_circuit()["circuit_id"] == "toy-cnot-copy"
    assert generate_toffoli_and_circuit()["circuit_id"] == "toy-toffoli-and"
    assert generate_swap_circuit()["circuit_id"] == "toy-swap"


def test_cnot_copy_expected_map():
    circuit = generate_cnot_copy_circuit()
    assert simulate_gate_list(circuit, [1, 0]) == [1, 1]
    assert simulate_gate_list(circuit, [1, 1]) == [1, 0]


def test_toffoli_and_expected_map():
    circuit = generate_toffoli_and_circuit()
    assert simulate_gate_list(circuit, [1, 1, 0]) == [1, 1, 1]


def test_swap_expected_map():
    circuit = generate_swap_circuit()
    assert simulate_gate_list(circuit, [0, 1]) == [1, 0]