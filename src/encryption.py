# Encrypted Merkle Tree utilities
# Author: GitHub Copilot (assistant)
from typing import Tuple
import base64
import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


def generate_key() -> bytes:
    """Generate a 256-bit AES key."""
    return AESGCM.generate_key(bit_length=256)


def encrypt(key: bytes, plaintext: bytes) -> str:
    """Encrypt plaintext using AES-GCM and return a base64 string containing nonce + ciphertext.

    The format is base64(nonce || ciphertext).
    """
    aesgcm = AESGCM(key)
    nonce = os.urandom(12)
    ct = aesgcm.encrypt(nonce, plaintext, associated_data=None)
    combined = nonce + ct
    return base64.b64encode(combined).decode("ascii")


def decrypt(key: bytes, token: str) -> bytes:
    """Decrypt a base64 token produced by encrypt(). Returns plaintext bytes."""
    aesgcm = AESGCM(key)
    combined = base64.b64decode(token)
    nonce = combined[:12]
    ct = combined[12:]
    return aesgcm.decrypt(nonce, ct, associated_data=None)
