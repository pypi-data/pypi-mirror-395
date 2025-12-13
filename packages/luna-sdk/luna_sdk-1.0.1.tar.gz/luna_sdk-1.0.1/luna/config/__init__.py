"""Configuration loader for Luna SDK."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Literal

LogLevel = Literal["error", "warn", "info", "debug", "trace"]


@dataclass
class Config:
    """Luna SDK configuration."""
    
    api_key: str | None = None
    access_token: str | None = None
    refresh_token: str | None = None
    base_url: str = "https://api.eclipse.dev"
    timeout: float = 30.0
    max_retries: int = 3
    log_level: LogLevel = "info"


# Environment variable names
ENV_VARS = {
    "api_key": "LUNA_API_KEY",
    "access_token": "LUNA_ACCESS_TOKEN",
    "refresh_token": "LUNA_REFRESH_TOKEN",
    "base_url": "LUNA_BASE_URL",
    "timeout": "LUNA_TIMEOUT",
    "max_retries": "LUNA_MAX_RETRIES",
    "log_level": "LUNA_LOG_LEVEL",
}

# Default configuration
DEFAULTS = Config()


def load_from_env() -> Config:
    """Load configuration from environment variables."""
    config = Config()
    
    # Auth
    if api_key := os.environ.get(ENV_VARS["api_key"]):
        config.api_key = api_key
    
    if access_token := os.environ.get(ENV_VARS["access_token"]):
        config.access_token = access_token
    
    if refresh_token := os.environ.get(ENV_VARS["refresh_token"]):
        config.refresh_token = refresh_token
    
    # Base URL
    if base_url := os.environ.get(ENV_VARS["base_url"]):
        config.base_url = base_url
    
    # Timeout
    if timeout_str := os.environ.get(ENV_VARS["timeout"]):
        try:
            config.timeout = float(timeout_str)
        except ValueError:
            pass
    
    # Max retries
    if max_retries_str := os.environ.get(ENV_VARS["max_retries"]):
        try:
            config.max_retries = int(max_retries_str)
        except ValueError:
            pass
    
    # Log level
    if log_level := os.environ.get(ENV_VARS["log_level"]):
        if log_level in ("error", "warn", "info", "debug", "trace"):
            config.log_level = log_level  # type: ignore
    
    return config


def merge_config(user_config: dict) -> Config:
    """Merge user config with environment and defaults."""
    env_config = load_from_env()
    
    return Config(
        api_key=user_config.get("api_key") or env_config.api_key,
        access_token=user_config.get("access_token") or env_config.access_token,
        refresh_token=user_config.get("refresh_token") or env_config.refresh_token,
        base_url=user_config.get("base_url") or env_config.base_url or DEFAULTS.base_url,
        timeout=user_config.get("timeout") or env_config.timeout or DEFAULTS.timeout,
        max_retries=user_config.get("max_retries") if user_config.get("max_retries") is not None else (env_config.max_retries if env_config.max_retries is not None else DEFAULTS.max_retries),
        log_level=user_config.get("log_level") or env_config.log_level or DEFAULTS.log_level,
    )


def validate_config(config: Config) -> None:
    """Validate configuration."""
    if not config.api_key and not config.access_token:
        raise ValueError("Either api_key or access_token must be provided")
    
    if config.timeout <= 0:
        raise ValueError("timeout must be positive")
    
    if config.max_retries < 0:
        raise ValueError("max_retries must be non-negative")
    
    if config.base_url:
        from urllib.parse import urlparse
        parsed = urlparse(config.base_url)
        if not parsed.scheme or not parsed.netloc:
            raise ValueError("base_url must be a valid URL")
