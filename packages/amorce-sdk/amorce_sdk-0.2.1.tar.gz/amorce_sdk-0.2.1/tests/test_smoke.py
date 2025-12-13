import unittest
import sys
import os
import hashlib

# Adjust path to include the parent directory (project root)
# This allows importing the 'nexus' module without installing it via pip
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    # TEST IMPORT (CRITICAL v0.1.6)
    # Check that export aliases are working correctly
    from amorce import (
        IdentityManager,
        AmorceClient,
        Envelope,  # Alias for AmorceEnvelope
        AmorceEnvelope,  # Original Name
        PriorityLevel
    )
    print("✅ [IMPORT] Amorce modules loaded successfully.")
except ImportError as e:
    print(f"❌ [IMPORT] Critical failure: {e}")
    sys.exit(1)


class TestSmokeV016(unittest.TestCase):
    """
    Smoke Test Suite for Release v0.1.6
    Target: Agent ID Derivation, Clean Client API, Exports.
    """

    def test_01_identity_derivation(self):
        """Verifies that Agent ID is automatically derived from the key."""
        print("\n--- Test 1: Identity Derivation ---")

        # 1. Ephemeral Generation (API v0.1.5+)
        identity = IdentityManager.generate_ephemeral()

        # 2. Agent ID Verification (New in v0.1.6)
        agent_id = identity.agent_id

        print(f"Public Key (Snippet): {identity.public_key_pem.splitlines()[1][:20]}...")
        print(f"Derived Agent ID: {agent_id}")

        self.assertIsNotNone(agent_id)
        self.assertEqual(len(agent_id), 64)  # SHA-256 hex digest length

        # Consistency Check (Determinism)
        # Manually re-calculate hash to be sure
        clean_pem = identity.public_key_pem.strip()
        expected_id = hashlib.sha256(clean_pem.encode('utf-8')).hexdigest()
        self.assertEqual(agent_id, expected_id)
        print("✅ [PASS] Agent ID is mathematically correct (SHA-256).")

    def test_02_client_instantiation(self):
        """Verifies that Client no longer needs the agent_id argument."""
        print("\n--- Test 2: Simplified Client API ---")

        identity = IdentityManager.generate_ephemeral()

        # 1. "Clean" Instantiation (Without explicit agent_id)
        client = AmorceClient(
            identity=identity,
            directory_url="http://mock-dir",
            orchestrator_url="http://mock-orch"
        )

        # 2. Did the client find the ID by itself?
        print(f"Client Agent ID: {client.agent_id}")
        self.assertEqual(client.agent_id, identity.agent_id)
        print("✅ [PASS] AmorceClient retrieved Agent ID from identity.")

    def test_03_envelope_alias_and_priority(self):
        """Verifies that Envelope alias works and priority is passed."""
        print("\n--- Test 3: Envelope & Priority ---")

        identity = IdentityManager.generate_ephemeral()
        client = AmorceClient(identity, "http://d", "http://o")

        payload = {"test": "v0.1.6"}

        # Use internal method to test construction
        # We use PriorityLevel.CRITICAL
        envelope = client._create_envelope(payload, priority=PriorityLevel.CRITICAL)

        # Type Verification (Alias vs Class)
        self.assertIsInstance(envelope, AmorceEnvelope)
        self.assertIsInstance(envelope, Envelope)  # The alias must work for isinstance

        # Field Verification
        self.assertEqual(envelope.priority, "critical")
        print(f"Envelope Priority: {envelope.priority}")

        # Signature Verification
        self.assertTrue(envelope.verify())
        print("✅ [PASS] Envelope created with alias 'Envelope' and priority 'critical'.")


if __name__ == '__main__':
    unittest.main()