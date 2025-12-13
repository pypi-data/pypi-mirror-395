"""Projects resource."""

from __future__ import annotations

import re
from typing import TYPE_CHECKING

from luna.types import Project, ProjectCreate, ProjectUpdate, ProjectList

if TYPE_CHECKING:
    from luna.http import HttpClient


class ProjectsResource:
    """
    Projects resource for managing projects.

    Example:
        # List projects
        projects = await client.projects.list(limit=10)

        # Get a project
        project = await client.projects.get("prj_123")

        # Create a project
        new_project = await client.projects.create(
            ProjectCreate(name="My Project", description="A new project")
        )

        # Update a project
        updated = await client.projects.update("prj_123", ProjectUpdate(name="Updated"))

        # Delete a project
        await client.projects.delete("prj_123")
    """

    _PROJECT_ID_PATTERN = re.compile(r"^prj_[a-zA-Z0-9]+$")
    _BASE_PATH = "/v1/projects"

    def __init__(self, http_client: "HttpClient") -> None:
        self._http_client = http_client

    async def list(
        self,
        limit: int | None = None,
        cursor: str | None = None,
    ) -> ProjectList:
        """List all projects with pagination."""
        from luna.http.types import RequestConfig

        response = await self._http_client.request(
            RequestConfig(
                method="GET",
                path=self._BASE_PATH,
                query={
                    "limit": str(limit) if limit else None,
                    "cursor": cursor,
                },
            )
        )
        return ProjectList.model_validate(response.data)

    async def get(self, project_id: str) -> Project:
        """Get a project by ID."""
        from luna.http.types import RequestConfig

        self._validate_project_id(project_id)

        response = await self._http_client.request(
            RequestConfig(
                method="GET",
                path=f"{self._BASE_PATH}/{project_id}",
            )
        )
        return Project.model_validate(response.data)

    async def create(self, data: ProjectCreate) -> Project:
        """Create a new project."""
        from luna.http.types import RequestConfig

        response = await self._http_client.request(
            RequestConfig(
                method="POST",
                path=self._BASE_PATH,
                body=data.model_dump(exclude_none=True),
            )
        )
        return Project.model_validate(response.data)

    async def update(self, project_id: str, data: ProjectUpdate) -> Project:
        """Update an existing project."""
        from luna.http.types import RequestConfig

        self._validate_project_id(project_id)

        response = await self._http_client.request(
            RequestConfig(
                method="PATCH",
                path=f"{self._BASE_PATH}/{project_id}",
                body=data.model_dump(exclude_none=True),
            )
        )
        return Project.model_validate(response.data)

    async def delete(self, project_id: str) -> None:
        """Delete a project."""
        from luna.http.types import RequestConfig

        self._validate_project_id(project_id)

        await self._http_client.request(
            RequestConfig(
                method="DELETE",
                path=f"{self._BASE_PATH}/{project_id}",
            )
        )

    def _validate_project_id(self, project_id: str) -> None:
        """Validate project ID format."""
        if not project_id:
            raise ValueError("Project ID is required")
        if not self._PROJECT_ID_PATTERN.match(project_id):
            raise ValueError("Invalid project ID format. Expected: prj_<id>")
