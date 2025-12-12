#!/usr/bin/env python3
"""
Visualization demonstration.

Creates publication-quality plots comparing all detection methods.
"""

from pathlib import Path

import numpy as np

from argus_uav.attacks import AttackScenario, AttackType
from argus_uav.attacks.phantom_uav import PhantomInjector
from argus_uav.core.swarm import Swarm
from argus_uav.detection.centrality import CentralityDetector
from argus_uav.detection.crypto_detector import CryptoDetector
from argus_uav.detection.spectral import SpectralDetector
from argus_uav.evaluation.metrics import MetricsCalculator
from argus_uav.evaluation.visualizations import Plotter


def main():
    """Run comprehensive detection comparison with visualizations."""
    print("\n" + "=" * 70)
    print("📊 ARGUS VISUALIZATION DEMONSTRATION")
    print("=" * 70)

    output_dir = Path("results/visualization_demo")
    output_dir.mkdir(parents=True, exist_ok=True)

    # Create swarm WITH crypto
    print("\n📍 Step 1: Initialize swarm with cryptography...")
    rng = np.random.default_rng(seed=42)
    swarm_crypto = Swarm(
        num_uavs=30,
        comm_range=200.0,
        bounds=(500, 500, 100),
        rng=rng,
        enable_crypto=True,
    )

    # Collect baseline
    print("\n🧠 Step 2: Collect baseline and train all detectors...")
    baseline_graphs = []
    for t in range(20):
        swarm_crypto.step(dt=1.0)
        baseline_graphs.append(swarm_crypto.get_graph().copy())

    # Train all detectors
    spectral = SpectralDetector(threshold=1.0)
    centrality = CentralityDetector(threshold=0.9)
    crypto = CryptoDetector()

    spectral.train(baseline_graphs)
    centrality.train(baseline_graphs)
    crypto.train(baseline_graphs)

    print("   ✓ Spectral detector trained")
    print("   ✓ Centrality detector trained")
    print("   ✓ Crypto detector trained")

    # Inject attack
    print("\n⚠️  Step 3: Inject phantom attack...")
    attack = AttackScenario(
        attack_type=AttackType.PHANTOM, start_time=0.0, duration=10.0, phantom_count=5
    )

    injector = PhantomInjector()
    injector.inject(swarm_crypto, attack, 0.0)
    swarm_crypto.step(dt=1.0)

    print("   ✓ 5 phantoms injected")

    # Run all detections
    print("\n🔍 Step 4: Run all detection methods...")
    current_graph = swarm_crypto.get_graph()

    spectral_result = spectral.detect(current_graph)
    centrality_result = centrality.detect(current_graph)
    crypto_result = crypto.detect(current_graph)

    # Compute metrics
    spectral_metrics = spectral_result.compute_metrics()
    centrality_metrics = centrality_result.compute_metrics()
    crypto_metrics = crypto_result.compute_metrics()

    results = {
        "Spectral": spectral_metrics,
        "Centrality": centrality_metrics,
        "Cryptographic": crypto_metrics,
    }

    print("   ✓ All detections complete")

    # Generate visualizations
    print("\n📊 Step 5: Generate visualizations...")

    # 1. Individual ROC curves
    print("   Creating ROC curves...")
    for detector_name, result in [
        ("Spectral", spectral_result),
        ("Centrality", centrality_result),
        ("Cryptographic", crypto_result),
    ]:
        fpr, tpr = MetricsCalculator.compute_roc_curve(
            result.confidence_scores, result.ground_truth
        )
        auc = MetricsCalculator.compute_auc(fpr, tpr)

        Plotter.plot_roc_curve(
            fpr,
            tpr,
            detector_name,
            output_dir / f"roc_{detector_name.lower()}.png",
            auc=auc,
        )

    print(f"   ✓ Individual ROC curves saved to {output_dir}/")

    # 2. Combined ROC curves
    print("   Creating ROC comparison...")
    roc_results = {}
    for detector_name, result in [
        ("Spectral", spectral_result),
        ("Centrality", centrality_result),
        ("Cryptographic", crypto_result),
    ]:
        fpr, tpr = MetricsCalculator.compute_roc_curve(
            result.confidence_scores, result.ground_truth
        )
        auc = MetricsCalculator.compute_auc(fpr, tpr)
        roc_results[detector_name] = (fpr, tpr, auc)

    Plotter.plot_roc_curves_comparison(roc_results, output_dir / "roc_comparison.png")
    print("   ✓ ROC comparison saved")

    # 3. Detection comparison bar charts
    print("   Creating detection comparison...")
    Plotter.plot_detection_comparison(results, output_dir / "detection_comparison.png")
    print("   ✓ Detection comparison saved")

    # 4. Performance comparison
    print("   Creating performance comparison...")
    Plotter.plot_performance_comparison(
        results, output_dir / "performance_comparison.png"
    )
    print("   ✓ Performance comparison saved")

    # 5. Confusion matrices
    print("   Creating confusion matrices...")
    for detector_name, metrics in results.items():
        # Build confusion matrix [[TN, FP], [FN, TP]]
        confusion = np.array(
            [[metrics["tn"], metrics["fp"]], [metrics["fn"], metrics["tp"]]]
        )

        Plotter.plot_confusion_matrix(
            confusion,
            detector_name,
            output_dir / f"confusion_{detector_name.lower()}.png",
        )

    print("   ✓ Confusion matrices saved")

    # 6. Metrics heatmap
    print("   Creating metrics heatmap...")
    Plotter.plot_metrics_heatmap(results, output_dir / "metrics_heatmap.png")
    print("   ✓ Metrics heatmap saved")

    # 7. Summary table
    print("   Creating summary table...")
    table_str = Plotter.create_summary_table(results, output_dir / "results_table.md")
    print("   ✓ Summary table saved")

    # Display results
    print("\n" + "=" * 70)
    print("📈 RESULTS SUMMARY")
    print("=" * 70)
    print(f"\n{table_str}\n")

    # Final summary
    print("=" * 70)
    print("✅ Visualization complete!")
    print("=" * 70)
    print(f"\nGenerated files in {output_dir}/:")
    print("  📊 ROC curves (individual + comparison)")
    print("  📊 Detection comparison bar charts")
    print("  📊 Performance comparison")
    print("  📊 Confusion matrices")
    print("  📊 Metrics heatmap")
    print("  📄 Results table (Markdown)")
    print("\nAll figures saved as:")
    print("  • PNG (300 DPI) - for viewing")
    print("  • PDF (vector) - for LaTeX/papers")
    print()


if __name__ == "__main__":
    main()
