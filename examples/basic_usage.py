"""
Basic Usage Example

Demonstrates basic operations with Merkle Tree HE.
"""

from src.crypto.fhe_engine import FHEEngine
from src.merkle.tree import MerkleTreeHE


def main():
    """Run basic usage example."""
    print("=" * 60)
    print("Merkle Tree with Homomorphic Encryption - Basic Usage")
    print("=" * 60)

    # Initialize FHE engine
    print("\n1. Initializing FHE Engine...")
    fhe = FHEEngine()
    fhe.setup()
    print("   ✓ FHE context created")

    # Create encrypted Merkle tree
    print("\n2. Creating Encrypted Merkle Tree...")
    tree = MerkleTreeHE(fhe)
    print("   ✓ Tree initialized")

    # Add encrypted items
    print("\n3. Adding Encrypted Items...")
    data = [10, 20, 30, 40, 50]
    for i, item in enumerate(data):
        tree.add_encrypted_item(item)
        print(f"   ✓ Added encrypted item {i+1}: {item}")

    # Build tree
    print("\n4. Building Merkle Tree...")
    tree.build_tree()
    print("   ✓ Tree built successfully")

    # Get tree info
    print("\n5. Tree Information:")
    info = tree.get_tree_info()
    for key, value in info.items():
        print(f"   {key}: {value}")

    # Generate membership proof
    print("\n6. Generating Membership Proof...")
    root = tree.get_root()
    leaf_index = 2
    leaf_hash = tree.leaves[leaf_index].hash_value
    proof = tree.get_proof(leaf_index)
    print(f"   ✓ Proof generated for leaf {leaf_index}")
    print(f"   ✓ Proof length: {len(proof)}")

    # Verify membership
    print("\n7. Verifying Membership...")
    is_valid = tree.verify_proof(leaf_hash, proof, root)
    print(f"   ✓ Verification result: {is_valid}")

    # Decrypt and verify
    print("\n8. Decrypting and Verifying...")
    encrypted = tree.encrypted_data[leaf_index]
    decrypted = fhe.decrypt(encrypted)
    print(f"   ✓ Decrypted value: {decrypted[0]}")
    print(f"   ✓ Original value: {data[leaf_index]}")
    assert decrypted[0] == data[leaf_index]

    print("\n" + "=" * 60)
    print("Example completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()
