import unittest
import sys
import os
from unittest.mock import MagicMock, patch
import requests

# Adjust path to include the parent directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from amorce import (
    IdentityManager,
    NexusClient,
    NexusEnvelope,
    NexusConfigError,
    NexusNetworkError,
    NexusAPIError,
    NexusSecurityError,
    NexusValidationError
)

class TestNexusErrors(unittest.TestCase):

    def setUp(self):
        self.identity = IdentityManager.generate_ephemeral()

    def test_config_error_invalid_url(self):
        """Test that NexusConfigError is raised for invalid URLs."""
        with self.assertRaises(NexusConfigError):
            NexusClient(self.identity, "invalid-url", "http://valid-url")
        
        with self.assertRaises(NexusConfigError):
            NexusClient(self.identity, "http://valid-url", "invalid-url")

    @patch('nexus.client.requests.Session.get')
    def test_network_error_discovery(self, mock_get):
        """Test that NexusNetworkError is raised on connection failure during discovery."""
        mock_get.side_effect = requests.exceptions.ConnectionError("Connection refused")
        
        client = NexusClient(self.identity, "http://mock-dir", "http://mock-orch")
        
        with self.assertRaises(NexusNetworkError):
            client.discover("test-service")

    @patch('nexus.client.requests.Session.get')
    def test_api_error_discovery(self, mock_get):
        """Test that NexusAPIError is raised on 4xx/5xx response during discovery."""
        mock_resp = MagicMock()
        mock_resp.status_code = 500
        mock_resp.text = "Internal Server Error"
        mock_resp.raise_for_status.side_effect = requests.exceptions.HTTPError(response=mock_resp)
        mock_get.return_value = mock_resp
        
        client = NexusClient(self.identity, "http://mock-dir", "http://mock-orch")
        
        with self.assertRaises(NexusAPIError) as cm:
            client.discover("test-service")
        
        self.assertEqual(cm.exception.status_code, 500)
        self.assertIn("Internal Server Error", cm.exception.response_body)

    @patch('nexus.client.requests.Session.post')
    def test_api_error_transaction(self, mock_post):
        """Test that NexusAPIError is raised on non-200 response during transaction."""
        mock_resp = MagicMock()
        mock_resp.status_code = 400
        mock_resp.text = "Bad Request"
        mock_post.return_value = mock_resp
        
        client = NexusClient(self.identity, "http://mock-dir", "http://mock-orch")
        
        with self.assertRaises(NexusAPIError) as cm:
            client.transact({"service_id": "svc-1"}, {"data": "test"})
            
        self.assertEqual(cm.exception.status_code, 400)

    def test_validation_error_envelope(self):
        """Test that NexusValidationError is raised for invalid envelope version."""
        with self.assertRaises(NexusValidationError):
            NexusEnvelope(
                natp_version="0.9.9", # Invalid
                sender=MagicMock(),
                payload={}
            )

if __name__ == '__main__':
    unittest.main()
