"""Generate public toy reversible gate-list circuits."""

from __future__ import annotations

import json
from pathlib import Path

from verifier.toy_generators import generate_cnot_copy_circuit, generate_swap_circuit, generate_toffoli_and_circuit

GENERATED_CIRCUITS = [
    (Path("circuits/toy_cnot_copy.json"), generate_cnot_copy_circuit),
    (Path("circuits/toy_toffoli_and.json"), generate_toffoli_and_circuit),
    (Path("circuits/toy_swap.json"), generate_swap_circuit),
]


def write_circuit(path: Path, circuit: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(circuit, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    for path, generator in GENERATED_CIRCUITS:
        write_circuit(path, generator())
        print(f"wrote {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())