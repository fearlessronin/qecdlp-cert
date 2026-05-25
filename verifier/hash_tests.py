"""Deterministic hash-derived test generation and transcript hashing."""

from __future__ import annotations

import json
from hashlib import sha256, shake_256


def normalize_hex(s: str) -> str:
    """Return lowercase hex text without a leading ``0x`` prefix."""
    value = s.strip().lower()
    if value.startswith("0x"):
        value = value[2:]
    return value


def seed_material(circuit_hash: str, modulus: int, label: str) -> bytes:
    """Build the binding seed material for deterministic tests."""
    if modulus < 2:
        raise ValueError("modulus must be at least 2")
    return f"{normalize_hex(circuit_hash)}|{modulus}|{label}".encode("utf-8")


def shake256_bytes(seed: bytes, nbytes: int) -> bytes:
    """Return ``nbytes`` bytes from SHAKE256(seed)."""
    if nbytes < 0:
        raise ValueError("nbytes must be nonnegative")
    return shake_256(seed).digest(nbytes)


def derive_test_inputs(circuit_hash: str, modulus: int, count: int, label: str = "modinv") -> list[int]:
    """Derive deterministic modular-inversion inputs in ``1..modulus-1``.

    The XOF stream is interpreted in fixed-width chunks. Each chunk is reduced
    modulo ``modulus``; zero is rejected because modular inversion is defined on
    ``F_p^*`` for these certificates.
    """
    if modulus <= 2:
        raise ValueError("modulus must be greater than 2")
    if count < 0:
        raise ValueError("count must be nonnegative")

    seed = seed_material(circuit_hash, modulus, label)
    width = max(2, (modulus.bit_length() + 7) // 8)
    block_index = 0
    stream = b""
    values: list[int] = []
    cursor = 0

    while len(values) < count:
        if cursor + width > len(stream):
            block_seed = seed + block_index.to_bytes(8, "big")
            stream += shake256_bytes(block_seed, width * max(count, 8))
            block_index += 1
        chunk = stream[cursor : cursor + width]
        cursor += width
        value = int.from_bytes(chunk, "big") % modulus
        if value == 0:
            continue
        values.append(value)
    return values


def canonical_json(obj) -> bytes:
    """Return canonical JSON bytes used for transcript commitments."""
    return json.dumps(obj, sort_keys=True, separators=(",", ":")).encode("utf-8")


def sha256_hex(data: bytes) -> str:
    """Return SHA-256 hex digest for ``data``."""
    return sha256(data).hexdigest()


def transcript_hash(tests: list[dict]) -> str:
    """Hash the canonical JSON encoding of transcript test rows."""
    return sha256_hex(canonical_json(tests))