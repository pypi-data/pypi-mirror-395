"""
Groqqy Provider Interface - Pure domain contract
No implementation, no I/O, no side effects
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Dict, Any, Optional


@dataclass
class LLMResponse:
    """Standardized LLM response - pure data."""
    text: str
    tool_calls: Optional[List[Dict]] = None
    usage: Optional[Dict] = None


class Provider(ABC):
    """
    Minimal provider interface for agent kernel.

    Pure contract - implementation details hidden.
    Any object implementing these two methods can power Groqqy.
    """

    @abstractmethod
    def chat(self, messages: List[Dict], tools: List = None) -> LLMResponse:
        """Send messages to LLM and get response."""
        pass

    @abstractmethod
    def get_cost(self, usage: Dict) -> float:
        """Calculate cost from usage statistics."""
        pass
