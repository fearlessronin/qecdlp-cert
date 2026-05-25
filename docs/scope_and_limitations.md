# Scope and Limitations

This project does not implement a quantum attack, recover private keys, or verify withheld circuits from prior work.

The initial scope is public reversible arithmetic-block certification.

Step 1 certificates verify arithmetic transcripts and metadata only. The current modular-inversion examples check deterministic test generation, public input-output transcripts, and transcript hashes. Their resource counts are toy metadata and do not certify a gate-level circuit.

Randomized deterministic testing is probabilistic unless the test domain is exhausted or the circuit is formally verified. Future versions may add gate-list examples, formal proof artifacts, zero-knowledge proof prototypes, or full circuit resource recomputation.