#!/usr/bin/env python3
"""
Dense swarm example with better connectivity.

Uses smaller area and larger comm range for a well-connected swarm.
"""

import numpy as np

from argus_uav.core.swarm import Swarm


def main():
    """Run a dense 30-UAV swarm with good connectivity."""
    print("🚁 Argus UAV Swarm Simulator - Dense Network Example")
    print("=" * 60)

    # Create reproducible random generator
    rng = np.random.default_rng(seed=42)

    # Initialize dense swarm
    print("\n📍 Initializing swarm with 30 UAVs in compact area...")
    swarm = Swarm(
        num_uavs=30,
        comm_range=200.0,  # Larger comm range
        bounds=(500, 500, 100),  # Smaller area
        rng=rng,
    )

    # Display initial state
    stats = swarm.get_statistics()
    print(f"   • Number of UAVs: {stats['num_uavs']}")
    print(f"   • Communication links: {stats['num_edges']}")
    print(f"   • Average degree: {stats['avg_degree']:.2f}")
    print(f"   • Network connected: {'✓ YES' if stats['is_connected'] else '✗ NO'}")

    # Run simulation
    print("\n⏱️  Running simulation for 15 seconds...")
    print("\nTime | UAVs | Links | Avg Degree | Connected")
    print("-" * 60)

    for t in range(16):
        stats = swarm.get_statistics()
        connected_str = "✓" if stats["is_connected"] else "✗"
        print(
            f"{t:3d}s | {stats['num_uavs']:4d} | {stats['num_edges']:5d} | "
            f"{stats['avg_degree']:10.2f} | {connected_str:>9}"
        )

        if t < 15:
            swarm.step(dt=1.0)

    # Final analysis
    final_stats = swarm.get_statistics()
    print("\n" + "=" * 60)
    print("📊 Final Network Analysis:")
    print(f"   • Total UAVs: {final_stats['num_uavs']}")
    print(f"   • Total Links: {final_stats['num_edges']}")
    print(f"   • Average Degree: {final_stats['avg_degree']:.2f}")
    print(
        f"   • Connected Network: {'✓ YES' if final_stats['is_connected'] else '✗ NO'}"
    )

    # Maximum possible edges in complete graph
    max_edges = final_stats["num_uavs"] * (final_stats["num_uavs"] - 1) // 2
    density = (final_stats["num_edges"] / max_edges) * 100 if max_edges > 0 else 0
    print(f"   • Network Density: {density:.1f}%")

    print("\n✅ Dense swarm simulation complete!")
    print(
        f"\nThis is a {'' if final_stats['is_connected'] else 'NOT '}connected network"
    )
    print("suitable for demonstrating swarm coordination algorithms.")


if __name__ == "__main__":
    main()
