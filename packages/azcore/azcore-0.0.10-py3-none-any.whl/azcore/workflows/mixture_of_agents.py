"""
Mixture of Agents (MoA) for Azcore.

Utilizes multiple expert agents in parallel and synthesizes their outputs.
Achieves state-of-the-art performance through collaborative intelligence.

Use Cases:
- Complex problem-solving requiring multiple perspectives
- Expert collaboration and consensus building
- State-of-the-art performance through aggregation
- Multi-expert decision making
"""

import logging
from typing import List, Dict, Any, Optional, Callable, Union
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langchain_core.language_models.chat_models import BaseChatModel
from azcore.core.base import BaseAgent
from azcore.exceptions import ValidationError

logger = logging.getLogger(__name__)


class MixtureOfAgents:
    """
    Mixture of Agents workflow with expert synthesis.
    
    Multiple expert agents process the same input in parallel, then
    a synthesizer agent aggregates their outputs into a final response.
    
    Attributes:
        name (str): Workflow identifier
        expert_agents (List): List of expert agents
        synthesizer_agent: Agent for synthesizing expert outputs
        aggregation_method (str): How to present outputs to synthesizer
    
    Example:
        >>> from azcore.workflows import MixtureOfAgents
        >>> from azcore.agents import ReactAgent
        >>> 
        >>> # Create expert agents
        >>> expert1 = ReactAgent(name="Expert1", llm=llm, tools=tools1)
        >>> expert2 = ReactAgent(name="Expert2", llm=llm, tools=tools2)
        >>> expert3 = ReactAgent(name="Expert3", llm=llm, tools=tools3)
        >>> 
        >>> # Create synthesizer
        >>> synthesizer = ReactAgent(name="Synthesizer", llm=llm, 
        ...     prompt="Synthesize multiple expert opinions into a coherent answer")
        >>> 
        >>> # Create MoA workflow
        >>> moa = MixtureOfAgents(
        ...     name="ExpertConsensus",
        ...     expert_agents=[expert1, expert2, expert3],
        ...     synthesizer_agent=synthesizer,
        ...     aggregation_method="structured"
        ... )
        >>> 
        >>> # Execute
        >>> result = moa.run("What is the future of quantum computing?")
        >>> print(result['synthesized_output'])
    """
    
    def __init__(
        self,
        name: str,
        expert_agents: List[Union[BaseAgent, Callable]],
        synthesizer_agent: Union[BaseAgent, Callable],
        aggregation_method: str = "structured",
        max_workers: Optional[int] = None,
        description: str = ""
    ):
        """
        Initialize Mixture of Agents workflow.
        
        Args:
            name: Workflow identifier
            expert_agents: List of expert agents
            synthesizer_agent: Agent for synthesizing outputs
            aggregation_method: How to aggregate expert outputs
                - "structured": Format with headers (default)
                - "concat": Simple concatenation
                - "weighted": Weighted combination (requires weights)
            max_workers: Max parallel workers for experts
            description: Workflow description
            
        Raises:
            ValidationError: If configuration is invalid
        """
        self.name = name
        self.expert_agents = expert_agents
        self.synthesizer_agent = synthesizer_agent
        self.aggregation_method = aggregation_method
        self.max_workers = max_workers or min(len(expert_agents), 10)
        self.description = description or f"Mixture of Agents: {name}"
        
        self._logger = logging.getLogger(f"{self.__class__.__name__}.{name}")
        
        # Validation
        self._validate()
        
        self._logger.info(
            f"MixtureOfAgents '{name}' initialized with "
            f"{len(expert_agents)} experts"
        )
    
    def _validate(self):
        """Validate workflow configuration."""
        if not self.expert_agents:
            raise ValidationError("MixtureOfAgents requires at least one expert agent")
        
        if not self.synthesizer_agent:
            raise ValidationError("MixtureOfAgents requires a synthesizer agent")
        
        valid_methods = ["structured", "concat", "weighted"]
        if self.aggregation_method not in valid_methods:
            raise ValidationError(
                f"Invalid aggregation_method '{self.aggregation_method}'. "
                f"Must be one of: {valid_methods}"
            )
        
        # Validate agents
        for i, agent in enumerate(self.expert_agents):
            if not (isinstance(agent, BaseAgent) or callable(agent)):
                raise ValidationError(
                    f"Expert agent at index {i} must be BaseAgent or callable"
                )
        
        if not (isinstance(self.synthesizer_agent, BaseAgent) or 
                callable(self.synthesizer_agent)):
            raise ValidationError("Synthesizer agent must be BaseAgent or callable")
    
    def run(
        self,
        input_data: Union[str, Dict[str, Any]],
        config: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Execute the Mixture of Agents workflow.
        
        Args:
            input_data: Input for all expert agents
            config: Optional configuration
            
        Returns:
            Dict containing:
                - synthesized_output: Final synthesized output
                - expert_outputs: Individual expert outputs
                - synthesis_prompt: Prompt used for synthesis
                - metadata: Execution metadata
        """
        self._logger.info(f"Starting MixtureOfAgents '{self.name}'")
        
        # Prepare input state
        if isinstance(input_data, str):
            state = {"messages": [HumanMessage(content=input_data)]}
            input_text = input_data
        else:
            state = input_data
            input_text = self._extract_content(state['messages'][0])
        
        # Step 1: Run all expert agents in parallel
        self._logger.info("Phase 1: Collecting expert opinions...")
        expert_outputs = self._run_experts(state)
        
        # Step 2: Aggregate expert outputs
        self._logger.info("Phase 2: Aggregating expert outputs...")
        aggregated_text = self._aggregate_expert_outputs(expert_outputs, input_text)
        
        # Step 3: Synthesize using synthesizer agent
        self._logger.info("Phase 3: Synthesizing final output...")
        synthesis_state = {
            "messages": [HumanMessage(content=aggregated_text)]
        }
        
        synthesized_output = self._run_synthesizer(synthesis_state)
        
        result = {
            "synthesized_output": synthesized_output,
            "expert_outputs": expert_outputs,
            "synthesis_prompt": aggregated_text,
            "metadata": {
                "workflow": self.name,
                "num_experts": len(self.expert_agents),
                "aggregation_method": self.aggregation_method
            }
        }
        
        self._logger.info(f"MixtureOfAgents '{self.name}' completed")
        
        return result
    
    async def arun(
        self,
        input_data: Union[str, Dict[str, Any]],
        config: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Asynchronously execute the Mixture of Agents workflow.
        
        Args:
            input_data: Input for all expert agents
            config: Optional configuration
            
        Returns:
            Dict with synthesized output and expert outputs
        """
        import asyncio
        
        self._logger.info(f"Starting async MixtureOfAgents '{self.name}'")
        
        # Prepare input
        if isinstance(input_data, str):
            state = {"messages": [HumanMessage(content=input_data)]}
            input_text = input_data
        else:
            state = input_data
            input_text = self._extract_content(state['messages'][0])
        
        # Run experts concurrently
        expert_tasks = [
            self._execute_expert_async(agent, state, idx)
            for idx, agent in enumerate(self.expert_agents)
        ]
        
        expert_results = await asyncio.gather(*expert_tasks, return_exceptions=True)
        
        # Process expert outputs
        expert_outputs = []
        for idx, (agent, result) in enumerate(zip(self.expert_agents, expert_results)):
            agent_name = getattr(agent, 'name', f'Expert_{idx}')
            
            if isinstance(result, Exception):
                self._logger.error(f"Expert {agent_name} failed: {result}")
                expert_outputs.append({
                    "agent": agent_name,
                    "output": f"ERROR: {result}"
                })
            else:
                expert_outputs.append({
                    "agent": agent_name,
                    "output": result
                })
        
        # Aggregate and synthesize
        aggregated_text = self._aggregate_expert_outputs(expert_outputs, input_text)
        synthesis_state = {"messages": [HumanMessage(content=aggregated_text)]}
        
        synthesized_output = await self._run_synthesizer_async(synthesis_state)
        
        return {
            "synthesized_output": synthesized_output,
            "expert_outputs": expert_outputs,
            "synthesis_prompt": aggregated_text,
            "metadata": {
                "workflow": self.name,
                "num_experts": len(self.expert_agents),
                "aggregation_method": self.aggregation_method
            }
        }
    
    def _run_experts(self, state: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Run all expert agents in parallel."""
        from concurrent.futures import ThreadPoolExecutor, as_completed
        
        expert_outputs = []
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_agent = {
                executor.submit(self._execute_expert, agent, state, idx): (agent, idx)
                for idx, agent in enumerate(self.expert_agents)
            }
            
            for future in as_completed(future_to_agent):
                agent, idx = future_to_agent[future]
                agent_name = getattr(agent, 'name', f'Expert_{idx}')
                
                try:
                    output = future.result()
                    expert_outputs.append({
                        "agent": agent_name,
                        "output": output,
                        "index": idx
                    })
                    self._logger.debug(f"Expert {agent_name} completed")
                    
                except Exception as e:
                    self._logger.error(f"Expert {agent_name} failed: {e}")
                    expert_outputs.append({
                        "agent": agent_name,
                        "output": f"ERROR: {e}",
                        "index": idx
                    })
        
        # Sort by original order
        expert_outputs.sort(key=lambda x: x['index'])
        
        return expert_outputs
    
    def _execute_expert(
        self,
        agent: Union[BaseAgent, Callable],
        state: Dict[str, Any],
        idx: int
    ) -> str:
        """Execute a single expert agent."""
        if hasattr(agent, 'invoke'):
            result = agent.invoke(state)
        else:
            result = agent(state)
        
        if isinstance(result, dict) and 'messages' in result:
            return self._extract_content(result['messages'][-1])
        else:
            return str(result)
    
    async def _execute_expert_async(
        self,
        agent: Union[BaseAgent, Callable],
        state: Dict[str, Any],
        idx: int
    ) -> str:
        """Asynchronously execute a single expert agent."""
        if hasattr(agent, 'ainvoke'):
            result = await agent.ainvoke(state)
        elif hasattr(agent, 'invoke'):
            result = agent.invoke(state)
        else:
            result = agent(state)
        
        if isinstance(result, dict) and 'messages' in result:
            return self._extract_content(result['messages'][-1])
        else:
            return str(result)
    
    def _aggregate_expert_outputs(
        self,
        expert_outputs: List[Dict[str, Any]],
        original_query: str
    ) -> str:
        """Aggregate expert outputs into synthesis prompt."""
        if self.aggregation_method == "structured":
            lines = [
                "Task: Synthesize the following expert opinions into a comprehensive answer.",
                f"\nOriginal Question: {original_query}",
                "\nExpert Opinions:",
                "=" * 50,
                ""
            ]
            
            for expert in expert_outputs:
                lines.append(f"Expert: {expert['agent']}")
                lines.append(f"Opinion: {expert['output']}")
                lines.append("-" * 50)
            
            lines.append("\nPlease synthesize these expert opinions into a coherent, "
                        "comprehensive answer that captures the key insights from all experts.")
            
            return "\n".join(lines)
        
        elif self.aggregation_method == "concat":
            opinions = [f"{e['agent']}: {e['output']}" for e in expert_outputs]
            return f"Question: {original_query}\n\nExpert Opinions:\n" + "\n\n".join(opinions)
        
        else:  # weighted or default
            return self._aggregate_expert_outputs(expert_outputs, original_query)
    
    def _run_synthesizer(self, state: Dict[str, Any]) -> str:
        """Run the synthesizer agent."""
        if hasattr(self.synthesizer_agent, 'invoke'):
            result = self.synthesizer_agent.invoke(state)
        else:
            result = self.synthesizer_agent(state)
        
        if isinstance(result, dict) and 'messages' in result:
            return self._extract_content(result['messages'][-1])
        else:
            return str(result)
    
    async def _run_synthesizer_async(self, state: Dict[str, Any]) -> str:
        """Asynchronously run the synthesizer agent."""
        if hasattr(self.synthesizer_agent, 'ainvoke'):
            result = await self.synthesizer_agent.ainvoke(state)
        elif hasattr(self.synthesizer_agent, 'invoke'):
            result = self.synthesizer_agent.invoke(state)
        else:
            result = self.synthesizer_agent(state)
        
        if isinstance(result, dict) and 'messages' in result:
            return self._extract_content(result['messages'][-1])
        else:
            return str(result)
    
    def _extract_content(self, message: Union[BaseMessage, Dict, str]) -> str:
        """Extract content from message."""
        if isinstance(message, str):
            return message
        if isinstance(message, dict):
            return message.get("content", str(message))
        return getattr(message, "content", str(message))
    
    def __repr__(self) -> str:
        """Return a string representation of the MixtureOfAgents object.
        
        This representation can be used to recreate the object and is
        useful for debugging and logging purposes.
        """
        
        return (
            f"MixtureOfAgents(name='{self.name}', "
            f"experts={len(self.expert_agents)}, "
            f"method='{self.aggregation_method}')"
        )
