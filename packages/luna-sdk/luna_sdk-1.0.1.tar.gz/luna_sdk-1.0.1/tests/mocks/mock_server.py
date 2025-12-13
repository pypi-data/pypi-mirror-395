"""Mock server setup for Python SDK tests using respx."""
import respx
from httpx import Response
import json
from typing import Any

from .fixtures import (
    MOCK_USER,
    MOCK_USERS,
    MOCK_PROJECT,
    MOCK_PROJECTS,
    MOCK_BUCKET,
    MOCK_BUCKETS,
    MOCK_FILE,
    mock_list_response,
    MOCK_ERROR_NOT_FOUND,
    MOCK_ERROR_AUTH,
)

BASE_URL = "https://api.eclipse.dev"


def setup_mock_routes(mock: respx.MockRouter) -> None:
    """Set up all mock routes for the API."""
    
    # ==================== USERS ====================
    
    # List users
    mock.get(f"{BASE_URL}/v1/users").mock(
        return_value=Response(200, json=mock_list_response(MOCK_USERS))
    )
    
    # Get user by ID (success)
    mock.get(f"{BASE_URL}/v1/users/{MOCK_USER['id']}").mock(
        return_value=Response(200, json=MOCK_USER)
    )
    
    # Get user by ID (not found)
    mock.get(f"{BASE_URL}/v1/users/usr_nonexistent").mock(
        return_value=Response(404, json=MOCK_ERROR_NOT_FOUND)
    )
    
    # Create user
    mock.post(f"{BASE_URL}/v1/users").mock(
        return_value=Response(201, json={
            **MOCK_USER,
            "id": f"usr_{int(__import__('time').time())}",
        })
    )
    
    # Update user
    mock.patch(f"{BASE_URL}/v1/users/{MOCK_USER['id']}").mock(
        return_value=Response(200, json=MOCK_USER)
    )
    
    # Delete user (success)
    mock.delete(f"{BASE_URL}/v1/users/{MOCK_USER['id']}").mock(
        return_value=Response(204)
    )
    
    # Delete user (not found)
    mock.delete(f"{BASE_URL}/v1/users/usr_nonexistent").mock(
        return_value=Response(404, json=MOCK_ERROR_NOT_FOUND)
    )
    
    # ==================== PROJECTS ====================
    
    # List projects
    mock.get(f"{BASE_URL}/v1/projects").mock(
        return_value=Response(200, json=mock_list_response(MOCK_PROJECTS))
    )
    
    # Get project by ID (success)
    mock.get(f"{BASE_URL}/v1/projects/{MOCK_PROJECT['id']}").mock(
        return_value=Response(200, json=MOCK_PROJECT)
    )
    
    # Get project by ID (not found)
    mock.get(f"{BASE_URL}/v1/projects/prj_nonexistent").mock(
        return_value=Response(404, json=MOCK_ERROR_NOT_FOUND)
    )
    
    # Create project
    mock.post(f"{BASE_URL}/v1/projects").mock(
        return_value=Response(201, json={
            **MOCK_PROJECT,
            "id": f"prj_{int(__import__('time').time())}",
        })
    )
    
    # Delete project (success)
    mock.delete(f"{BASE_URL}/v1/projects/{MOCK_PROJECT['id']}").mock(
        return_value=Response(204)
    )
    
    # ==================== STORAGE ====================
    
    # List buckets
    mock.get(f"{BASE_URL}/v1/storage/buckets").mock(
        return_value=Response(200, json=mock_list_response(MOCK_BUCKETS))
    )
    
    # Get bucket by ID
    mock.get(f"{BASE_URL}/v1/storage/buckets/{MOCK_BUCKET['id']}").mock(
        return_value=Response(200, json=MOCK_BUCKET)
    )
    
    # List files in bucket
    mock.get(f"{BASE_URL}/v1/storage/buckets/{MOCK_BUCKET['id']}/files").mock(
        return_value=Response(200, json=mock_list_response([MOCK_FILE]))
    )
    
    # Upload file
    mock.post(f"{BASE_URL}/v1/storage/buckets/{MOCK_BUCKET['id']}/upload").mock(
        return_value=Response(201, json=MOCK_FILE)
    )
    
    # ==================== HEALTH ====================
    
    mock.get(f"{BASE_URL}/health").mock(
        return_value=Response(200, json={"status": "healthy", "version": "1.0.0"})
    )


def setup_error_routes(mock: respx.MockRouter) -> None:
    """Set up error simulation routes."""
    
    # Rate limit
    mock.get(f"{BASE_URL}/v1/users").mock(
        return_value=Response(
            429,
            json={"error": {"message": "Rate limit exceeded", "code": "RATE_LIMIT_EXCEEDED", "status": 429}},
            headers={"Retry-After": "60"},
        )
    )


def setup_auth_error_routes(mock: respx.MockRouter) -> None:
    """Set up authentication error routes."""
    mock.get(f"{BASE_URL}/v1/users").mock(
        return_value=Response(401, json=MOCK_ERROR_AUTH)
    )
