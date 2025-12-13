"""API Key authentication provider."""

from __future__ import annotations

import re

from luna.auth.types import AuthProvider
from luna.errors.base import AuthenticationError
from luna.errors.codes import ErrorCode


class ApiKeyAuth(AuthProvider):
    """
    API Key authentication provider.

    Example:
        auth = ApiKeyAuth("lk_live_xxxx")
        headers = await auth.get_headers()
        # {"X-Luna-Api-Key": "lk_live_xxxx"}
    """

    _API_KEY_PATTERN = re.compile(r"^lk_(live|test|dev)_[a-zA-Z0-9]{32}$")

    def __init__(self, api_key: str) -> None:
        """
        Initialize API key authentication.

        Args:
            api_key: API key in format lk_<env>_<32 chars>

        Raises:
            ValueError: If API key is invalid
        """
        if not api_key:
            raise AuthenticationError(
                code=ErrorCode.AUTH_INVALID_KEY,
                message="API key is required",
                request_id="local",
            )
        if not self._is_valid_api_key(api_key):
            raise AuthenticationError(
                code=ErrorCode.AUTH_INVALID_KEY,
                message="Invalid API key format. Expected: lk_<env>_<key>",
                request_id="local",
            )
        self._api_key = api_key

    async def get_headers(self) -> dict[str, str]:
        """Get authorization headers with API key."""
        return {"X-Luna-Api-Key": self._api_key}

    def needs_refresh(self) -> bool:
        """API keys don't expire."""
        return False

    def _is_valid_api_key(self, key: str) -> bool:
        """Validate API key format."""
        return bool(self._API_KEY_PATTERN.match(key))
