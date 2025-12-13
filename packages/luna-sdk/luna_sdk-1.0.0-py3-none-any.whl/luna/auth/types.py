"""Authentication type definitions."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import Awaitable, Callable


@dataclass
class TokenPair:
    """Token pair returned from authentication."""

    access_token: str
    refresh_token: str
    expires_at: datetime | None = None


TokenRefreshCallback = Callable[[TokenPair], Awaitable[None]]


class AuthProvider(ABC):
    """Interface for authentication providers."""

    @abstractmethod
    async def get_headers(self) -> dict[str, str]:
        """Get authorization headers for a request."""
        ...

    @abstractmethod
    def needs_refresh(self) -> bool:
        """Check if credentials need refresh."""
        ...

    async def refresh(self) -> None:
        """Refresh credentials if needed."""
        pass
