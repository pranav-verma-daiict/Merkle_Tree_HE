# Cryptographic Protocols

## Overview

This document details the cryptographic protocols used in the Merkle Tree HE system.

## 1. Fully Homomorphic Encryption (FHE)

### Scheme: BFV (Brakerski-Fan-Vercauteren)

Used via TenSEAL library.

### Parameters
- Polynomial modulus degree: 8192 (configurable)
- Coefficient modulus: Multiple-bit precision
- Scale: 2^40 for fixed-point arithmetic

### Operations

#### Encryption
```
E(m) = (c0, c1)
where m is plaintext, c0 and c1 are ciphertext components
```

#### Decryption
```
m = D(c) = [c0 + c1 * s] mod q
where s is secret key
```

#### Homomorphic Addition
```
E(m1 + m2) = E(m1) + E(m2)
```

#### Homomorphic Multiplication
```
E(m1 * m2) = E(m1) * E(m2)
```

### Security
- Based on Learning With Errors (LWE) problem
- Security level: ~128 bits for typical parameters
- Semantic security: IND-CPA secure

## 2. Commitment Schemes

### Pedersen Commitment

#### Setup
```
Choose random generator g of order p
p is a prime
```

#### Commit
```
C(m, r) = H(m || r)
where:
  m = message (plaintext)
  r = random value (randomness)
  H = hash function
  || = concatenation
```

#### Verify
```
C' = H(m' || r')
Valid if C' == C
```

### Properties
- **Binding**: Cannot find (m, r) and (m', r') such that C(m,r) = C(m',r') with m ≠ m'
- **Hiding**: No information about m is leaked from C(m, r)
- **Efficient**: Fast computation using cryptographic hash

## 3. Merkle Tree Construction

### Hash Function
```
H: {0,1}* → {0,1}^256
```
Using SHA-256 by default.

### Leaf Node Hash
```
hash_leaf = H(commitment)
```

### Internal Node Hash
```
hash_parent = H(hash_left || hash_right)
```

### Tree Structure
```
              root_hash
             /          \
        left_hash      right_hash
        /      \        /        \
      h1      h2      h3        h4
      |       |       |         |
      leaf1   leaf2   leaf3     leaf4
```

### Properties
- **Deterministic**: Same input always produces same output
- **Collision Resistant**: Infeasible to find two different inputs with same hash
- **One-way**: Cannot reverse hash to get original value

## 4. Merkle Proof (Membership Proof)

### Proof Generation
For leaf at index i:
```
1. Start at leaf_i
2. Get sibling hash
3. Move to parent
4. Repeat until reaching root

Proof = [sibling_1, sibling_2, ..., sibling_log(n)]
with directions: [right, left, ...]
```

### Proof Verification
```
1. Start with leaf_hash
2. For each (sibling, direction) in proof:
   if direction == right:
       current = H(current || sibling)
   else:
       current = H(sibling || current)
3. Check if current == root_hash
```

### Complexity
- Proof generation: O(log n) hashes
- Proof size: O(log n) hash values
- Verification: O(log n) hashes
- where n = number of leaves

## 5. Zero-Knowledge Membership Proof

### Protocol Overview

#### Prover's Goal
Prove: "I know a plaintext m such that:
1. m is a member of the encrypted set
2. The commitment to m exists in the Merkle tree"

Without revealing m.

#### Proof Structure
```
ZK_Proof = {
  challenge: random value,
  commitment: C(m, r),
  index: position in tree,
  merkle_proof: proof that commitment is in tree,
  randomness_hash: H(r)
}
```

#### Verification Steps
```
1. Check if commitment exists at index in tree
2. If so, verify merkle_proof(commitment) leads to root
3. If both checks pass, membership is proven
```

### Security Properties

#### Completeness
```
If m is a member, prover can always generate valid proof
with probability 1
```

#### Soundness
```
If m is not a member, prover can generate valid proof
with probability at most 1/2^256 (negligible)
```

#### Zero-Knowledge
```
Verifier learns nothing except that m is in the set
No information about m, r, or other members is leaked
```

## 6. Key Generation

### FHE Key Generation
```
1. Sample error polynomials from distribution
2. Generate secret key s = polynomial of error
3. Compute public key from s and random polynomial
4. Generate evaluation keys for Galois operations
5. Generate relinearization keys for multiplication
```

### Security Assumption
Based on Ring Learning With Errors (RLWE):
```
Given (a_i, b_i = a_i * s + e_i) for random a_i,
it is hard to recover s when e_i is small.
```

## 7. Hash Function Properties

### Requirements
1. **Deterministic**: Same input → same output
2. **Quick**: Fast to compute
3. **One-way**: Infeasible to reverse
4. **Avalanche effect**: Small input change → large output change
5. **Collision resistant**: Hard to find same-hash inputs

### Used Algorithm: SHA-256
- Output: 256 bits (32 bytes)
- Security: Collision resistance up to 2^128 operations
- Standardized: FIPS 180-4

## 8. Security Analysis

### Assumptions
1. **FHE Security**: BFV is semantically secure under RLWE
2. **Hash Security**: SHA-256 is collision resistant
3. **Commitment Security**: Hashing is one-way

### Attack Resistance

#### Ciphertext Attack
- **Resistant**: FHE prevents plaintext recovery
- **Resistant**: Ciphertexts are computationally indistinguishable

#### Membership Attack
- **Resistant**: Cannot forge Merkle proofs (hash collision resistance)
- **Resistant**: Cannot modify proof (verification fails)

#### ZK Proof Attack
- **Resistant**: Cannot reuse proofs (different challenges each time)
- **Resistant**: Cannot fake membership (soundness property)

## 9. Practical Considerations

### Parameter Selection
- Larger polynomials = higher security, slower computation
- Recommended minimum: poly_modulus_degree = 8192
- Security level: ~128 bits with standard parameters

### Efficiency
- FHE operations: 10-100ms per operation
- Merkle tree: Construction ~O(n) where n = tree size
- Proofs: Verification ~1-10ms depending on depth

### Batch Operations
- TenSEAL supports SIMD-style batching
- Multiple values encrypted in single ciphertext
- Reduces computation overhead

## References

1. "Fully Homomorphic Encryption from LWE" - Brakerski et al., 2011
2. "Encrypted Search" - Bost et al., 2014
3. "Pedersen Commitments" - Pedersen, 1991
4. "FIPS 180-4: Secure Hash Standard"
5. "TenSEAL: A Library for Encrypted Tensor Operations" - Microsoft
