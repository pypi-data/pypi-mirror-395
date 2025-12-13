"""
Graph orchestration for the Azcore..

This module provides the GraphOrchestrator class which manages the
construction and execution of multi-agent workflow graphs.
"""

from typing import List, Dict, Any, Optional, Callable, Set
from collections import defaultdict
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from azcore.core.base import BaseTeam, BaseNode
from azcore.core.supervisor import Supervisor
from azcore.core.state import State
from azcore.exceptions import (
    GraphError,
    GraphCycleError,
    MaxIterationsExceededError,
    ValidationError
)
import logging

logger = logging.getLogger(__name__)


class GraphOrchestrator:
    """
    Orchestrator for managing multi-agent workflow graphs.
    
    The GraphOrchestrator provides a high-level API for building complex
    agent workflows with coordinators, planners, supervisors, and teams.
    
    Attributes:
        state_class: State class to use for the graph
        graph_builder: LangGraph StateGraph builder
        checkpointer: Optional checkpointer for conversation persistence
    """
    
    def __init__(
        self,
        state_class: type = State,
        checkpointer: Optional[Any] = None,
        max_iterations: int = 20,
        enable_cycle_detection: bool = True
    ):
        """
        Initialize the graph orchestrator.
        
        Args:
            state_class: State class to use (default: State)
            checkpointer: Optional checkpointer for persistence
            max_iterations: Maximum workflow iterations (default: 20)
            enable_cycle_detection: Enable cycle detection (default: True)
        """
        self.state_class = state_class
        self.checkpointer = checkpointer or MemorySaver()
        self.graph_builder = StateGraph(state_class)
        self._nodes: Dict[str, Callable] = {}
        self._teams: Dict[str, BaseTeam] = {}
        self._supervisor: Optional[Supervisor] = None
        self._logger = logging.getLogger(self.__class__.__name__)
        
        # Execution control
        self.max_iterations = max_iterations
        self.enable_cycle_detection = enable_cycle_detection
        self._edges: Dict[str, List[str]] = defaultdict(list)
        
        self._logger.info(
            f"GraphOrchestrator initialized (max_iterations={max_iterations}, "
            f"cycle_detection={enable_cycle_detection})"
        )
    
    def add_node(self, name: str, node: Callable | BaseNode) -> 'GraphOrchestrator':
        """
        Add a node to the graph.
        
        Args:
            name: Unique name for the node
            node: Node callable or BaseNode instance
            
        Returns:
            Self for method chaining
        """
        if isinstance(node, BaseNode):
            callable_node = node.__call__
        else:
            callable_node = node
        
        self.graph_builder.add_node(name, callable_node)
        self._nodes[name] = callable_node
        self._logger.info(f"Added node: {name}")
        
        return self
    
    def add_team(self, team: BaseTeam) -> 'GraphOrchestrator':
        """
        Add a team to the graph.
        
        Teams are automatically built and added as nodes.
        
        Args:
            team: Team to add
            
        Returns:
            Self for method chaining
        """
        team_callable = team.build()
        self.add_node(team.name, team_callable)
        self._teams[team.name] = team
        
        # Add team to supervisor if present
        if self._supervisor:
            self._supervisor.add_member(team.name)
        
        self._logger.info(f"Added team: {team.name}")
        
        return self
    
    def set_supervisor(
        self,
        supervisor: Supervisor,
        name: str = "supervisor"
    ) -> 'GraphOrchestrator':
        """
        Set the supervisor for the graph.
        
        Args:
            supervisor: Supervisor instance
            name: Node name for the supervisor (default: "supervisor")
            
        Returns:
            Self for method chaining
        """
        self._supervisor = supervisor
        
        # Add all existing teams to supervisor
        for team_name in self._teams.keys():
            supervisor.add_member(team_name)
        
        supervisor_node = supervisor.create_node()
        self.add_node(name, supervisor_node)
        
        self._logger.info("Set supervisor node")
        
        return self
    
    def add_edge(self, from_node: str, to_node: str) -> 'GraphOrchestrator':
        """
        Add a directed edge between nodes.
        
        Args:
            from_node: Source node name
            to_node: Destination node name
            
        Returns:
            Self for method chaining
            
        Raises:
            ValidationError: If edge would create invalid graph structure
        """
        # Store original names for cycle detection
        original_from = from_node
        original_to = to_node
        
        # Handle special nodes
        if from_node.lower() == "start":
            from_node = START
        if to_node.lower() == "end":
            to_node = END
        
        # Track edges for cycle detection
        if (original_from.lower() != "start" and 
            original_to.lower() != "end"):
            self._edges[original_from].append(original_to)
        
        # Check for cycles if enabled
        if self.enable_cycle_detection and original_to.lower() != "end":
            if self._has_cycle():
                raise GraphCycleError(
                    f"Adding edge {original_from} -> {original_to} would create a cycle",
                    details={"from": original_from, "to": original_to}
                )
        
        self.graph_builder.add_edge(from_node, to_node)
        self._logger.debug(f"Added edge: {from_node} -> {to_node}")
        
        return self
    
    def set_entry_point(self, node_name: str) -> 'GraphOrchestrator':
        """
        Set the entry point for the graph.
        
        Args:
            node_name: Name of the entry node
            
        Returns:
            Self for method chaining
        """
        self.add_edge(START, node_name)
        self._logger.info(f"Set entry point: {node_name}")
        
        return self
    
    def compile(self) -> Any:
        """
        Compile the graph for execution.
        
        Returns:
            Compiled graph ready for invocation
        """
        compiled_graph = self.graph_builder.compile(
            checkpointer=self.checkpointer
        )
        
        self._logger.info(f"Compiled graph with {len(self._nodes)} nodes")
        
        return compiled_graph
    
    def build_hierarchical_graph(
        self,
        coordinator: Optional[Callable] = None,
        planner: Optional[Callable] = None,
        supervisor: Optional[Supervisor] = None,
        teams: Optional[List[BaseTeam]] = None,
        generator: Optional[Callable] = None
    ) -> Any:
        """
        Build a complete hierarchical agent graph.
        
        This is a convenience method that sets up the common pattern:
        START -> Coordinator -> Planner -> Supervisor -> Teams -> Generator -> END
        
        Args:
            coordinator: Optional coordinator node
            planner: Optional planner node
            supervisor: Optional supervisor
            teams: Optional list of teams
            generator: Optional response generator node
            
        Returns:
            Compiled graph
        """
        # Add coordinator if provided
        if coordinator:
            self.add_node("coordinator", coordinator)
            self.set_entry_point("coordinator")
        
        # Add planner if provided
        if planner:
            self.add_node("planner", planner)
        
        # Add supervisor if provided
        if supervisor:
            self.set_supervisor(supervisor)
        
        # Add teams if provided
        if teams:
            for team in teams:
                self.add_team(team)
        
        # Add generator if provided
        if generator:
            self.add_node("response_generator", generator)
        
        self._logger.info("Built hierarchical graph structure")
        
        return self.compile()
    
    def get_node(self, name: str) -> Optional[Callable]:
        """
        Get a node by name.
        
        Args:
            name: Node name
            
        Returns:
            Node callable or None
        """
        return self._nodes.get(name)
    
    def get_team(self, name: str) -> Optional[BaseTeam]:
        """
        Get a team by name.
        
        Args:
            name: Team name
            
        Returns:
            Team instance or None
        """
        return self._teams.get(name)
    
    def get_all_nodes(self) -> Dict[str, Callable]:
        """
        Get all registered nodes.
        
        Returns:
            Dictionary of node names to callables
        """
        return self._nodes.copy()
    
    def get_all_teams(self) -> Dict[str, BaseTeam]:
        """
        Get all registered teams.
        
        Returns:
            Dictionary of team names to team instances
        """
        return self._teams.copy()
    
    def _has_cycle(self) -> bool:
        """
        Check if the graph has a cycle using DFS.
        
        Returns:
            True if cycle detected, False otherwise
        """
        visited: Set[str] = set()
        rec_stack: Set[str] = set()
        
        def dfs(node: str) -> bool:
            """Depth-first search to detect cycles."""
            visited.add(node)
            rec_stack.add(node)
            
            for neighbor in self._edges.get(node, []):
                if neighbor not in visited:
                    if dfs(neighbor):
                        return True
                elif neighbor in rec_stack:
                    return True
            
            rec_stack.remove(node)
            return False
        
        # Check from all nodes
        for node in self._edges.keys():
            if node not in visited:
                if dfs(node):
                    return True
        
        return False
    
    def validate_graph(self) -> None:
        """
        Validate the graph structure.
        
        Raises:
            ValidationError: If graph structure is invalid
        """
        if not self._nodes:
            raise ValidationError("Graph has no nodes")
        
        if self.enable_cycle_detection and self._has_cycle():
            raise GraphCycleError("Graph contains a cycle")
        
        self._logger.info("Graph validation passed")
    
    def __repr__(self) -> str:
        return f"GraphOrchestrator(nodes={len(self._nodes)}, teams={len(self._teams)})"
