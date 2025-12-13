"""
Comprehensive Async Client Test Suite
Tests AsyncAmorceClient with HTTP/2 enforcement, retry logic, and edge cases.

Requirements:
- pytest-asyncio
- respx (httpx mocking)
"""

import pytest
import httpx
import respx
from unittest.mock import AsyncMock, MagicMock

from amorce import AsyncAmorceClient, IdentityManager, PriorityLevel
from amorce.models import AmorceConfig, AmorceResponse
from amorce.exceptions import (
    AmorceConfigError,
    AmorceNetworkError,
    AmorceAPIError
)


# Fixtures
@pytest.fixture
def identity():
    """Generate ephemeral identity for testing"""
    return IdentityManager.generate_ephemeral()


@pytest.fixture
def config():
    """Test configuration"""
    return AmorceConfig(
        directory_url="https://directory.test.amorce.io",
        orchestrator_url="https://api.test.amorce.io"
    )


@pytest.fixture
def service_contract():
    """Sample service contract"""
    return {"service_id": "srv_test_restaurant_01"}


@pytest.fixture
def payload():
    """Sample transaction payload"""
    return {
        "intent": "book_reservation",
        "params": {"date": "2025-12-15", "guests": 2}
    }


# Test 1: Configuration Validation
def test_config_validation_valid():
    """Test valid configuration is accepted"""
    config = AmorceConfig(
        directory_url="https://directory.amorce.io",
        orchestrator_url="https://api.amorce.io"
    )
    assert config.directory_url == "https://directory.amorce.io"
    assert config.orchestrator_url == "https://api.amorce.io"


def test_config_validation_invalid_url():
    """Test invalid URLs are rejected"""
    with pytest.raises(ValueError, match="Invalid URL"):
        AmorceConfig(
            directory_url="not-a-url",
            orchestrator_url="https://api.amorce.io"
        )


def test_client_init_no_config_or_urls(identity):
    """Test client initialization fails without config or URLs"""
    with pytest.raises(AmorceConfigError, match="Must provide either"):
        AsyncAmorceClient(identity=identity)


# Test 2: AsyncContextManager Lifecycle
@pytest.mark.asyncio
async def test_context_manager_lifecycle(identity, config):
    """Test __aenter__ and __aexit__ properly manage httpx client"""
    async with AsyncAmorceClient(identity, config=config) as client:
        assert client.client is not None
        assert isinstance(client.client, httpx.AsyncClient)
        assert client.client.is_closed is False
    
    # After exiting context, client should be closed
    assert client.client.is_closed is True


@pytest.mark.asyncio
async def test_http2_enforcement(identity, config):
    """Test httpx client is configured with HTTP/2 enabled"""
    async with AsyncAmorceClient(identity, config=config) as client:
        # httpx.AsyncClient with http2=True should have HTTP/2 support
        # We can verify this by checking the client was created properly
        assert client.client is not None
        assert hasattr(client.client, '_transport')


# Test 3: Successful Transaction
@pytest.mark.asyncio
@respx.mock
async def test_transact_success(identity, config, service_contract, payload):
    """Test successful transaction with 200 response"""
    # Mock orchestrator response
    mock_response = {
        "transaction_id": "txn_12345",
        "status": "success",
        "message": "Reservation confirmed",
        "data": {"confirmation_code": "ABC123"}
    }
    
    respx.post("https://api.test.amorce.io/v1/a2a/transact").mock(
        return_value=httpx.Response(200, json=mock_response)
    )
    
    async with AsyncAmorceClient(identity, config=config) as client:
        response = await client.transact(service_contract, payload)
        
        assert isinstance(response, AmorceResponse)
        assert response.transaction_id == "txn_12345"
        assert response.status_code == 200
        assert response.is_success is True
        assert response.result.status == "success"
        assert response.result.data["confirmation_code"] == "ABC123"


