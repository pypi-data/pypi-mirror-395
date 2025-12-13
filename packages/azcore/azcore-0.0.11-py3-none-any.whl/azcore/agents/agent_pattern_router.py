"""
Agent Pattern Router for Azcore.

A flexible router for dynamically selecting and instantiating various agent patterns
based on task requirements. This provides a unified interface for all advanced
reasoning agent patterns in the Azcore..

Supported Agent Patterns:
- self-consistency: Multiple independent solutions with consensus
- reflexion: Iterative reflection and refinement
- reasoning-duo: Collaborative dual-agent system
- agent-judge: Evaluation and critique agent
- react: Standard ReAct agent (default)
"""

import logging
from typing import Dict, Any, Optional, Literal, List
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.tools import BaseTool

from azcore.core.base import BaseAgent
from azcore.agents.agent_factory import ReactAgent
from azcore.agents.self_consistency_agent import SelfConsistencyAgent
from azcore.agents.reflexion_agent import ReflexionAgent
from azcore.agents.reasoning_duo_agent import ReasoningDuoAgent
from azcore.agents.agent_judge import AgentJudge
from azcore.exceptions import ConfigurationError, ValidationError

logger = logging.getLogger(__name__)


# Type definition for supported agent patterns
AgentPattern = Literal[
    "self-consistency",
    "consistency",
    "reflexion",
    "reasoning-duo",
    "duo",
    "agent-judge",
    "judge",
    "react",
]


