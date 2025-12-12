"""
ConversationExporter - Export conversations to various formats

Single responsibility: Transform conversation history into readable formats
"""

from typing import List, Dict, Any
from datetime import datetime
import json


class ConversationExporter:
    """
    Exports conversation history to markdown and HTML formats.

    Handles:
    - User messages
    - Assistant messages (with and without tool calls)
    - Tool execution results
    - Formatting and styling
    """

    def __init__(self, conversation_history: List[Dict[str, Any]]):
        """
        Initialize exporter with conversation history.

        Args:
            conversation_history: List of message dictionaries
        """
        self.history = conversation_history
        self.timestamp = datetime.now()

    def to_markdown(self) -> str:
        """
        Export conversation to Markdown format.

        Returns:
            Markdown-formatted conversation string
        """
        lines = []

        # Header
        lines.append("# Groqqy Conversation")
        lines.append(f"\n**Date**: {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append(f"**Messages**: {len(self.history)}")
        lines.append("\n---\n")

        # Process each message
        for i, msg in enumerate(self.history, 1):
            role = msg.get("role", "unknown")

            if role == "user":
                lines.append(f"## Message {i}: User\n")
                lines.append(f"{msg.get('content', '')}\n")

            elif role == "assistant":
                lines.append(f"## Message {i}: Assistant\n")

                # Check for tool calls
                tool_calls = msg.get("tool_calls", [])
                if tool_calls:
                    lines.append("**Tool Calls:**\n")
                    for tc in tool_calls:
                        func = tc.get("function", {})
                        lines.append(f"- **{func.get('name', 'unknown')}**")

                        # Pretty print arguments
                        args = func.get("arguments", "{}")
                        try:
                            if isinstance(args, str):
                                args_dict = json.loads(args)
                            else:
                                args_dict = args
                            lines.append("  ```json")
                            lines.append(f"  {json.dumps(args_dict, indent=2)}")
                            lines.append("  ```")
                        except (json.JSONDecodeError, TypeError, AttributeError):
                            lines.append(f"  ```\n  {args}\n  ```")
                    lines.append("")

                # Assistant content
                content = msg.get("content", "")
                if content:
                    lines.append(f"{content}\n")

            elif role == "tool":
                lines.append(f"## Message {i}: Tool Result\n")
                tool_call_id = msg.get('tool_call_id', 'unknown')
                lines.append(f"**Tool Call ID**: `{tool_call_id}`\n")
                lines.append("**Result:**\n")
                lines.append("```")
                lines.append(msg.get("content", ""))
                lines.append("```\n")

            else:
                lines.append(f"## Message {i}: {role.title()}\n")
                lines.append(f"{msg.get('content', '')}\n")

        lines.append("\n---\n")
        timestamp_str = self.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        lines.append(f"*Exported by Groqqy on {timestamp_str}*\n")

        return "\n".join(lines)

    def to_html(self, include_css: bool = True) -> str:
        """
        Export conversation to HTML format with styling.

        Args:
            include_css: Include embedded CSS styling

        Returns:
            HTML-formatted conversation string
        """
        html_parts = []

        # HTML header
        html_parts.append("<!DOCTYPE html>")
        html_parts.append("<html lang='en'>")
        html_parts.append("<head>")
        html_parts.append("  <meta charset='UTF-8'>")
        viewport = (
            "  <meta name='viewport' "
            "content='width=device-width, initial-scale=1.0'>"
        )
        html_parts.append(viewport)
        html_parts.append("  <title>Groqqy Conversation</title>")

        if include_css:
            html_parts.append(self._get_css())

        html_parts.append("</head>")
        html_parts.append("<body>")

        # Header
        html_parts.append("  <div class='container'>")
        html_parts.append("    <header>")
        html_parts.append("      <h1>🤖 Groqqy Conversation</h1>")
        html_parts.append(f"      <div class='meta'>")
        timestamp_str = self.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        html_parts.append(f"        <span>📅 {timestamp_str}</span>")
        html_parts.append(f"        <span>💬 {len(self.history)} messages</span>")
        html_parts.append(f"      </div>")
        html_parts.append("    </header>")

        # Messages
        html_parts.append("    <div class='conversation'>")

        for i, msg in enumerate(self.history, 1):
            role = msg.get("role", "unknown")

            if role == "user":
                html_parts.append(f"      <div class='message user'>")
                html_parts.append(f"        <div class='message-header'>👤 User</div>")
                html_parts.append(f"        <div class='message-content'>")
                user_content = self._escape_html(msg.get('content', ''))
                html_parts.append(f"          {user_content}")
                html_parts.append(f"        </div>")
                html_parts.append(f"      </div>")

            elif role == "assistant":
                html_parts.append(f"      <div class='message assistant'>")
                header = "        <div class='message-header'>🤖 Assistant</div>"
                html_parts.append(header)

                # Tool calls
                tool_calls = msg.get("tool_calls", [])
                if tool_calls:
                    html_parts.append(f"        <div class='tool-calls'>")
                    tool_header = (
                        "          <div class='tool-calls-header'>"
                        "🔧 Tool Calls:</div>"
                    )
                    html_parts.append(tool_header)
                    for tc in tool_calls:
                        func = tc.get("function", {})
                        func_name = func.get("name", "unknown")
                        html_parts.append(f"          <div class='tool-call'>")
                        tool_name_div = (
                            f"            <div class='tool-name'>"
                            f"{func_name}</div>"
                        )
                        html_parts.append(tool_name_div)

                        # Arguments
                        args = func.get("arguments", "{}")
                        try:
                            if isinstance(args, str):
                                args_dict = json.loads(args)
                            else:
                                args_dict = args
                            args_json = json.dumps(args_dict, indent=2)
                        except (json.JSONDecodeError, TypeError, AttributeError):
                            args_json = str(args)

                        escaped_args = self._escape_html(args_json)
                        args_pre = (
                            f"            <pre class='tool-args'>"
                            f"{escaped_args}</pre>"
                        )
                        html_parts.append(args_pre)
                        html_parts.append(f"          </div>")
                    html_parts.append(f"        </div>")

                # Content
                content = msg.get("content", "")
                if content:
                    html_parts.append(f"        <div class='message-content'>")
                    html_parts.append(f"          {self._escape_html(content)}")
                    html_parts.append(f"        </div>")

                html_parts.append(f"      </div>")

            elif role == "tool":
                html_parts.append(f"      <div class='message tool'>")
                tool_header = "        <div class='message-header'>⚙️ Tool Result</div>"
                html_parts.append(tool_header)
                tool_id = msg.get('tool_call_id', 'unknown')
                html_parts.append(f"        <div class='tool-id'>ID: {tool_id}</div>")
                tool_content = self._escape_html(msg.get('content', ''))
                result_pre = (
                    f"        <pre class='tool-result'>{tool_content}</pre>"
                )
                html_parts.append(result_pre)
                html_parts.append(f"      </div>")

            else:
                html_parts.append(f"      <div class='message other'>")
                role_header = (
                    f"        <div class='message-header'>"
                    f"{role.title()}</div>"
                )
                html_parts.append(role_header)
                other_content = self._escape_html(msg.get('content', ''))
                msg_content_div = (
                    f"        <div class='message-content'>"
                    f"{other_content}</div>"
                )
                html_parts.append(msg_content_div)
                html_parts.append(f"      </div>")

        html_parts.append("    </div>")

        # Footer
        html_parts.append("    <footer>")
        footer_time = self.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        html_parts.append(f"      <p>Exported by Groqqy on {footer_time}</p>")
        html_parts.append("    </footer>")
        html_parts.append("  </div>")

        html_parts.append("</body>")
        html_parts.append("</html>")

        return "\n".join(html_parts)

    def _get_css(self) -> str:
        """Generate embedded CSS styles."""
        return """  <style>
    * {
      margin: 0;
      padding: 0;
      box-sizing: border-box;
    }

    body {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto,
                   'Helvetica Neue', Arial, sans-serif;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      padding: 20px;
      line-height: 1.6;
    }

    .container {
      max-width: 900px;
      margin: 0 auto;
      background: white;
      border-radius: 12px;
      box-shadow: 0 10px 40px rgba(0,0,0,0.2);
      overflow: hidden;
    }

    header {
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      color: white;
      padding: 30px;
      text-align: center;
    }

    header h1 {
      font-size: 2em;
      margin-bottom: 10px;
    }

    .meta {
      display: flex;
      justify-content: center;
      gap: 20px;
      font-size: 0.9em;
      opacity: 0.9;
    }

    .conversation {
      padding: 30px;
    }

    .message {
      margin-bottom: 25px;
      border-radius: 8px;
      padding: 20px;
      border-left: 4px solid;
    }

    .message.user {
      background: #e3f2fd;
      border-left-color: #2196f3;
    }

    .message.assistant {
      background: #f3e5f5;
      border-left-color: #9c27b0;
    }

    .message.tool {
      background: #fff3e0;
      border-left-color: #ff9800;
    }

    .message.other {
      background: #f5f5f5;
      border-left-color: #9e9e9e;
    }

    .message-header {
      font-weight: bold;
      font-size: 1.1em;
      margin-bottom: 12px;
      color: #333;
    }

    .message-content {
      color: #555;
      white-space: pre-wrap;
      word-wrap: break-word;
    }

    .tool-calls {
      background: rgba(0,0,0,0.03);
      border-radius: 6px;
      padding: 15px;
      margin-bottom: 15px;
    }

    .tool-calls-header {
      font-weight: bold;
      margin-bottom: 10px;
      color: #666;
    }

    .tool-call {
      background: white;
      border-radius: 4px;
      padding: 12px;
      margin-bottom: 8px;
      border: 1px solid rgba(0,0,0,0.1);
    }

    .tool-name {
      font-weight: bold;
      color: #9c27b0;
      margin-bottom: 8px;
    }

    .tool-args, .tool-result {
      background: #2d2d2d;
      color: #f8f8f2;
      padding: 12px;
      border-radius: 4px;
      overflow-x: auto;
      font-family: 'Courier New', Courier, monospace;
      font-size: 0.9em;
    }

    .tool-id {
      font-size: 0.85em;
      color: #666;
      margin-bottom: 10px;
      font-family: monospace;
    }

    footer {
      background: #f5f5f5;
      padding: 20px;
      text-align: center;
      color: #666;
      font-size: 0.9em;
      border-top: 1px solid #e0e0e0;
    }
  </style>"""

    def _escape_html(self, text: str) -> str:
        """Escape HTML special characters."""
        return (text
                .replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;")
                .replace('"', "&quot;")
                .replace("'", "&#39;"))
