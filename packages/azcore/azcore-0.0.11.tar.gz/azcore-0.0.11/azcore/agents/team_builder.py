"""
TeamBuilder for constructing specialized teams with agents and sub-graphs.

This module provides the TeamBuilder class which uses a fluent interface
to construct teams with agents, supervisors, and custom workflows.
"""

from typing import Sequence, Optional, Callable, Any
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.tools import BaseTool
from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph, START
from langgraph.types import Command
from azcore.core.agent_executor import create_thinkat_agent
from azcore.core.base import BaseTeam
from azcore.core.state import State
from azcore.core.supervisor import Supervisor
from azcore.exceptions import TeamError, ConfigurationError
import logging

logger = logging.getLogger(__name__)

# Import RL components if available
try:
    from azcore.rl.rl_manager import RLManager
    from azcore.rl.rewards import RewardCalculator
    RL_AVAILABLE = True
except ImportError:
    RL_AVAILABLE = False
    RLManager = None
    RewardCalculator = None
    logger.debug("RL components not available")


class TeamBuilder(BaseTeam):
    """
    Builder for creating specialized agent teams.
    
    TeamBuilder uses a fluent interface pattern to construct teams with
    custom configurations, tools, prompts, and sub-graphs. Supports optional
    Reinforcement Learning for intelligent tool selection.
    
    Example (Standard Team):
        >>> team = (TeamBuilder("security_team")
        ...     .with_llm(llm)
        ...     .with_tools([camera_tool, alert_tool])
        ...     .with_prompt("You are a security monitoring agent...")
        ...     .with_description("Handles security-related tasks")
        ...     .build())
    
    Example (RL-Enabled Team):
        >>> from azcore.rl import RLManager, HeuristicRewardCalculator
        >>> rl_manager = RLManager(
        ...     tool_names=["camera_tool", "alert_tool"],
        ...     q_table_path="rl_data/security_q_table.pkl"
        ... )
        >>> reward_calc = HeuristicRewardCalculator()
        >>> team = (TeamBuilder("security_team")
        ...     .with_llm(llm)
        ...     .with_tools([camera_tool, alert_tool])
        ...     .with_prompt("You are a security monitoring agent...")
        ...     .with_rl(rl_manager, reward_calc)  # Enable RL!
        ...     .with_description("RL-optimized security team")
        ...     .build())
    """
    
    def __init__(self, name: str):
        """
        Initialize a team builder.
        
        Args:
            name: Unique identifier for the team
        """
        super().__init__(name=name)
        self._llm: Optional[BaseChatModel] = None
        self._tools: Sequence[BaseTool] = []
        self._prompt: Optional[str] = None
        self._sub_agent: Optional[Any] = None
        self._sub_graph: Optional[Any] = None
        self._built = False
        
        # RL components
        self._rl_enabled: bool = False
        self._rl_manager: Optional[Any] = None  # RLManager instance
        self._reward_calculator: Optional[Any] = None  # RewardCalculator instance
        
        self._logger = logging.getLogger(f"{self.__class__.__name__}.{name}")
    
    def with_llm(self, llm: BaseChatModel) -> 'TeamBuilder':
        """
        Set the language model for the team.
        
        Args:
            llm: Language model to use
            
        Returns:
            Self for method chaining
        """
        self._llm = llm
        self._logger.debug(f"Set LLM for team '{self.name}'")
        return self
    
    def with_tools(self, tools: Sequence[BaseTool]) -> 'TeamBuilder':
        """
        Set the tools available to the team.
        
        Args:
            tools: Sequence of tools
            
        Returns:
            Self for method chaining
        """
        self._tools = list(tools)
        tool_names = [tool.name for tool in tools]
        self._logger.info(f"Set {len(tools)} tools for team '{self.name}': {tool_names}")
        return self
    
    def with_prompt(self, prompt: str) -> 'TeamBuilder':
        """
        Set the system prompt for the team.
        
        Args:
            prompt: System prompt
            
        Returns:
            Self for method chaining
        """
        self._prompt = prompt
        self._logger.debug(f"Set prompt for team '{self.name}'")
        return self
    
    def with_description(self, description: str) -> 'TeamBuilder':
        """
        Set the team description.
        
        Args:
            description: Description of the team's purpose
            
        Returns:
            Self for method chaining
        """
        self.description = description
        return self
    
    def with_rl(
        self,
        rl_manager: Any,
        reward_calculator: Any
    ) -> 'TeamBuilder':
        """
        Enable Reinforcement Learning for intelligent tool selection.
        
        When RL is enabled, the team will use Q-learning to optimize
        which tools to select for different types of queries over time.
        
        Args:
            rl_manager: RLManager instance for Q-learning
            reward_calculator: RewardCalculator for computing rewards
            
        Returns:
            Self for method chaining
            
        Example:
            >>> from azcore.rl import RLManager, HeuristicRewardCalculator
            >>> rl_manager = RLManager(
            ...     tool_names=["tool1", "tool2"],
            ...     q_table_path="rl_data/team_q_table.pkl"
            ... )
            >>> reward_calc = HeuristicRewardCalculator()
            >>> team = (TeamBuilder("my_team")
            ...     .with_llm(llm)
            ...     .with_tools([tool1, tool2])
            ...     .with_rl(rl_manager, reward_calc)
            ...     .build())
        """
        if not RL_AVAILABLE:
            self._logger.warning(
                "RL components not available. "
                "RL will be disabled for this team."
            )
            return self
        
        self._rl_enabled = True
        self._rl_manager = rl_manager
        self._reward_calculator = reward_calculator
        
        self._logger.info(f"RL enabled for team '{self.name}'")
        return self
    
    def build(self) -> Callable:
        """
        Build the team and return a callable.
        
        This method constructs the internal sub-graph with a supervisor
        and agent node, then returns a callable that invokes the team.
        
        If RL is enabled via with_rl(), the team will use an RL-enabled
        ReactAgent for intelligent tool selection.
        
        Returns:
            Callable that represents the team's functionality
            
        Raises:
            ConfigurationError: If required components are not set
        """
        if self._built:
            self._logger.warning(f"Team '{self.name}' already built")
            return self._create_team_callable()
        
        if not self._llm:
            self._logger.error(f"Cannot build team '{self.name}': LLM not configured")
            raise ConfigurationError(
                f"LLM not set for team '{self.name}'. Use with_llm()",
                details={"team_name": self.name, "tools_count": len(self._tools)}
            )
        
        # Create agent based on RL configuration
        if self._rl_enabled and RL_AVAILABLE:
            self._logger.info(f"Building RL-enabled agent for team '{self.name}'")
            self._sub_agent = self._create_rl_agent()
        else:
            # Create standard agent
            self._sub_agent = create_thinkat_agent(
                model=self._llm,
                prompt=self._prompt,
                tools=self._tools,
            )
        
        # Build the sub-graph
        self._build_sub_graph()
        self._built = True
        
        rl_status = " with RL" if self._rl_enabled else ""
        self._logger.info(f"Built team '{self.name}' with {len(self._tools)} tools{rl_status}")
        
        return self._create_team_callable()
    
    def _create_rl_agent(self) -> Any:
        """
        Create an RL-enabled ReactAgent.
        
        Returns:
            RL-enabled ReactAgent instance
        """
        from azcore.agents.agent_factory import AgentFactory
        
        factory = AgentFactory(default_llm=self._llm)
        
        rl_agent = factory.create_react_agent(
            name=f"{self.name}_agent",
            tools=self._tools,
            prompt=self._prompt,
            description=self.description,
            rl_enabled=True,
            rl_manager=self._rl_manager,
            reward_calculator=self._reward_calculator
        )
        
        return rl_agent
    
    def _build_sub_graph(self) -> None:
        """Build the internal sub-graph for the team."""
        
        # For RL-enabled agents, invoke method is different
        if self._rl_enabled and hasattr(self._sub_agent, 'invoke'):
            def agent_node(state: State) -> Command:
                """Agent node for RL-enabled agent."""
                result = self._sub_agent.invoke(state)
                
                return Command(
                    update={
                        "messages": [
                            HumanMessage(
                                content=result["messages"][-1].content,
                                name=f"{self.name}_supervisor"
                            )
                        ]
                    },
                    goto="supervisor"
                )
        else:
            # Standard agent node
            def agent_node(state: State) -> Command:
                """Agent node that uses tools to complete tasks."""
                result = self._sub_agent.invoke(state)
                
                return Command(
                    update={
                        "messages": [
                            HumanMessage(
                                content=result["messages"][-1].content,
                                name=f"{self.name}_supervisor"
                            )
                        ]
                    },
                    goto="supervisor"
                )
        
        # Create supervisor for the sub-graph
        # The supervisor needs to route to "agent" not to self.name
        supervisor = Supervisor(
            llm=self._llm,
            members=[self.name]
        )
        supervisor_node = supervisor.create_node()
        
        # Build the sub-graph
        sub_graph_builder = StateGraph(State)
        sub_graph_builder.add_node("supervisor", supervisor_node)
        sub_graph_builder.add_node(self.name, agent_node)
        sub_graph_builder.add_edge(START, "supervisor")
        
        self._sub_graph = sub_graph_builder.compile()
        
        self._logger.debug(f"Built sub-graph for team '{self.name}'")
    
    def _create_team_callable(self) -> Callable:
        """Create the callable that represents the team."""
        
        def call_team(state: State) -> Command:
            """
            Invoke the team's sub-graph and return results.
            
            Args:
                state: Current workflow state
                
            Returns:
                Command with team's response
            """
            # Invoke the sub-graph with the last message
            response = self._sub_graph.invoke({
                "messages": state["messages"][-1:]
            })
            
            return Command(
                update={
                    "messages": [
                        HumanMessage(
                            content=response["messages"][-1].content,
                            name=self.name
                        )
                    ]
                },
                goto="supervisor"
            )
        
        return call_team
    
    def get_team_callable(self) -> Callable:
        """
        Get the team callable (builds if not already built).
        
        Returns:
            Team callable
        """
        if not self._built:
            return self.build()
        return self._create_team_callable()
    
    def is_built(self) -> bool:
        """
        Check if the team has been built.
        
        Returns:
            True if built, False otherwise
        """
        return self._built
    
    def get_tool_names(self) -> list[str]:
        """
        Get the names of all tools in the team.
        
        Returns:
            List of tool names
        """
        return [tool.name for tool in self._tools]
    
    def __repr__(self) -> str:
        status = "built" if self._built else "not built"
        rl_status = ", RL enabled" if self._rl_enabled else ""
        return f"TeamBuilder(name='{self.name}', tools={len(self._tools)}, {status}{rl_status})"
