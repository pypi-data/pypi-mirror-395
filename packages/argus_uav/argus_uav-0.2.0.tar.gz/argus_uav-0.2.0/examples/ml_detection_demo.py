#!/usr/bin/env python3
"""
Machine Learning detection demonstration using Node2Vec + Isolation Forest.

Shows advanced ML-based anomaly detection compared to graph-only methods.
"""

import numpy as np

from argus_uav.attacks import AttackScenario, AttackType
from argus_uav.attacks.phantom_uav import PhantomInjector
from argus_uav.core.swarm import Swarm
from argus_uav.detection.centrality import CentralityDetector
from argus_uav.detection.ml_detection import Node2VecDetector
from argus_uav.detection.spectral import SpectralDetector


def main():
    """Demonstrate Node2Vec ML detection."""
    print("\n" + "=" * 70)
    print("🤖 MACHINE LEARNING DETECTION DEMONSTRATION")
    print("   Node2Vec Embeddings + Isolation Forest")
    print("=" * 70)

    # Create swarm
    print("\n📍 Step 1: Initialize swarm...")
    rng = np.random.default_rng(seed=42)
    swarm = Swarm(num_uavs=30, comm_range=200.0, bounds=(500, 500, 100), rng=rng)

    # Collect baseline
    print("\n🧠 Step 2: Collect baseline (this may take a moment)...")
    baseline_graphs = []
    for t in range(20):
        swarm.step(dt=1.0)
        baseline_graphs.append(swarm.get_graph().copy())

    print(f"   ✓ Baseline collected: {len(baseline_graphs)} snapshots")

    # Train all detectors
    print("\n🎓 Step 3: Train detectors (ML training takes longer)...")

    spectral = SpectralDetector(threshold=1.0)
    centrality = CentralityDetector(threshold=0.9)
    ml_detector = Node2VecDetector(
        embedding_dim=64,  # Smaller for speed
        walk_length=20,
        num_walks=100,
        contamination=0.15,
    )

    print("   Training Spectral...")
    spectral.train(baseline_graphs)
    print("   ✓ Spectral trained")

    print("   Training Centrality...")
    centrality.train(baseline_graphs)
    print("   ✓ Centrality trained")

    print("   Training Node2Vec (this takes ~30-60 seconds)...")
    ml_detector.train(baseline_graphs)
    print("   ✓ Node2Vec trained")

    # Inject attack
    print("\n⚠️  Step 4: Inject phantom attack...")
    attack = AttackScenario(
        attack_type=AttackType.PHANTOM, start_time=0.0, duration=10.0, phantom_count=5
    )

    injector = PhantomInjector()
    injector.inject(swarm, attack, 0.0)

    print(f"   ✓ 5 phantoms injected, total {len(swarm.uavs)} UAVs")

    # Run detection
    print("\n🔍 Step 5: Run all detection methods...")
    swarm.step(dt=1.0)
    current_graph = swarm.get_graph()

    print("   Running Spectral...")
    spectral_result = spectral.detect(current_graph)
    spectral_metrics = spectral_result.compute_metrics()

    print("   Running Centrality...")
    centrality_result = centrality.detect(current_graph)
    centrality_metrics = centrality_result.compute_metrics()

    print("   Running Node2Vec (generates new embeddings)...")
    ml_result = ml_detector.detect(current_graph)
    ml_metrics = ml_result.compute_metrics()

    # Display results
    print("\n" + "=" * 70)
    print("📊 DETECTION RESULTS COMPARISON")
    print("=" * 70)

    print(
        f"\n{'Method':<20} {'Flagged':>10} {'TPR':>8} {'FPR':>8} {'F1':>8} {'Time(ms)':>10}"
    )
    print("-" * 70)

    for name, result, metrics in [
        ("Spectral", spectral_result, spectral_metrics),
        ("Centrality", centrality_result, centrality_metrics),
        ("Node2Vec ML", ml_result, ml_metrics),
    ]:
        print(
            f"{name:<20} {len(result.anomalous_uav_ids):>10} "
            f"{metrics['tpr']:>7.2%} {metrics['fpr']:>7.2%} "
            f"{metrics['f1']:>8.3f} {metrics['detection_time'] * 1000:>9.2f}"
        )

    # Detailed metrics
    print("\n" + "=" * 70)
    print("DETAILED METRICS")
    print("=" * 70)

    for name, metrics in [
        ("Spectral", spectral_metrics),
        ("Centrality", centrality_metrics),
        ("Node2Vec ML", ml_metrics),
    ]:
        print(f"\n{name}:")
        print(f"  • True Positive Rate:  {metrics['tpr']:.2%}")
        print(f"  • False Positive Rate: {metrics['fpr']:.2%}")
        print(f"  • Precision: {metrics['precision']:.2%}")
        print(f"  • Recall:    {metrics['recall']:.2%}")
        print(f"  • F1 Score:  {metrics['f1']:.3f}")
        print(f"  • Detection time: {metrics['detection_time'] * 1000:.2f}ms")
        print(
            f"  • Confusion: TP={metrics['tp']}, FP={metrics['fp']}, "
            f"TN={metrics['tn']}, FN={metrics['fn']}"
        )

    # Identify best
    best_f1 = max(spectral_metrics["f1"], centrality_metrics["f1"], ml_metrics["f1"])

    if ml_metrics["f1"] == best_f1:
        print(f"\n🏆 Node2Vec ML achieves best F1 score: {best_f1:.3f}")
    elif (
        ml_metrics["f1"] > spectral_metrics["f1"]
        and ml_metrics["f1"] > centrality_metrics["f1"]
    ):
        print(
            f"\n✓ Node2Vec ML outperforms graph-only methods (F1={ml_metrics['f1']:.3f})"
        )
    else:
        print(
            f"\n○ Node2Vec ML: F1={ml_metrics['f1']:.3f} "
            f"(vs Spectral={spectral_metrics['f1']:.3f}, Centrality={centrality_metrics['f1']:.3f})"
        )

    print("\n" + "=" * 70)
    print("✅ ML detection demonstration complete!")
    print("=" * 70)
    print("\nKey Findings:")
    print("  • ML detection takes longer (~seconds vs milliseconds)")
    print("  • But may provide better accuracy for complex patterns")
    print("  • Trade-off: accuracy vs real-time performance")
    print()


if __name__ == "__main__":
    main()
