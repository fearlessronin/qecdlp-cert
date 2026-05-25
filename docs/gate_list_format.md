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

## Scope

The toy circuits are public plumbing examples. `toy_modinv_stub_8bit.json` is not a real modular inversion circuit. It exists only to test circuit hashing, gate-index validation, and resource-count comparison.