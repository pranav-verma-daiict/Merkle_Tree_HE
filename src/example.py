"""A runnable example that demonstrates encrypted Merkle tree creation and membership proofs.

Run with:
  python -m src.example
"""
from .encryption import generate_key, encrypt, decrypt
from .merkle import MerkleTree


def run_example():
    print("== Encrypted Merkle Tree Example ==")
    key = generate_key()
    items = [b"hello", b"world", b"test", b"secret"]
    ciphertexts = [encrypt(key, it) for it in items]
    print("Ciphertexts (base64):")
    for i, c in enumerate(ciphertexts):
        print(i, c)
    tree = MerkleTree([c.encode() for c in ciphertexts])
    root = tree.get_root_hex()
    print("Merkle root:", root)
    # pick an item to prove
    i = 1
    proof = tree.get_proof(i)
    print("Proof for index", i)
    print(proof)
    ok = MerkleTree.verify_proof(ciphertexts[i].encode(), proof, root)
    print("Proof valid (verifier who doesn't have decryption key):", ok)
    # decrypt as key holder
    pt = decrypt(key, ciphertexts[i])
    print("Decrypted plaintext (key-holder):", pt)


if __name__ == "__main__":
    run_example()
