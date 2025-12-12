"""
Groqqy Configuration Management

Handles ~/.groqqy/ directory and knowledge loading.
"""

from pathlib import Path
from typing import List, Optional


class GroqqyConfig:
    """Manages Groqqy configuration and knowledge loading."""

    def __init__(self):
        """Initialize configuration paths."""
        self.config_dir = Path.home() / ".groqqy"
        self.boot_file = self.config_dir / "boot.md"
        self.knowledge_dir = self.config_dir / "knowledge"

    def ensure_config_exists(self):
        """Create ~/.groqqy directory structure if it doesn't exist."""
        self.config_dir.mkdir(exist_ok=True)
        self.knowledge_dir.mkdir(exist_ok=True)

        # Create default boot.md if it doesn't exist
        if not self.boot_file.exists():
            self._create_default_boot()

    def load_system_instruction(
        self,
        context_files: Optional[List[str]] = None,
        extra_prompt: Optional[str] = None
    ) -> str:
        """
        Load and combine system instruction from:
        1. ~/.groqqy/boot.md (base instruction)
        2. Additional context files (if provided)
        3. Extra prompt (if provided)
        """
        parts = []

        # Load boot.md
        boot_content = self._load_boot()
        if boot_content:
            parts.append(boot_content)

        # Load additional context files
        if context_files:
            for file_path in context_files:
                content = self._load_file(file_path)
                if content:
                    parts.append(f"\n# Additional Context: {file_path}\n\n{content}")

        # Add extra prompt
        if extra_prompt:
            parts.append(f"\n# Additional Instructions\n\n{extra_prompt}")

        # If nothing loaded, use default
        if not parts:
            return self._default_instruction()

        return "\n\n".join(parts)

    def _load_boot(self) -> Optional[str]:
        """Load boot.md if it exists."""
        if self.boot_file.exists():
            return self._load_file(str(self.boot_file))
        return None

    def _load_file(self, file_path: str) -> Optional[str]:
        """Load content from file."""
        try:
            path = Path(file_path)
            if path.exists():
                return path.read_text(encoding='utf-8')
        except Exception as e:
            print(f"Warning: Could not read {file_path}: {e}")
        return None

    def _create_default_boot(self):
        """Create default boot.md with helpful instructions."""
        default_content = """# Groqqy Boot Instructions

You are Groqqy, a helpful AI assistant powered by Groq's fast LLM inference.

## Your Capabilities

You have access to tools for:
- **read_file**: Read contents of files
- **run_command**: Execute shell commands (use carefully!)
- **search_files**: Find files matching patterns
- **search_content**: Search for text in files

## Guidelines

- Keep responses concise and friendly
- Use tools when they help answer the question
- Explain what you're doing when using tools
- If a command might be destructive, ask first
- Provide context with your answers

## Custom Instructions

Add your own instructions below this line:

---


"""
        self.boot_file.write_text(default_content, encoding='utf-8')

    def _default_instruction(self) -> str:
        """Fallback instruction if nothing else loads."""
        return """You are Groqqy, a helpful assistant.
You have access to tools for reading files, running commands, and searching.
Keep responses concise and friendly. Use tools when needed to help the user."""
