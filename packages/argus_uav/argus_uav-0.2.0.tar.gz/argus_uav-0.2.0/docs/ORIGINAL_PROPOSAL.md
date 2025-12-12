# UAV Remote ID Spoofing: Graph-Theoretic Modeling and Cryptographic Defenses

Sang Xing (solo)

## Project Description

This project investigates UAV swarm vulnerabilities to Remote ID spoofing attacks and explores graph-theoretic modeling combined with cryptographic defenses as countermeasures. Remote ID is a mandated standard for UAV identification, but it is susceptible to falsified messages (phantom UAVs, spoofed positions). In swarm operations, such spoofing can mislead consensus, disrupt connectivity, and enable malicious control. We will simulate UAV swarms as dynamic graphs, implement spoofing attacks, and evaluate detection using spectral methods and anomaly detection. We will also prototype lightweight cryptographic signing (Ed25519) to validate Remote ID authenticity and compare its effectiveness against graph-only defenses.

## Programming Language

- Python 3 - for simulation, graph analysis, cryptography, and anomaly detection.
- Possible Libraries: networkx, numpy, scikit-learn, pycryptodome, matplotlib.

## Hardware + Software List

- Laptop/PC for all simulations and analysis.
- Optional: Raspberry Pi with RTL-SDR receiver (for simulated or controlled Remote ID traffic).
- Software: Python packages listed above; GitHub code bases (Remote ID spoofers) for generating attack data in simulation.

## Project Timeline

- Week 1 (current):
- Set up GitHub repo, Python environment, and dependencies (networkx, pycryptodome, scikit-learn).
- Review background literature on UAV Remote ID and spoofing attacks.
- Week 2:
- Build basic swarm simulator (graph model with UAV nodes, edges by comm range).

- Implement Remote ID message format (fields for ID, position, timestamp).
- Week 3:
- Implement spoofing attack scenarios:
- Phantom UAV injection
- Position falsification
- Multiple coordinated spoofers
- Generate initial attack datasets.
- Week 4:
- Implement graph-theoretic metrics: centrality, connectivity, community structure.
- Begin spectral anomaly detection (Laplacian eigenvalue monitoring).
- Week 5:
- Implement machine learning anomaly detection (Node2Vec embeddings + isolation forest).
- Evaluate on spoofed vs clean datasets.
- Week 6:
- Prototype cryptographic defense: Ed25519 signing of Remote ID messages.
- Integrate into simulator; test verification times and message overhead.
- Week 7:
- Run combined experiments: graph-based detection vs crypto signing vs hybrid approach.
- Measure TPR, FPR, detection latency, and computational overhead.
- Week 8:
- Study swarm consensus under spoofing (e.g., average consensus algorithm).
- Quantify consensus error and resilience improvements with crypto + detection.
- Week 9:
- Finalize results: produce figures, graphs, and quantitative tables.
- Draft full project report, including methodology, results, and discussion.
- Week 10:
- Polish code repo with documentation.
- Prepare presentation slides and demo video.
- Submit final report and present findings.

# Expected Deliverables

- Python-based UAV swarm and Remote ID spoofing simulator.
- Graph-theoretic analysis and detection methods (spectral anomaly, Node2Vec embeddings).
- Cryptographic signing prototype with performance benchmarks.
- Final written report and demo with plots showing spoof detection accuracy and resilience.

## Risks / Open Questions

- Limited access to physical hardware (RTL-SDR/UAV boards) may restrict real-world testing.
- Crypto defenses may introduce latency/overhead in swarm messaging — scalability trade-offs need evaluation.

# Possible Extensions

- Explore threshold/group signatures for swarm consensus.
- Apply GNN-based graph anomaly detection to spoofed networks.
- Study hybrid defense (cryptographic signing + graph anomaly monitoring) for layered resilience.
