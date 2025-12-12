"""
Tools that Groqqy can use
"""

import subprocess
import shlex
from pathlib import Path
from typing import Optional


def read_file(file_path: str, start_line: Optional[int] = None,
              end_line: Optional[int] = None) -> str:
    """
    Read and return contents of a file.

    Args:
        file_path: Path to file
        start_line: Starting line number (1-indexed), None = from beginning
        end_line: Ending line number (inclusive), None = to end

    Returns:
        File contents or specified line range

    Examples:
        read_file("file.txt")              # Full file
        read_file("file.txt", 10, 20)      # Lines 10-20
        read_file("file.txt", start_line=50)  # From line 50 to end
        read_file("file.txt", end_line=100)   # First 100 lines
    """
    try:
        with open(file_path, 'r') as f:
            # Fast path for full file read
            if start_line is None and end_line is None:
                return f.read()

            # Line range reading
            lines = f.readlines()
            start = (start_line - 1) if start_line else 0
            end = end_line if end_line else len(lines)

            # Validate bounds
            if start < 0:
                start = 0
            if end > len(lines):
                end = len(lines)

            return ''.join(lines[start:end])
    except FileNotFoundError:
        return f"Error: File not found: {file_path}"
    except Exception as e:
        return f"Error reading file: {e}"


def run_command(command: str) -> str:
    """
    Execute a shell command and return output.

    WARNING: This executes arbitrary shell commands. Use with caution.
    The LLM has full shell access through this tool.
    """
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=30
        )
        output = result.stdout
        if result.stderr:
            output += f"\nErrors: {result.stderr}"
        return output
    except Exception as e:
        return f"Error running command: {e}"


def search_files(pattern: str, path: str = ".") -> str:
    """Find files matching a pattern (uses shell glob pattern)."""
    try:
        # Use shlex.quote to prevent injection attacks
        safe_path = shlex.quote(path)
        safe_pattern = shlex.quote(pattern)

        result = subprocess.run(
            f"find {safe_path} -name {safe_pattern} -type f 2>/dev/null | head -20",
            shell=True,
            capture_output=True,
            text=True
        )
        files = result.stdout.strip()
        return files if files else "No files found"
    except Exception as e:
        return f"Error searching files: {e}"


def search_content(query: str, path: str = ".") -> str:
    """Search for text in files."""
    try:
        # Use shlex.quote to prevent injection attacks
        safe_path = shlex.quote(path)
        safe_query = shlex.quote(query)

        result = subprocess.run(
            f"grep -r {safe_query} {safe_path} 2>/dev/null | head -20",
            shell=True,
            capture_output=True,
            text=True
        )
        matches = result.stdout.strip()
        return matches if matches else "No matches found"
    except Exception as e:
        return f"Error searching content: {e}"
