"""Tests for LunaClient."""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from luna import LunaClient
from luna.errors import LunaError, AuthenticationError, NotFoundError


class TestLunaClient:
    """Tests for LunaClient initialization and configuration."""

    def test_create_client_with_api_key(self) -> None:
        """Should create client with API key."""
        client = LunaClient(api_key="lk_test_aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
        assert client.version == "1.0.0"

    def test_create_client_with_access_token(self) -> None:
        """Should create client with access token."""
        client = LunaClient(access_token="test-access-token")
        assert client.version == "1.0.0"

    def test_error_when_no_auth_provided(self) -> None:
        """Should raise error when no auth provided."""
        with pytest.raises(ValueError, match="Either api_key or access_token must be provided"):
            LunaClient()

    def test_custom_base_url(self) -> None:
        """Should accept custom base URL."""
        client = LunaClient(
            api_key="lk_test_aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
            base_url="https://api.staging.eclipse.dev",
        )
        assert client.version == "1.0.0"

    def test_resources_exposed(self) -> None:
        """Should expose users and projects resources."""
        client = LunaClient(api_key="lk_test_aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
        assert hasattr(client, "users")
        assert hasattr(client, "projects")


class TestLunaError:
    """Tests for LunaError."""

    def test_error_creation(self) -> None:
        """Should create error with all properties."""
        error = LunaError(
            code="LUNA_ERR_TEST",
            message="Test error",
            status=500,
            request_id="req_123",
            details={"key": "value"},
        )
        
        assert error.code == "LUNA_ERR_TEST"
        assert error.message == "Test error"
        assert error.status == 500
        assert error.request_id == "req_123"
        assert error.details == {"key": "value"}

    def test_error_docs_url(self) -> None:
        """Should generate docs URL."""
        error = LunaError(
            code="LUNA_ERR_TEST",
            message="Test error",
            status=500,
            request_id="req_123",
        )
        
        assert error.docs_url == "https://docs.eclipse.dev/luna/errors#LUNA_ERR_TEST"

    def test_error_to_dict(self) -> None:
        """Should convert error to dictionary."""
        error = LunaError(
            code="LUNA_ERR_TEST",
            message="Test error",
            status=500,
            request_id="req_123",
        )
        
        result = error.to_dict()
        assert result["code"] == "LUNA_ERR_TEST"
        assert result["message"] == "Test error"
        assert result["status"] == 500
        assert result["request_id"] == "req_123"

    def test_retryable_errors(self) -> None:
        """Should identify retryable errors."""
        server_error = LunaError(
            code="LUNA_ERR_SERVER_INTERNAL",
            message="Internal error",
            status=500,
            request_id="req_123",
        )
        
        auth_error = AuthenticationError(
            code="LUNA_ERR_AUTH_INVALID_KEY",
            message="Invalid key",
            status=401,
            request_id="req_123",
        )
        
        assert server_error.retryable is True
        assert auth_error.retryable is False


class TestErrorClasses:
    """Tests for specific error classes."""

    def test_authentication_error(self) -> None:
        """Should create AuthenticationError with 401 status."""
        error = AuthenticationError(
            code="LUNA_ERR_AUTH_INVALID_KEY",
            message="Invalid API key",
            status=401,
            request_id="req_123",
        )
        
        assert error.status == 401

    def test_not_found_error(self) -> None:
        """Should create NotFoundError with 404 status."""
        error = NotFoundError(
            code="LUNA_ERR_RESOURCE_NOT_FOUND",
            message="User not found",
            status=404,
            request_id="req_123",
        )
        
        assert error.status == 404
