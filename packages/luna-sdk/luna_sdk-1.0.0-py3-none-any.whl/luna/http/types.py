"""HTTP type definitions."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal


@dataclass
class RequestConfig:
    """HTTP request configuration."""

    method: Literal["GET", "POST", "PUT", "PATCH", "DELETE"]
    path: str
    headers: dict[str, str] | None = None
    query: dict[str, str | list[str] | None] | None = None
    body: Any | None = None
    files: dict[str, Any] | None = None
    content_type: str | None = None
    timeout: float | None = None


@dataclass
class Response[T]:
    """HTTP response wrapper."""

    data: T
    status: int
    headers: dict[str, str]
    request_id: str


@dataclass
class RetryConfig:
    """Retry configuration."""

    max_retries: int = 3
    initial_delay_ms: int = 500
    max_delay_ms: int = 30_000
    backoff_multiplier: float = 2.0
    retryable_statuses: list[int] = field(
        default_factory=lambda: [408, 429, 500, 502, 503, 504]
    )
