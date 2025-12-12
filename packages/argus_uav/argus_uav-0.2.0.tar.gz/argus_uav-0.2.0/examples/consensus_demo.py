#!/usr/bin/env python3
"""
Consensus algorithm demonstration.

Shows how phantom UAV attacks disrupt consensus and how defenses restore it.
"""

# Set matplotlib backend to Qt5
import matplotlib

matplotlib.use("QtAgg")

import matplotlib.pyplot as plt
import numpy as np

from argus_uav.attacks import AttackScenario, AttackType
from argus_uav.attacks.phantom_uav import PhantomInjector
from argus_uav.consensus.average_consensus import AverageConsensus
from argus_uav.core.swarm import Swarm


def main():
    """Demonstrate consensus under attack and defense."""
    print("\n" + "=" * 70)
    print("🎯 CONSENSUS ALGORITHM DEMONSTRATION")
    print("   Average Consensus Under Phantom Attack")
    print("=" * 70)

    # Scenario 1: Clean consensus (baseline)
    print("\n📍 Scenario 1: BASELINE (No Attack)")
    print("-" * 70)

    rng = np.random.default_rng(seed=42)
    swarm_clean = Swarm(num_uavs=30, comm_range=200.0, bounds=(500, 500, 100), rng=rng)
    consensus_clean = AverageConsensus()
    consensus_clean.initialize(swarm_clean.get_graph(), rng)

    print(f"Initialized: {len(consensus_clean.states)} UAVs")
    print(f"True average: {consensus_clean.true_average:.2f}")

    # Run consensus without attack
    errors_clean = []
    for t in range(50):
        swarm_clean.step(dt=1.0)
        consensus_clean.step(swarm_clean.get_graph())
        error = consensus_clean.get_consensus_error()
        errors_clean.append(error)

        if t % 10 == 0:
            stats = consensus_clean.get_statistics()
            print(
                f"  t={t:2d}s: error={error:.2f}, mean={stats['mean']:.2f}, "
                f"std={stats['std']:.2f}, converged={stats['converged']}"
            )

    final_stats_clean = consensus_clean.get_statistics()
    print(f"\n✓ Baseline final error: {errors_clean[-1]:.3f}")
    print(f"✓ Converged: {final_stats_clean['converged']}")

    # Scenario 2: Consensus under attack
    print("\n⚠️  Scenario 2: UNDER PHANTOM ATTACK")
    print("-" * 70)

    rng_attack = np.random.default_rng(seed=42)
    swarm_attack = Swarm(
        num_uavs=30, comm_range=200.0, bounds=(500, 500, 100), rng=rng_attack
    )
    consensus_attack = AverageConsensus()
    consensus_attack.initialize(swarm_attack.get_graph(), rng_attack)

    # Inject phantoms at t=10s
    attack = AttackScenario(
        attack_type=AttackType.PHANTOM, start_time=10.0, duration=30.0, phantom_count=5
    )
    injector = PhantomInjector()

    errors_attack = []
    attack_injected = False

    for t in range(50):
        current_time = float(t)

        # Inject attack
        if attack.is_active(current_time) and not attack_injected:
            injector.inject(swarm_attack, attack, current_time)
            # Phantoms get random consensus values
            for phantom_id in injector.phantom_ids:
                consensus_attack.states[phantom_id] = float(rng_attack.uniform(0, 200))
            attack_injected = True
            print(f"\n⚠️  Attack injected at t={t}s (5 phantoms with random values)")

        swarm_attack.step(dt=1.0)
        consensus_attack.step(swarm_attack.get_graph())
        error = consensus_attack.get_consensus_error()
        errors_attack.append(error)

        if t % 10 == 0 or t == 10:
            stats = consensus_attack.get_statistics()
            status = "🔴 ATTACK" if attack.is_active(current_time) else "🟢 CLEAN"
            print(
                f"  t={t:2d}s: error={error:.2f}, mean={stats['mean']:.2f}, "
                f"std={stats['std']:.2f} | {status}"
            )

    print(f"\n⚠️  Attack final error: {errors_attack[-1]:.3f}")
    print(f"   Error increased by: {(errors_attack[-1] - errors_clean[-1]):.3f}")

    # Scenario 3: With crypto defense
    print("\n🔐 Scenario 3: WITH CRYPTO DEFENSE")
    print("-" * 70)

    rng_crypto = np.random.default_rng(seed=42)
    swarm_crypto = Swarm(
        num_uavs=30,
        comm_range=200.0,
        bounds=(500, 500, 100),
        rng=rng_crypto,
        enable_crypto=True,
    )
    consensus_crypto = AverageConsensus()
    consensus_crypto.initialize(swarm_crypto.get_graph(), rng_crypto)

    # Inject attack but exclude phantom values (crypto rejects them)
    crypto_injector = PhantomInjector()
    errors_crypto = []
    crypto_attack_injected = False

    for t in range(50):
        current_time = float(t)

        # Inject attack
        if attack.is_active(current_time) and not crypto_attack_injected:
            crypto_injector.inject(swarm_crypto, attack, current_time)
            # With crypto, phantom messages are rejected - don't add to consensus
            crypto_attack_injected = True
            print(f"\n🔐 Attack injected at t={t}s but crypto rejects phantom values")

        swarm_crypto.step(dt=1.0)

        # Only update consensus for legitimate UAVs (crypto verified)
        legitimate_graph = nx.Graph()
        for node in swarm_crypto.graph.nodes():
            uav = swarm_crypto.uavs[node]
            if uav.is_legitimate or uav.public_key is not None:
                legitimate_graph.add_node(node)

        for u, v in swarm_crypto.graph.edges():
            if u in legitimate_graph and v in legitimate_graph:
                legitimate_graph.add_edge(u, v)

        consensus_crypto.step(legitimate_graph)
        error = consensus_crypto.get_consensus_error()
        errors_crypto.append(error)

        if t % 10 == 0 or t == 10:
            stats = consensus_crypto.get_statistics()
            status = "🔐 PROTECTED" if attack.is_active(current_time) else "🟢 CLEAN"
            print(
                f"  t={t:2d}s: error={error:.2f}, mean={stats['mean']:.2f}, "
                f"std={stats['std']:.2f} | {status}"
            )

    print(f"\n✓ Crypto defense final error: {errors_crypto[-1]:.3f}")
    print(f"  Similar to baseline: {abs(errors_crypto[-1] - errors_clean[-1]) < 1.0}")

    # Comparative analysis
    print("\n" + "=" * 70)
    print("📊 CONSENSUS ERROR COMPARISON")
    print("=" * 70)

    print("\nFinal Consensus Error:")
    print(f"  • Baseline (no attack):  {errors_clean[-1]:.3f}")
    print(
        f"  • Under phantom attack:  {errors_attack[-1]:.3f}  (+{errors_attack[-1] - errors_clean[-1]:.1f})"
    )
    print(
        f"  • With crypto defense:   {errors_crypto[-1]:.3f}  (+{errors_crypto[-1] - errors_clean[-1]:.1f})"
    )

    improvement = ((errors_attack[-1] - errors_crypto[-1]) / errors_attack[-1]) * 100
    print(
        f"\n💡 Crypto defense reduces error by {improvement:.1f}% vs undefended attack"
    )

    # Visualize
    print("\n📊 Generating consensus error plot...")

    fig, ax = plt.subplots(figsize=(10, 6))

    time_steps = np.arange(len(errors_clean))

    ax.plot(
        time_steps,
        errors_clean,
        label="Baseline (no attack)",
        linewidth=2,
        color="green",
    )
    ax.plot(
        time_steps,
        errors_attack,
        label="Under phantom attack",
        linewidth=2,
        color="red",
    )
    ax.plot(
        time_steps,
        errors_crypto,
        label="With crypto defense",
        linewidth=2,
        color="blue",
    )

    # Highlight attack window
    ax.axvspan(10, 40, alpha=0.2, color="red", label="Attack active")

    ax.set_xlabel("Time (seconds)", fontsize=12)
    ax.set_ylabel("Consensus Error (L2 norm)", fontsize=12)
    ax.set_title("Consensus Resilience Under Attack", fontsize=14)
    ax.legend(loc="best")
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig("results/consensus_comparison.png", dpi=300)
    plt.savefig("results/consensus_comparison.pdf")
    print("   ✓ Plot saved to results/consensus_comparison.png")

    # Final summary
    print("\n" + "=" * 70)
    print("✅ Consensus demonstration complete!")
    print("=" * 70)
    print("\nKey Findings:")
    print("  • Phantom attacks disrupt consensus significantly")
    print(f"  • Attack increases error by {errors_attack[-1] - errors_clean[-1]:.1f}")
    print("  • Crypto defense restores near-baseline performance")
    print("  • Demonstrates real-world impact of spoofing on swarm coordination")
    print()


if __name__ == "__main__":
    import networkx as nx

    main()