class AgentPatternRouter:
    """
    A router for advanced agent patterns in the Azcore..

    The AgentPatternRouter enables dynamic selection, instantiation, and management
    of various reasoning agent patterns for flexible, robust problem-solving.

    Args:
        pattern (AgentPattern): Type of agent pattern to use
        name (str): Name identifier for the agent instance
        llm (BaseChatModel): Language model to use
        tools (Optional[List[BaseTool]]): Optional list of tools
        prompt (str): System prompt for the agent
        description (str): Description of the agent's capabilities
        **kwargs: Additional pattern-specific configuration

    Pattern-Specific Parameters:
        self-consistency:
            - num_samples (int): Number of independent responses (default: 5)
            - majority_voting_prompt (str): Custom voting prompt
            - eval_mode (bool): Enable evaluation mode
        
        reflexion:
            - max_loops (int): Number of reflection iterations (default: 3)
            - memory_capacity (int): Memory system capacity (default: 100)
        
        reasoning-duo:
            - max_loops (int): Number of reasoning iterations (default: 1)
        
        agent-judge:
            - evaluation_criteria (Dict[str, float]): Criteria with weights
            - return_score (bool): Return score instead of text
            - max_loops (int): Evaluation iterations (default: 1)
        
        react:
            - rl_enabled (bool): Enable reinforcement learning
            - rl_manager: RL manager instance
            - reward_calculator: Reward calculator instance

    Example:
        >>> from langchain_openai import ChatOpenAI
        >>> from azcore.agents.agent_pattern_router import AgentPatternRouter
        >>> 
        >>> llm = ChatOpenAI(model="gpt-4o-mini")
        >>> 
        >>> # Use self-consistency pattern
        >>> router = AgentPatternRouter(
        ...     pattern="self-consistency",
        ...     llm=llm,
        ...     num_samples=5,
        ... )
        >>> state = {"messages": [{"role": "user", "content": "What is 2+2?"}]}
        >>> result = router.invoke(state)
        >>> 
        >>> # Use reflexion pattern
        >>> router = AgentPatternRouter(
        ...     pattern="reflexion",
        ...     llm=llm,
        ...     max_loops=3,
        ... )
        >>> result = router.invoke(state)
    """

    def __init__(
        self,
        pattern: AgentPattern = "react",
        name: str = "agent",
        llm: BaseChatModel = None,
        tools: Optional[List[BaseTool]] = None,
        prompt: str = "You are a helpful assistant.",
        description: str = "An intelligent agent for problem-solving.",
        **kwargs,
    ):
        """
        Initialize the AgentPatternRouter with the specified configuration.

        Args:
            pattern (AgentPattern): Type of agent pattern to use
            name (str): Name identifier for the agent
            llm (BaseChatModel): Language model to use
            tools (Optional[List[BaseTool]]): Optional list of tools
            prompt (str): System prompt for the agent
            description (str): Description of the agent
            **kwargs: Pattern-specific configuration
        """
        self.pattern = pattern
        self.name = name
        self.llm = llm
        self.tools = tools
        self.prompt = prompt
        self.description = description
        self.kwargs = kwargs

        # Validate configuration
        self._validate_config()

        # Initialize the agent factory mapping
        self.agent_factories = self._initialize_agent_factories()

        logger.info(f"Initialized AgentPatternRouter with pattern: {pattern}")

    def _validate_config(self):
        """Validate the router configuration."""
        if self.llm is None:
            logger.error("AgentPatternRouter: No LLM provided")
            raise ConfigurationError(
                "AgentPatternRouter: llm must be provided",
                details={"pattern": self.pattern}
            )

        if self.pattern not in [
            "self-consistency", "consistency",
            "reflexion",
            "reasoning-duo", "duo",
            "agent-judge", "judge",
            "react",
        ]:
            logger.error(f"AgentPatternRouter: Invalid pattern '{self.pattern}'")
            raise ValidationError(
                f"AgentPatternRouter: Invalid pattern '{self.pattern}'. "
                f"Must be one of: self-consistency, reflexion, reasoning-duo, agent-judge, react",
                details={
                    "requested_pattern": self.pattern,
                    "valid_patterns": ["self-consistency", "reflexion", "reasoning-duo", "agent-judge", "react"]
                }
            )

    def _initialize_agent_factories(self) -> Dict:
        """
        Initialize the agent factory mapping dictionary.

        Returns:
            Dict: Mapping of pattern names to factory functions
        """
        return {
            "self-consistency": self._create_self_consistency,
            "consistency": self._create_self_consistency,
            "reflexion": self._create_reflexion,
            "reasoning-duo": self._create_reasoning_duo,
            "duo": self._create_reasoning_duo,
            "agent-judge": self._create_agent_judge,
            "judge": self._create_agent_judge,
            "react": self._create_react,
        }

    def _create_self_consistency(self) -> BaseAgent:
        """Create a SelfConsistencyAgent instance."""
        num_samples = self.kwargs.get("num_samples", 5)
        majority_voting_prompt = self.kwargs.get("majority_voting_prompt", None)
        eval_mode = self.kwargs.get("eval_mode", False)
        rl_enabled = self.kwargs.get("rl_enabled", False)
        rl_manager = self.kwargs.get("rl_manager", None)
        reward_calculator = self.kwargs.get("reward_calculator", None)

        return SelfConsistencyAgent(
            name=self.name,
            llm=self.llm,
            tools=self.tools,
            prompt=self.prompt,
            description=self.description,
            num_samples=num_samples,
            majority_voting_prompt=majority_voting_prompt,
            eval_mode=eval_mode,
            rl_enabled=rl_enabled,
            rl_manager=rl_manager,
            reward_calculator=reward_calculator,
        )

    def _create_reflexion(self) -> BaseAgent:
        """Create a ReflexionAgent instance."""
        max_loops = self.kwargs.get("max_loops", 3)
        memory_capacity = self.kwargs.get("memory_capacity", 100)
        rl_enabled = self.kwargs.get("rl_enabled", False)
        rl_manager = self.kwargs.get("rl_manager", None)
        reward_calculator = self.kwargs.get("reward_calculator", None)

        return ReflexionAgent(
            name=self.name,
            llm=self.llm,
            tools=self.tools,
            prompt=self.prompt,
            description=self.description,
            max_loops=max_loops,
            memory_capacity=memory_capacity,
            rl_enabled=rl_enabled,
            rl_manager=rl_manager,
            reward_calculator=reward_calculator,
        )

    def _create_reasoning_duo(self) -> BaseAgent:
        """Create a ReasoningDuoAgent instance."""
        max_loops = self.kwargs.get("max_loops", 1)
        rl_enabled = self.kwargs.get("rl_enabled", False)
        rl_manager = self.kwargs.get("rl_manager", None)
        reward_calculator = self.kwargs.get("reward_calculator", None)

        return ReasoningDuoAgent(
            name=self.name,
            llm=self.llm,
            tools=self.tools,
            prompt=self.prompt,
            description=self.description,
            max_loops=max_loops,
            rl_enabled=rl_enabled,
            rl_manager=rl_manager,
            reward_calculator=reward_calculator,
        )

    def _create_agent_judge(self) -> BaseAgent:
        """Create an AgentJudge instance."""
        evaluation_criteria = self.kwargs.get("evaluation_criteria", None)
        return_score = self.kwargs.get("return_score", False)
        max_loops = self.kwargs.get("max_loops", 1)

        return AgentJudge(
            name=self.name,
            llm=self.llm,
            tools=self.tools,
            prompt=self.prompt,
            description=self.description,
            evaluation_criteria=evaluation_criteria,
            return_score=return_score,
            max_loops=max_loops,
        )

    def _create_react(self) -> BaseAgent:
        """Create a standard ReactAgent instance."""
        rl_enabled = self.kwargs.get("rl_enabled", False)
        rl_manager = self.kwargs.get("rl_manager", None)
        reward_calculator = self.kwargs.get("reward_calculator", None)

        return ReactAgent(
            name=self.name,
            llm=self.llm,
            tools=self.tools or [],
            prompt=self.prompt,
            rl_enabled=rl_enabled,
            rl_manager=rl_manager,
            reward_calculator=reward_calculator,
        )

    def create_agent(self) -> BaseAgent:
        """
        Create and return the selected agent pattern instance.

        Returns:
            BaseAgent: The instantiated agent

        Raises:
            ValueError: If an invalid pattern is specified
        """
        if self.pattern in self.agent_factories:
            return self.agent_factories[self.pattern]()
        else:
            logger.error(f"AgentPatternRouter: Invalid pattern '{self.pattern}'")
            raise ValidationError(
                f"AgentPatternRouter: Invalid pattern '{self.pattern}'",
                details={
                    "requested_pattern": self.pattern,
                    "available_patterns": list(self.agent_factories.keys())
                }
            )

    def invoke(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the selected agent pattern on the given state.

        Args:
            state (Dict[str, Any]): Current workflow state

        Returns:
            Dict[str, Any]: Updated state after agent execution
        """
        agent = self.create_agent()
        return agent.invoke(state)

    async def ainvoke(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Asynchronously execute the selected agent pattern.

        Args:
            state (Dict[str, Any]): Current workflow state

        Returns:
            Dict[str, Any]: Updated state
        """
        agent = self.create_agent()
        return await agent.ainvoke(state)

    def run_batch(
        self, states: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Execute the agent pattern on multiple states in batch.

        Args:
            states (List[Dict[str, Any]]): List of states to process

        Returns:
            List[Dict[str, Any]]: List of results
        """
        agent = self.create_agent()
        results = []
        
        for state in states:
            result = agent.invoke(state)
            results.append(result)
        
        return results

    def get_pattern_info(self) -> Dict[str, Any]:
        """
        Get information about the current pattern configuration.

        Returns:
            Dict[str, Any]: Pattern configuration details
        """
        return {
            "pattern": self.pattern,
            "name": self.name,
            "llm": str(self.llm),
            "tools_count": len(self.tools) if self.tools else 0,
            "description": self.description,
            "config": self.kwargs,
        }


# Convenience function for quick agent creation
def create_agent(
    pattern: AgentPattern,
    llm: BaseChatModel,
    **kwargs,
) -> BaseAgent:
    """
    Convenience function to create an agent with a specific pattern.

    Args:
        pattern (AgentPattern): The agent pattern to use
        llm (BaseChatModel): Language model to use
        **kwargs: Additional configuration for the pattern

    Returns:
        BaseAgent: The created agent instance

    Example:
        >>> from langchain_openai import ChatOpenAI
        >>> from azcore.agents.agent_pattern_router import create_agent
        >>> 
        >>> llm = ChatOpenAI(model="gpt-4o-mini")
        >>> agent = create_agent("self-consistency", llm, num_samples=5)
    """
    router = AgentPatternRouter(
        pattern=pattern,
        llm=llm,
        **kwargs,
    )
    return router.create_agent()
