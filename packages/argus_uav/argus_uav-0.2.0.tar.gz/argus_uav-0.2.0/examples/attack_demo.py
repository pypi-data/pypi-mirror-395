#!/usr/bin/env python3
"""
Attack injection demonstration.

Shows phantom UAV injection, position falsification, and coordinated attacks.
"""

import numpy as np

from argus_uav.attacks import AttackScenario, AttackType
from argus_uav.attacks.coordinated import CoordinatedInjector
from argus_uav.attacks.phantom_uav import PhantomInjector
from argus_uav.attacks.position_spoof import PositionFalsifier
from argus_uav.core.swarm import Swarm


def demo_phantom_attack():
    """Demonstrate phantom UAV injection."""
    print("\n" + "=" * 70)
    print("🎭 PHANTOM UAV ATTACK DEMONSTRATION")
    print("=" * 70)

    # Create swarm
    rng = np.random.default_rng(seed=42)
    swarm = Swarm(num_uavs=30, comm_range=200.0, bounds=(500, 500, 100), rng=rng)

    print(f"\n📍 Initial swarm: {swarm.get_statistics()['num_uavs']} UAVs")

    # Configure phantom attack
    attack = AttackScenario(
        attack_type=AttackType.PHANTOM, start_time=5.0, duration=10.0, phantom_count=5
    )

    injector = PhantomInjector()

    # Run simulation
    print("\n⏱️  Running simulation...")
    for t in range(20):
        current_time = float(t)

        # Inject attack when active
        if attack.is_active(current_time) and not injector.injected:
            injector.inject(swarm, attack, current_time)
            print(f"\n⚠️  Attack injected at t={t}s")

        # Remove attack when done
        if current_time >= attack.start_time + attack.duration and injector.injected:
            injector.remove_phantoms(swarm)
            print(f"\n✓ Attack removed at t={t}s")

        swarm.step(dt=1.0)

        stats = swarm.get_statistics()
        status = "🔴 UNDER ATTACK" if attack.is_active(current_time) else "🟢 CLEAN"
        print(
            f"t={t:2d}s: {stats['num_uavs']:2d} UAVs, {stats['num_edges']:3d} links | {status}"
        )

    # Show ground truth
    ground_truth = injector.get_ground_truth()
    legitimate = sum(1 for is_legit in ground_truth.values() if is_legit)
    spoofed = sum(1 for is_legit in ground_truth.values() if not is_legit)
    print(f"\n📊 Ground Truth: {legitimate} legitimate, {spoofed} spoofed")


def demo_position_falsification():
    """Demonstrate position falsification attack."""
    print("\n" + "=" * 70)
    print("📍 POSITION FALSIFICATION ATTACK DEMONSTRATION")
    print("=" * 70)

    # Create swarm
    rng = np.random.default_rng(seed=123)
    swarm = Swarm(num_uavs=20, comm_range=150.0, bounds=(400, 400, 100), rng=rng)

    print(f"\n📍 Initial swarm: {swarm.get_statistics()['num_uavs']} UAVs")

    # Configure position falsification
    attack = AttackScenario(
        attack_type=AttackType.POSITION_FALSIFICATION,
        start_time=3.0,
        duration=8.0,
        intensity=0.25,  # 25% of UAVs compromised
        falsification_magnitude=50.0,  # 50m offset
    )

    falsifier = PositionFalsifier()

    # Run simulation
    print("\n⏱️  Running simulation...")
    for t in range(15):
        current_time = float(t)

        # Inject attack when active
        if attack.is_active(current_time) and not falsifier.injected:
            falsifier.inject(swarm, attack, current_time)
            print(f"\n⚠️  Position falsification active at t={t}s")
            print(f"    Compromised UAVs: {len(falsifier.target_uav_ids)}")

        # Remove attack when done
        if current_time >= attack.start_time + attack.duration and falsifier.injected:
            falsifier.restore_positions(swarm)
            print(f"\n✓ Positions restored at t={t}s")

        swarm.step(dt=1.0)

        stats = swarm.get_statistics()
        status = "🔴 FALSIFIED" if attack.is_active(current_time) else "🟢 ACCURATE"
        print(
            f"t={t:2d}s: {stats['num_uavs']:2d} UAVs, {stats['num_edges']:3d} links | {status}"
        )

    # Show ground truth
    ground_truth = falsifier.get_ground_truth()
    legitimate = sum(1 for is_legit in ground_truth.values() if is_legit)
    compromised = sum(1 for is_legit in ground_truth.values() if not is_legit)
    print(f"\n📊 Ground Truth: {legitimate} accurate, {compromised} falsified")


def demo_coordinated_attack():
    """Demonstrate coordinated phantom attack."""
    print("\n" + "=" * 70)
    print("🎯 COORDINATED ATTACK DEMONSTRATION")
    print("=" * 70)

    # Create swarm
    rng = np.random.default_rng(seed=456)
    swarm = Swarm(num_uavs=25, comm_range=180.0, bounds=(450, 450, 100), rng=rng)

    print(f"\n📍 Initial swarm: {swarm.get_statistics()['num_uavs']} UAVs")

    # Configure coordinated attack
    attack = AttackScenario(
        attack_type=AttackType.COORDINATED,
        start_time=4.0,
        duration=10.0,
        phantom_count=6,
        coordination_pattern="circle",
    )

    injector = CoordinatedInjector()

    # Run simulation
    print("\n⏱️  Running simulation...")
    for t in range(18):
        current_time = float(t)

        # Inject attack when active
        if attack.is_active(current_time) and not injector.injected:
            injector.inject(swarm, attack, current_time)
            print(f"\n⚠️  Coordinated attack (circle formation) at t={t}s")

        # Remove attack when done
        if current_time >= attack.start_time + attack.duration and injector.injected:
            injector.remove_coordinated(swarm)
            print(f"\n✓ Coordinated phantoms removed at t={t}s")

        swarm.step(dt=1.0)

        stats = swarm.get_statistics()
        status = (
            "🔴 COORDINATED ATTACK" if attack.is_active(current_time) else "🟢 CLEAN"
        )
        print(
            f"t={t:2d}s: {stats['num_uavs']:2d} UAVs, {stats['num_edges']:3d} links | {status}"
        )

    # Show ground truth
    ground_truth = injector.get_ground_truth()
    legitimate = sum(1 for is_legit in ground_truth.values() if is_legit)
    coordinated = sum(1 for is_legit in ground_truth.values() if not is_legit)
    print(
        f"\n📊 Ground Truth: {legitimate} legitimate, {coordinated} coordinated phantoms"
    )


def main():
    """Run all attack demonstrations."""
    print("\n🚁 ARGUS UAV REMOTE ID SPOOFING ATTACK DEMONSTRATIONS")
    print("=" * 70)

    demo_phantom_attack()
    demo_position_falsification()
    demo_coordinated_attack()

    print("\n" + "=" * 70)
    print("✅ All attack demonstrations complete!")
    print("=" * 70)
    print("\nKey Observations:")
    print("  • Phantom attacks increase UAV count and network edges")
    print("  • Position falsification compromises specific UAVs")
    print("  • Coordinated attacks create believable phantom sub-swarms")
    print("  • Ground truth tracking enables detection evaluation")
    print()


if __name__ == "__main__":
    main()
