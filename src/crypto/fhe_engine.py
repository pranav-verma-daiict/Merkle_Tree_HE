"""
Fully Homomorphic Encryption Engine

Wrapper around TenSEAL for FHE operations.
"""

import tenseal as ts
import pickle
from pathlib import Path
from src.logger import get_logger
from src.config import Config
from typing import Optional, List, Union

logger = get_logger(__name__)


class FHEEngine:
    """Wrapper class for TenSEAL FHE operations."""

    def __init__(self, deterministic: bool = True):
        """
        Initialize FHE engine.

        Args:
            deterministic: Whether to use deterministic encryption mode
        """
        self.deterministic = deterministic
        self.context = None
        self.secret_key = None
        self.public_key = None
        logger.info("FHE Engine initialized")

    def setup(self, poly_modulus_degree: Optional[int] = None) -> None:
        """
        Setup FHE parameters and generate keys.

        Args:
            poly_modulus_degree: Polynomial modulus degree (default from config)
        """
        if poly_modulus_degree is None:
            poly_modulus_degree = Config.POLY_MODULUS_DEGREE

        try:
            # Create TenSEAL context
            self.context = ts.context(
                ts.SCHEME_TYPE.BFV,
                poly_modulus_degree=poly_modulus_degree,
                coeff_modulus_bits=[60, 40, 40, 60],
            )
            self.context.generate_galois_keys()
            self.context.generate_relin_keys()

            logger.info(f"FHE context created with poly_modulus_degree={poly_modulus_degree}")
        except Exception as e:
            logger.error(f"Failed to setup FHE context: {e}")
            raise

    def encrypt(self, plaintext: Union[int, float, List[int]]) -> ts.BFVVector:
        """
        Encrypt plaintext using FHE.

        Args:
            plaintext: Data to encrypt (int, float, or list)

        Returns:
            Encrypted ciphertext
        """
        if self.context is None:
            raise RuntimeError("FHE engine not initialized. Call setup() first.")

        try:
            if isinstance(plaintext, (list, tuple)):
                ciphertext = ts.bfv_vector(self.context, plaintext)
            else:
                ciphertext = ts.bfv_vector(self.context, [plaintext])
            logger.debug(f"Encrypted plaintext: {plaintext}")
            return ciphertext
        except Exception as e:
            logger.error(f"Encryption failed: {e}")
            raise

    def decrypt(self, ciphertext: ts.BFVVector) -> Union[int, List[int]]:
        """
        Decrypt ciphertext using secret key.

        Args:
            ciphertext: Encrypted data

        Returns:
            Decrypted plaintext
        """
        if self.context is None:
            raise RuntimeError("FHE engine not initialized. Call setup() first.")

        try:
            plaintext = ciphertext.decrypt()
            logger.debug(f"Decrypted ciphertext")
            return plaintext
        except Exception as e:
            logger.error(f"Decryption failed: {e}")
            raise

    def add(self, ct1: ts.BFVVector, ct2: Union[ts.BFVVector, int]) -> ts.BFVVector:
        """
        Homomorphic addition.

        Args:
            ct1: First ciphertext
            ct2: Second ciphertext or plaintext integer

        Returns:
            Sum of ct1 and ct2 (encrypted)
        """
        try:
            if isinstance(ct2, int):
                result = ct1 + ct2
            else:
                result = ct1 + ct2
            logger.debug("Homomorphic addition completed")
            return result
        except Exception as e:
            logger.error(f"Homomorphic addition failed: {e}")
            raise

    def multiply(self, ct1: ts.BFVVector, ct2: Union[ts.BFVVector, int]) -> ts.BFVVector:
        """
        Homomorphic multiplication.

        Args:
            ct1: First ciphertext
            ct2: Second ciphertext or plaintext integer

        Returns:
            Product of ct1 and ct2 (encrypted)
        """
        try:
            if isinstance(ct2, int):
                result = ct1 * ct2
            else:
                result = ct1 * ct2
            logger.debug("Homomorphic multiplication completed")
            return result
        except Exception as e:
            logger.error(f"Homomorphic multiplication failed: {e}")
            raise

    def save_keys(self, directory: Optional[Path] = None) -> None:
        """
        Save public and secret keys to files.

        Args:
            directory: Directory to save keys (default from config)
        """
        if directory is None:
            directory = Config.KEYS_DIR

        try:
            directory.mkdir(parents=True, exist_ok=True)
            with open(directory / "context.pkl", "wb") as f:
                pickle.dump(self.context, f)
            logger.info(f"Keys saved to {directory}")
        except Exception as e:
            logger.error(f"Failed to save keys: {e}")
            raise

    def load_keys(self, directory: Optional[Path] = None) -> None:
        """
        Load public and secret keys from files.

        Args:
            directory: Directory to load keys from (default from config)
        """
        if directory is None:
            directory = Config.KEYS_DIR

        try:
            with open(directory / "context.pkl", "rb") as f:
                self.context = pickle.load(f)
            logger.info(f"Keys loaded from {directory}")
        except Exception as e:
            logger.error(f"Failed to load keys: {e}")
            raise

    def get_context(self) -> ts.Context:
        """
        Get the TenSEAL context.

        Returns:
            TenSEAL context
        """
        if self.context is None:
            raise RuntimeError("FHE context not initialized. Call setup() first.")
        return self.context
