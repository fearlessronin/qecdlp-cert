from verifier.hash_tests import derive_test_inputs, shake256_bytes


def test_shake256_bytes_length():
    assert len(shake256_bytes(b"seed", 16)) == 16


def test_derive_test_inputs_deterministic():
    first = derive_test_inputs("abc", 251, 10)
    second = derive_test_inputs("abc", 251, 10)
    assert first == second


def test_derive_test_inputs_domain():
    values = derive_test_inputs("abc", 251, 50)
    assert all(1 <= value <= 250 for value in values)
