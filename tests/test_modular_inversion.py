from verifier.certificate import load_certificate
from verifier.modular_inversion import (
    check_modinv_pair,
    expected_modinv_tests,
    inv_mod,
    verify_modinv_transcript,
)


def test_inv_mod_small_primes():
    assert inv_mod(2, 5) == 3
    assert inv_mod(3, 7) == 5


def test_check_modinv_pair():
    assert check_modinv_pair(2, 3, 5)
    assert not check_modinv_pair(2, 4, 5)


def test_expected_modinv_tests():
    assert expected_modinv_tests([2, 3], 5) == [
        {"x": 2, "y": 3, "passed": True},
        {"x": 3, "y": 2, "passed": True},
    ]


def test_verify_example_transcripts():
    for path in ["examples/inv_8bit.json", "examples/inv_16bit.json"]:
        cert = load_certificate(path)
        ok, messages = verify_modinv_transcript(cert)
        assert ok, messages