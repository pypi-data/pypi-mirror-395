"""
Groqqy - Micro agentic bot (facade over Agent)

Clean API over composable components:
- Agent: Agentic loop (think/act/observe)
- Provider: LLM backend
- ToolRegistry: Available tools
"""

import uuid
from typing import Optional, List, Dict, Any

from .providers.groq import GroqProvider
from .agent import Agent
from .tool import ToolRegistry, create_default_registry
from .log import get_logger
from .components.exporter import ConversationExporter

# Sentinel for distinguishing "not provided" from "explicitly None"
_USE_DEFAULTS = object()


class Groqqy:
    """
    Simple micro agentic bot powered by Groq.

    Features:
    - Multi-step reasoning (agent loop)
    - Tool chaining
    - Extensible tool registry
    - Clean, composable architecture

    This is a thin facade - all heavy lifting done by Agent.
    """

    def __init__(
        self,
        model: str = "llama-3.1-8b-instant",
        tools: Optional[ToolRegistry] = _USE_DEFAULTS,
        system_instruction: Optional[str] = None,
        max_iterations: int = 10,
        temperature: float = 0.5,
        top_p: float = 0.65
    ):
        """
        Initialize Groqqy.

        Args:
            model: Groq model name
            tools: ToolRegistry, None to disable tools, or omit for defaults
            system_instruction: Custom system prompt (uses default if not provided)
            max_iterations: Maximum agent loop iterations
            temperature: Sampling temperature (0.0-2.0, default 0.5 for tool calling)
            top_p: Nucleus sampling parameter (0.0-1.0, default 0.65 for tool calling)
        """
        # Session tracking
        self.session_id = str(uuid.uuid4())[:8]
        self.log = get_logger("groqqy").bind(
            session_id=self.session_id,
            model=model
        )

        # Provider (LLM backend)
        self.provider = GroqProvider(
            model=model,
            system_instruction=system_instruction or self._default_instruction(),
            temperature=temperature,
            top_p=top_p
        )

        # Tool registry (distinguish None from omitted for backwards compat)
        if tools is _USE_DEFAULTS:
            # Parameter omitted - use defaults (backwards compatible)
            self.tools = create_default_registry()
        elif tools is None:
            # Explicitly None - disable tools (--no-tools mode)
            self.tools = None
        else:
            # Custom ToolRegistry provided
            self.tools = tools

        # Agent (does the heavy lifting)
        self.agent = Agent(
            provider=self.provider,
            tools=self.tools,
            max_iterations=max_iterations,
            logger=self.log
        )

        tool_info = {}
        if self.tools is not None:
            tool_info = {
                "tool_count": len(self.tools),
                "tools": self.tools.list_names()
            }
        else:
            tool_info = {
                "tool_count": 0,
                "tools": []
            }

        self.log.info("Groqqy initialized",
                     **tool_info,
                     max_iterations=max_iterations,
                     has_custom_instruction=bool(system_instruction))

    def chat(self, user_message: str) -> tuple[str, float]:
        """
        Send message and get response.

        Runs the full agent loop:
        - Can use tools multiple times
        - Can chain tool calls
        - Multi-step reasoning

        Args:
            user_message: User's input

        Returns:
            (response_text, cost) tuple
        """
        self.log.debug("Chat started",
                      message_length=len(user_message),
                      message_preview=user_message[:100])

        result = self.agent.run(user_message)

        self.log.info("Chat completed",
                     iterations=result.iterations,
                     tool_calls=result.tool_calls_made,
                     cost=result.total_cost,
                     total_cost=self.total_cost)

        return result.response, result.total_cost

    def reset(self):
        """Reset conversation history and cost tracking."""
        prev_turns = len(self.agent.conversation)
        prev_cost = self.agent.tracker.get_total()

        self.agent.reset()

        self.log.info("Conversation reset",
                     previous_turns=prev_turns,
                     previous_cost=prev_cost)

    # ========================================================================
    # Properties (for backwards compatibility)
    # ========================================================================

    @property
    def total_cost(self) -> float:
        """Get total accumulated cost."""
        return self.agent.tracker.get_total()

    @property
    def conversation(self) -> List[Dict[str, Any]]:
        """Get conversation history."""
        return self.agent.conversation.get_history()

    # ========================================================================
    # Helpers
    # ========================================================================

    def export_markdown(self) -> str:
        """
        Export current conversation to Markdown format.

        Returns:
            Markdown-formatted conversation string
        """
        exporter = ConversationExporter(self.conversation)
        return exporter.to_markdown()

    def export_html(self, include_css: bool = True) -> str:
        """
        Export current conversation to HTML format.

        Args:
            include_css: Include embedded CSS styling

        Returns:
            HTML-formatted conversation string
        """
        exporter = ConversationExporter(self.conversation)
        return exporter.to_html(include_css=include_css)

    def save_conversation(self, filepath: str, format: str = "markdown"):
        """
        Save conversation to file.

        Args:
            filepath: Path to save file
            format: Export format - "markdown" or "html"
        """
        if format.lower() == "markdown":
            content = self.export_markdown()
        elif format.lower() == "html":
            content = self.export_html()
        else:
            raise ValueError(f"Unsupported format: {format}. Use 'markdown' or 'html'")

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

        self.log.info("Conversation exported",
                     filepath=filepath,
                     format=format,
                     message_count=len(self.conversation))

    def _default_instruction(self) -> str:
        """Return default system instruction."""
        return """You are Groqqy, a helpful assistant.
You have access to tools for reading files, running commands, and searching.
Keep responses concise and friendly. Use tools when needed to help the user."""
