# Deterministic Test Generation

Tests are generated from a binding circuit or certificate commitment using a deterministic hash-derived procedure.

For example:

1. compute `seed = SHAKE256(circuit_hash || modulus || label)`;
2. generate integers from the XOF stream;
3. reduce into the input domain;
4. reject invalid inputs such as zero for modular inversion over `F_p^*`;
5. verify the arithmetic relation.

For modular inversion, the correctness check is:

`x * y % p == 1`.
