# Paper Artifact Summary

Generated from `outputs/certificate_report.csv` and `outputs/toy_circuit_report.csv`.

## Modular inversion certificates

| Artifact | Function | Bits | Tests | Transcript | Circuit/resources | Status |
| --- | --- | --- | --- | --- | --- | --- |
| inv_8bit | modular inversion | 8 | 32 | hash verified | not attached | pass |
| inv_16bit | modular inversion | 16 | 64 | hash verified | not attached | pass |
| inv_8bit+circuit | modular inversion | 8 | 32 | hash verified | hash/counts verified | pass |

## Toy exhaustive certificates

| Artifact | Function | Bits | Tests | Transcript | Circuit/resources | Status |
| --- | --- | --- | --- | --- | --- | --- |
| CNOT-copy | CNOT copy | 2 | 4 | hash verified | hash/counts verified | pass |
| Toffoli-AND | Toffoli AND | 3 | 8 | hash verified | hash/counts verified | pass |
| SWAP | SWAP | 2 | 4 | hash verified | hash/counts verified | pass |
| add-mod-4 | add mod 4 | 2 | 16 | hash verified | hash/counts verified | pass |

## Resource-count verification fields

| Field | Source | Paper wording |
| --- | --- | --- |
| transcript_hash_verified | certificate report | hash verified |
| public_circuit_attached | certificate report | attached / not attached |
| circuit_hash_verified | certificate report | hash verified / not applicable |
| resource_counts_verified | certificate report | counts verified / not applicable |
| total_gates | toy circuit report | serial gate count |
| serial_depth | toy circuit report | serial gate-count depth; not architecture-aware |

## Notes on limitations

These artifacts certify public toy transcripts, public toy gate-list hashes, and resource-count metadata. They do not implement a quantum attack, recover private keys, verify withheld circuits, or implement a production modular-inversion circuit.
