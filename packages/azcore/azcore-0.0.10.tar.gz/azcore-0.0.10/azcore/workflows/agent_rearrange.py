"""
Agent Rearrange for Azcore.

Dynamically maps complex relationships between agents (e.g., a -> b, c).
Provides flexible and adaptive workflows with dynamic routing.

Use Cases:
- Flexible task distribution
- Dynamic agent routing based on conditions
- Adaptive workflows
- Complex agent relationships
"""

import logging
from typing import List, Dict, Any, Optional, Callable, Union, Set, Tuple
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from azcore.core.base import BaseAgent
from azcore.exceptions import ValidationError, GraphCycleError

logger = logging.getLogger(__name__)


class AgentRearrange:
    """
    Dynamic agent relationship mapper with flexible routing.
    
    Allows defining complex agent relationships like:
    - Agent A -> Agent B, Agent C (one-to-many)
    - Agent A, Agent B -> Agent C (many-to-one)
    - Conditional routing based on output
    
    Attributes:
        name (str): Workflow identifier
        agents (Dict): Dictionary of agent_id -> agent
        relationships (List): List of (from_agent, to_agents) tuples
    
    Example:
        >>> from azcore.workflows import AgentRearrange
        >>> 
        >>> # Create agents
        >>> coordinator = ReactAgent(name="Coordinator", llm=llm)
        >>> researcher1 = ReactAgent(name="Researcher1", llm=llm)
        >>> researcher2 = ReactAgent(name="Researcher2", llm=llm)
        >>> synthesizer = ReactAgent(name="Synthesizer", llm=llm)
        >>> 
        >>> # Create rearrange workflow
        >>> workflow = AgentRearrange(name="DynamicResearch")
        >>> workflow.add_agent("coord", coordinator)
        >>> workflow.add_agent("r1", researcher1)
        >>> workflow.add_agent("r2", researcher2)
        >>> workflow.add_agent("synth", synthesizer)
        >>> 
        >>> # Define relationships: coord -> r1, r2 -> synth
        >>> workflow.add_relationship("coord", ["r1", "r2"])
        >>> workflow.add_relationship("r1", ["synth"])
        >>> workflow.add_relationship("r2", ["synth"])
        >>> workflow.set_entry_point("coord")
        >>> 
        >>> # Execute with dynamic routing
        >>> result = workflow.run("Research AI safety")
    """
    
    def __init__(
        self,
        name: str,
        enable_cycle_detection: bool = True,
        description: str = ""
    ):
        """
        Initialize AgentRearrange workflow.
        
        Args:
            name: Workflow identifier
            enable_cycle_detection: Check for cycles (default: True)
            description: Workflow description
        """
        self.name = name
        self.enable_cycle_detection = enable_cycle_detection
        self.description = description or f"Agent Rearrange workflow: {name}"
        
        self._agents: Dict[str, Union[BaseAgent, Callable]] = {}
        self._relationships: Dict[str, List[str]] = {}
        self._entry_point: Optional[str] = None
        self._terminal_agents: Set[str] = set()
        
        self._logger = logging.getLogger(f"{self.__class__.__name__}.{name}")
        self._logger.info(f"AgentRearrange '{name}' initialized")
    
    def add_agent(
        self,
        agent_id: str,
        agent: Union[BaseAgent, Callable],
        is_terminal: bool = False
    ) -> 'AgentRearrange':
        """
        Add an agent to the workflow.
        
        Args:
            agent_id: Unique identifier for the agent
            agent: Agent instance or callable
            is_terminal: Whether this agent is a terminal node (default: False)
            
        Returns:
            Self for method chaining
            
        Raises:
            ValidationError: If agent_id already exists
        """
        if agent_id in self._agents:
            raise ValidationError(f"Agent ID '{agent_id}' already exists")
        
        if not (isinstance(agent, BaseAgent) or callable(agent)):
            raise ValidationError("Agent must be BaseAgent or callable")
        
        self._agents[agent_id] = agent
        
        if is_terminal:
            self._terminal_agents.add(agent_id)
        
        self._logger.debug(f"Added agent '{agent_id}'")
        
        return self
    
    def add_relationship(
        self,
        from_agent: str,
        to_agents: Union[str, List[str]],
        condition: Optional[Callable] = None
    ) -> 'AgentRearrange':
        """
        Add a relationship between agents.
        
        Args:
            from_agent: Source agent ID
            to_agents: Target agent ID(s)
            condition: Optional condition function for routing
            
        Returns:
            Self for method chaining
            
        Raises:
            ValidationError: If agents don't exist
            GraphCycleError: If relationship would create cycle
        """
        if from_agent not in self._agents:
            raise ValidationError(f"Agent '{from_agent}' not found")
        
        # Convert single agent to list
        if isinstance(to_agents, str):
            to_agents = [to_agents]
        
        # Validate target agents
        for to_agent in to_agents:
            if to_agent not in self._agents:
                raise ValidationError(f"Agent '{to_agent}' not found")
        
        # Check for cycles if enabled
        if self.enable_cycle_detection:
            for to_agent in to_agents:
                if self._would_create_cycle(from_agent, to_agent):
                    raise GraphCycleError(
                        f"Relationship {from_agent} -> {to_agent} would create cycle"
                    )
        
        # Store relationship
        if from_agent not in self._relationships:
            self._relationships[from_agent] = []
        
        self._relationships[from_agent].extend(to_agents)
        
        self._logger.debug(f"Added relationship: {from_agent} -> {to_agents}")
        
        return self
    
    def set_entry_point(self, agent_id: str) -> 'AgentRearrange':
        """
        Set the entry point agent.
        
        Args:
            agent_id: ID of the entry agent
            
        Returns:
            Self for method chaining
        """
        if agent_id not in self._agents:
            raise ValidationError(f"Agent '{agent_id}' not found")
        
        self._entry_point = agent_id
        self._logger.info(f"Set entry point: {agent_id}")
        
        return self
    
    def run(
        self,
        initial_input: Union[str, Dict[str, Any]],
        config: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Execute the workflow with dynamic routing.
        
        Args:
            initial_input: Starting input
            config: Optional configuration
            
        Returns:
            Dict containing:
                - output: Final output
                - execution_trace: Trace of agent executions
                - agent_outputs: All agent outputs
                - metadata: Execution metadata
        """
        if not self._entry_point:
            raise ValidationError("Entry point not set. Call set_entry_point() first.")
        
        self._logger.info(f"Starting AgentRearrange workflow '{self.name}'")
        
        # Prepare initial state
        if isinstance(initial_input, str):
            state = {"messages": [HumanMessage(content=initial_input)]}
        else:
            state = initial_input
        
        # Track execution
        execution_trace = []
        agent_outputs = {}
        states_by_agent = {self._entry_point: state}
        
        # BFS execution with dynamic routing
        queue = [self._entry_point]
        visited = set()
        
        while queue:
            current_agent_id = queue.pop(0)
            
            if current_agent_id in visited:
                continue
            
            visited.add(current_agent_id)
            current_agent = self._agents[current_agent_id]
            current_state = states_by_agent.get(current_agent_id, state)
            
            self._logger.debug(f"Executing agent: {current_agent_id}")
            
            # Execute agent
            try:
                if hasattr(current_agent, 'invoke'):
                    result = current_agent.invoke(current_state)
                else:
                    result = current_agent(current_state)
                
                # Extract output
                if isinstance(result, dict) and 'messages' in result:
                    output = self._extract_content(result['messages'][-1])
                    result_state = result
                else:
                    output = str(result)
                    result_state = {
                        "messages": current_state.get("messages", []) + [AIMessage(content=output)]
                    }
                
                # Store output
                agent_outputs[current_agent_id] = output
                execution_trace.append({
                    "agent": current_agent_id,
                    "output": output
                })
                
                self._logger.debug(f"Agent {current_agent_id} completed")
                
                # Route to next agents
                next_agents = self._relationships.get(current_agent_id, [])
                for next_agent_id in next_agents:
                    if next_agent_id not in visited:
                        states_by_agent[next_agent_id] = result_state
                        queue.append(next_agent_id)
                
            except Exception as e:
                self._logger.error(f"Error in agent {current_agent_id}: {e}")
                agent_outputs[current_agent_id] = f"ERROR: {e}"
                execution_trace.append({
                    "agent": current_agent_id,
                    "error": str(e)
                })
        
        # Get final output (from terminal agents or last executed)
        final_output = self._get_final_output(agent_outputs, execution_trace)
        
        result = {
            "output": final_output,
            "execution_trace": execution_trace,
            "agent_outputs": agent_outputs,
            "metadata": {
                "workflow": self.name,
                "agents_executed": len(visited),
                "total_agents": len(self._agents),
                "entry_point": self._entry_point
            }
        }
        
        self._logger.info(
            f"AgentRearrange workflow '{self.name}' completed "
            f"({len(visited)} agents executed)"
        )
        
        return result
    
    def _would_create_cycle(self, from_agent: str, to_agent: str) -> bool:
        """Check if adding edge would create cycle using DFS."""
        visited = set()
        
        def dfs(node: str) -> bool:
            if node == from_agent:
                return True
            if node in visited:
                return False
            
            visited.add(node)
            
            for next_node in self._relationships.get(node, []):
                if dfs(next_node):
                    return True
            
            return False
        
        return dfs(to_agent)
    
    def _get_final_output(
        self,
        agent_outputs: Dict[str, str],
        execution_trace: List[Dict[str, Any]]
    ) -> str:
        """Determine final output from terminal agents or last executed."""
        # Check terminal agents first
        terminal_outputs = [
            agent_outputs[agent_id]
            for agent_id in self._terminal_agents
            if agent_id in agent_outputs
        ]
        
        if terminal_outputs:
            return "\n\n".join(terminal_outputs)
        
        # Fall back to last executed agent
        if execution_trace:
            last_execution = execution_trace[-1]
            return last_execution.get('output', last_execution.get('error', ''))
        
        return "No output generated"
    
    def get_graph_structure(self) -> Dict[str, Any]:
        """
        Get the graph structure.
        
        Returns:
            Dict with agents and relationships
        """
        return {
            "agents": list(self._agents.keys()),
            "relationships": self._relationships,
            "entry_point": self._entry_point,
            "terminal_agents": list(self._terminal_agents)
        }
    
    def _extract_content(self, message: Union[BaseMessage, Dict, str]) -> str:
        """Extract content from message."""
        if isinstance(message, str):
            return message
        if isinstance(message, dict):
            return message.get("content", str(message))
        return getattr(message, "content", str(message))
    
    def __repr__(self) -> str:
        return (
            f"AgentRearrange(name='{self.name}', "
            f"agents={len(self._agents)}, "
            f"relationships={len(self._relationships)})"
        )
