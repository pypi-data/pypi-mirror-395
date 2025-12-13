"""
Forest Swarm for Azcore.

Dynamically selects the most suitable agent or tree of agents for a given task.
Optimizes for expertise matching and complex decision-making trees.

Use Cases:
- Task routing to best-suited agents
- Expertise-based agent selection
- Complex decision trees
- Dynamic workflow adaptation
"""

import logging
from typing import List, Dict, Any, Optional, Callable, Union, Tuple
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_core.language_models.chat_models import BaseChatModel
from azcore.core.base import BaseAgent
from azcore.exceptions import ValidationError

logger = logging.getLogger(__name__)


class AgentTree:
    """Represents a tree of agents with a specific expertise."""
    
    def __init__(
        self,
        name: str,
        root_agent: Union[BaseAgent, Callable],
        sub_agents: Optional[List[Union[BaseAgent, Callable]]] = None,
        expertise: Optional[List[str]] = None
    ):
        """
        Initialize an agent tree.
        
        Args:
            name: Tree identifier
            root_agent: Root/primary agent
            sub_agents: Optional child agents
            expertise: List of expertise keywords
        """
        self.name = name
        self.root_agent = root_agent
        self.sub_agents = sub_agents or []
        self.expertise = expertise or []
    
    def __repr__(self) -> str:
        return f"AgentTree(name='{self.name}', sub_agents={len(self.sub_agents)})"


