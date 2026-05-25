# Gate List Format

Step 2 adds a small public toy gate-list format for resource-count verification. These files are not attack circuits and are not claimed to implement production modular inversion.

A gate-list JSON file contains:

- `circuit_id`: stable identifier.
- `circuit_version`: format or example version.
- `description`: human-readable scope statement.
- `gate_basis`: list of supported gate names.
- `qubit_count`: number of logical qubit wires.
- `gates`: ordered list of gate objects.

Each gate object contains:

- `type`: gate type such as `NOT`, `CNOT`, `TOFFOLI`, or `SWAP`.
- `targets`: target qubit indices.
- `controls`: optional control qubit indices.
- `comment`: optional note.

Example:

```json
{
  "type": "TOFFOLI",
  "controls": [0, 1],
  "targets": [2]
}
```

## Hash Convention

The circuit hash is SHA-256 of the canonical JSON encoding of the full gate-list object. Canonical JSON uses sorted keys and compact separators.

## Count Convention

The verifier computes:

- logical qubits from `qubit_count`;
- gate counts by `type`;
- Toffoli count;
- CNOT count;
- SWAP count;
- NOT count;
- total gates.

The current depth convention is simple serial depth, so `depth = total_gates`.

## Classical Reversible Simulation

Toy gate lists can be simulated on computational-basis bit inputs. The simulator supports `NOT`, `CNOT`, `TOFFOLI`, and `SWAP`, validates input bitstrings, and can generate a full truth table for small circuits.

Toy gate-list circuits can now be bound to certificates with exhaustive truth-table transcripts. The verifier checks the public circuit hash, resource counts, transcript hash, and simulated input-output behavior for supported toy functions.

This simulator does not model quantum superposition, amplitudes, phase, measurement, noise, or fault tolerance. It is only a classical reversible Boolean simulator for small public test circuits. That is enough to check basic reversible behavior for toy examples before connecting generated circuits to certificate metadata.

## Scope

The toy circuits are public plumbing examples. `toy_modinv_stub_8bit.json` is not a real modular inversion circuit. It exists only to test circuit hashing, gate-index validation, and resource-count comparison.