"""
Merkle Proof Management

Handles generation and verification of Merkle proofs.
"""

from typing import List, Tuple, Optional, Any
from dataclasses import dataclass
from src.logger import get_logger

logger = get_logger(__name__)


@dataclass
class MerkleProof:
    """Data structure for Merkle proof."""

    leaf_index: int
    leaf_hash: str
    proof_path: List[Tuple[str, str]]  # (hash, direction)
    root_hash: str

    def __repr__(self) -> str:
        return f"MerkleProof(leaf={self.leaf_index}, depth={len(self.proof_path)})"

    def to_dict(self) -> dict:
        """Convert proof to dictionary."""
        return {
            "leaf_index": self.leaf_index,
            "leaf_hash": self.leaf_hash,
            "proof_path": self.proof_path,
            "root_hash": self.root_hash,
        }


class ProofManager:
    """Manages Merkle proof operations."""

    @staticmethod
    def create_proof(
        leaf_index: int, leaf_hash: str, proof_path: List[Tuple[str, str]], root_hash: str
    ) -> MerkleProof:
        """
        Create a Merkle proof object.

        Args:
            leaf_index: Index of the leaf
            leaf_hash: Hash of the leaf
            proof_path: Proof path (siblings)
            root_hash: Root hash

        Returns:
            MerkleProof object
        """
        proof = MerkleProof(
            leaf_index=leaf_index,
            leaf_hash=leaf_hash,
            proof_path=proof_path,
            root_hash=root_hash,
        )
        logger.debug(f"Created proof for leaf {leaf_index}")
        return proof

    @staticmethod
    def verify_proof(proof: MerkleProof, hash_fn) -> bool:
        """
        Verify a Merkle proof using the provided hash function.

        Args:
            proof: MerkleProof object to verify
            hash_fn: Hash function to use for verification

        Returns:
            True if proof is valid, False otherwise
        """
        try:
            current_hash = proof.leaf_hash
            for sibling_hash, direction in proof.proof_path:
                if direction == "right":
                    current_hash = hash_fn.hash_pair(current_hash, sibling_hash)
                else:
                    current_hash = hash_fn.hash_pair(sibling_hash, current_hash)

            is_valid = current_hash == proof.root_hash
            logger.debug(f"Proof verification result: {is_valid}")
            return is_valid
        except Exception as e:
            logger.error(f"Proof verification failed: {e}")
            raise
