#!/usr/bin/env python3
"""
Enhanced live visualization with detection method selection.

Shows UAV swarm with phantom attack and real-time detection overlay.
User can select which detection method to visualize.
"""

# Set matplotlib backend to Qt5
import matplotlib

matplotlib.use("QtAgg")

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Patch

from argus_uav.attacks import AttackScenario, AttackType
from argus_uav.attacks.phantom_uav import PhantomInjector
from argus_uav.core.swarm import Swarm
from argus_uav.detection.centrality import CentralityDetector
from argus_uav.detection.crypto_detector import CryptoDetector
from argus_uav.detection.spectral import SpectralDetector


def main():
    """Run enhanced live visualization with detection selection."""
    print("\n" + "=" * 70)
    print("📺 ENHANCED LIVE VISUALIZATION WITH DETECTION")
    print("=" * 70)

    # User selects detection method
    print("\nSelect detection method:")
    print("  1. None (just show attacks)")
    print("  2. Spectral detection")
    print("  3. Centrality detection")
    print("  4. Cryptographic detection")
    print("  5. All methods comparison")

    try:
        choice = input("\nEnter choice (1-5) [default: 1]: ").strip() or "1"
        choice_num = int(choice)
    except ValueError:
        choice_num = 1

    # Create swarm (with crypto if method 4 selected)
    enable_crypto = choice_num == 4

    print(f"\n📍 Initializing {'crypto-enabled ' if enable_crypto else ''}swarm...")
    rng = np.random.default_rng(seed=42)
    swarm = Swarm(
        num_uavs=30,
        comm_range=200.0,
        bounds=(500, 500, 100),
        rng=rng,
        enable_crypto=enable_crypto,
    )

    # Setup attack
    attack = AttackScenario(
        attack_type=AttackType.PHANTOM, start_time=10.0, duration=20.0, phantom_count=5
    )

    injector = PhantomInjector()

    # Train detectors if needed
    detectors = {}
    if choice_num >= 2:
        print("\n🧠 Training detectors on baseline...")
        baseline = [swarm.get_graph().copy() for _ in range(10)]

        if choice_num == 2 or choice_num == 5:
            detectors["spectral"] = SpectralDetector(threshold=1.0)
            detectors["spectral"].train(baseline)
            print("   ✓ Spectral trained")

        if choice_num == 3 or choice_num == 5:
            detectors["centrality"] = CentralityDetector(threshold=0.9)
            detectors["centrality"].train(baseline)
            print("   ✓ Centrality trained")

        if choice_num == 4 or choice_num == 5:
            detectors["crypto"] = CryptoDetector()
            detectors["crypto"].train(baseline)
            print("   ✓ Crypto trained")

    # Setup visualization
    print("\n🎬 Starting visualization...")
    print("\nColor Legend:")
    print("  🟢 Green circle = Legitimate UAV")
    if enable_crypto:
        print("  🔵 Blue circle = Legitimate UAV (crypto enabled)")
    print("  🔴 Red X = Phantom UAV")
    if detectors:
        print("  ⚠️  Yellow outline = Flagged by detector")

    print("\n⏱️  Timeline:")
    print("   • t=0-10s:  Normal operation (30 UAVs)")
    print("   • t=10-30s: PHANTOM ATTACK (5 phantoms)")
    print("   • t=30s+:   Attack removed")
    print("\n   Close window to exit...")

    # Create figure
    fig, (ax_main, ax_stats) = plt.subplots(1, 2, figsize=(16, 8))

    # Data tracking
    time_history = []
    edge_history = []
    phantom_count_history = []
    detection_count_history = []

    attack_injected = False
    attack_removed = False

    def update(frame):
        nonlocal attack_injected, attack_removed

        current_time = swarm.simulation_time

        # Inject attack
        if attack.is_active(current_time) and not attack_injected:
            injector.inject(swarm, attack, current_time)
            attack_injected = True
            print(f"\n⚠️  5 Phantom UAVs injected at t={current_time:.1f}s!")

        # Remove attack
        if (
            not attack.is_active(current_time)
            and attack_injected
            and not attack_removed
        ):
            injector.remove_phantoms(swarm)
            attack_removed = True
            print(f"\n✓ Phantoms removed at t={current_time:.1f}s")

        # Run detection if enabled
        detected_uavs = set()
        if detectors:
            graph = swarm.get_graph()
            for detector in detectors.values():
                result = detector.detect(graph)
                detected_uavs.update(result.anomalous_uav_ids)

        # Clear and redraw
        ax_main.clear()
        ax_main.set_xlim(0, swarm.bounds[0])
        ax_main.set_ylim(0, swarm.bounds[1])
        ax_main.set_xlabel("X Position (meters)", fontsize=11)
        ax_main.set_ylabel("Y Position (meters)", fontsize=11)
        ax_main.set_title(
            "UAV Swarm - Live Simulation with Attack Visualization", fontsize=13
        )
        ax_main.grid(True, alpha=0.3)
        ax_main.set_aspect("equal")

        # Draw communication links
        for u, v in swarm.graph.edges():
            uav_u = swarm.uavs[u]
            uav_v = swarm.uavs[v]
            ax_main.plot(
                [uav_u.position[0], uav_v.position[0]],
                [uav_u.position[1], uav_v.position[1]],
                "gray",
                alpha=0.3,
                linewidth=0.5,
            )

        # Draw UAVs
        for uav_id, uav in swarm.uavs.items():
            x, y = uav.position[0], uav.position[1]

            # Determine color and marker based on UAV type
            if not uav.is_legitimate:
                # PHANTOM UAV - Always red X
                color = "red"
                marker = "X"
                size = 200
                edge_color = "darkred"
            elif uav.public_key is not None:
                # Legitimate with crypto - Blue circle
                color = "blue"
                marker = "o"
                size = 100
                edge_color = "darkblue"
            else:
                # Legitimate without crypto - Green circle
                color = "green"
                marker = "o"
                size = 100
                edge_color = "darkgreen"

            # Add yellow outline if detected as anomalous
            if uav_id in detected_uavs:
                edge_color = "yellow"
                linewidth = 3
            else:
                linewidth = 1.5

            ax_main.scatter(
                x,
                y,
                c=color,
                marker=marker,
                s=size,
                alpha=0.9,
                edgecolors=edge_color,
                linewidth=linewidth,
                zorder=10,  # Draw UAVs on top of links
            )

            # Label phantoms and detected UAVs
            if not uav.is_legitimate or uav_id in detected_uavs:
                ax_main.text(
                    x,
                    y + 25,
                    uav_id,
                    fontsize=8,
                    ha="center",
                    fontweight="bold" if not uav.is_legitimate else "normal",
                )

        # Update statistics tracking
        stats = swarm.get_statistics()
        time_history.append(current_time)
        edge_history.append(stats["num_edges"])
        num_phantoms = sum(1 for u in swarm.uavs.values() if not u.is_legitimate)
        phantom_count_history.append(num_phantoms)
        detection_count_history.append(len(detected_uavs))

        # Draw statistics
        ax_stats.clear()

        # Plot 1: Edges and UAV count
        ax_stats_1 = ax_stats
        color_edges = "tab:blue"
        ax_stats_1.set_xlabel("Time (seconds)", fontsize=10)
        ax_stats_1.set_ylabel("Network Edges", color=color_edges, fontsize=10)
        ax_stats_1.plot(
            time_history, edge_history, color=color_edges, linewidth=2, label="Edges"
        )
        ax_stats_1.tick_params(axis="y", labelcolor=color_edges)
        ax_stats_1.grid(True, alpha=0.3)

        # Plot 2: Phantom count
        ax_stats_2 = ax_stats_1.twinx()
        color_phantoms = "tab:red"
        ax_stats_2.set_ylabel("Phantom UAVs", color=color_phantoms, fontsize=10)
        ax_stats_2.plot(
            time_history,
            phantom_count_history,
            color=color_phantoms,
            linewidth=2,
            label="Phantoms",
        )
        ax_stats_2.tick_params(axis="y", labelcolor=color_phantoms)

        # Highlight attack window
        if (
            time_history
            and attack.start_time <= current_time < attack.start_time + attack.duration
        ):
            ax_stats_1.axvspan(
                attack.start_time,
                attack.start_time + attack.duration,
                alpha=0.2,
                color="red",
            )

        ax_stats_1.set_title("Network Statistics Over Time", fontsize=11)

        # Add status text
        status_text = f"Frame: {frame}\n"
        status_text += f"Time: {current_time:.1f}s\n"
        status_text += f"Legitimate: {stats['num_uavs'] - num_phantoms}\n"
        status_text += f"Phantoms: {num_phantoms}\n"
        status_text += f"Total UAVs: {stats['num_uavs']}\n"
        status_text += f"Links: {stats['num_edges']}\n"
        if detectors:
            status_text += f"Detected: {len(detected_uavs)}"

        ax_main.text(
            0.02,
            0.02,
            status_text,
            transform=ax_main.transAxes,
            fontsize=10,
            verticalalignment="bottom",
            bbox=dict(boxstyle="round", facecolor="lightyellow", alpha=0.9),
        )

        # Add legend
        legend_elements = [
            Patch(facecolor="green", edgecolor="darkgreen", label="Legitimate UAV"),
        ]
        if enable_crypto:
            legend_elements.append(
                Patch(
                    facecolor="blue", edgecolor="darkblue", label="Legitimate (crypto)"
                )
            )
        legend_elements.append(
            Patch(facecolor="red", edgecolor="darkred", label="Phantom UAV")
        )
        if detectors:
            legend_elements.append(
                Patch(
                    facecolor="white", edgecolor="yellow", linewidth=3, label="Detected"
                )
            )

        ax_main.legend(handles=legend_elements, loc="upper right", fontsize=10)

        # Step simulation
        swarm.step(dt=1.0)

    # Create animation
    from matplotlib.animation import FuncAnimation

    # IMPORTANT: Assign to variable to prevent garbage collection
    _ = FuncAnimation(
        fig,
        update,
        frames=120,
        interval=200,  # 200ms per frame
        blit=False,
        repeat=False,
    )

    plt.tight_layout()
    plt.show()

    print("\n✅ Visualization complete!")
    print("\nFinal stats:")
    print(
        f"  • Legitimate UAVs: {sum(1 for u in swarm.uavs.values() if u.is_legitimate)}"
    )
    print(
        f"  • Phantom UAVs: {sum(1 for u in swarm.uavs.values() if not u.is_legitimate)}"
    )
    if detectors and detection_count_history:
        print(f"  • Last detection count: {detection_count_history[-1]}")


if __name__ == "__main__":
    main()
