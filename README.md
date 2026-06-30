# Merkle Tree with Homomorphic Encryption

A complete implementation of a Merkle tree where elements are encrypted using Fully Homomorphic Encryption (FHE). This project explores zero-knowledge membership queries on encrypted data without revealing the plaintext values.

## Project Overview

### Problem Statement
Traditional Merkle trees use hash functions to create a tree structure for efficient membership proofs. However, when data is encrypted using probabilistic HE schemes, each encryption of the same plaintext produces different ciphertexts, making traditional hashing unstable.

### Solution Approach
This project implements **Encrypted Merkle Tree with Zero-Knowledge Proofs** using:
1. **Deterministic Encryption Mode** - For consistent ciphertexts
2. **Commitment Schemes** - To bind plaintexts to encrypted values
3. **Zero-Knowledge Proofs** - For membership verification without revealing data
4. **Homomorphic Hash Functions** - For computation in encrypted domain

## Architecture

```
┌─────────────────────────────────────────┐
│   Encrypted Merkle Tree Layer           │
│  (with ZK Proofs & Commitments)         │
├─────────────────────────────────────────┤
│                                         │
│  ┌─────────────────────────────────┐   │
│  │  Merkle Tree Structure           │   │
│  │  (Root & Intermediate Nodes)     │   │
│  └─────────────────────────────────┘   │
│                 ↓                       │
│  ┌─────────────────────────────────┐   │
│  │  Commitment Layer               │   │
│  │  (Pedersen/Hash Commitments)    │   │
│  └─────────────────────────────────┘   │
│                 ↓                       │
│  ┌─────────────────────────────────┐   │
│  │  Encrypted Data Layer           │   │
│  │  (Ciphertexts & Public Keys)    │   │
│  └─────────────────────────────────┘   │
│                 ↓                       │
│  ┌─────────────────────────────────┐   │
│  │  Zero-Knowledge Proofs          │   │
│  │  (Sigma Protocols/Range Proofs) │   │
│  └─────────────────────────────────┘   │
│                                         │
└─────────────────────────────────────────┘
```

## Features

- ✅ Fully Homomorphic Encryption support
- ✅ Merkle tree construction on encrypted data
- ✅ Zero-knowledge membership proofs
- ✅ Commitment schemes for data binding
- ✅ Deterministic and probabilistic encryption modes
- ✅ Comprehensive test suite
- ✅ Documentation and examples

## Project Structure

```
Merkle_Tree_HE/
├── README.md                    # This file
├── requirements.txt             # Python dependencies
├── setup.py                     # Package setup
├── .gitignore                   # Git ignore rules
├── .env.example                 # Environment variables template
│
├── src/
│   ├── __init__.py
│   ├── config.py               # Configuration settings
│   ├── logger.py               # Logging utilities
│   │
│   ├── crypto/
│   │   ├── __init__.py
│   │   ├── fhe_engine.py       # FHE operations wrapper
│   │   ├── encryption.py       # Encryption/Decryption
│   │   ├── commitments.py      # Commitment schemes
│   │   └── hash_functions.py   # Homomorphic hash functions
│   │
│   ├── merkle/
│   │   ├── __init__.py
│   │   ├── tree.py             # Core Merkle tree implementation
│   │   ├── node.py             # Merkle tree node structure
│   │   └── proof.py            # Membership proof generation
│   │
│   ├── zk_proof/
│   │   ├── __init__.py
│   │   ├── protocols.py        # Zero-knowledge protocols
│   │   ├── verifier.py         # Proof verification
│   │   └── prover.py           # Proof generation
│   │
│   └── utils/
│       ├── __init__.py
│       ├── serialization.py    # Data serialization
│       └── helpers.py          # Utility functions
│
├── tests/
│   ├── __init__.py
│   ├── test_encryption.py      # Encryption tests
│   ├── test_commitments.py     # Commitment tests
│   ├── test_merkle_tree.py     # Merkle tree tests
│   ├── test_zk_proofs.py       # ZK proof tests
│   └── test_integration.py     # End-to-end tests
│
├── examples/
│   ├── basic_usage.py          # Basic usage example
│   ├── zk_membership.py        # ZK membership example
│   └── benchmark.py            # Performance benchmarks
│
├── docs/
│   ├── ARCHITECTURE.md         # Architecture documentation
│   ├── CRYPTOGRAPHY.md         # Cryptographic protocols
│   ├── API.md                  # API reference
│   └── IMPLEMENTATION.md       # Implementation notes
│
└── scripts/
    ├── setup_keys.py           # Generate cryptographic keys
    └── benchmark.py            # Run benchmarks
```

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Git

### Step 1: Clone the Repository

```bash
git clone https://github.com/pranav-verma-daiict/Merkle_Tree_HE.git
cd Merkle_Tree_HE
```

### Step 2: Create Virtual Environment

```bash
# On macOS/Linux
python3 -m venv venv
source venv/bin/activate

# On Windows
python -m venv venv
venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
# Upgrade pip
pip install --upgrade pip

# Install required packages
pip install -r requirements.txt
```

### Step 4: Verify Installation

```bash
# Run tests
python -m pytest tests/ -v

# Or run a basic example
python examples/basic_usage.py
```

## Dependencies Explained

### Core Cryptography
- **tenseal** (0.3.14): Microsoft's Tensor Encrypted Approximate Logging - FHE library for encrypted computation
- **cryptography** (41.0.0): Low-level cryptographic primitives
- **pycryptodome** (3.19.0): Pure-Python implementation of cryptographic algorithms

### Zero-Knowledge Proofs
- **zksnark** (or custom implementation): For zero-knowledge proof protocols
- **gmpy2** (2.1.5): Multiple precision arithmetic (optimizes cryptographic operations)

