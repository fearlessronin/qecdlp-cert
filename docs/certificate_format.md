# Certificate Format

A reversible arithmetic resource certificate records a public claim about a reversible arithmetic block. The certificate is intended to make public quantum-ECDLP arithmetic claims reproducible, comparable, and independently auditable.

A certificate should include:

- circuit commitment or circuit hash;
- gate basis;
- arithmetic parameters;
- resource counts;
- input-output specification;
- deterministic test-generation rule;
- correctness transcript hash;
- optional proof artifact.

The first target is modular inversion over prime fields.
