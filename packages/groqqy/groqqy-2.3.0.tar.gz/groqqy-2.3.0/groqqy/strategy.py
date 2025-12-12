"""
Tool Execution Strategies

This module defines how tools are executed in the agentic loop.

WHY THIS EXISTS:
    Different tools execute in different ways:
    - Local tools (read_file, run_command) execute on your machine
    - Platform tools (browser_search, web_search) execute on Groq's servers
    - Hybrid systems use both types together

    The Strategy Pattern lets us handle all these cases without changing
    the core Agent loop.

ARCHITECTURE:
    ToolExecutionStrategy (abstract)
        ├── LocalToolStrategy      - For function-based tools
        ├── PlatformToolStrategy   - For server-executed tools
        └── HybridToolStrategy     - Mix of both

TEACHING POINTS:
    1. Strategy Pattern - swap execution behavior at runtime
    2. Open/Closed Principle - extend without modifying Agent
    3. Separation of Concerns - Agent doesn't know HOW tools execute
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
from dataclasses import dataclass


@dataclass
class ExecutionResult:
    """Result of handling an LLM response."""
    needs_continuation: bool  # Should agent continue the loop?
    content: Optional[str] = None  # Final response content
    tool_calls: Optional[List[Dict]] = None  # Tools to execute locally


class ToolExecutionStrategy(ABC):
    """
    Abstract strategy for tool execution.

    Determines:
    - Whether tools need local execution
    - How to handle LLM responses based on tool types
    - When the agentic loop should continue vs stop
    """

    @abstractmethod
    def handle_response(self, response, tools: List[Dict]) -> ExecutionResult:
        """
        Process LLM response based on tool execution model.

        Args:
            response: LLM response object (has .tool_calls, .content)
            tools: List of tool schemas provided to LLM

        Returns:
            ExecutionResult indicating what to do next
        """
        pass

    def describe(self) -> str:
        """Human-readable description of this strategy."""
        return self.__class__.__name__


class LocalToolStrategy(ToolExecutionStrategy):
    """
    Strategy for function-based tools that execute locally.

    Examples: read_file, run_command, search_files, custom functions

    Flow:
        LLM returns tool_calls → Execute locally → Feed results back to LLM
        LLM returns no tool_calls → Done
    """

    def handle_response(self, response, tools: List[Dict]) -> ExecutionResult:
        """
        Check if LLM wants to call tools.

        If tool_calls present: Agent should execute them
        If no tool_calls: Task complete
        """
        if response.tool_calls:
            return ExecutionResult(
                needs_continuation=True,
                tool_calls=response.tool_calls
            )

        # No tools requested, we're done
        return ExecutionResult(
            needs_continuation=False,
            content=response.text
        )


class PlatformToolStrategy(ToolExecutionStrategy):
    """
    Strategy for platform tools that execute server-side.

    Examples: browser_search, web_search (Groq Compound)

    Flow:
        Tools execute on Groq's servers
        Results appear directly in response.content
        No tool_calls in response (already executed)

    Note:
        Platform tools are declared upfront but don't return tool_calls.
        The execution happens transparently on the server.
    """

    def handle_response(self, response, tools: List[Dict]) -> ExecutionResult:
        """
        Platform tools execute server-side, no local execution needed.

        Response content contains the final result.
        """
        # Platform tools execute on server, no tool_calls expected
        return ExecutionResult(
            needs_continuation=False,
            content=response.text
        )


class HybridToolStrategy(ToolExecutionStrategy):
    """
    Strategy for mixing local and platform tools.

    Examples: browser_search + read_file in same agent

    Flow:
        - Platform tools execute server-side first
        - Then LLM may call local tools
        - Or may be done after platform tool

    This is the most flexible strategy but requires careful handling:
    - Check if response has tool_calls (local tools need execution)
    - If no tool_calls, platform tools may have executed or task complete
    """

    def __init__(self):
        self.local = LocalToolStrategy()
        self.platform = PlatformToolStrategy()

    def handle_response(self, response, tools: List[Dict]) -> ExecutionResult:
        """
        Handle mixed tool types intelligently.

        Decision logic:
        1. If tool_calls present → local tools need execution
        2. If no tool_calls → platform tool executed OR task done
        """
        # Classify tools
        platform_tools = [t for t in tools if self._is_platform_tool(t)]
        local_tools = [t for t in tools if not self._is_platform_tool(t)]

        # If LLM called local tools, execute them
        if response.tool_calls:
            return self.local.handle_response(response, local_tools)

        # No tool_calls - either platform tool executed or done
        # Platform tools don't return tool_calls (executed server-side)
        return ExecutionResult(
            needs_continuation=False,
            content=response.text
        )

    def _is_platform_tool(self, tool: Dict) -> bool:
        """Check if tool is a platform tool (server-executed)."""
        return tool.get("type") in ["browser_search", "web_search"]


def detect_strategy(tools: List[Dict]) -> ToolExecutionStrategy:
    """
    Auto-detect the appropriate strategy based on tool types.

    Args:
        tools: List of tool schemas

    Returns:
        Appropriate strategy for the tool mix

    Examples:
        >>> detect_strategy([{"type": "function", ...}])
        LocalToolStrategy()

        >>> detect_strategy([{"type": "browser_search"}])
        PlatformToolStrategy()

        >>> detect_strategy([{"type": "function", ...}, {"type": "browser_search"}])
        HybridToolStrategy()
    """
    if not tools:
        return LocalToolStrategy()  # Default

    has_platform = any(t.get("type") in ["browser_search", "web_search"] for t in tools)
    has_local = any(t.get("type") == "function" for t in tools)

    if has_platform and has_local:
        return HybridToolStrategy()
    elif has_platform:
        return PlatformToolStrategy()
    else:
        return LocalToolStrategy()
