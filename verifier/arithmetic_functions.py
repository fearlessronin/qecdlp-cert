"""Expected behavior for small reversible arithmetic toy functions."""

from __future__ import annotations


def bits_to_int(bits: list[int]) -> int:
    """Interpret little-endian bits as an integer."""
    value = 0
    for index, bit in enumerate(bits):
        if bit not in (0, 1):
            raise ValueError("bits must be 0 or 1")
        value |= bit << index
    return value


def int_to_bits(x: int, n: int) -> list[int]:
    """Return the ``n`` low bits of ``x`` in little-endian order."""
    if n < 0:
        raise ValueError("n must be nonnegative")
    if x < 0:
        raise ValueError("x must be nonnegative")
    return [(x >> index) & 1 for index in range(n)]


def expected_add_mod_2n(input_bits: list[int], n: int) -> list[int]:
    """Return expected output for ``(a,b) -> (a,b+a mod 2^n)``.

    The first ``n`` bits are the little-endian ``a`` register and the next ``n``
    bits are the little-endian ``b`` register. Extra work bits are preserved.
    """
    if n <= 0:
        raise ValueError("n must be positive")
    if len(input_bits) < 2 * n:
        raise ValueError("input_bits length must be at least 2n")
    if any(bit not in (0, 1) for bit in input_bits):
        raise ValueError("bits must be 0 or 1")
    a_bits = input_bits[:n]
    b_bits = input_bits[n : 2 * n]
    work_bits = input_bits[2 * n :]
    a = bits_to_int(a_bits)
    b = bits_to_int(b_bits)
    modulus = 2**n
    return a_bits + int_to_bits((b + a) % modulus, n) + work_bits