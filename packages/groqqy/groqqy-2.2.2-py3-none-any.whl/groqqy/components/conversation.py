"""
ConversationManager - Manages conversation history

Single responsibility: Message list management
"""

from typing import List, Dict, Any


class ConversationManager:
    """
    Manages conversation message history.

    Provides simple, clear API for adding different message types.
    """

    def __init__(self):
        """Initialize with empty conversation."""
        self._messages: List[Dict[str, Any]] = []

    def add_user(self, message: str):
        """
        Add user message.

        Args:
            message: User's text message
        """
        self._messages.append({
            "role": "user",
            "content": message
        })

    def add_assistant(self, message: str):
        """
        Add assistant message.

        Args:
            message: Assistant's text response
        """
        self._messages.append({
            "role": "assistant",
            "content": message
        })

    def add_tool_calls(self, text: str, tool_calls: List[Dict]):
        """
        Add assistant message with tool calls.

        Args:
            text: Optional text from assistant
            tool_calls: List of tool call objects
        """
        self._messages.append({
            "role": "assistant",
            "content": text or "",
            "tool_calls": tool_calls
        })

    def add_tool_result(self, tool_call_id: str, result: str):
        """
        Add tool execution result.

        Args:
            tool_call_id: ID of the tool call
            result: String result from tool execution
        """
        self._messages.append({
            "role": "tool",
            "tool_call_id": tool_call_id,
            "content": result
        })

    def get_history(self) -> List[Dict[str, Any]]:
        """
        Get full conversation history.

        Returns:
            List of message dictionaries
        """
        return self._messages

    def reset(self):
        """Clear all messages."""
        self._messages = []

    def __len__(self) -> int:
        """Return number of messages."""
        return len(self._messages)

    def __repr__(self) -> str:
        """String representation."""
        return f"ConversationManager({len(self._messages)} messages)"
