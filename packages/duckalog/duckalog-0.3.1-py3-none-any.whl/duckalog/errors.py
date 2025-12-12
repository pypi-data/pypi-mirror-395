"""Unified exception hierarchy for Duckalog.

This module provides a consistent exception hierarchy for all Duckalog errors,
ensuring that all library exceptions derive from a common base class and can be
caught uniformly by users.
"""

from __future__ import annotations


class DuckalogError(Exception):
    """Base exception for all Duckalog errors.

    This is the root of the exception hierarchy. All Duckalog-specific exceptions
    should inherit from this class to provide a unified error handling interface
    for users of the library.

    Users can catch this class to handle any Duckalog-specific error, or catch
    more specific subclasses for targeted error handling.
    """

    def __init__(self, message: str, cause: Exception | None = None):
        """Initialize DuckalogError with optional cause chaining.

        Args:
            message: Human-readable error message.
            cause: Optional underlying exception that caused this error.
        """
        super().__init__(message)
        self.cause = cause

    def __str__(self) -> str:
        """Return the error message."""
        return super().__str__()


class ConfigError(DuckalogError):
    """Configuration-related errors.

    This exception is raised when a catalog configuration cannot be read,
    parsed, interpolated, or validated according to the Duckalog schema.

    Typical error conditions include:

    * The config file does not exist or cannot be read.
    * The file is not valid YAML/JSON.
    * Required fields are missing or invalid.
    * An environment variable placeholder cannot be resolved.
    """

    def __init__(self, message: str, cause: Exception | None = None):
        super().__init__(message, cause)


class PathResolutionError(ConfigError):
    """Raised when path resolution fails due to security or access issues.

    This exception is a subclass of ConfigError since path resolution issues
    are typically configuration-related problems.
    """

    def __init__(
        self,
        message: str,
        original_path: str | None = None,
        resolved_path: str | None = None,
        cause: Exception | None = None,
    ):
        super().__init__(message, cause)
        self.original_path = original_path
        self.resolved_path = resolved_path


class RemoteConfigError(ConfigError):
    """Error raised when remote configuration loading fails.

    This exception wraps lower-level errors from remote storage systems
    when attempting to load configuration files from locations like S3,
    GCS, Azure Blob Storage, or HTTP endpoints.
    """

    def __init__(self, message: str, cause: Exception | None = None):
        super().__init__(message, cause)


class SQLFileError(ConfigError):
    """Base exception for SQL file-related errors.

    This exception is raised when SQL file operations fail, such as when
    a referenced SQL file cannot be found, read, or processed.
    """

    def __init__(self, message: str, cause: Exception | None = None):
        super().__init__(message, cause)


class SQLFileNotFoundError(SQLFileError):
    """Raised when a referenced SQL file does not exist."""

    pass


class SQLFilePermissionError(SQLFileError):
    """Raised when a SQL file cannot be read due to permissions."""

    pass


class SQLFileEncodingError(SQLFileError):
    """Raised when a SQL file has invalid encoding."""

    pass


class SQLFileSizeError(SQLFileError):
    """Raised when a SQL file exceeds size limits."""

    pass


class SQLTemplateError(SQLFileError):
    """Raised when template processing fails."""

    pass


class EngineError(DuckalogError):
    """Engine-level error raised during catalog builds.

    This exception wraps lower-level DuckDB errors, such as failures to
    connect to the database, attach external systems, or execute generated
    SQL statements.
    """

    def __init__(self, message: str, cause: Exception | None = None):
        super().__init__(message, cause)


__all__ = [
    "DuckalogError",
    "ConfigError", 
    "PathResolutionError",
    "RemoteConfigError",
    "SQLFileError",
    "SQLFileNotFoundError",
    "SQLFilePermissionError",
    "SQLFileEncodingError", 
    "SQLFileSizeError",
    "SQLTemplateError",
    "EngineError",
]
