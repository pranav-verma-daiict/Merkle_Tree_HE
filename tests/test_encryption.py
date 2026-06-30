"""
Tests for Encryption Module
"""

import pytest
from src.crypto.fhe_engine import FHEEngine
from src.crypto.encryption import EncryptionManager


class TestFHEEngine:
    """Test FHE engine functionality."""

    def test_fhe_setup(self):
        """Test FHE context setup."""
        fhe = FHEEngine()
        fhe.setup()
        assert fhe.context is not None

    def test_encryption_decryption(self):
        """Test encrypt and decrypt operations."""
        fhe = FHEEngine()
        fhe.setup()

        plaintext = 42
        ciphertext = fhe.encrypt(plaintext)
        decrypted = fhe.decrypt(ciphertext)
        assert decrypted[0] == plaintext

    def test_batch_encryption(self):
        """Test batch encryption."""
        fhe = FHEEngine()
        fhe.setup()

        plaintexts = [1, 2, 3, 4, 5]
        ciphertext = fhe.encrypt(plaintexts)
        decrypted = fhe.decrypt(ciphertext)
        assert decrypted == plaintexts


class TestEncryptionManager:
    """Test encryption manager."""

    def test_encrypt_single_value(self):
        """Test encrypting single value."""
        fhe = FHEEngine()
        fhe.setup()
        manager = EncryptionManager(fhe)

        plaintext = 100
        ciphertext = manager.encrypt_value(plaintext)
        assert ciphertext is not None
