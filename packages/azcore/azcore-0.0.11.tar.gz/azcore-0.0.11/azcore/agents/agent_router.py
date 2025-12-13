"""
Agent routing and handoff capabilities for the Azcore..

This module provides dynamic agent selection and handoff mechanisms
inspired by Swarm's MultiAgentRouter functionality.
"""

from typing import List, Optional, Dict, Any, Callable, Sequence
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.tools import BaseTool
from azcore.core.base import BaseAgent
from azcore.exceptions import AgentError, ValidationError, StateError
import logging
import json

logger = logging.getLogger(__name__)


class AgentRouter:
    """
    Routes tasks to appropriate agents based on capabilities and context.

    The AgentRouter analyzes incoming tasks and selects the most suitable
    agent from a pool of available agents. It supports both automatic
    routing via LLM and manual routing via capability matching.

    Attributes:
        name: Router identifier
        description: Router description
        agents: List of available agents
        llm: Language model for routing decisions
        routing_prompt: Custom routing prompt template

    Example:
        >>> security_agent = ReactAgent(name="security", ...)
        >>> maintenance_agent = ReactAgent(name="maintenance", ...)
        >>> router = AgentRouter(
        ...     name="facility_router",
        ...     agents=[security_agent, maintenance_agent],
        ...     llm=llm
        ... )
        >>> result = router.route_task("Check camera feeds")
        >>> # Automatically routes to security_agent
    """

    def __init__(
        self,
        name: str,
        agents: List[BaseAgent],
        llm: Optional[BaseChatModel] = None,
        description: str = "",
        routing_prompt: Optional[str] = None,
        capabilities_key: str = "capabilities"
    ):
        """
        Initialize the agent router.

        Args:
            name: Router identifier
            agents: List of available agents
            llm: Language model for routing (required for automatic routing)
            description: Router description
            routing_prompt: Custom routing prompt template
            capabilities_key: Key for agent capabilities in description
        """
        self.name = name
        self.agents = agents
        self.llm = llm
        self.description = description
        self.capabilities_key = capabilities_key
        self._logger = logging.getLogger(f"{self.__class__.__name__}.{name}")

        if not agents:
            self._logger.error("AgentRouter: No agents provided")
            raise ValidationError(
                "At least one agent must be provided",
                details={"agent_count": 0}
            )

        # Build agent registry
        self.agent_registry: Dict[str, BaseAgent] = {
            agent.name: agent for agent in agents
        }

        # Setup routing prompt
        self.routing_prompt = routing_prompt or self._build_default_routing_prompt()

        self._logger.info(
            f"Initialized AgentRouter '{name}' with {len(agents)} agents"
        )

    def _build_default_routing_prompt(self) -> str:
        """Build default routing prompt with agent information."""
        agent_info = []
        for agent in self.agents:
            info = f"- **{agent.name}**: {agent.description or 'No description'}"
            agent_info.append(info)

        agent_list = "\n".join(agent_info)

        return f"""You are a routing agent that selects the most appropriate agent for a given task.

Available Agents:
{agent_list}

Given a task, analyze it and select the BEST agent to handle it.
Respond with ONLY the agent name, nothing else.

Task: {{task}}
Selected Agent:"""

    def route_task(
        self,
        task: str,
        state: Optional[Dict[str, Any]] = None,
        agent_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Route a task to an appropriate agent.

        Args:
            task: Task to route
            state: Optional state dictionary
            agent_name: Optional explicit agent name (bypasses routing)

        Returns:
            Result from the selected agent

        Raises:
            ValueError: If agent not found or routing fails
        """
        state = state or {}

        # Manual routing if agent_name provided
        if agent_name:
            return self._execute_agent(agent_name, task, state)

        # Automatic routing via LLM
        if not self.llm:
            # Fallback to first agent if no LLM
            self._logger.warning(
                "No LLM provided, routing to first agent"
            )
            return self._execute_agent(self.agents[0].name, task, state)

        # Use LLM to select agent
        selected_agent_name = self._select_agent_via_llm(task)
        return self._execute_agent(selected_agent_name, task, state)

    def _select_agent_via_llm(self, task: str) -> str:
        """
        Select an agent using LLM.

        Args:
            task: Task to route

        Returns:
            Selected agent name

        Raises:
            ValueError: If no agent selected or invalid selection
        """
        prompt = self.routing_prompt.format(task=task)
        messages = [HumanMessage(content=prompt)]

        try:
            response = self.llm.invoke(messages)
            selected_name = response.content.strip()

            # Validate selection
            if selected_name not in self.agent_registry:
                self._logger.warning(
                    f"LLM selected unknown agent '{selected_name}', "
                    f"falling back to first agent"
                )
                selected_name = self.agents[0].name

            self._logger.info(f"Routed task to agent: {selected_name}")
            return selected_name

        except Exception as e:
            self._logger.error(f"Agent selection failed: {e}")
            # Fallback to first agent
            return self.agents[0].name

    def _execute_agent(
        self,
        agent_name: str,
        task: str,
        state: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Execute a specific agent.

        Args:
            agent_name: Name of agent to execute
            task: Task for the agent
            state: Current state

        Returns:
            Updated state from agent execution

        Raises:
            AgentError: If agent not found
        """
        agent = self.agent_registry.get(agent_name)
        if not agent:
            self._logger.error(f"Agent '{agent_name}' not found in registry")
            raise AgentError(
                f"Agent '{agent_name}' not found in registry",
                details={
                    "requested_agent": agent_name,
                    "available_agents": list(self.agent_registry.keys())
                }
            )

        self._logger.info(f"Executing agent: {agent_name}")

        # Update state with task
        state["messages"] = state.get("messages", []) + [
            HumanMessage(content=task)
        ]

        # Execute agent
        try:
            result = agent.invoke(state)
            result["routed_to"] = agent_name
            return result
        except Exception as e:
            self._logger.error(f"Agent execution failed: {e}")
            raise

    def add_agent(self, agent: BaseAgent) -> None:
        """
        Add an agent to the router.

        Args:
            agent: Agent to add
        """
        if agent.name in self.agent_registry:
            self._logger.warning(
                f"Agent '{agent.name}' already exists, replacing"
            )

        self.agents.append(agent)
        self.agent_registry[agent.name] = agent
        self._logger.info(f"Added agent: {agent.name}")

        # Rebuild routing prompt
        self.routing_prompt = self._build_default_routing_prompt()

    def remove_agent(self, agent_name: str) -> bool:
        """
        Remove an agent from the router.

        Args:
            agent_name: Name of agent to remove

        Returns:
            True if removed, False if not found
        """
        if agent_name not in self.agent_registry:
            return False

        agent = self.agent_registry.pop(agent_name)
        self.agents = [a for a in self.agents if a.name != agent_name]
        self._logger.info(f"Removed agent: {agent_name}")

        # Rebuild routing prompt
        self.routing_prompt = self._build_default_routing_prompt()
        return True

    def get_agent(self, agent_name: str) -> Optional[BaseAgent]:
        """Get an agent by name."""
        return self.agent_registry.get(agent_name)

    def list_agents(self) -> List[str]:
        """List all available agent names."""
        return list(self.agent_registry.keys())

    def __repr__(self) -> str:
        return f"AgentRouter(name='{self.name}', agents={len(self.agents)})"


class HandoffAgent(BaseAgent):
    """
    Agent with handoff capabilities to other agents.

    HandoffAgent can delegate tasks to other agents based on routing logic.
    It acts as a coordinator that decides which specialist agent should
    handle specific tasks.

    Attributes:
        handoff_agents: List of agents that can be handed off to
        router: AgentRouter for selecting handoff targets

    Example:
        >>> specialist1 = ReactAgent(name="specialist1", ...)
        >>> specialist2 = ReactAgent(name="specialist2", ...)
        >>> coordinator = HandoffAgent(
        ...     name="coordinator",
        ...     llm=llm,
        ...     handoff_agents=[specialist1, specialist2]
        ... )
        >>> result = coordinator.invoke({"messages": [...]})
    """

    def __init__(
        self,
        name: str,
        llm: BaseChatModel,
        handoff_agents: List[BaseAgent],
        tools: Optional[Sequence[BaseTool]] = None,
        prompt: Optional[str] = None,
        description: str = "",
        routing_prompt: Optional[str] = None
    ):
        """
        Initialize a handoff agent.

        Args:
            name: Agent identifier
            llm: Language model
            handoff_agents: Agents that can be handed off to
            tools: Optional tools for this agent
            prompt: Optional system prompt
            description: Agent description
            routing_prompt: Custom routing prompt
        """
        super().__init__(name, llm, tools, prompt, description)

        if not handoff_agents:
            self._logger.error("HandoffAgent: No handoff agents provided")
            raise ValidationError(
                "At least one handoff agent must be provided",
                details={"agent_count": 0}
            )

        self.handoff_agents = handoff_agents

        # Create router
        self.router = AgentRouter(
            name=f"{name}_router",
            agents=handoff_agents,
            llm=llm,
            routing_prompt=routing_prompt
        )

        self._logger.info(
            f"Initialized HandoffAgent '{name}' with "
            f"{len(handoff_agents)} handoff targets"
        )

    def invoke(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Invoke the handoff agent.

        The agent analyzes the task and hands off to appropriate specialist.

        Args:
            state: Current workflow state

        Returns:
            Updated state from handoff agent execution
        """
        self._logger.debug(f"Invoking HandoffAgent '{self.name}'")

        # Extract task from state
        messages = state.get("messages", [])
        if not messages:
            self._logger.error("HandoffAgent: State has no messages")
            raise StateError(
                "No messages in state",
                details={"state_keys": list(state.keys())}
            )

        last_message = messages[-1]
        if hasattr(last_message, "content"):
            task = last_message.content
        else:
            task = str(last_message)

        # Route to appropriate agent
        result = self.router.route_task(task, state)

        self._logger.info(
            f"Handed off task to: {result.get('routed_to', 'unknown')}"
        )

        return result

    async def ainvoke(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Async invoke (delegates to sync invoke for now)."""
        return self.invoke(state)

    def __repr__(self) -> str:
        return (
            f"HandoffAgent(name='{self.name}', "
            f"handoff_agents={len(self.handoff_agents)})"
        )
