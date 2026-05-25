"""Generate toy modular-inversion resource certificates."""

from __future__ import annotations

import argparse
import json
from hashlib import sha256
from pathlib import Path

from verifier.hash_tests import derive_test_inputs, transcript_hash
from verifier.modular_inversion import expected_modinv_tests


def toy_circuit_hash(modulus: int, bits: int) -> str:
    """Return a deterministic placeholder circuit hash for the toy transcript."""
    return sha256(f"toy-modinv-{modulus}-{bits}".encode("utf-8")).hexdigest()


def build_certificate(bits: int, modulus: int, count: int, exhaustive: bool = False) -> dict:
    circuit_hash = toy_circuit_hash(modulus, bits)
    label = "modinv"
    inputs = list(range(1, modulus)) if exhaustive else derive_test_inputs(circuit_hash, modulus, count, label)
    tests = expected_modinv_tests(inputs, modulus)
    return {
        "certificate_version": "0.1.0",
        "certificate_id": f"inv-{bits}bit-toy-transcript",
        "circuit_hash": circuit_hash,
        "gate_basis": ["NOT", "CNOT", "TOFFOLI"],
        "arithmetic_function": "modular_inversion",
        "arithmetic_parameters": {
            "modulus": modulus,
            "bit_length": bits,
            "field": "prime_field",
        },
        "resource_counts": {
            "logical_qubits": 2 * bits,
            "ancilla_qubits": bits,
            "toffoli_count": 0,
            "cnot_count": 0,
            "depth": 0,
            "source": "toy arithmetic transcript only; no gate-level circuit supplied",
        },
        "io_spec": {
            "domain": "F_p^*",
            "input_register": "x",
            "output_register": "x^{-1} mod p",
            "relation": "x * y % p == 1",
        },
        "test_generation": {
            "method": "shake256",
            "label": label,
            "test_count": len(tests),
            "exhaustive": exhaustive,
        },
        "correctness_transcript": {
            "tests": tests,
        },
        "transcript_hash": transcript_hash(tests),
        "proof_artifact": {"type": "none"},
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate a toy modular-inversion certificate.")
    parser.add_argument("--bits", type=int, required=True)
    parser.add_argument("--modulus", type=int, required=True)
    parser.add_argument("--count", type=int, required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--exhaustive", action="store_true")
    args = parser.parse_args(argv)

    cert = build_certificate(args.bits, args.modulus, args.count, args.exhaustive)
    output = Path(args.out)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(cert, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"wrote {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())