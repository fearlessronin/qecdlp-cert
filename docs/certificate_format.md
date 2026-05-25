# Certificate Format

A reversible arithmetic resource certificate records a public claim about a reversible arithmetic block. The certificate is intended to make public quantum-ECDLP arithmetic claims reproducible, comparable, and independently auditable.

The v0.1 format requires the following top-level fields:

- `certificate_version`: schema/prototype version string.
- `certificate_id`: human-readable identifier.
- `circuit_hash`: binding commitment for deterministic tests or a public circuit hash when a gate-list file is attached.
- `gate_basis`: declared reversible gate basis.
- `arithmetic_function`: supported values are `modular_inversion`, `toy_cnot_copy`, `toy_toffoli_and`, and `toy_swap`.
- `arithmetic_parameters`: modulus, bit length, and field descriptor.
- `resource_counts`: public metadata such as qubit counts, Toffoli count, CNOT count, depth, and source.
- `io_spec`: domain, input register, output register, and arithmetic relation.
- `test_generation`: deterministic test rule metadata.
- `correctness_transcript`: test rows containing either modular-inversion fields `x`, `y`, `passed`, or toy Boolean fields `input_bits`, `output_bits`, `passed`.
- `transcript_hash`: SHA-256 hash of the canonical JSON transcript rows.
- `proof_artifact`: optional proof metadata.

For v0.1, `proof_artifact` may be `{ "type": "none" }`. This means the verifier checks the public transcript and metadata only; it does not claim a formal proof of a gate-level circuit.

## Public Circuit Metadata

A certificate may optionally include `public_circuit`:

- `circuit_file`: path to a public gate-list JSON file.
- `circuit_id`: expected circuit identifier.
- `circuit_hash`: SHA-256 hash of the canonical JSON gate list.

When a public circuit is supplied to the verifier with `--circuit`, the verifier recomputes the circuit hash, validates gate indices, summarizes gate counts, and compares selected resource-count fields against the certificate.

The transcript test seed may be stored as `test_generation.seed_circuit_hash` when a certificate is attached to a later public gate-list hash while preserving an already generated arithmetic transcript.

## Modular Inversion Certificates

The modular-inversion target is over prime fields, with relation:

`x * y % p == 1`.

## Toy Boolean Circuit Certificates

The toy Boolean certificate targets are:

- `toy_cnot_copy`: `(x, y) -> (x, y xor x)`.
- `toy_toffoli_and`: `(x, y, z) -> (x, y, z xor (x and y))`.
- `toy_swap`: `(x, y) -> (y, x)`.

These certificates use exhaustive truth-table transcripts over small public reversible circuits. They validate the certificate pipeline and public-circuit binding mechanism; they are not quantum-ECDLP attack circuits.

## Toy Modular Addition Certificate

`toy_add_mod_2n` certifies a small reversible arithmetic demonstration:

`(a, b) -> (a, b + a mod 2^n)`

The current generated example uses `n=2` with little-endian registers. It is a toy arithmetic block over `Z/(2^n)`, not modular addition over an arbitrary prime field and not a modular inversion circuit.