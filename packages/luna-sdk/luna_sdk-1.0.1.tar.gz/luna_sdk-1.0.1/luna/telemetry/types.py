"""Telemetry type definitions."""

from __future__ import annotations

from typing import Any, Literal, Protocol

LogLevel = Literal["error", "warn", "info", "debug", "trace"]
LogContext = dict[str, Any]

LOG_LEVEL_PRIORITY: dict[LogLevel, int] = {
    "error": 50,
    "warn": 40,
    "info": 30,
    "debug": 20,
    "trace": 10,
}


class Logger(Protocol):
    """Logger interface for SDK operations."""

    def error(self, message: str, context: LogContext | None = None) -> None: ...
    def warn(self, message: str, context: LogContext | None = None) -> None: ...
    def info(self, message: str, context: LogContext | None = None) -> None: ...
    def debug(self, message: str, context: LogContext | None = None) -> None: ...
    def trace(self, message: str, context: LogContext | None = None) -> None: ...
