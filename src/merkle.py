"""Simple Merkle tree implementation operating over hashes (SHA-256).

Leaves are expected to be bytes (e.g., ciphertext bytes) or hex strings; the API normalizes to bytes.
"""
from __future__ import annotations

from typing import List, Tuple
import hashlib


def _to_bytes(x) -> bytes:
    if isinstance(x, str):
        # assume hex string
        try:
            return bytes.fromhex(x)
        except ValueError:
            return x.encode()
    if isinstance(x, bytes):
        return x
    return str(x).encode()


def sha256(data: bytes) -> bytes:
    return hashlib.sha256(data).digest()


class MerkleTree:
    def __init__(self, leaves: List[bytes]):
        # normalize leaves to hashes of the provided data
        self.leaves = [sha256(_to_bytes(x)) for x in leaves]
        if not self.leaves:
            self.levels: List[List[bytes]] = []
            return
        self.levels = [self.leaves]
        self._build()

    def _build(self) -> None:
        current = self.leaves
        while len(current) > 1:
            next_level: List[bytes] = []
            # if odd, duplicate the last node
            if len(current) % 2 == 1:
                current = current + [current[-1]]
            for i in range(0, len(current), 2):
                left = current[i]
                right = current[i + 1]
                parent = sha256(left + right)
                next_level.append(parent)
            self.levels.append(next_level)
            current = next_level

    @property
    def root(self) -> bytes:
        if not self.levels:
            return b""
        return self.levels[-1][0]

    def get_root_hex(self) -> str:
        return self.root.hex()

    def get_proof(self, index: int) -> List[Tuple[str, str]]:
        """Return a Merkle proof for the leaf at index.

        The proof is a list of tuples (sibling_hex, position) where position is 'left' or 'right'
        indicating sibling's position relative to the node.
        """
        if index < 0 or index >= len(self.leaves):
            raise IndexError("leaf index out of range")
        proof: List[Tuple[str, str]] = []
        idx = index
        for level in self.levels[:-1]:
            # ensure even length
            level_nodes = level
            if len(level_nodes) % 2 == 1:
                level_nodes = level_nodes + [level_nodes[-1]]
            sibling_index = idx ^ 1
            sibling = level_nodes[sibling_index]
            pos = "left" if sibling_index < idx else "right"
            proof.append((sibling.hex(), pos))
            idx = idx // 2
        return proof

    @staticmethod
    def verify_proof(leaf_data: bytes, proof: List[Tuple[str, str]], root_hex: str) -> bool:
        current = sha256(_to_bytes(leaf_data))
        for sibling_hex, pos in proof:
            sibling = bytes.fromhex(sibling_hex)
            if pos == "left":
                current = sha256(sibling + current)
            else:
                current = sha256(current + sibling)
        return current.hex() == root_hex


if __name__ == "__main__":
    # small demo
    data = [b"a", b"b", b"c"]
    t = MerkleTree(data)
    print("root:", t.get_root_hex())
    proof = t.get_proof(1)
    print("proof for index 1:", proof)
    ok = MerkleTree.verify_proof(b"b", proof, t.get_root_hex())
    print("verify (plaintext) ->", ok)
