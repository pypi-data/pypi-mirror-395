"""
Request verification utilities for service providers (Builders).
Allows AI Agent developers to verify incoming signed requests.
"""
import json
import requests
from typing import Dict, List, Optional
from .crypto import IdentityManager
from .exceptions import AmorceSecurityError

# Production mainnet default
DEFAULT_DIRECTORY_URL = "https://directory.amorce.io"


class VerifiedRequest:
    """Represents a successfully verified incoming request."""
    
    def __init__(self, agent_id: str, payload: dict, signature: str):
        self.agent_id = agent_id
        self.payload = payload
        self.signature = signature
    
    def __repr__(self):
        return f"VerifiedRequest(agent_id={self.agent_id[:12]}..., intent={self.payload.get('payload', {}).get('intent')})"


def verify_request(
    headers: Dict[str, str],
    body: bytes,
    allowed_intents: Optional[List[str]] = None,
    public_key: Optional[str] = None,
    directory_url: str = DEFAULT_DIRECTORY_URL
) -> VerifiedRequest:
    """
    Verify an incoming Amorce transaction request.
    
    This is the main function for Builders to protect their APIs.
    
    Args:
        headers: HTTP request headers (must include X-Agent-Signature, X-Amorce-Agent-ID)
        body: Raw request body as bytes
        allowed_intents: Optional whitelist of permitted intents
        public_key: Optional public key PEM (if provided, skips directory lookup)
        directory_url: Trust Directory URL (defaults to production mainnet)
    
    Returns:
        VerifiedRequest with agent_id and payload
    
    Raises:
        AmorceSecurityError: If signature is invalid, agent unknown, or intent not allowed
    
    Examples:
        # Automatic public key fetch (recommended for production)
        verified = verify_request(
            headers=request.headers,
            body=request.get_data(),
            allowed_intents=['book_table', 'cancel_reservation']
        )
        
        # Manual public key (for testing or offline)
        verified = verify_request(
            headers=request.headers,
            body=request.get_data(),
            public_key="-----BEGIN PUBLIC KEY-----\\n..."
        )
    """
    # Extract required headers (case-insensitive)
    signature = None
    agent_id = None
    
    for key, value in headers.items():
        if key.lower() == 'x-agent-signature':
            signature = value
        elif key.lower() == 'x-amorce-agent-id':
            agent_id = value
    
    if not signature:
        raise AmorceSecurityError("Missing X-Agent-Signature header")
    if not agent_id:
        raise AmorceSecurityError("Missing X-Amorce-Agent-ID header")
    
    # Parse request body
    try:
        payload = json.loads(body)
    except json.JSONDecodeError:
        raise AmorceSecurityError("Invalid JSON in request body")
    
    # Get public key (auto-fetch or manual)
    if public_key is None:
        # AUTO-FETCH from Trust Directory
        public_key = _fetch_public_key_from_directory(agent_id, directory_url)
    
    # Verify signature
    canonical_bytes = IdentityManager.get_canonical_json_bytes(payload)
    is_valid = IdentityManager.verify_signature(public_key, canonical_bytes, signature)
    
    if not is_valid:
        raise AmorceSecurityError(f"Invalid signature for agent {agent_id}")
    
    # Check intent whitelist
    if allowed_intents:
        intent = payload.get('payload', {}).get('intent')
        if intent not in allowed_intents:
            raise AmorceSecurityError(
                f"Intent '{intent}' not in allowed list: {allowed_intents}"
            )
    
    return VerifiedRequest(agent_id, payload, signature)


def _fetch_public_key_from_directory(agent_id: str, directory_url: str) -> str:
    """
    Fetch public key from Trust Directory.
    
    Args:
        agent_id: The agent's ID (SHA-256 of public key)
        directory_url: Trust Directory base URL
    
    Returns:
        Public key in PEM format
    
    Raises:
        AmorceSecurityError: If agent not found or directory unreachable
    """
    url = f"{directory_url.rstrip('/')}/api/v1/agents/{agent_id}"
    
    try:
        response = requests.get(url, timeout=5)
        
        if response.status_code == 404:
            raise AmorceSecurityError(f"Agent {agent_id} not found in Trust Directory")
        
        if response.status_code != 200:
            raise AmorceSecurityError(
                f"Directory returned {response.status_code}: {response.text}"
            )
        
        data = response.json()
        public_key = data.get('public_key')
        
        if not public_key:
            raise AmorceSecurityError("No public_key in directory response")
        
        return public_key
        
    except requests.exceptions.RequestException as e:
        raise AmorceSecurityError(f"Failed to reach Trust Directory: {e}")
