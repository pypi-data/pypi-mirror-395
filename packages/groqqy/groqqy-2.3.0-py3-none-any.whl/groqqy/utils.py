"""Utility functions for converting Python functions to OpenAI tool schemas"""

import inspect
import typing
from typing import Callable, Dict, Any


def build_tool_schema(tool: Callable) -> Dict[str, Any]:
    """Convert Python function to OpenAI tool schema via introspection."""
    sig = inspect.signature(tool)
    parameters = _build_parameters(sig, tool)

    return {
        "type": "function",
        "function": {
            "name": tool.__name__,
            "description": tool.__doc__ or f"{tool.__name__} function",
            "parameters": parameters
        }
    }


def _build_parameters(sig: inspect.Signature, tool: Callable) -> Dict[str, Any]:
    properties = {}
    required = []

    for param_name, param in sig.parameters.items():
        properties[param_name] = _param_to_schema(param)
        if _is_required(param):
            required.append(param_name)

    return {
        "type": "object",
        "properties": properties,
        "required": required
    }


def _param_to_schema(param: inspect.Parameter) -> Dict[str, str]:
    param_type = _map_type(param.annotation)
    return {
        "type": param_type,
        "description": f"{param.name} parameter"
    }


def _is_required(param: inspect.Parameter) -> bool:
    return param.default == inspect.Parameter.empty


def _map_type(annotation) -> str:
    """Map Python type annotations to OpenAI JSON schema types."""
    if annotation == inspect.Parameter.empty:
        return "string"

    # Handle Optional[T] and Union[T, None]
    origin = typing.get_origin(annotation)
    if origin is typing.Union:
        args = typing.get_args(annotation)
        # Filter out NoneType
        non_none_args = [arg for arg in args if arg is not type(None)]
        if len(non_none_args) == 1:
            # This is Optional[T] - recursively map the inner type
            return _map_type(non_none_args[0])
        # Multiple non-None types in Union - can't represent simply
        return "string"  # Conservative fallback

    # Handle List[T], Dict[K,V] generic types
    if origin is list:
        return "array"
    if origin is dict:
        return "object"

    # Basic type mapping
    type_map = {
        str: "string",
        int: "integer",
        float: "number",
        bool: "boolean",
        list: "array",
        dict: "object"
    }

    return type_map.get(annotation, "string")
