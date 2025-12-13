"""
[SDK Exceptions]
================
- Purpose: Custom exceptions for Poping SDK
- Usage: Raise specific exceptions for different error scenarios
"""


class PopingError(Exception):
    """Base exception for Poping SDK."""
    pass


class AuthenticationError(PopingError):
    """Authentication failed (invalid API key)."""
    pass


class APIError(PopingError):
    """API request failed."""

    def __init__(self, message: str, status_code: int | None = None, response: dict | None = None):
        super().__init__(message)
        self.status_code = status_code
        self.response = response


class ValidationError(PopingError):
    """Input validation failed."""
    pass


class ToolError(PopingError):
    """Tool execution failed."""
    pass


class ConfigurationError(PopingError):
    """SDK configuration error."""
    pass


class SubagentError(PopingError):
    """Subagent execution failed."""
    pass
