# Argus Project Status

**UAV Remote ID Spoofing: Graph-Theoretic Modeling and Cryptographic Defenses**

**Date**: December 2025  
**Version**: 0.2.0

---

## 🎯 Quick Summary

✅ **All phases complete**  
✅ **4 detection methods** implemented (Spectral, Centrality, ML, Crypto)  
✅ **3 attack types** working (Phantom, Position, Coordinated)  
✅ **Cryptographic authentication** achieves **100% TPR, 0% FPR**  
✅ **Live visualization** with real-time animation  
✅ **Consensus algorithms** implemented  
✅ **Publication-ready** with research paper

---

## 📊 Detection Performance Results

### Stationary Swarms (30 UAVs, 200m comm range)

Results from experimental evaluation in the research paper:

| Attack Type     | Detector   | TPR       | FPR       | Precision | F1        | Time (ms) |
| --------------- | ---------- | --------- | --------- | --------- | --------- | --------- |
| **Phantom**     | Spectral   | 1.000     | 0.000     | 1.000     | 1.000     | 1.97      |
|                 | Centrality | 0.667     | 1.000     | 0.062     | 0.114     | 1.24      |
|                 | **Crypto** | **1.000** | **0.000** | **1.000** | **1.000** | 57.90     |
|                 | ML         | 0.333     | 0.933     | 0.034     | 0.062     | 4.88      |
| **Position**    | Spectral   | 0.000     | 0.000     | 0.000     | 0.000     | 1.75      |
|                 | Centrality | 1.000     | 1.000     | 0.100     | 0.182     | 1.12      |
|                 | **Crypto** | **0.000** | **0.000** | **0.000** | **0.000** | 57.27     |
|                 | ML         | 0.667     | 0.963     | 0.071     | 0.129     | 4.63      |
| **Coordinated** | Spectral   | 1.000     | 0.000     | 1.000     | 1.000     | 1.90      |
|                 | Centrality | 1.000     | 1.000     | 0.091     | 0.167     | 1.51      |
|                 | **Crypto** | **1.000** | **0.000** | **1.000** | **1.000** | 57.21     |
|                 | ML         | 1.000     | 0.867     | 0.103     | 0.188     | 5.11      |

### Mobility Impact (10 m/s UAV movement)

| Attack      | Detector   | Stationary (TPR/FPR) | Mobile (TPR/FPR) | FPR Change |
| ----------- | ---------- | -------------------- | ---------------- | ---------- |
| Phantom     | Spectral   | 100%/0%              | 99.2%/62.5%      | **+62.5%** |
|             | **Crypto** | **100%/0%**          | **100%/0%**      | **0%**     |
| Position    | Spectral   | 0%/0%                | 1.9%/3.2%        | +3.2%      |
|             | **Crypto** | **0%/0%**            | **0%/0%**        | **0%**     |
| Coordinated | Spectral   | 98.5%/0%             | 99.0%/6.7%       | +6.7%      |
|             | **Crypto** | **100%/0%**          | **100%/0%**      | **0%**     |

### Key Findings

1. **Cryptographic detection** achieves **perfect performance** (100% TPR, 0% FPR) for phantom and coordinated attacks across all mobility scenarios

2. **Spectral detection** works well for stationary swarms but **degrades under mobility** (FPR increases up to 62.5%)

3. **Centrality and ML detectors** exhibit **unacceptable false positive rates** (87-100%) - not recommended for production

4. **Position falsification is fundamentally undetectable** by all methods (topology-preserving attack)

5. **Computational overhead**: ~58ms for crypto vs ~2ms for spectral (30× slower but still real-time)

---

## 🚀 System Capabilities

### Simulation

- ✅ 20-30 UAV swarms (validated in paper)
- ✅ Dynamic graph topology (NetworkX)
- ✅ Configurable parameters (comm range, bounds, frequency)
- ✅ Reproducible experiments (fixed random seeds)
- ✅ Ed25519 cryptographic keys

### Attack Injection

- ✅ **Phantom UAVs** - Inject 3+ fake nodes
- ✅ **Position Falsification** - GPS spoofing (~13% compromised)
- ✅ **Coordinated Attacks** - 5 phantoms in circular formation
- ✅ Ground truth tracking
- ✅ Temporal control (start time, duration)

### Detection Methods

| Method               | Recommendation                  | Use Case                                     |
| -------------------- | ------------------------------- | -------------------------------------------- |
| 🔐 **Cryptographic** | ✅ **MANDATORY** for production | Perfect detection of phantom/coordinated     |
| 📊 **Spectral**      | ⚠️ Supplementary only           | Fast monitoring (~2ms), stationary scenarios |
| 🎯 **Centrality**    | ❌ Not recommended              | High FPR (87-100%)                           |
| 🤖 **ML (Node2Vec)** | ❌ Not recommended              | High FPR (87-97%)                            |

