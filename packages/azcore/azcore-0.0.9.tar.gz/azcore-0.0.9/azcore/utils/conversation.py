"""
Conversation management for the Azcore..

This module provides conversation history tracking, persistence, and
token management capabilities inspired by Swarm's conversation system.
"""

import json
import uuid
import datetime
from typing import Any, Dict, List, Optional, Literal
from pathlib import Path
import logging
from azcore.exceptions import ValidationError

logger = logging.getLogger(__name__)


def generate_conversation_id() -> str:
    """Generate a unique conversation ID."""
    return str(uuid.uuid4())


class Conversation:
    """
    Manages conversation history with persistence and token tracking.

    This class provides structured conversation management with support for:
    - Message history tracking
    - Automatic persistence (JSON/YAML)
    - Token counting and context management
    - Export/import capabilities
    - Time tracking

    Attributes:
        id: Unique conversation identifier
        name: Human-readable conversation name
        system_prompt: Optional system prompt
        conversation_history: List of conversation messages
        context_length: Maximum context length in tokens
        autosave: Enable automatic saving
        save_filepath: Path for saving conversation

    Example:
        >>> conversation = Conversation(
        ...     name="security_chat",
        ...     system_prompt="You are a security agent",
        ...     autosave=True
        ... )
        >>> conversation.add(role="user", content="Check cameras")
        >>> conversation.add(role="assistant", content="All cameras operational")
        >>> conversation.export_to_json("chat.json")
    """

    def __init__(
        self,
        id: Optional[str] = None,
        name: str = "conversation",
        system_prompt: Optional[str] = None,
        time_enabled: bool = True,
        autosave: bool = False,
        save_filepath: Optional[str] = None,
        context_length: int = 8192,
        export_format: Literal["json", "yaml"] = "json",
        conversations_dir: Optional[str] = None,
    ):
        """
        Initialize a conversation.

        Args:
            id: Unique identifier (auto-generated if not provided)
            name: Human-readable name
            system_prompt: Optional system prompt
            time_enabled: Track timestamps for messages
            autosave: Enable automatic saving
            save_filepath: Custom save file path
            context_length: Maximum context length
            export_format: Default export format
            conversations_dir: Directory for conversation files
        """
        self.id = id or generate_conversation_id()
        self.name = name
        self.system_prompt = system_prompt
        self.time_enabled = time_enabled
        self.autosave = autosave
        self.context_length = context_length
        self.export_format = export_format
        self.conversation_history: List[Dict[str, Any]] = []
        self.created_at = datetime.datetime.now().isoformat()

        # Setup directory
        if conversations_dir:
            self.conversations_dir = Path(conversations_dir)
        else:
            self.conversations_dir = Path.home() / ".arc" / "conversations"

        self.conversations_dir.mkdir(parents=True, exist_ok=True)

        # Setup filepath
        if save_filepath:
            self.save_filepath = Path(save_filepath)
        else:
            ext = ".json" if export_format == "json" else ".yaml"
            self.save_filepath = self.conversations_dir / f"{name}_{self.id[:8]}{ext}"

        # Add system prompt if provided
        if system_prompt:
            self.add(role="system", content=system_prompt)

        # Load existing conversation if file exists
        if self.save_filepath.exists():
            try:
                self.load(str(self.save_filepath))
                logger.info(f"Loaded existing conversation from {self.save_filepath}")
            except Exception as e:
                logger.warning(f"Could not load conversation: {e}")

    def add(
        self,
        role: str,
        content: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Add a message to the conversation history.

        Args:
            role: Message role (e.g., "user", "assistant", "system")
            content: Message content
            metadata: Optional metadata for the message
        """
        message: Dict[str, Any] = {
            "role": role,
            "content": content,
        }

        if self.time_enabled:
            message["timestamp"] = datetime.datetime.now().isoformat()

        if metadata:
            message["metadata"] = metadata

        self.conversation_history.append(message)

        if self.autosave:
            self.save()

    def get_history(self) -> List[Dict[str, Any]]:
        """
        Get the conversation history.

        Returns:
            List of conversation messages
        """
        return self.conversation_history.copy()

    def get_str(self, include_system: bool = True) -> str:
        """
        Get conversation history as a formatted string.

        Args:
            include_system: Include system messages

        Returns:
            Formatted conversation string
        """
        lines = []
        for msg in self.conversation_history:
            if not include_system and msg["role"] == "system":
                continue

            role = msg["role"].upper()
            content = msg["content"]

            if self.time_enabled and "timestamp" in msg:
                timestamp = msg["timestamp"]
                lines.append(f"[{timestamp}] {role}: {content}")
            else:
                lines.append(f"{role}: {content}")

        return "\n\n".join(lines)

    def clear(self, keep_system: bool = True) -> None:
        """
        Clear conversation history.

        Args:
            keep_system: Keep system prompt message
        """
        if keep_system and self.conversation_history:
            # Keep only system messages
            self.conversation_history = [
                msg for msg in self.conversation_history
                if msg["role"] == "system"
            ]
        else:
            self.conversation_history = []

        if self.autosave:
            self.save()

    def save(self, filepath: Optional[str] = None) -> None:
        """
        Save conversation to file.

        Args:
            filepath: Optional custom filepath
        """
        save_path = Path(filepath) if filepath else self.save_filepath

        data = {
            "id": self.id,
            "name": self.name,
            "created_at": self.created_at,
            "system_prompt": self.system_prompt,
            "conversation_history": self.conversation_history
        }

        save_path.parent.mkdir(parents=True, exist_ok=True)

        if save_path.suffix == ".json" or self.export_format == "json":
            with open(save_path, "w") as f:
                json.dump(data, f, indent=2)
        elif save_path.suffix == ".yaml" or self.export_format == "yaml":
            try:
                import yaml
                with open(save_path, "w") as f:
                    yaml.dump(data, f, default_flow_style=False)
            except ImportError:
                logger.warning("PyYAML not installed, falling back to JSON")
                with open(save_path.with_suffix(".json"), "w") as f:
                    json.dump(data, f, indent=2)

        logger.debug(f"Saved conversation to {save_path}")

    def load(self, filepath: str) -> None:
        """
        Load conversation from file.

        Args:
            filepath: Path to conversation file
        """
        path = Path(filepath)

        if not path.exists():
            raise FileNotFoundError(f"Conversation file not found: {filepath}")

        if path.suffix == ".json":
            with open(path) as f:
                data = json.load(f)
        elif path.suffix == ".yaml":
            try:
                import yaml
                with open(path) as f:
                    data = yaml.safe_load(f)
            except ImportError:
                raise ImportError("PyYAML required for loading YAML files")
        else:
            logger.error(f"Unsupported conversation file format: {path.suffix} for file {path}")
            raise ValidationError(
                f"Unsupported file format: {path.suffix}",
                details={
                    "file_path": str(path),
                    "format": path.suffix,
                    "supported_formats": [".json", ".yaml"]
                }
            )

        self.id = data.get("id", self.id)
        self.name = data.get("name", self.name)
        self.created_at = data.get("created_at", self.created_at)
        self.system_prompt = data.get("system_prompt")
        self.conversation_history = data.get("conversation_history", [])

    def export_to_json(self, filepath: str) -> None:
        """Export conversation to JSON file."""
        self.save(filepath)

    def export_to_yaml(self, filepath: str) -> None:
        """Export conversation to YAML file."""
        self.save(filepath)

    def export_to_markdown(self, filepath: str) -> None:
        """
        Export conversation to Markdown file.

        Args:
            filepath: Path to output Markdown file
        """
        md_lines = [
            f"# {self.name}",
            f"",
            f"**ID:** {self.id}",
            f"**Created:** {self.created_at}",
            f"",
        ]

        if self.system_prompt:
            md_lines.extend([
                "## System Prompt",
                "",
                f"```",
                self.system_prompt,
                f"```",
                "",
            ])

        md_lines.append("## Conversation")
        md_lines.append("")

        for msg in self.conversation_history:
            if msg["role"] == "system":
                continue

            role = msg["role"].title()
            content = msg["content"]

            if self.time_enabled and "timestamp" in msg:
                timestamp = msg["timestamp"]
                md_lines.append(f"### {role} - {timestamp}")
            else:
                md_lines.append(f"### {role}")

            md_lines.append("")
            md_lines.append(content)
            md_lines.append("")

        with open(filepath, "w") as f:
            f.write("\n".join(md_lines))

        logger.info(f"Exported conversation to Markdown: {filepath}")

    def get_context_window_messages(
        self,
        max_tokens: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Get messages within context window.

        Args:
            max_tokens: Maximum tokens (uses context_length if not provided)

        Returns:
            List of messages within context window
        """
        # Simple implementation - in production, would use actual tokenizer
        max_tokens = max_tokens or self.context_length

        # Approximate: 1 token ≈ 4 characters
        char_limit = max_tokens * 4

        messages = []
        total_chars = 0

        # Add messages from most recent backwards
        for msg in reversed(self.conversation_history):
            msg_chars = len(msg["content"])
            if total_chars + msg_chars > char_limit:
                break

            messages.insert(0, msg)
            total_chars += msg_chars

        return messages

    def __len__(self) -> int:
        """Return number of messages in conversation."""
        return len(self.conversation_history)

    def __repr__(self) -> str:
        return f"Conversation(name='{self.name}', messages={len(self)})"
