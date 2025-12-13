"""Async paginator implementation."""

from __future__ import annotations

from typing import TypeVar, AsyncIterator, Callable, Awaitable
from luna.types import ListResponse

T = TypeVar("T")

class Paginator(AsyncIterator[T]):
    """
    Async iterator for auto-pagination.
    
    Yields individual items from pages, fetching new pages as needed.
    """
    
    def __init__(
        self,
        fetch_next: Callable[[str | None], Awaitable[ListResponse]],
    ) -> None:
        self._fetch_next = fetch_next
        self._buffer: list[T] = []
        self._next_cursor: str | None = None
        self._has_more = True
        self._initialized = False

    def __aiter__(self) -> AsyncIterator[T]:
        return self

    async def __anext__(self) -> T:
        if self._buffer:
            return self._buffer.pop(0)

        if self._initialized and not self._has_more:
            raise StopAsyncIteration

        # Fetch next page
        page = await self._fetch_next(self._next_cursor)
        self._initialized = True
        self._buffer = list(page.data) # type: ignore
        self._has_more = page.has_more
        self._next_cursor = page.next_cursor

        if not self._buffer:
            raise StopAsyncIteration
            
        return self._buffer.pop(0)
