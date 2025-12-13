"""
[SDK Types]
===========
- Purpose: Shared type definitions for Poping SDK
- Data Structures:
    - StructuredResponse: Wrapper for structured output (Pydantic models)
"""

from typing import Any, TypeVar

T = TypeVar('T')


class StructuredResponse:
    """
    Wrapper for structured output responses.

    Contains both the parsed Pydantic model and the raw response.

    Usage:
        response = session.chat("Extract person info")
        person = response.parsed  # Pydantic model instance
        raw = response.raw  # Raw backend response
    """

    def __init__(self, parsed: Any, raw: dict):
        """
        Initialize structured response.

        Args:
            parsed: Parsed Pydantic model instance
            raw: Raw backend response dict
        """
        self.parsed = parsed
        self.raw = raw

    def __repr__(self) -> str:
        return f"StructuredResponse(parsed={self.parsed!r})"

    def __str__(self) -> str:
        return str(self.parsed)
