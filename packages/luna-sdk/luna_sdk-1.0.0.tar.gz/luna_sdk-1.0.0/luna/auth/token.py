from __future__ import annotations
import asyncio
from datetime import datetime, timedelta
from typing import Awaitable, Callable
import httpx
from luna.auth.types import AuthProvider, TokenPair
from luna.errors.base import AuthenticationError
from luna.errors.codes import ErrorCode

class TokenAuth(AuthProvider):
    def __init__(
        self,
        access_token: str,
        refresh_token: str | None = None,
        expires_at: datetime | None = None,
        on_refresh: Callable[[TokenPair], Awaitable[None]] | None = None,
    ) -> None:
        if not access_token:
            raise AuthenticationError(
                code=ErrorCode.AUTH_INVALID_KEY,
                message="Access token is required",
                request_id="local",
            )
        self._access_token = access_token
        self._refresh_token = refresh_token
        self._expires_at = expires_at
        self._on_refresh = on_refresh
        self._refresh_lock = asyncio.Lock()

    async def get_headers(self) -> dict[str, str]:
        if self.needs_refresh():
            await self.refresh()
        return {"Authorization": f"Bearer {self._access_token}"}

    def needs_refresh(self) -> bool:
        if self._expires_at is None: return False
        return datetime.now() + timedelta(minutes=5) >= self._expires_at

    async def refresh(self) -> None:
        async with self._refresh_lock:
            if not self.needs_refresh(): return
            if not self._refresh_token:
                raise AuthenticationError(
                    code=ErrorCode.AUTH_INVALID_KEY,
                    message="No refresh token available",
                    request_id="local"
                )

            async with httpx.AsyncClient() as client:
                resp = await client.post(
                    "https://api.eclipse.dev/v1/auth/refresh",
                    json={"refresh_token": self._refresh_token},
                )
                if not resp.is_success:
                    raise AuthenticationError(
                        code=ErrorCode.AUTH_TOKEN_EXPIRED,
                        message=f"Refresh failed: {resp.status_code}",
                        request_id=resp.headers.get("x-request-id", "unknown")
                    )
                data = resp.json()

            self._access_token = data["access_token"]
            self._refresh_token = data["refresh_token"]
            self._expires_at = datetime.now() + timedelta(seconds=data["expires_in"])

            if self._on_refresh:
                await self._on_refresh(TokenPair(
                    access_token=self._access_token,
                    refresh_token=self._refresh_token,
                    expires_at=self._expires_at
                ))

    def update_tokens(self, tokens: TokenPair) -> None:
        """Update tokens manually."""
        self._access_token = tokens.access_token
        self._refresh_token = tokens.refresh_token
        self._expires_at = tokens.expires_at
