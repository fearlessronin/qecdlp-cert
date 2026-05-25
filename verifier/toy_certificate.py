"""Certificate transcript helpers for public simulated toy Boolean circuits."""

from __future__ import annotations

from .hash_tests import transcript_hash
from .simulate import all_bitstrings, simulate_gate_list
from .toy_functions import TOY_ARITHMETIC_FUNCTIONS, expected_output


def expected_toy_tests(circuit: dict, arithmetic_function: str) -> list[dict]:
    """Return exhaustive toy transcript rows from simulation and expected behavior."""
    qubit_count = circuit.get("qubit_count")
    if not isinstance(qubit_count, int) or qubit_count < 0:
        raise ValueError("circuit.qubit_count must be a nonnegative integer")
    rows = []
    for input_bits in all_bitstrings(qubit_count):
        simulated = simulate_gate_list(circuit, input_bits)
        expected = expected_output(arithmetic_function, input_bits)
        rows.append(
            {
                "input_bits": input_bits,
                "output_bits": simulated,
                "passed": simulated == expected,
            }
        )
    return rows


def verify_toy_transcript(cert: dict, circuit: dict) -> tuple[bool, list[str]]:
    """Verify exhaustive transcript rows for a supported toy reversible Boolean circuit."""
    messages: list[str] = []
    arithmetic_function = cert.get("arithmetic_function")
    if arithmetic_function not in TOY_ARITHMETIC_FUNCTIONS:
        return False, [f"unsupported toy arithmetic_function: {arithmetic_function}"]
    if not cert.get("public_circuit"):
        return False, ["toy certificate requires public_circuit metadata"]

    transcript = cert.get("correctness_transcript", {})
    observed_tests = transcript.get("tests", [])
    expected_tests = expected_toy_tests(circuit, arithmetic_function)

    if observed_tests != expected_tests:
        messages.append("toy truth-table transcript does not match simulated expected rows")

    for index, row in enumerate(observed_tests):
        input_bits = row.get("input_bits")
        output_bits = row.get("output_bits")
        passed = row.get("passed")
        if not isinstance(input_bits, list) or not isinstance(output_bits, list):
            messages.append(f"row {index}: input_bits and output_bits must be lists")
            continue
        try:
            simulated = simulate_gate_list(circuit, input_bits)
            expected = expected_output(arithmetic_function, input_bits)
        except ValueError as exc:
            messages.append(f"row {index}: {exc}")
            continue
        relation_ok = output_bits == simulated == expected
        if passed is not relation_ok:
            messages.append(f"row {index}: passed flag {passed!r} does not match relation result {relation_ok!r}")
        if not relation_ok:
            messages.append(f"row {index}: output_bits do not match simulation and expected function")

    test_generation = cert.get("test_generation", {})
    if not test_generation.get("exhaustive"):
        messages.append("toy transcript must be exhaustive")
    if test_generation.get("test_count") != len(expected_tests):
        messages.append("test_generation.test_count does not match exhaustive truth-table size")

    computed_hash = transcript_hash(observed_tests)
    if computed_hash != cert.get("transcript_hash"):
        messages.append("transcript_hash does not match correctness_transcript.tests")
    else:
        messages.append("transcript hash verified")

    ok = not [message for message in messages if not message.endswith("verified")]
    if ok:
        messages.insert(0, "toy truth-table transcript verified")
    return ok, messages