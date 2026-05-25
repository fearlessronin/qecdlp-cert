# Deterministic Test Generation

Tests are generated from a binding circuit or certificate commitment using a deterministic hash-derived procedure.

For modular inversion certificates, the verifier uses:

1. normalize the `circuit_hash`;
2. compute seed material from `circuit_hash || modulus || label`;
3. expand bytes with SHAKE256;
4. interpret fixed-width chunks as integers;
5. reduce each chunk modulo `p`;
6. reject zero, since modular inversion is defined over `F_p^*`;
7. verify the arithmetic relation.

For modular inversion, the correctness check is:

`x * y % p == 1`.

The transcript hash is:

`SHA256(canonical_json(correctness_transcript.tests))`

where canonical JSON uses sorted keys and compact separators. The verifier recomputes this hash and rejects certificates whose transcript rows do not match the committed hash.

If `test_generation.exhaustive` is `false`, the verifier regenerates the deterministic test inputs and checks that the transcript uses exactly those `x` values. If `exhaustive` is `true`, the transcript must contain exactly all values in `1..p-1`.