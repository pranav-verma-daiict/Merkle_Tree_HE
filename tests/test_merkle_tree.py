"""
Tests for Merkle Tree
"""

import pytest
from src.crypto.fhe_engine import FHEEngine
from src.merkle.tree import MerkleTreeHE


class TestMerkleTreeHE:
    """Test Merkle Tree with HE."""

    def setup_method(self):
        """Setup for each test."""
        self.fhe = FHEEngine()
        self.fhe.setup()
        self.tree = MerkleTreeHE(self.fhe)

    def test_add_encrypted_items(self):
        """Test adding encrypted items."""
        data = [1, 2, 3, 4, 5]
        for item in data:
            self.tree.add_encrypted_item(item)
        assert len(self.tree.leaves) == len(data)

    def test_build_tree(self):
        """Test building tree."""
        data = [10, 20, 30, 40]
        for item in data:
            self.tree.add_encrypted_item(item)
        self.tree.build_tree()
        assert self.tree.root is not None
        assert self.tree.get_root() is not None

    def test_merkle_proof(self):
        """Test merkle proof generation and verification."""
        data = [5, 10, 15, 20]
        for item in data:
            self.tree.add_encrypted_item(item)
        self.tree.build_tree()

        root = self.tree.get_root()
        leaf_index = 1
        leaf_hash = self.tree.leaves[leaf_index].hash_value
        proof = self.tree.get_proof(leaf_index)

        is_valid = self.tree.verify_proof(leaf_hash, proof, root)
        assert is_valid is True
