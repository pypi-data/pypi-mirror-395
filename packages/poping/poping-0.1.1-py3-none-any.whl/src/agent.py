"""
[Agent Builder & Agent]
=======================
- Purpose: Builder pattern for creating agents + Agent instance for sessions
- Data Flow:
    AgentBuilder → build(name) → backend API → Agent instance → session()
- Core Classes:
    - AgentBuilder: Fluent API for agent configuration
    - Agent: Agent instance with session creation
- Related Files:
    @/poping/src/client.py → HTTP client
    @/poping/src/session.py → Session management
    @/poping/src/tool.py → Tool metadata extraction
"""

from __future__ import annotations

from contextlib import contextmanager
from typing import Any, Dict, List, Optional, Type, TypeVar

from .client import PopingClient
from .exceptions import ConfigurationError, ValidationError
from .tool import get_tool_definition

__all__ = ["AgentBuilder", "Agent"]

T = TypeVar('T')


class AgentBuilder:
    """
    Builder for creating/updating agents.

    Fluent API for agent configuration:
        - with_tools(local=[...], cloud=[...])
        - with_knowledge([...])
        - with_data([...])
        - with_subagent(agent, description)
        - with_llm_config(system, temp, max_tokens, response_model)
        - build(name) → Agent

    Design:
        - SDK sends minimal payload to backend
        - Backend validates and expands config
        - Local tools: SDK sends metadata (name, description, schema)
        - Cloud tools: SDK sends names only
        - Subagents: SDK builds call_subagent tool
    """

    def __init__(
        self,
        client: PopingClient,
        llm: str | None = None,
        agent_id: str | None = None,
        project_id: str | None = None,
    ):
        """
        Initialize agent builder.

        Args:
            client: HTTP client
            llm: Model identifier (e.g., "claude-sonnet-4-5")
            agent_id: Agent ID (for updates, None for create)
            project_id: Project ID
        """
        self.client = client
        self.llm = llm or "claude-sonnet-4-5"
        self.agent_id = agent_id
        self.project_id = project_id

        # Config
        self.system_prompt: str | None = None
        self.temperature: float | None = None
        self.max_tokens: int = 2048
        self.response_model: Type[Any] | None = None

        # Tools
        self.local_tools_metadata: List[Dict[str, Any]] = []  # {name, description, input_schema, callable}
        self.cloud_tools: List[str] = []  # Tool names/slugs

        # Resources
        self.knowledge_bases: List[str] = []
        self.datasets: List[str] = []

        # Subagents
        self.subagents: List[Dict[str, Any]] = []  # {agent_id, name, description, agent_instance}

    def with_tools(
        self,
        local: List[Any] | None = None,
        cloud: List[str] | None = None,
    ) -> AgentBuilder:
        """
        Register tools.

        Args:
            local: List of @tool() decorated functions
            cloud: List of cloud tool names/slugs

        Returns:
            Self (for chaining)

        Raises:
            ValidationError: If local tool invalid
        """
        if local:
            for fn in local:
                # Extract metadata
                tool_def = get_tool_definition(fn)
                if not tool_def:
                    raise ValidationError(
                        f"Invalid local tool: {fn}. Must be decorated with @tool() or be a dict"
                    )

                # Validate schema
                if "input_schema" not in tool_def or not tool_def["input_schema"]:
                    raise ValidationError(
                        f"Tool {tool_def['name']} missing input_schema"
                    )

                # Store metadata with callable for direct access in build()
                self.local_tools_metadata.append({
                    **tool_def,
                    "callable": fn._poping_tool["callable"] if hasattr(fn, "_poping_tool") else fn,
                })

        if cloud:
            self.cloud_tools.extend(cloud)

        return self

    def with_knowledge(self, knowledge_bases: List[str]) -> AgentBuilder:
        """
        Register knowledge bases.

        Args:
            knowledge_bases: List of knowledge base names

        Returns:
            Self (for chaining)
        """
        self.knowledge_bases.extend(knowledge_bases)
        return self

    def with_dataset(self, datasets: List[str]) -> AgentBuilder:
        """
        Register datasets.

        Args:
            datasets: List of dataset names

        Returns:
            Self (for chaining)
        """
        self.datasets.extend(datasets)
        return self

    def with_subagent(
        self,
        agent: Agent,
        description: str,
    ) -> AgentBuilder:
        """
        Register subagent.

        Args:
            agent: Sub-agent instance
            description: Description for LLM

        Returns:
            Self (for chaining)
        """
        self.subagents.append({
            "agent_id": agent.agent_id,
            "name": agent.agent_id,  # Use agent_id as name
            "description": description,
            "agent_instance": agent,
        })
        return self

    def with_llm_config(
        self,
        system_prompt: str | None = None,
        temperature: float | None = None,
        max_tokens: int | None = None,
        response_model: Type[T] | None = None,
    ) -> AgentBuilder:
        """
        Configure LLM parameters.

        Args:
            system_prompt: System prompt
            temperature: Sampling temperature (0.0-1.0)
            max_tokens: Max tokens per response
            response_model: Pydantic model for structured output

        Returns:
            Self (for chaining)
        """
        if system_prompt is not None:
            self.system_prompt = system_prompt
        if temperature is not None:
            self.temperature = temperature
        if max_tokens is not None:
            self.max_tokens = max_tokens
        if response_model is not None:
            self.response_model = response_model

        return self

    def _build_subagent_tool(self) -> Dict[str, Any]:
        """
        Build call_subagent tool schema.

        Returns:
            Tool definition dict

        Logic:
            - Enum of agent_ids from registered subagents
            - Description lists available subagents
        """
        subagent_list = "\n".join(
            f"  - {s['agent_id']}: {s['description']}"
            for s in self.subagents
        )

        return {
            "name": "call_subagent",
            "description": f"Call a subagent to handle a subtask. Available subagents:\n{subagent_list}",
            "input_schema": {
                "type": "object",
                "properties": {
                    "agent_id": {
                        "type": "string",
                        "description": "Subagent identifier",
                        "enum": [s["agent_id"] for s in self.subagents],
                    },
                    "task": {
                        "type": "string",
                        "description": "Task description for subagent",
                    },
                },
                "required": ["agent_id", "task"],
            },
            "type": "local",  # SDK executes this
        }

    def _build_backend_payload(self, name: str) -> Dict[str, Any]:
        """
        Build backend API payload.

        Args:
            name: Agent name

        Returns:
            Payload dict for create/update agent

        Logic:
            - Local tools: send metadata (name, description, input_schema)
            - Cloud tools: send names only
            - Subagents: add call_subagent tool
            - Backend handles: tool registry lookup, resource tools, validation
        """
        tools: List[Dict[str, Any]] = []

        # Local tools - send full metadata for LLM
        for tool_meta in self.local_tools_metadata:
            tools.append({
                "name": tool_meta["name"],
                "description": tool_meta["description"],
                "input_schema": tool_meta["input_schema"],
                "type": "local",  # Mark as SDK-executed
            })

        # Cloud tools - send names only
        for cloud_name in self.cloud_tools:
            tools.append({
                "name": cloud_name,
                "type": "cloud",
            })

        # Subagent tool - if subagents registered
        if self.subagents:
            tools.append(self._build_subagent_tool())

        return {
            "name": name,
            "model": self.llm,
            "provider": "anthropic",  # TODO: Make configurable?
            "system": self.system_prompt,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "tools": tools,
            "knowledge": self.knowledge_bases,
            "datasets": self.datasets,
            "project_id": self.project_id,
            "agent_id": self.agent_id,  # None for create, set for update
        }

    def build(self, name: str) -> Agent:
        """
        Create or update agent on backend.

        Args:
            name: Agent name

        Returns:
            Agent instance

        Raises:
            ValidationError: If config invalid
            APIError: If backend request fails

        Logic:
            1. Check if agent with same name exists
            2. If exists and config unchanged → reuse
            3. If exists and config changed → update
            4. If not exists → create
            5. Return Agent instance with local tool references and subagents
        """
        # Validate
        if not name:
            raise ValidationError("Agent name is required")

        # Build payload
        payload = self._build_backend_payload(name)

        # Check if agent with this name already exists
        if not self.agent_id:
            existing_agents = self.client.list_agents(
                project_id=self.project_id,
                name=name
            )
            if existing_agents:
                # Found existing agent with same name
                existing_agent_summary = existing_agents[0]
                existing_agent_id = existing_agent_summary["agent_id"]

                # Fetch full config for comparison
                existing_agent = self.client.get_agent(
                    agent_id=existing_agent_id,
                    project_id=self.project_id
                )

                # Check if configuration has changed by comparing key fields
                config_changed = (
                    existing_agent.get("model") != payload.get("model") or
                    existing_agent.get("system") != payload.get("system") or
                    existing_agent.get("temperature") != payload.get("temperature") or
                    existing_agent.get("max_tokens") != payload.get("max_tokens")
                    # Note: tools, knowledge, datasets are harder to compare deeply
                    # so we'll update if any basic config changed
                )

                if config_changed:
                    # Update existing agent
                    self.client.update_agent(
                        agent_id=existing_agent_id,
                        name=payload["name"],
                        model=payload["model"],
                        provider=payload["provider"],
                        system=payload.get("system"),
                        temperature=payload.get("temperature"),
                        max_tokens=payload["max_tokens"],
                        tools=payload["tools"],
                        knowledge=payload.get("knowledge", []),
                        datasets=payload.get("datasets", []),
                        project_id=payload.get("project_id"),
                    )

                # Reuse existing agent_id
                agent_id = existing_agent_id
            else:
                # No existing agent, create new
                response = self.client.create_agent(
                    name=payload["name"],
                    model=payload["model"],
                    provider=payload["provider"],
                    system=payload.get("system"),
                    temperature=payload.get("temperature"),
                    max_tokens=payload["max_tokens"],
                    tools=payload["tools"],
                    knowledge=payload.get("knowledge", []),
                    datasets=payload.get("datasets", []),
                    project_id=payload.get("project_id"),
                    agent_id=None,
                )
                agent_id = response["agent_id"]
        else:
            # agent_id explicitly provided, update that specific agent
            response = self.client.update_agent(
                agent_id=self.agent_id,
                name=payload["name"],
                model=payload["model"],
                provider=payload["provider"],
                system=payload.get("system"),
                temperature=payload.get("temperature"),
                max_tokens=payload["max_tokens"],
                tools=payload["tools"],
                knowledge=payload.get("knowledge", []),
                datasets=payload.get("datasets", []),
                project_id=payload.get("project_id"),
            )
            agent_id = self.agent_id

        # Extract local tool functions (callable objects)
        local_tool_funcs = {
            tool_def["name"]: tool_def["callable"]
            for tool_def in self.local_tools_metadata
        }

        # Build subagent objects map
        subagent_objects = {
            s["agent_id"]: s["agent_instance"]
            for s in self.subagents
        }

        return Agent(
            client=self.client,
            agent_id=agent_id,
            project_id=self.project_id,
            local_tool_funcs=local_tool_funcs,
            subagent_objects=subagent_objects,
            response_model=self.response_model,
        )


