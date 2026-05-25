"""Generate a toy reversible add-mod-2^n gate-list circuit."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from verifier.adder_generator import generate_add_mod_2n_circuit


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate a toy reversible add-mod-2^n circuit.")
    parser.add_argument("--n", type=int, default=2)
    parser.add_argument("--out", required=True)
    args = parser.parse_args(argv)

    circuit = generate_add_mod_2n_circuit(args.n)
    output = Path(args.out)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(circuit, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"wrote {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())