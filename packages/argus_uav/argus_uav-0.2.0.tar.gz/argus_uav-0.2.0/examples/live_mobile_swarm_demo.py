#!/usr/bin/env python3
"""
Live visualization of mobile swarms with real-time attack detection.

Shows UAVs moving to destinations while detectors analyze for attacks.
"""

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from matplotlib.animation import FuncAnimation

from argus_uav.attacks import AttackScenario, AttackType
from argus_uav.attacks.phantom_uav import PhantomInjector
from argus_uav.core.swarm import Swarm
from argus_uav.detection.centrality import CentralityDetector
from argus_uav.detection.crypto_detector import CryptoDetector
from argus_uav.detection.ml_detection import Node2VecDetector
from argus_uav.detection.spectral import SpectralDetector


class LiveMobileSwarmViz:
    """Live visualization of mobile swarm with attack detection."""

    def __init__(self, num_uavs=20, attack_type=AttackType.PHANTOM):
        self.rng = np.random.default_rng(seed=42)
        self.swarm = Swarm(
            num_uavs=num_uavs,
            comm_range=100.0,
            bounds=(1000, 1000, 200),
            rng=self.rng,
            enable_crypto=True,
        )

        self.attack_type = attack_type
        self.attack_active = False
        self.attack_start_time = 15.0

        # Assign destinations
        self._assign_destinations()

        # Collect baseline
        print("Collecting baseline...")
        baseline_graphs = []
        for _ in range(30):
            self._update_velocities()
            self.swarm.step(dt=1.0)
            baseline_graphs.append(self.swarm.get_graph().copy())

        # Initialize detectors
        print("Initializing detectors...")
        self.detectors = {
            "Spectral": SpectralDetector(threshold=2.5),
            "Centrality": CentralityDetector(threshold=2.5),
            "ML": Node2VecDetector(contamination=0.08, score_threshold=0.75),
            "Crypto": CryptoDetector(),
        }

        for detector in self.detectors.values():
            detector.train(baseline_graphs)

        # Setup visualization
        self.fig, self.axes = plt.subplots(2, 2, figsize=(16, 12))
        self.fig.suptitle("Live Mobile Swarm Detection", fontsize=16, fontweight="bold")

        self.current_time = 0.0
        self.detection_history = {
            name: {"tpr": [], "fpr": []} for name in self.detectors.keys()
        }

    def _assign_destinations(self):
        """Assign random destinations to all UAVs."""
        for uav in self.swarm.uavs.values():
            dest = (
                float(self.rng.uniform(100, 900)),
                float(self.rng.uniform(100, 900)),
                float(self.rng.uniform(20, 180)),
            )
            uav.destination = dest

            # Set velocity toward destination
            dx = dest[0] - uav.position[0]
            dy = dest[1] - uav.position[1]
            dz = dest[2] - uav.position[2]
            dist = np.sqrt(dx**2 + dy**2 + dz**2)

            if dist > 0:
                speed = 10.0
                uav.velocity = (speed * dx / dist, speed * dy / dist, speed * dz / dist)

    def _update_velocities(self):
        """Update UAV velocities toward destinations."""
        for uav in self.swarm.uavs.values():
            if not hasattr(uav, "destination"):
                continue

            dx = uav.destination[0] - uav.position[0]
            dy = uav.destination[1] - uav.position[1]
            dz = uav.destination[2] - uav.position[2]
            dist = np.sqrt(dx**2 + dy**2 + dz**2)

            # Reassign destination if close
            if dist < 50:
                dest = (
                    float(self.rng.uniform(100, 900)),
                    float(self.rng.uniform(100, 900)),
                    float(self.rng.uniform(20, 180)),
                )
                uav.destination = dest
                dx = dest[0] - uav.position[0]
                dy = dest[1] - uav.position[1]
                dz = dest[2] - uav.position[2]
                dist = np.sqrt(dx**2 + dy**2 + dz**2)

            if dist > 0:
                speed = 10.0 + float(self.rng.uniform(-2, 2))
                uav.velocity = (speed * dx / dist, speed * dy / dist, speed * dz / dist)

    def _inject_attack(self):
        """Inject attack at specified time."""
        if self.attack_type == AttackType.PHANTOM:
            attack = AttackScenario(
                attack_type=AttackType.PHANTOM,
                start_time=self.attack_start_time,
                duration=100.0,
                phantom_count=3,
            )
            injector = PhantomInjector()
            injector.inject(self.swarm, attack, self.attack_start_time)
            print(f"✗ PHANTOM ATTACK injected at t={self.attack_start_time:.1f}s")

    def update(self, frame):
        """Update animation frame."""
        # Update simulation
        self._update_velocities()
        self.swarm.step(dt=1.0)
        self.current_time += 1.0

        # Inject attack
        if not self.attack_active and self.current_time >= self.attack_start_time:
            self._inject_attack()
            self.attack_active = True

        # Get current graph
        graph = self.swarm.get_graph()

        # Run detectors
        results = {}
        for name, detector in self.detectors.items():
            result = detector.detect(graph)
            results[name] = result

            if self.attack_active:
                metrics = result.compute_metrics()
                self.detection_history[name]["tpr"].append(metrics["tpr"] * 100)
                self.detection_history[name]["fpr"].append(metrics["fpr"] * 100)

        # Clear all axes
        for ax in self.axes.flat:
            ax.clear()

        # Panel 1: Swarm positions (top-left)
        ax_swarm = self.axes[0, 0]
        ax_swarm.set_xlim(0, 1000)
        ax_swarm.set_ylim(0, 1000)
        ax_swarm.set_aspect("equal")
        ax_swarm.set_title(
            f"Swarm Movement (t={self.current_time:.1f}s)", fontweight="bold"
        )
        ax_swarm.set_xlabel("X (m)")
        ax_swarm.set_ylabel("Y (m)")
        ax_swarm.grid(True, alpha=0.3)

        # Draw edges
        for u, v in graph.edges():
            u_data = graph.nodes[u]
            v_data = graph.nodes[v]
            if "uav" in u_data and "uav" in v_data:
                u_pos = u_data["uav"].position
                v_pos = v_data["uav"].position
                ax_swarm.plot(
                    [u_pos[0], v_pos[0]],
                    [u_pos[1], v_pos[1]],
                    "gray",
                    alpha=0.3,
                    linewidth=0.5,
                    zorder=1,
                )

        # Draw UAVs
        for node in graph.nodes():
            node_data = graph.nodes[node]
            if "uav" not in node_data:
                continue

            uav = node_data["uav"]
            pos = uav.position

            # Determine color based on detection
            is_detected = any(
                node in results[name].anomalous_uav_ids
                for name in self.detectors.keys()
            )

            if not uav.is_legitimate:
                color = "red" if is_detected else "darkred"
                marker = "X"
                size = 200
            else:
                color = "orange" if is_detected else "blue"
                marker = "o"
                size = 100

            ax_swarm.scatter(
                pos[0],
                pos[1],
                c=color,
                marker=marker,
                s=size,
                edgecolors="black",
                linewidths=2,
                zorder=3,
                alpha=0.8,
            )

            # Draw destination
            if hasattr(uav, "destination") and uav.is_legitimate:
                dest = uav.destination
                ax_swarm.plot(
                    [pos[0], dest[0]],
                    [pos[1], dest[1]],
                    "b--",
                    alpha=0.2,
                    linewidth=1,
                    zorder=2,
                )
                ax_swarm.scatter(
                    dest[0],
                    dest[1],
                    c="lightblue",
                    marker="*",
                    s=50,
                    alpha=0.5,
                    zorder=2,
                )

        # Legend
        if self.attack_active:
            ax_swarm.text(
                0.02,
                0.98,
                "⚠️ ATTACK ACTIVE",
                transform=ax_swarm.transAxes,
                fontsize=12,
                fontweight="bold",
                color="red",
                verticalalignment="top",
                bbox=dict(boxstyle="round", facecolor="yellow", alpha=0.7),
            )

        # Panel 2: Network graph (top-right)
        ax_graph = self.axes[0, 1]
        ax_graph.set_title("Communication Graph", fontweight="bold")
        ax_graph.axis("off")

        pos_dict = {}
        node_colors = []
        for node in graph.nodes():
            node_data = graph.nodes[node]
            if "uav" in node_data:
                uav = node_data["uav"]
                pos_dict[node] = (uav.position[0], uav.position[1])

                is_detected = any(
                    node in results[name].anomalous_uav_ids
                    for name in self.detectors.keys()
                )

                if not uav.is_legitimate:
                    node_colors.append("red" if is_detected else "darkred")
                else:
                    node_colors.append("orange" if is_detected else "lightblue")

        if pos_dict:
            nx.draw(
                graph,
                pos=pos_dict,
                ax=ax_graph,
                node_color=node_colors,
                node_size=100,
                edge_color="gray",
                alpha=0.6,
                width=0.5,
                with_labels=False,
            )

        # Panel 3: TPR over time (bottom-left)
        ax_tpr = self.axes[1, 0]
        ax_tpr.set_title("True Positive Rate Over Time", fontweight="bold")
        ax_tpr.set_xlabel("Time since attack (s)")
        ax_tpr.set_ylabel("TPR (%)")
        ax_tpr.set_ylim([-5, 105])
        ax_tpr.grid(True, alpha=0.3)

        if self.attack_active and any(
            len(v["tpr"]) > 0 for v in self.detection_history.values()
        ):
            colors = {
                "Spectral": "green",
                "Centrality": "red",
                "ML": "orange",
                "Crypto": "blue",
            }
            for name, history in self.detection_history.items():
                if history["tpr"]:
                    times = list(range(len(history["tpr"])))
                    ax_tpr.plot(
                        times,
                        history["tpr"],
                        label=name,
                        color=colors.get(name, "gray"),
                        linewidth=2,
                        marker="o",
                        markersize=4,
                    )

            ax_tpr.legend(loc="lower right")
            ax_tpr.axhline(
                y=100, color="green", linestyle="--", alpha=0.3, label="Perfect"
            )
        else:
            ax_tpr.text(
                0.5,
                0.5,
                "Waiting for attack...",
                transform=ax_tpr.transAxes,
                ha="center",
                va="center",
                fontsize=12,
                color="gray",
            )

        # Panel 4: FPR over time (bottom-right)
        ax_fpr = self.axes[1, 1]
        ax_fpr.set_title("False Positive Rate Over Time", fontweight="bold")
        ax_fpr.set_xlabel("Time since attack (s)")
        ax_fpr.set_ylabel("FPR (%)")
        ax_fpr.set_ylim([-5, 70])
        ax_fpr.grid(True, alpha=0.3)

        if self.attack_active and any(
            len(v["fpr"]) > 0 for v in self.detection_history.values()
        ):
            colors = {
                "Spectral": "green",
                "Centrality": "red",
                "ML": "orange",
                "Crypto": "blue",
            }
            for name, history in self.detection_history.items():
                if history["fpr"]:
                    times = list(range(len(history["fpr"])))
                    ax_fpr.plot(
                        times,
                        history["fpr"],
                        label=name,
                        color=colors.get(name, "gray"),
                        linewidth=2,
                        marker="o",
                        markersize=4,
                    )

            ax_fpr.legend(loc="upper right")
            ax_fpr.axhline(
                y=0, color="green", linestyle="--", alpha=0.3, label="Perfect"
            )
        else:
            ax_fpr.text(
                0.5,
                0.5,
                "Waiting for attack...",
                transform=ax_fpr.transAxes,
                ha="center",
                va="center",
                fontsize=12,
                color="gray",
            )

        plt.tight_layout()

        return self.axes.flat

    def run(self, frames=100, interval=200):
        """Run live visualization."""
        print("\n🎬 Starting live visualization...")
        print(
            "Watch as UAVs move toward destinations while detectors analyze for attacks!"
        )

        _ = FuncAnimation(
            self.fig,
            self.update,
            frames=frames,
            interval=interval,
            blit=False,
            repeat=False,
        )

        plt.show()

        # Print final stats
        if self.attack_active:
            print("\n📊 Final Detection Statistics:")
            for name, history in self.detection_history.items():
                if history["tpr"]:
                    avg_tpr = np.mean(history["tpr"])
                    avg_fpr = np.mean(history["fpr"])
                    print(f"  {name:12s}: TPR={avg_tpr:5.1f}%  FPR={avg_fpr:5.1f}%")


def main():
    """Run live mobile swarm visualization."""
    print("=" * 70)
    print("LIVE MOBILE SWARM VISUALIZATION")
    print("=" * 70)
    print("\nThis demo shows:")
    print("  • UAVs moving toward random destinations")
    print("  • Real-time attack detection (Phantom attack at t=15s)")
    print("  • 4 detectors analyzing in parallel")
    print("  • TPR/FPR evolution over time")
    print("=" * 70)

    viz = LiveMobileSwarmViz(num_uavs=20, attack_type=AttackType.PHANTOM)
    viz.run(frames=50, interval=200)  # 200ms per frame = ~5 FPS


if __name__ == "__main__":
    main()
