"""
Merkle Tree Node Structure

Defines the node structure for encrypted Merkle trees.
"""

from typing import Optional, Any
from dataclasses import dataclass
from src.logger import get_logger

logger = get_logger(__name__)


@dataclass
class MerkleNode:
    """
    Merkle Tree Node

    Represents a node in the encrypted Merkle tree.
    """

    index: int
    hash_value: str
    left_child: Optional['MerkleNode'] = None
    right_child: Optional['MerkleNode'] = None
    is_leaf: bool = False
    encrypted_value: Optional[Any] = None
    commitment: Optional[str] = None
    parent: Optional['MerkleNode'] = None

    def __repr__(self) -> str:
        """String representation of node."""
        return f"MerkleNode(index={self.index}, hash={self.hash_value[:16]}..., leaf={self.is_leaf})"

    def get_depth(self) -> int:
        """
        Calculate depth of subtree rooted at this node.

        Returns:
            Depth of the subtree
        """
        if self.is_leaf:
            return 0
        left_depth = self.left_child.get_depth() if self.left_child else 0
        right_depth = self.right_child.get_depth() if self.right_child else 0
        return 1 + max(left_depth, right_depth)

    def get_size(self) -> int:
        """
        Calculate number of nodes in subtree rooted at this node.

        Returns:
            Number of nodes
        """
        if self.is_leaf:
            return 1
        left_size = self.left_child.get_size() if self.left_child else 0
        right_size = self.right_child.get_size() if self.right_child else 0
        return 1 + left_size + right_size

    def get_leaf_nodes(self) -> list:
        """
        Get all leaf nodes in subtree.

        Returns:
            List of leaf nodes
        """
        if self.is_leaf:
            return [self]
        leaves = []
        if self.left_child:
            leaves.extend(self.left_child.get_leaf_nodes())
        if self.right_child:
            leaves.extend(self.right_child.get_leaf_nodes())
        return leaves
