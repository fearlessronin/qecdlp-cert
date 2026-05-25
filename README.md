# qecdlp-cert

`qecdlp-cert` is a research prototype for verifiable resource certificates for public reversible arithmetic blocks used in quantum elliptic-curve discrete logarithm problem (ECDLP) resource estimation.

The project focuses first on modular inversion over prime fields, a key arithmetic subroutine in affine-coordinate quantum ECDLP implementations. It provides a certificate schema, deterministic hash-derived test generation, toy verification routines, and reproducible examples for checking arithmetic correctness and resource-count claims.

This repository does **not** implement a quantum attack, recover private keys, or verify withheld circuits from prior work. Its purpose is to make public reversible arithmetic claims more reproducible, comparable, and independently auditable.

## Project goals

- Define a reusable resource-certificate format for public reversible arithmetic blocks.
- Support deterministic hash-derived test generation.
- Provide toy modular-inversion certificate examples.
- Provide lightweight verification routines for correctness transcripts and resource metadata.
- Support an IACR Cryptology ePrint paper on verifiable quantum-ECDLP arithmetic claims.

## Repository layout

- `schema/` - JSON schema for reversible arithmetic certificates.
- `verifier/` - Python package for certificate parsing, deterministic test generation, modular inversion checks, gate-count metadata checks, and reports.
- `examples/` - example certificate files.
- `tests/` - pytest tests.
- `docs/` - project documentation and design notes.
- `paper/` - LaTeX source for the ePrint paper.

## Scope and non-goals

This project is limited to public reversible arithmetic-block certification. It does not provide attack circuits, private-key recovery tools, or verification of withheld circuits from prior work.

## Planned paper

Working title:

**Verifiable Resource Certificates for Public Reversible Arithmetic Blocks in Quantum ECDLP**

## Development status

Initial repository scaffold.
