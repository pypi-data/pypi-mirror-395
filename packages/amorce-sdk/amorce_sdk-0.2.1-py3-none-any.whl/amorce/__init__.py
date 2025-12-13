"""
Amorce Python SDK - The Standard for Secure AI Agent Transactions
"""

__version__ = "0.2.1"

# Core clients
from .client import AmorceClient
from .core.async_client import AsyncAmorceClient

# Identity management
from .crypto import (
    IdentityManager,
    LocalFileProvider,
    EnvVarProvider,
    GoogleSecretManagerProvider,
)

# Request verification (for Builders)
from .verification import verify_request, VerifiedRequest

# Protocol primitives
from .envelope import (
    AmorceEnvelope,
    SenderInfo,
    SettlementInfo,
    PriorityLevel,
)

# Models
from .models import AmorceConfig, AmorceResponse, TransactionResult

# Exceptions
from .exceptions import (
    AmorceError,
    AmorceConfigError,
    AmorceNetworkError,
    AmorceAPIError,
    AmorceSecurityError,
    AmorceValidationError,
)

# MCP Integration (NEW)
from .mcp_helpers import MCPToolClient

__all__ = [
    # Version
    "__version__",
    # Clients
    "AmorceClient",
    "AsyncAmorceClient",
    # Identity
    "IdentityManager",
    "LocalFileProvider",
    "EnvVarProvider",
    "GoogleSecretManagerProvider",
    # Verification (NEW - for Builders)
    "verify_request",
    "VerifiedRequest",
    # Protocol
    "AmorceEnvelope",
    "SenderInfo",
    "SettlementInfo",
    "PriorityLevel",
    # Models
    "AmorceConfig",
    "AmorceResponse",
    "TransactionResult",
    # Exceptions
    "AmorceError",
    "AmorceConfigError",
    "AmorceNetworkError",
    "AmorceAPIError",
    "AmorceSecurityError",
    "AmorceValidationError",
    # MCP Integration (NEW)
    "MCPToolClient",
]

print(f"Amorce SDK v{__version__} loaded.")