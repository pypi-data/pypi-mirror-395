"""Custom exceptions for database operations."""

from __future__ import annotations

from typing import Any


class DatabaseError(Exception):
    """Base exception for database operations."""

    def __init__(self, message: str, details: dict[str, Any] | None = None) -> None:
        super().__init__(message)
        self.details = details or {}


class InfluxDBConnectionError(DatabaseError):
    """Raised when unable to connect to InfluxDB."""

    pass


class WriteError(DatabaseError):
    """Raised when unable to write data to InfluxDB."""

    pass


class ValidationError(DatabaseError):
    """Raised when data validation fails."""

    pass


class ConfigurationError(DatabaseError):
    """Raised when configuration is invalid."""

    pass
