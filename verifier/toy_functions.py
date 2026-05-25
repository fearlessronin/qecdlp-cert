"""Expected behavior for supported public toy reversible Boolean functions."""

from __future__ import annotations

TOY_ARITHMETIC_FUNCTIONS = {"toy_cnot_copy", "toy_toffoli_and", "toy_swap"}


def _require_bits(input_bits: list[int], size: int, name: str) -> None:
    if len(input_bits) != size:
        raise ValueError(f"{name} expects {size} input bits")
    if any(bit not in (0, 1) for bit in input_bits):
        raise ValueError("input bits must be 0 or 1")


def expected_cnot_copy(input_bits: list[int]) -> list[int]:
    """Return expected output for ``(x,y) -> (x, y xor x)``."""
    _require_bits(input_bits, 2, "toy_cnot_copy")
    x, y = input_bits
    return [x, y ^ x]


def expected_toffoli_and(input_bits: list[int]) -> list[int]:
    """Return expected output for ``(x,y,z) -> (x, y, z xor (x and y))``."""
    _require_bits(input_bits, 3, "toy_toffoli_and")
    x, y, z = input_bits
    return [x, y, z ^ (x & y)]


def expected_swap(input_bits: list[int]) -> list[int]:
    """Return expected output for ``(x,y) -> (y,x)``."""
    _require_bits(input_bits, 2, "toy_swap")
    x, y = input_bits
    return [y, x]


def expected_output(arithmetic_function: str, input_bits: list[int]) -> list[int]:
    """Dispatch to the expected output for a supported toy function."""
    if arithmetic_function == "toy_cnot_copy":
        return expected_cnot_copy(input_bits)
    if arithmetic_function == "toy_toffoli_and":
        return expected_toffoli_and(input_bits)
    if arithmetic_function == "toy_swap":
        return expected_swap(input_bits)
    raise ValueError(f"unsupported toy arithmetic function: {arithmetic_function}")