### Utilities
- **numpy** (1.24.0): Numerical computing library
- **scipy** (1.11.0): Scientific computing tools

### Development & Testing
- **pytest** (7.4.0): Testing framework
- **pytest-cov** (4.1.0): Code coverage plugin
- **black** (23.7.0): Code formatter
- **flake8** (6.0.0): Code linter
- **mypy** (1.5.0): Static type checker

### Documentation
- **sphinx** (7.2.0): Documentation generator
- **sphinx-rtd-theme** (1.3.0): ReadTheDocs theme

## Configuration

### Environment Variables

Create a `.env` file based on `.env.example`:

```bash
cp .env.example .env
```

Edit `.env` with your settings:

```env
# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/merkle_tree_he.log

# Cryptography
KEY_SIZE=4096
SECURITY_LEVEL=128  # bits

# FHE Parameters
POLY_MODULUS_DEGREE=8192
COEFF_MODULUS=3
SCALE=2^40

# Merkle Tree
MAX_TREE_DEPTH=20
DETERMINISTIC_MODE=true
```

## Usage

### Basic Example

```python
from src.crypto.fhe_engine import FHEEngine
from src.merkle.tree import MerkleTreeHE

# Initialize FHE engine
fhe = FHEEngine()
fhe.setup()  # Generate keys

# Create encrypted Merkle tree
tree = MerkleTreeHE(fhe)

# Add encrypted items
data = [10, 20, 30, 40, 50]
for item in data:
    tree.add_encrypted_item(item)

# Get root
root = tree.get_root()
print(f"Merkle Root: {root}")

# Generate membership proof
proof = tree.generate_membership_proof(item=20, index=1)

# Verify membership
is_valid = tree.verify_membership(proof, root)
print(f"Membership Valid: {is_valid}")
```

### Zero-Knowledge Membership Query

```python
from src.zk_proof.protocols import ZKMembershipProof

# Generate ZK proof for membership
zk_prover = ZKMembershipProof(fhe, tree)
zk_proof = zk_prover.prove(plaintext=20, index=1)

# Verify without revealing plaintext
zk_verifier = ZKMembershipProof(fhe, tree)
is_valid = zk_verifier.verify(zk_proof, root)
print(f"ZK Proof Valid: {is_valid}")
```

For more examples, see the `examples/` directory.

## Development

### Running Tests

```bash
# Run all tests
python -m pytest tests/ -v

# Run with coverage
python -m pytest tests/ --cov=src --cov-report=html

# Run specific test file
python -m pytest tests/test_merkle_tree.py -v
```

### Code Quality

```bash
# Format code
black src/ tests/ examples/

# Lint code
flake8 src/ tests/ examples/

# Type checking
mypy src/
```

### Building Documentation

```bash
cd docs/
make html
# Open _build/html/index.html in browser
```

## Cryptographic Protocols

### 1. Deterministic Encryption
- Uses a seed-based encryption mode
- Same plaintext → Same ciphertext
- Trade-off: Reduced semantic security
- Use case: Merkle tree leaf consistency

### 2. Commitment Schemes
- Pedersen commitments for binding
- Hash-based commitments for simplicity
- Allows verification without revealing data

### 3. Zero-Knowledge Proofs
- Sigma protocols for membership
- Range proofs for value bounds
- Interactive and non-interactive variants

### 4. Homomorphic Hash Functions
- Compute hashes on encrypted data
- Maintain encryption throughout tree
- Based on lattice-based cryptography

See `docs/CRYPTOGRAPHY.md` for detailed protocols.

## Performance

### Benchmarks

Run performance benchmarks:

```bash
python scripts/benchmark.py
```

Expected metrics:
- Key generation: ~500ms
- Single item encryption: ~50ms
- Tree construction (1000 items): ~10s
- Membership proof generation: ~100ms
- Proof verification: ~50ms

## Troubleshooting

### Issue: TenSEAL Installation Fails

**Solution**: Pre-built wheels may not be available for your platform.

```bash
# Install from source
git clone https://github.com/microsoft/TenSEAL.git
cd TenSEAL
python setup.py install
```

### Issue: Memory Issues with Large Trees

**Solution**: Use batch processing or reduce tree size.

```python
# Process in batches
for batch in chunks(data, 100):
    tree.add_encrypted_items(batch)
```

### Issue: Slow Homomorphic Operations

**Solution**: Optimize FHE parameters or use GPU acceleration.

See `docs/IMPLEMENTATION.md` for optimization tips.

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit changes (`git commit -am 'Add feature'`)
4. Push to branch (`git push origin feature/your-feature`)
5. Open a Pull Request

Please ensure:
- Code passes all tests
- Code is formatted with Black
- Code passes Flake8 linting
- Type hints are included

## References

### Papers
1. "Merkle Trees Optimized for Stateless Clients" - Vitalik Buterin, 2021
2. "Zero-Knowledge Proofs: A Primer" - Zcash Blog
3. "Fully Homomorphic Encryption from LWE" - Brakerski et al., 2011
4. "Lattice Cryptography" - Chris Peikert, 2014

### Libraries & Resources
- [TenSEAL Documentation](https://github.com/microsoft/TenSEAL)
- [OpenFHE](https://github.com/openfheorg/openfhe-development)
- [Bulletproofs](https://github.com/dalek-cryptography/bulletproofs)

## License

MIT License - See LICENSE file for details

## Author

Pranav Verma - [@pranav-verma-daiict](https://github.com/pranav-verma-daiict)

## Disclaimer

⚠️ **This is a research project.** Not for production use without thorough security audits.

Use at your own risk. No guarantees about cryptographic security or correctness.
