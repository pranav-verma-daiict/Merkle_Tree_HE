"""
Configuration module for Merkle Tree HE

Manages environment variables and configuration settings.
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from typing import Optional

# Load environment variables
env_file = Path(__file__).parent.parent / ".env"
if env_file.exists():
    load_dotenv(env_file)


class Config:
    """Configuration class for the entire application."""

    # Project paths
    PROJECT_ROOT = Path(__file__).parent.parent
    LOGS_DIR = PROJECT_ROOT / "logs"
    OUTPUT_DIR = PROJECT_ROOT / "output"
    KEYS_DIR = PROJECT_ROOT / "keys"

    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE = LOGS_DIR / os.getenv("LOG_FILE", "merkle_tree_he.log")
    LOG_FORMAT = os.getenv("LOG_FORMAT", "%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    # Cryptography
    KEY_SIZE = int(os.getenv("KEY_SIZE", "4096"))
    SECURITY_LEVEL = int(os.getenv("SECURITY_LEVEL", "128"))  # bits

    # FHE Parameters (TenSEAL)
    POLY_MODULUS_DEGREE = int(os.getenv("POLY_MODULUS_DEGREE", "8192"))
    COEFF_MODULUS = int(os.getenv("COEFF_MODULUS", "3"))
    SCALE_BITS = int(os.getenv("SCALE_BITS", "40"))

    # Merkle Tree
    MAX_TREE_DEPTH = int(os.getenv("MAX_TREE_DEPTH", "20"))
    DETERMINISTIC_MODE = os.getenv("DETERMINISTIC_MODE", "true").lower() == "true"
    HASH_ALGORITHM = os.getenv("HASH_ALGORITHM", "sha256")

    # Performance
    BATCH_SIZE = int(os.getenv("BATCH_SIZE", "100"))
    MAX_WORKERS = int(os.getenv("MAX_WORKERS", "4"))
    USE_GPU = os.getenv("USE_GPU", "false").lower() == "true"

    # Output
    SAVE_PROOFS = os.getenv("SAVE_PROOFS", "true").lower() == "true"
    SAVE_KEYS = os.getenv("SAVE_KEYS", "true").lower() == "true"

    @classmethod
    def create_directories(cls) -> None:
        """Create necessary directories if they don't exist."""
        for directory in [cls.LOGS_DIR, cls.OUTPUT_DIR, cls.KEYS_DIR]:
            directory.mkdir(parents=True, exist_ok=True)

    @classmethod
    def get_config_dict(cls) -> dict:
        """Get all configuration as a dictionary."""
        return {
            "PROJECT_ROOT": str(cls.PROJECT_ROOT),
            "LOG_LEVEL": cls.LOG_LEVEL,
            "KEY_SIZE": cls.KEY_SIZE,
            "SECURITY_LEVEL": cls.SECURITY_LEVEL,
            "POLY_MODULUS_DEGREE": cls.POLY_MODULUS_DEGREE,
            "COEFF_MODULUS": cls.COEFF_MODULUS,
            "SCALE_BITS": cls.SCALE_BITS,
            "MAX_TREE_DEPTH": cls.MAX_TREE_DEPTH,
            "DETERMINISTIC_MODE": cls.DETERMINISTIC_MODE,
            "BATCH_SIZE": cls.BATCH_SIZE,
            "USE_GPU": cls.USE_GPU,
        }


# Create directories on module import
Config.create_directories()
