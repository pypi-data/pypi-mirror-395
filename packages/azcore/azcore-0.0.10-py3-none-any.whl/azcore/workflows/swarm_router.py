"""
Swarm Router for Azcore.

Universal orchestrator that can instantiate and route to any workflow type
based on task analysis.

Use Cases:
- Simplifying workflow selection
- Dynamic task routing
- Unified multi-agent management
- Adaptive execution strategies
"""

import logging
from typing import List, Dict, Any, Optional, Union, Callable
from langchain_core.messages import BaseMessage, HumanMessage
from azcore.core.base import BaseAgent
from azcore.exceptions import ValidationError

# Import all workflow types
from azcore.workflows.sequential_workflow import SequentialWorkflow
from azcore.workflows.concurrent_workflow import ConcurrentWorkflow
from azcore.workflows.agent_rearrange import AgentRearrange
from azcore.workflows.graph_workflow import GraphWorkflow
from azcore.workflows.mixture_of_agents import MixtureOfAgents
from azcore.workflows.group_chat import GroupChat
from azcore.workflows.forest_swarm import ForestSwarm
from azcore.workflows.hierarchical_swarm import HierarchicalSwarm
from azcore.workflows.heavy_swarm import HeavySwarm

logger = logging.getLogger(__name__)


class SwarmRouter:
    """
    Universal orchestrator for all workflow types.
    
    Provides single interface for creating and executing any workflow type.
    Can automatically select appropriate workflow based on task analysis.
    
    Supported Workflows:
    - sequential: Linear chain execution
    - concurrent: Parallel execution
    - rearrange: Dynamic routing
    - graph: DAG orchestration
    - mixture: Expert synthesis
    - group_chat: Conversational collaboration
    - forest: Dynamic tree selection
    - hierarchical: Director-worker
    - heavy: Five-phase comprehensive
    
    Attributes:
        name (str): Router identifier
        default_workflow (str): Default workflow type
        router_llm: LLM for task analysis (optional)
    
    Example:
        >>> from azcore.workflows import SwarmRouter
        >>> 
        >>> # Create router
        >>> router = SwarmRouter(
        ...     name="UniversalRouter",
        ...     default_workflow="sequential",
        ...     router_llm=llm  # Optional for auto-routing
        ... )
        >>> 
        >>> # Manual workflow creation
        >>> workflow = router.create_workflow(
        ...     workflow_type="sequential",
        ...     agents=[agent1, agent2, agent3]
        ... )
        >>> result = workflow.run("Process this task")
        >>> 
        >>> # Auto-routing (requires router_llm)
        >>> result = router.route_and_execute(
        ...     task="Analyze this complex problem",
        ...     agents=[researcher, analyst, synthesizer]
        ... )
    """
    
    def __init__(
        self,
        name: str = "SwarmRouter",
        default_workflow: str = "sequential",
        router_llm: Optional[BaseAgent] = None,
        description: str = ""
    ):
        """
        Initialize SwarmRouter.
        
        Args:
            name: Router identifier
            default_workflow: Default workflow type
            router_llm: LLM for task analysis and routing
            description: Router description
            
        Raises:
            ValidationError: If configuration is invalid
        """
        self.name = name
        self.default_workflow = default_workflow
        self.router_llm = router_llm
        self.description = description or f"Swarm Router: {name}"
        
        self._workflow_registry = self._build_registry()
        self._routing_history: List[Dict[str, Any]] = []
        
        self._logger = logging.getLogger(f"{self.__class__.__name__}.{name}")
        
        # Validation
        self._validate()
        
        self._logger.info(f"SwarmRouter '{name}' initialized with {len(self._workflow_registry)} workflows")
    
    def _validate(self):
        """Validate router configuration."""
        if self.default_workflow not in self._workflow_registry:
            raise ValidationError(
                f"Invalid default_workflow '{self.default_workflow}'. "
                f"Must be one of: {list(self._workflow_registry.keys())}"
            )
    
    def _build_registry(self) -> Dict[str, Dict[str, Any]]:
        """Build registry of all available workflows."""
        return {
            "sequential": {
                "class": SequentialWorkflow,
                "description": "Linear chain execution where output flows agent to agent",
                "use_cases": ["pipelines", "transformations", "step-by-step processing"],
                "complexity": "low"
            },
            "concurrent": {
                "class": ConcurrentWorkflow,
                "description": "Parallel execution for maximum efficiency",
                "use_cases": ["independent tasks", "parallel processing", "speed optimization"],
                "complexity": "low"
            },
            "rearrange": {
                "class": AgentRearrange,
                "description": "Dynamic routing with flexible relationships",
                "use_cases": ["conditional flows", "adaptive routing", "complex branching"],
                "complexity": "medium"
            },
            "graph": {
                "class": GraphWorkflow,
                "description": "DAG-based orchestration with explicit dependencies",
                "use_cases": ["complex workflows", "dependency management", "structured flows"],
                "complexity": "medium"
            },
            "mixture": {
                "class": MixtureOfAgents,
                "description": "Multiple experts with synthesis agent",
                "use_cases": ["expert consensus", "diverse perspectives", "synthesis"],
                "complexity": "medium"
            },
            "group_chat": {
                "class": GroupChat,
                "description": "Conversational collaboration between agents",
                "use_cases": ["discussions", "collaborative problem solving", "iterative refinement"],
                "complexity": "medium"
            },
            "forest": {
                "class": ForestSwarm,
                "description": "Dynamic agent tree selection based on expertise",
                "use_cases": ["expertise routing", "hierarchical teams", "specialized processing"],
                "complexity": "high"
            },
            "hierarchical": {
                "class": HierarchicalSwarm,
                "description": "Director-worker architecture with feedback",
                "use_cases": ["supervised execution", "quality control", "iterative refinement"],
                "complexity": "high"
            },
            "heavy": {
                "class": HeavySwarm,
                "description": "Five-phase comprehensive analysis workflow",
                "use_cases": ["complex research", "thorough analysis", "comprehensive reports"],
                "complexity": "high"
            }
        }
    
    def create_workflow(
        self,
        workflow_type: str,
        agents: List[Union[BaseAgent, Callable]],
        **kwargs
    ) -> Any:
        """
        Create workflow of specified type.
        
        Args:
            workflow_type: Type of workflow to create
            agents: List of agents to use
            **kwargs: Additional workflow-specific arguments
            
        Returns:
            Instantiated workflow
            
        Raises:
            ValidationError: If workflow_type is invalid
        """
        if workflow_type not in self._workflow_registry:
            raise ValidationError(
                f"Unknown workflow type '{workflow_type}'. "
                f"Available: {list(self._workflow_registry.keys())}"
            )
        
        workflow_info = self._workflow_registry[workflow_type]
        workflow_class = workflow_info['class']
        
        workflow_name = kwargs.pop('name', f"{self.name}_{workflow_type}")
        
        self._logger.info(f"Creating {workflow_type} workflow with {len(agents)} agents")
        
        # Create workflow based on type
        if workflow_type == "sequential":
            return workflow_class(name=workflow_name, agents=agents, **kwargs)
        
        elif workflow_type == "concurrent":
            return workflow_class(name=workflow_name, agents=agents, **kwargs)
        
        elif workflow_type == "rearrange":
            workflow = workflow_class(name=workflow_name, agents=agents, **kwargs)
            # AgentRearrange requires setup of relationships
            return workflow
        
        elif workflow_type == "graph":
            return workflow_class(name=workflow_name, **kwargs)
        
        elif workflow_type == "mixture":
            if 'synthesizer_agent' in kwargs:
                return workflow_class(
                    name=workflow_name,
                    expert_agents=agents,
                    synthesizer_agent=kwargs['synthesizer_agent'],
                    **{k: v for k, v in kwargs.items() if k != 'synthesizer_agent'}
                )
            else:
                raise ValidationError("MixtureOfAgents requires 'synthesizer_agent' parameter")
        
        elif workflow_type == "group_chat":
            return workflow_class(name=workflow_name, agents=agents, **kwargs)
        
        elif workflow_type == "forest":
            if 'trees' in kwargs:
                return workflow_class(
                    name=workflow_name,
                    trees=kwargs['trees'],
                    **{k: v for k, v in kwargs.items() if k != 'trees'}
                )
            else:
                raise ValidationError("ForestSwarm requires 'trees' parameter")
        
        elif workflow_type == "hierarchical":
            if 'director_agent' in kwargs:
                return workflow_class(
                    name=workflow_name,
                    director_agent=kwargs['director_agent'],
                    worker_agents=agents,
                    **{k: v for k, v in kwargs.items() if k != 'director_agent'}
                )
            else:
                raise ValidationError("HierarchicalSwarm requires 'director_agent' parameter")
        
        elif workflow_type == "heavy":
            if len(agents) >= 5:
                return workflow_class(
                    name=workflow_name,
                    research_agent=agents[0],
                    analysis_agent=agents[1],
                    alternatives_agent=agents[2],
                    verification_agent=agents[3],
                    synthesis_agent=agents[4],
                    **kwargs
                )
            else:
                raise ValidationError("HeavySwarm requires at least 5 agents")
    
    def route_and_execute(
        self,
        task: Union[str, Dict[str, Any]],
        agents: List[Union[BaseAgent, Callable]],
        workflow_type: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Route task to appropriate workflow and execute.
        
        Args:
            task: Task to execute
            agents: Available agents
            workflow_type: Explicit workflow type (None for auto-routing)
            **kwargs: Additional workflow arguments
            
        Returns:
            Execution results with routing metadata
        """
        # Determine workflow type
        if workflow_type:
            selected_workflow = workflow_type
            routing_method = "explicit"
            self._logger.info(f"Using explicit workflow: {workflow_type}")
        elif self.router_llm:
            selected_workflow = self._auto_route(task, agents)
            routing_method = "auto"
            self._logger.info(f"Auto-routed to workflow: {selected_workflow}")
        else:
            selected_workflow = self.default_workflow
            routing_method = "default"
            self._logger.info(f"Using default workflow: {self.default_workflow}")
        
        # Create workflow
        try:
            workflow = self.create_workflow(selected_workflow, agents, **kwargs)
        except Exception as e:
            self._logger.warning(f"Failed to create {selected_workflow}: {e}. Using default.")
            workflow = self.create_workflow(self.default_workflow, agents)
            selected_workflow = self.default_workflow
        
        # Execute workflow
        result = workflow.run(task)
        
        # Add routing metadata
        result['routing'] = {
            "selected_workflow": selected_workflow,
            "routing_method": routing_method,
            "router": self.name,
            "available_workflows": list(self._workflow_registry.keys())
        }
        
        # Record routing history
        self._routing_history.append({
            "task": str(task)[:100],
            "workflow": selected_workflow,
            "method": routing_method,
            "agent_count": len(agents)
        })
        
        return result
    
    def _auto_route(
        self,
        task: Union[str, Dict[str, Any]],
        agents: List[Union[BaseAgent, Callable]]
    ) -> str:
        """
        Automatically select workflow based on task analysis.
        
        Args:
            task: Task to analyze
            agents: Available agents
            
        Returns:
            Selected workflow type
        """
        if not self.router_llm:
            return self.default_workflow
        
        # Prepare task description
        if isinstance(task, str):
            task_text = task
        else:
            messages = task.get('messages', [])
            task_text = self._extract_content(messages[0]) if messages else str(task)
        
        # Build workflow options
        workflow_options = []
        for name, info in self._workflow_registry.items():
            workflow_options.append(
                f"- {name}: {info['description']} "
                f"(Use cases: {', '.join(info['use_cases'])})"
            )
        
        # Create routing prompt
        routing_prompt = f"""Analyze the following task and select the most appropriate workflow type.

Task: {task_text}

Available Workflows:
{chr(10).join(workflow_options)}

Available Agents: {len(agents)}

Consider:
1. Task complexity and structure
2. Need for parallel vs sequential processing
3. Need for expert consensus or synthesis
4. Need for iterative refinement
5. Number and specialization of agents

Respond with ONLY the workflow name (e.g., "sequential", "mixture", "heavy").
"""
        
        state = {"messages": [HumanMessage(content=routing_prompt)]}
        
        try:
            if hasattr(self.router_llm, 'invoke'):
                result = self.router_llm.invoke(state)
            else:
                result = self.router_llm(state)
            
            # Extract workflow name
            if isinstance(result, dict) and 'messages' in result:
                response = self._extract_content(result['messages'][-1])
            else:
                response = str(result)
            
            # Parse response
            response_lower = response.lower().strip()
            
            for workflow_name in self._workflow_registry.keys():
                if workflow_name in response_lower:
                    self._logger.debug(f"LLM selected workflow: {workflow_name}")
                    return workflow_name
            
            self._logger.warning(f"Could not parse workflow from response: {response}")
            return self.default_workflow
            
        except Exception as e:
            self._logger.error(f"Auto-routing failed: {e}")
            return self.default_workflow
    
    def list_workflows(self) -> List[Dict[str, Any]]:
        """
        Get list of all available workflows.
        
        Returns:
            List of workflow information
        """
        workflows = []
        for name, info in self._workflow_registry.items():
            workflows.append({
                "name": name,
                "description": info['description'],
                "use_cases": info['use_cases'],
                "complexity": info['complexity']
            })
        return workflows
    
    def get_routing_history(self) -> List[Dict[str, Any]]:
        """
        Get history of routing decisions.
        
        Returns:
            List of routing history entries
        """
        return self._routing_history.copy()
    
    def _extract_content(self, message: Union[BaseMessage, Dict, str]) -> str:
        """Extract content from message."""
        if isinstance(message, str):
            return message
        if isinstance(message, dict):
            return message.get("content", str(message))
        return getattr(message, "content", str(message))
    
    def __repr__(self) -> str:
        """Return a string representation of the SwarmRouter object.

        This method returns a string of the form
        "SwarmRouter(name='<name>', workflows=<num_workflows>)"
        which is useful for debugging and logging purposes.

        Returns:
            str: A string representation of the SwarmRouter instance."""
        return f"SwarmRouter(name='{self.name}', workflows={len(self._workflow_registry)})"
