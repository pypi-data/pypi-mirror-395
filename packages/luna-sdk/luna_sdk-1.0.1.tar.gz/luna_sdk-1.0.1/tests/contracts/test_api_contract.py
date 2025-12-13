"""Contract validation tests for Python SDK."""
import pytest
import respx
from httpx import Response
import re

from luna import LunaClient
from tests.mocks.fixtures import (
    MOCK_USER,
    MOCK_PROJECT,
    MOCK_BUCKET,
    mock_list_response,
)

BASE_URL = "https://api.eclipse.dev"


@pytest.fixture
def client() -> LunaClient:
    """Create a LunaClient instance for testing."""
    return LunaClient(api_key="lk_test_12345678901234567890123456789012")


class TestUserContract:
    """Contract validation tests for User resource."""
    
    @respx.mock
    async def test_user_has_required_fields(self, client: LunaClient) -> None:
        """User should have all required fields."""
        respx.get(f"{BASE_URL}/v1/users/{MOCK_USER['id']}").mock(
            return_value=Response(200, json=MOCK_USER)
        )
        
        user = await client.users.get(MOCK_USER["id"])
        
        # Required fields
        assert hasattr(user, 'id')
        assert hasattr(user, 'name')
        assert hasattr(user, 'email')
        assert hasattr(user, 'created_at')
        assert hasattr(user, 'updated_at')
    
    @respx.mock
    async def test_user_id_format(self, client: LunaClient) -> None:
        """User ID should have correct prefix."""
        respx.get(f"{BASE_URL}/v1/users/{MOCK_USER['id']}").mock(
            return_value=Response(200, json=MOCK_USER)
        )
        
        user = await client.users.get(MOCK_USER["id"])
        
        assert user.id.startswith("usr_")
    
    @respx.mock
    async def test_user_email_format(self, client: LunaClient) -> None:
        """User email should be valid format."""
        respx.get(f"{BASE_URL}/v1/users/{MOCK_USER['id']}").mock(
            return_value=Response(200, json=MOCK_USER)
        )
        
        user = await client.users.get(MOCK_USER["id"])
        
        # Basic email validation
        email_pattern = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'
        assert re.match(email_pattern, user.email)


class TestProjectContract:
    """Contract validation tests for Project resource."""
    
    @respx.mock
    async def test_project_has_required_fields(self, client: LunaClient) -> None:
        """Project should have all required fields."""
        respx.get(f"{BASE_URL}/v1/projects/{MOCK_PROJECT['id']}").mock(
            return_value=Response(200, json=MOCK_PROJECT)
        )
        
        project = await client.projects.get(MOCK_PROJECT["id"])
        
        # Required fields
        assert hasattr(project, 'id')
        assert hasattr(project, 'name')
        assert hasattr(project, 'created_at')
        assert hasattr(project, 'updated_at')
    
    @respx.mock
    async def test_project_id_format(self, client: LunaClient) -> None:
        """Project ID should have correct prefix."""
        respx.get(f"{BASE_URL}/v1/projects/{MOCK_PROJECT['id']}").mock(
            return_value=Response(200, json=MOCK_PROJECT)
        )
        
        project = await client.projects.get(MOCK_PROJECT["id"])
        
        assert project.id.startswith("prj_")
    
    @respx.mock
    async def test_project_description_optional(self, client: LunaClient) -> None:
        """Project description should be optional (can be None)."""
        project_no_desc = {**MOCK_PROJECT, "description": None}
        respx.get(f"{BASE_URL}/v1/projects/prj_nodesc").mock(
            return_value=Response(200, json=project_no_desc)
        )
        
        project = await client.projects.get("prj_nodesc")
        
        # Should not raise even if description is None
        assert project.id is not None


class TestBucketContract:
    """Contract validation tests for Bucket resource."""
    
    @respx.mock
    async def test_bucket_has_required_fields(self, client: LunaClient) -> None:
        """Bucket should have all required fields."""
        respx.get(f"{BASE_URL}/v1/storage/buckets/{MOCK_BUCKET['id']}").mock(
            return_value=Response(200, json=MOCK_BUCKET)
        )
        
        bucket = await client.storage.buckets.get(MOCK_BUCKET["id"])
        
        # Required fields
        assert hasattr(bucket, 'id')
        assert hasattr(bucket, 'name')
        assert hasattr(bucket, 'created_at')
    
    @respx.mock
    async def test_bucket_id_format(self, client: LunaClient) -> None:
        """Bucket ID should have correct prefix."""
        respx.get(f"{BASE_URL}/v1/storage/buckets/{MOCK_BUCKET['id']}").mock(
            return_value=Response(200, json=MOCK_BUCKET)
        )
        
        bucket = await client.storage.buckets.get(MOCK_BUCKET["id"])
        
        assert bucket.id.startswith("bkt_")
    
    @respx.mock
    async def test_bucket_public_is_boolean(self, client: LunaClient) -> None:
        """Bucket public field should be boolean."""
        respx.get(f"{BASE_URL}/v1/storage/buckets/{MOCK_BUCKET['id']}").mock(
            return_value=Response(200, json=MOCK_BUCKET)
        )
        
        bucket = await client.storage.buckets.get(MOCK_BUCKET["id"])
        
        assert isinstance(bucket.public, bool)


class TestListResponseContract:
    """Contract validation tests for list responses."""
    
    @respx.mock
    async def test_list_response_structure(self, client: LunaClient) -> None:
        """List response should have correct structure."""
        respx.get(f"{BASE_URL}/v1/users").mock(
            return_value=Response(200, json=mock_list_response([MOCK_USER]))
        )
        
        result = await client.users.list()
        
        assert hasattr(result, 'data')
        assert hasattr(result, 'has_more')
        assert isinstance(result.data, list)
        assert isinstance(result.has_more, bool)
    
    @respx.mock
    async def test_list_response_with_pagination(self, client: LunaClient) -> None:
        """List response should include next_cursor when has_more is True."""
        respx.get(f"{BASE_URL}/v1/users").mock(
            return_value=Response(200, json={
                "data": [MOCK_USER],
                "has_more": True,
                "next_cursor": "cursor_abc123",
            })
        )
        
        result = await client.users.list()
        
        assert result.has_more is True
        assert result.next_cursor is not None
        assert isinstance(result.next_cursor, str)


class TestTimestampFormats:
    """Contract validation tests for timestamp formats."""
    
    @respx.mock
    async def test_timestamps_are_valid(self, client: LunaClient) -> None:
        """Timestamps should be valid datetime objects or ISO strings."""
        respx.get(f"{BASE_URL}/v1/users/{MOCK_USER['id']}").mock(
            return_value=Response(200, json=MOCK_USER)
        )
        
        user = await client.users.get(MOCK_USER["id"])
        
        # created_at should be parseable
        from datetime import datetime
        created = user.created_at
        
        if isinstance(created, str):
            # Should be valid ISO format
            datetime.fromisoformat(created.replace('Z', '+00:00'))
        elif isinstance(created, datetime):
            # Already a datetime object
            assert created is not None