class ForestSwarm:
    """
    Dynamic agent/tree selection based on task requirements.
    
    ForestSwarm maintains multiple agent trees, each with specific expertise.
    It intelligently routes tasks to the most suitable tree based on
    task analysis and expertise matching.
    
    Attributes:
        name (str): Forest identifier
        trees (List[AgentTree]): Available agent trees
        router_agent: Agent for task routing decisions
    
    Example:
        >>> from azcore.workflows import ForestSwarm, AgentTree
        >>> 
        >>> # Create specialized agent trees
        >>> research_tree = AgentTree(
        ...     name="ResearchTeam",
        ...     root_agent=research_lead,
        ...     sub_agents=[researcher1, researcher2],
        ...     expertise=["research", "analysis", "data"]
        ... )
        >>> 
        >>> coding_tree = AgentTree(
        ...     name="CodingTeam",
        ...     root_agent=coding_lead,
        ...     sub_agents=[backend_dev, frontend_dev],
        ...     expertise=["code", "programming", "software"]
        ... )
        >>> 
        >>> writing_tree = AgentTree(
        ...     name="WritingTeam",
        ...     root_agent=writer_lead,
        ...     sub_agents=[editor, copywriter],
        ...     expertise=["writing", "content", "documentation"]
        ... )
        >>> 
        >>> # Create forest swarm
        >>> forest = ForestSwarm(
        ...     name="TaskForest",
        ...     trees=[research_tree, coding_tree, writing_tree],
        ...     router_agent=router_llm
        ... )
        >>> 
        >>> # Route and execute task
        >>> result = forest.run("Write documentation for the API")
        >>> print(result['selected_tree'], result['output'])
    """
    
    def __init__(
        self,
        name: str,
        trees: List[AgentTree],
        router_agent: Optional[Union[BaseAgent, BaseChatModel]] = None,
        selection_mode: str = "auto",
        description: str = ""
    ):
        """
        Initialize ForestSwarm.
        
        Args:
            name: Forest identifier
            trees: List of agent trees
            router_agent: Agent/LLM for routing decisions
            selection_mode: Selection method
                - "auto": Automatic based on expertise (default)
                - "llm": Use LLM router agent
                - "keyword": Keyword matching
                - "sequential": Try trees in order
            description: Forest description
            
        Raises:
            ValidationError: If configuration is invalid
        """
        self.name = name
        self.trees = trees
        self.router_agent = router_agent
        self.selection_mode = selection_mode
        self.description = description or f"Forest Swarm: {name}"
        
        self._logger = logging.getLogger(f"{self.__class__.__name__}.{name}")
        
        # Validation
        self._validate()
        
        self._logger.info(
            f"ForestSwarm '{name}' initialized with {len(trees)} trees "
            f"(mode={selection_mode})"
        )
    
    def _validate(self):
        """Validate forest configuration."""
        if not self.trees:
            raise ValidationError("ForestSwarm requires at least one tree")
        
        valid_modes = ["auto", "llm", "keyword", "sequential"]
        if self.selection_mode not in valid_modes:
            raise ValidationError(
                f"Invalid selection_mode '{self.selection_mode}'. "
                f"Must be one of: {valid_modes}"
            )
        
        # Validate trees
        for i, tree in enumerate(self.trees):
            if not isinstance(tree, AgentTree):
                raise ValidationError(f"Tree at index {i} must be AgentTree instance")
    
    def run(
        self,
        task: Union[str, Dict[str, Any]],
        config: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Route task to appropriate tree and execute.
        
        Args:
            task: Task description or state
            config: Optional configuration
            
        Returns:
            Dict containing:
                - output: Final output from selected tree
                - selected_tree: Name of selected tree
                - selection_reasoning: Why this tree was selected
                - tree_outputs: Outputs from tree execution
                - metadata: Execution metadata
        """
        self._logger.info(f"Starting ForestSwarm '{self.name}'")
        
        # Extract task description
        if isinstance(task, str):
            task_description = task
            state = {"messages": [HumanMessage(content=task)]}
        else:
            task_description = self._extract_content(task.get('messages', [{}])[0])
            state = task
        
        # Step 1: Select appropriate tree
        self._logger.info("Phase 1: Selecting appropriate agent tree...")
        selected_tree, reasoning = self._select_tree(task_description)
        
        self._logger.info(f"Selected tree: {selected_tree.name}")
        self._logger.debug(f"Reasoning: {reasoning}")
        
        # Step 2: Execute with selected tree
        self._logger.info("Phase 2: Executing task with selected tree...")
        tree_outputs = self._execute_tree(selected_tree, state)
        
        # Step 3: Prepare result
        final_output = tree_outputs.get('output', '')
        
        result = {
            "output": final_output,
            "selected_tree": selected_tree.name,
            "selection_reasoning": reasoning,
            "tree_outputs": tree_outputs,
            "metadata": {
                "workflow": self.name,
                "total_trees": len(self.trees),
                "selection_mode": self.selection_mode,
                "tree_expertise": selected_tree.expertise
            }
        }
        
        self._logger.info(f"ForestSwarm '{self.name}' completed")
        
        return result
    
    def _select_tree(self, task_description: str) -> Tuple[AgentTree, str]:
        """Select the most appropriate tree for the task."""
        if self.selection_mode == "llm" and self.router_agent:
            return self._select_with_llm(task_description)
        
        elif self.selection_mode == "keyword":
            return self._select_by_keyword(task_description)
        
        elif self.selection_mode == "sequential":
            return self.trees[0], "Sequential selection (first tree)"
        
        else:  # auto
            # Try keyword first, fallback to LLM if available
            try:
                return self._select_by_keyword(task_description)
            except:
                if self.router_agent:
                    return self._select_with_llm(task_description)
                return self.trees[0], "Default selection (first tree)"
    
    def _select_with_llm(self, task_description: str) -> Tuple[AgentTree, str]:
        """Use LLM router to select tree."""
        # Build selection prompt
        tree_descriptions = []
        for tree in self.trees:
            expertise_str = ", ".join(tree.expertise) if tree.expertise else "general"
            tree_descriptions.append(
                f"- {tree.name}: Expertise in {expertise_str}"
            )
        
        prompt = f"""Given the following task, select the most appropriate agent tree to handle it.

Task: {task_description}

Available Trees:
{chr(10).join(tree_descriptions)}

Respond with ONLY the tree name, nothing else."""
        
        try:
            if isinstance(self.router_agent, BaseChatModel):
                response = self.router_agent.invoke([HumanMessage(content=prompt)])
                selected_name = response.content.strip()
            elif hasattr(self.router_agent, 'invoke'):
                result = self.router_agent.invoke({"messages": [HumanMessage(content=prompt)]})
                selected_name = self._extract_content(result['messages'][-1]).strip()
            else:
                selected_name = self.trees[0].name
            
            # Find tree by name
            for tree in self.trees:
                if tree.name.lower() == selected_name.lower():
                    return tree, f"LLM-selected based on task analysis"
            
            # Fallback
            return self.trees[0], "LLM selection failed, using default"
            
        except Exception as e:
            self._logger.error(f"LLM selection failed: {e}")
            return self.trees[0], f"Error in selection, using default"
    
    def _select_by_keyword(self, task_description: str) -> Tuple[AgentTree, str]:
        """Select tree based on keyword matching."""
        task_lower = task_description.lower()
        
        # Score each tree based on keyword matches
        best_tree = None
        best_score = 0
        best_matches = []
        
        for tree in self.trees:
            score = 0
            matches = []
            
            for keyword in tree.expertise:
                if keyword.lower() in task_lower:
                    score += 1
                    matches.append(keyword)
            
            if score > best_score:
                best_score = score
                best_tree = tree
                best_matches = matches
        
        if best_tree and best_score > 0:
            reasoning = f"Keyword match: {', '.join(best_matches)}"
            return best_tree, reasoning
        
        # No matches, return first tree
        return self.trees[0], "No keyword matches, using default tree"
    
    def _execute_tree(
        self,
        tree: AgentTree,
        state: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute task with selected tree."""
        outputs = {
            "tree": tree.name,
            "agents_executed": []
        }
        
        # Execute root agent
        try:
            root_agent = tree.root_agent
            agent_name = getattr(root_agent, 'name', tree.name)
            
            self._logger.debug(f"Executing root agent: {agent_name}")
            
            if hasattr(root_agent, 'invoke'):
                result = root_agent.invoke(state)
            else:
                result = root_agent(state)
            
            # Extract output
            if isinstance(result, dict) and 'messages' in result:
                output = self._extract_content(result['messages'][-1])
                state = result
            else:
                output = str(result)
            
            outputs['output'] = output
            outputs['agents_executed'].append(agent_name)
            
            # Optionally execute sub-agents if needed
            if tree.sub_agents:
                self._logger.debug(f"Tree has {len(tree.sub_agents)} sub-agents available")
                # Could implement sub-agent execution here if needed
            
        except Exception as e:
            self._logger.error(f"Error executing tree {tree.name}: {e}")
            outputs['output'] = f"ERROR: {e}"
            outputs['error'] = str(e)
        
        return outputs
    
    def add_tree(self, tree: AgentTree) -> 'ForestSwarm':
        """
        Add a new agent tree to the forest.
        
        Args:
            tree: Agent tree to add
            
        Returns:
            Self for method chaining
        """
        if not isinstance(tree, AgentTree):
            raise ValidationError("Must provide AgentTree instance")
        
        self.trees.append(tree)
        self._logger.info(f"Added tree '{tree.name}' (total: {len(self.trees)})")
        
        return self
    
    def get_tree_by_name(self, name: str) -> Optional[AgentTree]:
        """
        Get a tree by name.
        
        Args:
            name: Tree name
            
        Returns:
            AgentTree or None
        """
        for tree in self.trees:
            if tree.name == name:
                return tree
        return None
    
    def get_forest_structure(self) -> Dict[str, Any]:
        """
        Get the forest structure.
        
        Returns:
            Dict with trees and their expertise
        """
        return {
            "name": self.name,
            "total_trees": len(self.trees),
            "trees": [
                {
                    "name": tree.name,
                    "expertise": tree.expertise,
                    "sub_agents": len(tree.sub_agents)
                }
                for tree in self.trees
            ]
        }
    
    def _extract_content(self, message: Union[BaseMessage, Dict, str]) -> str:
        """Extract content from message."""
        if isinstance(message, str):
            return message
        if isinstance(message, dict):
            return message.get("content", str(message))
        return getattr(message, "content", str(message))
    
    def __repr__(self) -> str:
        """Return a string representation of the ForestSwarm.

        Includes the name, number of trees and selection mode.
        """
        return (
            f"ForestSwarm(name='{self.name}', "
            f"trees={len(self.trees)}, "
            f"mode='{self.selection_mode}')"
        )
