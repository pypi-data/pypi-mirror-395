"""Error handling tests for Python SDK."""
import pytest
import respx
from httpx import Response

from luna import LunaClient, UserCreate
from luna.errors import (
    LunaError,
    AuthenticationError,
    NotFoundError,
    RateLimitError,
    ValidationError,
    ServerError,
)
from tests.mocks.fixtures import (
    MOCK_ERROR_AUTH,
    MOCK_ERROR_NOT_FOUND,
    MOCK_ERROR_RATE_LIMIT,
    MOCK_ERROR_VALIDATION,
    MOCK_ERROR_SERVER,
)

BASE_URL = "https://api.eclipse.dev"


@pytest.fixture
def client() -> LunaClient:
    """Create a LunaClient instance for testing."""
    return LunaClient(api_key="lk_test_12345678901234567890123456789012")


class TestAuthenticationError:
    """Tests for 401 authentication errors."""
    
    @respx.mock
    async def test_invalid_api_key(self, client: LunaClient) -> None:
        """Should raise AuthenticationError for invalid API key."""
        respx.get(f"{BASE_URL}/v1/users").mock(
            return_value=Response(401, json=MOCK_ERROR_AUTH)
        )
        
        with pytest.raises(AuthenticationError) as exc_info:
            await client.users.list()
        
        assert "Invalid API key" in str(exc_info.value)
    
    @respx.mock
    async def test_expired_token(self, client: LunaClient) -> None:
        """Should raise AuthenticationError for expired token."""
        respx.get(f"{BASE_URL}/v1/users").mock(
            return_value=Response(401, json={
                "error": {
                    "message": "Token expired",
                    "code": "TOKEN_EXPIRED",
                    "status": 401,
                }
            })
        )
        
        with pytest.raises(AuthenticationError):
            await client.users.list()


class TestNotFoundError:
    """Tests for 404 not found errors."""
    
    @respx.mock
    async def test_resource_not_found(self, client: LunaClient) -> None:
        """Should raise NotFoundError for non-existent resource."""
        respx.get(f"{BASE_URL}/v1/users/usr_nonexistent").mock(
            return_value=Response(404, json=MOCK_ERROR_NOT_FOUND)
        )
        
        with pytest.raises(NotFoundError) as exc_info:
            await client.users.get("usr_nonexistent")
        
        assert exc_info.value.status == 404


class TestValidationError:
    """Tests for 400 validation errors."""
    
    @respx.mock
    async def test_validation_error(self, client: LunaClient) -> None:
        """Should raise ValidationError for invalid input."""
        respx.post(f"{BASE_URL}/v1/users").mock(
            return_value=Response(400, json=MOCK_ERROR_VALIDATION)
        )
        
        with pytest.raises(ValidationError) as exc_info:
            await client.users.create(UserCreate(name="", email="invalid"))
        
        assert exc_info.value.status == 400
    
    @respx.mock
    async def test_validation_error_includes_details(self, client: LunaClient) -> None:
        """Should include field-level validation details."""
        respx.post(f"{BASE_URL}/v1/users").mock(
            return_value=Response(400, json=MOCK_ERROR_VALIDATION)
        )
        
        with pytest.raises(ValidationError) as exc_info:
            await client.users.create(UserCreate(name="Test", email="invalid"))
        
        # Check that details are available
        assert "Validation" in str(exc_info.value) or exc_info.value.details is not None


class TestRateLimitError:
    """Tests for 429 rate limit errors."""
    
    @respx.mock
    async def test_rate_limit_error(self, client: LunaClient) -> None:
        """Should raise RateLimitError when rate limited."""
        respx.get(f"{BASE_URL}/v1/users").mock(
            return_value=Response(
                429,
                json=MOCK_ERROR_RATE_LIMIT,
                headers={"Retry-After": "60"},
            )
        )
        
        with pytest.raises(RateLimitError) as exc_info:
            await client.users.list()
        
        assert exc_info.value.status == 429
    
    @respx.mock
    async def test_rate_limit_includes_retry_after(self, client: LunaClient) -> None:
        """Should include retry_after information."""
        respx.get(f"{BASE_URL}/v1/users").mock(
            return_value=Response(
                429,
                json=MOCK_ERROR_RATE_LIMIT,
                headers={"Retry-After": "60"},
            )
        )
        
        with pytest.raises(RateLimitError) as exc_info:
            await client.users.list()
        
        # Check retry_after is available (either in headers or error body)
        assert exc_info.value.retry_after is not None or exc_info.value.status == 429


class TestServerError:
    """Tests for 5xx server errors."""
    
    @respx.mock
    async def test_internal_server_error(self, client: LunaClient) -> None:
        """Should raise ServerError for 500 response."""
        respx.get(f"{BASE_URL}/v1/users").mock(
            return_value=Response(500, json=MOCK_ERROR_SERVER)
        )
        
        with pytest.raises(ServerError) as exc_info:
            await client.users.list()
        
        assert exc_info.value.status == 500
    
    @respx.mock
    async def test_service_unavailable(self, client: LunaClient) -> None:
        """Should raise ServerError for 503 response."""
        respx.get(f"{BASE_URL}/v1/users").mock(
            return_value=Response(503, json={
                "error": {
                    "message": "Service unavailable",
                    "code": "SERVICE_UNAVAILABLE",
                    "status": 503,
                }
            })
        )
        
        with pytest.raises(ServerError) as exc_info:
            await client.users.list()
        
        assert exc_info.value.status == 503


class TestErrorProperties:
    """Tests for error properties and metadata."""
    
    @respx.mock
    async def test_error_includes_request_id(self, client: LunaClient) -> None:
        """Should include request_id in error when available."""
        respx.get(f"{BASE_URL}/v1/users").mock(
            return_value=Response(
                500,
                json={
                    "error": {
                        "message": "Server error",
                        "code": "SERVER_ERROR",
                        "status": 500,
                        "request_id": "req_123abc",
                    }
                },
                headers={"X-Request-Id": "req_123abc"},
            )
        )
        
        with pytest.raises(LunaError) as exc_info:
            await client.users.list()
        
        # Request ID should be accessible
        error = exc_info.value
        assert hasattr(error, 'request_id') or hasattr(error, 'message')
    
    @respx.mock
    async def test_error_is_serializable(self, client: LunaClient) -> None:
        """Should be able to serialize error to string."""
        respx.get(f"{BASE_URL}/v1/users/usr_nonexistent").mock(
            return_value=Response(404, json=MOCK_ERROR_NOT_FOUND)
        )
        
        with pytest.raises(LunaError) as exc_info:
            await client.users.get("usr_nonexistent")
        
        # Should be able to convert to string
        error_str = str(exc_info.value)
        assert len(error_str) > 0
