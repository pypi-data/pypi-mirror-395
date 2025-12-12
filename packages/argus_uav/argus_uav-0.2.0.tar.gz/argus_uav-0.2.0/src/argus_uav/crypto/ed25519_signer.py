"""
Ed25519 digital signature implementation for Remote ID authentication.

Provides fast signing and verification with 256-bit security level.
"""

from typing import Tuple

from Crypto.PublicKey import ECC
from Crypto.Signature import eddsa


class Ed25519Signer:
    """
    Ed25519 digital signature manager for Remote ID message authentication.

    Ed25519 provides:
    - Fast signing (~0.05ms per message)
    - Fast verification (~0.1ms per message)
    - Small keys (32 bytes) and signatures (64 bytes)
    - 256-bit security level
    """

    @staticmethod
    def generate_keypair() -> Tuple[bytes, bytes]:
        """
        Generate Ed25519 key pair.

        Returns:
            Tuple of (private_key, public_key) as DER-encoded bytes

        Example:
            >>> priv_key, pub_key = Ed25519Signer.generate_keypair()
            >>> len(priv_key) > 0, len(pub_key) > 0
            (True, True)
        """
        # Generate ECC key on Ed25519 curve
        key = ECC.generate(curve="ed25519")

        # Export private key in DER format
        private_key = key.export_key(format="DER")

        # Export public key in DER format
        public_key = key.public_key().export_key(format="DER")

        return private_key, public_key

    @staticmethod
    def sign(message: bytes, private_key: bytes) -> bytes:
        """
        Sign message with Ed25519 private key.

        Args:
            message: Raw message bytes to sign
            private_key: DER-encoded Ed25519 private key

        Returns:
            64-byte signature

        Raises:
            ValueError: If private key is invalid

        Example:
            >>> priv_key, _ = Ed25519Signer.generate_keypair()
            >>> signature = Ed25519Signer.sign(b"test message", priv_key)
            >>> len(signature)
            64
        """
        # Import private key (DER format)
        key = ECC.import_key(private_key)

        # Create signer
        signer = eddsa.new(key, "rfc8032")

        # Sign message
        signature = signer.sign(message)

        return signature

    @staticmethod
    def verify(message: bytes, signature: bytes, public_key: bytes) -> bool:
        """
        Verify Ed25519 signature authenticity.

        Args:
            message: Raw message bytes
            signature: 64-byte Ed25519 signature
            public_key: DER-encoded Ed25519 public key

        Returns:
            True if signature is valid, False otherwise

        Example:
            >>> priv_key, pub_key = Ed25519Signer.generate_keypair()
            >>> message = b"test message"
            >>> signature = Ed25519Signer.sign(message, priv_key)
            >>> Ed25519Signer.verify(message, signature, pub_key)
            True
            >>> Ed25519Signer.verify(b"wrong message", signature, pub_key)
            False
        """
        if len(signature) != 64:
            raise ValueError(f"Signature must be 64 bytes, got {len(signature)}")

        try:
            # Import public key (DER format)
            key = ECC.import_key(public_key)

            # Create verifier
            verifier = eddsa.new(key, "rfc8032")

            # Verify signature
            verifier.verify(message, signature)
            return True

        except (ValueError, TypeError):
            # Signature verification failed
            return False

    @staticmethod
    def batch_verify(
        messages: list[bytes], signatures: list[bytes], public_keys: list[bytes]
    ) -> list[bool]:
        """
        Verify multiple signatures (optimized batch operation).

        Args:
            messages: List of raw message bytes
            signatures: List of 64-byte signatures
            public_keys: List of 32-byte public keys

        Returns:
            List of verification results (True/False for each message)

        Note:
            Currently implements sequential verification.
            Future optimization: parallel verification or batch algorithms.
        """
        if not (len(messages) == len(signatures) == len(public_keys)):
            raise ValueError(
                "Messages, signatures, and public keys must have same length"
            )

        results = []
        for msg, sig, pub_key in zip(messages, signatures, public_keys):
            results.append(Ed25519Signer.verify(msg, sig, pub_key))

        return results
