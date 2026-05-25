# Certificate Format

A reversible arithmetic resource certificate records a public claim about a reversible arithmetic block. The certificate is intended to make public quantum-ECDLP arithmetic claims reproducible, comparable, and independently auditable.

The v0.1 format requires the following top-level fields:

- `certificate_version`: schema/prototype version string.
- `certificate_id`: human-readable identifier.
- `circuit_hash`: binding commitment for deterministic tests.
- `gate_basis`: declared reversible gate basis.
- `arithmetic_function`: currently `modular_inversion`.
- `arithmetic_parameters`: modulus, bit length, and field descriptor.
- `resource_counts`: public metadata such as qubit counts, Toffoli count, CNOT count, depth, and source.
- `io_spec`: domain, input register, output register, and arithmetic relation.
- `test_generation`: deterministic test rule metadata.
- `correctness_transcript`: test rows containing `x`, `y`, and `passed`.
- `transcript_hash`: SHA-256 hash of the canonical JSON transcript rows.
- `proof_artifact`: optional proof metadata.

For v0.1, `proof_artifact` may be `{ "type": "none" }`. This means the verifier checks the public transcript and metadata only; it does not claim a formal proof of a gate-level circuit.

The first target is modular inversion over prime fields, with relation:

`x * y % p == 1`.