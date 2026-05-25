from copy import deepcopy

from scripts.generate_toy_circuit_certificates import TOY_CERTIFICATES, build_toy_certificate
from verifier.certificate import verify_certificate
from verifier.gate_counts import load_gate_list
from verifier.toy_certificate import expected_toy_tests, verify_toy_transcript


def test_expected_toy_tests_are_exhaustive():
    for arithmetic_function, circuit_path, _ in TOY_CERTIFICATES:
        circuit = load_gate_list(circuit_path)
        tests = expected_toy_tests(circuit, arithmetic_function)
        assert len(tests) == 2 ** circuit["qubit_count"]
        assert all(row["passed"] for row in tests)


def test_generated_toy_certificates_verify():
    for arithmetic_function, circuit_path, _ in TOY_CERTIFICATES:
        circuit = load_gate_list(circuit_path)
        cert = build_toy_certificate(arithmetic_function, circuit_path)
        ok, messages = verify_certificate(cert, circuit_path)
        assert ok, messages
        assert len(cert["correctness_transcript"]["tests"]) == 2 ** circuit["qubit_count"]


def test_tampering_with_output_bit_fails():
    arithmetic_function, circuit_path, _ = TOY_CERTIFICATES[0]
    circuit = load_gate_list(circuit_path)
    cert = build_toy_certificate(arithmetic_function, circuit_path)
    tampered = deepcopy(cert)
    tampered["correctness_transcript"]["tests"][0]["output_bits"][0] ^= 1
    ok, messages = verify_toy_transcript(tampered, circuit)
    assert not ok
    assert any("transcript" in message or "output_bits" in message for message in messages)


def test_tampering_with_resource_count_fails():
    arithmetic_function, circuit_path, _ = TOY_CERTIFICATES[0]
    cert = build_toy_certificate(arithmetic_function, circuit_path)
    tampered = deepcopy(cert)
    tampered["resource_counts"]["cnot_count"] += 1
    ok, messages = verify_certificate(tampered, circuit_path)
    assert not ok
    assert any("resource_counts.cnot_count" in message for message in messages)