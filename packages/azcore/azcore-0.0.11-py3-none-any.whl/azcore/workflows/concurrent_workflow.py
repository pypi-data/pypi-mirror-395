"""
Concurrent Workflow for Azcore.

Implements parallel execution of multiple agents for maximum efficiency.
All agents run simultaneously on the same input.

Use Cases:
- High-throughput batch processing
- Parallel data analysis
- Multiple perspectives on same problem
- Independent task execution
"""

import logging
import asyncio
from typing import List, Dict, Any, Optional, Callable, Union
from concurrent.futures import ThreadPoolExecutor, as_completed
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from azcore.core.base import BaseAgent
from azcore.exceptions import ValidationError

logger = logging.getLogger(__name__)


class ConcurrentWorkflow:
    """
    Parallel execution workflow for maximum efficiency.
    
    All agents execute simultaneously on the same input. Results are
    collected and can be aggregated using various strategies.
    
    Attributes:
        name (str): Workflow identifier
        agents (List): List of agents to execute in parallel
        max_workers (int): Maximum parallel workers
        aggregation_strategy (str): How to combine outputs
    
    Example:
        >>> from azcore.workflows import ConcurrentWorkflow
        >>> 
        >>> # Create multiple agents
        >>> analyst1 = ReactAgent(name="Analyst1", llm=llm, tools=tools1)
        >>> analyst2 = ReactAgent(name="Analyst2", llm=llm, tools=tools2)
        >>> analyst3 = ReactAgent(name="Analyst3", llm=llm, tools=tools3)
        >>> 
        >>> # Create concurrent workflow
        >>> workflow = ConcurrentWorkflow(
        ...     name="ParallelAnalysis",
        ...     agents=[analyst1, analyst2, analyst3],
        ...     aggregation_strategy="all",  # Keep all outputs
        ...     max_workers=3
        ... )
        >>> 
        >>> # Execute all agents in parallel
        >>> result = workflow.run("Analyze market trends")
        >>> print(result['aggregated_output'])
    """
    
    def __init__(
        self,
        name: str,
        agents: List[Union[BaseAgent, Callable]],
        aggregation_strategy: str = "all",
        max_workers: Optional[int] = None,
        timeout: Optional[float] = None,
        description: str = ""
    ):
        """
        Initialize ConcurrentWorkflow.
        
        Args:
            name: Workflow identifier
            agents: List of agents to execute in parallel
            aggregation_strategy: Output aggregation method
                - "all": Return all outputs (default)
                - "first": Return first completed output
                - "majority": Use majority voting (requires similar outputs)
                - "concat": Concatenate all outputs
                - "best": Select best output (requires scoring)
            max_workers: Maximum parallel workers (default: None = auto)
            timeout: Execution timeout in seconds (default: None)
            description: Workflow description
            
        Raises:
            ValidationError: If configuration is invalid
        """
        self.name = name
        self.agents = agents
        self.aggregation_strategy = aggregation_strategy
        self.max_workers = max_workers or min(len(agents), 10)
        self.timeout = timeout
        self.description = description or f"Concurrent workflow: {name}"
        
        self._logger = logging.getLogger(f"{self.__class__.__name__}.{name}")
        
        # Validation
        self._validate()
        
        self._logger.info(
            f"ConcurrentWorkflow '{name}' initialized with {len(agents)} agents "
            f"(max_workers={self.max_workers})"
        )
    
    def _validate(self):
        """Validate workflow configuration."""
        if not self.agents:
            raise ValidationError("ConcurrentWorkflow requires at least one agent")
        
        valid_strategies = ["all", "first", "majority", "concat", "best"]
        if self.aggregation_strategy not in valid_strategies:
            raise ValidationError(
                f"Invalid aggregation_strategy '{self.aggregation_strategy}'. "
                f"Must be one of: {valid_strategies}"
            )
        
        if self.max_workers < 1:
            raise ValidationError("max_workers must be >= 1")
        
        # Validate agents
        for i, agent in enumerate(self.agents):
            if not (isinstance(agent, BaseAgent) or callable(agent)):
                raise ValidationError(
                    f"Agent at index {i} must be BaseAgent or callable"
                )
    
    def run(
        self,
        input_data: Union[str, Dict[str, Any]],
        config: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Execute all agents concurrently.
        
        Args:
            input_data: Input for all agents (string or state dict)
            config: Optional configuration
            
        Returns:
            Dict containing:
                - aggregated_output: Aggregated result based on strategy
                - individual_outputs: List of outputs from each agent
                - execution_times: Execution time for each agent
                - metadata: Execution metadata
        """
        self._logger.info(
            f"Starting concurrent workflow '{self.name}' "
            f"with {len(self.agents)} agents"
        )
        
        # Prepare input state
        if isinstance(input_data, str):
            state = {"messages": [HumanMessage(content=input_data)]}
        else:
            state = input_data
        
        # Execute agents in parallel using ThreadPoolExecutor
        individual_outputs = []
        execution_times = {}
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all agent tasks
            future_to_agent = {
                executor.submit(self._execute_agent, agent, state, idx): (agent, idx)
                for idx, agent in enumerate(self.agents)
            }
            
            # Collect results as they complete
            for future in as_completed(future_to_agent, timeout=self.timeout):
                agent, idx = future_to_agent[future]
                agent_name = getattr(agent, 'name', f'Agent_{idx}')
                
                try:
                    result = future.result()
                    individual_outputs.append({
                        "agent": agent_name,
                        "output": result['output'],
                        "execution_time": result['execution_time'],
                        "index": idx
                    })
                    execution_times[agent_name] = result['execution_time']
                    
                    self._logger.debug(
                        f"Agent {agent_name} completed in {result['execution_time']:.2f}s"
                    )
                    
                except Exception as e:
                    self._logger.error(f"Agent {agent_name} failed: {e}")
                    individual_outputs.append({
                        "agent": agent_name,
                        "output": None,
                        "error": str(e),
                        "index": idx
                    })
        
        # Sort outputs by original agent order
        individual_outputs.sort(key=lambda x: x['index'])
        
        # Aggregate outputs based on strategy
        aggregated_output = self._aggregate_outputs(individual_outputs)
        
        result = {
            "aggregated_output": aggregated_output,
            "individual_outputs": individual_outputs,
            "execution_times": execution_times,
            "metadata": {
                "workflow": self.name,
                "agents_executed": len(self.agents),
                "aggregation_strategy": self.aggregation_strategy,
                "total_agents": len(self.agents),
                "successful_agents": sum(1 for o in individual_outputs if o.get('output'))
            }
        }
        
        self._logger.info(
            f"Concurrent workflow '{self.name}' completed "
            f"({len(individual_outputs)} agents)"
        )
        
        return result
    
    async def arun(
        self,
        input_data: Union[str, Dict[str, Any]],
        config: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Asynchronously execute all agents concurrently.
        
        Args:
            input_data: Input for all agents
            config: Optional configuration
            
        Returns:
            Dict with aggregated and individual outputs
        """
        self._logger.info(f"Starting async concurrent workflow '{self.name}'")
        
        # Prepare input state
        if isinstance(input_data, str):
            state = {"messages": [HumanMessage(content=input_data)]}
        else:
            state = input_data
        
        # Execute agents concurrently using asyncio
        tasks = [
            self._execute_agent_async(agent, state, idx)
            for idx, agent in enumerate(self.agents)
        ]
        
        # Wait for all tasks to complete
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Process results
        individual_outputs = []
        execution_times = {}
        
        for idx, (agent, result) in enumerate(zip(self.agents, results)):
            agent_name = getattr(agent, 'name', f'Agent_{idx}')
            
            if isinstance(result, Exception):
                self._logger.error(f"Agent {agent_name} failed: {result}")
                individual_outputs.append({
                    "agent": agent_name,
                    "output": None,
                    "error": str(result),
                    "index": idx
                })
            else:
                individual_outputs.append({
                    "agent": agent_name,
                    "output": result['output'],
                    "execution_time": result['execution_time'],
                    "index": idx
                })
                execution_times[agent_name] = result['execution_time']
        
        # Aggregate outputs
        aggregated_output = self._aggregate_outputs(individual_outputs)
        
        return {
            "aggregated_output": aggregated_output,
            "individual_outputs": individual_outputs,
            "execution_times": execution_times,
            "metadata": {
                "workflow": self.name,
                "agents_executed": len(self.agents),
                "aggregation_strategy": self.aggregation_strategy,
                "successful_agents": sum(1 for o in individual_outputs if o.get('output'))
            }
        }
    
    def _execute_agent(
        self,
        agent: Union[BaseAgent, Callable],
        state: Dict[str, Any],
        idx: int
    ) -> Dict[str, Any]:
        """Execute a single agent and track timing."""
        import time
        
        start_time = time.time()
        agent_name = getattr(agent, 'name', f'Agent_{idx}')
        
        try:
            if hasattr(agent, 'invoke'):
                result = agent.invoke(state)
            else:
                result = agent(state)
            
            # Extract output
            if isinstance(result, dict) and 'messages' in result:
                output = self._extract_content(result['messages'][-1])
            else:
                output = str(result)
            
            execution_time = time.time() - start_time
            
            return {
                "output": output,
                "execution_time": execution_time
            }
            
        except Exception as e:
            execution_time = time.time() - start_time
            self._logger.error(f"Error in agent {agent_name}: {e}")
            raise
    
    async def _execute_agent_async(
        self,
        agent: Union[BaseAgent, Callable],
        state: Dict[str, Any],
        idx: int
    ) -> Dict[str, Any]:
        """Asynchronously execute a single agent."""
        import time
        
        start_time = time.time()
        
        try:
            if hasattr(agent, 'ainvoke'):
                result = await agent.ainvoke(state)
            elif hasattr(agent, 'invoke'):
                result = agent.invoke(state)
            else:
                result = agent(state)
            
            if isinstance(result, dict) and 'messages' in result:
                output = self._extract_content(result['messages'][-1])
            else:
                output = str(result)
            
            execution_time = time.time() - start_time
            
            return {
                "output": output,
                "execution_time": execution_time
            }
            
        except Exception as e:
            execution_time = time.time() - start_time
            raise
    
    def _aggregate_outputs(self, outputs: List[Dict[str, Any]]) -> str:
        """Aggregate agent outputs based on strategy."""
        # Filter successful outputs
        successful = [o for o in outputs if o.get('output')]
        
        if not successful:
            return "All agents failed to produce output"
        
        if self.aggregation_strategy == "all":
            # Return all outputs as structured data
            return "\n\n---\n\n".join([
                f"Agent: {o['agent']}\nOutput: {o['output']}"
                for o in successful
            ])
        
        elif self.aggregation_strategy == "first":
            # Return first completed output
            return successful[0]['output']
        
        elif self.aggregation_strategy == "concat":
            # Concatenate all outputs
            return " ".join([o['output'] for o in successful])
        
        elif self.aggregation_strategy == "majority":
            # Simple majority voting (returns most common output)
            from collections import Counter
            outputs_list = [o['output'] for o in successful]
            counter = Counter(outputs_list)
            most_common = counter.most_common(1)[0][0]
            return most_common
        
        elif self.aggregation_strategy == "best":
            # Return longest output as "best" (simple heuristic)
            best = max(successful, key=lambda o: len(o['output']))
            return best['output']
        
        else:
            return successful[0]['output']
    
    def add_agent(self, agent: Union[BaseAgent, Callable]) -> 'ConcurrentWorkflow':
        """
        Add an agent to the workflow.
        
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
    
    def _extract_content(self, message: Union[BaseMessage, Dict, str]) -> str:
        """Extract content from message."""
        if isinstance(message, str):
            return message
        if isinstance(message, dict):
            return message.get("content", str(message))
        return getattr(message, "content", str(message))
    
    def __repr__(self) -> str:
        """Return a string representation of the ConcurrentWorkflow instance.

        This method returns a string of the form
        "ConcurrentWorkflow(name='<name>', agents=<num_agents>, strategy='<strategy>')"
        which is useful for debugging and logging purposes.

        Returns:
            str: A string representation of the ConcurrentWorkflow instance."""
        agent_names = [getattr(a, 'name', f'Agent_{i}') for i, a in enumerate(self.agents)]
        return f"ConcurrentWorkflow(name='{self.name}', agents={len(agent_names)}, strategy='{self.aggregation_strategy}')"
    
    def __len__(self) -> int:
        """Return the number of agents in the workflow.

        This method returns the number of agents added to the workflow using the add_agent method.

        Returns:
            int: The number of agents in the workflow."""
        return len(self.agents)
