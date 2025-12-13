"""
[HTTP Client]
=============
- Purpose: Thin HTTP wrapper for Poping backend API
- Data Flow: SDK request → HTTP → backend → HTTP → SDK response
- Core Functions:
    - chat: Send message or tool_results, get complete response
    - chat_stream_events: Stream events from backend
    - create_agent: POST /agents
    - update_agent: PATCH /agents/{agent_id}
    - get_agent: GET /agents/{agent_id}
"""

from __future__ import annotations

import json
from typing import Any, Dict, Iterator, List, Optional

import requests

from .exceptions import APIError, AuthenticationError, ValidationError

__all__ = ["PopingClient"]


class PopingClient:
    """
    HTTP client for Poping backend API.

    Thin wrapper over requests library.
    Handles authentication, error responses, and streaming.
    """

    def __init__(self, api_key: str, base_url: str | None = None):
        """
        Initialize client.

        Args:
            api_key: Poping API key
            base_url: Backend URL (defaults to http://127.0.0.1:8000)
        """
        self.api_key = api_key
        self.base_url = base_url or "http://127.0.0.1:8000"
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        })

    def _request(
        self,
        method: str,
        path: str,
        json_data: Dict[str, Any] | None = None,
        params: Dict[str, Any] | None = None,
    ) -> Dict[str, Any]:
        """
        Make HTTP request and handle errors.

        Args:
            method: HTTP method (GET, POST, PATCH, DELETE)
            path: API path (e.g., "/api/v1/agents")
            json_data: JSON payload
            params: Query parameters

        Returns:
            Response JSON

        Raises:
            AuthenticationError: 401
            ValidationError: 400
            APIError: Other errors
        """
        url = f"{self.base_url}{path}"

        try:
            response = self.session.request(
                method=method,
                url=url,
                json=json_data,
                params=params,
                timeout=60,
            )

            # Handle error status codes
            if response.status_code == 401:
                raise AuthenticationError("Invalid API key")
            elif response.status_code == 400:
                try:
                    error_detail = response.json().get("detail", "Validation error")
                except:
                    error_detail = response.text or "Validation error"
                raise ValidationError(error_detail)
            elif response.status_code >= 400:
                try:
                    error_detail = response.json().get("detail", f"HTTP {response.status_code}")
                    error_response = response.json() if response.content else None
                except:
                    error_detail = response.text or f"HTTP {response.status_code}"
                    error_response = None
                raise APIError(
                    error_detail,
                    status_code=response.status_code,
                    response=error_response,
                )

            return response.json()

        except requests.exceptions.Timeout:
            raise APIError("Request timeout")
        except requests.exceptions.ConnectionError:
            raise APIError(f"Connection failed: {self.base_url}")
        except requests.exceptions.RequestException as e:
            raise APIError(f"Request failed: {str(e)}")

    def _stream_request(
        self,
        method: str,
        path: str,
        json_data: Dict[str, Any] | None = None,
    ) -> Iterator[Dict[str, Any]]:
        """
        Make streaming HTTP request (NDJSON).

        Args:
            method: HTTP method (POST)
            path: API path
            json_data: JSON payload

        Yields:
            Event dicts (parsed from NDJSON lines)

        Raises:
            APIError: On HTTP errors
        """
        url = f"{self.base_url}{path}"

        try:
            response = self.session.request(
                method=method,
                url=url,
                json=json_data,
                stream=True,
                timeout=120,
            )

            # Check for errors
            if response.status_code >= 400:
                error_detail = response.json().get("detail", f"HTTP {response.status_code}")
                raise APIError(
                    error_detail,
                    status_code=response.status_code,
                )

            # Stream NDJSON lines
            for line in response.iter_lines():
                if line:
                    try:
                        event = json.loads(line.decode("utf-8"))
                        yield event
                    except json.JSONDecodeError:
                        continue  # Skip malformed lines

        except requests.exceptions.Timeout:
            raise APIError("Stream timeout")
        except requests.exceptions.ConnectionError:
            raise APIError(f"Connection failed: {self.base_url}")
        except requests.exceptions.RequestException as e:
            raise APIError(f"Stream failed: {str(e)}")

    # === Agent CRUD ===

    def create_agent(
        self,
        name: str,
        model: str,
        provider: str,
        system: str | None,
        temperature: float | None,
        max_tokens: int,
        tools: List[Dict[str, Any]],
        knowledge: List[str],
        datasets: List[str],
        project_id: str | None,
        agent_id: str | None,
    ) -> Dict[str, Any]:
        """Create agent on backend."""
        payload = {
            "name": name,
            "model": model,
            "provider": provider,
            "system": system,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "tools": tools,
            "knowledge": knowledge,
            "datasets": datasets,
            "project_id": project_id,
            "agent_id": agent_id,
        }
        return self._request("POST", "/api/v1/agents", json_data=payload)

    def update_agent(
        self,
        agent_id: str,
        name: str | None,
        model: str | None,
        provider: str | None,
        system: str | None,
        temperature: float | None,
        max_tokens: int | None,
        tools: List[Dict[str, Any]] | None,
        knowledge: List[str] | None,
        datasets: List[str] | None,
        project_id: str | None,
    ) -> Dict[str, Any]:
        """Update agent on backend."""
        payload = {
            "name": name,
            "model": model,
            "provider": provider,
            "system": system,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "tools": tools,
            "knowledge": knowledge,
            "datasets": datasets,
            "project_id": project_id,
        }
        # Remove None values
        payload = {k: v for k, v in payload.items() if v is not None}
        return self._request("PATCH", f"/api/v1/agents/{agent_id}", json_data=payload)

    def get_agent(self, agent_id: str, project_id: str | None = None) -> Dict[str, Any]:
        """Get agent config from backend."""
        params = {"project_id": project_id} if project_id else None
        return self._request("GET", f"/api/v1/agents/{agent_id}", params=params)

    def list_agents(
        self,
        project_id: str | None = None,
        name: str | None = None,
    ) -> List[Dict[str, Any]]:
        """
        List agents with optional filters.

        Args:
            project_id: Filter by project
            name: Filter by exact agent name

        Returns:
            List of agent configs
        """
        params = {}
        if project_id:
            params["project_id"] = project_id
        if name:
            params["name"] = name

        response = self._request("GET", "/api/v1/agents", params=params if params else None)
        # Backend returns list directly or dict with "agents" key
        if isinstance(response, list):
            return response
        return response.get("agents", [])

    # === Chat ===

    def chat(
        self,
        agent_id: str,
        message: str | None = None,
        tool_results: List[Dict[str, Any]] | None = None,
        session_id: str | None = None,
        project_id: str | None = None,
        end_user_id: str | None = None,
        parent_session_id: str | None = None,
        response_model_schema: Dict[str, Any] | None = None,
    ) -> Dict[str, Any]:
        """
        Send chat message (non-streaming).

        Args:
            agent_id: Agent identifier
            message: User message (mutually exclusive with tool_results)
            tool_results: Tool execution results (mutually exclusive with message)
            session_id: Session identifier
            project_id: Project identifier
            end_user_id: End user identifier
            parent_session_id: Parent session ID (for subagents)
            response_model_schema: JSON schema for structured output

        Returns:
            Response dict with message, session_id, etc.
        """
        payload = {
            "message": message,
            "tool_results": tool_results,
            "session_id": session_id,
            "project_id": project_id,
            "end_user_id": end_user_id,
            "parent_session_id": parent_session_id,
            "response_model_schema": response_model_schema,
        }
        # Remove None values
        payload = {k: v for k, v in payload.items() if v is not None}

        return self._request("POST", f"/api/v1/agents/{agent_id}/chat", json_data=payload)

    def chat_stream_events(
        self,
        agent_id: str,
        message: str | None = None,
        tool_results: List[Dict[str, Any]] | None = None,
        session_id: str | None = None,
        project_id: str | None = None,
        end_user_id: str | None = None,
        parent_session_id: str | None = None,
    ) -> Iterator[Dict[str, Any]]:
        """
        Stream chat messages (NDJSON).

        Args:
            agent_id: Agent identifier
            message: User message (mutually exclusive with tool_results)
            tool_results: Tool execution results (mutually exclusive with message)
            session_id: Session identifier
            project_id: Project identifier
            end_user_id: End user identifier
            parent_session_id: Parent session ID (for subagents)

        Yields:
            Event dicts (message_start, content_block_delta, tool_use, etc.)
        """
        payload = {
            "message": message,
            "tool_results": tool_results,
            "session_id": session_id,
            "project_id": project_id,
            "end_user_id": end_user_id,
            "parent_session_id": parent_session_id,
        }
        # Remove None values
        payload = {k: v for k, v in payload.items() if v is not None}

        return self._stream_request("POST", f"/api/v1/agents/{agent_id}/chat/stream", json_data=payload)
