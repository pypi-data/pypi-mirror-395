"""
Graph Workflow for Azcore.

Orchestrates agents as nodes in a Directed Acyclic Graph (DAG).
Builds on the existing GraphOrchestrator with enhanced workflow features.

Use Cases:
- Complex projects with intricate dependencies
- Software build pipelines
- Data processing DAGs
- Multi-stage workflows with dependencies
"""

import logging
from typing import List, Dict, Any, Optional, Callable, Union
from langchain_core.messages import BaseMessage, HumanMessage
from azcore.core.base import BaseAgent
from azcore.core.orchestrator import GraphOrchestrator
from azcore.core.state import State
from azcore.exceptions import ValidationError

logger = logging.getLogger(__name__)


class GraphWorkflow:
    """
    DAG-based workflow orchestration.
    
    Provides a higher-level interface over GraphOrchestrator with
    workflow-specific features like validation, execution tracking,
    and result aggregation.
    
    Attributes:
        name (str): Workflow identifier
        orchestrator (GraphOrchestrator): Underlying graph orchestrator
        agents (Dict): Registered agents
    
    Example:
        >>> from azcore.workflows import GraphWorkflow
        >>> 
        >>> # Create workflow
        >>> workflow = GraphWorkflow(
        ...     name="BuildPipeline",
        ...     max_iterations=20,
        ...     enable_cycle_detection=True
        ... )
        >>> 
        >>> # Add agents as nodes
        >>> workflow.add_node("fetch", fetcher_agent)
        >>> workflow.add_node("process", processor_agent)
        >>> workflow.add_node("validate", validator_agent)
        >>> workflow.add_node("deploy", deployer_agent)
        >>> 
        >>> # Define DAG structure
        >>> workflow.add_edge("fetch", "process")
        >>> workflow.add_edge("process", "validate")
        >>> workflow.add_edge("validate", "deploy")
        >>> workflow.set_entry_point("fetch")
        >>> workflow.set_exit_point("deploy")
        >>> 
        >>> # Compile and execute
        >>> compiled = workflow.compile()
        >>> result = workflow.run("Deploy version 2.0")
    """
    
    def __init__(
        self,
        name: str,
        state_class: type = State,
        max_iterations: int = 20,
        enable_cycle_detection: bool = True,
        description: str = ""
    ):
        """
        Initialize GraphWorkflow.
        
        Args:
            name: Workflow identifier
            state_class: State class to use (default: State)
            max_iterations: Maximum workflow iterations (default: 20)
            enable_cycle_detection: Enable cycle detection (default: True)
            description: Workflow description
        """
        self.name = name
        self.description = description or f"Graph workflow: {name}"
        
        # Create underlying orchestrator
        self.orchestrator = GraphOrchestrator(
            state_class=state_class,
            max_iterations=max_iterations,
            enable_cycle_detection=enable_cycle_detection
        )
        
        self._agents: Dict[str, Union[BaseAgent, Callable]] = {}
        self._entry_point: Optional[str] = None
        self._exit_points: List[str] = []
        self._compiled_graph: Optional[Any] = None
        
        self._logger = logging.getLogger(f"{self.__class__.__name__}.{name}")
        self._logger.info(
            f"GraphWorkflow '{name}' initialized "
            f"(max_iterations={max_iterations}, cycle_detection={enable_cycle_detection})"
        )
    
    def add_node(
        self,
        name: str,
        agent: Union[BaseAgent, Callable],
        description: str = ""
    ) -> 'GraphWorkflow':
        """
        Add an agent node to the workflow.
        
        Args:
            name: Node name
            agent: Agent or callable
            description: Node description
            
        Returns:
            Self for method chaining
        """
        self._agents[name] = agent
        self.orchestrator.add_node(name, agent)
        
        self._logger.debug(f"Added node: {name}")
        
        return self
    
    def add_edge(
        self,
        from_node: str,
        to_node: str
    ) -> 'GraphWorkflow':
        """
        Add a directed edge between nodes.
        
        Args:
            from_node: Source node name
            to_node: Destination node name
            
        Returns:
            Self for method chaining
        """
        self.orchestrator.add_edge(from_node, to_node)
        
        self._logger.debug(f"Added edge: {from_node} -> {to_node}")
        
        return self
    
    def set_entry_point(self, node_name: str) -> 'GraphWorkflow':
        """
        Set the workflow entry point.
        
        Args:
            node_name: Name of entry node
            
        Returns:
            Self for method chaining
        """
        if node_name not in self._agents:
            raise ValidationError(f"Node '{node_name}' not found")
        
        self._entry_point = node_name
        self.orchestrator.set_entry_point(node_name)
        
        self._logger.info(f"Set entry point: {node_name}")
        
        return self
    
    def set_exit_point(self, node_name: str) -> 'GraphWorkflow':
        """
        Set a workflow exit point.
        
        Args:
            node_name: Name of exit node
            
        Returns:
            Self for method chaining
        """
        if node_name not in self._agents:
            raise ValidationError(f"Node '{node_name}' not found")
        
        if node_name not in self._exit_points:
            self._exit_points.append(node_name)
            self.orchestrator.add_edge(node_name, "END")
        
        self._logger.debug(f"Set exit point: {node_name}")
        
        return self
    
    def compile(self) -> Any:
        """
        Compile the workflow graph.
        
        Returns:
            Compiled graph ready for execution
            
        Raises:
            ValidationError: If graph structure is invalid
        """
        if not self._entry_point:
            raise ValidationError("Entry point not set. Call set_entry_point() first.")
        
        if not self._exit_points:
            self._logger.warning("No exit points set. Workflow may not terminate properly.")
        
        # Validate graph structure
        self.orchestrator.validate_graph()
        
        # Compile
        self._compiled_graph = self.orchestrator.compile()
        
        self._logger.info(f"Compiled workflow '{self.name}' with {len(self._agents)} nodes")
        
        return self._compiled_graph
    
    def run(
        self,
        initial_input: Union[str, Dict[str, Any]],
        config: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Execute the workflow.
        
        Args:
            initial_input: Starting input (string or state dict)
            config: Optional execution configuration
            
        Returns:
            Dict containing:
                - output: Final output
                - messages: Message history
                - metadata: Execution metadata
        """
        if not self._compiled_graph:
            self.compile()
        
        self._logger.info(f"Executing GraphWorkflow '{self.name}'")
        
        # Prepare input state
        if isinstance(initial_input, str):
            state = {"messages": [HumanMessage(content=initial_input)]}
        else:
            state = initial_input
        
        # Execute compiled graph
        result = self._compiled_graph.invoke(state, config=config)
        
        # Extract final output
        if isinstance(result, dict) and 'messages' in result:
            final_message = result['messages'][-1]
            output = self._extract_content(final_message)
        else:
            output = str(result)
        
        formatted_result = {
            "output": output,
            "messages": result.get('messages', []) if isinstance(result, dict) else [],
            "metadata": {
                "workflow": self.name,
                "nodes_executed": len(self._agents),
                "entry_point": self._entry_point,
                "exit_points": self._exit_points
            }
        }
        
        self._logger.info(f"GraphWorkflow '{self.name}' completed")
        
        return formatted_result
    
    async def arun(
        self,
        initial_input: Union[str, Dict[str, Any]],
        config: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Asynchronously execute the workflow.
        
        Args:
            initial_input: Starting input
            config: Optional configuration
            
        Returns:
            Dict with output and metadata
        """
        if not self._compiled_graph:
            self.compile()
        
        self._logger.info(f"Executing async GraphWorkflow '{self.name}'")
        
        # Prepare input state
        if isinstance(initial_input, str):
            state = {"messages": [HumanMessage(content=initial_input)]}
        else:
            state = initial_input
        
        # Execute compiled graph asynchronously
        result = await self._compiled_graph.ainvoke(state, config=config)
        
        # Extract final output
        if isinstance(result, dict) and 'messages' in result:
            final_message = result['messages'][-1]
            output = self._extract_content(final_message)
        else:
            output = str(result)
        
        return {
            "output": output,
            "messages": result.get('messages', []) if isinstance(result, dict) else [],
            "metadata": {
                "workflow": self.name,
                "nodes_executed": len(self._agents),
                "entry_point": self._entry_point,
                "exit_points": self._exit_points
            }
        }
    
    def get_graph_structure(self) -> Dict[str, Any]:
        """
        Get the workflow graph structure.
        
        Returns:
            Dict with nodes and edges information
        """
        return {
            "name": self.name,
            "nodes": list(self._agents.keys()),
            "edges": dict(self.orchestrator._edges),
            "entry_point": self._entry_point,
            "exit_points": self._exit_points,
            "total_nodes": len(self._agents)
        }
    
    def visualize(self) -> str:
        """
        Generate a simple text visualization of the workflow.
        
        Returns:
            String representation of the workflow graph
        """
        lines = [
            f"GraphWorkflow: {self.name}",
            f"{'=' * 50}",
            f"Entry Point: {self._entry_point}",
            f"Exit Points: {', '.join(self._exit_points)}",
            f"Total Nodes: {len(self._agents)}",
            "",
            "Graph Structure:",
        ]
        
        for from_node, to_nodes in self.orchestrator._edges.items():
            for to_node in to_nodes:
                lines.append(f"  {from_node} -> {to_node}")
        
        return "\n".join(lines)
    
    def _extract_content(self, message: Union[BaseMessage, Dict, str]) -> str:
        """Extract content from message."""
        if isinstance(message, str):
            return message
        if isinstance(message, dict):
            return message.get("content", str(message))
        return getattr(message, "content", str(message))
    
    def __repr__(self) -> str:
        """Return a string representation of the workflow.

        The string representation includes the name of the workflow, the number of nodes, and the entry point.

        Returns:
            str: String representation of the workflow
        """
        return (
            f"GraphWorkflow(name='{self.name}', "
            f"nodes={len(self._agents)}, "
            f"entry='{self._entry_point}')"
        )
