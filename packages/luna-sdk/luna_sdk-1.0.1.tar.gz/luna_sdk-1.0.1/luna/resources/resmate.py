from __future__ import annotations

from typing import cast

from luna.http import HttpClient
from luna.types import (
    Residence,
    ResidenceSearch,
    ResidenceList,
    CampusList,
)
from luna.resources.pagination import Paginator


class ResidencesResource:
    """Manages residence resources."""

    def __init__(self, client: HttpClient) -> None:
        self._client = client
        self._base_path = "/v1/resmate/residences"

    async def list(
        self,
        params: ResidenceSearch | None = None,
        # Allow passing individual parameters for convenience
        query: str | None = None,
        nsfas: bool | None = None,
        min_price: float | None = None,
        max_price: float | None = None,
        gender: str | None = None,
        campus_id: str | None = None,
        radius: float | None = None,
        min_rating: float | None = None,
        limit: int | None = None,
        cursor: str | None = None,
    ) -> ResidenceList:
        """List and search residences."""
        if params is None:
            params = ResidenceSearch(
                limit=limit,
                cursor=cursor,
                query=query,
                nsfas=nsfas,
                min_price=min_price,
                max_price=max_price,
                gender=gender,
                campus_id=campus_id,
                radius=radius,
                min_rating=min_rating,
            )

        # Convert params to dict and filter None values
        # Pydantic's model_dump(exclude_none=True) is useful here
        query_params = {
            k: v
            for k, v in params.model_dump(exclude_none=True).items()
            if v is not None
        }

        resp = await self._client.request(
            method="GET",
            path=self._base_path,
            query=query_params,
        )
        return ResidenceList.model_validate(resp.data)

    async def get(self, id: str) -> Residence:
        """Get residence by ID."""
        resp = await self._client.request(
            method="GET",
            path=f"{self._base_path}/{id}",
        )
        return Residence.model_validate(resp.data)

    def iterate(self, params: ResidenceSearch | None = None) -> Paginator[Residence]:
        """Iterate over residences."""
        
        async def fetch_next(cursor: str | None) -> ResidenceList:
            if params:
                # Create a copy with updating cursor
                p = params.model_copy(update={"cursor": cursor})
                return await self.list(params=p)
            return await self.list(cursor=cursor)

        return Paginator(fetch_next)


class CampusesResource:
    """Manages campus resources."""

    def __init__(self, client: HttpClient) -> None:
        self._client = client
        self._base_path = "/v1/resmate/campuses"

    async def list(self) -> CampusList:
        """List all campuses."""
        resp = await self._client.request(
            method="GET",
            path=self._base_path,
        )
        return CampusList.model_validate(resp.data)


class ResMateResource:
    """ResMate Service resources."""

    def __init__(self, client: HttpClient) -> None:
        self.residences = ResidencesResource(client)
        self.campuses = CampusesResource(client)
