"""
Automatic JSON-based conversation persistence for Buchi CLI.
Each working directory gets its own isolated conversation history.
"""

import json
import os
import tempfile
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path


class JSONStorage:
    """Automatic JSON-based conversation persistence"""

    def __init__(self, working_dir: str):
        """
        Initialize storage for a working directory.

        Args:
            working_dir: The project directory to store conversations for
        """
        self.working_dir = Path(working_dir).resolve()
        self.buchi_dir = self.working_dir / ".buchi"
        self.conversations_file = self.buchi_dir / "conversations.json"
        self.config_file = self.buchi_dir / "config.json"

        # Automatically setup storage
        self._setup()

    def _setup(self):
        """Automatically create storage structure"""
        # Create .buchi directory
        self.buchi_dir.mkdir(exist_ok=True)

        # Create .gitignore in .buchi directory
        gitignore = self.buchi_dir / ".gitignore"
        if not gitignore.exists():
            gitignore.write_text(
                "# Buchi CLI conversation history\n"
                "# Remove this file to track conversations in git\n"
            )

        # Initialize conversations file
        if not self.conversations_file.exists():
            self._write_json(self.conversations_file, {"messages": []})

        # Initialize config with default limit
        if not self.config_file.exists():
            self._write_json(self.config_file, {"message_limit": 20})

    @contextmanager
    def _atomic_write(self, filepath: Path):
        """
        Context manager for atomic file writes.
        Prevents corruption by writing to temp file first, then replacing.
        """
        # Create temp file in same directory as target
        temp_fd, temp_path = tempfile.mkstemp(
            dir=filepath.parent, suffix=".tmp", prefix=".buchi_"
        )

        try:
            with os.fdopen(temp_fd, "w", encoding="utf-8") as f:
                yield f
            # Atomic rename (replaces target file)
            os.replace(temp_path, filepath)
        except Exception:
            # Clean up temp file on error
            try:
                os.unlink(temp_path)
            except OSError:
                pass
            raise

    def _write_json(self, filepath: Path, data: dict):
        """Write JSON atomically to prevent corruption"""
        with self._atomic_write(filepath) as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def _read_json(self, filepath: Path) -> dict:
        """Read JSON file safely"""
        try:
            with open(filepath, encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError) as e:
            print(f"Warning: Could not read {filepath}: {e}")
            return {}

    def add_message(self, role: str, content: str, tool_calls: list[dict] = None):
        """
        Add a message to conversation history.

        Args:
            role: Either "user" or "assistant"
            content: The message content
            tool_calls: Optional list of tool calls made (for debugging)
        """
        data = self._read_json(self.conversations_file)

        message = {
            "timestamp": datetime.now().isoformat(),
            "role": role,
            "content": content,
        }

        if tool_calls:
            message["tool_calls"] = tool_calls

        data["messages"].append(message)
        self._write_json(self.conversations_file, data)

    def get_messages(self, limit: int | None = None) -> list[dict]:
        """
        Get recent messages based on configured or specified limit.

        Args:
            limit: Number of recent messages to return (None = use config)

        Returns:
            List of message dictionaries
        """
        data = self._read_json(self.conversations_file)
        messages = data.get("messages", [])

        # Use specified limit or config limit
        if limit is None:
            config = self._read_json(self.config_file)
            limit = config.get("message_limit", 20)

        # Return last N messages
        if limit > 0:
            return messages[-limit:]
        else:
            return messages  # 0 = unlimited

    def get_all_messages(self) -> list[dict]:
        """Get all messages (for history viewing)"""
        data = self._read_json(self.conversations_file)
        return data.get("messages", [])

    def clear_messages(self):
        """Clear all conversation history"""
        self._write_json(self.conversations_file, {"messages": []})

    def get_message_count(self) -> int:
        """Get total message count"""
        data = self._read_json(self.conversations_file)
        return len(data.get("messages", []))

    def get_config(self) -> dict:
        """Get configuration"""
        return self._read_json(self.config_file)

    def set_message_limit(self, limit: int):
        """
        Set message limit for AI context.

        Args:
            limit: Number of messages to keep in context (0 = unlimited)

        Raises:
            ValueError: If limit is negative
        """
        if limit < 0:
            raise ValueError("Message limit must be non-negative (0 = unlimited)")

        config = self.get_config()
        config["message_limit"] = limit
        self._write_json(self.config_file, config)

    def get_message_limit(self) -> int:
        """Get current message limit"""
        config = self.get_config()
        return config.get("message_limit", 20)

    def get_summary(self) -> dict:
        """
        Get conversation statistics.

        Returns:
            Dictionary with total_messages, first_interaction,
            last_interaction, and current_limit
        """
        messages = self.get_all_messages()

        if not messages:
            return {
                "total_messages": 0,
                "first_interaction": None,
                "last_interaction": None,
                "current_limit": self.get_message_limit(),
            }

        return {
            "total_messages": len(messages),
            "first_interaction": messages[0]["timestamp"],
            "last_interaction": messages[-1]["timestamp"],
            "current_limit": self.get_message_limit(),
        }
