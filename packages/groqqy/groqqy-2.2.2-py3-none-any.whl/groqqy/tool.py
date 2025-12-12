"""
Tool Registry System - Dynamic, extensible tool management

Provides:
- Tool class: Function + metadata
- ToolRegistry: Dynamic registration and discovery
- @tool decorator: Easy tool creation
"""

from dataclasses import dataclass
from typing import Callable, Dict, Any, List, Optional


@dataclass
class Tool:
    """
    A tool that agents can use.

    Combines function implementation with metadata for LLM.
    """
    name: str
    description: str
    function: Callable
    parameters: Dict[str, Any]  # JSON schema

    @classmethod
    def from_function(cls, func: Callable, description: str = None) -> 'Tool':
        """
        Create tool from function using introspection.

        Args:
            func: Python function to wrap
            description: Human-readable description (uses docstring if not provided)

        Returns:
            Tool instance with auto-generated schema
        """
        from .utils import build_tool_schema

        schema = build_tool_schema(func)

        return cls(
            name=func.__name__,
            description=description or func.__doc__ or "",
            function=func,
            parameters=schema['function']['parameters']
        )

    def to_schema(self) -> Dict[str, Any]:
        """Convert to OpenAI tool schema format."""
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.parameters
            }
        }

    def execute(self, **kwargs) -> Any:
        """Execute the tool with given arguments."""
        return self.function(**kwargs)


class ToolRegistry:
    """
    Registry for managing available tools.

    Provides dynamic registration, discovery, and schema generation.
    Supports both local function-based tools and platform tools.
    """

    def __init__(self):
        """Initialize empty registry."""
        self._tools: Dict[str, Tool] = {}
        # Platform tools (e.g., browser_search)
        self._platform_tools: List[Dict[str, Any]] = []

    def register(self, tool: Tool):
        """
        Register a tool.

        Args:
            tool: Tool instance to register
        """
        self._tools[tool.name] = tool

    def register_function(self, func: Callable, description: str = None):
        """
        Register a function as a tool (convenience method).

        Args:
            func: Function to register
            description: Optional description (uses docstring if not provided)
        """
        tool = Tool.from_function(func, description)
        self.register(tool)

    def register_platform_tool(self, tool_type: str):
        """
        Register a platform tool (executes on LLM provider's servers).

        Platform tools like browser_search, web_search execute server-side
        and don't require local function implementations.

        Args:
            tool_type: Type of platform tool (e.g., "browser_search", "web_search")

        Example:
            registry.register_platform_tool("browser_search")
        """
        self._platform_tools.append({"type": tool_type})

    def get(self, name: str) -> Optional[Tool]:
        """
        Get tool by name.

        Args:
            name: Tool name

        Returns:
            Tool instance or None if not found
        """
        return self._tools.get(name)

    def list_all(self) -> List[Tool]:
        """
        List all registered tools.

        Returns:
            List of all Tool instances
        """
        return list(self._tools.values())

    def list_names(self) -> List[str]:
        """
        List all tool names.

        Returns:
            List of tool name strings
        """
        return list(self._tools.keys())

    def to_schemas(self) -> List[Dict[str, Any]]:
        """
        Convert all tools to OpenAI tool schemas.

        Returns both function-based tools and platform tools.

        Returns:
            List of tool schemas for LLM API
        """
        schemas = [tool.to_schema() for tool in self._tools.values()]
        schemas.extend(self._platform_tools)
        return schemas

    def __len__(self) -> int:
        """Return number of registered tools."""
        return len(self._tools)

    def __contains__(self, name: str) -> bool:
        """Check if tool is registered."""
        return name in self._tools

    def __repr__(self) -> str:
        """String representation."""
        return f"ToolRegistry({len(self._tools)} tools: {self.list_names()})"


def tool(description: str = None):
    """
    Decorator to mark a function as a tool.

    Usage:
        @tool(description="Read a file")
        def read_file(path: str) -> str:
            return open(path).read()

    Args:
        description: Human-readable description

    Note: Decorator just marks the function. You still need to register it
          with a ToolRegistry manually.
    """
    def decorator(func: Callable) -> Callable:
        # Store metadata on function for later registration
        func._tool_description = description or func.__doc__ or ""
        func._is_tool = True
        return func
    return decorator


def create_default_registry() -> ToolRegistry:
    """
    Create registry with default tools.

    Returns:
        ToolRegistry with read_file, run_command, search_files, search_content
    """
    from .tools import read_file, run_command, search_files, search_content

    registry = ToolRegistry()

    registry.register_function(
        read_file,
        "Read and return the contents of a file"
    )
    registry.register_function(
        run_command,
        "Execute a shell command and return output (use with caution!)"
    )
    registry.register_function(
        search_files,
        "Find files matching a pattern in a directory"
    )
    registry.register_function(
        search_content,
        "Search for text content in files"
    )

    return registry
