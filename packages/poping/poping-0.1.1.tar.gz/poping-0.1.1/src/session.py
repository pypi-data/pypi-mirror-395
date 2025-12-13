"""
[Session - Chat Session Management]
====================================
- Purpose: Manage conversation with automatic tool execution
- Data Flow:
    user message → backend → tool_use → execute local/subagent → tool_result → backend → response
- Core Logic:
    1. Non-streaming: _chat_sync() - simple loop
    2. Streaming: _chat_stream() - event-driven loop
    3. Shared: _execute_tools() - unified tool execution
- Tools Handled:
    - Local tools: Python functions (SDK executes)
    - Subagents: Other agents (SDK orchestrates)
    - Cloud tools: Backend executes (SDK skips)
- Related Files:
    @/poping/src/client.py → HTTP client
    @/poping/src/agent.py → Agent instance
"""

from __future__ import annotations

import json
from typing import Any, Dict, Iterator, List, Optional, Type

from .client import PopingClient
from .exceptions import APIError, SubagentError, ToolError
from .types import StructuredResponse

__all__ = ["Session"]


class Session:
    """
    Chat session with automatic tool execution.

    Responsibilities:
    - Send messages to backend
    - Execute local tools and subagents
    - Handle streaming events
    - Return formatted responses

    Usage:
        with agent.session(end_user_id="alice") as session:
            # Non-streaming
            response = session.chat("Hello")

            # Streaming
            for event in session.stream("Hello"):
                if event["type"] == "text_delta":
                    print(event["delta"]["text"], end="")
    """

    def __init__(
        self,
        client: PopingClient,
        agent_id: str,
        project_id: str | None,
        end_user_id: str,
        session_id: str | None,
        parent_session_id: str | None,
        local_tool_funcs: Dict[str, Any],
        subagent_objects: Dict[str, Any],
        response_model: Type[Any] | None,
    ):
        """
        Initialize session.

        Args:
            client: HTTP client
            agent_id: Agent identifier
            project_id: Project identifier
            end_user_id: End user identifier
            session_id: Session identifier (backend generates if None)
            parent_session_id: Parent session ID (for subagents)
            local_tool_funcs: Map of tool name → callable
            subagent_objects: Map of agent_id → Agent instance
            response_model: Pydantic model for structured output
        """
        import uuid

        self.client = client
        self.agent_id = agent_id
        self.project_id = project_id
        self.end_user_id = end_user_id
        # Generate session_id if not provided
        self.session_id = session_id or f"sess_{uuid.uuid4().hex[:12]}"
        self.parent_session_id = parent_session_id
        self.local_tool_funcs = local_tool_funcs
        self.subagent_objects = subagent_objects
        self.response_model = response_model
        # Track streaming mode for sub-agent execution
        self._streaming_mode = False
        self._streaming_event_callback = None

    # === Public API ===

    def chat(self, message: str, raw: bool = False) -> str | StructuredResponse:
        """
        Non-streaming chat with automatic tool execution.

        Args:
            message: User message
            raw: If True, return dict response; if False, return text or StructuredResponse

        Returns:
            Text response or StructuredResponse (if response_model configured)

        Raises:
            ToolError: If tool execution fails
            SubagentError: If subagent execution fails
            APIError: If backend request fails
        """
        return self._chat_sync(message, raw)

    def stream(self, message: str) -> Iterator[Dict[str, Any]]:
        """
        Streaming chat with automatic tool execution.

        Args:
            message: User message

        Yields:
            Event dicts (message_start, content_block_delta, tool_result, etc.)

        Raises:
            ToolError: If tool execution fails
            SubagentError: If subagent execution fails
            APIError: If backend request fails
        """
        return self._chat_stream(message)

    @property
    def messages(self) -> list[Dict[str, Any]]:
        """
        Get full conversation history for this session.

        Returns:
            List of message dicts with role, content, model, etc.

        Raises:
            APIError: If backend request fails

        Usage:
            messages = session.messages
            for msg in messages:
                print(f"{msg['role']}: {msg['content']}")
        """
        if not self.session_id:
            return []

        response = self.client._request(
            "GET",
            f"/api/v1/sessions/{self.session_id}/messages",
            params={
                "project_id": self.project_id,
                "end_user_id": self.end_user_id,
            }
        )

        # Backend returns list directly, not dict with "messages" key
        return response

    def upload(self, file_path: str, target_path: str | None = None) -> str:
        """
        Upload file to session storage.

        Args:
            file_path: Local file path to upload
            target_path: Target path in session storage (defaults to filename)

        Returns:
            Storage URI (@context://...)

        Raises:
            FileNotFoundError: If local file not found
            APIError: If upload fails

        Usage:
            uri = session.upload("image.png")
            # Returns: @context://image.png
        """
        import os
        import requests

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        # Determine filename
        if target_path is None:
            filename = os.path.basename(file_path)
        else:
            filename = target_path

        # Read file
        with open(file_path, "rb") as f:
            file_content = f.read()

        # Upload using backend endpoint: POST /api/v1/sessions/{session_id}/artifacts
        url = f"{self.client.base_url}/api/v1/sessions/{self.session_id}/artifacts"
        files = {"file": (filename, file_content)}
        params = {
            "project_id": self.project_id,
            "end_user_id": self.end_user_id,
        }

        headers = {"Authorization": f"Bearer {self.client.api_key}"}
        response = requests.post(url, files=files, params=params, headers=headers)

        if response.status_code != 200:
            from .exceptions import APIError
            raise APIError(f"Upload failed: {response.status_code} {response.text}")

        result = response.json()
        # Backend returns: {"status": "success", "filename": ..., "uri": "@context://folder/file", "folder": ...}
        return result["uri"]

    # === Tool Execution (Shared by sync and stream) ===

    def _execute_tools(self, tool_uses: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Execute local tools and subagents.

        Args:
            tool_uses: List of tool_use dicts from backend

        Returns:
            List of tool_result dicts (only for local tools + subagents)

        Logic:
            1. For each tool_use:
                - If local tool → execute
                - If call_subagent → execute
                - Else → skip (cloud tool, backend handled)
            2. Return tool_results (empty if no local tools)

        Note: This is the ONLY place tool execution happens.
              Both chat() and stream() call this function.
        """
        tool_results = []

        for tool_use in tool_uses:
            tool_name = tool_use.get("name")
            tool_use_id = tool_use.get("id")
            tool_input = tool_use.get("input", {})

            # Local tool
            if tool_name in self.local_tool_funcs:
                try:
                    func = self.local_tool_funcs[tool_name]
                    result = func(**tool_input)
                    tool_results.append({
                        "tool_use_id": tool_use_id,
                        "content": str(result),
                        "is_error": False,
                    })
                except Exception as e:
                    tool_results.append({
                        "tool_use_id": tool_use_id,
                        "content": f"Tool error: {type(e).__name__}: {str(e)}",
                        "is_error": True,
                    })

            # Subagent
            elif tool_name == "call_subagent":
                result = self._execute_subagent(tool_use)
                tool_results.append(result)

            # Else: cloud tool (backend handled, no SDK action)

        return tool_results

    def _execute_subagent(self, tool_use: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute subagent.

        Args:
            tool_use: tool_use dict for call_subagent

        Returns:
            tool_result dict

        Logic:
            1. Extract agent_id and task
            2. Lookup subagent in self.subagent_objects
            3. Create subagent session with parent_session_id
            4. If streaming mode: call sub_session.stream() and forward events
            5. Else: call sub_session.chat(task)
            6. Return result
        """
        agent_id = tool_use.get("input", {}).get("agent_id")
        task = tool_use.get("input", {}).get("task", "")
        tool_use_id = tool_use.get("id")

        if agent_id not in self.subagent_objects:
            return {
                "tool_use_id": tool_use_id,
                "content": f"Subagent '{agent_id}' not found. Make sure to register it with with_subagent().",
                "is_error": True,
            }

        subagent = self.subagent_objects[agent_id]

        try:
            # Create subagent session with parent reference
            # Key: parent_session_id allows subagent to access parent's context via @context[parent]://
            with subagent.session(
                end_user_id=self.end_user_id,
                session_id=None,  # Backend generates new session_id
                parent_session_id=self.session_id,  # SDK provides parent context
            ) as sub_session:
                # If parent is streaming, stream sub-agent events too
                if self._streaming_mode and self._streaming_event_callback:
                    result_text = ""
                    for event in sub_session.stream(task):
                        # Forward sub-agent streaming events to parent
                        self._streaming_event_callback(event)
                        # Accumulate text from content_block_delta events for final result
                        if event.get("type") == "content_block_delta":
                            delta = event.get("delta", {})
                            if delta.get("type") == "text_delta":
                                result_text += delta.get("text", "")

                    return {
                        "tool_use_id": tool_use_id,
                        "content": result_text if result_text else "Sub-agent completed (streaming)",
                        "is_error": False,
                    }
                else:
                    # Non-streaming mode
                    result = sub_session.chat(task)
                    return {
                        "tool_use_id": tool_use_id,
                        "content": str(result),
                        "is_error": False,
                    }
        except Exception as e:
            return {
                "tool_use_id": tool_use_id,
                "content": f"Subagent error: {type(e).__name__}: {str(e)}",
                "is_error": True,
            }

    # === Non-Streaming Path ===

    def _chat_sync(self, message: str, raw: bool) -> str | Dict[str, Any] | StructuredResponse:
        """
        Simple synchronous tool execution loop.

        Args:
            message: User message
            raw: Return raw dict if True

        Returns:
            Text response, StructuredResponse, or raw dict

        Logic:
            1. Send message → backend returns complete response
            2. Extract tool_use blocks from response.content
            3. Execute tools via _execute_tools()
            4. Send tool_results back → backend returns next response
            5. Repeat until no tool_use blocks
            6. Return final response
        """
        pending_tool_results = None

        for iteration in range(300):  # Max iterations to prevent infinite loops
            # Send request
            if pending_tool_results:
                # Continue with tool results
                resp = self.client.chat(
                    self.agent_id,
                    tool_results=pending_tool_results,
                    session_id=self.session_id,
                    project_id=self.project_id,
                    end_user_id=self.end_user_id,
                    parent_session_id=self.parent_session_id,
                )
            else:
                # Initial message
                resp = self.client.chat(
                    self.agent_id,
                    message=message,
                    session_id=self.session_id,
                    project_id=self.project_id,
                    end_user_id=self.end_user_id,
                    parent_session_id=self.parent_session_id,
                    response_model_schema=self._get_response_schema(),
                )

            # Update session_id from response (backend generates it on first call)
            if not self.session_id and "session_id" in resp:
                self.session_id = resp["session_id"]

            # Extract tool uses
            message_content = resp.get("message", {}).get("content", [])
            tool_uses = [b for b in message_content if b.get("type") == "tool_use"]

            if not tool_uses:
                # No tools - done
                return self._format_response(resp, raw)

            # Execute tools
            tool_results = self._execute_tools(tool_uses)

            if not tool_results:
                # All tools were cloud tools (backend handled)
                return self._format_response(resp, raw)

            # Continue with tool results
            pending_tool_results = tool_results
            message = None  # Clear message for next iteration

        raise ToolError("Max tool execution rounds (300) exceeded. Possible infinite loop.")

    # === Streaming Path ===

    def _chat_stream(self, message: str) -> Iterator[Dict[str, Any]]:
        """
        Event-driven streaming loop with tool execution.

        Args:
            message: User message

        Yields:
            Event dicts (message_start, content_block_delta, tool_result, etc.)

        Logic:
            1. Stream from backend (yields events)
            2. Accumulate tool_use blocks:
                - content_block_start: init tool_use
                - content_block_delta: accumulate partial JSON
                - content_block_stop: finalize tool_use
            3. When message_stop:
                - Execute tools via _execute_tools()
                - Emit synthetic tool_result events
                - If tools executed, continue stream with tool_results
                - Else, done

        Critical: Emit events immediately for text, buffer for tools.
        """
        # Enable streaming mode for sub-agents
        self._streaming_mode = True

        # Event buffer for sub-agent streaming events
        subagent_events = []

        def event_callback(event):
            """Callback to buffer sub-agent events"""
            subagent_events.append(event)

        self._streaming_event_callback = event_callback

        pending_tool_results = None

        for iteration in range(300):  # Max iterations
            # State for this streaming round
            current_tool_use = None
            accumulated_tool_uses = []
            partial_json_buffer = {}  # index → partial JSON string
            got_message_stop = False
            got_any_content = False  # Track if we received any content this iteration

            # Stream from backend
            if pending_tool_results:
                events = self.client.chat_stream_events(
                    self.agent_id,
                    tool_results=pending_tool_results,
                    session_id=self.session_id,
                    project_id=self.project_id,
                    end_user_id=self.end_user_id,
                    parent_session_id=self.parent_session_id,
                )
            else:
                events = self.client.chat_stream_events(
                    self.agent_id,
                    message=message,
                    session_id=self.session_id,
                    project_id=self.project_id,
                    end_user_id=self.end_user_id,
                    parent_session_id=self.parent_session_id,
                )

            # Process events (with graceful handling of premature stream end)
            try:
                for event in events:
                    event_type = event.get("type")

                    # === Text events: emit immediately ===
                    if event_type == "content_block_delta":
                        got_any_content = True
                        delta = event.get("delta", {})
                        if delta.get("type") == "text_delta":
                            yield event  # Pass through
                        elif delta.get("type") == "input_json_delta":
                            # Tool input - buffer it
                            idx = event.get("index")
                            partial = delta.get("partial_json", "")
                            partial_json_buffer[idx] = partial_json_buffer.get(idx, "") + partial

                    # === Tool events: accumulate ===
                    elif event_type == "content_block_start":
                        got_any_content = True
                        cb = event.get("content_block", {})
                        if cb.get("type") == "tool_use":
                            idx = event.get("index")
                            current_tool_use = {
                                "index": idx,
                                "id": cb.get("id"),
                                "name": cb.get("name"),
                                "input": cb.get("input") or {},
                            }

                    elif event_type == "content_block_stop":
                        if current_tool_use:
                            # Finalize tool_use: parse buffered JSON
                            idx = current_tool_use["index"]
                            if idx in partial_json_buffer:
                                try:
                                    current_tool_use["input"] = json.loads(partial_json_buffer[idx])
                                except json.JSONDecodeError:
                                    pass  # Keep existing input
                            accumulated_tool_uses.append(current_tool_use)
                            current_tool_use = None

                    # === Other events: pass through ===
                    elif event_type in ("message_start", "message_delta"):
                        got_any_content = True
                        # Extract session_id from source field (e.g., "agent:sess_123")
                        if not self.session_id and "source" in event:
                            source = event["source"]
                            if ":" in source:
                                potential_session_id = source.split(":")[-1]
                                if potential_session_id.startswith("sess_"):
                                    self.session_id = potential_session_id
                        yield event

                    elif event_type == "tool_result":
                        # Backend-executed tool result - pass through and continue
                        got_any_content = True
                        yield event

                    elif event_type == "message_stop":
                        got_message_stop = True
                        # Note: Don't break here - backend may send more rounds for cloud tool execution
                        # Just mark that we got message_stop and continue processing events
                        yield event

            except APIError as e:
                # Handle premature stream end gracefully
                # If we've already processed some content, this is likely just a cleanup issue
                if "Response ended prematurely" in str(e) or "Stream failed" in str(e):
                    # Stream ended early but we may have gotten useful data
                    # Continue to check what we received
                    pass
                else:
                    # Real error - re-raise
                    raise

            # Check if we have tools to execute
            if not accumulated_tool_uses:
                # No tools in this iteration
                # If this is iteration 0 OR we got message_stop properly, we're done
                # If got some content (text) in this iteration, we're also done
                if iteration == 0 or got_message_stop or got_any_content:
                    return
                # Otherwise: stream ended prematurely after tool execution
                # Backend should have sent final text but didn't - return gracefully
                return

            # Execute tools
            tool_results = self._execute_tools(accumulated_tool_uses)

            # Yield buffered sub-agent streaming events first
            if subagent_events:
                for event in subagent_events:
                    yield event
                subagent_events.clear()

            if not tool_results:
                # No local tools (all cloud tools were executed by backend)
                # The backend stream should continue automatically with more rounds
                # We already consumed all events from the stream above (no break on message_stop)
                # So if we're here, the stream has ended - we're done
                return

            # Emit synthetic tool_result events
            for tr in tool_results:
                yield {
                    "type": "tool_result",
                    "tool_use_id": tr["tool_use_id"],
                    "content": tr["content"],
                    "is_error": tr.get("is_error", False),
                }

            # Continue with tool results
            pending_tool_results = tool_results
            message = None  # Clear message for next iteration

        raise ToolError("Max tool execution rounds (300) exceeded in streaming loop.")

    # === Helpers ===

    def _format_response(self, resp: Dict[str, Any], raw: bool) -> str | Dict[str, Any] | StructuredResponse:
        """
        Format response based on raw flag and response_model.

        Args:
            resp: Backend response dict
            raw: Return raw dict if True

        Returns:
            - If raw=True: return full response dict
            - If response_model set: return StructuredResponse
            - Else: return text content
        """
        if raw:
            return resp

        # Structured output
        if "parsed" in resp and self.response_model:
            # Backend returned parsed Pydantic model dict
            parsed_data = resp["parsed"]
            # Reconstruct Pydantic model
            try:
                parsed_obj = self.response_model(**parsed_data)
                return StructuredResponse(parsed=parsed_obj, raw=resp)
            except Exception:
                # Fallback: return raw dict
                return StructuredResponse(parsed=parsed_data, raw=resp)

        # Text output
        message_content = resp.get("message", {}).get("content", [])
        text_blocks = [b.get("text", "") for b in message_content if b.get("type") == "text"]
        return "".join(text_blocks)

    def _get_response_schema(self) -> Dict[str, Any] | None:
        """
        Get JSON schema for structured output.

        Returns:
            JSON schema dict or None

        Logic:
            - If response_model set, generate schema using Pydantic
            - Supports both Pydantic v1 and v2
        """
        if not self.response_model:
            return None

        # Try Pydantic v2 first
        if hasattr(self.response_model, "model_json_schema"):
            return self.response_model.model_json_schema()

        # Fall back to Pydantic v1
        if hasattr(self.response_model, "schema"):
            return self.response_model.schema()

        return None
