"""Attach public toy gate-list metadata to a certificate."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from verifier.certificate import load_certificate
from verifier.gate_counts import circuit_hash_from_gate_list, load_gate_list, summarize_gate_counts, validate_gate_indices


def attach_circuit(cert: dict, circuit: dict, circuit_path: str) -> dict:
    """Attach public circuit metadata and gate-list resource counts."""
    errors = validate_gate_indices(circuit)
    if errors:
        raise ValueError("invalid gate list: " + "; ".join(errors))

    circuit_hash = circuit_hash_from_gate_list(circuit)
    summary = summarize_gate_counts(circuit)
    updated = dict(cert)
    test_generation = dict(updated.get("test_generation", {}))
    test_generation.setdefault("seed_circuit_hash", cert.get("circuit_hash", ""))
    updated["test_generation"] = test_generation
    updated["public_circuit"] = {
        "circuit_file": circuit_path,
        "circuit_hash": circuit_hash,
        "circuit_id": circuit.get("circuit_id"),
    }
    updated["circuit_hash"] = circuit_hash
    resource_counts = dict(updated.get("resource_counts", {}))
    resource_counts.update(
        {
            "logical_qubits": summary["logical_qubits"],
            "toffoli_count": summary["toffoli_count"],
            "cnot_count": summary["cnot_count"],
            "depth": summary["depth"],
            "source": "public toy gate-list circuit; not a real modular inversion implementation",
        }
    )
    updated["resource_counts"] = resource_counts
    return updated


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Attach public circuit metadata to a certificate.")
    parser.add_argument("--cert", required=True)
    parser.add_argument("--circuit", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args(argv)

    cert = load_certificate(args.cert)
    circuit = load_gate_list(args.circuit)
    updated = attach_circuit(cert, circuit, args.circuit)
    output = Path(args.out)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(updated, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"wrote {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())