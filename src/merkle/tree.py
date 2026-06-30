"""
Encrypted Merkle Tree Implementation

Core Merkle tree with homomorphic encryption support.
"""

from typing import List, Optional, Tuple, Dict, Any
from src.logger import get_logger
from src.crypto.fhe_engine import FHEEngine
from src.crypto.hash_functions import MerkleHash
from src.crypto.commitments import PedersenCommitment
from src.merkle.node import MerkleNode
from src.config import Config

logger = get_logger(__name__)


class MerkleTreeHE:
    """
    Merkle Tree with Homomorphic Encryption

    A complete Merkle tree implementation for encrypted data.
    """

    def __init__(self, fhe_engine: FHEEngine, hash_algorithm: str = "sha256"):
        """
        Initialize encrypted Merkle tree.

        Args:
            fhe_engine: FHE engine for encryption operations
            hash_algorithm: Hash algorithm for tree construction
        """
        self.fhe = fhe_engine
        self.hash_fn = MerkleHash(hash_algorithm)
        self.commitment_scheme = PedersenCommitment(hash_algorithm)
        self.leaves: List[MerkleNode] = []
        self.root: Optional[MerkleNode] = None
        self.encrypted_data: Dict[int, Any] = {}
        self.commitments: Dict[int, Tuple[str, bytes]] = {}
        logger.info("Encrypted Merkle tree initialized")

    def add_encrypted_item(self, plaintext: int, index: Optional[int] = None) -> None:
        """
        Add an encrypted item to the tree.

        Args:
            plaintext: The plaintext value to encrypt
            index: Optional index for the item
        """
        try:
            if index is None:
                index = len(self.leaves)

            # Encrypt the value
            ciphertext = self.fhe.encrypt(plaintext)
            self.encrypted_data[index] = ciphertext

            # Create commitment to plaintext
            commitment, randomness = self.commitment_scheme.commit(plaintext)
            self.commitments[index] = (commitment, randomness)

            # Create leaf node
            leaf_hash = self.hash_fn.hash(commitment)  # Hash the commitment
            leaf_node = MerkleNode(
                index=index,
                hash_value=leaf_hash,
                is_leaf=True,
                encrypted_value=ciphertext,
                commitment=commitment,
            )
            self.leaves.append(leaf_node)
            logger.debug(f"Added encrypted item at index {index}")
        except Exception as e:
            logger.error(f"Failed to add encrypted item: {e}")
            raise

    def build_tree(self) -> None:
        """
        Build the complete Merkle tree from leaves.
        """
        if not self.leaves:
            logger.warning("Cannot build tree: no leaves")
            return

        try:
            current_level = self.leaves.copy()

            while len(current_level) > 1:
                next_level = []
                for i in range(0, len(current_level), 2):
                    left = current_level[i]
                    right = current_level[i + 1] if i + 1 < len(current_level) else left

                    # Create parent node
                    parent_hash = self.hash_fn.hash_pair(left.hash_value, right.hash_value)
                    parent = MerkleNode(
                        index=len(next_level),
                        hash_value=parent_hash,
                        left_child=left,
                        right_child=right,
                        is_leaf=False,
                    )
                    left.parent = parent
                    right.parent = parent
                    next_level.append(parent)

                current_level = next_level

            self.root = current_level[0]
            logger.info(f"Merkle tree built with root hash: {self.root.hash_value[:16]}...")
        except Exception as e:
            logger.error(f"Tree building failed: {e}")
            raise

    def get_root(self) -> str:
        """
        Get the root hash of the tree.

        Returns:
            Root hash value
        """
        if self.root is None:
            raise RuntimeError("Tree not built yet. Call build_tree() first.")
        return self.root.hash_value

    def get_proof(self, leaf_index: int) -> List[Tuple[str, str]]:
        """
        Generate Merkle proof for a leaf.

        Args:
            leaf_index: Index of the leaf

        Returns:
            List of (hash, direction) tuples representing the proof path
        """
        if leaf_index >= len(self.leaves):
            raise ValueError(f"Leaf index {leaf_index} out of range")

        try:
            proof = []
            node = self.leaves[leaf_index]

            while node.parent is not None:
                parent = node.parent
                if node == parent.left_child:
                    # Node is left child, add right sibling
                    sibling = parent.right_child
                    proof.append((sibling.hash_value, "right"))
                else:
                    # Node is right child, add left sibling
                    sibling = parent.left_child
                    proof.append((sibling.hash_value, "left"))
                node = parent

            logger.debug(f"Generated proof for leaf {leaf_index}")
            return proof
        except Exception as e:
            logger.error(f"Proof generation failed: {e}")
            raise

    def verify_proof(self, leaf_hash: str, proof: List[Tuple[str, str]], root: str) -> bool:
        """
        Verify a Merkle proof.

        Args:
            leaf_hash: Hash of the leaf
            proof: Merkle proof (list of sibling hashes)
            root: Expected root hash

        Returns:
            True if proof is valid, False otherwise
        """
        try:
            current_hash = leaf_hash
            for sibling_hash, direction in proof:
                if direction == "right":
                    current_hash = self.hash_fn.hash_pair(current_hash, sibling_hash)
                else:
                    current_hash = self.hash_fn.hash_pair(sibling_hash, current_hash)

            is_valid = current_hash == root
            logger.debug(f"Proof verification: {is_valid}")
            return is_valid
        except Exception as e:
            logger.error(f"Proof verification failed: {e}")
            raise

    def get_tree_info(self) -> Dict[str, Any]:
        """
        Get information about the tree.

        Returns:
            Dictionary with tree statistics
        """
        if self.root is None:
            return {"status": "Tree not built", "leaves": len(self.leaves)}

        return {
            "root_hash": self.root.hash_value[:16] + "...",
            "num_leaves": len(self.leaves),
            "num_nodes": self.root.get_size(),
            "depth": self.root.get_depth(),
        }
