"""Unit tests for UsersResource."""
import pytest
import respx
from httpx import Response

from luna import LunaClient, UserCreate, UserUpdate
from luna.errors import NotFoundError, ValidationError
from tests.mocks.fixtures import (
    MOCK_USER,
    MOCK_USERS,
    MOCK_USER_CREATE,
    mock_list_response,
    MOCK_ERROR_NOT_FOUND,
)

BASE_URL = "https://api.eclipse.dev"


@pytest.fixture
def client() -> LunaClient:
    """Create a LunaClient instance for testing."""
    return LunaClient(api_key="lk_test_12345678901234567890123456789012")


class TestUsersList:
    """Tests for users.list()"""
    
    @respx.mock
    async def test_list_users_success(self, client: LunaClient) -> None:
        """Should return a list of users."""
        respx.get(f"{BASE_URL}/v1/users").mock(
            return_value=Response(200, json=mock_list_response(MOCK_USERS))
        )
        
        result = await client.users.list()
        
        assert len(result.data) == len(MOCK_USERS)
        assert result.data[0].id == MOCK_USERS[0]["id"]
        assert result.data[0].name == MOCK_USERS[0]["name"]
    
    @respx.mock
    async def test_list_users_with_limit(self, client: LunaClient) -> None:
        """Should support pagination with limit."""
        respx.get(f"{BASE_URL}/v1/users").mock(
            return_value=Response(200, json=mock_list_response(MOCK_USERS[:1]))
        )
        
        result = await client.users.list(limit=1)
        
        assert len(result.data) == 1
    
    @respx.mock
    async def test_list_users_with_cursor(self, client: LunaClient) -> None:
        """Should support pagination with cursor."""
        respx.get(f"{BASE_URL}/v1/users").mock(
            return_value=Response(200, json=mock_list_response(MOCK_USERS[1:], has_more=False))
        )
        
        result = await client.users.list(cursor="next_cursor")
        
        assert result.data is not None


class TestUsersGet:
    """Tests for users.get()"""
    
    @respx.mock
    async def test_get_user_success(self, client: LunaClient) -> None:
        """Should return a single user by ID."""
        respx.get(f"{BASE_URL}/v1/users/{MOCK_USER['id']}").mock(
            return_value=Response(200, json=MOCK_USER)
        )
        
        result = await client.users.get(MOCK_USER["id"])
        
        assert result.id == MOCK_USER["id"]
        assert result.name == MOCK_USER["name"]
        assert result.email == MOCK_USER["email"]
    
    @respx.mock
    async def test_get_user_not_found(self, client: LunaClient) -> None:
        """Should raise NotFoundError for non-existent user."""
        respx.get(f"{BASE_URL}/v1/users/usr_nonexistent").mock(
            return_value=Response(404, json=MOCK_ERROR_NOT_FOUND)
        )
        
        with pytest.raises(NotFoundError):
            await client.users.get("usr_nonexistent")


class TestUsersCreate:
    """Tests for users.create()"""
    
    @respx.mock
    async def test_create_user_success(self, client: LunaClient) -> None:
        """Should create a new user."""
        new_user = {**MOCK_USER, "id": "usr_new123", "name": MOCK_USER_CREATE["name"]}
        respx.post(f"{BASE_URL}/v1/users").mock(
            return_value=Response(201, json=new_user)
        )
        
        result = await client.users.create(UserCreate(
            name=MOCK_USER_CREATE["name"],
            email=MOCK_USER_CREATE["email"],
        ))
        
        assert result.name == MOCK_USER_CREATE["name"]
        assert result.id.startswith("usr_")
    
    @respx.mock
    async def test_create_user_validation_error(self, client: LunaClient) -> None:
        """Should raise ValidationError for invalid input."""
        respx.post(f"{BASE_URL}/v1/users").mock(
            return_value=Response(400, json={
                "error": {
                    "message": "Validation failed",
                    "code": "VALIDATION_ERROR",
                    "status": 400,
                }
            })
        )
        
        with pytest.raises(ValidationError):
            await client.users.create(UserCreate(name="Invalid", email="invalid"))


class TestUsersUpdate:
    """Tests for users.update()"""
    
    @respx.mock
    async def test_update_user_success(self, client: LunaClient) -> None:
        """Should update an existing user."""
        updated = {**MOCK_USER, "name": "Updated Name"}
        respx.patch(f"{BASE_URL}/v1/users/{MOCK_USER['id']}").mock(
            return_value=Response(200, json=updated)
        )
        
        result = await client.users.update(MOCK_USER["id"], UserUpdate(name="Updated Name"))
        
        assert result.name == "Updated Name"
    
    @respx.mock
    async def test_update_user_not_found(self, client: LunaClient) -> None:
        """Should raise NotFoundError for non-existent user."""
        respx.patch(f"{BASE_URL}/v1/users/usr_nonexistent").mock(
            return_value=Response(404, json=MOCK_ERROR_NOT_FOUND)
        )
        
        with pytest.raises(NotFoundError):
            await client.users.update("usr_nonexistent", UserUpdate(name="Test"))


class TestUsersDelete:
    """Tests for users.delete()"""
    
    @respx.mock
    async def test_delete_user_success(self, client: LunaClient) -> None:
        """Should delete an existing user."""
        respx.delete(f"{BASE_URL}/v1/users/{MOCK_USER['id']}").mock(
            return_value=Response(204)
        )
        
        # Should not raise
        await client.users.delete(MOCK_USER["id"])
    
    @respx.mock
    async def test_delete_user_not_found(self, client: LunaClient) -> None:
        """Should raise NotFoundError for non-existent user."""
        respx.delete(f"{BASE_URL}/v1/users/usr_nonexistent").mock(
            return_value=Response(404, json=MOCK_ERROR_NOT_FOUND)
        )
        
        with pytest.raises(NotFoundError):
            await client.users.delete("usr_nonexistent")
