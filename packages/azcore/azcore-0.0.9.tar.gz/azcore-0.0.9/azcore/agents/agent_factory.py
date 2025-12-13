"""
AgentFactory for creating different types of agents.

This module provides a factory pattern for creating various agent types
with consistent configuration and behavior.
"""

from typing import Sequence, Optional, Dict, Any, Union
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.tools import BaseTool
from azcore.core.agent_executor import create_thinkat_agent
from azcore.core.base import BaseAgent
from azcore.utils.cached_llm import CachedLLM, enable_llm_caching
from azcore.exceptions import AgentError, ConfigurationError, ValidationError
import logging

logger = logging.getLogger(__name__)

# Import RL components if available
try:
    from azcore.rl.rl_manager import RLManager
    from azcore.rl.rewards import RewardCalculator
    RL_AVAILABLE = True
except ImportError:
    RL_AVAILABLE = False
    logger.debug("RL components not available")


class ReactAgent(BaseAgent):
    """
    React-style agent that uses tools to accomplish tasks.
    
    This agent follows the ReAct (Reasoning and Acting) pattern,
    iteratively reasoning about tasks and using tools to accomplish them.
    """
    
    def __init__(
        self,
        name: str,
        llm: Union[BaseChatModel, CachedLLM],
        tools: Optional[Sequence[BaseTool]] = None,
        prompt: Optional[str] = None,
        description: str = "",
        rl_enabled: bool = False,
        rl_manager: Optional['RLManager'] = None,
        reward_calculator: Optional['RewardCalculator'] = None,
        enable_caching: bool = True,
        cache_type: str = "exact"
    ):
        """
        Initialize a ReAct agent.
        
        Args:
            name: Unique identifier for the agent
            llm: Language model (will be wrapped with caching if enable_caching=True)
            tools: Optional sequence of tools
            prompt: Optional system prompt
            description: Human-readable description
            rl_enabled: Enable RL-based tool selection
            rl_manager: Optional RLManager instance
            reward_calculator: Optional reward calculator
            enable_caching: Enable LLM response caching
            cache_type: Cache type ("exact" or "semantic")
        """
        # Wrap LLM with caching if enabled and not already cached
        if enable_caching and not isinstance(llm, CachedLLM):
            llm = enable_llm_caching(llm, cache_type=cache_type)
            logger.info(f"Enabled {cache_type} caching for agent '{name}' LLM")
        
        super().__init__(name, llm, tools, prompt, description)
        
        # RL configuration
        self.rl_enabled = rl_enabled and RL_AVAILABLE
        self.rl_manager = rl_manager
        self.reward_calculator = reward_calculator
        self._all_tools = list(tools) if tools else []
        
        if self.rl_enabled and not self.rl_manager:
            self._logger.warning("RL enabled but no RLManager provided")
            self.rl_enabled = False
        
        self._agent = create_thinkat_agent(
            model=llm,
            tools=self.tools,
            prompt=prompt
        )
        
    
        self._logger.info(
            f"Created ReactAgent '{name}' with {len(self.tools)} tools"
            + (f", RL enabled" if self.rl_enabled else "")
        )
    
    def invoke(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Invoke the agent synchronously.
        
        Args:
            state: Current workflow state
            
        Returns:
            Updated state after agent execution
        """
        self._logger.debug(f"Invoking ReactAgent '{self.name}'")
        
        # Apply RL tool selection if enabled
        if self.rl_enabled:
            state = self._apply_rl_tool_selection(state)
        
        result = self._agent.invoke(state)
        
        # Apply RL reward update if enabled
        if self.rl_enabled:
            self._apply_rl_reward(state, result)
        
        return result
    
    def _apply_rl_tool_selection(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Select tools using RL manager based on current state."""
        if not self.rl_manager:
            return state
        
        # Extract query from state
        query = self._extract_query_from_state(state)
        
        # Get RL-recommended tools
        selected_tool_names, state_key = self.rl_manager.select_tools(query)
        
        # Filter tools
        selected_tools = [t for t in self._all_tools if t.name in selected_tool_names]
        
        # Update agent with selected tools
        self.tools = selected_tools
        self._agent = create_thinkat_agent(
            model=self.llm,
            tools=self.tools,
            prompt=self.prompt
        )
        
        # Store RL metadata in state
        rl_metadata = state.get("rl_metadata", {})
        rl_metadata.update({
            "state_key": state_key,
            "selected_tools": selected_tool_names,
            "query": query
        })
        state["rl_metadata"] = rl_metadata
        
        self._logger.info(f"RL selected tools: {selected_tool_names}")
        
        return state
    
    def _apply_rl_reward(self, state: Dict[str, Any], result: Dict[str, Any]) -> None:
        """Calculate and apply reward to RL manager."""
        if not self.rl_manager or not self.reward_calculator:
            return
        
        rl_metadata = state.get("rl_metadata", {})
        state_key = rl_metadata.get("state_key")
        selected_tools = rl_metadata.get("selected_tools", [])
        query = rl_metadata.get("query", "")
        
        if not state_key or not selected_tools:
            return
        
        # Calculate reward
        try:
            reward = self.reward_calculator.calculate(result, result, query)
            
            # Update RL for each selected tool
            self.rl_manager.update_batch(state_key, selected_tools, reward)
            
            self._logger.info(f"RL reward applied: {reward:.3f} for tools: {selected_tools}")
        except Exception as e:
            self._logger.error(f"Error applying RL reward: {e}")
    
    def _extract_query_from_state(self, state: Dict[str, Any]) -> str:
        """Extract user query from state."""
        messages = state.get("messages", [])
        if messages:
            last_msg = messages[-1]
            if isinstance(last_msg, tuple) and len(last_msg) > 1:
                return str(last_msg[1])
            elif hasattr(last_msg, "content"):
                return last_msg.content
        return ""
    
    async def ainvoke(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Invoke the agent asynchronously.
        
        Args:
            state: Current workflow state
            
        Returns:
            Updated state after agent execution
        """
        self._logger.debug(f"Async invoking ReactAgent '{self.name}'")
        
        # Apply RL tool selection if enabled
        if self.rl_enabled:
            state = self._apply_rl_tool_selection(state)
        
        result = await self._agent.ainvoke(state)
        
        # Apply RL reward update if enabled
        if self.rl_enabled:
            self._apply_rl_reward(state, result)
        
        return result
    
    def stream(self, state: Dict[str, Any]):
        """
        Stream agent responses.
        
        Args:
            state: Current workflow state
            
        Yields:
            Agent response chunks
        """
        return self._agent.stream(state)
    
    async def astream(self, state: Dict[str, Any]):
        """
        Asynchronously stream agent responses.
        
        Args:
            state: Current workflow state
            
        Yields:
            Agent response chunks
        """
        async for chunk in self._agent.astream(state):
            yield chunk


class AgentFactory:
    """
    Factory for creating different types of agents.
    
    This factory provides a consistent interface for creating various
    agent types with common configurations.
    
    Example:
        >>> factory = AgentFactory(default_llm=llm)
        >>> agent = factory.create_react_agent(
        ...     name="security_agent",
        ...     tools=[camera_tool],
        ...     prompt="You are a security agent..."
        ... )
    """
    
    def __init__(
        self,
        default_llm: Optional[BaseChatModel] = None,
        default_tools: Optional[Sequence[BaseTool]] = None
    ):
        """
        Initialize the agent factory.
        
        Args:
            default_llm: Default language model for agents
            default_tools: Default tools for agents
        """
        self.default_llm = default_llm
        self.default_tools = list(default_tools) if default_tools else []
        self._logger = logging.getLogger(self.__class__.__name__)
        
        self._logger.info("AgentFactory initialized")
    
    def create_react_agent(
        self,
        name: str,
        llm: Optional[Union[BaseChatModel, CachedLLM]] = None,
        tools: Optional[Sequence[BaseTool]] = None,
        prompt: Optional[str] = None,
        description: str = "",
        rl_enabled: bool = False,
        rl_manager: Optional['RLManager'] = None,
        reward_calculator: Optional['RewardCalculator'] = None,
        enable_caching: bool = True,
        cache_type: str = "exact"
    ) -> ReactAgent:
        """
        Create a ReAct-style agent.
        
        Args:
            name: Agent name
            llm: Language model (uses default if not provided)
            tools: Tools for the agent (uses default if not provided)
            prompt: System prompt
            description: Agent description
            rl_enabled: Enable RL-based tool selection
            rl_manager: Optional RLManager instance
            reward_calculator: Optional reward calculator
            enable_caching: Enable LLM response caching
            cache_type: Cache type ("exact" or "semantic")
            
        Returns:
            ReactAgent instance
            
        Raises:
            ConfigurationError: If no LLM is provided and no default is set
        """
        agent_llm = llm or self.default_llm
        if not agent_llm:
            self._logger.error("Cannot create agent: No LLM configured")
            raise ConfigurationError(
                "No LLM provided and no default LLM set",
                details={"agent_name": name, "has_default_llm": self.default_llm is not None}
            )
        
        agent_tools = list(tools) if tools else self.default_tools
        
        agent = ReactAgent(
            name=name,
            llm=agent_llm,
            tools=agent_tools,
            prompt=prompt,
            description=description,
            rl_enabled=rl_enabled,
            rl_manager=rl_manager,
            reward_calculator=reward_calculator,
            enable_caching=enable_caching,
            cache_type=cache_type
        )
        
        self._logger.info(
            f"Created ReactAgent '{name}'"
            + (f" with RL" if rl_enabled else "")
        )
        
        return agent
    
    def create_custom_agent(
        self,
        agent_class: type,
        name: str,
        **kwargs
    ) -> BaseAgent:
        """
        Create a custom agent type.
        
        Args:
            agent_class: Agent class to instantiate
            name: Agent name
            **kwargs: Additional arguments for the agent
            
        Returns:
            Agent instance
            
        Raises:
            ValidationError: If agent_class doesn't inherit from BaseAgent
        """
        if not issubclass(agent_class, BaseAgent):
            self._logger.error(f"Invalid agent class: {agent_class.__name__} does not inherit from BaseAgent")
            raise ValidationError(
                f"Agent class must inherit from BaseAgent",
                details={
                    "agent_class": agent_class.__name__,
                    "agent_name": name,
                    "base_class": BaseAgent.__name__
                }
            )
        
        # Provide defaults if not in kwargs
        if 'llm' not in kwargs and self.default_llm:
            kwargs['llm'] = self.default_llm
        
        if 'tools' not in kwargs and self.default_tools:
            kwargs['tools'] = self.default_tools
        
        agent = agent_class(name=name, **kwargs)
        
        self._logger.info(f"Created custom agent '{name}' of type {agent_class.__name__}")
        
        return agent
    
    def set_default_llm(self, llm: BaseChatModel) -> None:
        """
        Set the default language model.
        
        Args:
            llm: Language model to set as default
        """
        self.default_llm = llm
        self._logger.info("Updated default LLM")
    
    def set_default_tools(self, tools: Sequence[BaseTool]) -> None:
        """
        Set the default tools.
        
        Args:
            tools: Tools to set as default
        """
        self.default_tools = list(tools)
        self._logger.info(f"Updated default tools ({len(self.default_tools)} tools)")
    
    def add_default_tool(self, tool: BaseTool) -> None:
        """
        Add a tool to the default tools.
        
        Args:
            tool: Tool to add
        """
        if tool not in self.default_tools:
            self.default_tools.append(tool)
            self._logger.info(f"Added tool '{tool.name}' to default tools")
    
    def __repr__(self) -> str:
        return f"AgentFactory(default_tools={len(self.default_tools)})"
