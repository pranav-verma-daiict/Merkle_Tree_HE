"""
Encryption and Decryption utilities

Provides high-level encryption/decryption functions.
"""

from src.logger import get_logger
from src.crypto.fhe_engine import FHEEngine
from typing import Union, List
import hashlib

logger = get_logger(__name__)


class EncryptionManager:
    """Manages encryption operations."""

    def __init__(self, fhe_engine: FHEEngine):
        """
        Initialize encryption manager.

        Args:
            fhe_engine: FHE engine instance
        """
        self.fhe = fhe_engine

    def encrypt_value(self, value: int) -> bytes:
        """
        Encrypt a single integer value.

        Args:
            value: Integer to encrypt

        Returns:
            Encrypted value
        """
        try:
            ciphertext = self.fhe.encrypt(value)
            logger.debug(f"Encrypted value: {value}")
            return ciphertext
        except Exception as e:
            logger.error(f"Encryption failed: {e}")
            raise

    def encrypt_batch(self, values: List[int]) -> List[bytes]:
        """
        Encrypt multiple values.

        Args:
            values: List of integers to encrypt

        Returns:
            List of encrypted values
        """
        try:
            ciphertexts = [self.fhe.encrypt(v) for v in values]
            logger.debug(f"Encrypted {len(values)} values")
            return ciphertexts
        except Exception as e:
            logger.error(f"Batch encryption failed: {e}")
            raise

    def decrypt_value(self, ciphertext: bytes) -> int:
        """
        Decrypt a ciphertext.

        Args:
            ciphertext: Encrypted data

        Returns:
            Decrypted integer
        """
        try:
            plaintext = self.fhe.decrypt(ciphertext)
            logger.debug(f"Decrypted ciphertext")
            return plaintext[0] if isinstance(plaintext, list) else plaintext
        except Exception as e:
            logger.error(f"Decryption failed: {e}")
            raise
