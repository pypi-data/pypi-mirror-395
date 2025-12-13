"""Base error classes for Luna SDK."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from luna.errors.codes import ErrorCode, RETRYABLE_CODES


@dataclass
class LunaError(Exception):
    """Base error class for all Luna SDK errors."""

    code: str
    message: str
    request_id: str
    status: int
    details: dict[str, Any] | None = None

    def __post_init__(self) -> None:
        super().__init__(self.message)

    @property
    def docs_url(self) -> str:
        """URL to documentation for this error."""
        return f"https://docs.eclipse.dev/luna/errors#{self.code}"

    @property
    def retryable(self) -> bool:
        """Check if this error is retryable."""
        try:
            return ErrorCode(self.code) in RETRYABLE_CODES
        except ValueError:
            return False

    def to_dict(self) -> dict[str, Any]:
        """Convert error to dictionary."""
        return {
            "code": self.code,
            "message": self.message,
            "status": self.status,
            "request_id": self.request_id,
            "details": self.details,
            "docs_url": self.docs_url,
        }


@dataclass
class AuthenticationError(LunaError):
    """Authentication failed (invalid API key, expired token)."""

    status: int = field(default=401)


@dataclass
class AuthorizationError(LunaError):
    """Authorization failed (insufficient permissions)."""

    status: int = field(default=403)


@dataclass
class ValidationError(LunaError):
    """Validation failed for request parameters."""

    status: int = field(default=400)


@dataclass
class RateLimitError(LunaError):
    """Rate limit exceeded."""

    status: int = field(default=429)
    retry_after: int | None = None


@dataclass
class NetworkError(LunaError):
    """Network-related errors (timeout, connection)."""

    status: int = field(default=0)


@dataclass
class NotFoundError(LunaError):
    """Resource not found."""

    status: int = field(default=404)


@dataclass
class ConflictError(LunaError):
    """Resource conflict (e.g., duplicate creation)."""

    status: int = field(default=409)


@dataclass
class ServerError(LunaError):
    """Server-side errors."""

    status: int = field(default=500)


def create_error(
    status: int,
    body: dict[str, Any],
    request_id: str,
    retry_after: int | None = None,
) -> LunaError:
    """Create appropriate error class from API response."""
    code = body.get("code", "LUNA_ERR_UNKNOWN")
    message = body.get("message", "An unknown error occurred")
    details = body.get("details")

    base_params = {
        "code": code,
        "message": message,
        "request_id": request_id,
        "details": details,
    }

    if status == 400:
        return ValidationError(**base_params)
    elif status == 401:
        return AuthenticationError(**base_params)
    elif status == 403:
        return AuthorizationError(**base_params)
    elif status == 404:
        return NotFoundError(**base_params)
    elif status == 409:
        return ConflictError(**base_params)
    elif status == 429:
        return RateLimitError(**base_params, retry_after=retry_after)
    elif status >= 500:
        return ServerError(**base_params, status=status)
    else:
        return LunaError(**base_params, status=status)
