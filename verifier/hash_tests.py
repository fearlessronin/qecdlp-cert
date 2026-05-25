"""Deterministic hash-derived test generation."""

from hashlib import shake_256


def shake256_bytes(seed: bytes, nbytes: int) -> bytes:
    """Return nbytes from SHAKE256(seed)."""
    return shake_256(seed).digest(nbytes)


def derive_test_inputs(circuit_hash: str, modulus: int, count: int, label: str = "modinv") -> list[int]:
    """Derive deterministic modular-inversion inputs in 1..modulus-1."""
    if modulus <= 2:
        raise ValueError("modulus must be greater than 2")
    if count < 0:
        raise ValueError("count must be nonnegative")

    seed = f"{circuit_hash}|{modulus}|{label}".encode("utf-8")
    width = max(2, (modulus.bit_length() + 7) // 8)
    stream = shake256_bytes(seed, width * max(count, 1) * 2)
    values = []
    cursor = 0
    while len(values) < count:
        if cursor + width > len(stream):
            stream += shake256_bytes(seed + len(stream).to_bytes(8, "big"), width * count)
        chunk = stream[cursor : cursor + width]
        cursor += width
        value = int.from_bytes(chunk, "big") % modulus
        if value == 0:
            continue
        values.append(value)
    return values
