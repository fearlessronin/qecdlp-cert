from verifier.hash_tests import derive_test_inputs, transcript_hash


def test_derive_test_inputs_is_deterministic():
    first = derive_test_inputs("abc123", 251, 16, "modinv")
    second = derive_test_inputs("abc123", 251, 16, "modinv")
    assert first == second


def test_derive_test_inputs_avoids_zero():
    values = derive_test_inputs("abc123", 251, 64, "modinv")
    assert all(1 <= value <= 250 for value in values)


def test_transcript_hash_is_stable():
    tests = [{"x": 2, "y": 3, "passed": True}]
    assert transcript_hash(tests) == transcript_hash(tests)
    assert transcript_hash(tests) != transcript_hash([{ "x": 2, "y": 4, "passed": False }])