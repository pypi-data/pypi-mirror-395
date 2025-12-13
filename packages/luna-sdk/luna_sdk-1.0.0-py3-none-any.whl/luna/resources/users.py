"""Users resource."""

from __future__ import annotations

import re
from typing import TYPE_CHECKING

from luna.types import User, UserCreate, UserUpdate, UserList, PaginationParams
from luna.resources.pagination import Paginator

if TYPE_CHECKING:
    from luna.http import HttpClient


class UsersResource:
    """
    Users resource for managing user accounts.

    Example:
        # List users
        users = await client.users.list(limit=10)

        # Get a user
        user = await client.users.get("usr_123")

        # Create a user
        new_user = await client.users.create(
            UserCreate(email="john@example.com", name="John Doe")
        )

        # Update a user
        updated = await client.users.update("usr_123", UserUpdate(name="Jane Doe"))

        # Delete a user
        await client.users.delete("usr_123")
    """

    _USER_ID_PATTERN = re.compile(r"^usr_[a-zA-Z0-9]+$")
    _BASE_PATH = "/v1/users"

    def __init__(self, http_client: "HttpClient") -> None:
        self._http_client = http_client

    async def list(
        self,
        limit: int | None = None,
        cursor: str | None = None,
    ) -> UserList:
        """List all users with pagination."""
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
        return UserList.model_validate(response.data)

    def iterate(self, limit: int | None = None) -> Paginator[User]:
        """Iterate over all users automatically handling pagination."""
        from luna.resources.pagination import Paginator
        
        async def fetch_next(cursor: str | None) -> UserList:
            return await self.list(limit=limit, cursor=cursor)
            
        return Paginator(fetch_next)

    async def get(self, user_id: str) -> User:
        """Get a user by ID."""
        from luna.http.types import RequestConfig

        self._validate_user_id(user_id)

        response = await self._http_client.request(
            RequestConfig(
                method="GET",
                path=f"{self._BASE_PATH}/{user_id}",
            )
        )
        return User.model_validate(response.data)

    async def create(self, data: UserCreate) -> User:
        """Create a new user."""
        from luna.http.types import RequestConfig

        response = await self._http_client.request(
            RequestConfig(
                method="POST",
                path=self._BASE_PATH,
                body=data.model_dump(exclude_none=True),
            )
        )
        return User.model_validate(response.data)

    async def update(self, user_id: str, data: UserUpdate) -> User:
        """Update an existing user."""
        from luna.http.types import RequestConfig

        self._validate_user_id(user_id)

        response = await self._http_client.request(
            RequestConfig(
                method="PATCH",
                path=f"{self._BASE_PATH}/{user_id}",
                body=data.model_dump(exclude_none=True),
            )
        )
        return User.model_validate(response.data)

    async def delete(self, user_id: str) -> None:
        """Delete a user."""
        from luna.http.types import RequestConfig

        self._validate_user_id(user_id)

        await self._http_client.request(
            RequestConfig(
                method="DELETE",
                path=f"{self._BASE_PATH}/{user_id}",
            )
        )

    def _validate_user_id(self, user_id: str) -> None:
        """Validate user ID format."""
        if not user_id:
            raise ValueError("User ID is required")
        if not self._USER_ID_PATTERN.match(user_id):
            raise ValueError("Invalid user ID format. Expected: usr_<id>")
