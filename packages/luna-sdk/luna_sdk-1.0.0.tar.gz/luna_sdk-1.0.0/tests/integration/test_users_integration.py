"""Integration tests for Users resource."""
import pytest
import respx
from httpx import Response

from luna import LunaClient, UserCreate, UserUpdate
from tests.mocks.fixtures import (
    MOCK_USER,
    MOCK_USERS,
    mock_list_response,
)

BASE_URL = "https://api.eclipse.dev"


@pytest.fixture
def client() -> LunaClient:
    """Create a LunaClient instance for testing."""
    return LunaClient(api_key="lk_test_12345678901234567890123456789012")


class TestUsersCRUDWorkflow:
    """Integration tests for full CRUD workflow."""
    
    @respx.mock
    async def test_full_crud_workflow(self, client: LunaClient) -> None:
        """Should complete create, read, update, delete workflow."""
        created_id = "usr_integrationtest"
        
        # CREATE
        respx.post(f"{BASE_URL}/v1/users").mock(
            return_value=Response(201, json={
                "id": created_id,
                "name": "Integration User",
                "email": "integration@test.com",
                "created_at": "2024-01-01T00:00:00Z",
                "updated_at": "2024-01-01T00:00:00Z",
            })
        )
        
        created = await client.users.create(UserCreate(
            name="Integration User",
            email="integration@test.com",
        ))
        assert created.id == created_id
        
        # READ
        respx.get(f"{BASE_URL}/v1/users/{created_id}").mock(
            return_value=Response(200, json={
                "id": created_id,
                "name": "Integration User",
                "email": "integration@test.com",
                "created_at": "2024-01-01T00:00:00Z",
                "updated_at": "2024-01-01T00:00:00Z",
            })
        )
        
        fetched = await client.users.get(created_id)
        assert fetched.id == created_id
        
        # UPDATE
        respx.patch(f"{BASE_URL}/v1/users/{created_id}").mock(
            return_value=Response(200, json={
                "id": created_id,
                "name": "Updated Name",
                "email": "integration@test.com",
                "created_at": "2024-01-01T00:00:00Z",
                "updated_at": "2024-01-01T00:00:00Z",
            })
        )
        
        updated = await client.users.update(created_id, UserUpdate(name="Updated Name"))
        assert updated.name == "Updated Name"
        
        # DELETE
        respx.delete(f"{BASE_URL}/v1/users/{created_id}").mock(
            return_value=Response(204)
        )
        
        await client.users.delete(created_id)


class TestUsersPaginationWorkflow:
    """Integration tests for pagination workflow."""
    
    @respx.mock
    async def test_paginate_through_all_users(self, client: LunaClient) -> None:
        """Should paginate through all users."""
        call_count = 0
        
        def mock_handler(request):
            nonlocal call_count
            call_count += 1
            
            # Parse cursor from URL if present
            cursor = None
            if "cursor=" in str(request.url):
                cursor = str(request.url).split("cursor=")[1].split("&")[0]
            
            if cursor is None:
                return Response(200, json={
                    "data": MOCK_USERS[:1],
                    "has_more": True,
                    "next_cursor": "page2",
                })
            elif cursor == "page2":
                return Response(200, json={
                    "data": MOCK_USERS[1:],
                    "has_more": False,
                    "next_cursor": None,
                })
            return Response(200, json={"data": [], "has_more": False})
        
        respx.get(f"{BASE_URL}/v1/users").mock(side_effect=mock_handler)
        
        # Fetch first page
        page1 = await client.users.list(limit=1)
        assert len(page1.data) == 1
        assert page1.has_more is True
        
        # Fetch second page
        page2 = await client.users.list(cursor=page1.next_cursor)
        assert len(page2.data) > 0
        assert page2.has_more is False
        
        assert call_count == 2


class TestRequestHeaders:
    """Integration tests for request header handling."""
    
    @respx.mock
    async def test_sends_correct_auth_header(self) -> None:
        """Should send correct Authorization header."""
        from luna.auth import TokenAuth

        client = LunaClient(
            base_url=BASE_URL,
            access_token="test-token"
        )

        captured_request = None
        
        def capture_request(request):
            nonlocal captured_request
            captured_request = request
            return Response(200, json=mock_list_response(MOCK_USERS))
        
        respx.get(f"{BASE_URL}/v1/users").mock(side_effect=capture_request)
        
        await client.users.list()
        
        assert captured_request is not None
        assert "Authorization" in captured_request.headers
        assert captured_request.headers["Authorization"].startswith("Bearer ")
    
    @respx.mock
    async def test_sends_content_type_header(self, client: LunaClient) -> None:
        """Should send Content-Type header for POST requests."""
        captured_request = None
        
        def capture_request(request):
            nonlocal captured_request
            captured_request = request
            return Response(201, json=MOCK_USER)
        
        respx.post(f"{BASE_URL}/v1/users").mock(side_effect=capture_request)
        
        await client.users.create(UserCreate(name="Test", email="test@test.com"))
        
        assert captured_request is not None
        assert "Content-Type" in captured_request.headers
        assert "application/json" in captured_request.headers["Content-Type"]
