"""
Enhanced detection demonstration with improvements for coordinated attacks.

This example demonstrates the three key improvements:
1. Temporal Correlation Detector - for coordinated attacks
2. Enhanced Spectral Detector - with eigenvector residuals
3. Calibrated ML Detector - with adjustable threshold
"""

import argparse
import sys
from pathlib import Path

import numpy as np

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from argus_uav.attacks import AttackScenario
from argus_uav.attacks.coordinated import CoordinatedInjector
from argus_uav.attacks.phantom_uav import PhantomInjector
from argus_uav.attacks.position_spoof import PositionFalsifier
from argus_uav.core.swarm import Swarm
from argus_uav.detection.centrality import CentralityDetector
from argus_uav.detection.crypto_detector import CryptoDetector
from argus_uav.detection.ml_detection import Node2VecDetector
from argus_uav.detection.spectral import SpectralDetector
from argus_uav.detection.temporal_correlation import TemporalCorrelationDetector
from argus_uav.evaluation.metrics import MetricsCalculator
from argus_uav.utils.logging_config import get_logger, setup_logging

logger = get_logger(__name__)


def run_enhanced_detection_demo(attack_type: str = "coordinated"):
    """
    Run enhanced detection demonstration.

    Args:
        attack_type: Type of attack to simulate ('phantom', 'position', 'coordinated')
    """
    print("=" * 80)
    print("🚀 ENHANCED DETECTION DEMO")
    print("=" * 80)
    print(f"\nAttack Type: {attack_type.upper()}")
    print("\nImprovements:")
    print("  1. ✅ Temporal Correlation Detector - tracks coordinated behavior")
    print(
        "  2. ✅ Enhanced Spectral Detector - eigenvector residuals + position validation"
    )
    print("  3. ✅ Calibrated ML Detector - adjustable threshold (FPR reduction)")
    print("=" * 80)

    # Initialize swarm
    print("\n📡 Initializing swarm...")
    rng = np.random.default_rng(seed=42)
    swarm = Swarm(
        num_uavs=20,
        comm_range=150.0,
        bounds=(1000, 1000, 500),
        rng=rng,
    )

    # Initialize detectors with improvements
    print("\n🔍 Initializing enhanced detectors...")

    detectors = {
        "crypto": CryptoDetector(),
        "spectral_basic": SpectralDetector(
            name="spectral_basic",
            threshold=2.5,
            use_eigenvector_residuals=False,
        ),
        "spectral_enhanced": SpectralDetector(
            name="spectral_enhanced",
            threshold=2.2,
            use_eigenvector_residuals=True,
        ),
        "centrality": CentralityDetector(threshold=2.0),
        "ml_aggressive": Node2VecDetector(
            name="ml_aggressive",
            contamination=0.1,
            score_threshold=0.5,  # Default aggressive
        ),
        "ml_calibrated": Node2VecDetector(
            name="ml_calibrated",
            contamination=0.1,
            score_threshold=0.7,  # Calibrated to reduce FPR
        ),
        "temporal_correlation": TemporalCorrelationDetector(
            threshold=2.5,
            history_size=10,
            correlation_threshold=0.85,
        ),
    }

    # Train detectors on clean baseline
    print("\n📊 Training detectors on clean baseline...")
    baseline_timesteps = 20
    clean_graphs = []

    for t in range(baseline_timesteps):
        swarm.step(dt=1.0)
        graph = swarm.get_graph()
        clean_graphs.append(graph)

    for name, detector in detectors.items():
        detector.train(clean_graphs)
        print(f"  ✓ {name} trained")

    # Setup attack
    print(f"\n💥 Setting up {attack_type} attack...")

    if attack_type == "phantom":
        injector = PhantomInjector()
        scenario = AttackScenario(
            attack_type="phantom",
            phantom_count=3,
            start_time=0.0,
            duration=5.0,
        )
    elif attack_type == "position":
        injector = PositionFalsifier()
        scenario = AttackScenario(
            attack_type="position_falsification",
            target_uav_ids=[f"UAV-{i:03d}" for i in range(5)],
            start_time=0.0,
            duration=5.0,
            falsification_magnitude=100.0,
        )
    else:  # coordinated
        injector = CoordinatedInjector()
        scenario = AttackScenario(
            attack_type="coordinated",
            phantom_count=4,
            coordination_pattern="circle",
            start_time=0.0,
            duration=5.0,
        )

    # Inject attack
    injector.inject(swarm, scenario, 0.0)
    print(
        f"  ✓ Attack injected: {scenario.phantom_count if hasattr(scenario, 'phantom_count') else 'position spoofing'}"
    )

    # Run detection
    print("\n🔎 Running detection...")
    attack_timesteps = 20  # Increased for better temporal correlation
    all_results = {name: [] for name in detectors.keys()}

    for t in range(attack_timesteps):
        swarm.step(dt=1.0)
        graph = swarm.get_graph()

        for name, detector in detectors.items():
            result = detector.detect(graph)
            all_results[name].append(result)

    # Compute metrics
    print("\n📈 Computing detection metrics...\n")
    print("-" * 80)
    print(
        f"{'Detector':<25} {'TPR':<8} {'FPR':<8} {'Precision':<10} {'F1':<8} {'Time (ms)':<12}"
    )
    print("-" * 80)

    metrics_summary = {}

    for name, results in all_results.items():
        # Aggregate metrics across all timesteps
        all_tpr = []
        all_fpr = []
        all_precision = []
        all_f1 = []
        all_times = []

        for result in results:
            # Compute metrics for this timestep
            metrics = MetricsCalculator.compute_detection_metrics(
                result.anomalous_uav_ids, result.ground_truth
            )
            all_tpr.append(metrics["tpr"])
            all_fpr.append(metrics["fpr"])
            all_precision.append(metrics["precision"])
            all_f1.append(metrics["f1"])
            all_times.append(result.detection_time)

        # Compute averages
        summary = {
            "average_tpr": np.mean(all_tpr) if all_tpr else 0.0,
            "average_fpr": np.mean(all_fpr) if all_fpr else 0.0,
            "average_precision": np.mean(all_precision) if all_precision else 0.0,
            "average_f1": np.mean(all_f1) if all_f1 else 0.0,
            "average_detection_time": np.mean(all_times) if all_times else 0.0,
        }

        metrics_summary[name] = summary

        print(
            f"{name:<25} "
            f"{summary['average_tpr']:<8.2f} "
            f"{summary['average_fpr']:<8.2f} "
            f"{summary['average_precision']:<10.2f} "
            f"{summary['average_f1']:<8.2f} "
            f"{summary['average_detection_time'] * 1000:<12.1f}"
        )

    print("-" * 80)

    # Highlight improvements
    print("\n💡 Key Improvements:\n")

    if attack_type == "coordinated":
        temp_f1 = metrics_summary.get("temporal_correlation", {}).get("average_f1", 0)
        print(f"  • Temporal Correlation F1: {temp_f1:.2f}")
        print("    → NEW detector specifically for coordinated attacks!")

    if attack_type in ["phantom", "position"]:
        basic_f1 = metrics_summary.get("spectral_basic", {}).get("average_f1", 0)
        enhanced_f1 = metrics_summary.get("spectral_enhanced", {}).get("average_f1", 0)
        improvement = enhanced_f1 - basic_f1
        print(f"  • Spectral Detector Improvement: {improvement:+.2f} F1")
        print("    → Eigenvector residuals + position validation")

    aggressive_fpr = metrics_summary.get("ml_aggressive", {}).get("average_fpr", 0)
    calibrated_fpr = metrics_summary.get("ml_calibrated", {}).get("average_fpr", 0)
    fpr_reduction = aggressive_fpr - calibrated_fpr
    print(f"  • ML FPR Reduction: {fpr_reduction:+.2f}")
    print("    → Adjustable threshold (0.7 vs 0.5)")

    print("\n" + "=" * 80)
    print("✅ Enhanced detection demo completed!")
    print("=" * 80)


if __name__ == "__main__":
    setup_logging(level="INFO")

    parser = argparse.ArgumentParser(description="Enhanced detection demonstration")
    parser.add_argument(
        "--attack",
        choices=["phantom", "position", "coordinated"],
        default="coordinated",
        help="Type of attack to demonstrate",
    )

    args = parser.parse_args()

    run_enhanced_detection_demo(attack_type=args.attack)
