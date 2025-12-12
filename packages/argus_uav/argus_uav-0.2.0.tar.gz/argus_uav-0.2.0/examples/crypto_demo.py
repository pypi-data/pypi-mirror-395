#!/usr/bin/env python3
"""
Cryptographic defense demonstration.

Shows Ed25519 digital signatures providing perfect detection (100% TPR, 0% FPR).
"""

import time

import numpy as np

from argus_uav.attacks import AttackScenario, AttackType
from argus_uav.attacks.phantom_uav import PhantomInjector
from argus_uav.core.swarm import Swarm
from argus_uav.detection.crypto_detector import CryptoDetector


def main():
    """Demonstrate cryptographic defense against phantom UAVs."""
    print("\n" + "=" * 70)
    print("🔐 ARGUS CRYPTOGRAPHIC DEFENSE DEMONSTRATION")
    print("=" * 70)

    # Create swarm WITH crypto enabled
    print("\n📍 Step 1: Initialize swarm with Ed25519 cryptography...")
    rng = np.random.default_rng(seed=42)
    swarm = Swarm(
        num_uavs=30,
        comm_range=200.0,
        bounds=(500, 500, 100),
        rng=rng,
        enable_crypto=True,  # Enable cryptographic signing!
    )

    print(f"   ✓ Swarm initialized with {swarm.num_uavs} UAVs")
    print("   ✓ Ed25519 key pairs generated for all legitimate UAVs")

    # Verify keys were generated
    num_with_keys = sum(1 for uav in swarm.uavs.values() if uav.private_key is not None)
    print(f"   ✓ {num_with_keys} UAVs have cryptographic keys")

    # Collect baseline and train detector
    print("\n🧠 Step 2: Collect baseline and train crypto detector...")
    baseline_graphs = []
    for t in range(10):
        swarm.step(dt=1.0)
        baseline_graphs.append(swarm.get_graph().copy())

    detector = CryptoDetector()
    detector.train(baseline_graphs)
    print(
        f"   ✓ Detector trained with {len(detector.public_keys)} registered public keys"
    )

    # Verify signatures are being created
    sample_uav = list(swarm.uavs.values())[0]
    if sample_uav.message_queue:
        sample_msg = sample_uav.message_queue[-1]
        print(f"   ✓ Sample message has signature: {sample_msg.signature is not None}")
        print(
            f"   ✓ Signature length: {len(sample_msg.signature) if sample_msg.signature else 0} bytes"
        )

    # Inject phantom attack
    print("\n⚠️  Step 3: Inject phantom UAV attack...")
    print("   (Phantoms have no cryptographic keys!)")

    attack = AttackScenario(
        attack_type=AttackType.PHANTOM, start_time=0.0, duration=10.0, phantom_count=5
    )

    injector = PhantomInjector()
    injector.inject(swarm, attack, 0.0)

    print("   ✓ Attack injected: 5 phantom UAVs added")
    print(f"   ✓ Total UAVs: {len(swarm.uavs)} (30 legitimate + 5 phantoms)")

    # Verify phantoms have no keys
    num_phantoms_without_keys = sum(
        1
        for uav in swarm.uavs.values()
        if not uav.is_legitimate and uav.private_key is None
    )
    print(f"   ✓ {num_phantoms_without_keys} phantoms have no cryptographic keys")

    # Run one more step to generate messages from phantoms
    swarm.step(dt=1.0)

    # Run cryptographic detection
    print("\n🔍 Step 4: Run cryptographic signature verification...")
    result = detector.detect(swarm.get_graph())
    metrics = result.compute_metrics()

    print("\n" + "-" * 70)
    print("CRYPTOGRAPHIC VERIFICATION RESULTS")
    print("-" * 70)
    print(f"Flagged UAVs: {len(result.anomalous_uav_ids)}")
    print(f"Detection time: {metrics['detection_time'] * 1000:.2f}ms")

    print("\n🎯 Detection Metrics:")
    print(f"  • True Positive Rate (TPR):  {metrics['tpr']:.2%}")
    print(f"  • False Positive Rate (FPR): {metrics['fpr']:.2%}")
    print(f"  • Precision: {metrics['precision']:.2%}")
    print(f"  • Recall:    {metrics['recall']:.2%}")
    print(f"  • F1 Score:  {metrics['f1']:.2f}")

    print("\n📊 Confusion Matrix:")
    print(f"  • True Positives:  {metrics['tp']} (phantoms detected)")
    print(f"  • False Positives: {metrics['fp']} (legitimate UAVs flagged)")
    print(f"  • True Negatives:  {metrics['tn']} (legitimate UAVs passed)")
    print(f"  • False Negatives: {metrics['fn']} (phantoms missed)")

    # Show flagged UAVs
    print("\n🚨 Flagged UAVs (no valid signature):")
    for uav_id in sorted(result.anomalous_uav_ids):
        is_legit = result.ground_truth.get(uav_id, True)
        status = "✗ PHANTOM" if not is_legit else "⚠️ LEGIT (FALSE POSITIVE)"
        score = result.confidence_scores.get(uav_id, 0)
        print(f"  • {uav_id:<20} Confidence: {score:.2f}  {status}")

    # Performance benchmark
    print("\n" + "=" * 70)
    print("⚡ PERFORMANCE BENCHMARK")
    print("=" * 70)

    # Measure signing performance
    test_uav = list(swarm.uavs.values())[0]
    if test_uav.private_key:
        from argus_uav.crypto.ed25519_signer import Ed25519Signer

        test_message = test_uav.broadcast_remote_id(time.time())

        # Signing benchmark
        sign_times = []
        for _ in range(100):
            start = time.time()
            signature = Ed25519Signer.sign(
                test_message.to_bytes(), test_uav.private_key
            )
            sign_times.append(time.time() - start)

        avg_sign_time = np.mean(sign_times) * 1000  # Convert to ms

        # Verification benchmark
        verify_times = []
        for _ in range(100):
            start = time.time()
            Ed25519Signer.verify(
                test_message.to_bytes(), signature, test_uav.public_key
            )
            verify_times.append(time.time() - start)

        avg_verify_time = np.mean(verify_times) * 1000  # Convert to ms

        print("Signing performance (avg of 100):")
        print(f"  • Average signing time:       {avg_sign_time:.3f}ms")
        print(f"  • Average verification time:  {avg_verify_time:.3f}ms")
        print(
            f"  • Requirement: < 10ms         {'✓ PASS' if avg_sign_time < 10 and avg_verify_time < 10 else '✗ FAIL'}"
        )

        # Message overhead
        msg_size_unsigned = len(test_message.to_bytes())
        msg_size_with_sig = msg_size_unsigned + 64  # 64-byte signature
        overhead_pct = (64 / msg_size_unsigned) * 100

        print("\nMessage overhead:")
        print(f"  • Unsigned message:   {msg_size_unsigned} bytes")
        print("  • Signature:          64 bytes")
        print(f"  • Total with sig:     {msg_size_with_sig} bytes")
        print(f"  • Overhead:           {overhead_pct:.1f}%")

    # Final summary
    print("\n" + "=" * 70)
    print("✅ Cryptographic defense demonstration complete!")
    print("=" * 70)
    print("\nKey Findings:")
    print(f"  • Detection Accuracy: TPR={metrics['tpr']:.0%}, FPR={metrics['fpr']:.0%}")
    print(f"  • Signing Speed: {avg_sign_time:.3f}ms (requirement: < 10ms)")
    print(f"  • Verification Speed: {avg_verify_time:.3f}ms (requirement: < 10ms)")
    print(f"  • Message Overhead: {overhead_pct:.1f}%")

    if metrics["tpr"] == 1.0 and metrics["fpr"] == 0.0:
        print("\n  🎯 PERFECT DETECTION: 100% TPR, 0% FPR!")
        print("  Cryptographic authentication provides complete protection")
        print("  against phantom UAVs and message spoofing.")
    else:
        print("\n  ⚠️  Detection not perfect - check signature implementation")

    print()


if __name__ == "__main__":
    main()
