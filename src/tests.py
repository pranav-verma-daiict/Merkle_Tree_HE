# Simple tests for the module

from .encryption import generate_key, encrypt, decrypt
from .merkle import MerkleTree


def test_encrypt_decrypt():
    key = generate_key()
    pt = b"sensitive"
    token = encrypt(key, pt)
    out = decrypt(key, token)
    assert out == pt


def test_merkle():
    data = [b"a", b"b", b"c"]
    t = MerkleTree(data)
    root = t.get_root_hex()
    proof = t.get_proof(0)
    assert MerkleTree.verify_proof(data[0], proof, root)


if __name__ == "__main__":
    test_encrypt_decrypt()
    test_merkle()
    print("All tests passed")