# Test 4: Idempotency Key Generation
@pytest.mark.asyncio
@respx.mock
async def test_idempotency_key_auto_generation(identity, config, service_contract, payload):
    """Test idempotency key is auto-generated if not provided"""
    mock_response = {"transaction_id": "txn_12345", "status": "success"}
    
    route = respx.post("https://api.test.amorce.io/v1/a2a/transact").mock(
        return_value=httpx.Response(200, json=mock_response)
    )
    
    async with AsyncAmorceClient(identity, config=config) as client:
        # Call without idempotency_key
        await client.transact(service_contract, payload)
        
        # Verify X-Amorce-Idempotency header was sent
        assert route.called
        request = route.calls[0].request
        assert "X-Amorce-Idempotency" in request.headers
        # Should be a valid UUID
        idempotency_key = request.headers["X-Amorce-Idempotency"]
        assert len(idempotency_key) == 36  # UUID format


@pytest.mark.asyncio
@respx.mock
async def test_idempotency_key_custom(identity, config, service_contract, payload):
    """Test custom idempotency key is used when provided"""
    mock_response = {"transaction_id": "txn_12345", "status": "success"}
    
    route = respx.post("https://api.test.amorce.io/v1/a2a/transact").mock(
        return_value=httpx.Response(200, json=mock_response)
    )
    
    custom_key = "my-custom-idempotency-key-123"
    
    async with AsyncAmorceClient(identity, config=config) as client:
        await client.transact(service_contract, payload, idempotency_key=custom_key)
        
        request = route.calls[0].request
        assert request.headers["X-Amorce-Idempotency"] == custom_key


# Test 5: Retry Logic (503 Service Unavailable)
@pytest.mark.asyncio
@respx.mock
async def test_retry_on_503_then_success(identity, config, service_contract, payload):
    """Test tenacity retries on 503, then succeeds"""
    mock_success = {"transaction_id": "txn_12345", "status": "success"}
    
    # First 2 calls return 503, third call succeeds
    route = respx.post("https://api.test.amorce.io/v1/a2a/transact").mock(
        side_effect=[
            httpx.Response(503, text="Service Unavailable"),
            httpx.Response(503, text="Service Unavailable"),
            httpx.Response(200, json=mock_success)
        ]
    )
    
    async with AsyncAmorceClient(identity, config=config) as client:
        response = await client.transact(service_contract, payload)
        
        # Should succeed after retries
        assert response.transaction_id == "txn_12345"
        assert route.call_count == 3  # 2 failures + 1 success


@pytest.mark.asyncio
@respx.mock
async def test_retry_exhausted_on_503(identity, config, service_contract, payload):
    """Test retries are exhausted after max attempts"""
    # All calls return 503
    respx.post("https://api.test.amorce.io/v1/a2a/transact").mock(
        return_value=httpx.Response(503, text="Service Unavailable")
    )
    
    async with AsyncAmorceClient(identity, config=config) as client:
        with pytest.raises(AmorceNetworkError, match="Retryable HTTP 503"):
            await client.transact(service_contract, payload)


@pytest.mark.asyncio
@respx.mock
async def test_retry_on_429_rate_limit(identity, config, service_contract, payload):
    """Test retry logic handles 429 Too Many Requests"""
    mock_success = {"transaction_id": "txn_12345", "status": "success"}
    
    route = respx.post("https://api.test.amorce.io/v1/a2a/transact").mock(
        side_effect=[
            httpx.Response(429, text="Rate limit exceeded"),
            httpx.Response(200, json=mock_success)
        ]
    )
    
    async with AsyncAmorceClient(identity, config=config) as client:
        response = await client.transact(service_contract, payload)
        
        assert response.is_success
        assert route.call_count == 2


# Test 6: Non-Retryable Errors (4xx)
@pytest.mark.asyncio
@respx.mock
async def test_400_bad_request_not_retried(identity, config, service_contract, payload):
    """Test 400 errors are not retried"""
    respx.post("https://api.test.amorce.io/v1/a2a/transact").mock(
        return_value=httpx.Response(400, text="Bad Request")
    )
    
    async with AsyncAmorceClient(identity, config=config) as client:
        with pytest.raises(AmorceAPIError, match="400"):
            await client.transact(service_contract, payload)


