"""
CostTracker - Tracks API costs

Single responsibility: Cost accumulation and reporting
"""

import time
from typing import List, Dict, Any


class CostTracker:
    """
    Tracks API costs across calls.

    Maintains running total and per-call history.
    """

    def __init__(self):
        """Initialize with zero cost."""
        self._total = 0.0
        self._calls: List[Dict[str, Any]] = []

    def add(self, cost: float, metadata: Dict[str, Any] = None):
        """
        Add cost from an API call.

        Args:
            cost: Cost in dollars
            metadata: Optional metadata (iteration, model, etc.)
        """
        self._total += cost
        self._calls.append({
            "cost": cost,
            "timestamp": time.time(),
            **(metadata or {})
        })

    def get_total(self) -> float:
        """
        Get total accumulated cost.

        Returns:
            Total cost in dollars
        """
        return self._total

    def get_history(self) -> List[Dict[str, Any]]:
        """
        Get full cost history.

        Returns:
            List of cost records with metadata
        """
        return self._calls

    def get_call_count(self) -> int:
        """
        Get number of API calls made.

        Returns:
            Number of calls
        """
        return len(self._calls)

    def reset(self):
        """Reset cost and history."""
        self._total = 0.0
        self._calls = []

    def __repr__(self) -> str:
        """String representation."""
        return f"CostTracker(${self._total:.6f}, {len(self._calls)} calls)"
