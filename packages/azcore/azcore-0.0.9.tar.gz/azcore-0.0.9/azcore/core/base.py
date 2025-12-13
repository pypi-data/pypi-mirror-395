"""
Base classes and abstract interfaces for the Azcore..

This module provides the foundational abstract base classes that define
the contract for agents, teams, and nodes in the framework.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Callable, Sequence
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.tools import BaseTool
from langgraph.types import Command
import logging

logger = logging.getLogger(__name__)


class BaseNode(ABC):
    """
    Abstract base class for all nodes in the framework.
    
    Nodes represent individual processing units in the agent workflow graph.
    Each node performs a specific task and can transition to other nodes.
    
    Attributes:
        name: Unique identifier for the node
        description: Human-readable description of the node's purpose
    """
    
    def __init__(self, name: str, description: str = ""):
        """
        Initialize a base node.
        
        Args:
            name: Unique identifier for the node
            description: Human-readable description of the node's purpose
        """
        self.name = name
        self.description = description
        self._logger = logging.getLogger(f"{self.__class__.__name__}.{name}")
    
    @abstractmethod
    def execute(self, state: Dict[str, Any]) -> Command:
        """
        Execute the node's logic.
        
        Args:
            state: Current state of the workflow
            
        Returns:
            Command object with updates and next node
        """
        pass
    
    def __call__(self, state: Dict[str, Any]) -> Command:
        """
        Make the node callable.
        
        Args:
            state: Current state of the workflow
            
        Returns:
            Command object from execute()
        """
        self._logger.info(f"Executing node: {self.name}")
        return self.execute(state)
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name='{self.name}')"


class BaseAgent(ABC):
    """
    Abstract base class for all agents in the framework.
    
    Agents are autonomous entities that can perform tasks using tools
    and language models. They can be simple or complex, with sub-graphs
    and multiple capabilities.
    
    Attributes:
        name: Unique identifier for the agent
        llm: Language model used by the agent
        tools: List of tools available to the agent
        prompt: System prompt for the agent
    """
    
    def __init__(
        self,
        name: str,
        llm: BaseChatModel,
        tools: Optional[Sequence[BaseTool]] = None,
        prompt: Optional[str] = None,
        description: str = ""
    ):
        """
        Initialize a base agent.
        
        Args:
            name: Unique identifier for the agent
            llm: Language model for the agent
            tools: Optional sequence of tools for the agent
            prompt: Optional system prompt
            description: Human-readable description
        """
        self.name = name
        self.llm = llm
        self.tools = list(tools) if tools else []
        self.prompt = prompt
        self.description = description
        self._logger = logging.getLogger(f"{self.__class__.__name__}.{name}")
        
    @abstractmethod
    def invoke(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Invoke the agent with the current state.
        
        Args:
            state: Current workflow state
            
        Returns:
            Updated state after agent execution
        """
        pass
    
    @abstractmethod
    async def ainvoke(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Asynchronously invoke the agent with the current state.
        
        Args:
            state: Current workflow state
            
        Returns:
            Updated state after agent execution
        """
        pass
    
    def add_tool(self, tool: BaseTool) -> None:
        """
        Add a tool to the agent's toolkit.
        
        Args:
            tool: Tool to add
        """
        if tool not in self.tools:
            self.tools.append(tool)
            self._logger.info(f"Added tool '{tool.name}' to agent '{self.name}'")
    
    def remove_tool(self, tool_name: str) -> bool:
        """
        Remove a tool from the agent's toolkit.
        
        Args:
            tool_name: Name of the tool to remove
            
        Returns:
            True if tool was removed, False otherwise
        """
        for i, tool in enumerate(self.tools):
            if tool.name == tool_name:
                self.tools.pop(i)
                self._logger.info(f"Removed tool '{tool_name}' from agent '{self.name}'")
                return True
        return False
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name='{self.name}', tools={len(self.tools)})"


class BaseTeam(ABC):
    """
    Abstract base class for teams in the framework.
    
    Teams are collections of agents that work together to accomplish
    complex tasks. They have their own sub-graphs and can contain
    supervisors, coordinators, and multiple specialized agents.
    
    Attributes:
        name: Unique identifier for the team
        description: Description of the team's purpose
        agents: List of agents in the team
        supervisor: Optional supervisor agent
    """
    
    def __init__(
        self,
        name: str,
        description: str = "",
        agents: Optional[List[BaseAgent]] = None
    ):
        """
        Initialize a base team.
        
        Args:
            name: Unique identifier for the team
            description: Description of the team's purpose
            agents: Optional list of initial agents
        """
        self.name = name
        self.description = description
        self.agents = agents if agents else []
        self.supervisor = None
        self._graph = None
        self._logger = logging.getLogger(f"{self.__class__.__name__}.{name}")
    
    @abstractmethod
    def build(self) -> Callable:
        """
        Build the team's graph and return a callable.
        
        Returns:
            Callable that represents the team's functionality
        """
        pass
    
    def add_agent(self, agent: BaseAgent) -> None:
        """
        Add an agent to the team.
        
        Args:
            agent: Agent to add to the team
        """
        if agent not in self.agents:
            self.agents.append(agent)
            self._logger.info(f"Added agent '{agent.name}' to team '{self.name}'")
    
    def remove_agent(self, agent_name: str) -> bool:
        """
        Remove an agent from the team.
        
        Args:
            agent_name: Name of the agent to remove
            
        Returns:
            True if agent was removed, False otherwise
        """
        for i, agent in enumerate(self.agents):
            if agent.name == agent_name:
                self.agents.pop(i)
                self._logger.info(f"Removed agent '{agent_name}' from team '{self.name}'")
                return True
        return False
    
    def get_agent(self, agent_name: str) -> Optional[BaseAgent]:
        """
        Get an agent by name.
        
        Args:
            agent_name: Name of the agent to retrieve
            
        Returns:
            Agent if found, None otherwise
        """
        for agent in self.agents:
            if agent.name == agent_name:
                return agent
        return None
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name='{self.name}', agents={len(self.agents)})"
