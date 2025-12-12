"""
Live visualization of UAV swarm simulation.

Real-time animated plot showing UAV positions, connections, and attacks.
"""

# Set matplotlib backend to Qt5 for interactive plots
import matplotlib

matplotlib.use("QtAgg")

from typing import Callable, Optional

import matplotlib.animation as animation
import matplotlib.pyplot as plt


class LiveSwarmVisualizer:
    """
    Real-time visualization of UAV swarm.

    Creates animated plot showing:
    - UAV positions (3D projected to 2D)
    - Communication links (edges)
    - Attack status (color-coded)
    - Network statistics
    """

    def __init__(
        self,
        swarm,
        figsize: tuple[int, int] = (12, 10),
        update_interval: int = 100,  # milliseconds
    ):
        """
        Initialize live visualizer.

        Args:
            swarm: Swarm object to visualize
            figsize: Figure size (width, height)
            update_interval: Animation update interval in milliseconds
        """
        self.swarm = swarm
        self.update_interval = update_interval

        # Create figure with subplots
        self.fig = plt.figure(figsize=figsize)

        # Main plot: UAV positions and connections
        self.ax_main = plt.subplot2grid((3, 2), (0, 0), rowspan=2, colspan=2)

        # Statistics plots
        self.ax_stats1 = plt.subplot2grid((3, 2), (2, 0))
        self.ax_stats2 = plt.subplot2grid((3, 2), (2, 1))

        # Data tracking
        self.time_history = []
        self.edge_history = []
        self.uav_count_history = []

        # Animation
        self.anim = None
        self.frame_count = 0

        self._setup_plot()

    def _setup_plot(self):
        """Configure plot appearance."""
        # Main plot
        self.ax_main.set_xlim(0, self.swarm.bounds[0])
        self.ax_main.set_ylim(0, self.swarm.bounds[1])
        self.ax_main.set_xlabel("X Position (meters)", fontsize=11)
        self.ax_main.set_ylabel("Y Position (meters)", fontsize=11)
        self.ax_main.set_title("UAV Swarm Live Simulation", fontsize=13)
        self.ax_main.grid(True, alpha=0.3)
        self.ax_main.set_aspect("equal")

        # Stats plots
        self.ax_stats1.set_title("Network Edges", fontsize=10)
        self.ax_stats1.set_xlabel("Time (s)", fontsize=9)
        self.ax_stats1.set_ylabel("# Edges", fontsize=9)
        self.ax_stats1.grid(True, alpha=0.3)

        self.ax_stats2.set_title("UAV Count", fontsize=10)
        self.ax_stats2.set_xlabel("Time (s)", fontsize=9)
        self.ax_stats2.set_ylabel("# UAVs", fontsize=9)
        self.ax_stats2.grid(True, alpha=0.3)

    def _update_frame(self, frame):
        """Update animation frame."""
        # Call attack callback if provided
        if hasattr(self, "attack_callback") and self.attack_callback is not None:
            self.attack_callback(frame)

        # Clear main plot
        self.ax_main.clear()
        self._setup_plot()

        # Get current graph
        graph = self.swarm.get_graph()

        # Draw communication links (edges)
        for u, v in graph.edges():
            uav_u = self.swarm.uavs[u]
            uav_v = self.swarm.uavs[v]

            x_coords = [uav_u.position[0], uav_v.position[0]]
            y_coords = [uav_u.position[1], uav_v.position[1]]

            self.ax_main.plot(x_coords, y_coords, "gray", alpha=0.3, linewidth=0.5)

        # Draw UAVs
        for uav_id, uav in self.swarm.uavs.items():
            x, y = uav.position[0], uav.position[1]

            # Color code by legitimacy
            if uav.is_legitimate:
                if uav.public_key is not None:
                    color = "blue"  # Legitimate with crypto
                    marker = "o"
                    size = 80
                else:
                    color = "green"  # Legitimate without crypto
                    marker = "o"
                    size = 80
            else:
                color = "red"  # Phantom
                marker = "X"
                size = 150

            self.ax_main.scatter(
                x,
                y,
                c=color,
                marker=marker,
                s=size,
                alpha=0.8,
                edgecolors="black",
                linewidth=0.5,
            )

            # Label (show phantoms and every 10th UAV to avoid clutter)
            show_label = False
            if not uav.is_legitimate:
                show_label = True  # Always show phantom labels
            else:
                try:
                    uav_num = int(uav_id.split("-")[1])
                    if uav_num % 10 == 0:
                        show_label = True
                except (IndexError, ValueError):
                    pass  # Skip label if ID format unexpected

            if show_label:
                self.ax_main.text(x, y + 20, uav_id, fontsize=7, ha="center")

        # Update statistics
        stats = self.swarm.get_statistics()
        self.time_history.append(self.swarm.simulation_time)
        self.edge_history.append(stats["num_edges"])
        self.uav_count_history.append(stats["num_uavs"])

        # Update time series plots
        self.ax_stats1.clear()
        self.ax_stats1.plot(
            self.time_history, self.edge_history, "steelblue", linewidth=2
        )
        self.ax_stats1.set_title("Network Edges Over Time", fontsize=10)
        self.ax_stats1.set_xlabel("Time (s)", fontsize=9)
        self.ax_stats1.set_ylabel("# Edges", fontsize=9)
        self.ax_stats1.grid(True, alpha=0.3)

        self.ax_stats2.clear()
        self.ax_stats2.plot(
            self.time_history, self.uav_count_history, "darkgreen", linewidth=2
        )
        self.ax_stats2.axhline(
            y=self.swarm.num_uavs,
            color="green",
            linestyle="--",
            alpha=0.5,
            label="Initial count",
        )
        self.ax_stats2.set_title("UAV Count Over Time", fontsize=10)
        self.ax_stats2.set_xlabel("Time (s)", fontsize=9)
        self.ax_stats2.set_ylabel("# UAVs", fontsize=9)
        self.ax_stats2.legend(fontsize=8)
        self.ax_stats2.grid(True, alpha=0.3)

        # Add legend to main plot
        from matplotlib.patches import Patch

        legend_elements = [
            Patch(facecolor="green", label="Legitimate UAV"),
            Patch(facecolor="blue", label="Legitimate (crypto)"),
            Patch(facecolor="red", label="Phantom UAV"),
        ]
        self.ax_main.legend(handles=legend_elements, loc="upper right", fontsize=9)

        # Add statistics text
        num_phantoms = sum(
            1 for uav in self.swarm.uavs.values() if not uav.is_legitimate
        )
        num_legitimate = sum(1 for uav in self.swarm.uavs.values() if uav.is_legitimate)

        text_str = f"Time: {self.swarm.simulation_time:.1f}s\n"
        text_str += f"Legitimate: {num_legitimate}\n"
        text_str += f"Phantoms: {num_phantoms}\n"
        text_str += f"Links: {stats['num_edges']}\n"
        text_str += f"Avg Degree: {stats['avg_degree']:.2f}\n"
        text_str += f"Connected: {'Yes' if stats['is_connected'] else 'No'}"

        self.ax_main.text(
            0.02,
            0.98,
            text_str,
            transform=self.ax_main.transAxes,
            fontsize=10,
            verticalalignment="top",
            bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.8),
        )

        self.frame_count += 1

        # Step simulation for next frame
        self.swarm.step(dt=1.0)

    def animate(self, frames: int = 100, attack_callback: Optional[Callable] = None):
        """
        Run animation.

        Args:
            frames: Number of frames to animate
            attack_callback: Optional function called each frame for attack injection
        """
        # Store attack callback
        self.attack_callback = attack_callback

        # Create animation
        self.anim = animation.FuncAnimation(
            self.fig,
            self._update_frame,
            frames=frames,
            interval=self.update_interval,
            blit=False,
            repeat=False,
        )

        plt.tight_layout()
        plt.show()

    def save_animation(self, filename: str, frames: int = 100, fps: int = 10):
        """
        Save animation to video file.

        Args:
            filename: Output filename (.mp4, .gif)
            frames: Number of frames
            fps: Frames per second
        """
        self.anim = animation.FuncAnimation(
            self.fig,
            self._update_frame,
            frames=frames,
            interval=1000 // fps,
            blit=False,
        )

        # Save
        if filename.endswith(".gif"):
            self.anim.save(filename, writer="pillow", fps=fps)
        else:
            self.anim.save(filename, writer="ffmpeg", fps=fps, dpi=150)

        print(f"Animation saved to {filename}")
