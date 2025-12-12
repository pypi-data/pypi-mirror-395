"""
Remote ID message protocol implementation.

Based on FAA 14 CFR Part 89 Remote ID standard for UAV identification.
"""

import struct
from dataclasses import dataclass
from typing import Optional


@dataclass
class RemoteIDMessage:
    """
    Remote ID broadcast message containing UAV identification and telemetry.

    Attributes:
        uav_id: Identifier of broadcasting UAV
        timestamp: Unix timestamp when message was created
        latitude: GPS latitude in degrees (-90 to 90)
        longitude: GPS longitude in degrees (-180 to 180)
        altitude: Altitude in meters (MSL or AGL)
        velocity: Velocity vector (vx, vy, vz) in m/s
        signature: Ed25519 signature (64 bytes) if crypto enabled
        is_spoofed: Ground truth label for evaluation
    """

    uav_id: str
    timestamp: float
    latitude: float
    longitude: float
    altitude: float
    velocity: tuple[float, float, float]
    signature: Optional[bytes] = None
    is_spoofed: bool = False

    def __post_init__(self):
        """Validate message fields."""
        if not (-90 <= self.latitude <= 90):
            raise ValueError(f"Latitude {self.latitude} out of range [-90, 90]")

        if not (-180 <= self.longitude <= 180):
            raise ValueError(f"Longitude {self.longitude} out of range [-180, 180]")

        if self.altitude < 0:
            raise ValueError(f"Altitude {self.altitude} must be >= 0")

        if self.signature is not None and len(self.signature) != 64:
            raise ValueError(
                f"Signature must be exactly 64 bytes, got {len(self.signature)}"
            )

    def to_bytes(self) -> bytes:
        """
        Serialize message for signing or transmission.

        Returns:
            Byte representation of message (without signature field)

        Format: timestamp (8), lat (8), lon (8), alt (8), vx (8), vy (8), vz (8), id (variable)
        """
        # Pack numeric fields
        numeric_bytes = struct.pack(
            "ddddddd",  # 7 doubles (8 bytes each)
            self.timestamp,
            self.latitude,
            self.longitude,
            self.altitude,
            self.velocity[0],
            self.velocity[1],
            self.velocity[2],
        )

        # Append UAV ID
        id_bytes = self.uav_id.encode("utf-8")

        return numeric_bytes + id_bytes

    @classmethod
    def from_bytes(cls, data: bytes) -> "RemoteIDMessage":
        """
        Deserialize message from bytes.

        Args:
            data: Serialized message bytes

        Returns:
            RemoteIDMessage instance
        """
        # Unpack numeric fields (56 bytes)
        numeric_data = struct.unpack("ddddddd", data[:56])

        # Extract UAV ID
        uav_id = data[56:].decode("utf-8")

        return cls(
            uav_id=uav_id,
            timestamp=numeric_data[0],
            latitude=numeric_data[1],
            longitude=numeric_data[2],
            altitude=numeric_data[3],
            velocity=(numeric_data[4], numeric_data[5], numeric_data[6]),
            signature=None,
            is_spoofed=False,
        )

    def verify_signature(self, public_key: bytes) -> bool:
        """
        Verify message signature using public key.

        Args:
            public_key: Ed25519 public key (32 bytes)

        Returns:
            True if signature is valid, False otherwise
        """
        if self.signature is None:
            return False

        from argus_uav.crypto.ed25519_signer import Ed25519Signer

        return Ed25519Signer.verify(self.to_bytes(), self.signature, public_key)

    def __repr__(self) -> str:
        """String representation for debugging."""
        signed = "signed" if self.signature is not None else "unsigned"
        spoofed = "SPOOFED" if self.is_spoofed else "legit"
        return (
            f"RemoteID({self.uav_id}, "
            f"lat={self.latitude:.6f}, lon={self.longitude:.6f}, "
            f"alt={self.altitude:.1f}m, {signed}, {spoofed})"
        )
