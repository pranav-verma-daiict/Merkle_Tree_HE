# Architecture Documentation

## Overview

The Merkle Tree with Homomorphic Encryption project is organized into modular components that work together to provide encrypted data structures with zero-knowledge proofs.

## System Architecture

### 1. Cryptography Layer (`src/crypto/`)

Handles all cryptographic operations:

- **fhe_engine.py**: Wrapper around TenSEAL for FHE operations
  - Manages encryption/decryption
  - Handles key generation
  - Supports homomorphic operations (add, multiply)

- **encryption.py**: High-level encryption management
  - Simplifies encryption operations
  - Supports batch operations
  - Manages encrypted data lifecycle

- **commitments.py**: Commitment schemes
  - Pedersen commitments
  - Hash-based commitments
  - Binding plaintexts to ciphertexts

- **hash_functions.py**: Cryptographic hashing
  - Merkle tree hashing
  - Pair hashing for tree construction
  - Support for multiple hash algorithms

### 2. Merkle Tree Layer (`src/merkle/`)

Core tree implementation:

- **node.py**: Merkle tree node structure
  - Leaf and internal nodes
  - Tree navigation
  - Subtree operations

- **tree.py**: Main Merkle tree implementation
  - Tree construction from encrypted data
  - Membership proof generation
  - Root computation

- **proof.py**: Proof management
  - Merkle proof creation
  - Proof verification
  - Proof serialization

### 3. Zero-Knowledge Proof Layer (`src/zk_proof/`)

ZK proof protocols:

- **protocols.py**: ZK proof protocols
  - Membership proof protocol
  - Challenge generation
  - Proof verification without revealing data

### 4. Utilities (`src/utils/`)

Helper functions and utilities:

- **helpers.py**: General utility functions
  - List chunking
  - Power of 2 checks
  - Bit operations

## Data Flow

### Adding an Encrypted Item

```
Plaintext Value
    ↓
Encryption (FHE)
    ↓
Ciphertext
    ↓
Create Commitment
    ↓
Commitment + Randomness
    ↓
Hash Commitment
    ↓
Create Leaf Node
    ↓
Add to Tree
```

### Building the Tree

```
Leaf Nodes (Hashed Commitments)
    ↓
Pair Hashing
    ↓
Create Parent Nodes
    ↓
Repeat Until Single Root
    ↓
Root Hash
```

### Membership Proof

```
Leaf Index
    ↓
Traverse to Root
    ↓
Collect Sibling Hashes
    ↓
Proof Path (Hash + Direction)
    ↓
Merkle Proof
```

### ZK Proof

```
Plaintext + Index
    ↓
Generate Challenge
    ↓
Retrieve Commitment
    ↓
Optional: Generate Merkle Proof
    ↓
ZK Proof Structure
    ↓
Proof Ready for Verification
```

## Security Considerations

### Encryption Security
- FHE provides semantic security
- Ciphertexts are computationally indistinguishable
- No information leakage about plaintexts

### Commitment Security
- Pedersen commitments are computationally binding
- Hides plaintext values
- Can be opened only by the prover

### Merkle Tree Security
- Hash collision resistance
- Tree root uniquely identifies all leaves
- Proof is logarithmic in tree size

### ZK Proof Security
- Completeness: Valid proofs always verify
- Soundness: Invalid proofs fail verification with high probability
- Zero-knowledge: Proof reveals only membership, not the value

## Performance Characteristics

### Time Complexity
- Adding item: O(1) encryption + O(log n) tree rebuild
- Membership proof: O(log n)
- Proof verification: O(log n)
- ZK proof: O(log n)

### Space Complexity
- Tree storage: O(n) nodes
- Proof size: O(log n)
- ZK proof: O(log n)

## Extension Points

The architecture supports these extensions:

1. **Additional Hash Algorithms**: Add to `hash_functions.py`
2. **Different Commitment Schemes**: Extend `commitments.py`
3. **Alternative ZK Protocols**: Add to `zk_proof/protocols.py`
4. **Batch Operations**: Optimize in merkle tree layer
5. **GPU Acceleration**: Hook into FHE engine

## Configuration Management

Configuration is centralized in `src/config.py`:

- Loaded from `.env` file at startup
- Provides defaults for all parameters
- Type-checked at module level
- Directories created automatically

## Logging

Logging is configured via `src/logger.py`:

- Console output for immediate feedback
- File logging with rotation
- Configurable log levels
- Consistent formatting across modules
