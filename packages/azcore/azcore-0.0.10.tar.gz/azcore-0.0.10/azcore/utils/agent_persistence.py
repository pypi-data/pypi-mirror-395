"""
Agent persistence and state management for the Azcore..

This module provides utilities for saving and loading agent states,
configurations, and conversation histories.
"""

import json
import pickle
from typing import Any, Dict, Optional, Literal
from pathlib import Path
from datetime import datetime
import logging
from azcore.exceptions import ValidationError

try:
    import yaml
    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False

logger = logging.getLogger(__name__)


class AgentPersistence:
    """
    Handles agent state persistence and configuration management.

    Provides functionality to:
    - Save/load agent states
    - Export agent configurations
    - Manage conversation history
    - Create checkpoints
    - Handle various file formats (JSON, YAML, Pickle)

    Example:
        >>> from azcore.utils import AgentPersistence
        >>> from azcore.agents import ReactAgent
        >>>
        >>> agent = ReactAgent(name="worker", llm=llm)
        >>> persistence = AgentPersistence(agent=agent, save_dir="./agent_data")
        >>>
        >>> # Save agent state
        >>> persistence.save_state()
        >>>
        >>> # Load agent state later
        >>> persistence.load_state()
        >>>
        >>> # Export configuration
        >>> persistence.export_config("agent_config.json")
    """

    def __init__(
        self,
        agent: Any,
        save_dir: str = "./agent_states",
        auto_save: bool = False,
        save_format: Literal["json", "yaml", "pickle"] = "json"
    ):
        """
        Initialize agent persistence.

        Args:
            agent: Agent instance to persist
            save_dir: Directory for saving agent data
            auto_save: Enable automatic state saving
            save_format: Default save format
        """
        self.agent = agent
        self.save_dir = Path(save_dir)
        self.auto_save = auto_save
        self.save_format = save_format

        # Create directories
        self.save_dir.mkdir(parents=True, exist_ok=True)
        (self.save_dir / "checkpoints").mkdir(exist_ok=True)
        (self.save_dir / "configs").mkdir(exist_ok=True)

        self._logger = logging.getLogger(
            f"{self.__class__.__name__}.{agent.name}"
        )

    def save_state(
        self,
        filepath: Optional[str] = None,
        include_history: bool = True
    ) -> str:
        """
        Save agent state to file.

        Args:
            filepath: Custom filepath (optional)
            include_history: Include conversation history

        Returns:
            Path to saved state file
        """
        if not filepath:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{self.agent.name}_state_{timestamp}.{self.save_format}"
            filepath = str(self.save_dir / filename)

        # Collect agent state
        state = self._collect_agent_state(include_history)

        # Save based on format
        if self.save_format == "json":
            self._save_json(state, filepath)
        elif self.save_format == "yaml":
            self._save_yaml(state, filepath)
        elif self.save_format == "pickle":
            self._save_pickle(state, filepath)
        else:
            logger.error(f"Unsupported agent save format: {self.save_format}")
            raise ValidationError(
                f"Unsupported format: {self.save_format}",
                details={
                    "format": self.save_format,
                    "supported_formats": ["json", "yaml", "pickle"]
                }
            )

        self._logger.info(f"Saved agent state to {filepath}")
        return filepath

    def load_state(self, filepath: str) -> Dict[str, Any]:
        """
        Load agent state from file.

        Args:
            filepath: Path to state file

        Returns:
            Loaded state dictionary
        """
        path = Path(filepath)

        if not path.exists():
            raise FileNotFoundError(f"State file not found: {filepath}")

        # Load based on format
        if path.suffix == ".json":
            state = self._load_json(filepath)
        elif path.suffix in [".yaml", ".yml"]:
            state = self._load_yaml(filepath)
        elif path.suffix in [".pkl", ".pickle"]:
            state = self._load_pickle(filepath)
        else:
            logger.error(f"Unsupported agent file format: {path.suffix}")
            raise ValidationError(
                f"Unsupported file format: {path.suffix}",
                details={
                    "file_path": str(path),
                    "format": path.suffix,
                    "supported_formats": [".json", ".yaml", ".yml", ".pkl", ".pickle"]
                }
            )

        # Restore agent state
        self._restore_agent_state(state)

        self._logger.info(f"Loaded agent state from {filepath}")
        return state

    def create_checkpoint(self, checkpoint_name: str) -> str:
        """
        Create a named checkpoint of agent state.

        Args:
            checkpoint_name: Name for the checkpoint

        Returns:
            Path to checkpoint file
        """
        checkpoint_path = (
            self.save_dir / "checkpoints" /
            f"{self.agent.name}_{checkpoint_name}.{self.save_format}"
        )

        self.save_state(str(checkpoint_path))
        self._logger.info(f"Created checkpoint: {checkpoint_name}")
        return str(checkpoint_path)

    def load_checkpoint(self, checkpoint_name: str) -> Dict[str, Any]:
        """
        Load a named checkpoint.

        Args:
            checkpoint_name: Name of checkpoint to load

        Returns:
            Loaded state dictionary
        """
        checkpoint_path = (
            self.save_dir / "checkpoints" /
            f"{self.agent.name}_{checkpoint_name}.{self.save_format}"
        )

        return self.load_state(str(checkpoint_path))

    def export_config(
        self,
        filepath: str,
        format: Optional[Literal["json", "yaml"]] = None
    ) -> None:
        """
        Export agent configuration to file.

        Args:
            filepath: Target file path
            format: Export format (inferred from extension if not provided)
        """
        config = self._extract_agent_config()

        path = Path(filepath)
        export_format = format or path.suffix.lstrip(".")

        if export_format == "json":
            self._save_json(config, filepath)
        elif export_format in ["yaml", "yml"]:
            self._save_yaml(config, filepath)
        else:
            logger.error(f"Unsupported export format: {export_format}")
            raise ValidationError(
                f"Unsupported export format: {export_format}",
                details={
                    "format": export_format,
                    "supported_formats": ["json", "yaml", "yml"]
                }
            )

        self._logger.info(f"Exported agent config to {filepath}")

    def _collect_agent_state(self, include_history: bool = True) -> Dict[str, Any]:
        """Collect current agent state."""
        state = {
            "agent_name": self.agent.name,
            "agent_type": self.agent.__class__.__name__,
            "description": getattr(self.agent, "description", ""),
            "saved_at": datetime.now().isoformat(),
        }

        # Add configuration
        if hasattr(self.agent, "prompt"):
            state["prompt"] = self.agent.prompt

        # Add tools info
        if hasattr(self.agent, "tools"):
            state["tools"] = [
                {
                    "name": tool.name,
                    "description": getattr(tool, "description", "")
                }
                for tool in self.agent.tools
            ]

        # Add conversation history if available
        if include_history and hasattr(self.agent, "conversation"):
            state["conversation_history"] = (
                self.agent.conversation.get_history()
            )

        # Add any custom state
        if hasattr(self.agent, "get_state"):
            state["custom_state"] = self.agent.get_state()

        return state

    def _restore_agent_state(self, state: Dict[str, Any]) -> None:
        """Restore agent from state dictionary."""
        # Restore basic attributes
        if "description" in state:
            self.agent.description = state["description"]

        if "prompt" in state and hasattr(self.agent, "prompt"):
            self.agent.prompt = state["prompt"]

        # Restore conversation history
        if "conversation_history" in state and hasattr(self.agent, "conversation"):
            self.agent.conversation.conversation_history = (
                state["conversation_history"]
            )

        # Restore custom state
        if "custom_state" in state and hasattr(self.agent, "set_state"):
            self.agent.set_state(state["custom_state"])

    def _extract_agent_config(self) -> Dict[str, Any]:
        """Extract agent configuration."""
        config = {
            "agent_name": self.agent.name,
            "agent_type": self.agent.__class__.__name__,
            "description": getattr(self.agent, "description", ""),
        }

        # Add prompt
        if hasattr(self.agent, "prompt"):
            config["prompt"] = self.agent.prompt

        # Add tools
        if hasattr(self.agent, "tools"):
            config["tools"] = [
                {
                    "name": tool.name,
                    "description": getattr(tool, "description", ""),
                    "type": tool.__class__.__name__
                }
                for tool in self.agent.tools
            ]

        # Add LLM info
        if hasattr(self.agent, "llm"):
            llm = self.agent.llm
            config["llm"] = {
                "type": llm.__class__.__name__,
                "model": getattr(llm, "model_name", "unknown")
            }

        return config

    def _save_json(self, data: Dict[str, Any], filepath: str) -> None:
        """Save data as JSON."""
        with open(filepath, "w") as f:
            json.dump(data, f, indent=2, default=str)

    def _load_json(self, filepath: str) -> Dict[str, Any]:
        """Load data from JSON."""
        with open(filepath) as f:
            return json.load(f)

    def _save_yaml(self, data: Dict[str, Any], filepath: str) -> None:
        """Save data as YAML."""
        if not YAML_AVAILABLE:
            raise ImportError("PyYAML required for YAML export")

        with open(filepath, "w") as f:
            yaml.dump(data, f, default_flow_style=False)

    def _load_yaml(self, filepath: str) -> Dict[str, Any]:
        """Load data from YAML."""
        if not YAML_AVAILABLE:
            raise ImportError("PyYAML required for YAML loading")

        with open(filepath) as f:
            return yaml.safe_load(f)

    def _save_pickle(self, data: Dict[str, Any], filepath: str) -> None:
        """Save data as pickle."""
        with open(filepath, "wb") as f:
            pickle.dump(data, f)

    def _load_pickle(self, filepath: str) -> Dict[str, Any]:
        """Load data from pickle."""
        with open(filepath, "rb") as f:
            return pickle.load(f)

    def list_saved_states(self) -> list[str]:
        """List all saved state files."""
        states = []
        for pattern in ["*.json", "*.yaml", "*.yml", "*.pkl", "*.pickle"]:
            states.extend([str(p) for p in self.save_dir.glob(pattern)])
        return sorted(states)

    def list_checkpoints(self) -> list[str]:
        """List all checkpoint names."""
        checkpoint_dir = self.save_dir / "checkpoints"
        checkpoints = []

        for pattern in ["*.json", "*.yaml", "*.yml", "*.pkl", "*.pickle"]:
            for path in checkpoint_dir.glob(pattern):
                # Extract checkpoint name
                name = path.stem.replace(f"{self.agent.name}_", "")
                checkpoints.append(name)

        return sorted(checkpoints)

    def delete_checkpoint(self, checkpoint_name: str) -> bool:
        """
        Delete a checkpoint.

        Args:
            checkpoint_name: Name of checkpoint to delete

        Returns:
            True if deleted, False if not found
        """
        checkpoint_path = (
            self.save_dir / "checkpoints" /
            f"{self.agent.name}_{checkpoint_name}.{self.save_format}"
        )

        if checkpoint_path.exists():
            checkpoint_path.unlink()
            self._logger.info(f"Deleted checkpoint: {checkpoint_name}")
            return True

        return False

    def __repr__(self) -> str:
        """Return a string representation of the AgentPersistence instance.

        The string representation includes the agent name and the save format.

        Returns:
            str: A string representation of the AgentPersistence instance.
        """
        return f"AgentPersistence(agent='{self.agent.name}', format='{self.save_format}')"
