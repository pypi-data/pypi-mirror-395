"""
Amorce Core Crypto Module (Task 1)
Handles identity management (Ed25519 keys) and cryptographic primitives.
"""

import os
import base64
import json
import logging
import hashlib  # Required for MCP 1.0 (Agent ID Derivation)
from abc import ABC, abstractmethod
from typing import Optional, Union, List

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.exceptions import InvalidSignature

from .exceptions import AmorceSecurityError

# Configure logging
logger = logging.getLogger("nexus.crypto")


class IdentityProvider(ABC):
    """Abstract base class for retrieving private keys."""

    @abstractmethod
    def get_private_key(self) -> ed25519.Ed25519PrivateKey:
        pass


class LocalFileProvider(IdentityProvider):
    """Loads a private key from a local PEM file."""

    def __init__(self, filepath: str):
        self.filepath = filepath

    def get_private_key(self) -> ed25519.Ed25519PrivateKey:
        try:
            with open(self.filepath, "rb") as key_file:
                private_key = serialization.load_pem_private_key(
                    key_file.read(),
                    password=None
                )
            if not isinstance(private_key, ed25519.Ed25519PrivateKey):
                raise AmorceSecurityError("Key is not an Ed25519 private key.")
            return private_key
        except Exception as e:
            logger.error(f"Failed to load local key from {self.filepath}: {e}")
            raise AmorceSecurityError(f"Failed to load local key from {self.filepath}: {e}")


class EnvVarProvider(IdentityProvider):
    """Loads a private key directly from an environment variable string."""

    def __init__(self, env_var_name: str = "AGENT_PRIVATE_KEY"):
        self.env_var_name = env_var_name

    def get_private_key(self) -> ed25519.Ed25519PrivateKey:
        pem_data = os.environ.get(self.env_var_name)
        if not pem_data:
            raise AmorceSecurityError(f"Environment variable {self.env_var_name} is not set.")

        # Handle cases where newlines are escaped (common in some CI/CD)
        pem_data = pem_data.replace("\\n", "\n")

        try:
            private_key = serialization.load_pem_private_key(
                pem_data.encode("utf-8"),
                password=None
            )
            return private_key
        except Exception as e:
            logger.error(f"Failed to load key from environment variable: {e}")
            raise AmorceSecurityError(f"Failed to load key from environment variable: {e}")


class GoogleSecretManagerProvider(IdentityProvider):
    """Loads a private key from Google Secret Manager."""

    def __init__(self, project_id: str, secret_name: str, version: str = "latest"):
        self.project_id = project_id
        self.secret_name = secret_name
        self.version = version

    def get_private_key(self) -> ed25519.Ed25519PrivateKey:
        try:
            from google.cloud import secretmanager
            client = secretmanager.SecretManagerServiceClient()
            name = f"projects/{self.project_id}/secrets/{self.secret_name}/versions/{self.version}"
            response = client.access_secret_version(request={"name": name})
            pem_data = response.payload.data

            private_key = serialization.load_pem_private_key(
                pem_data,
                password=None
            )
            return private_key
            return private_key
        except ImportError:
            logger.error("google-cloud-secret-manager not installed.")
            raise AmorceSecurityError("google-cloud-secret-manager not installed.")
        except Exception as e:
            logger.error(f"Failed to load key from Secret Manager: {e}")
            raise AmorceSecurityError(f"Failed to load key from Secret Manager: {e}")

# --- Internal Provider for In-Memory Keys ---
class InMemoryProvider(IdentityProvider):
    """Holds a generated key in memory (Ephemeral)."""
    def __init__(self, private_key: ed25519.Ed25519PrivateKey):
        self._key = private_key

    def get_private_key(self) -> ed25519.Ed25519PrivateKey:
        return self._key


