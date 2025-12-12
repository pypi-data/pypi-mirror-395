"""Custom exceptions for the ado-task-manager MCP."""

from __future__ import annotations


class MCPUserError(RuntimeError):
    """Exception raised for expected, user-facing errors."""

    def __init__(self, message: str, status: int = 400) -> None:
        super().__init__(message)
        self.status = status


class AdoRequestError(RuntimeError):
    """Raised when Azure DevOps API returns an unexpected error."""

    def __init__(self, message: str, status: int) -> None:
        super().__init__(message)
        self.status = status


class MissingConfigurationError(RuntimeError):
    """Raised when required environment configuration is missing."""
