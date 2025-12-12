#!/usr/bin/env python3
"""
Simple example demonstrating baseline UAV swarm simulation.

This is the MVP - a working swarm simulator without attacks or detection.
"""

import numpy as np

from argus_uav.core.swarm import Swarm


def main():
    """Run a simple 20-UAV swarm simulation."""
    print("🚁 Argus UAV Swarm Simulator - Simple Example")
    print("=" * 50)

    # Create reproducible random generator
    rng = np.random.default_rng(seed=42)

    # Initialize swarm
    print("\n📍 Initializing swarm with 20 UAVs...")
    swarm = Swarm(
        num_uavs=20,
        comm_range=100.0,  # meters
        bounds=(1000, 1000, 200),  # x, y, z limits
        rng=rng,
    )

    # Display initial state
    stats = swarm.get_statistics()
    print(f"   • Number of UAVs: {stats['num_uavs']}")
    print(f"   • Communication links: {stats['num_edges']}")
    print(f"   • Average degree: {stats['avg_degree']:.2f}")
    print(f"   • Network connected: {stats['is_connected']}")

    # Run simulation for 10 seconds
    print("\n⏱️  Running simulation for 10 seconds...")
    print("\nTime | UAVs | Links | Avg Degree | Connected")
    print("-" * 50)

    for t in range(11):
        stats = swarm.get_statistics()
        connected_str = "✓" if stats["is_connected"] else "✗"
        print(
            f"{t:3d}s | {stats['num_uavs']:4d} | {stats['num_edges']:5d} | "
            f"{stats['avg_degree']:10.2f} | {connected_str:>9}"
        )

        if t < 10:
            swarm.step(dt=1.0)

    print("\n✅ Simulation complete!")
    print(f"\nFinal state: {swarm}")

    # Show sample UAV positions
    print("\n📊 Sample UAV positions:")
    sample_uavs = list(swarm.get_uavs().values())[:3]
    for uav in sample_uavs:
        x, y, z = uav.position
        print(f"   • {uav.uav_id}: ({x:.1f}, {y:.1f}, {z:.1f})")


if __name__ == "__main__":
    main()
