"""
ToolExecutor - Executes tools from registry

Single responsibility: Tool execution with error handling
"""

import json
import time
from typing import Dict, List, Tuple, Any, Optional

from ..tool import ToolRegistry
from ..log import get_logger


class ToolExecutor:
    """
    Executes tools from a registry.

    Handles execution, error handling, and logging.
    """

    def __init__(self, registry: ToolRegistry, logger=None):
        """
        Initialize executor.

        Args:
            registry: ToolRegistry containing available tools
            logger: Optional logger (creates one if not provided)
        """
        self.registry = registry
        self.log = logger or get_logger("executor")

    def execute(self, tool_call: Dict[str, Any]) -> str:
        """
        Execute a single tool call.

        Args:
            tool_call: Tool call object with 'function' containing
                'name' and 'arguments'

        Returns:
            String result from tool execution (or error message)
        """
        name = tool_call['function']['name']
        args_json = tool_call['function']['arguments']

        # Parse arguments
        try:
            args = json.loads(args_json)
        except json.JSONDecodeError as e:
            error_msg = f"Error parsing arguments for {name}: {e}"
            self.log.error("Argument parsing failed", tool=name, error=str(e))
            return error_msg

        # Get tool
        tool = self.registry.get(name)
        if not tool:
            error_msg = f"Error: Tool '{name}' not found"
            self.log.error("Tool not found", tool=name)
            return error_msg

        # Execute tool
        start = time.time()

        # Create human-readable description of what's being executed
        if name == "run_command" and "command" in args:
            exec_desc = f"{name}('{args['command']}')"
        else:
            # Show first few args for other tools
            arg_items = list(args.items())[:2]
            arg_preview = ", ".join(f"{k}={repr(v)[:50]}" for k, v in arg_items)
            exec_desc = f"{name}({arg_preview})"

        self.log.info("Executing tool", tool=exec_desc)
        self.log.debug("Tool execution started", tool=name, args=args)

        try:
            result = tool.execute(**args)
            result_str = str(result)

            elapsed_ms = (time.time() - start) * 1000
            if len(result_str) > 100:
                result_preview = result_str[:100] + "..."
            else:
                result_preview = result_str

            self.log.info("Tool execution succeeded",
                         tool=name,
                         duration_ms=round(elapsed_ms, 2),
                         result_length=len(result_str),
                         result_preview=result_preview)

            return result_str

        except Exception as e:
            error_msg = f"Error executing {name}: {e}"
            elapsed_ms = (time.time() - start) * 1000

            self.log.error("Tool execution failed",
                          tool=name,
                          duration_ms=round(elapsed_ms, 2),
                          error=str(e),
                          error_type=type(e).__name__)

            return error_msg

    def execute_all(self, tool_calls: List[Dict]) -> List[Tuple[str, str]]:
        """
        Execute multiple tool calls.

        Args:
            tool_calls: List of tool call objects

        Returns:
            List of (tool_call_id, result) tuples
        """
        return [
            (tc['id'], self.execute(tc))
            for tc in tool_calls
        ]
