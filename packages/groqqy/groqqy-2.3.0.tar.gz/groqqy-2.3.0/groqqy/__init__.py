"""
Groqqy - Micro agentic bot powered by Groq

Fast, cheap, helpful, and extensible.
"""

__version__ = "2.3.0"

# Main bot
from .bot import Groqqy

# Tool system
from .tool import Tool, ToolRegistry, tool, create_default_registry

# Components (for advanced users)
from .components import ConversationManager, ToolExecutor, CostTracker

# Agent (for advanced users)
from .agent import Agent, AgentResult

# Strategies (for advanced users)
from .strategy import (
    ToolExecutionStrategy,
    LocalToolStrategy,
    PlatformToolStrategy,
    HybridToolStrategy,
    detect_strategy
)

# Default tools
from .tools import read_file, run_command, search_files, search_content

__all__ = [
    # Main API
    "Groqqy",

    # Tool system
    "Tool",
    "ToolRegistry",
    "tool",
    "create_default_registry",

    # Components
    "ConversationManager",
    "ToolExecutor",
    "CostTracker",

    # Agent
    "Agent",
    "AgentResult",

    # Strategies
    "ToolExecutionStrategy",
    "LocalToolStrategy",
    "PlatformToolStrategy",
    "HybridToolStrategy",
    "detect_strategy",

    # Default tools
    "read_file",
    "run_command",
    "search_files",
    "search_content",
]
