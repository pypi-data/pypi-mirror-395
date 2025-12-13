import unittest
import sys
import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

# Ajout du chemin racine
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from amorce.client import NexusClient
from amorce.crypto import IdentityManager, IdentityProvider
from cryptography.hazmat.primitives.asymmetric import ed25519


# --- MOCK KEY ---
class MockKeyProvider(IdentityProvider):
    def __init__(self):
        self.key = ed25519.Ed25519PrivateKey.generate()

    def get_private_key(self):
        return self.key


# --- LE SERVEUR CAPRICIEUX STABILISÉ ---
class CapriciousHandler(BaseHTTPRequestHandler):
    request_count = 0

    def do_POST(self):
        # FIX CRITIQUE : On force la fermeture de la connexion après chaque réponse.
        # Cela empêche 'requests' d'essayer de réutiliser un socket mort (Keep-Alive)
        # et évite le "ConnectionResetError".
        self.close_connection = True

        CapriciousHandler.request_count += 1

        if CapriciousHandler.request_count < 3:
            # Cas d'erreur (503)
            content = b'Service Unavailable'
            self.send_response(503)
            # Bonne pratique : toujours définir Content-Length
            self.send_header('Content-Length', str(len(content)))
            self.end_headers()
            self.wfile.write(content)
        else:
            # Cas de succès (200)
            content = b'{"status": "success", "tx_id": "abc-123"}'
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Content-Length', str(len(content)))
            self.end_headers()
            self.wfile.write(content)

    def log_message(self, format, *args):
        pass  # Silence les logs


class TestResilienceReal(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Port 0 = L'OS choisit un port libre aléatoire
        cls.server = HTTPServer(('localhost', 0), CapriciousHandler)
        cls.port = cls.server.server_port

        cls.thread = threading.Thread(target=cls.server.serve_forever)
        cls.thread.daemon = True
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()

    def setUp(self):
        CapriciousHandler.request_count = 0
        self.identity = IdentityManager(MockKeyProvider())

        self.client = NexusClient(
            identity=self.identity,
            directory_url=f"http://localhost:{self.port}",
            orchestrator_url=f"http://localhost:{self.port}"
        )

        # Backoff accéléré pour le test
        adapter = self.client.session.get_adapter("http://")
        adapter.max_retries.backoff_factor = 0.1

    def test_real_retry_sequence(self):
        """
        Integration Test: Vérifie que le client survit aux erreurs réseaux réelles.
        """
        print(f"\n[TEST] Connexion au serveur local (Port {self.port})...")

        result = self.client.transact(
            service_contract={"service_id": "srv-real"},
            payload={"msg": "resilience_check"}
        )

        # Analyse des résultats
        if result is None:
            print("❌ ECHEC : Le client a renvoyé None (tous les retries ont échoué).")
        else:
            print("✅ SUCCÈS : Le client a récupéré la réponse 200 après les échecs.")

        self.assertIsNotNone(result, "Le client a abandonné trop tôt !")
        self.assertEqual(result.get("status"), "success")

        # On attend exactement 3 appels (2 échecs + 1 succès)
        self.assertEqual(CapriciousHandler.request_count, 3,
                         f"Nombre d'appels incorrect : {CapriciousHandler.request_count} (Attendu: 3)")

        print(f"[SUCCESS] Résilience validée : {CapriciousHandler.request_count} appels réseaux effectués.")


if __name__ == '__main__':
    unittest.main()