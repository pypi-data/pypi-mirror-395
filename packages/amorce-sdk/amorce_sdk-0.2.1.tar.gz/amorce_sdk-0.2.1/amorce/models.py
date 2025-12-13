"""
Amorce Models Module
Centralized Pydantic models for client requests and responses.
Ensures strict typing for AsyncAmorceClient and future client implementations.
"""

from typing import Optional, Dict, Any
from pydantic import BaseModel, Field, field_validator


class AmorceConfig(BaseModel):
    """
    Configuration for Amorce clients.
    Encapsulates directory and orchestrator URLs with validation.
    """
    directory_url: str = Field(..., description="Trust Directory URL")
    orchestrator_url: str = Field(..., description="Orchestrator API URL")
    
    @field_validator('directory_url', 'orchestrator_url')
    @classmethod
    def validate_url(cls, v: str) -> str:
        """Ensure URLs start with http:// or https://"""
        if not v.startswith(('http://', 'https://')):
            raise ValueError(f"Invalid URL: {v}. Must start with http:// or https://")
        return v.rstrip('/')


class TransactionResult(BaseModel):
    """
    Nested result data from a successful transaction.
    """
    status: str = Field(..., description="Transaction status (e.g., 'success', 'pending')")
    message: Optional[str] = Field(None, description="Human-readable message")
    data: Optional[Dict[str, Any]] = Field(None, description="Provider-specific response data")


class AmorceResponse(BaseModel):
    """
    Standardized response wrapper for transact() operations.
    Provides consistent interface for all client implementations.
    """
    transaction_id: str = Field(..., description="Unique transaction identifier")
    status_code: int = Field(..., description="HTTP status code from orchestrator")
    result: Optional[TransactionResult] = Field(None, description="Transaction result data")
    error: Optional[str] = Field(None, description="Error message if transaction failed")
    
    @property
    def is_success(self) -> bool:
        """Check if transaction was successful (2xx status)"""
        return 200 <= self.status_code < 300
    
    @property
    def is_retryable(self) -> bool:
        """Check if error is retryable (5xx or 429)"""
        return self.status_code in [429, 500, 502, 503, 504]
