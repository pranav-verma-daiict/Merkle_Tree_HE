"""
Merkle Tree with Homomorphic Encryption

A complete implementation of a Merkle tree where elements are encrypted
using Fully Homomorphic Encryption (FHE), with zero-knowledge membership proofs.
"""

__version__ = "0.1.0"
__author__ = "Pranav Verma"
__license__ = "MIT"

from src.config import Config
from src.logger import get_logger

logger = get_logger(__name__)

__all__ = ["Config", "get_logger", "logger"]
