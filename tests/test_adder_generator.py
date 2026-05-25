import pytest

from verifier.adder_generator import generate_add_mod_2n_circuit
from verifier.arithmetic_functions import expected_add_mod_2n
from verifier.simulate import all_bitstrings, simulate_gate_list


def test_generate_add_mod_2n_n2_circuit_metadata():
    circuit = generate_add_mod_2n_circuit(2)
    assert circuit["circuit_id"] == "toy-add-mod-2n-n2"
    assert circuit["arithmetic_function"] == "toy_add_mod_2n"
    assert circuit["qubit_count"] == 4
    assert circuit["registers"]["a"] == [0, 1]
    assert circuit["registers"]["b"] == [2, 3]


def test_generate_add_mod_2n_rejects_other_n_for_now():
    with pytest.raises(ValueError):
        generate_add_mod_2n_circuit(3)


def test_add_mod_2n_circuit_matches_expected_exhaustively():
    circuit = generate_add_mod_2n_circuit(2)
    for input_bits in all_bitstrings(circuit["qubit_count"]):
        assert simulate_gate_list(circuit, input_bits) == expected_add_mod_2n(input_bits, 2)