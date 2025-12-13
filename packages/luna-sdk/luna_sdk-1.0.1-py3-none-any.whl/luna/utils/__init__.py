"""Utility functions for Luna SDK."""

from __future__ import annotations

import random
import string
import time
from typing import Any, TypeVar, Callable, Awaitable
from functools import wraps

T = TypeVar("T")


def generate_request_id() -> str:
    """Generate a unique request ID."""
    timestamp = hex(int(time.time() * 1000))[2:]
    random_part = "".join(random.choices(string.ascii_lowercase + string.digits, k=8))
    return f"req_{timestamp}{random_part}"


def deep_merge(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    """Deep merge two dictionaries."""
    result = base.copy()
    
    for key, value in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = deep_merge(result[key], value)
        else:
            result[key] = value
    
    return result


def omit(obj: dict[str, T], keys: list[str]) -> dict[str, T]:
    """Create a new dict with specified keys omitted."""
    return {k: v for k, v in obj.items() if k not in keys}


def pick(obj: dict[str, T], keys: list[str]) -> dict[str, T]:
    """Create a new dict with only specified keys."""
    return {k: v for k, v in obj.items() if k in keys}


def is_retryable_status(status: int) -> bool:
    """Check if an HTTP status code is retryable."""
    return status in {408, 429, 500, 502, 503, 504}


def mask_sensitive(value: str, visible_start: int = 7, visible_end: int = 4) -> str:
    """Mask a sensitive string, showing only start and end characters."""
    if len(value) <= visible_start + visible_end:
        return "*" * len(value)
    return value[:visible_start] + "****" + value[-visible_end:]


def validate_id(id_value: str, prefix: str, name: str) -> None:
    """Validate an ID has the correct format."""
    import re
    
    if not id_value:
        raise ValueError(f"{name} is required")
    
    pattern = rf"^{prefix}_[a-zA-Z0-9]+$"
    if not re.match(pattern, id_value):
        raise ValueError(f"Invalid {name} format. Expected: {prefix}_<id>")
