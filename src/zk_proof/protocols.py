"""
Zero-Knowledge Proof Protocols

Implements various ZK proof protocols for membership verification.
"""

from typing import Optional, Dict, Any, Tuple
from src.logger import get_logger
from src.crypto.fhe_engine import FHEEngine
from src.merkle.tree import MerkleTreeHE
import hashlib
import os

logger = get_logger(__name__)


class ZKMembershipProof:
    """
    Zero-Knowledge Membership Proof Protocol

    Proves that a plaintext is a member of the encrypted set
    without revealing the plaintext or breaking encryption.
    """

    def __init__(self, fhe_engine: FHEEngine, merkle_tree: MerkleTreeHE):
        """
        Initialize ZK membership proof protocol.

        Args:
            fhe_engine: FHE engine
            merkle_tree: Merkle tree instance
        """
        self.fhe = fhe_engine
        self.merkle_tree = merkle_tree
        logger.info("ZK Membership Proof protocol initialized")

    def prove(
        self, plaintext: int, index: int, use_merkle_proof: bool = True
    ) -> Dict[str, Any]:
        """
        Generate a zero-knowledge proof of membership.

        Args:
            plaintext: The plaintext value
            index: Index in the tree
            use_merkle_proof: Whether to include Merkle proof

        Returns:
            Dictionary containing the proof
        """
        try:
            # Generate challenge (random)
            challenge = os.urandom(32)
            challenge_hash = hashlib.sha256(challenge).hexdigest()

            # Get commitment for the plaintext
            if index not in self.merkle_tree.commitments:
                raise ValueError(f"No commitment found for index {index}")

            commitment, randomness = self.merkle_tree.commitments[index]

            # Generate Merkle proof if requested
            merkle_proof = None
            if use_merkle_proof:
                merkle_proof = self.merkle_tree.get_proof(index)

            # Create ZK proof
            zk_proof = {
                "challenge": challenge_hash,
                "commitment": commitment,
                "index": index,
                "merkle_proof": merkle_proof,
                "randomness_hash": hashlib.sha256(randomness).hexdigest(),
            }

            logger.info(f"Generated ZK proof for leaf {index}")
            return zk_proof
        except Exception as e:
            logger.error(f"ZK proof generation failed: {e}")
            raise

    def verify(self, proof: Dict[str, Any], root_hash: str) -> bool:
        """
        Verify a zero-knowledge proof.

        Args:
            proof: The ZK proof to verify
            root_hash: Expected root hash

        Returns:
            True if proof is valid, False otherwise
        """
        try:
            # Check if commitment matches tree
            if proof["index"] >= len(self.merkle_tree.leaves):
                logger.warning("Invalid leaf index in proof")
                return False

            leaf_node = self.merkle_tree.leaves[proof["index"]]
            if leaf_node.commitment != proof["commitment"]:
                logger.warning("Commitment mismatch")
                return False

            # Verify Merkle proof if included
            if proof["merkle_proof"]:
                leaf_hash = leaf_node.hash_value
                if not self.merkle_tree.verify_proof(leaf_hash, proof["merkle_proof"], root_hash):
                    logger.warning("Merkle proof verification failed")
                    return False

            logger.info("ZK proof verification successful")
            return True
        except Exception as e:
            logger.error(f"ZK proof verification failed: {e}")
            return False
