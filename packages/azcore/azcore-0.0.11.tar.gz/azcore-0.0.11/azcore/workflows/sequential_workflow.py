"""
Sequential Workflow for Azcore.

Implements a linear chain workflow where the output of one agent
becomes the input for the next agent in sequence.

Use Cases:
- Step-by-step data transformation pipelines
- Report generation with multiple stages
- Sequential processing workflows
- Multi-stage analysis tasks
"""

import logging
from typing import List, Dict, Any, Optional, Callable, Union
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from azcore.core.base import BaseAgent
from azcore.exceptions import ValidationError

logger = logging.getLogger(__name__)


class SequentialWorkflow:
    """
    Linear chain workflow where agents execute in sequence.
    
    Each agent's output becomes the next agent's input, forming a
    processing pipeline. Useful for step-by-step transformations.
    
    Attributes:
        name (str): Workflow identifier
        agents (List): List of agents in execution order
        max_iterations (int): Maximum iterations per agent
        enable_memory (bool): Whether to maintain conversation history
    
    Example:
        >>> from azcore.workflows import SequentialWorkflow
        >>> 
        >>> # Create agents
        >>> researcher = SelfConsistencyAgent(name="Researcher", llm=llm, tools=tools)
        >>> analyst = ReflexionAgent(name="Analyst", llm=llm, tools=tools)
        >>> writer = ReactAgent(name="Writer", llm=llm, tools=tools)
        >>> 
        >>> # Create sequential workflow
        >>> workflow = SequentialWorkflow(
        ...     name="ResearchPipeline",
        ...     agents=[researcher, analyst, writer],
        ...     enable_memory=True
        ... )
        >>> 
        >>> # Execute workflow
        >>> result = workflow.run("Analyze AI trends and write a report")
        >>> print(result['output'])
    """
    
    def __init__(
        self,
        name: str,
        agents: List[Union[BaseAgent, Callable]],
        max_iterations: int = 1,
        enable_memory: bool = True,
        description: str = ""
    ):
        """
        Initialize SequentialWorkflow.
        
        Args:
            name: Workflow identifier
            agents: List of agents to execute in order
            max_iterations: Maximum iterations per agent (default: 1)
            enable_memory: Maintain conversation history (default: True)
            description: Workflow description
            
        Raises:
            ValidationError: If agents list is invalid
        """
        self.name = name
        self.agents = agents
        self.max_iterations = max_iterations
        self.enable_memory = enable_memory
        self.description = description or f"Sequential workflow: {name}"
        
        self._logger = logging.getLogger(f"{self.__class__.__name__}.{name}")
        self._conversation_history: List[BaseMessage] = []
        
        # Validation
        self._validate()
        
        self._logger.info(
            f"SequentialWorkflow '{name}' initialized with {len(agents)} agents"
        )
    
    def _validate(self):
        """Validate workflow configuration."""
        if not self.agents:
            raise ValidationError("SequentialWorkflow requires at least one agent")
        
        if self.max_iterations < 1:
            raise ValidationError("max_iterations must be >= 1")
        
        # Validate agents
        for i, agent in enumerate(self.agents):
            if not (isinstance(agent, BaseAgent) or callable(agent)):
                raise ValidationError(
                    f"Agent at index {i} must be BaseAgent or callable"
                )
    
    def run(
        self,
        initial_input: Union[str, Dict[str, Any]],
        config: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Execute the sequential workflow.
        
        Args:
            initial_input: Starting input (string or state dict)
            config: Optional configuration for execution
            
        Returns:
            Dict containing:
                - output: Final output from last agent
                - intermediate_outputs: List of outputs from each agent
                - conversation_history: Full conversation if memory enabled
                - metadata: Execution metadata
        """
        self._logger.info(f"Starting sequential workflow '{self.name}'")
        
        # Prepare initial state
        if isinstance(initial_input, str):
            state = {"messages": [HumanMessage(content=initial_input)]}
        else:
            state = initial_input
        
        # Track intermediate outputs
        intermediate_outputs = []
        agent_outputs = []
        
        # Execute agents sequentially
        for idx, agent in enumerate(self.agents):
            agent_name = getattr(agent, 'name', f'Agent_{idx}')
            self._logger.info(f"Executing agent {idx + 1}/{len(self.agents)}: {agent_name}")
            
            try:
                # Execute agent
                if hasattr(agent, 'invoke'):
                    result = agent.invoke(state)
                else:
                    result = agent(state)
                
                # Extract output
                if isinstance(result, dict) and 'messages' in result:
                    output_message = result['messages'][-1]
                    output_content = self._extract_content(output_message)
                    state = result  # Update state for next agent
                else:
                    output_content = str(result)
                    state = {"messages": state.get("messages", []) + [AIMessage(content=output_content)]}
                
                # Store intermediate output
                intermediate_outputs.append({
                    "agent": agent_name,
                    "output": output_content,
                    "step": idx + 1
                })
                agent_outputs.append(output_content)
                
                # Update conversation history if memory enabled
                if self.enable_memory and isinstance(state, dict) and 'messages' in state:
                    self._conversation_history.extend(state['messages'])
                
                self._logger.debug(f"Agent {agent_name} completed: {output_content[:100]}...")
                
            except Exception as e:
                self._logger.error(f"Error in agent {agent_name}: {e}")
                raise
        
        # Prepare final result
        final_output = agent_outputs[-1] if agent_outputs else ""
        
        result = {
            "output": final_output,
            "intermediate_outputs": intermediate_outputs,
            "conversation_history": self._conversation_history if self.enable_memory else [],
            "metadata": {
                "workflow": self.name,
                "agents_executed": len(self.agents),
                "total_steps": len(intermediate_outputs)
            }
        }
        
        self._logger.info(
            f"Sequential workflow '{self.name}' completed successfully "
            f"({len(self.agents)} agents)"
        )
        
        return result
    
    async def arun(
        self,
        initial_input: Union[str, Dict[str, Any]],
        config: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Asynchronously execute the sequential workflow.
        
        Args:
            initial_input: Starting input
            config: Optional configuration
            
        Returns:
            Dict with output and metadata
        """
        self._logger.info(f"Starting async sequential workflow '{self.name}'")
        
        # Prepare initial state
        if isinstance(initial_input, str):
            state = {"messages": [HumanMessage(content=initial_input)]}
        else:
            state = initial_input
        
        intermediate_outputs = []
        agent_outputs = []
        
        # Execute agents sequentially (async)
        for idx, agent in enumerate(self.agents):
            agent_name = getattr(agent, 'name', f'Agent_{idx}')
            
            try:
                if hasattr(agent, 'ainvoke'):
                    result = await agent.ainvoke(state)
                else:
                    result = agent(state)  # Fallback to sync
                
                if isinstance(result, dict) and 'messages' in result:
                    output_message = result['messages'][-1]
                    output_content = self._extract_content(output_message)
                    state = result
                else:
                    output_content = str(result)
                    state = {"messages": state.get("messages", []) + [AIMessage(content=output_content)]}
                
                intermediate_outputs.append({
                    "agent": agent_name,
                    "output": output_content,
                    "step": idx + 1
                })
                agent_outputs.append(output_content)
                
                if self.enable_memory and isinstance(state, dict) and 'messages' in state:
                    self._conversation_history.extend(state['messages'])
                
            except Exception as e:
                self._logger.error(f"Error in agent {agent_name}: {e}")
                raise
        
        final_output = agent_outputs[-1] if agent_outputs else ""
        
        return {
            "output": final_output,
            "intermediate_outputs": intermediate_outputs,
            "conversation_history": self._conversation_history if self.enable_memory else [],
            "metadata": {
                "workflow": self.name,
                "agents_executed": len(self.agents),
                "total_steps": len(intermediate_outputs)
            }
        }
    
    def add_agent(self, agent: Union[BaseAgent, Callable]) -> 'SequentialWorkflow':
        """
        Add an agent to the end of the sequence.
        
        Args:
            agent: Agent to add
            
        Returns:
            Self for method chaining
        """
        if not (isinstance(agent, BaseAgent) or callable(agent)):
            raise ValidationError("Agent must be BaseAgent or callable")
        
        self.agents.append(agent)
        self._logger.info(f"Added agent to workflow (total: {len(self.agents)})")
        
        return self
    
    def insert_agent(
        self,
        agent: Union[BaseAgent, Callable],
        position: int
    ) -> 'SequentialWorkflow':
        """
        Insert an agent at a specific position.
        
        Args:
            agent: Agent to insert
            position: Position to insert at (0-based)
            
        Returns:
            Self for method chaining
        """
        if not (isinstance(agent, BaseAgent) or callable(agent)):
            raise ValidationError("Agent must be BaseAgent or callable")
        
        if position < 0 or position > len(self.agents):
            raise ValidationError(f"Invalid position {position}")
        
        self.agents.insert(position, agent)
        self._logger.info(f"Inserted agent at position {position}")
        
        return self
    
    def remove_agent(self, index: int) -> 'SequentialWorkflow':
        """
        Remove an agent by index.
        
        Args:
            index: Agent index to remove
            
        Returns:
            Self for method chaining
        """
        if index < 0 or index >= len(self.agents):
            raise ValidationError(f"Invalid index {index}")
        
        removed = self.agents.pop(index)
        self._logger.info(f"Removed agent at index {index}")
        
        return self
    
    def clear_history(self):
        """Clear conversation history."""
        self._conversation_history = []
        self._logger.debug("Cleared conversation history")
    
    def get_agent_chain(self) -> List[str]:
        """
        Get list of agent names in execution order.
        
        Returns:
            List of agent names
        """
        return [
            getattr(agent, 'name', f'Agent_{i}')
            for i, agent in enumerate(self.agents)
        ]
    
    def _extract_content(self, message: Union[BaseMessage, Dict, str]) -> str:
        """Extract content from message."""
        if isinstance(message, str):
            return message
        if isinstance(message, dict):
            return message.get("content", str(message))
        return getattr(message, "content", str(message))
    
    def __repr__(self) -> str:
        """
        Return a string representation of the SequentialWorkflow instance.

        This method returns a string of the form
        "SequentialWorkflow(name='<name>', agents=[<agent1>, <agent2>, ...])"
        which is useful for debugging and logging purposes.

        Returns:
            str: A string representation of the SequentialWorkflow instance.
        """
        agent_names = ", ".join(self.get_agent_chain())
        return f"SequentialWorkflow(name='{self.name}', agents=[{agent_names}])"
    
    def __len__(self) -> int:
        """
        Return the number of agents in the workflow.
        
        This method returns the number of agents added to the workflow using the add_agent method.
        
        Returns:
            int: The number of agents in the workflow.
        """
        return len(self.agents)
