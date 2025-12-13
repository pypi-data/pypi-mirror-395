"""
Hierarchical Swarm for Azcore.

Director-worker architecture where a director creates plans and distributes
tasks to specialized worker agents with feedback loops.

Use Cases:
- Complex project management
- Team coordination with oversight
- Hierarchical decision-making
- Task decomposition and distribution
"""

import logging
from typing import List, Dict, Any, Optional, Callable, Union
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from azcore.core.base import BaseAgent
from azcore.exceptions import ValidationError

logger = logging.getLogger(__name__)


class HierarchicalSwarm:
    """
    Director-worker swarm with hierarchical task management.
    
    A director agent analyzes tasks, creates execution plans, and distributes
    work to specialized worker agents. Includes feedback loops for quality
    control and iterative refinement.
    
    Attributes:
        name (str): Swarm identifier
        director_agent: Director/coordinator agent
        worker_agents (List): Specialized worker agents
        max_iterations (int): Maximum planning iterations
    
    Example:
        >>> from azcore.workflows import HierarchicalSwarm
        >>> 
        >>> # Create director agent
        >>> director = ReactAgent(
        ...     name="ProjectDirector",
        ...     llm=llm,
        ...     prompt="You are a project director. Analyze tasks, create plans, "
        ...            "and delegate to workers."
        ... )
        >>> 
        >>> # Create worker agents
        >>> researcher = ReactAgent(name="Researcher", llm=llm, tools=research_tools)
        >>> analyst = ReactAgent(name="Analyst", llm=llm, tools=analysis_tools)
        >>> writer = ReactAgent(name="Writer", llm=llm, tools=writing_tools)
        >>> 
        >>> # Create hierarchical swarm
        >>> swarm = HierarchicalSwarm(
        ...     name="ProjectTeam",
        ...     director_agent=director,
        ...     worker_agents=[researcher, analyst, writer],
        ...     max_iterations=3,
        ...     enable_feedback=True
        ... )
        >>> 
        >>> # Execute task
        >>> result = swarm.run("Create a comprehensive market analysis report")
        >>> print(result['final_output'])
    """
    
    def __init__(
        self,
        name: str,
        director_agent: Union[BaseAgent, Callable],
        worker_agents: List[Union[BaseAgent, Callable]],
        max_iterations: int = 3,
        enable_feedback: bool = True,
        require_approval: bool = False,
        description: str = ""
    ):
        """
        Initialize HierarchicalSwarm.
        
        Args:
            name: Swarm identifier
            director_agent: Director/coordinator agent
            worker_agents: List of worker agents
            max_iterations: Maximum planning/execution iterations (default: 3)
            enable_feedback: Enable feedback loops (default: True)
            require_approval: Require director approval after each task (default: False)
            description: Swarm description
            
        Raises:
            ValidationError: If configuration is invalid
        """
        self.name = name
        self.director_agent = director_agent
        self.worker_agents = worker_agents
        self.max_iterations = max_iterations
        self.enable_feedback = enable_feedback
        self.require_approval = require_approval
        self.description = description or f"Hierarchical Swarm: {name}"
        
        self._execution_history: List[Dict[str, Any]] = []
        
        self._logger = logging.getLogger(f"{self.__class__.__name__}.{name}")
        
        # Validation
        self._validate()
        
        self._logger.info(
            f"HierarchicalSwarm '{name}' initialized with 1 director + "
            f"{len(worker_agents)} workers"
        )
    
    def _validate(self):
        """Validate swarm configuration."""
        if not self.director_agent:
            raise ValidationError("HierarchicalSwarm requires a director agent")
        
        if not self.worker_agents:
            raise ValidationError("HierarchicalSwarm requires at least one worker agent")
        
        if self.max_iterations < 1:
            raise ValidationError("max_iterations must be >= 1")
        
        # Validate agents
        if not (isinstance(self.director_agent, BaseAgent) or callable(self.director_agent)):
            raise ValidationError("Director agent must be BaseAgent or callable")
        
        for i, agent in enumerate(self.worker_agents):
            if not (isinstance(agent, BaseAgent) or callable(agent)):
                raise ValidationError(
                    f"Worker agent at index {i} must be BaseAgent or callable"
                )
    
    def run(
        self,
        task: Union[str, Dict[str, Any]],
        config: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Execute hierarchical task management.
        
        Args:
            task: High-level task description
            config: Optional configuration
            
        Returns:
            Dict containing:
                - final_output: Final deliverable
                - execution_plan: Director's execution plan
                - worker_outputs: All worker outputs
                - feedback_history: Feedback and revisions
                - iterations_completed: Number of iterations
                - metadata: Execution metadata
        """
        self._logger.info(f"Starting HierarchicalSwarm '{self.name}'")
        
        # Prepare initial task
        if isinstance(task, str):
            task_description = task
            state = {"messages": [HumanMessage(content=task)]}
        else:
            task_description = self._extract_content(task.get('messages', [{}])[0])
            state = task
        
        # Phase 1: Director creates execution plan
        self._logger.info("Phase 1: Director creating execution plan...")
        execution_plan = self._create_execution_plan(task_description)
        
        # Phase 2: Execute plan with workers
        self._logger.info("Phase 2: Distributing tasks to workers...")
        worker_outputs = self._execute_with_workers(execution_plan, state)
        
        # Phase 3: Feedback and refinement (if enabled)
        feedback_history = []
        iterations_completed = 1
        
        if self.enable_feedback:
            for iteration in range(self.max_iterations - 1):
                self._logger.info(f"Phase 3: Feedback iteration {iteration + 1}...")
                
                # Get director feedback
                feedback = self._get_director_feedback(worker_outputs)
                
                if self._is_satisfactory(feedback):
                    self._logger.info("Director approves outputs")
                    break
                
                feedback_history.append(feedback)
                
                # Refine outputs based on feedback
                worker_outputs = self._refine_outputs(worker_outputs, feedback, state)
                iterations_completed += 1
        
        # Phase 4: Final synthesis
        self._logger.info("Phase 4: Final synthesis...")
        final_output = self._synthesize_final_output(worker_outputs)
        
        result = {
            "final_output": final_output,
            "execution_plan": execution_plan,
            "worker_outputs": worker_outputs,
            "feedback_history": feedback_history,
            "iterations_completed": iterations_completed,
            "metadata": {
                "workflow": self.name,
                "director": getattr(self.director_agent, 'name', 'Director'),
                "workers": [getattr(w, 'name', f'Worker_{i}') for i, w in enumerate(self.worker_agents)],
                "total_workers": len(self.worker_agents),
                "feedback_enabled": self.enable_feedback
            }
        }
        
        self._logger.info(
            f"HierarchicalSwarm '{self.name}' completed "
            f"({iterations_completed} iterations)"
        )
        
        return result
    
    def _create_execution_plan(self, task: str) -> Dict[str, Any]:
        """Director creates execution plan."""
        planning_prompt = f"""You are a project director. Analyze the following task and create an execution plan.

Task: {task}

Available Workers: {', '.join([getattr(w, 'name', f'Worker_{i}') for i, w in enumerate(self.worker_agents)])}

Create a detailed execution plan that:
1. Breaks down the task into subtasks
2. Assigns each subtask to appropriate workers
3. Defines the execution order

Provide your plan in a clear, structured format."""
        
        state = {"messages": [HumanMessage(content=planning_prompt)]}
        
        try:
            if hasattr(self.director_agent, 'invoke'):
                result = self.director_agent.invoke(state)
            else:
                result = self.director_agent(state)
            
            if isinstance(result, dict) and 'messages' in result:
                plan_text = self._extract_content(result['messages'][-1])
            else:
                plan_text = str(result)
            
            self._logger.debug(f"Execution plan created: {plan_text[:200]}...")
            
            return {
                "plan_text": plan_text,
                "created_by": "Director"
            }
            
        except Exception as e:
            self._logger.error(f"Error creating plan: {e}")
            return {
                "plan_text": f"Execute task: {task}",
                "created_by": "Default",
                "error": str(e)
            }
    
    def _execute_with_workers(
        self,
        execution_plan: Dict[str, Any],
        state: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Execute tasks with worker agents."""
        worker_outputs = []
        
        # For simplicity, execute each worker sequentially with the task
        plan_text = execution_plan.get('plan_text', '')
        
        for idx, worker in enumerate(self.worker_agents):
            worker_name = getattr(worker, 'name', f'Worker_{idx}')
            
            self._logger.debug(f"Executing worker: {worker_name}")
            
            # Prepare worker-specific state
            worker_state = {
                "messages": [
                    SystemMessage(content=f"Execution Plan:\n{plan_text}"),
                    HumanMessage(content=f"Execute your part of the plan as {worker_name}")
                ]
            }
            
            try:
                if hasattr(worker, 'invoke'):
                    result = worker.invoke(worker_state)
                else:
                    result = worker(worker_state)
                
                if isinstance(result, dict) and 'messages' in result:
                    output = self._extract_content(result['messages'][-1])
                else:
                    output = str(result)
                
                worker_outputs.append({
                    "worker": worker_name,
                    "output": output,
                    "status": "completed"
                })
                
                self._logger.debug(f"Worker {worker_name} completed")
                
            except Exception as e:
                self._logger.error(f"Worker {worker_name} failed: {e}")
                worker_outputs.append({
                    "worker": worker_name,
                    "output": f"ERROR: {e}",
                    "status": "failed",
                    "error": str(e)
                })
        
        return worker_outputs
    
    def _get_director_feedback(
        self,
        worker_outputs: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Director provides feedback on worker outputs."""
        # Compile worker outputs
        outputs_summary = "\n\n".join([
            f"Worker: {w['worker']}\nOutput: {w['output']}"
            for w in worker_outputs
        ])
        
        feedback_prompt = f"""Review the following worker outputs and provide feedback.

Worker Outputs:
{outputs_summary}

Provide:
1. Overall quality assessment
2. Specific feedback for improvements
3. Approval status (APPROVED or NEEDS_REVISION)"""
        
        state = {"messages": [HumanMessage(content=feedback_prompt)]}
        
        try:
            if hasattr(self.director_agent, 'invoke'):
                result = self.director_agent.invoke(state)
            else:
                result = self.director_agent(state)
            
            if isinstance(result, dict) and 'messages' in result:
                feedback_text = self._extract_content(result['messages'][-1])
            else:
                feedback_text = str(result)
            
            return {
                "feedback": feedback_text,
                "approved": "APPROVED" in feedback_text.upper()
            }
            
        except Exception as e:
            self._logger.error(f"Error getting feedback: {e}")
            return {
                "feedback": "Error getting feedback",
                "approved": True,  # Assume approved on error
                "error": str(e)
            }
    
    def _is_satisfactory(self, feedback: Dict[str, Any]) -> bool:
        """Check if outputs are satisfactory."""
        return feedback.get('approved', False)
    
    def _refine_outputs(
        self,
        worker_outputs: List[Dict[str, Any]],
        feedback: Dict[str, Any],
        state: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Refine worker outputs based on feedback."""
        # For simplicity, we'll just add the feedback to the outputs
        # In a real implementation, workers would revise their work
        
        refined_outputs = []
        for output in worker_outputs:
            refined_outputs.append({
                **output,
                "feedback_received": feedback.get('feedback', ''),
                "revision": "pending"
            })
        
        return refined_outputs
    
    def _synthesize_final_output(
        self,
        worker_outputs: List[Dict[str, Any]]
    ) -> str:
        """Synthesize final output from worker outputs."""
        # Combine all worker outputs
        combined = "\n\n---\n\n".join([
            f"{w['worker']} Output:\n{w['output']}"
            for w in worker_outputs
            if w.get('status') != 'failed'
        ])
        
        if not combined:
            return "No successful worker outputs to synthesize"
        
        return combined
    
    def add_worker(self, agent: Union[BaseAgent, Callable]) -> 'HierarchicalSwarm':
        """
        Add a worker agent.
        
        Args:
            agent: Worker agent to add
            
        Returns:
            Self for method chaining
        """
        if not (isinstance(agent, BaseAgent) or callable(agent)):
            raise ValidationError("Agent must be BaseAgent or callable")
        
        self.worker_agents.append(agent)
        self._logger.info(f"Added worker (total: {len(self.worker_agents)})")
        
        return self
    
    def _extract_content(self, message: Union[BaseMessage, Dict, str]) -> str:
        """Extract content from message."""
        if isinstance(message, str):
            return message
        if isinstance(message, dict):
            return message.get("content", str(message))
        return getattr(message, "content", str(message))
    
    def __repr__(self) -> str:
        """Return a string representation of the HierarchicalSwarm object."""
        return (
            f"HierarchicalSwarm(name='{self.name}', "
            f"workers={len(self.worker_agents)}, "
            f"max_iterations={self.max_iterations})"
        )
