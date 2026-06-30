"""
Hash Functions for Merkle Tree

Provides cryptographic hash functions for merkle tree construction.
"""

import hashlib
from typing import Union, List
from src.logger import get_logger

logger = get_logger(__name__)


class MerkleHash:
    """Hash functions for Merkle tree operations."""

    def __init__(self, algorithm: str = "sha256"):
        """
        Initialize hash function.

        Args:
            algorithm: Hash algorithm (sha256, sha512, etc.)
        """
        self.algorithm = algorithm
        logger.info(f"MerkleHash initialized with {algorithm}")

    def hash(self, data: Union[str, bytes, int]) -> str:
        """
        Hash data using the specified algorithm.

        Args:
            data: Data to hash (converted to string if needed)

        Returns:
            Hash digest as hexadecimal string
        """
        try:
            if isinstance(data, int):
                data = str(data)
            if isinstance(data, str):
                data = data.encode()

            hasher = hashlib.new(self.algorithm)
            hasher.update(data)
            digest = hasher.hexdigest()
            return digest
        except Exception as e:
            logger.error(f"Hashing failed: {e}")
            raise

    def hash_pair(self, left: str, right: str) -> str:
        """
        Hash two values together (for merkle tree parent nodes).

        Args:
            left: Left child hash
            right: Right child hash

        Returns:
            Parent node hash
        """
        try:
            combined = left + right
            parent_hash = self.hash(combined)
            logger.debug(f"Pair hash computed")
            return parent_hash
        except Exception as e:
            logger.error(f"Pair hashing failed: {e}")
            raise

    def hash_list(self, data_list: List[Union[str, bytes, int]]) -> str:
        """
        Hash a list of values.

        Args:
            data_list: List of values to hash

        Returns:
            Combined hash of all values
        """
        try:
            combined = "".join(self.hash(item) for item in data_list)
            result_hash = self.hash(combined)
            logger.debug(f"List hash computed for {len(data_list)} items")
            return result_hash
        except Exception as e:
            logger.error(f"List hashing failed: {e}")
            raise

    def verify_pair_hash(self, left: str, right: str, expected_parent: str) -> bool:
        """
        Verify that parent hash is correct for given children.

        Args:
            left: Left child hash
            right: Right child hash
            expected_parent: Expected parent hash

        Returns:
            True if hash is valid, False otherwise
        """
        try:
            computed_parent = self.hash_pair(left, right)
            is_valid = computed_parent == expected_parent
            logger.debug(f"Pair hash verification: {is_valid}")
            return is_valid
        except Exception as e:
            logger.error(f"Pair hash verification failed: {e}")
            raise
