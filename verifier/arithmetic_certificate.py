"""Certificate verification for small reversible arithmetic toy circuits."""

from __future__ import annotations

from .arithmetic_functions import expected_add_mod_2n
from .hash_tests import transcript_hash
from .simulate import all_bitstrings, simulate_gate_list


def _work_indices(circuit: dict) -> list[int]:
    registers = circuit.get("registers", {})
    work = registers.get("work", [])
    return work if isinstance(work, list) else []


def clean_input_bitstrings(circuit: dict) -> list[list[int]]:
    """Return bitstrings with work bits initialized to zero."""
    qubit_count = circuit.get("qubit_count")
    if not isinstance(qubit_count, int) or qubit_count < 0:
        raise ValueError("circuit.qubit_count must be a nonnegative integer")
    work = set(_work_indices(circuit))
    return [bits for bits in all_bitstrings(qubit_count) if all(bits[index] == 0 for index in work)]


def expected_add_mod_2n_tests(circuit: dict, n: int) -> list[dict]:
    """Return exhaustive clean-work transcript rows for toy add mod 2^n."""
    rows = []
    for input_bits in clean_input_bitstrings(circuit):
        simulated = simulate_gate_list(circuit, input_bits)
        expected = expected_add_mod_2n(input_bits, n)
        rows.append(
            {
                "input_bits": input_bits,
                "output_bits": simulated,
                "passed": simulated == expected,
            }
        )
    return rows


def verify_add_mod_2n_transcript(cert: dict, circuit: dict) -> tuple[bool, list[str]]:
    """Verify a toy ``(a,b)->(a,b+a mod 2^n)`` certificate transcript."""
    messages: list[str] = []
    if cert.get("arithmetic_function") != "toy_add_mod_2n":
        return False, ["arithmetic_function is not toy_add_mod_2n"]
    if not cert.get("public_circuit"):
        return False, ["toy_add_mod_2n certificate requires public_circuit metadata"]

    params = cert.get("arithmetic_parameters", {})
    n = params.get("n")
    if not isinstance(n, int) or n <= 0:
        return False, ["arithmetic_parameters.n must be a positive integer"]

    observed_tests = cert.get("correctness_transcript", {}).get("tests", [])
    expected_tests = expected_add_mod_2n_tests(circuit, n)
    if observed_tests != expected_tests:
        messages.append("toy_add_mod_2n transcript does not match simulated expected rows")

    for index, row in enumerate(observed_tests):
        input_bits = row.get("input_bits")
        output_bits = row.get("output_bits")
        passed = row.get("passed")
        if not isinstance(input_bits, list) or not isinstance(output_bits, list):
            messages.append(f"row {index}: input_bits and output_bits must be lists")
            continue
        try:
            simulated = simulate_gate_list(circuit, input_bits)
            expected = expected_add_mod_2n(input_bits, n)
        except ValueError as exc:
            messages.append(f"row {index}: {exc}")
            continue
        relation_ok = output_bits == simulated == expected
        if passed is not relation_ok:
            messages.append(f"row {index}: passed flag {passed!r} does not match relation result {relation_ok!r}")
        if not relation_ok:
            messages.append(f"row {index}: output_bits do not match simulation and add-mod-2^n expectation")

    test_generation = cert.get("test_generation", {})
    if not test_generation.get("exhaustive"):
        messages.append("toy_add_mod_2n transcript must be exhaustive over clean work inputs")
    if test_generation.get("test_count") != len(expected_tests):
        messages.append("test_generation.test_count does not match clean-work truth-table size")

    computed_hash = transcript_hash(observed_tests)
    if computed_hash != cert.get("transcript_hash"):
        messages.append("transcript_hash does not match correctness_transcript.tests")
    else:
        messages.append("transcript hash verified")

    ok = not [message for message in messages if not message.endswith("verified")]
    if ok:
        messages.insert(0, "toy_add_mod_2n transcript verified")
    return ok, messages