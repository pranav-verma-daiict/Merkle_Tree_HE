"""
Commitment Schemes

Implements various commitment schemes for binding plaintexts to ciphertexts.
"""

import hashlib
import os
from typing import Tuple, Optional
from src.logger import get_logger

logger = get_logger(__name__)


class PedersenCommitment:
    """
    Pedersen Commitment Scheme

    Simple hash-based commitment for this implementation.
    """

    def __init__(self, hash_algorithm: str = "sha256"):
        """
        Initialize Pedersen commitment.

        Args:
            hash_algorithm: Hash algorithm to use
        """
        self.hash_algorithm = hash_algorithm
        logger.info(f"Pedersen commitment initialized with {hash_algorithm}")

    def commit(self, plaintext: int, randomness: Optional[bytes] = None) -> Tuple[str, bytes]:
        """
        Create a commitment to a plaintext.

        Args:
            plaintext: Value to commit to
            randomness: Random bytes (generated if not provided)

        Returns:
            Tuple of (commitment_hash, randomness)
        """
        if randomness is None:
            randomness = os.urandom(32)

        try:
            hasher = hashlib.new(self.hash_algorithm)
            hasher.update(str(plaintext).encode())
            hasher.update(randomness)
            commitment = hasher.hexdigest()
            logger.debug(f"Commitment created for plaintext: {plaintext}")
            return commitment, randomness
        except Exception as e:
            logger.error(f"Commitment creation failed: {e}")
            raise

    def verify(self, plaintext: int, commitment: str, randomness: bytes) -> bool:
        """
        Verify a commitment.

        Args:
            plaintext: Value claimed to be committed
            commitment: The commitment hash
            randomness: The randomness used in commitment

        Returns:
            True if commitment is valid, False otherwise
        """
        try:
            hasher = hashlib.new(self.hash_algorithm)
            hasher.update(str(plaintext).encode())
            hasher.update(randomness)
            computed_commitment = hasher.hexdigest()
            is_valid = computed_commitment == commitment
            logger.debug(f"Commitment verification: {is_valid}")
            return is_valid
        except Exception as e:
            logger.error(f"Commitment verification failed: {e}")
            raise


class HashCommitment:
    """
    Simple Hash-based Commitment

    Even simpler commitment scheme using just hashing.
    """

    def __init__(self, hash_algorithm: str = "sha256"):
        """
        Initialize hash commitment.

        Args:
            hash_algorithm: Hash algorithm to use
        """
        self.hash_algorithm = hash_algorithm

    def commit(self, plaintext: int) -> str:
        """
        Create a commitment by hashing plaintext.

        Args:
            plaintext: Value to commit to

        Returns:
            Hash commitment
        """
        try:
            hasher = hashlib.new(self.hash_algorithm)
            hasher.update(str(plaintext).encode())
            commitment = hasher.hexdigest()
            logger.debug(f"Hash commitment created")
            return commitment
        except Exception as e:
            logger.error(f"Hash commitment creation failed: {e}")
            raise

    def verify(self, plaintext: int, commitment: str) -> bool:
        """
        Verify a hash commitment.

        Args:
            plaintext: Value claimed to be committed
            commitment: The commitment hash

        Returns:
            True if commitment is valid, False otherwise
        """
        try:
            hasher = hashlib.new(self.hash_algorithm)
            hasher.update(str(plaintext).encode())
            computed_commitment = hasher.hexdigest()
            is_valid = computed_commitment == commitment
            logger.debug(f"Hash commitment verification: {is_valid}")
            return is_valid
        except Exception as e:
            logger.error(f"Hash commitment verification failed: {e}")
            raise
