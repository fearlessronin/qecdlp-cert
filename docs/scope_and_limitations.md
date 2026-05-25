# Scope and Limitations

This project does not implement a quantum attack, recover private keys, or verify withheld circuits from prior work.

The initial scope is public reversible arithmetic-block certification.

Step 1 certificates verify arithmetic transcripts and metadata only. The current modular-inversion examples check deterministic test generation, public input-output transcripts, and transcript hashes. Their resource counts are toy metadata and do not certify a gate-level circuit.

Step 2 adds public toy gate-list resource-count verification. The file `circuits/toy_modinv_stub_8bit.json` is not a real modular inversion circuit. It verifies resource-count plumbing, circuit hashing, and gate-index checks only. Real Luo-style inversion blocks are future work.

Randomized deterministic testing is probabilistic unless the test domain is exhausted or the circuit is formally verified. Future versions may add gate-list examples, formal proof artifacts, zero-knowledge proof prototypes, or full circuit resource recomputation.