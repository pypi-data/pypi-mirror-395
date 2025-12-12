"""
Phantom UAV attack injection.

Injects non-existent UAVs broadcasting fake Remote ID messages into the swarm.
"""

from typing import TYPE_CHECKING

from argus_uav.attacks import AttackInjector, AttackScenario
from argus_uav.core.uav import UAV
from argus_uav.utils.logging_config import get_logger

if TYPE_CHECKING:
    from argus_uav.core.swarm import Swarm

logger = get_logger(__name__)


class PhantomInjector(AttackInjector):
    """
    Injects phantom (non-existent) UAVs broadcasting fake Remote ID messages.

    Phantom UAVs appear in the swarm graph but are not legitimate aircraft.
    They disrupt network topology and can mislead consensus algorithms.
    """

    def __init__(self):
        """Initialize phantom injector."""
        super().__init__()
        self.phantom_ids: set[str] = set()
        self.injected = False

    def inject(
        self, swarm: "Swarm", scenario: AttackScenario, current_time: float
    ) -> None:
        """
        Inject phantom UAVs into swarm graph.

        Args:
            swarm: Target swarm to attack
            scenario: Attack configuration
            current_time: Current simulation time

        Effects:
            - Creates N phantom UAVs with random positions
            - Adds them to swarm graph
            - Marks them as illegitimate in ground truth
        """
        # Only inject once at attack start
        if self.injected:
            return

        # Get swarm bounds and RNG
        bounds = swarm.bounds
        rng = swarm.rng

        # Create phantom UAVs
        for i in range(scenario.phantom_count):
            phantom_id = f"PHANTOM-{i:03d}"

            # Random position within bounds
            position = (
                float(rng.uniform(0, bounds[0])),
                float(rng.uniform(0, bounds[1])),
                float(rng.uniform(0, bounds[2])),
            )

            # Random velocity (phantoms move too)
            max_speed = 15.0
            velocity = (
                float(rng.uniform(-max_speed, max_speed)),
                float(rng.uniform(-max_speed, max_speed)),
                float(rng.uniform(-max_speed / 2, max_speed / 2)),
            )

            # Create phantom UAV (marked as illegitimate)
            phantom = UAV(
                uav_id=phantom_id,
                position=position,
                velocity=velocity,
                is_legitimate=False,  # Key difference!
            )

            # Add to swarm
            swarm.add_uav(phantom)
            self.phantom_ids.add(phantom_id)

            logger.info(f"Injected phantom UAV {phantom_id} at position {position}")

        # Update ground truth for all UAVs
        self._update_ground_truth(swarm)

        self.injected = True
        logger.info(f"Phantom attack: injected {scenario.phantom_count} phantom UAVs")

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

    def remove_phantoms(self, swarm: "Swarm") -> None:
        """
        Remove all injected phantom UAVs from swarm.

        Args:
            swarm: Swarm to remove phantoms from
        """
        for phantom_id in self.phantom_ids:
            if phantom_id in swarm.uavs:
                swarm.remove_uav(phantom_id)
                logger.debug(f"Removed phantom UAV {phantom_id}")

        self.phantom_ids.clear()
        self.injected = False
        logger.info("All phantom UAVs removed")
