"""
Amorce Async Client Module
High-throughput async HTTP/2 client for the Amorce Agent Transaction Protocol (AATP).

Features:
- AsyncContextManager lifecycle for proper resource management
- HTTP/2 enforcement via httpx
- Exponential backoff retry logic via tenacity
- Zero-trust Ed25519 signing
- Automatic idempotency key generation
"""

import uuid
import logging
from typing import Dict, Any, Optional

import httpx
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    wait_random,
    wait_combine,
    retry_if_exception_type,
    before_sleep_log
)

from ..crypto import IdentityManager
from ..envelope import PriorityLevel
from ..models import AmorceConfig, AmorceResponse, TransactionResult
from ..exceptions import AmorceConfigError, AmorceNetworkError, AmorceAPIError

logger = logging.getLogger("amorce.async_client")


class AsyncAmorceClient:
    """
    Async client for high-throughput AI agents to transact on the Amorce Network.
    
    CRITICAL: Must be used as an AsyncContextManager to ensure proper cleanup.
    
    Example:
        async with AsyncAmorceClient(identity, config) as client:
            response = await client.transact(service_contract, payload)
    """
    
    def __init__(
        self,
        identity: IdentityManager,
        directory_url: Optional[str] = None,
        orchestrator_url: Optional[str] = None,
        config: Optional[AmorceConfig] = None,
        agent_id: Optional[str] = None,
        api_key: Optional[str] = None
    ):
        """
        Initialize the async client (does not open network sockets yet).
        
        Args:
            identity: IdentityManager instance for signing
            directory_url: Trust Directory URL (if not using config)
            orchestrator_url: Orchestrator API URL (if not using config)
            config: AmorceConfig instance (alternative to individual URLs)
            agent_id: Optional agent UUID (defaults to identity.agent_id)
            api_key: Optional API key for L1 authentication
        """
        self.identity = identity
        self.agent_id = agent_id if agent_id else identity.agent_id
        self.api_key = api_key
        
        # Configuration validation
        if config:
            self.config = config
        elif directory_url and orchestrator_url:
            self.config = AmorceConfig(
                directory_url=directory_url,
                orchestrator_url=orchestrator_url
            )
        else:
            raise AmorceConfigError(
                "Must provide either 'config' or both 'directory_url' and 'orchestrator_url'"
            )
        
        # Client will be initialized in __aenter__
        self.client: Optional[httpx.AsyncClient] = None
        
        logger.info(f"AsyncAmorceClient initialized for agent {self.agent_id}")
    
    async def __aenter__(self):
        """
        AsyncContextManager entry: Initialize httpx.AsyncClient with HTTP/2.
        """
        # CRITICAL: http2=True enforces HTTP/2 protocol
        self.client = httpx.AsyncClient(
            http2=True,
            timeout=httpx.Timeout(30.0),
            limits=httpx.Limits(max_keepalive_connections=20, max_connections=100)
        )
        
        # Set API key header if provided
        if self.api_key:
            self.client.headers.update({"X-API-Key": self.api_key})
        
        logger.debug("HTTP/2 client initialized")
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """
        AsyncContextManager exit: Properly close httpx client.
        CRITICAL: Prevents file descriptor leaks in high-concurrency environments.
        """
        if self.client:
            await self.client.aclose()
            logger.debug("HTTP/2 client closed")
        return False
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_combine(
            wait_exponential(multiplier=1, min=1, max=10),
            wait_random(0, 2)  # Add 0-2s random jitter
        ),
        retry=retry_if_exception_type(AmorceNetworkError),
        before_sleep=before_sleep_log(logger, logging.WARNING),
        reraise=True
    )
    async def _execute_with_retry(
        self,
        url: str,
        request_body: Dict[str, Any],
        headers: Dict[str, str]
    ) -> httpx.Response:
        """
        Execute HTTP POST with tenacity retry logic.
        
        Retries on:
        - 429 Too Many Requests
        - 503 Service Unavailable
        - 504 Gateway Timeout
        - Network errors (connection failures)
        
        Args:
            url: Target URL
            request_body: JSON request body
            headers: HTTP headers
            
        Returns:
            httpx.Response object
            
        Raises:
            AmorceNetworkError: On retryable errors (after max attempts)
            AmorceAPIError: On non-retryable errors (4xx except 429)
        """
        if not self.client:
            raise AmorceConfigError("Client not initialized. Use 'async with' context manager.")
        
        try:
            response = await self.client.post(
                url,
                json=request_body,
                headers=headers
            )
            
            # Check for retryable status codes
            if response.status_code in [429, 503, 504]:
                logger.warning(f"Retryable error {response.status_code}: {response.text[:200]}")
                raise AmorceNetworkError(
                    f"Retryable HTTP {response.status_code}: {response.text}"
                )
            
            # Non-retryable client errors (4xx except 429)
            if 400 <= response.status_code < 500:
                raise AmorceAPIError(
                    f"API error {response.status_code}",
                    status_code=response.status_code,
                    response_body=response.text
                )
            
            # Server errors (5xx)
            if response.status_code >= 500:
                raise AmorceNetworkError(
                    f"Server error {response.status_code}: {response.text}"
                )
            
            return response
            
        except httpx.RequestError as e:
            # Network-level errors (DNS, connection refused, etc.)
            logger.error(f"Network error: {e}")
            raise AmorceNetworkError(f"Network error: {e}")
    
    async def transact(
        self,
        service_contract: Dict[str, Any],
        payload: Dict[str, Any],
        priority: str = PriorityLevel.NORMAL,
        idempotency_key: Optional[str] = None
    ) -> AmorceResponse:
        """
        Execute a transaction via the Orchestrator with AATP v1.1 protocol.
        
        Pipeline:
        1. Idempotency key generation (UUIDv4 if not provided)
        2. Canonical JSON serialization (RFC 8785)
        3. Ed25519 signature generation
        4. HTTP POST with retry logic (tenacity)
        5. Response parsing and validation
        
        Args:
            service_contract: Service identifier (must contain 'service_id')
            payload: Transaction payload (intent, params, etc.)
            priority: Priority level (normal|high|critical)
            idempotency_key: Optional idempotency key (auto-generated if None)
            
        Returns:
            AmorceResponse with transaction_id and result
            
        Raises:
            AmorceConfigError: If service_id is missing
            AmorceNetworkError: On network errors (after retries)
            AmorceAPIError: On API errors (4xx)
        """
        # Step 1: Validate service contract
        service_id = service_contract.get("service_id")
        if not service_id:
            raise AmorceConfigError("Invalid service contract: missing 'service_id'")
        
        # Step 2: Idempotency key generation
        if idempotency_key is None:
            idempotency_key = str(uuid.uuid4())
            logger.debug(f"Generated idempotency key: {idempotency_key}")
        
        # Step 3: Build canonical request body
        request_body = {
            "service_id": service_id,
            "consumer_agent_id": self.agent_id,
            "payload": payload,
            "priority": priority
        }
        
        # Step 4: Canonicalization (RFC 8785)
        canonical_bytes = self.identity.get_canonical_json_bytes(request_body)
        
        # Step 5: Sign with Ed25519
        signature = self.identity.sign_data(canonical_bytes)
        
        # Step 6: Construct headers
        headers = {
            "Content-Type": "application/json",
            "X-Agent-Signature": signature,
            "X-Amorce-Idempotency": idempotency_key,
            "X-Amorce-Agent-ID": self.agent_id
        }
        
        # SECURITY: Never log private keys
        logger.info(
            f"Transacting: service={service_id}, priority={priority}, "
            f"idempotency={idempotency_key}"
        )
        
        # Step 7: Execute with retry logic
        url = f"{self.config.orchestrator_url}/v1/a2a/transact"
        
        try:
            response = await self._execute_with_retry(url, request_body, headers)
            
            # Step 8: Parse response
            response_data = response.json()
            
            # Build AmorceResponse
            return AmorceResponse(
                transaction_id=response_data.get("transaction_id", idempotency_key),
                status_code=response.status_code,
                result=TransactionResult(
                    status=response_data.get("status", "success"),
                    message=response_data.get("message"),
                    data=response_data.get("data")
                ),
                error=None  # No error for successful responses
            )
            
        except (AmorceNetworkError, AmorceAPIError):
            # Re-raise Amorce exceptions
            raise
        except Exception as e:
            logger.error(f"Unexpected error in transact(): {e}")
            raise AmorceNetworkError(f"Transaction failed: {e}")
    
    async def discover(self, service_type: str) -> Dict[str, Any]:
        """
        Discover services from the Trust Directory.
        
        Args:
            service_type: Type of service to search for
            
        Returns:
            List of matching services
            
        Raises:
            AmorceNetworkError: On network errors
            AmorceAPIError: On API errors
        """
        if not self.client:
            raise AmorceConfigError("Client not initialized. Use 'async with' context manager.")
        
        url = f"{self.config.directory_url}/api/v1/services/search"
        
        try:
            response = await self.client.get(
                url,
                params={"service_type": service_type},
                timeout=10.0
            )
            
            if response.status_code != 200:
                raise AmorceAPIError(
                    f"Discovery failed: {response.status_code}",
                    status_code=response.status_code,
                    response_body=response.text
                )
            
            return response.json()
            
        except httpx.RequestError as e:
            logger.error(f"Discovery network error: {e}")
            raise AmorceNetworkError(f"Discovery failed: {e}")
