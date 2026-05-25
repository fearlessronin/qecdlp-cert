from pathlib import Path

from verifier.certificate import certificate_summary, load_certificate, validate_certificate, verify_certificate
from verifier.gate_counts import load_gate_list


SCHEMA = Path("schema/reversible_arithmetic_certificate.schema.json")


def test_examples_validate_against_schema():
    for path in [
        Path("examples/inv_8bit.json"),
        Path("examples/inv_16bit.json"),
        Path("examples/inv_8bit_with_circuit.json"),
    ]:
        cert = load_certificate(path)
        validate_certificate(cert, SCHEMA)


def test_certificate_summary_has_core_fields():
    cert = load_certificate("examples/inv_8bit.json")
    summary = certificate_summary(cert)
    assert summary["certificate_id"]
    assert summary["arithmetic_function"] == "modular_inversion"
    assert summary["modulus"] == cert["arithmetic_parameters"]["modulus"]
    assert summary["bit_length"] == cert["arithmetic_parameters"]["bit_length"]
    assert summary["test_count"] == cert["test_generation"]["test_count"]
    assert summary["proof_artifact"] == "none"


def test_certificate_with_public_circuit_verifies():
    cert = load_certificate("examples/inv_8bit_with_circuit.json")
    load_gate_list("circuits/toy_modinv_stub_8bit.json")
    ok, messages = verify_certificate(cert, "circuits/toy_modinv_stub_8bit.json")
    assert ok, messages