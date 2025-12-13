"""
[Tool Decorator]
================
- Purpose: Decorator for marking Python functions as local tools
- Data Flow: @tool() → metadata extraction → tool definition
- Usage:
    @tool()
    def my_function(a: int, b: int) -> int:
        '''Add two numbers'''
        return a + b
"""

from __future__ import annotations

import inspect
from functools import wraps
from typing import Any, Callable, Dict, Optional

__all__ = ["tool", "get_tool_definition"]


def _schema_from_signature(func: Callable) -> Dict[str, Any]:
    """
    Generate JSON schema from function signature.

    Args:
        func: Python function with type hints

    Returns:
        JSON schema dict

    Logic:
        1. Inspect function signature
        2. For each parameter:
            - Map Python type to JSON type
            - Mark as required if no default value
        3. Return schema dict
    """
    sig = inspect.signature(func)
    props: Dict[str, Any] = {}
    required = []

    for name, param in sig.parameters.items():
        type_hint = param.annotation
        json_type = "string"  # Default

        # Map Python types to JSON schema types
        if type_hint is int:
            json_type = "integer"
        elif type_hint is float:
            json_type = "number"
        elif type_hint is bool:
            json_type = "boolean"
        elif type_hint in (list, tuple) or str(type_hint).startswith(("list", "List", "typing.List")):
            json_type = "array"
        elif type_hint in (dict,) or str(type_hint).startswith(("dict", "Dict", "typing.Dict")):
            json_type = "object"

        props[name] = {"type": json_type}

        # Required if no default
        if param.default is inspect.Parameter.empty:
            required.append(name)

    schema: Dict[str, Any] = {"type": "object", "properties": props}
    if required:
        schema["required"] = required

    return schema


def tool(name: Optional[str] = None, schema: Optional[Dict[str, Any]] = None) -> Callable[[Callable], Callable]:
    """
    Decorator to mark function as a local tool.

    Args:
        name: Tool name (defaults to function name)
        schema: JSON schema for input (auto-generated from signature if not provided)

    Returns:
        Decorated function with metadata attached

    Usage:
        @tool()
        def add(a: int, b: int) -> int:
            '''Add two numbers'''
            return a + b

        @tool(name="custom_name", schema={...})
        def my_func():
            pass
    """

    def decorator(func: Callable) -> Callable:
        # Generate or use provided schema
        tool_schema = schema or _schema_from_signature(func)

        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        # Attach metadata
        wrapper._poping_tool = {
            "name": name or func.__name__,
            "description": func.__doc__ or "",
            "input_schema": tool_schema,
            "callable": func,
        }

        return wrapper

    return decorator


def get_tool_definition(obj: Any) -> Optional[Dict[str, Any]]:
    """
    Extract tool definition from decorated callable.

    Args:
        obj: Decorated function, dict, or string

    Returns:
        Tool definition dict or None

    Supports:
        - Decorated function: extracts from _poping_tool attribute
        - Dict: validates and returns
        - String: tool name only (backend must know it)
    """
    # Decorated callable
    if callable(obj) and hasattr(obj, "_poping_tool"):
        data = getattr(obj, "_poping_tool")
        return {
            "name": data["name"],
            "description": data["description"],
            "input_schema": data["input_schema"],
        }

    # Raw dict
    if isinstance(obj, dict) and {"name", "description", "input_schema"} <= set(obj.keys()):
        return {
            "name": obj["name"],
            "description": obj.get("description", ""),
            "input_schema": obj.get("input_schema") or {},
        }

    # Bare name
    if isinstance(obj, str):
        return {"name": obj, "description": obj, "input_schema": {}}

    return None
