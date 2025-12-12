"""
Simple logging for Groqqy - JSONL logs with rotation.

Usage:
    from groqqy.log import log

    log.info("Message", key=value)
    log.debug("Detail", data=some_value)
    log.error("Problem", error=str(e))

Configuration (via environment variables):
    LOG_LEVEL=DEBUG    # Set verbosity (DEBUG, INFO, WARNING, ERROR)
    LOG_DIR=./logs     # Log directory (default: ./logs)

Features:
    - JSONL format (one JSON per line, grep-friendly)
    - Weekly rotation with gzip compression
    - 3-week retention (auto-delete old logs)
    - Colored console output in development
    - Structured logging (key-value pairs)

Example:
    from groqqy.log import log

    # Simple logging
    log.info("Chat started", user_id=123)

    # Bind context (follows through all subsequent logs)
    session_log = log.bind(session_id="abc123", model="llama-3.1-8b")
    session_log.info("Processing")  # Includes session_id and model
    session_log.debug("Detail", tokens=142)  # Also includes context

Searching logs:
    # Simple grep
    grep '"session_id": "abc123"' logs/groqqy.jsonl

    # Powerful jq
    cat logs/groqqy.jsonl | jq -r 'select(.record.level.name == "ERROR")'
    cat logs/groqqy.jsonl | jq -r 'select(.record.extra.cost > 0.001)'
"""

from loguru import logger
import sys
from pathlib import Path
import os

# ============================================================================
# One-time setup (happens on import)
# ============================================================================

# Remove default handler
logger.remove()

# Get configuration from environment
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
LOG_DIR = Path(os.getenv("LOG_DIR", "./logs"))

# Ensure log directory exists
LOG_DIR.mkdir(exist_ok=True, parents=True)

# ============================================================================
# Console output (human-readable, colorized for development)
# ============================================================================

def console_formatter(record):
    """Custom formatter that includes tool info."""
    base = (
        "<green>{time:HH:mm:ss}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{extra[component]}</cyan> | "
        "<level>{message}</level>"
    )

    # Add tool info if present
    if "tool" in record["extra"]:
        base += " | <yellow>tool={extra[tool]}</yellow>"

    # Add result info if present
    if "result_length" in record["extra"]:
        base += " | <blue>{extra[result_length]} chars</blue>"

    # Add duration if present
    if "duration_ms" in record["extra"]:
        base += " | <magenta>{extra[duration_ms]:.0f}ms</magenta>"

    return base + "\n"

logger.add(
    sys.stderr,
    level=LOG_LEVEL,
    format=console_formatter,
    colorize=True,
    # Only log if component is set
    filter=lambda record: "component" in record["extra"],
)

# ============================================================================
# File output (JSONL format with rotation and compression)
# ============================================================================

logger.add(
    LOG_DIR / "groqqy.jsonl",
    level=LOG_LEVEL,
    serialize=True,        # Output as JSON (one per line)
    rotation="1 week",     # Rotate weekly
    retention="3 weeks",   # Keep 3 weeks of logs
    compression="gz",      # Compress rotated logs (saves ~90% space)
    enqueue=True,          # Thread-safe async logging
    backtrace=True,        # Include full trace on errors
    diagnose=True,         # Detailed error diagnostics
)

# ============================================================================
# Export configured logger with default component binding
# ============================================================================

# Default logger with component tag
log = logger.bind(component="groqqy")

# ============================================================================
# Optional: Helper to get component-specific logger
# ============================================================================

def get_logger(component: str):
    """
    Get a logger with specific component tag.

    Usage:
        bot_log = get_logger("bot")
        bot_log.info("Bot started")

        tools_log = get_logger("tools")
        tools_log.debug("Tool executed", tool="read_file")

    Args:
        component: Component name (e.g. "bot", "tools", "provider")

    Returns:
        Logger bound to component
    """
    return logger.bind(component=component)
