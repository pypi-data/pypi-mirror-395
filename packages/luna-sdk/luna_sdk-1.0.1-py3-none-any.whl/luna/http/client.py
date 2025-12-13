"""HTTP client implementation."""

from __future__ import annotations

import asyncio
import random
import time
from typing import Any, TypeVar
from urllib.parse import urlencode

import httpx

from luna.auth.types import AuthProvider
from luna.errors import LunaError, NetworkError, create_error
from luna.errors.codes import ErrorCode
from luna.http.types import RequestConfig, Response, RetryConfig
from luna.telemetry import Logger
from luna.utils.system import get_system_info

T = TypeVar("T")


class HttpClient:
    """HTTP client with authentication, retry, and telemetry."""

    def __init__(
        self,
        base_url: str,
        timeout: float,
        max_retries: int,
        auth_provider: AuthProvider,
        logger: Logger,
    ) -> None:
        self._base_url = base_url
        self._timeout = timeout
        self._auth_provider = auth_provider
        self._logger = logger
        self._retry_config = RetryConfig(max_retries=max_retries)
        self._client: httpx.AsyncClient | None = None

    async def __aenter__(self) -> "HttpClient":
        """Enter async context."""
        await self._get_client()
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: Any | None,
    ) -> None:
        """Exit async context."""
        await self.close()

    async def _get_client(self) -> httpx.AsyncClient:
        """Get or create HTTP client."""
        if self._client is None:
            self._client = httpx.AsyncClient(timeout=self._timeout)
        return self._client

    async def close(self) -> None:
        """Close the HTTP client."""
        if self._client:
            await self._client.aclose()
            self._client = None

    async def request(self, config: RequestConfig) -> Response[Any]:
        """Make an HTTP request with retry logic."""
        url = self._build_url(config.path, config.query)
        request_id = self._generate_request_id()

        last_error: LunaError | None = None
        attempt = 0

        while True:
            try:
                response = await self._execute_request(url, config, request_id)
                self._logger.info(
                    "HTTP request completed",
                    {
                        "request_id": request_id,
                        "method": config.method,
                        "status": response.status,
                    },
                )
                return response

            except LunaError as error:
                last_error = error
                status = error.status

                should_retry = (
                    attempt < self._retry_config.max_retries
                    and self._is_retryable(status, error)
                )

                if not should_retry:
                    self._logger.error(
                        "HTTP request failed",
                        {
                            "request_id": request_id,
                            "method": config.method,
                            "path": config.path,
                            "error": error.code,
                            "attempt": attempt,
                        },
                    )
                    raise

                self._logger.warn(
                    "HTTP request failed, retrying",
                    {
                        "request_id": request_id,
                        "method": config.method,
                        "path": config.path,
                        "status": status,
                        "attempt": attempt,
                    },
                )

                retry_after = getattr(error, "retry_after", None)
                await self._wait_for_retry(attempt, retry_after)
                attempt += 1

    async def _execute_request(
        self, url: str, config: RequestConfig, request_id: str
    ) -> Response[Any]:
        """Execute a single HTTP request."""
        client = await self._get_client()
        auth_headers = await self._auth_provider.get_headers()

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "X-Request-Id": request_id,
            "User-Agent": self._get_user_agent(),
            **auth_headers,
            **(config.headers or {}),
        }

        self._logger.debug(
            "Sending HTTP request",
            {"request_id": request_id, "method": config.method, "url": url},
        )

        if config.content_type:
             headers["Content-Type"] = config.content_type
        elif config.files:
             # Let httpx handle boundary
             headers.pop("Content-Type", None)

        kwargs: dict[str, Any] = {
            "method": config.method,
            "url": url,
            "headers": headers,
            "timeout": config.timeout or self._timeout,
        }

        if config.files:
            kwargs["files"] = config.files
            if config.body:
                kwargs["data"] = config.body
        elif config.body is not None:
             # Standard JSON request
             kwargs["json"] = config.body

        try:
            response = await client.request(**kwargs)

        except httpx.TimeoutException:
            raise NetworkError(
                code=ErrorCode.NETWORK_TIMEOUT,
                message="Request timeout",
                request_id=request_id,
            )
        except httpx.ConnectError:
            raise NetworkError(
                code=ErrorCode.NETWORK_CONNECTION,
                message="Connection error",
                request_id=request_id,
            )

        server_request_id = response.headers.get("x-request-id", request_id)
        response_headers = dict(response.headers)

        # Parse response
        body: dict[str, Any] | None = None
        if response.headers.get("content-type", "").startswith("application/json"):
            try:
                body = response.json()
            except Exception:
                body = None

        # Handle errors
        if not response.is_success:
            retry_after = None
            if "retry-after" in response.headers:
                try:
                    retry_after = int(response.headers["retry-after"])
                except ValueError:
                    pass

            err_body = body or {}
            if "error" in err_body and isinstance(err_body["error"], dict):
                err_body = err_body["error"]

            raise create_error(
                status=response.status_code,
                body=err_body,
                request_id=server_request_id,
                retry_after=retry_after,
            )

        return Response(
            data=body,
            status=response.status_code,
            headers=response_headers,
            request_id=server_request_id,
        )

    def _build_url(
        self, path: str, query: dict[str, str | list[str] | None] | None
    ) -> str:
        """Build full URL with query parameters."""
        if not path.startswith("/"):
            path = f"/{path}"

        url = f"{self._base_url}{path}"

        if query:
            params = []
            for key, value in query.items():
                if value is None:
                    continue
                if isinstance(value, list):
                    for v in value:
                        params.append((key, v))
                else:
                    params.append((key, value))
            if params:
                url = f"{url}?{urlencode(params)}"

        return url

    def _get_user_agent(self) -> str:
        """Get the User-Agent string."""
        info = get_system_info()
        return f"luna-sdk-python/1.0.0 ({info['os']}; {info['arch']}) {info['runtime']}/{info['runtime_version']}"

    def _generate_request_id(self) -> str:
        """Generate unique request ID."""
        timestamp = hex(int(time.time() * 1000))[2:]
        random_part = hex(random.randint(0, 0xFFFFFFFF))[2:]
        return f"req_{timestamp}{random_part}"

    def _is_retryable(self, status: int, error: LunaError) -> bool:
        """Check if request should be retried."""
        if not error.retryable:
            return False
        return status in self._retry_config.retryable_statuses

    async def _wait_for_retry(self, attempt: int, retry_after: int | None) -> None:
        """Wait before retry with exponential backoff."""
        if retry_after:
            delay_ms = retry_after * 1000
        else:
            delay_ms = min(
                self._retry_config.initial_delay_ms
                * (self._retry_config.backoff_multiplier ** attempt),
                self._retry_config.max_delay_ms,
            )
            # Add jitter
            jitter = delay_ms * 0.1 * (random.random() * 2 - 1)
            delay_ms = delay_ms + jitter

        await asyncio.sleep(delay_ms / 1000)
