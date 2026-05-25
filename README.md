# qecdlp-cert

`qecdlp-cert` is a research prototype for verifiable resource certificates for public reversible arithmetic blocks used in quantum elliptic-curve discrete logarithm problem (ECDLP) resource estimation.

The project focuses first on modular inversion over prime fields, a key arithmetic subroutine in affine-coordinate quantum ECDLP implementations. It provides a certificate schema, deterministic hash-derived test generation, toy verification routines, public toy gate-list examples, reproducible reports, and a small classical reversible Boolean simulator for toy circuits.

This repository does **not** implement a quantum attack, recover private keys, or verify withheld circuits from prior work. Its purpose is to make public reversible arithmetic claims more reproducible, comparable, and independently auditable.

## Current status

Step 1 is complete: modular-inversion certificates can be validated against the JSON schema, deterministic SHAKE256-derived test inputs can be regenerated, correctness transcripts can be checked, and transcript hashes can be verified.

Step 2 is complete: certificates may reference a public toy gate-list JSON file. The verifier can recompute the circuit hash, validate qubit indices, count gates, and compare selected resource-count claims against the public gate list.

Step 3 is complete: reproducible certificate reports are generated in Markdown and CSV under `outputs/`.

Step 4 is complete: small public reversible Boolean circuits can be generated, simulated on classical computational-basis inputs, and summarized in a toy circuit report.

Step 5 is complete: supported toy reversible Boolean circuits can be bound to certificates with exhaustive truth-table transcripts, public circuit hashes, and resource-count checks.

The current public gate-list examples are toy artifacts only. `circuits/toy_modinv_stub_8bit.json` is **not** a real modular-inversion circuit; it exists to test certificate/resource-count plumbing.

## Project goals

- Define a reusable resource-certificate format for public reversible arithmetic blocks.
- Support deterministic hash-derived test generation.
- Provide toy modular-inversion certificate examples.
- Verify correctness transcripts and transcript hashes.
- Verify public toy gate-list hashes and resource-count metadata.
- Simulate small public reversible Boolean circuits on classical bit inputs.
- Bind toy simulated circuits to exhaustive truth-table certificates.
- Generate reproducible Markdown and CSV reports for prototype outputs.

## Repository layout

- `schema/` - JSON schema for reversible arithmetic certificates.
- `verifier/` - Python package for certificate parsing, deterministic test generation, modular inversion checks, gate-count checks, toy circuit simulation, toy transcript verification, and reports.
- `examples/` - example certificate files, including transcript-only, circuit-attached, and toy truth-table certificates.
- `circuits/` - public toy gate-list examples.
- `outputs/` - generated Markdown and CSV reports.
- `scripts/` - certificate generation, circuit-attachment, toy-circuit generation, and report helpers.
- `tests/` - pytest tests.
- `docs/` - project documentation and design notes.

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

Generate toy reversible circuits and truth-table certificates:

```bash
python scripts/generate_toy_circuits.py
python scripts/generate_toy_circuit_certificates.py
```

Verify toy truth-table certificates:

```bash
python -m verifier.certificate examples/toy_cnot_copy_cert.json --circuit circuits/toy_cnot_copy.json
python -m verifier.certificate examples/toy_toffoli_and_cert.json --circuit circuits/toy_toffoli_and.json
python -m verifier.certificate examples/toy_swap_cert.json --circuit circuits/toy_swap.json
```

Generate reports:

```bash
python scripts/generate_certificate_report.py
python scripts/generate_toy_circuit_report.py
```

Equivalent Makefile targets, when `make` is available:

```bash
make test
make generate-examples
make verify-examples
make attach-circuit-example
make verify-circuit-example
make verify-all
make report
make generate-toy-circuits
make toy-circuit-report
make generate-toy-certificates
make verify-toy-certificates
```

## Current examples

Certificates:

- `examples/inv_8bit.json` - modular inversion over modulus `251`, transcript-only.
- `examples/inv_16bit.json` - modular inversion over modulus `65521`, transcript-only.
- `examples/inv_8bit_with_circuit.json` - 8-bit transcript with attached public toy gate-list metadata.
- `examples/toy_cnot_copy_cert.json` - exhaustive truth-table certificate for CNOT copy/xor.
- `examples/toy_toffoli_and_cert.json` - exhaustive truth-table certificate for Toffoli AND.
- `examples/toy_swap_cert.json` - exhaustive truth-table certificate for SWAP.

Toy circuit files:

- `circuits/toy_toffoli_identity.json` - tiny identity-style circuit with two Toffoli gates.
- `circuits/toy_modinv_stub_8bit.json` - toy metadata stub, not a real inversion circuit.
- `circuits/toy_cnot_copy.json` - generated CNOT copy/xor toy circuit.
- `circuits/toy_toffoli_and.json` - generated Toffoli AND toy circuit.
- `circuits/toy_swap.json` - generated SWAP toy circuit.

Reports:

- `outputs/certificate_report.md`
- `outputs/certificate_report.csv`
- `outputs/toy_circuit_report.md`
- `outputs/toy_circuit_report.csv`

## Scope and non-goals

This project is limited to public reversible arithmetic-block certification. It does not provide attack circuits, private-key recovery tools, or verification of withheld circuits from prior work.

Current verification covers toy arithmetic transcripts, transcript hashes, public toy gate-list hashes, gate-index checks, selected resource-count metadata, classical simulation of small reversible Boolean toy circuits, and exhaustive truth-table certificates for supported toy functions.

The simulator does not model quantum superposition, amplitudes, phase, measurement, noise, or fault tolerance. Real reversible modular-inversion circuit generation and full circuit-level arithmetic verification are future work.

## Next development step

Step 6: implement a toy reversible modular addition circuit and certificate.