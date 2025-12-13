import unittest
import sys
import os
from pydantic import ValidationError

# Ajout du chemin racine pour importer le SDK localement
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from amorce.envelope import NexusEnvelope, SenderInfo
from amorce.client import NexusClient
from amorce.crypto import IdentityManager, IdentityProvider
from cryptography.hazmat.primitives.asymmetric import ed25519


# --- Mock Identity Provider pour les tests ---
class MockKeyProvider(IdentityProvider):
    def __init__(self):
        self.key = ed25519.Ed25519PrivateKey.generate()

    def get_private_key(self):
        return self.key


class TestPriorityLane(unittest.TestCase):
    """
    Validation Suite for Ticket-CORE-02 (Priority Lane).
    Target: NexusEnvelope & NexusClient
    """

    def setUp(self):
        # Setup d'une identité fictive pour signer les enveloppes
        self.mock_provider = MockKeyProvider()
        self.identity = IdentityManager(self.mock_provider)

        self.sender = SenderInfo(
            public_key=self.identity.public_key_pem,
            agent_id="test-agent-007"
        )

    def test_envelope_valid_priorities(self):
        """Test que les 3 niveaux de priorité valides sont acceptés."""
        valid_priorities = ["normal", "high", "critical"]

        for p in valid_priorities:
            with self.subTest(priority=p):
                env = NexusEnvelope(
                    priority=p,
                    sender=self.sender,
                    payload={"task": "test"}
                )
                self.assertEqual(env.priority, p)
                # Vérifie que la signature fonctionne toujours
                env.sign(self.identity)
                self.assertTrue(env.verify())

    def test_envelope_invalid_priority_raises_error(self):
        """Test que toute autre valeur est rejetée par le Regex Pydantic."""
        invalid_priorities = ["urgent", "low", "Critical", "HIGH", "1", ""]

        for p in invalid_priorities:
            with self.subTest(priority=p):
                with self.assertRaises(ValidationError):
                    NexusEnvelope(
                        priority=p,
                        sender=self.sender,
                        payload={"task": "fail"}
                    )

    def test_envelope_default_priority(self):
        """Test que la priorité par défaut est bien 'normal'."""
        env = NexusEnvelope(
            sender=self.sender,
            payload={"task": "default"}
        )
        self.assertEqual(env.priority, "normal")

    def test_client_propagation(self):
        """Test que le NexusClient passe bien l'argument priority à l'enveloppe."""
        # On instancie un client "hors ligne" (on ne fera pas d'appel réseau réel)
        client = NexusClient(
            identity=self.identity,
            directory_url="http://fake-directory",
            orchestrator_url="http://fake-orchestrator"
        )

        # On utilise la méthode interne _create_envelope pour vérifier la construction
        # sans avoir besoin de mocker requests.post

        # Cas 1: Priorité Critique
        env_crit = client._create_envelope(
            payload={"alert": "system_failure"},
            priority="critical"
        )
        self.assertEqual(env_crit.priority, "critical")

        # Cas 2: Défaut
        env_normal = client._create_envelope(
            payload={"msg": "hello"}
        )
        self.assertEqual(env_normal.priority, "normal")


if __name__ == '__main__':
    unittest.main()