# Algorithm Details

**Purpose**: Detailed explanations of detection algorithms and cryptographic methods used in Argus, including experimental findings from our research paper.

---

## Cryptographic Defense (Recommended)

### Ed25519 Digital Signatures

**Algorithm**: EdDSA (Edwards-curve Digital Signature Algorithm) on Curve25519

**Why Ed25519**:

- **Fast**: ~0.05ms signing, ~0.1ms verification per message
- **Secure**: 128-bit security level (requires O(2¹²⁸) operations to break)
- **Deterministic**: No random nonce needed (immune to nonce reuse attacks)
- **Small**: 32-byte keys, 64-byte signatures
- **Side-channel resistant**: Constant-time operations

**Security Guarantee**:

Based on the computational hardness of the discrete logarithm problem on Curve25519:

> **Theorem (Informal)**: Given a public key pk = [sk]G where G is the generator point and sk is the private key, computing sk from pk requires expected time O(2¹²⁸) using best-known algorithms (Pollard's rho).

**Consequence**: Phantom UAVs cannot forge valid signatures without the private key, enabling **perfect detection** with:

- TPR = 100% (all phantom/coordinated attacks detected)
- FPR = 0% (no false alarms)

### Detection Algorithm

```python
Algorithm: Cryptographic Detection
Input: Graph G(t), Public Key Database PKI
Output: Set of anomalous UAV IDs

Anomalous ← ∅
for each node v in V(G):
    msg ← latest_message(v)
    if msg.signature is NULL:
        Anomalous ← Anomalous ∪ {v}  # No signature
    elif v not in PKI:
        Anomalous ← Anomalous ∪ {v}  # Unknown UAV
    elif not Verify_Ed25519(msg, PKI[v]):
        Anomalous ← Anomalous ∪ {v}  # Invalid signature
return Anomalous
```

### Experimental Results

| Attack Type | TPR   | FPR   | F1    | Detection Time |
| ----------- | ----- | ----- | ----- | -------------- |
| Phantom     | 1.000 | 0.000 | 1.000 | 57.90ms        |
| Position    | 0.000 | 0.000 | 0.000 | 57.27ms        |
| Coordinated | 1.000 | 0.000 | 1.000 | 57.21ms        |

**Mobility Invariance**: Cryptographic detection maintains **zero FPR** regardless of UAV movement patterns (tested at 10 m/s).

### Limitations

- **Cannot detect position falsification**: Compromised UAVs with valid keys can sign false position data
- **Requires PKI infrastructure**: Public key distribution adds deployment complexity
- **30× computational overhead**: ~58ms vs ~2ms for spectral (still real-time)

**Reference**: Bernstein, D. J., et al. (2012). "High-speed high-security signatures"

---

## Graph-Theoretic Detection

### Spectral Analysis

**Based on**: Laplacian eigenvalue monitoring

**Theory**:

The graph Laplacian is defined as:

```
L = D - A
```

Where:

- `D` is the degree matrix (diagonal with node degrees)
- `A` is the adjacency matrix

Eigenvalues of the Laplacian (λ₁ ≤ λ₂ ≤ ... ≤ λₙ) reveal structural properties:

- λ₁ = 0 always (for connected graphs)
- λ₂ = **algebraic connectivity** (Fiedler value) - measures graph robustness
- Spectral gap (λₙ - λ₂) characterizes robustness against perturbations

### Detection Algorithm

```python
Algorithm: Spectral Detection
Input: Graph G(t), Baseline statistics (μ_λ, σ_λ)
Output: Set of anomalous UAV IDs

Compute Laplacian L = D - A
Compute eigenvalues λ₁ ≤ λ₂ ≤ ... ≤ λₙ
Compute eigenvectors u₁, u₂, ..., uₙ

# Algebraic connectivity check
z_AC ← |λ₂ - μ_λ₂| / σ_λ₂

# Per-node anomaly scoring
for each node v in V:
    score_degree ← z-score of degree(v)
    score_eigenvector ← residual in subspace projection
    score_position ← topology-position consistency

    combined_score ← 0.25×score_degree + 0.25×z_AC
                   + 0.20×score_eigenvector + 0.30×score_position

    if combined_score > threshold:
        flag v as anomalous
```

### Experimental Results

**Stationary Swarms**:

| Attack Type | TPR   | FPR   | F1    | Detection Time |
| ----------- | ----- | ----- | ----- | -------------- |
| Phantom     | 1.000 | 0.000 | 1.000 | 1.97ms         |
| Position    | 0.000 | 0.000 | 0.000 | 1.75ms         |
| Coordinated | 1.000 | 0.000 | 1.000 | 1.90ms         |

**Mobile Swarms (10 m/s)**:

| Attack Type | TPR   | FPR       | FPR Change |
| ----------- | ----- | --------- | ---------- |
| Phantom     | 99.2% | **62.5%** | +62.5%     |
| Position    | 1.9%  | 3.2%      | +3.2%      |
| Coordinated | 99.0% | **6.7%**  | +6.7%      |

### Critical Finding: Mobility Degradation

> **Spectral detection degrades significantly under mobility**. Movement-induced topology changes create false anomaly signals that spectral methods cannot distinguish from genuine attacks.

### Threshold Sensitivity

The spectral detector exhibits **extreme threshold sensitivity**:

| Threshold (τ) | TPR   | FPR   | F1    |
| ------------- | ----- | ----- | ----- |
| 2.0           | 1.000 | 0.267 | 0.600 |
| 2.5 (optimal) | 1.000 | 0.000 | 1.000 |
| 3.0           | 0.667 | 0.000 | 0.800 |
| 4.0           | 0.000 | 0.000 | 0.000 |

Threshold must be tuned for:

- Spatial domain size (affects graph density)
- Communication range (affects degree distribution)
- Swarm size (affects eigenvalue magnitudes)

**Reference**: Peel, L., et al. (2015). "Detecting Change Points in the Large-scale Structure of Evolving Networks"

---

### Centrality-Based Detection

**Metrics Used**:

1. **Degree Centrality**: `C_D(v) = deg(v) / (n-1)`
2. **Betweenness Centrality**: `C_B(v) = Σ(σ_st(v) / σ_st)`
3. **Closeness Centrality**: `C_C(v) = (n-1) / Σd(v,u)`

### Experimental Results

| Attack Type | TPR   | FPR       | F1    | Detection Time |
| ----------- | ----- | --------- | ----- | -------------- |
| Phantom     | 0.667 | **1.000** | 0.114 | 1.24ms         |
| Position    | 1.000 | **1.000** | 0.182 | 1.12ms         |
| Coordinated | 1.000 | **1.000** | 0.167 | 1.51ms         |

### ⚠️ Not Recommended

> **Centrality detection exhibits 100% false positive rate** across all attack types. This renders it **impractical for production deployment**.

The high FPR occurs because:

- Normal network dynamics create centrality variations
- Threshold tuning cannot eliminate false positives without sacrificing TPR
- Centrality metrics are too sensitive to natural topology changes

---

## Machine Learning Detection

### Node2Vec Graph Embeddings

**Algorithm**: Random walk-based graph embedding

**Process**:

1. Generate random walks starting from each node
2. Treat walks as "sentences" and nodes as "words"
3. Train Word2Vec to learn embeddings
4. Use embeddings as features for Isolation Forest

**Feature Vector**:

```
f(v) = [C_D(v), C_B(v), C_clustering(v), C_C(v)]
```

### Isolation Forest

**Intuition**: Anomalies are "few and different" - easier to isolate in decision trees.

**Parameters**:

- `n_estimators`: 100-200 trees
- `contamination`: 0.15 (expects 15% anomalies)

### Experimental Results

| Attack Type | TPR   | FPR       | F1    | Detection Time |
| ----------- | ----- | --------- | ----- | -------------- |
| Phantom     | 0.333 | **0.933** | 0.062 | 4.88ms         |
| Position    | 0.667 | **0.963** | 0.129 | 4.63ms         |
| Coordinated | 1.000 | **0.867** | 0.188 | 5.11ms         |

### ⚠️ Not Recommended

> **ML detection exhibits 87-97% false positive rate** - unsuitable for production deployment.

**Root Cause Analysis**:

1. **Contamination mismatch**: Initial parameter expected 5% anomalies while actual attack density reached ~9%
2. **Limited features**: 4D feature vector captures insufficient topological information
3. **Overfitting**: Trained on only 30 baseline graphs

**Future Work**: Consider Graph Neural Networks (GNN) for richer feature learning.

**References**:

- Grover, A., & Leskovec, J. (2016). "node2vec: Scalable Feature Learning for Networks"
- Liu, F. T., et al. (2008). "Isolation Forest"

---

## Position Falsification: An Open Problem

### Why All Methods Fail

Position falsification is **fundamentally undetectable** by graph-based methods when the falsified position preserves communication topology:

```
If ∥δ∥ < r_comm:
    G(p') = G(p)  →  L(p') = L(p)
```

Since spectral eigenvalues depend only on graph structure (not node positions), position falsification is **topologically invisible**.

### Cryptographic Limitation

Valid signatures only prove:

- **Message authenticity** (sender identity)
- **Data integrity** (message not tampered)

They do NOT prove **data truthfulness**. A compromised UAV can sign false position data with its legitimate private key.

### Mitigation Strategies (Future Work)

1. **Multi-lateration**: Verify reported positions against distance measurements from neighboring UAVs
2. **Physics-based validation**: Detect impossible velocities or accelerations
3. **Byzantine consensus**: Require agreement from ⌊n/3⌋ + 1 UAVs before accepting position claims

---

## Attack Models

### Phantom UAV Injection (A₁)

```python
# At time t_attack:
V(t_attack) ← V(t_attack) ∪ {phantom_1, ..., phantom_k}
# Phantom UAVs lack valid cryptographic credentials
```

**Parameters**: k = 3 phantom UAVs, randomly positioned within communication range

### Position Falsification (A₂)

```python
# For compromised UAV i:
p'_i(t) = p_i(t) + δ_i
# Where ∥δ_i∥ ≤ M_max (100m in experiments)
```

**Parameters**: m = 4 compromised UAVs (~13% of swarm)

### Coordinated Attack (A₃)

```python
# Circular formation:
for i in range(phantom_count):
    angle = 2π × i / phantom_count
    position = center + (radius × cos(angle), radius × sin(angle), 0)
```

**Parameters**: k = 5 phantoms in circular formation (radius = 50m)

---

## Consensus Algorithm

### Average Consensus

**Update Rule**:

```
x_i(t+1) = x_i(t) + ε × Σ_{j∈N_i} (x_j(t) - x_i(t))
```

Where:

- `x_i(t)` = state of UAV i at time t
- `N_i` = neighbors of UAV i (within comm range)
- `ε` = step size (typically `1 / max_degree`)

**Convergence**: If graph is connected, converges to x̄ = (1/n)Σx_i(0)

**Attack Impact**:

- Phantom UAVs inject false values
- Pulls consensus away from true average
- Crypto defense rejects phantom values → normal convergence

**Reference**: Olfati-Saber, R., & Murray, R. M. (2004). "Consensus Problems in Networks of Agents"

---

## Computational Complexity

| Operation                | Complexity            | Time (n=30) |
| ------------------------ | --------------------- | ----------- |
| Graph update             | O(n²)                 | ~0.5ms      |
| Laplacian eigenvalues    | O(n³)                 | ~1.9ms      |
| Centrality (betweenness) | O(n³)                 | ~1.3ms      |
| Ed25519 sign             | O(1)                  | ~0.05ms     |
| Ed25519 verify           | O(1)                  | ~0.1ms      |
| Node2Vec                 | O(n × walks × length) | ~5ms        |

### Scalability

**Cryptographic** (O(n)): Scales linearly, parallelizable verification

**Graph Methods** (O(n²) - O(n³)): Works well to n=100-200 UAVs

---

## Summary: Method Comparison

| Method     | Phantom/Coordinated  | Position         | Mobility      | Recommendation  |
| ---------- | -------------------- | ---------------- | ------------- | --------------- |
| **Crypto** | ✅ Perfect (F1=1.0)  | ❌ Cannot detect | ✅ Invariant  | **MANDATORY**   |
| Spectral   | ✅ Good (F1=1.0)     | ❌ Cannot detect | ⚠️ Degrades   | Supplementary   |
| Centrality | ❌ High FPR (100%)   | ❌ High FPR      | ❌ Unreliable | Not recommended |
| ML         | ❌ High FPR (87-97%) | ❌ High FPR      | ❌ Unreliable | Not recommended |

**Conclusion**: For security-critical UAV applications, **cryptographic authentication is mandatory**. Graph-based methods may supplement but cannot replace cryptographic security.
