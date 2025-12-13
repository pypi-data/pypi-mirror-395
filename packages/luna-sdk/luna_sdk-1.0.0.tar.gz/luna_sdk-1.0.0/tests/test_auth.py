"""Tests for auth providers."""

import pytest
from datetime import datetime, timedelta

from luna.auth import ApiKeyAuth, TokenAuth
from luna.errors import AuthenticationError


class TestApiKeyAuth:
    """Tests for API key authentication."""

    valid_api_key = "lk_test_aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"

    def test_create_with_valid_key(self) -> None:
        """Should create auth with valid API key."""
        auth = ApiKeyAuth(self.valid_api_key)
        assert auth is not None

    def test_error_on_empty_key(self) -> None:
        """Should raise error for empty API key."""
        with pytest.raises(AuthenticationError, match="API key is required"):
            ApiKeyAuth("")

    def test_error_on_invalid_format(self) -> None:
        """Should raise error for invalid API key format."""
        with pytest.raises(AuthenticationError, match="Invalid API key format"):
            ApiKeyAuth("invalid-key")

        with pytest.raises(AuthenticationError, match="Invalid API key format"):
            ApiKeyAuth("lk_invalid_key")

        with pytest.raises(AuthenticationError, match="Invalid API key format"):
            ApiKeyAuth("lk_test_short")

    @pytest.mark.asyncio
    async def test_get_headers(self) -> None:
        """Should return correct headers."""
        auth = ApiKeyAuth(self.valid_api_key)
        headers = await auth.get_headers()
        
        assert headers == {"X-Luna-Api-Key": self.valid_api_key}

    def test_needs_refresh(self) -> None:
        """Should not need refresh."""
        auth = ApiKeyAuth(self.valid_api_key)
        assert auth.needs_refresh() is False


class TestTokenAuth:
    """Tests for token authentication."""

    access_token = "test-access-token"
    refresh_token = "test-refresh-token"

    def test_create_with_access_token(self) -> None:
        """Should create auth with access token."""
        auth = TokenAuth(access_token=self.access_token)
        assert auth is not None

    def test_error_on_empty_token(self) -> None:
        """Should raise error for empty access token."""
        with pytest.raises(AuthenticationError, match="Access token is required"):
            TokenAuth(access_token="")

    @pytest.mark.asyncio
    async def test_get_headers(self) -> None:
        """Should return correct headers."""
        auth = TokenAuth(access_token=self.access_token)
        headers = await auth.get_headers()
        
        assert headers == {"Authorization": f"Bearer {self.access_token}"}

    def test_needs_refresh_without_expiry(self) -> None:
        """Should not need refresh without expiry."""
        auth = TokenAuth(access_token=self.access_token)
        assert auth.needs_refresh() is False

    def test_update_tokens(self) -> None:
        """Should update tokens."""
        auth = TokenAuth(
            access_token=self.access_token,
            refresh_token=self.refresh_token,
        )
        
        from luna.auth.types import TokenPair
        
        auth.update_tokens(TokenPair(
            access_token="new-access-token",
            refresh_token="new-refresh-token",
            expires_at=datetime.now() + timedelta(hours=1),
        ))
        
        assert auth.needs_refresh() is False
