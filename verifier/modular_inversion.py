"""Toy modular-inversion transcript verification routines."""

from __future__ import annotations

from .hash_tests import derive_test_inputs, transcript_hash


def inv_mod(x: int, p: int) -> int:
    """Return ``x^{-1} mod p``."""
    if p < 2:
        raise ValueError("modulus must be at least 2")
    if x % p == 0:
        raise ValueError("zero has no inverse modulo p")
    return pow(x, -1, p)


def check_modinv_pair(x: int, y: int, p: int) -> bool:
    """Check whether ``y`` is an inverse of ``x`` modulo ``p``."""
    return (x * y) % p == 1


def expected_modinv_tests(inputs: list[int], p: int) -> list[dict]:
    """Return canonical expected modular-inversion transcript rows."""
    return [{"x": x, "y": inv_mod(x, p), "passed": True} for x in inputs]


def verify_modinv_outputs(p: int, pairs) -> bool:
    """Verify an iterable of ``(x, y)`` modular-inversion pairs."""
    return all(check_modinv_pair(x, y, p) for x, y in pairs)


def verify_modinv_transcript(cert: dict) -> tuple[bool, list[str]]:
    """Verify a modular-inversion certificate transcript and transcript hash."""
    messages: list[str] = []
    if cert.get("arithmetic_function") != "modular_inversion":
        return False, ["arithmetic_function is not modular_inversion"]

    params = cert.get("arithmetic_parameters", {})
    test_generation = cert.get("test_generation", {})
    transcript = cert.get("correctness_transcript", {})
    tests = transcript.get("tests", [])
    p = params.get("modulus")
    if not isinstance(p, int):
        return False, ["arithmetic_parameters.modulus must be an integer"]

    row_errors = []
    for index, row in enumerate(tests):
        x = row.get("x")
        y = row.get("y")
        passed = row.get("passed")
        if not isinstance(x, int) or not isinstance(y, int):
            row_errors.append(f"row {index}: x and y must be integers")
            continue
        relation_ok = check_modinv_pair(x, y, p)
        if passed is not relation_ok:
            row_errors.append(f"row {index}: passed flag {passed!r} does not match relation result {relation_ok!r}")
        if not relation_ok:
            row_errors.append(f"row {index}: x*y % p != 1")
    if row_errors:
        messages.extend(row_errors)

    exhaustive = bool(test_generation.get("exhaustive", False))
    label = test_generation.get("label", "modinv")
    test_count = int(test_generation.get("test_count", len(tests)))
    observed_inputs = [row.get("x") for row in tests]

    if exhaustive:
        expected_inputs = list(range(1, p))
        if sorted(observed_inputs) != expected_inputs or len(observed_inputs) != len(expected_inputs):
            messages.append("exhaustive transcript must contain exactly all inputs in 1..p-1")
    else:
        seed_hash = test_generation.get("seed_circuit_hash", cert.get("circuit_hash", ""))
        expected_inputs = derive_test_inputs(seed_hash, p, test_count, label)
        if observed_inputs != expected_inputs:
            messages.append("transcript x values do not match deterministic test generation")
        if len(tests) != test_count:
            messages.append("transcript length does not match test_generation.test_count")

    computed_hash = transcript_hash(tests)
    if computed_hash != cert.get("transcript_hash"):
        messages.append("transcript_hash does not match correctness_transcript.tests")
    else:
        messages.append("transcript hash verified")

    ok = not [m for m in messages if not m.endswith("verified")]
    if ok:
        messages.insert(0, "modular inversion transcript verified")
    return ok, messages