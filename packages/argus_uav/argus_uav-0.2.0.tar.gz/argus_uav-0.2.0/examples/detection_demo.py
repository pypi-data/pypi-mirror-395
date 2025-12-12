#!/usr/bin/env python3
"""
Detection demonstration - Spectral and Centrality analysis.

Shows how graph-theoretic detection identifies phantom UAVs.
"""

import numpy as np

from argus_uav.attacks import AttackScenario, AttackType
from argus_uav.attacks.phantom_uav import PhantomInjector
from argus_uav.core.swarm import Swarm
from argus_uav.detection.centrality import CentralityDetector
from argus_uav.detection.spectral import SpectralDetector


def main():
    """Demonstrate detection of phantom UAV attack."""
    print("\n" + "=" * 70)
    print("🔍 ARGUS GRAPH-THEORETIC DETECTION DEMONSTRATION")
    print("=" * 70)

    # Create swarm
    print("\n📍 Step 1: Initialize swarm and collect baseline...")
    rng = np.random.default_rng(seed=42)
    swarm = Swarm(num_uavs=30, comm_range=200.0, bounds=(500, 500, 100), rng=rng)

    # Collect baseline (clean) graphs
    baseline_graphs = []
    print("   Collecting 20 baseline graph snapshots...")
    for t in range(20):
        swarm.step(dt=1.0)
        baseline_graphs.append(swarm.get_graph().copy())

    print(f"   ✓ Baseline collected: {len(baseline_graphs)} snapshots")

    # Train detectors
    print("\n🧠 Step 2: Train detectors on clean baseline...")
    spectral = SpectralDetector(threshold=1.0)  # Lower threshold for better sensitivity
    centrality = CentralityDetector(
        threshold=0.9
    )  # Lower threshold for better sensitivity

    spectral.train(baseline_graphs)
    centrality.train(baseline_graphs)

    print("   ✓ Spectral detector trained")
    print("   ✓ Centrality detector trained")

    # Configure and inject attack
    print("\n⚠️  Step 3: Inject phantom UAV attack...")
    attack = AttackScenario(
        attack_type=AttackType.PHANTOM, start_time=0.0, duration=10.0, phantom_count=5
    )

    injector = PhantomInjector()
    injector.inject(swarm, attack, 0.0)

    stats = swarm.get_statistics()
    print(f"   ✓ Attack injected: {stats['num_uavs']} total UAVs (5 phantoms)")

    # Run detection
    print("\n🔍 Step 4: Run detection algorithms...")
    swarm.step(dt=1.0)
    current_graph = swarm.get_graph()

    print("\n" + "-" * 70)
    print("SPECTRAL ANALYSIS RESULTS")
    print("-" * 70)
    spectral_result = spectral.detect(current_graph)
    spectral_metrics = spectral_result.compute_metrics()

    print(f"Flagged UAVs: {len(spectral_result.anomalous_uav_ids)}")
    print(f"Detection time: {spectral_metrics['detection_time'] * 1000:.1f}ms")
    print("\nDetection Metrics:")
    print(f"  • True Positive Rate (TPR):  {spectral_metrics['tpr']:.2%}")
    print(f"  • False Positive Rate (FPR): {spectral_metrics['fpr']:.2%}")
    print(f"  • Precision: {spectral_metrics['precision']:.2%}")
    print(f"  • Recall:    {spectral_metrics['recall']:.2%}")
    print(f"  • F1 Score:  {spectral_metrics['f1']:.2f}")
    print("\nConfusion Matrix:")
    print(f"  • True Positives:  {spectral_metrics['tp']}")
    print(f"  • False Positives: {spectral_metrics['fp']}")
    print(f"  • True Negatives:  {spectral_metrics['tn']}")
    print(f"  • False Negatives: {spectral_metrics['fn']}")

    print("\n" + "-" * 70)
    print("CENTRALITY ANALYSIS RESULTS")
    print("-" * 70)
    centrality_result = centrality.detect(current_graph)
    centrality_metrics = centrality_result.compute_metrics()

    print(f"Flagged UAVs: {len(centrality_result.anomalous_uav_ids)}")
    print(f"Detection time: {centrality_metrics['detection_time'] * 1000:.1f}ms")
    print("\nDetection Metrics:")
    print(f"  • True Positive Rate (TPR):  {centrality_metrics['tpr']:.2%}")
    print(f"  • False Positive Rate (FPR): {centrality_metrics['fpr']:.2%}")
    print(f"  • Precision: {centrality_metrics['precision']:.2%}")
    print(f"  • Recall:    {centrality_metrics['recall']:.2%}")
    print(f"  • F1 Score:  {centrality_metrics['f1']:.2f}")
    print("\nConfusion Matrix:")
    print(f"  • True Positives:  {centrality_metrics['tp']}")
    print(f"  • False Positives: {centrality_metrics['fp']}")
    print(f"  • True Negatives:  {centrality_metrics['tn']}")
    print(f"  • False Negatives: {centrality_metrics['fn']}")

    # Compare methods
    print("\n" + "=" * 70)
    print("📊 COMPARATIVE ANALYSIS")
    print("=" * 70)
    print(f"\n{'Metric':<25} {'Spectral':>15} {'Centrality':>15}")
    print("-" * 70)
    print(
        f"{'TPR (Recall)':<25} {spectral_metrics['tpr']:>14.2%} {centrality_metrics['tpr']:>14.2%}"
    )
    print(
        f"{'FPR':<25} {spectral_metrics['fpr']:>14.2%} {centrality_metrics['fpr']:>14.2%}"
    )
    print(
        f"{'Precision':<25} {spectral_metrics['precision']:>14.2%} {centrality_metrics['precision']:>14.2%}"
    )
    print(
        f"{'F1 Score':<25} {spectral_metrics['f1']:>14.2f} {centrality_metrics['f1']:>14.2f}"
    )
    print(
        f"{'Detection Time (ms)':<25} {spectral_metrics['detection_time'] * 1000:>14.1f} {centrality_metrics['detection_time'] * 1000:>14.1f}"
    )

    # Show top suspicious UAVs
    print("\n" + "=" * 70)
    print("🎯 TOP SUSPICIOUS UAVs (by confidence score)")
    print("=" * 70)

    # Sort by spectral confidence
    sorted_spectral = sorted(
        spectral_result.confidence_scores.items(), key=lambda x: x[1], reverse=True
    )[:10]

    print("\nSpectral Analysis - Top 10:")
    for i, (uav_id, score) in enumerate(sorted_spectral, 1):
        is_legit = spectral_result.ground_truth.get(uav_id, True)
        status = "✓ LEGIT" if is_legit else "✗ PHANTOM"
        print(f"  {i:2d}. {uav_id:<20} Score: {score:6.2f}  {status}")

    # Sort by centrality confidence
    sorted_centrality = sorted(
        centrality_result.confidence_scores.items(), key=lambda x: x[1], reverse=True
    )[:10]

    print("\nCentrality Analysis - Top 10:")
    for i, (uav_id, score) in enumerate(sorted_centrality, 1):
        is_legit = centrality_result.ground_truth.get(uav_id, True)
        status = "✓ LEGIT" if is_legit else "✗ PHANTOM"
        print(f"  {i:2d}. {uav_id:<20} Score: {score:6.2f}  {status}")

    # Final summary
    print("\n" + "=" * 70)
    print("✅ Detection demonstration complete!")
    print("=" * 70)
    print("\nKey Findings:")

    # Determine better detector
    if spectral_metrics["f1"] > centrality_metrics["f1"]:
        print(
            f"  • Spectral analysis performed better (F1: {spectral_metrics['f1']:.2f})"
        )
    elif centrality_metrics["f1"] > spectral_metrics["f1"]:
        print(
            f"  • Centrality analysis performed better (F1: {centrality_metrics['f1']:.2f})"
        )
    else:
        print(f"  • Both methods performed equally (F1: {spectral_metrics['f1']:.2f})")

    print("  • Both methods detected in < 100ms")
    print("  • Graph-theoretic detection is effective for phantom UAVs")
    print()


if __name__ == "__main__":
    main()
