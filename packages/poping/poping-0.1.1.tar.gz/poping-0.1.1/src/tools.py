"""
[Tools Module - Direct Tool Execution]
======================================
- Purpose: Access and execute marketplace tools directly without agents
- Data Flow: SDK → Backend /api/v1/tools/market/execute → Tool executor
- Usage:
    import poping
    tool = poping.tools["nano-banana-pro"]
    result = tool.execute({"prompt": "...", "image_uris": [...]})
"""

from __future__ import annotations

from typing import Any, Dict

from .client import PopingClient
from .exceptions import APIError, ConfigurationError

__all__ = ["MarketplaceTool", "ToolsRegistry"]


class MarketplaceTool:
    """
    Wrapper for direct marketplace tool execution.

    Usage:
        tool = poping.tools["nano-banana-pro"]
        result = tool.execute({
            "prompt": "orange cat",
            "image_uris": ["@context://images/white.png"]
        })
    """

    def __init__(self, client: PopingClient, tool_name: str):
        """
        Initialize tool wrapper.

        Args:
            client: HTTP client
            tool_name: Tool identifier
        """
        self.client = client
        self.tool_name = tool_name
        self._metadata: Dict[str, Any] | None = None

    def execute(self, input_data: Dict[str, Any]) -> Any:
        """
        Execute tool directly (calls underlying executor, no wrappers).

        Args:
            input_data: Tool parameters (matches tool's input_schema)

        Returns:
            Tool result (type depends on tool)

        Raises:
            APIError: If execution fails
            ConfigurationError: If tool not found

        Usage:
            result = tool.execute({
                "prompt": "a cute cat",
                "image_uris": ["@context://images/img.png"]
            })
        """
        payload = {
            "tool_name": self.tool_name,
            "input": input_data,
        }

        response = self.client._request(
            "POST",
            "/api/v1/tools/market/execute",
            json_data=payload
        )

        # Response format: {tool_name, result, credit_cost, credits_charged, credits_remaining}
        return response.get("result")

    @property
    def metadata(self) -> Dict[str, Any]:
        """
        Get tool metadata (lazy-loaded).

        Returns:
            {
                "name": str,
                "description": str,
                "category": str,
                "credit_cost": float,
                "input_schema": dict,
                "tags": list[str],
                "version": str
            }
        """
        if self._metadata is None:
            response = self.client._request(
                "GET",
                f"/api/v1/tools/market/{self.tool_name}"
            )
            self._metadata = response

        return self._metadata

    def __repr__(self) -> str:
        return f"MarketplaceTool(name='{self.tool_name}')"


class ToolsRegistry:
    """
    Registry for accessing marketplace tools via dict-like interface.

    Usage:
        import poping
        poping.set(api_key="...")

        # Access tool
        tool = poping.tools["nano-banana-pro"]

        # Execute
        result = tool.execute({"prompt": "...", ...})

        # List tools
        all_tools = poping.tools.list()
    """

    def __init__(self, client: PopingClient):
        """
        Initialize registry.

        Args:
            client: HTTP client
        """
        self.client = client

    def __getitem__(self, tool_name: str) -> MarketplaceTool:
        """
        Get tool by name (dict-style access).

        Args:
            tool_name: Tool identifier

        Returns:
            MarketplaceTool instance

        Usage:
            tool = poping.tools["nano-banana-pro"]
        """
        return MarketplaceTool(self.client, tool_name)

    def list(self, category: str | None = None) -> list[Dict[str, Any]]:
        """
        List all marketplace tools.

        Args:
            category: Optional filter by category (image, text, math, etc.)

        Returns:
            List of tool metadata dicts

        Usage:
            all_tools = poping.tools.list()
            image_tools = poping.tools.list(category="image")
        """
        params = {}
        if category:
            params["category"] = category

        response = self.client._request(
            "GET",
            "/api/v1/tools/market",
            params=params
        )

        return response.get("tools", [])

    def __repr__(self) -> str:
        return "ToolsRegistry()"
