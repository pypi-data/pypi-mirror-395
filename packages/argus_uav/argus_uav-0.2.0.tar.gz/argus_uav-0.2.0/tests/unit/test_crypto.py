"""
Unit tests for Ed25519 cryptographic signing.

Tests key generation, signing, verification, and performance.
"""

import time

import pytest

from argus_uav.crypto.ed25519_signer import Ed25519Signer


@pytest.mark.unit
def test_keypair_generation():
    """Test Ed25519 key pair generation."""
    priv_key, pub_key = Ed25519Signer.generate_keypair()

    assert isinstance(priv_key, bytes)
    assert isinstance(pub_key, bytes)
    # DER-encoded keys are larger than raw 32 bytes
    assert len(priv_key) > 32
    assert len(pub_key) > 32


@pytest.mark.unit
def test_message_signing():
    """Test Ed25519 message signing."""
    priv_key, _ = Ed25519Signer.generate_keypair()
    message = b"test message"

    signature = Ed25519Signer.sign(message, priv_key)

    assert isinstance(signature, bytes)
    assert len(signature) == 64


@pytest.mark.unit
def test_signature_verification():
    """Test Ed25519 signature verification."""
    priv_key, pub_key = Ed25519Signer.generate_keypair()
    message = b"test message"

    # Sign message
    signature = Ed25519Signer.sign(message, priv_key)

    # Verify with correct key
    assert Ed25519Signer.verify(message, signature, pub_key) is True


@pytest.mark.unit
def test_signature_verification_wrong_message():
    """Test signature verification fails for wrong message."""
    priv_key, pub_key = Ed25519Signer.generate_keypair()
    message = b"original message"

    signature = Ed25519Signer.sign(message, priv_key)

    # Verify with wrong message
    wrong_message = b"tampered message"
    assert Ed25519Signer.verify(wrong_message, signature, pub_key) is False


@pytest.mark.unit
def test_signature_verification_wrong_key():
    """Test signature verification fails with wrong public key."""
    priv_key1, pub_key1 = Ed25519Signer.generate_keypair()
    _, pub_key2 = Ed25519Signer.generate_keypair()
    message = b"test message"

    signature = Ed25519Signer.sign(message, priv_key1)

    # Verify with wrong key
    assert Ed25519Signer.verify(message, signature, pub_key2) is False


@pytest.mark.performance
def test_signing_performance():
    """Test Ed25519 signing completes in < 10ms."""
    priv_key, _ = Ed25519Signer.generate_keypair()
    message = b"test message" * 10

    # Warm-up
    Ed25519Signer.sign(message, priv_key)

    # Time 100 signatures
    start = time.time()
    for _ in range(100):
        Ed25519Signer.sign(message, priv_key)
    elapsed = time.time() - start

    avg_time = elapsed / 100
    assert avg_time < 0.010, f"Signing took {avg_time * 1000:.1f}ms (> 10ms)"


@pytest.mark.performance
def test_verification_performance():
    """Test Ed25519 verification completes in < 10ms."""
    priv_key, pub_key = Ed25519Signer.generate_keypair()
    message = b"test message" * 10
    signature = Ed25519Signer.sign(message, priv_key)

    # Warm-up
    Ed25519Signer.verify(message, signature, pub_key)

    # Time 100 verifications
    start = time.time()
    for _ in range(100):
        Ed25519Signer.verify(message, signature, pub_key)
    elapsed = time.time() - start

    avg_time = elapsed / 100
    assert avg_time < 0.010, f"Verification took {avg_time * 1000:.1f}ms (> 10ms)"


@pytest.mark.unit
def test_batch_verify():
    """Test batch signature verification."""
    # Generate multiple key pairs and messages
    num_messages = 10
    keypairs = [Ed25519Signer.generate_keypair() for _ in range(num_messages)]
    messages = [f"message {i}".encode() for i in range(num_messages)]

    # Sign all messages
    signatures = [
        Ed25519Signer.sign(msg, priv) for msg, (priv, _) in zip(messages, keypairs)
    ]

    # Extract public keys
    public_keys = [pub for _, pub in keypairs]

    # Batch verify
    results = Ed25519Signer.batch_verify(messages, signatures, public_keys)

    assert len(results) == num_messages
    assert all(results), "All signatures should be valid"


@pytest.mark.unit
def test_invalid_key_format():
    """Test signing/verification handles invalid key formats."""
    # Signing should raise with invalid key
    with pytest.raises(ValueError):
        Ed25519Signer.sign(b"message", b"invalid_key_data")

    priv_key, _ = Ed25519Signer.generate_keypair()
    signature = Ed25519Signer.sign(b"message", priv_key)

    # Verification should return False (not raise) with invalid key
    result = Ed25519Signer.verify(b"message", signature, b"invalid_key_data")
    assert result is False, "Invalid public key should result in failed verification"
