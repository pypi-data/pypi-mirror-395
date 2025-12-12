"""
UAV (Unmanned Aerial Vehicle) node representation.

Represents individual UAVs in the swarm with position, velocity, and cryptographic identity.
"""

import time
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from argus_uav.core.remote_id import RemoteIDMessage


@dataclass
class UAV:
    """
    Single UAV agent with position, velocity, and cryptographic identity.

    Attributes:
        uav_id: Unique identifier (UUID or sequential ID)
        position: 3D coordinates (x, y, z) in meters
        velocity: Velocity vector (vx, vy, vz) in m/s
        is_legitimate: Ground truth label (True=real, False=phantom)
        private_key: Ed25519 private key (32 bytes) for signing
        public_key: Ed25519 public key (32 bytes) for verification
        last_update: Timestamp of last state update
        message_queue: Recent broadcast messages
    """

    uav_id: str
    position: tuple[float, float, float]
    velocity: tuple[float, float, float]
    is_legitimate: bool = True
    private_key: Optional[bytes] = None
    public_key: Optional[bytes] = None
    last_update: float = field(default_factory=time.time)
    message_queue: list = field(default_factory=list)

    def move(self, dt: float, bounds: tuple[float, float, float]) -> None:
        """
        Update position based on velocity with boundary reflection.

        Args:
            dt: Time delta in seconds
            bounds: Simulation boundaries (x_max, y_max, z_max)

        Boundaries use reflection: UAV bounces off walls by reversing velocity component.
        """
        x, y, z = self.position
        vx, vy, vz = self.velocity
        x_max, y_max, z_max = bounds

        # Update position
        x += vx * dt
        y += vy * dt
        z += vz * dt

        # Boundary reflection
        if x < 0 or x > x_max:
            vx = -vx
            x = max(0, min(x, x_max))

        if y < 0 or y > y_max:
            vy = -vy
            y = max(0, min(y, y_max))

        if z < 0 or z > z_max:
            vz = -vz
            z = max(0, min(z, z_max))

        self.position = (x, y, z)
        self.velocity = (vx, vy, vz)
        self.last_update = time.time()

    def broadcast_remote_id(self, timestamp: float) -> "RemoteIDMessage":
        """
        Create Remote ID message with current state.

        Args:
            timestamp: Current simulation time

        Returns:
            RemoteIDMessage with UAV telemetry
        """
        from argus_uav.core.remote_id import RemoteIDMessage

        # For simplicity, use position as lat/lon/alt
        # In real implementation, would convert from local coordinates
        x, y, z = self.position

        message = RemoteIDMessage(
            uav_id=self.uav_id,
            timestamp=timestamp,
            latitude=y / 111000.0,  # Rough conversion to degrees (for simulation)
            longitude=x / 111000.0,
            altitude=z,
            velocity=self.velocity,
            signature=None,
            is_spoofed=not self.is_legitimate,
        )

        self.message_queue.append(message)
        return message

    def sign_message(self, message: "RemoteIDMessage") -> None:
        """
        Sign message with private key (modifies message in-place).

        Args:
            message: RemoteIDMessage to sign

        Raises:
            ValueError: If private key not set
        """
        if self.private_key is None:
            raise ValueError(f"UAV {self.uav_id} has no private key for signing")

        from argus_uav.crypto.ed25519_signer import Ed25519Signer

        message_bytes = message.to_bytes()
        message.signature = Ed25519Signer.sign(message_bytes, self.private_key)

    def __repr__(self) -> str:
        """String representation for debugging."""
        pos_str = (
            f"({self.position[0]:.1f}, {self.position[1]:.1f}, {self.position[2]:.1f})"
        )
        legit_str = "legitimate" if self.is_legitimate else "PHANTOM"
        return f"UAV({self.uav_id}, pos={pos_str}, {legit_str})"
