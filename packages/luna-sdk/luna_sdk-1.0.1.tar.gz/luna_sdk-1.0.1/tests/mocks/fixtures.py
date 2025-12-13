"""Test data fixtures for Python SDK tests."""
from datetime import datetime
from typing import Any

# User fixtures
MOCK_USER: dict[str, Any] = {
    "id": "usr_123456789",
    "name": "John Doe",
    "email": "john@example.com",
    "avatar": "https://example.com/avatar.jpg",
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:00:00Z",
}

MOCK_USERS: list[dict[str, Any]] = [
    MOCK_USER,
    {
        "id": "usr_987654321",
        "name": "Jane Smith",
        "email": "jane@example.com",
        "avatar": None,
        "created_at": "2024-01-02T00:00:00Z",
        "updated_at": "2024-01-02T00:00:00Z",
    },
]

MOCK_USER_CREATE: dict[str, str] = {
    "name": "New User",
    "email": "newuser@example.com",
}

# Project fixtures
MOCK_PROJECT: dict[str, Any] = {
    "id": "prj_123456789",
    "name": "Test Project",
    "description": "A test project for unit tests",
    "owner_id": "usr_123456789",
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:00:00Z",
}

MOCK_PROJECTS: list[dict[str, Any]] = [
    MOCK_PROJECT,
    {
        "id": "prj_987654321",
        "name": "Another Project",
        "description": "Another test project",
        "owner_id": "usr_987654321",
        "created_at": "2024-01-02T00:00:00Z",
        "updated_at": "2024-01-02T00:00:00Z",
    },
]

MOCK_PROJECT_CREATE: dict[str, str] = {
    "name": "New Project",
    "description": "A new project",
}

# Storage fixtures
MOCK_BUCKET: dict[str, Any] = {
    "id": "bkt_123456789",
    "name": "test-bucket",
    "public": False,
    "created_at": "2024-01-01T00:00:00Z",
}

MOCK_BUCKETS: list[dict[str, Any]] = [
    MOCK_BUCKET,
    {
        "id": "bkt_987654321",
        "name": "public-bucket",
        "public": True,
        "created_at": "2024-01-02T00:00:00Z",
    },
]

MOCK_FILE: dict[str, Any] = {
    "id": "file_123456789",
    "name": "test-file.pdf",
    "bucket_id": "bkt_123456789",
    "size": 1024,
    "mime_type": "application/pdf",
    "created_at": "2024-01-01T00:00:00Z",
}


def mock_list_response(data: list, has_more: bool = False, next_cursor: str | None = None) -> dict:
    """Create a mock list response."""
    return {
        "data": data,
        "has_more": has_more,
        "next_cursor": next_cursor,
    }


# Error response fixtures
MOCK_ERROR_NOT_FOUND: dict[str, Any] = {
    "error": {
        "message": "Resource not found",
        "code": "NOT_FOUND",
        "status": 404,
    }
}

MOCK_ERROR_VALIDATION: dict[str, Any] = {
    "error": {
        "message": "Validation failed",
        "code": "VALIDATION_ERROR",
        "status": 400,
        "details": [
            {"field": "email", "message": "Invalid email format"},
        ],
    }
}

MOCK_ERROR_RATE_LIMIT: dict[str, Any] = {
    "error": {
        "message": "Rate limit exceeded",
        "code": "RATE_LIMIT_EXCEEDED",
        "status": 429,
        "retry_after": 60,
    }
}

MOCK_ERROR_AUTH: dict[str, Any] = {
    "error": {
        "message": "Invalid API key",
        "code": "AUTHENTICATION_ERROR",
        "status": 401,
    }
}

MOCK_ERROR_SERVER: dict[str, Any] = {
    "error": {
        "message": "Internal server error",
        "code": "SERVER_ERROR",
        "status": 500,
    }
}
