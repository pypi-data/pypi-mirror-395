from __future__ import annotations

from luna.http import HttpClient
from luna.types import Group, GroupCreate, GroupList


class GroupsResource:
    """Manages group resources."""

    def __init__(self, client: HttpClient) -> None:
        self._client = client
        self._base_path = "/v1/identity/groups"

    async def list(self) -> GroupList:
        """List all groups."""
        resp = await self._client.request(
            method="GET",
            path=self._base_path,
        )
        return GroupList.model_validate(resp.data)

    async def get(self, id: str) -> Group:
        """Get group by ID."""
        resp = await self._client.request(
            method="GET",
            path=f"{self._base_path}/{id}",
        )
        return Group.model_validate(resp.data)

    async def create(self, params: GroupCreate) -> Group:
        """Create a new group."""
        resp = await self._client.request(
            method="POST",
            path=self._base_path,
            body=params.model_dump(exclude_none=True),
        )
        return Group.model_validate(resp.data)


class IdentityResource:
    """Identity Service resources."""

    def __init__(self, client: HttpClient) -> None:
        self.groups = GroupsResource(client)
