"""
Amorce Exception Hierarchy (Task 4)
Provides specific exception types for different failure modes.
"""

from typing import Optional


class AmorceError(Exception):
    """Base exception for all Amorce SDK errors."""
    pass


class AmorceConfigError(AmorceError):
    """Raised when configuration is invalid (e.g., missing URLs, bad keys)."""
    pass


class AmorceNetworkError(AmorceError):
    """Raised for network-level errors (DNS, connection, timeouts)."""
    pass


class AmorceAPIError(AmorceError):
    """Raised for API-level errors (4xx, 5xx responses from orchestrator/directory)."""
    def __init__(self, message: str, status_code: Optional[int] = None, response_body: Optional[str] = None):
        super().__init__(message)
        self.status_code = status_code
        self.response_body = response_body


class AmorceSecurityError(AmorceError):
    """Raised for cryptographic or signature verification failures."""
    pass


class AmorceValidationError(AmorceError):
    """Raised when data validation fails (e.g., invalid NATP version, malformed envelope)."""
    pass
