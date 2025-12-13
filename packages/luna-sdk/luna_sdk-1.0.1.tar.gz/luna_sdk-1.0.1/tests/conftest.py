"""Fixtures for Luna SDK tests."""

import pytest
from unittest.mock import AsyncMock, MagicMock


@pytest.fixture
def valid_api_key() -> str:
    """Return a valid test API key."""
    return "lk_test_aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"


@pytest.fixture
def access_token() -> str:
    """Return a test access token."""
    return "test-access-token"


@pytest.fixture
def refresh_token() -> str:
    """Return a test refresh token."""
    return "test-refresh-token"


@pytest.fixture
def mock_http_response() -> dict:
    """Return a mock HTTP response."""
    return {
        "id": "usr_abc123",
        "email": "test@example.com",
        "name": "Test User",
        "created_at": "2024-01-01T00:00:00Z",
        "updated_at": "2024-01-01T00:00:00Z",
    }


@pytest.fixture
def mock_users_list() -> dict:
    """Return a mock users list response."""
    return {
        "data": [
            {
                "id": "usr_abc123",
                "email": "test1@example.com",
                "name": "Test User 1",
                "created_at": "2024-01-01T00:00:00Z",
                "updated_at": "2024-01-01T00:00:00Z",
            },
            {
                "id": "usr_def456",
                "email": "test2@example.com",
                "name": "Test User 2",
                "created_at": "2024-01-02T00:00:00Z",
                "updated_at": "2024-01-02T00:00:00Z",
            },
        ],
        "has_more": False,
        "next_cursor": None,
    }