class IdentityManager:
    """
    Central class to manage the agent's identity.
    """

    def __init__(self, provider: IdentityProvider):
        self._private_key = provider.get_private_key()
        self._public_key = self._private_key.public_key()

    @staticmethod
    def generate_ephemeral() -> 'IdentityManager':
        """
        Factory method: Generates a new ephemeral Ed25519 identity in memory.
        Returns a self-contained IdentityManager instance ready for consumption.
        """
        # Generate a new keypair using cryptography
        new_key = ed25519.Ed25519PrivateKey.generate()

        # Wrap it in our internal provider
        provider = InMemoryProvider(new_key)

        # Return a ready-to-use IdentityManager
        return IdentityManager(provider)

    @property
    def public_key_pem(self) -> str:
        """Returns the public key in PEM format (for registration)."""
        pem_bytes = self._public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        return pem_bytes.decode("utf-8")

    @property
    def agent_id(self) -> str:
        """
        MCP 1.0: Deterministic Agent ID derivation.
        Returns the SHA-256 hash of the public key PEM.
        This ensures the ID is cryptographically bound to the key.
        """
        # We strip whitespace to ensure consistent hashing across platforms
        clean_pem = self.public_key_pem.strip()
        return hashlib.sha256(clean_pem.encode('utf-8')).hexdigest()

    @property
    def private_key_pem(self) -> str:
        """
        Returns the private key in PEM format.
        WARNING: Handle with extreme care. Used for saving generated identities.
        """
        pem_bytes = self._private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        return pem_bytes.decode("utf-8")

    def sign_data(self, data: bytes) -> str:
        """
        Signs raw bytes and returns a Base64 encoded signature.
        """
        signature = self._private_key.sign(data)
        return base64.b64encode(signature).decode("utf-8")

    @staticmethod
    def verify_signature(public_key_pem: str, data: bytes, signature_b64: str) -> bool:
        """
        Static utility to verify a signature given a public key PEM.
        """
        try:
            public_key = serialization.load_pem_public_key(
                public_key_pem.encode("utf-8")
            )
            if not isinstance(public_key, ed25519.Ed25519PublicKey):
                return False

            signature = base64.b64decode(signature_b64)
            public_key.verify(signature, data)
            return True
        except (InvalidSignature, Exception) as e:
            logger.warning(f"Signature verification failed: {e}")
            return False

    @staticmethod
    def get_canonical_json_bytes(payload: dict) -> bytes:
        """
        Returns the canonical JSON byte representation for signing.
        Strict: sort_keys=True, no whitespace.
        """
        return json.dumps(
            payload,
            sort_keys=True,
            separators=(',', ':')
        ).encode("utf-8")
    
    def to_manifest_json(
        self,
        name: str,
        endpoint: str,
        capabilities: Optional[List[str]] = None,
        description: str = ""
    ) -> str:
        """
        Generate an agent manifest for Trust Directory registration.
        
        Perfect for Builders who want to list their service in the network.
        
        Args:
            name: Human-readable agent name (e.g., "Le Petit Bistro")
            endpoint: Your API webhook URL (e.g., "https://my-api.com/webhook")
            capabilities: List of intents your agent supports (e.g., ["book_table", "cancel"])
            description: Optional description of your service
        
        Returns:
            JSON string ready to save as agent-manifest.json
        
        Example:
            identity = IdentityManager.generate_ephemeral()
            
            manifest = identity.to_manifest_json(
                name="My Restaurant Bot",
                endpoint="https://my-api.herokuapp.com/amorce",
                capabilities=["book_table", "check_availability", "cancel_reservation"],
                description="Fine dining reservations"
            )
            
            print(manifest)  # Copy-paste into agent-manifest.json
            
            # Or save directly:
            with open("agent-manifest.json", "w") as f:
                f.write(manifest)
        """
        manifest = {
            "name": name,
            "agent_id": self.agent_id,
            "public_key": self.public_key_pem,
            "endpoint": endpoint,
            "capabilities": capabilities or [],
            "description": description,
            "version": "1.0.0",
            "protocol": "aatp"
        }
        return json.dumps(manifest, indent=2)