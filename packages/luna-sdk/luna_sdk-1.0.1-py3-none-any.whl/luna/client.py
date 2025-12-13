"""Luna SDK Client."""

from __future__ import annotations

from typing import Callable, Awaitable

from luna.auth import ApiKeyAuth, TokenAuth, AuthProvider
from luna.http import HttpClient
from luna.resources import UsersResource, ProjectsResource
from luna.resources.resmate import ResMateResource
from luna.resources.identity import IdentityResource
from luna.resources.storage import StorageResource
from luna.resources.ai import AiResource
from luna.resources.automation import AutomationResource
from luna.telemetry import Logger, ConsoleLogger, LogLevel


class ClientConfig:
    """Configuration for the Luna client."""

    def __init__(
        self,
        api_key: str | None = None,
        access_token: str | None = None,
        refresh_token: str | None = None,
        on_token_refresh: Callable[[dict], Awaitable[None]] | None = None,
        base_url: str = "https://api.eclipse.dev",
        timeout: float = 30.0,
        max_retries: int = 3,
        logger: Logger | None = None,
        log_level: LogLevel = "info",
    ) -> None:
        self.api_key = api_key
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.on_token_refresh = on_token_refresh
        self.base_url = base_url
        self.timeout = timeout
        self.max_retries = max_retries
        self.logger = logger
        self.log_level = log_level


class LunaClient:
    """
    Luna SDK Client.

    Example:
        # API Key authentication
        client = LunaClient(api_key=os.environ["LUNA_API_KEY"])

        # Token authentication
        client = LunaClient(
            access_token=session.access_token,
            refresh_token=session.refresh_token,
            on_token_refresh=save_tokens,
        )

        # Usage
        users = await client.users.list()
        user = await client.users.get("usr_123")
    """

    def __init__(
        self,
        api_key: str | None = None,
        access_token: str | None = None,
        refresh_token: str | None = None,
        on_token_refresh: Callable[[dict], Awaitable[None]] | None = None,
        base_url: str = "https://api.eclipse.dev",
        timeout: float = 30.0,
        max_retries: int = 3,
        logger: Logger | None = None,
        log_level: LogLevel = "info",
    ) -> None:
        """
        Initialize the Luna client.

        Args:
            api_key: API key for authentication (format: lk_<env>_<key>)
            access_token: Access token for OAuth authentication
            refresh_token: Refresh token for automatic token refresh
            on_token_refresh: Callback when tokens are refreshed
            base_url: Base URL for the API
            timeout: Request timeout in seconds
            max_retries: Maximum number of retry attempts
            logger: Custom logger instance
            log_level: Log level
        """
        if not api_key and not access_token:
            raise ValueError("Either api_key or access_token must be provided")

        # Set up logger
        self._logger = logger or ConsoleLogger(log_level)

        # Set up auth provider
        auth_provider: AuthProvider
        if api_key:
            auth_provider = ApiKeyAuth(api_key)
        else:
            assert access_token is not None
            auth_provider = TokenAuth(
                access_token=access_token,
                refresh_token=refresh_token,
                on_refresh=on_token_refresh,
            )

        # Set up HTTP client
        self._http_client = HttpClient(
            base_url=base_url.rstrip("/"),
            timeout=timeout,
            max_retries=max_retries,
            auth_provider=auth_provider,
            logger=self._logger,
        )

        # Initialize resources
        self.users = UsersResource(self._http_client)
        self.projects = ProjectsResource(self._http_client)
        self.res_mate = ResMateResource(self._http_client)
        self.identity = IdentityResource(self._http_client)
        self.storage = StorageResource(self._http_client)
        self.ai = AiResource(self._http_client)
        self.automation = AutomationResource(self._http_client)

        self._logger.debug(
            "LunaClient initialized",
            {"base_url": base_url, "auth_type": "api_key" if api_key else "token"},
        )

    @property
    def version(self) -> str:
        """Get SDK version."""
        return "1.0.0"

    async def close(self) -> None:
        """Close the HTTP client connection."""
        await self._http_client.close()

    async def __aenter__(self) -> "LunaClient":
        """Async context manager entry."""
        return self

    async def __aexit__(self, *args: object) -> None:
        """Async context manager exit."""
        await self.close()
