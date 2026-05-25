# qecdlp-cert

`qecdlp-cert` is a research prototype for verifiable resource certificates for public reversible arithmetic blocks used in quantum elliptic-curve discrete logarithm problem (ECDLP) resource estimation.

The project focuses first on modular inversion over prime fields, a key arithmetic subroutine in affine-coordinate quantum ECDLP implementations. It provides a certificate schema, deterministic hash-derived test generation, toy verification routines, public toy gate-list examples, and reproducible checks for arithmetic correctness, transcript hashes, and resource-count metadata.

This repository does **not** implement a quantum attack, recover private keys, or verify withheld circuits from prior work. Its purpose is to make public reversible arithmetic claims more reproducible, comparable, and independently auditable.

## Current status

Step 1 is complete: modular-inversion certificates can be validated against the JSON schema, deterministic SHAKE256-derived test inputs can be regenerated, correctness transcripts can be checked, and transcript hashes can be verified.

Step 2 is complete: certificates may reference a public toy gate-list JSON file. The verifier can recompute the circuit hash, validate qubit indices, count gates, and compare selected resource-count claims against the public gate list.

The current public gate-list examples are toy artifacts only. `circuits/toy_modinv_stub_8bit.json` is **not** a real modular-inversion circuit; it exists to test certificate/resource-count plumbing.

## Project goals

- Define a reusable resource-certificate format for public reversible arithmetic blocks.
- Support deterministic hash-derived test generation.
- Provide toy modular-inversion certificate examples.
- Verify correctness transcripts and transcript hashes.
- Verify public toy gate-list hashes and resource-count metadata.
- Support an IACR Cryptology ePrint paper on verifiable quantum-ECDLP arithmetic claims.

## Repository layout

- `schema/` - JSON schema for reversible arithmetic certificates.
- `verifier/` - Python package for certificate parsing, deterministic test generation, modular inversion checks, gate-count metadata checks, and reports.
- `examples/` - example certificate files, including transcript-only and circuit-attached examples.
- `circuits/` - public toy gate-list examples.
- `scripts/` - certificate generation and circuit-attachment helpers.
- `tests/` - pytest tests.
- `docs/` - project documentation and design notes.
- `paper/` - LaTeX source for the ePrint paper.

## Quick start

Run the test suite:

```bash
python -m pytest -q
```

Regenerate the transcript-only modular-inversion examples:

```bash
python scripts/generate_modinv_certificate.py --bits 8 --modulus 251 --count 32 --out examples/inv_8bit.json
python scripts/generate_modinv_certificate.py --bits 16 --modulus 65521 --count 64 --out examples/inv_16bit.json
```

Verify transcript-only examples:

```bash
python -m verifier.certificate examples/inv_8bit.json
python -m verifier.certificate examples/inv_16bit.json
```

Attach the public toy 8-bit gate-list stub to the 8-bit certificate:

```bash
python scripts/attach_circuit_to_certificate.py --cert examples/inv_8bit.json --circuit circuits/toy_modinv_stub_8bit.json --out examples/inv_8bit_with_circuit.json
```

Verify transcript, circuit hash, gate indices, and resource counts:

```bash
python -m verifier.certificate examples/inv_8bit_with_circuit.json --circuit circuits/toy_modinv_stub_8bit.json
```

Equivalent Makefile targets:

```bash
make test
make generate-examples
make verify-examples
make attach-circuit-example
make verify-circuit-example
```

## Current examples

- `examples/inv_8bit.json` - modular inversion over modulus `251`, transcript-only.
- `examples/inv_16bit.json` - modular inversion over modulus `65521`, transcript-only.
- `examples/inv_8bit_with_circuit.json` - 8-bit transcript with attached public toy gate-list metadata.
- `circuits/toy_toffoli_identity.json` - tiny identity-style circuit with two Toffoli gates.
- `circuits/toy_modinv_stub_8bit.json` - toy metadata stub, not a real inversion circuit.

## Scope and non-goals

This project is limited to public reversible arithmetic-block certification. It does not provide attack circuits, private-key recovery tools, or verification of withheld circuits from prior work.

Current verification covers toy arithmetic transcripts, transcript hashes, public toy gate-list hashes, gate-index checks, and selected resource-count metadata. Real reversible modular-inversion circuit generation and full circuit-level arithmetic verification are future work.

## Planned paper

Working title:

**Verifiable Resource Certificates for Public Reversible Arithmetic Blocks in Quantum ECDLP**

## Next development step

Step 3: implement a small reversible arithmetic circuit generator for toy modular operations, then connect generated toy circuits to the certificate/resource-count verifier.