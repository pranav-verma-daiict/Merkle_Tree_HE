"""Command-line utilities and a demo for the Encrypted Merkle Tree project.

Usage examples:
  - Run the demo: python -m src.example
  - Use the functions programatically:
      from src.encryption import generate_key, encrypt, decrypt
      from src.merkle import MerkleTree
"""
from __future__ import annotations

import argparse
import json
from typing import List
from .encryption import generate_key, encrypt, decrypt
from .merkle import MerkleTree


def build_encrypted_tree(key: bytes, items: List[bytes]) -> MerkleTree:
    ciphertexts = [encrypt(key, it) for it in items]
    # MerkleTree wants bytes-like leaves; we use the ciphertext bytes (base64 string encoded)
    return MerkleTree([c.encode("utf-8") for c in ciphertexts]), ciphertexts


def demo():
    print("Encrypted Merkle Tree demo")
    key = generate_key()
    print("Generated AES-256 key (hex):", key.hex())
    items = [b"alice", b"bob", b"carol", b"dave"]
    tree, ciphertexts = build_encrypted_tree(key, items)
    print("Built tree with root:", tree.get_root_hex())
    # choose an index to prove membership
    idx = 2
    token = ciphertexts[idx]
    print(f"Selected index {idx} ciphertext (base64):", token)
    # verifier receives token (cannot decrypt without key) and proof
    proof = tree.get_proof(idx)
    print("Proof:", json.dumps(proof, indent=2))
    # verifier verifies that the ciphertext is contained in the tree
    ok = MerkleTree.verify_proof(token.encode("utf-8"), proof, tree.get_root_hex())
    print("Verifier check (without decryption):", ok)
    # Demonstrate decryption by the key-holder
    plaintext = decrypt(key, token)
    print("Decrypted plaintext by key-holder:", plaintext)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--demo", action="store_true", help="run the built-in demo")
    args = parser.parse_args()
    if args.demo:
        demo()
    else:
        demo()
