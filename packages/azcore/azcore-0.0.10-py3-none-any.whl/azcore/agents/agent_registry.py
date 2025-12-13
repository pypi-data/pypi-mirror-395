"""
Agent registry system for the Azcore..

This module provides centralized agent management, discovery, and lifecycle
management inspired by Swarms' agent registry capabilities.
"""

import json
import logging
from typing import Any, Dict, List, Optional, Callable
from datetime import datetime
from pathlib import Path
from dataclasses import dataclass, asdict

logger = logging.getLogger(__name__)


@dataclass
class AgentMetadata:
    """
    Metadata for a registered agent.

    Attributes:
        name: Agent identifier
        description: Agent description
        capabilities: List of agent capabilities
        created_at: Registration timestamp
        model_name: LLM model name
        tools: List of tool names
        tags: List of tags for categorization
        version: Agent version
    """
    name: str
    description: str
    capabilities: List[str]
    created_at: str
    model_name: Optional[str] = None
    tools: Optional[List[str]] = None
    tags: Optional[List[str]] = None
    version: str = "1.0.0"
    metadata: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'AgentMetadata':
        """Create from dictionary."""
        return cls(**data)


class AgentRegistry:
    """
    Centralized registry for agent management and discovery.

    The AgentRegistry provides a central location for:
    - Registering and deregistering agents
    - Discovering agents by capabilities
    - Tracking agent metadata and statistics
    - Persisting agent information

    Attributes:
        name: Registry name
        agents: Dictionary mapping agent names to agent instances
        metadata: Dictionary mapping agent names to metadata
        registry_path: Path for persisting registry data

    Example:
        >>> from azcore.agents import Agent
        >>> registry = AgentRegistry("production_registry")
        >>>
        >>> # Register an agent
        >>> agent = Agent(name="researcher", ...)
        >>> registry.register(
        ...     agent,
        ...     capabilities=["research", "analysis"],
        ...     tags=["data", "reports"]
        ... )
        >>>
        >>> # Find agents by capability
        >>> research_agents = registry.find_by_capability("research")
        >>>
        >>> # List all agents
        >>> all_agents = registry.list_agents()
    """

    def __init__(
        self,
        name: str = "agent_registry",
        registry_dir: Optional[str] = None,
        auto_save: bool = True
    ):
        """
        Initialize an agent registry.

        Args:
            name: Registry identifier
            registry_dir: Directory for registry persistence
            auto_save: Automatically save registry on changes
        """
        self.name = name
        self.auto_save = auto_save

        # Setup registry directory
        if registry_dir:
            self.registry_path = Path(registry_dir)
        else:
            self.registry_path = Path.home() / ".arc" / "registries"

        self.registry_path.mkdir(parents=True, exist_ok=True)

        # Storage
        self.agents: Dict[str, Any] = {}
        self.metadata: Dict[str, AgentMetadata] = {}
        self.execution_stats: Dict[str, Dict[str, Any]] = {}

        # Load existing registry
        self.registry_file = self.registry_path / f"{name}_registry.json"
        if self.registry_file.exists():
            self.load()

        logger.info(f"Initialized AgentRegistry: {name}")

    def register(
        self,
        agent: Any,
        description: str = "",
        capabilities: List[str] = None,
        tools: List[str] = None,
        tags: List[str] = None,
        version: str = "1.0.0",
        metadata: Dict[str, Any] = None
    ) -> None:
        """
        Register an agent in the registry.

        Args:
            agent: Agent instance to register
            description: Agent description
            capabilities: List of agent capabilities
            tools: List of tool names
            tags: Tags for categorization
            version: Agent version
            metadata: Additional metadata

        Raises:
            ValueError: If agent with same name already registered
        """
        agent_name = getattr(agent, "name", getattr(agent, "agent_name", str(agent)))

        if agent_name in self.agents:
            logger.warning(f"Agent '{agent_name}' already registered, updating...")

        # Extract model name if available
        model_name = None
        if hasattr(agent, "llm"):
            model_name = getattr(agent.llm, "model_name", None)
        elif hasattr(agent, "model_name"):
            model_name = agent.model_name

        # Create metadata
        agent_metadata = AgentMetadata(
            name=agent_name,
            description=description or getattr(agent, "description", ""),
            capabilities=capabilities or [],
            created_at=datetime.now().isoformat(),
            model_name=model_name,
            tools=tools or self._extract_tools(agent),
            tags=tags or [],
            version=version,
            metadata=metadata
        )

        # Register
        self.agents[agent_name] = agent
        self.metadata[agent_name] = agent_metadata
        self.execution_stats[agent_name] = {
            "executions": 0,
            "successes": 0,
            "failures": 0,
            "total_time": 0.0
        }

        logger.info(f"Registered agent: {agent_name}")

        if self.auto_save:
            self.save()

    def deregister(self, agent_name: str) -> None:
        """
        Deregister an agent from the registry.

        Args:
            agent_name: Name of agent to deregister
        """
        if agent_name in self.agents:
            del self.agents[agent_name]
            del self.metadata[agent_name]
            if agent_name in self.execution_stats:
                del self.execution_stats[agent_name]

            logger.info(f"Deregistered agent: {agent_name}")

            if self.auto_save:
                self.save()
        else:
            logger.warning(f"Agent '{agent_name}' not found in registry")

    def get(self, agent_name: str) -> Optional[Any]:
        """
        Get an agent by name.

        Args:
            agent_name: Agent name

        Returns:
            Agent instance or None
        """
        return self.agents.get(agent_name)

    def get_metadata(self, agent_name: str) -> Optional[AgentMetadata]:
        """
        Get agent metadata.

        Args:
            agent_name: Agent name

        Returns:
            AgentMetadata or None
        """
        return self.metadata.get(agent_name)

    def list_agents(self) -> List[str]:
        """
        List all registered agent names.

        Returns:
            List of agent names
        """
        return list(self.agents.keys())

    def find_by_capability(self, capability: str) -> List[str]:
        """
        Find agents by capability.

        Args:
            capability: Capability to search for

        Returns:
            List of agent names with the capability
        """
        matches = []
        for agent_name, meta in self.metadata.items():
            if capability.lower() in [c.lower() for c in meta.capabilities]:
                matches.append(agent_name)

        return matches

    def find_by_tag(self, tag: str) -> List[str]:
        """
        Find agents by tag.

        Args:
            tag: Tag to search for

        Returns:
            List of agent names with the tag
        """
        matches = []
        for agent_name, meta in self.metadata.items():
            if meta.tags and tag.lower() in [t.lower() for t in meta.tags]:
                matches.append(agent_name)

        return matches

    def find_by_tool(self, tool_name: str) -> List[str]:
        """
        Find agents that have a specific tool.

        Args:
            tool_name: Tool name to search for

        Returns:
            List of agent names with the tool
        """
        matches = []
        for agent_name, meta in self.metadata.items():
            if meta.tools and tool_name in meta.tools:
                matches.append(agent_name)

        return matches

    def search(self, query: str) -> List[str]:
        """
        Search agents by query string (searches name, description, capabilities).

        Args:
            query: Search query

        Returns:
            List of matching agent names
        """
        query_lower = query.lower()
        matches = []

        for agent_name, meta in self.metadata.items():
            # Search in name
            if query_lower in agent_name.lower():
                matches.append(agent_name)
                continue

            # Search in description
            if query_lower in meta.description.lower():
                matches.append(agent_name)
                continue

            # Search in capabilities
            if any(query_lower in cap.lower() for cap in meta.capabilities):
                matches.append(agent_name)
                continue

        return matches

    def record_execution(
        self,
        agent_name: str,
        success: bool,
        execution_time: float
    ) -> None:
        """
        Record an agent execution.

        Args:
            agent_name: Agent name
            success: Whether execution was successful
            execution_time: Execution time in seconds
        """
        if agent_name not in self.execution_stats:
            logger.warning(f"Agent '{agent_name}' not in registry")
            return

        stats = self.execution_stats[agent_name]
        stats["executions"] += 1
        stats["total_time"] += execution_time

        if success:
            stats["successes"] += 1
        else:
            stats["failures"] += 1

        if self.auto_save:
            self.save()

    def get_stats(self, agent_name: str) -> Dict[str, Any]:
        """
        Get execution statistics for an agent.

        Args:
            agent_name: Agent name

        Returns:
            Statistics dictionary
        """
        if agent_name not in self.execution_stats:
            return {}

        stats = self.execution_stats[agent_name].copy()
        if stats["executions"] > 0:
            stats["avg_time"] = stats["total_time"] / stats["executions"]
            stats["success_rate"] = stats["successes"] / stats["executions"]
        else:
            stats["avg_time"] = 0.0
            stats["success_rate"] = 0.0

        return stats

    def get_all_stats(self) -> Dict[str, Dict[str, Any]]:
        """
        Get execution statistics for all agents.

        Returns:
            Dictionary mapping agent names to statistics
        """
        return {
            agent_name: self.get_stats(agent_name)
            for agent_name in self.agents.keys()
        }

    def save(self, filepath: Optional[str] = None) -> None:
        """
        Save registry to file.

        Args:
            filepath: Optional custom filepath
        """
        save_path = Path(filepath) if filepath else self.registry_file

        data = {
            "name": self.name,
            "saved_at": datetime.now().isoformat(),
            "metadata": {
                name: meta.to_dict()
                for name, meta in self.metadata.items()
            },
            "execution_stats": self.execution_stats
        }

        with open(save_path, 'w') as f:
            json.dump(data, f, indent=2, default=str)

        logger.debug(f"Saved registry to {save_path}")

    def load(self, filepath: Optional[str] = None) -> None:
        """
        Load registry from file.

        Args:
            filepath: Optional custom filepath
        """
        load_path = Path(filepath) if filepath else self.registry_file

        if not load_path.exists():
            logger.warning(f"Registry file not found: {load_path}")
            return

        with open(load_path) as f:
            data = json.load(f)

        # Load metadata
        metadata_dict = data.get("metadata", {})
        self.metadata = {
            name: AgentMetadata.from_dict(meta_dict)
            for name, meta_dict in metadata_dict.items()
        }

        # Load execution stats
        self.execution_stats = data.get("execution_stats", {})

        logger.info(f"Loaded registry from {load_path}: {len(self.metadata)} agents")

    def export_info(self) -> Dict[str, Any]:
        """
        Export registry information.

        Returns:
            Dictionary with registry information
        """
        return {
            "name": self.name,
            "agent_count": len(self.agents),
            "agents": [
                {
                    "name": meta.name,
                    "description": meta.description,
                    "capabilities": meta.capabilities,
                    "tags": meta.tags,
                    "stats": self.get_stats(meta.name)
                }
                for meta in self.metadata.values()
            ]
        }

    def print_summary(self) -> None:
        """Print a summary of the registry."""
        print(f"\n{'=' * 60}")
        print(f"Agent Registry: {self.name}")
        print(f"{'=' * 60}")
        print(f"Total Agents: {len(self.agents)}\n")

        if not self.agents:
            print("No agents registered.")
            return

        for agent_name in self.agents.keys():
            meta = self.metadata[agent_name]
            stats = self.get_stats(agent_name)

            print(f"Agent: {agent_name}")
            print(f"  Description: {meta.description}")
            print(f"  Capabilities: {', '.join(meta.capabilities)}")
            if meta.tags:
                print(f"  Tags: {', '.join(meta.tags)}")
            if stats.get("executions", 0) > 0:
                print(f"  Executions: {stats['executions']}")
                print(f"  Success Rate: {stats['success_rate']:.1%}")
                print(f"  Avg Time: {stats['avg_time']:.2f}s")
            print()

    def _extract_tools(self, agent: Any) -> List[str]:
        """Extract tool names from an agent."""
        tools = []

        if hasattr(agent, "tools"):
            for tool in agent.tools:
                if hasattr(tool, "name"):
                    tools.append(tool.name)
                elif isinstance(tool, str):
                    tools.append(tool)

        return tools

    def __len__(self) -> int:
        """Return number of registered agents."""
        return len(self.agents)

    def __contains__(self, agent_name: str) -> bool:
        """Check if agent is registered."""
        return agent_name in self.agents

    def __repr__(self) -> str:
        return f"AgentRegistry(name='{self.name}', agents={len(self.agents)})"


# Global registry instance
_global_registry: Optional[AgentRegistry] = None


def get_global_registry() -> AgentRegistry:
    """
    Get the global agent registry.

    Returns:
        Global AgentRegistry instance
    """
    global _global_registry
    if _global_registry is None:
        _global_registry = AgentRegistry(name="global")
    return _global_registry


def register_agent_globally(
    agent: Any,
    **kwargs
) -> None:
    """
    Register an agent in the global registry.

    Args:
        agent: Agent to register
        **kwargs: Additional registration parameters
    """
    registry = get_global_registry()
    registry.register(agent, **kwargs)


def find_agent(agent_name: str) -> Optional[Any]:
    """
    Find an agent in the global registry.

    Args:
        agent_name: Agent name

    Returns:
        Agent instance or None
    """
    registry = get_global_registry()
    return registry.get(agent_name)