class Agent:
    """
    Agent instance for creating sessions.

    Holds agent configuration and provides session() context manager.

    Usage:
        agent = poping.agent(llm="...").build(name="my_agent")

        with agent.session(end_user_id="alice") as session:
            response = session.chat("Hello")
    """

    def __init__(
        self,
        client: PopingClient,
        agent_id: str,
        project_id: str | None,
        local_tool_funcs: Dict[str, Any],
        subagent_objects: Dict[str, Agent],
        response_model: Type[T] | None,
    ):
        """
        Initialize agent.

        Args:
            client: HTTP client
            agent_id: Agent identifier
            project_id: Project identifier
            local_tool_funcs: Map of tool name → callable
            subagent_objects: Map of agent_id → Agent instance
            response_model: Pydantic model for structured output
        """
        self.client = client
        self.agent_id = agent_id
        self.project_id = project_id
        self.local_tool_funcs = local_tool_funcs
        self.subagent_objects = subagent_objects
        self.response_model = response_model

    @contextmanager
    def session(
        self,
        end_user_id: str,
        session_id: str | None = None,
        parent_session_id: str | None = None,
    ):
        """
        Create session context.

        Args:
            end_user_id: End user identifier
            session_id: Session identifier (backend generates if None)
            parent_session_id: Parent session ID (for subagents)

        Yields:
            Session instance

        Usage:
            with agent.session(end_user_id="alice") as session:
                response = session.chat("Hello")
        """
        from .session import Session

        session = Session(
            client=self.client,
            agent_id=self.agent_id,
            project_id=self.project_id,
            end_user_id=end_user_id,
            session_id=session_id,
            parent_session_id=parent_session_id,
            local_tool_funcs=self.local_tool_funcs,
            subagent_objects=self.subagent_objects,
            response_model=self.response_model,
        )

        yield session

        # Cleanup (if needed)
        pass