### Consensus & Coordination

- ✅ Average consensus algorithm
- ✅ Attack impact quantification
- ✅ Defense effectiveness measurement
- ✅ Convergence analysis

### Visualization

- ✅ ROC curves (individual + comparison)
- ✅ Detection comparison bar charts
- ✅ Performance scatter plots
- ✅ Confusion matrices
- ✅ Metrics heatmaps
- ✅ **Live real-time animation** (PySide6/Qt6)
- ✅ 300 DPI PNG + vector PDF

---

## 📈 Computational Overhead

| Detector   | Mean (ms) | Std Dev (ms) | Overhead vs Spectral |
| ---------- | --------- | ------------ | -------------------- |
| Spectral   | 1.87      | 0.12         | 1.0×                 |
| Centrality | 1.29      | 0.17         | 0.7×                 |
| **Crypto** | **57.46** | **2.31**     | **30.7×**            |
| ML         | 4.87      | 0.51         | 2.6×                 |

**Trade-off**: Pay ~56ms additional latency for **100% security guarantee** versus probabilistic heuristics.

For 30 UAVs at 1 Hz broadcast rate: 58ms per detection cycle is well within real-time constraints (<1000ms budget).

---

## 📦 Project Deliverables

### Source Code (~3,500 LOC)

- Core simulation modules
- 4 detection method implementations
- 3 attack injection modules
- Interactive CLI tool (`argus` command)
- Live visualization system

### Documentation

- Complete README with installation
- Quickstart guide
- Algorithm details with theory
- Data format specifications
- Research paper citations
- CLI user guide

### Research Paper

- IEEE conference format
- Comprehensive experimental evaluation
- Reproducibility statement
- Open-source framework

---

## 🎓 Research Contributions

### Questions Answered

✅ **Can graph-theoretic metrics detect topological anomalies from phantom UAVs?**  
Yes - Spectral achieves 100% TPR in stationary scenarios

✅ **How effective is ML (Node2Vec + Isolation Forests) vs pure graph analysis?**  
ML has unacceptably high FPR (87-97%) - not recommended

✅ **What is the performance overhead of Ed25519 cryptographic signing?**  
~58ms detection latency (30× overhead) - acceptable for real-time

✅ **How do spoofing attacks impact swarm consensus algorithms?**  
Phantoms disrupt consensus; crypto defense restores baseline

### Novel Contributions

1. **First systematic evaluation** comparing cryptographic and graph-based detection for UAV spoofing
2. **Mobility impact quantification** - crypto invariant, heuristics degrade
3. **Threshold scaling analysis** for graph-based detectors
4. **Open-source framework** (Argus) enabling reproducible research

---

## 🚀 Quick Usage

### Interactive CLI (Recommended)

```bash
# Interactive mode with guided prompts
argus

# Quick command-line usage
argus --attack phantom --detectors all --mode comparison
argus --attack coordinated --detectors spectral crypto --mode live
argus --attack position --detectors all --mode both

# Custom swarm configuration
argus --attack phantom --detectors all --mode comparison \
    --num-uavs 30 --comm-range 200
```

### Reproduce Paper Results

```bash
git clone https://github.com/Sang-Buster/Argus
cd Argus
uv sync
uv run argus --attack phantom --detectors all --mode comparison --num-uavs 30
```

Expected: Crypto detector shows TPR=1.000, FPR=0.000, F1=1.000

---

## 🎯 Recommendations

### For Production UAV Systems

**Cryptographic authentication is MANDATORY.**

- Deploy Ed25519 signatures on all legitimate UAVs
- Reject unsigned/invalid messages at receiver
- Accept ~58ms detection latency for provable security

### For Research/Monitoring

- Use spectral detection as **supplementary** fast alerting
- Do NOT rely on centrality or ML for security-critical decisions
- Consider mobility-aware threshold adaptation for graph methods

### For Position Falsification

Position attacks remain an **open problem**. Consider:

- Multi-lateration with signal strength measurements
- Physics-based trajectory validation
- Byzantine consensus protocols

---

## 📁 Project Structure

```
Argus/
├── README.md              # Main documentation
├── src/argus_uav/         # Package source code
├── tests/                 # Unit and integration tests
├── examples/              # Demonstration scripts
├── docs/                  # Documentation files
└── results/               # Experiment outputs
```

---

**Last Updated**: December 2025  
**Project Version**: 1.0.0  
**Paper**: "Cryptographic Authentication for UAV Swarm Security"
