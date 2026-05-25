from copy import deepcopy

from scripts.generate_add_mod_2n_certificate import build_add_mod_2n_certificate
from verifier.adder_generator import generate_add_mod_2n_circuit
from verifier.arithmetic_certificate import expected_add_mod_2n_tests, verify_add_mod_2n_transcript
from verifier.certificate import verify_certificate


def test_generated_adder_certificate_verifies():
    circuit = generate_add_mod_2n_circuit(2)
    cert = build_add_mod_2n_certificate(circuit, __import__("pathlib").Path("circuits/toy_add_mod_2n_n2.json"))
    ok, messages = verify_certificate(cert, "circuits/toy_add_mod_2n_n2.json")
    # verify_certificate loads the committed circuit path, so this test assumes generation has run.
    assert ok, messages


def test_expected_add_mod_2n_tests_are_exhaustive():
    circuit = generate_add_mod_2n_circuit(2)
    tests = expected_add_mod_2n_tests(circuit, 2)
    assert len(tests) == 16
    assert all(row["passed"] for row in tests)


def test_tampering_add_mod_output_fails():
    circuit = generate_add_mod_2n_circuit(2)
    cert = build_add_mod_2n_certificate(circuit, __import__("pathlib").Path("circuits/toy_add_mod_2n_n2.json"))
    tampered = deepcopy(cert)
    tampered["correctness_transcript"]["tests"][0]["output_bits"][0] ^= 1
    ok, messages = verify_add_mod_2n_transcript(tampered, circuit)
    assert not ok
    assert any("transcript" in message or "output_bits" in message for message in messages)


def test_tampering_add_mod_resource_count_fails():
    circuit = generate_add_mod_2n_circuit(2)
    cert = build_add_mod_2n_certificate(circuit, __import__("pathlib").Path("circuits/toy_add_mod_2n_n2.json"))
    tampered = deepcopy(cert)
    tampered["resource_counts"]["toffoli_count"] += 1
    ok, messages = verify_certificate(tampered, "circuits/toy_add_mod_2n_n2.json")
    assert not ok
    assert any("resource_counts.toffoli_count" in message for message in messages)