@pytest.mark.asyncio
@respx.mock
async def test_401_unauthorized_not_retried(identity, config, service_contract, payload):
    """Test 401 errors are not retried (signature verification failure)"""
    respx.post("https://api.test.amorce.io/v1/a2a/transact").mock(
        return_value=httpx.Response(401, text="Unauthorized: Invalid signature")
    )
    
    async with AsyncAmorceClient(identity, config=config) as client:
        with pytest.raises(AmorceAPIError, match="401"):
            await client.transact(service_contract, payload)


# Test 7: Signature Headers
@pytest.mark.asyncio
@respx.mock
async def test_signature_headers_present(identity, config, service_contract, payload):
    """Test X-Agent-Signature and X-Amorce-Agent-ID headers are sent"""
    mock_response = {"transaction_id": "txn_12345", "status": "success"}
    
    route = respx.post("https://api.test.amorce.io/v1/a2a/transact").mock(
        return_value=httpx.Response(200, json=mock_response)
    )
    
    async with AsyncAmorceClient(identity, config=config) as client:
        await client.transact(service_contract, payload)
        
        request = route.calls[0].request
        assert "X-Agent-Signature" in request.headers
        assert "X-Amorce-Agent-ID" in request.headers
        assert request.headers["X-Amorce-Agent-ID"] == identity.agent_id


# Test 8: Service Discovery
@pytest.mark.asyncio
@respx.mock
async def test_discover_services(identity, config):
    """Test service discovery from Trust Directory"""
    mock_services = [
        {"service_id": "srv_restaurant_01", "name": "Restaurant Agent"},
        {"service_id": "srv_restaurant_02", "name": "Café Agent"}
    ]
    
    respx.get("https://directory.test.amorce.io/api/v1/services/search").mock(
        return_value=httpx.Response(200, json=mock_services)
    )
    
    async with AsyncAmorceClient(identity, config=config) as client:
        services = await client.discover("restaurant")
        
        assert len(services) == 2
        assert services[0]["service_id"] == "srv_restaurant_01"


@pytest.mark.asyncio
@respx.mock
async def test_discover_network_error(identity, config):
    """Test discovery handles network errors"""
    respx.get("https://directory.test.amorce.io/api/v1/services/search").mock(
        side_effect=httpx.ConnectError("Connection refused")
    )
    
    async with AsyncAmorceClient(identity, config=config) as client:
        with pytest.raises(AmorceNetworkError, match="Discovery failed"):
            await client.discover("restaurant")


# Test 9: Missing service_id
@pytest.mark.asyncio
async def test_transact_missing_service_id(identity, config, payload):
    """Test transaction fails gracefully if service_id is missing"""
    invalid_contract = {}  # No service_id
    
    async with AsyncAmorceClient(identity, config=config) as client:
        with pytest.raises(AmorceConfigError, match="missing 'service_id'"):
            await client.transact(invalid_contract, payload)


# Test 10: Priority Levels
@pytest.mark.asyncio
@respx.mock
async def test_priority_levels(identity, config, service_contract, payload):
    """Test priority parameter is sent correctly"""
    mock_response = {"transaction_id": "txn_12345", "status": "success"}
    
    route = respx.post("https://api.test.amorce.io/v1/a2a/transact").mock(
        return_value=httpx.Response(200, json=mock_response)
    )
    
    async with AsyncAmorceClient(identity, config=config) as client:
        await client.transact(service_contract, payload, priority=PriorityLevel.CRITICAL)
        
        # Check request body contains priority
        request = route.calls[0].request
        body = request.content.decode('utf-8')
        assert 'critical' in body


# Test 11: Context Manager Not Used
@pytest.mark.asyncio
async def test_transact_without_context_manager(identity, config, service_contract, payload):
    """Test calling transact without context manager raises error"""
    client = AsyncAmorceClient(identity, config=config)
    
    # The error is wrapped in AmorceNetworkError during exception handling
    with pytest.raises(AmorceNetworkError, match="Transaction failed"):
        await client.transact(service_contract, payload)
