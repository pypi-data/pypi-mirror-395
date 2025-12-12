"""
Coordinated multi-spoofer attack.

Multiple synchronized phantom UAVs with coordinated movement patterns
to form a believable sub-swarm.
"""

from typing import TYPE_CHECKING

import numpy as np

from argus_uav.attacks import AttackInjector, AttackScenario
from argus_uav.core.uav import UAV
from argus_uav.utils.logging_config import get_logger

if TYPE_CHECKING:
    from argus_uav.core.swarm import Swarm

logger = get_logger(__name__)


class CoordinatedInjector(AttackInjector):
    """
    Injects multiple coordinated phantom UAVs with synchronized behavior.

    Creates a group of phantom UAVs that move together in formation,
    making them harder to detect than random phantoms.
    """

    def __init__(self):
        """Initialize coordinated injector."""
        super().__init__()
        self.phantom_ids: set[str] = set()
        self.formation_center: tuple[float, float, float] = (0, 0, 0)
        self.formation_velocity: tuple[float, float, float] = (0, 0, 0)
        self.injected = False

    def inject(
        self, swarm: "Swarm", scenario: AttackScenario, current_time: float
    ) -> None:
        """
        Inject coordinated phantom UAVs into swarm.

        Args:
            swarm: Target swarm to attack
            scenario: Attack configuration
            current_time: Current simulation time

        Effects:
            - Creates N phantom UAVs in formation
            - Gives them coordinated movement
            - Adds them to swarm graph
        """
        # Only inject once at attack start
        if self.injected:
            return

        bounds = swarm.bounds
        rng = swarm.rng

        # Choose formation center (random location in swarm space)
        self.formation_center = (
            float(rng.uniform(bounds[0] * 0.2, bounds[0] * 0.8)),
            float(rng.uniform(bounds[1] * 0.2, bounds[1] * 0.8)),
            float(rng.uniform(bounds[2] * 0.3, bounds[2] * 0.7)),
        )

        # Choose formation velocity (all move together)
        speed = 10.0  # m/s
        direction = rng.uniform(0, 2 * np.pi)
        self.formation_velocity = (
            float(speed * np.cos(direction)),
            float(speed * np.sin(direction)),
            0.0,  # Minimal vertical movement
        )

        # Create phantoms in formation
        formation_radius = 50.0  # meters
        pattern = scenario.coordination_pattern or "circle"

        for i in range(scenario.phantom_count):
            phantom_id = f"COORDINATED-{i:03d}"

            # Position relative to formation center
            if pattern == "circle":
                angle = 2 * np.pi * i / scenario.phantom_count
                offset_x = formation_radius * np.cos(angle)
                offset_y = formation_radius * np.sin(angle)
                offset_z = 0
            elif pattern == "line":
                spacing = 30.0  # meters between UAVs
                offset_x = spacing * i - (spacing * scenario.phantom_count / 2)
                offset_y = 0
                offset_z = 0
            else:  # random but close
                offset_x = rng.uniform(-formation_radius, formation_radius)
                offset_y = rng.uniform(-formation_radius, formation_radius)
                offset_z = rng.uniform(-10, 10)

            position = (
                self.formation_center[0] + offset_x,
                self.formation_center[1] + offset_y,
                self.formation_center[2] + offset_z,
            )

            # All have same velocity (coordinated movement)
            velocity = self.formation_velocity

            # Create phantom UAV
            phantom = UAV(
                uav_id=phantom_id,
                position=position,
                velocity=velocity,
                is_legitimate=False,
            )

            # Add to swarm
            swarm.add_uav(phantom)
            self.phantom_ids.add(phantom_id)

            logger.debug(f"Injected coordinated phantom {phantom_id} at {position}")

        # Update ground truth
        self._update_ground_truth(swarm)

        self.injected = True
        logger.info(
            f"Coordinated attack: injected {scenario.phantom_count} phantoms "
            f"in {pattern} formation at {self.formation_center}"
        )

    def _update_ground_truth(self, swarm: "Swarm") -> None:
        """Update ground truth labels for all UAVs."""
        self.ground_truth = {
            uav_id: uav.is_legitimate for uav_id, uav in swarm.uavs.items()
        }

    def get_ground_truth(self) -> dict[str, bool]:
        """
        Returns ground truth labels for all UAVs.

        Returns:
            Mapping of UAV ID to is_legitimate flag
        """
        return self.ground_truth.copy()

    def remove_coordinated(self, swarm: "Swarm") -> None:
        """
        Remove all coordinated phantom UAVs from swarm.

        Args:
            swarm: Swarm to remove phantoms from
        """
        for phantom_id in self.phantom_ids:
            if phantom_id in swarm.uavs:
                swarm.remove_uav(phantom_id)

        self.phantom_ids.clear()
        self.injected = False
        logger.info("All coordinated phantoms removed")
