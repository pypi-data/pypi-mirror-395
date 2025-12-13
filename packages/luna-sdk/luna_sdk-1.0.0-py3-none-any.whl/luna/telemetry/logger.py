"""Console logger implementation."""

from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timezone
from typing import Any

from luna.telemetry.types import LogLevel, LogContext, LOG_LEVEL_PRIORITY

# Patterns for sensitive data that should be redacted
REDACT_PATTERNS = [
    re.compile(r"api[_-]?key", re.IGNORECASE),
    re.compile(r"authorization", re.IGNORECASE),
    re.compile(r"x-luna-api-key", re.IGNORECASE),
    re.compile(r"password", re.IGNORECASE),
    re.compile(r"secret", re.IGNORECASE),
    re.compile(r"token", re.IGNORECASE),
    re.compile(r"bearer", re.IGNORECASE),
]


class ConsoleLogger:
    """Console-based logger with redaction support."""

    def __init__(self, level: LogLevel = "info") -> None:
        self._level = level
        self._level_priority = LOG_LEVEL_PRIORITY[level]

    def error(self, message: str, context: LogContext | None = None) -> None:
        self._log("error", message, context)

    def warn(self, message: str, context: LogContext | None = None) -> None:
        self._log("warn", message, context)

    def info(self, message: str, context: LogContext | None = None) -> None:
        self._log("info", message, context)

    def debug(self, message: str, context: LogContext | None = None) -> None:
        self._log("debug", message, context)

    def trace(self, message: str, context: LogContext | None = None) -> None:
        self._log("trace", message, context)

    def _log(
        self, level: LogLevel, message: str, context: LogContext | None
    ) -> None:
        if LOG_LEVEL_PRIORITY[level] < self._level_priority:
            return

        timestamp = datetime.now(timezone.utc).isoformat()
        sanitized_context = self._sanitize(context) if context else None

        log_entry: dict[str, Any] = {
            "timestamp": timestamp,
            "level": level.upper(),
            "message": message,
            "sdk": "luna-sdk",
            "version": "1.0.0",
            "language": "python",
        }

        if sanitized_context:
            log_entry["context"] = sanitized_context

        output = json.dumps(log_entry)

        if level == "error":
            print(output, file=sys.stderr)
        else:
            print(output)

    def _sanitize(self, obj: LogContext) -> LogContext:
        """Sanitize context by redacting sensitive values."""
        result: LogContext = {}

        for key, value in obj.items():
            if self._is_sensitive_key(key):
                result[key] = "[REDACTED]"
            elif isinstance(value, dict):
                result[key] = self._sanitize(value)
            else:
                result[key] = value

        return result

    def _is_sensitive_key(self, key: str) -> bool:
        """Check if a key contains sensitive data."""
        return any(pattern.search(key) for pattern in REDACT_PATTERNS)
