#!/usr/bin/env python3
"""
Scalability test for large UAV swarms.

Tests performance with 50, 100, 150, and 200+ UAVs.
"""

import time

import numpy as np

from argus_uav.attacks import AttackScenario, AttackType
from argus_uav.attacks.phantom_uav import PhantomInjector
from argus_uav.core.swarm import Swarm
from argus_uav.detection.centrality import CentralityDetector
from argus_uav.detection.spectral import SpectralDetector


def test_swarm_size(num_uavs: int, num_steps: int = 100):
    """
    Test swarm simulation performance.

    Args:
        num_uavs: Number of UAVs in swarm
        num_steps: Number of simulation steps

    Returns:
        Performance metrics
    """
    print(f"\n{'=' * 70}")
    print(f"Testing {num_uavs} UAVs")
    print(f"{'=' * 70}")

    # Create swarm
    rng = np.random.default_rng(seed=42)

    # Scale bounds with swarm size for reasonable density
    scale_factor = np.sqrt(num_uavs / 50)
    bounds = (int(1000 * scale_factor), int(1000 * scale_factor), 200)
    comm_range = 100.0 * scale_factor

    print(f"  Bounds: {bounds}, Comm range: {comm_range:.1f}m")

    start = time.time()
    swarm = Swarm(num_uavs=num_uavs, comm_range=comm_range, bounds=bounds, rng=rng)
    init_time = time.time() - start

    stats = swarm.get_statistics()
    print(f"  Initialization: {init_time * 1000:.1f}ms")
    print(f"  Initial edges: {stats['num_edges']}")
    print(f"  Avg degree: {stats['avg_degree']:.2f}")
    print(f"  Connected: {stats['is_connected']}")

    # Run simulation
    print(f"\n  Running {num_steps} simulation steps...")
    start = time.time()

    for i in range(num_steps):
        swarm.step(dt=1.0)
        if i % 20 == 0:
            stats = swarm.get_statistics()
            print(
                f"    Step {i:3d}: {stats['num_edges']} edges, {stats['avg_degree']:.2f} avg degree"
            )

    sim_time = time.time() - start

    print(f"\n  Simulation time: {sim_time:.2f}s ({num_steps} steps)")
    print(f"  Average per step: {sim_time / num_steps * 1000:.2f}ms")

    # Test detection
    print("\n  Testing detection methods...")

    # Collect small baseline
    baseline = [swarm.get_graph().copy() for _ in range(5)]

    # Inject attack
    attack = AttackScenario(
        attack_type=AttackType.PHANTOM,
        start_time=0.0,
        duration=10.0,
        phantom_count=int(num_uavs * 0.1),  # 10% phantoms
    )
    injector = PhantomInjector()
    injector.inject(swarm, attack, 0.0)
    swarm.step(dt=1.0)

    print(f"    Injected {len(injector.phantom_ids)} phantoms")

    # Spectral detection
    spectral = SpectralDetector(threshold=1.0)
    spectral.train(baseline)

    start = time.time()
    result = spectral.detect(swarm.get_graph())
    spectral_time = time.time() - start

    metrics = result.compute_metrics()
    print(
        f"    Spectral: {spectral_time * 1000:.2f}ms, TPR={metrics['tpr']:.2%}, FPR={metrics['fpr']:.2%}"
    )

    # Centrality detection
    centrality = CentralityDetector(threshold=0.9)
    centrality.train(baseline)

    start = time.time()
    result = centrality.detect(swarm.get_graph())
    centrality_time = time.time() - start

    metrics = result.compute_metrics()
    print(
        f"    Centrality: {centrality_time * 1000:.2f}ms, TPR={metrics['tpr']:.2%}, FPR={metrics['fpr']:.2%}"
    )

    return {
        "num_uavs": num_uavs,
        "init_time": init_time,
        "sim_time": sim_time,
        "avg_step_time": sim_time / num_steps,
        "spectral_time": spectral_time,
        "centrality_time": centrality_time,
        "num_edges": swarm.get_statistics()["num_edges"],
    }


def main():
    """Run scalability tests."""
    print("\n" + "=" * 70)
    print("⚡ ARGUS SCALABILITY TEST")
    print("   Testing performance with 50, 100, 150, 200, 250 UAVs")
    print("=" * 70)

    sizes = [50, 100, 150, 200, 250]
    results = []

    for size in sizes:
        result = test_swarm_size(size, num_steps=50)
        results.append(result)

    # Summary table
    print("\n" + "=" * 70)
    print("📊 SCALABILITY SUMMARY")
    print("=" * 70)

    print(
        f"\n{'UAVs':>6} | {'Edges':>6} | {'Init(ms)':>10} | {'Step(ms)':>10} | "
        f"{'Spectral(ms)':>13} | {'Centrality(ms)':>15}"
    )
    print("-" * 70)

    for r in results:
        print(
            f"{r['num_uavs']:>6} | {r['num_edges']:>6} | "
            f"{r['init_time'] * 1000:>10.1f} | {r['avg_step_time'] * 1000:>10.2f} | "
            f"{r['spectral_time'] * 1000:>13.2f} | {r['centrality_time'] * 1000:>15.2f}"
        )

    # Check if all meet requirements
    print("\n" + "=" * 70)
    print("✅ PERFORMANCE VALIDATION")
    print("=" * 70)

    max_step_time = max(r["avg_step_time"] for r in results)
    max_detection = max(max(r["spectral_time"], r["centrality_time"]) for r in results)

    print("\nRequirement: Detection < 100ms")
    print(f"  Maximum step time: {max_step_time * 1000:.2f}ms")
    print(f"  Maximum detection: {max_detection * 1000:.2f}ms")

    if max_detection < 0.100:
        print(f"\n🎯 ALL TESTS PASS: System scales to {max(sizes)} UAVs!")
        print("   Detection remains real-time even at large scale.")
    else:
        print(f"\n⚠️  Warning: Detection exceeds 100ms at {max(sizes)} UAVs")
        print("   Consider optimizations for larger swarms.")

    # Scalability insights
    print("\n💡 Scalability Insights:")

    # Compute growth rates
    time_50 = results[0]["avg_step_time"]
    time_250 = results[-1]["avg_step_time"]
    speedup_ratio = time_250 / time_50

    print(f"   • 50 UAVs: {time_50 * 1000:.2f}ms per step")
    print(f"   • 250 UAVs: {time_250 * 1000:.2f}ms per step")
    print(f"   • 5× size increase → {speedup_ratio:.1f}× time increase")

    # Expected complexity
    if speedup_ratio < 30:  # Less than O(n²)
        print("   • Growth rate: Better than O(n²) - good scaling!")
    elif speedup_ratio < 100:  # Around O(n²)
        print("   • Growth rate: ~O(n²) - acceptable for graph operations")
    else:
        print("   • Growth rate: Approaching O(n³) - consider optimizations")

    print()


if __name__ == "__main__":
    main()
