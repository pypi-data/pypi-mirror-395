"""Unit tests for ProjectsResource."""
import pytest
import respx
from httpx import Response

from luna import LunaClient, ProjectCreate
from luna.errors import NotFoundError, ValidationError
from tests.mocks.fixtures import (
    MOCK_PROJECT,
    MOCK_PROJECTS,
    MOCK_PROJECT_CREATE,
    mock_list_response,
    MOCK_ERROR_NOT_FOUND,
)

BASE_URL = "https://api.eclipse.dev"


@pytest.fixture
def client() -> LunaClient:
    """Create a LunaClient instance for testing."""
    return LunaClient(api_key="lk_test_12345678901234567890123456789012")


class TestProjectsList:
    """Tests for projects.list()"""
    
    @respx.mock
    async def test_list_projects_success(self, client: LunaClient) -> None:
        """Should return a list of projects."""
        respx.get(f"{BASE_URL}/v1/projects").mock(
            return_value=Response(200, json=mock_list_response(MOCK_PROJECTS))
        )
        
        result = await client.projects.list()
        
        assert len(result.data) == len(MOCK_PROJECTS)
        assert result.data[0].id == MOCK_PROJECTS[0]["id"]
        assert result.data[0].name == MOCK_PROJECTS[0]["name"]
    
    @respx.mock
    async def test_list_projects_with_pagination(self, client: LunaClient) -> None:
        """Should support pagination parameters."""
        respx.get(f"{BASE_URL}/v1/projects").mock(
            return_value=Response(200, json=mock_list_response(MOCK_PROJECTS[:1], has_more=True))
        )
        
        result = await client.projects.list(limit=1)
        
        assert len(result.data) == 1
        assert result.has_more is True


class TestProjectsGet:
    """Tests for projects.get()"""
    
    @respx.mock
    async def test_get_project_success(self, client: LunaClient) -> None:
        """Should return a single project by ID."""
        respx.get(f"{BASE_URL}/v1/projects/{MOCK_PROJECT['id']}").mock(
            return_value=Response(200, json=MOCK_PROJECT)
        )
        
        result = await client.projects.get(MOCK_PROJECT["id"])
        
        assert result.id == MOCK_PROJECT["id"]
        assert result.name == MOCK_PROJECT["name"]
        assert result.description == MOCK_PROJECT["description"]
    
    @respx.mock
    async def test_get_project_not_found(self, client: LunaClient) -> None:
        """Should raise NotFoundError for non-existent project."""
        respx.get(f"{BASE_URL}/v1/projects/prj_nonexistent").mock(
            return_value=Response(404, json=MOCK_ERROR_NOT_FOUND)
        )
        
        with pytest.raises(NotFoundError):
            await client.projects.get("prj_nonexistent")


class TestProjectsCreate:
    """Tests for projects.create()"""
    
    @respx.mock
    async def test_create_project_success(self, client: LunaClient) -> None:
        """Should create a new project."""
        new_project = {**MOCK_PROJECT, "id": "prj_new123"}
        respx.post(f"{BASE_URL}/v1/projects").mock(
            return_value=Response(201, json=new_project)
        )
        
        result = await client.projects.create(ProjectCreate(
            name=MOCK_PROJECT_CREATE["name"],
            description=MOCK_PROJECT_CREATE["description"],
        ))
        
        assert result.name == MOCK_PROJECT["name"]
        assert result.id.startswith("prj_")
    
    @respx.mock
    async def test_create_project_minimal(self, client: LunaClient) -> None:
        """Should create project with only required fields."""
        new_project = {**MOCK_PROJECT, "id": "prj_min123", "description": None}
        respx.post(f"{BASE_URL}/v1/projects").mock(
            return_value=Response(201, json=new_project)
        )
        
        result = await client.projects.create(ProjectCreate(name="Minimal Project"))
        
        assert result.name == MOCK_PROJECT["name"]


class TestProjectsDelete:
    """Tests for projects.delete()"""
    
    @respx.mock
    async def test_delete_project_success(self, client: LunaClient) -> None:
        """Should delete an existing project."""
        respx.delete(f"{BASE_URL}/v1/projects/{MOCK_PROJECT['id']}").mock(
            return_value=Response(204)
        )
        
        # Should not raise
        await client.projects.delete(MOCK_PROJECT["id"])
    
    @respx.mock
    async def test_delete_project_not_found(self, client: LunaClient) -> None:
        """Should raise NotFoundError for non-existent project."""
        respx.delete(f"{BASE_URL}/v1/projects/prj_nonexistent").mock(
            return_value=Response(404, json=MOCK_ERROR_NOT_FOUND)
        )
        
        with pytest.raises(NotFoundError):
            await client.projects.delete("prj_nonexistent")
