"""
Helper Functions

General utility functions.
"""

from typing import List, Any
from src.logger import get_logger

logger = get_logger(__name__)


def chunk_list(lst: List[Any], chunk_size: int) -> List[List[Any]]:
    """
    Split list into chunks.

    Args:
        lst: List to chunk
        chunk_size: Size of each chunk

    Returns:
        List of chunks
    """
    return [lst[i : i + chunk_size] for i in range(0, len(lst), chunk_size)]


def power_of_two(n: int) -> bool:
    """
    Check if number is a power of 2.

    Args:
        n: Number to check

    Returns:
        True if power of 2, False otherwise
    """
    return n > 0 and (n & (n - 1)) == 0


def next_power_of_two(n: int) -> int:
    """
    Get next power of 2 >= n.

    Args:
        n: Starting number

    Returns:
        Next power of 2
    """
    if n <= 1:
        return 1
    return 1 << (n - 1).bit_length()
