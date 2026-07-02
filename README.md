# Encrypted Merkle Tree

This repository implements a simple encrypted Merkle tree demo in Python.

Files added to src/:
- encryption.py: AES-GCM encrypt/decrypt helpers (uses cryptography library)
- merkle.py: MerkleTree implementation that builds a tree over SHA-256 of leaves
- cli.py: small CLI and demo helper
- example.py: runnable example script
- tests.py: small tests

Quick start:

1. Create a virtual environment and install dependencies:

   python -m venv .venv
   source .venv/bin/activate   # or .venv\Scripts\activate on Windows
   pip install -r requirements.txt

2. Run the example:

   python -m src.example

Notes:
- This project demonstrates storing ciphertexts in a Merkle tree and producing membership proofs for ciphertexts.
- The verifier who receives ciphertext+proof can check membership without learning the plaintext (unless they also have the decryption key).
- This is a demonstration; it is not intended to be a production-ready zero-knowledge proof system. For robust ZK membership proofs over encrypted data you would combine cryptographic commitments and specialized ZK proof systems.
