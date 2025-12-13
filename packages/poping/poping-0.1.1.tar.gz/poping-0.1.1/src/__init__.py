"""
[Poping SDK - Public API]
==========================
- Purpose: Module-level convenience API
- Data Flow: poping.set() → global context → poping.agent() → AgentBuilder
- Core Functions:
    - set(api_key, base_url, project): Configure SDK
    - agent(llm, agent_id) → AgentBuilder: Create agent builder
- Usage:
    import poping

    poping.set(api_key="pk_...", project="my_project")
    agent = poping.agent(llm="claude-sonnet-4-5").with_tools(local=[...]).build(name="my_agent")

    with agent.session(end_user_id="alice") as session:
        response = session.chat("Hello")
"""

from .agent import Agent, AgentBuilder
from .client import PopingClient
from .exceptions import (
    APIError,
    AuthenticationError,
    ConfigurationError,
    PopingError,
    SubagentError,
    ToolError,
    ValidationError,
)
from .session import Session
from .tool import get_tool_definition, tool
from .tools import ToolsRegistry
from .types import StructuredResponse

__all__ = [
    # Core
    "set",
    "agent",
    "tools",
    # Classes
    "Agent",
    "AgentBuilder",
    "Session",
    "PopingClient",
    "StructuredResponse",
    "ToolsRegistry",
    # Exceptions
    "PopingError",
    "AuthenticationError",
    "APIError",
    "ValidationError",
    "ToolError",
    "ConfigurationError",
    "SubagentError",
    # Tool
    "tool",
    "get_tool_definition",
]

# Global state
_global_client: PopingClient | None = None
_global_project: str | None = None
_global_tools: ToolsRegistry | None = None


def set(api_key: str, base_url: str | None = None, project: str | None = None) -> None:
    """
    Configure SDK globally.

    Args:
        api_key: Poping API key
        base_url: Backend URL (defaults to http://127.0.0.1:8000)
        project: Default project ID

    Usage:
        poping.set(api_key="pk_...", project="my_project")
    """
    global _global_client, _global_project, _global_tools

    _global_client = PopingClient(api_key=api_key, base_url=base_url)
    _global_project = project
    _global_tools = ToolsRegistry(_global_client)


def agent(llm: str | None = None, agent_id: str | None = None, *, project: str | None = None) -> AgentBuilder:
    """
    Create agent builder.

    Args:
        llm: Model identifier (e.g., "claude-sonnet-4-5")
        agent_id: Agent ID (for updates, None for create)
        project: Project ID (overrides global)

    Returns:
        AgentBuilder instance

    Raises:
        ConfigurationError: If SDK not configured (call poping.set() first)

    Usage:
        # Create new agent
        agent = poping.agent(llm="claude-sonnet-4-5").with_tools(...).build(name="my_agent")

        # Update existing agent
        agent = poping.agent(agent_id="agt_123").with_tools(...).build(name="updated_agent")
    """
    if not _global_client:
        raise ConfigurationError(
            "SDK not configured. Call poping.set(api_key='...') first."
        )

    return AgentBuilder(
        client=_global_client,
        llm=llm,
        agent_id=agent_id,
        project_id=project or _global_project,
    )


class _ToolsProxy:
    """Proxy object for accessing tools attribute."""
    def __getitem__(self, tool_name: str):
        if not _global_tools:
            raise ConfigurationError(
                "SDK not configured. Call poping.set(api_key='...') first."
            )
        return _global_tools[tool_name]

    def list(self, category: str | None = None):
        if not _global_tools:
            raise ConfigurationError(
                "SDK not configured. Call poping.set(api_key='...') first."
            )
        return _global_tools.list(category=category)

# Create singleton proxy instance
tools = _ToolsProxy()
