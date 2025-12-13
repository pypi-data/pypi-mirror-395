"""
Advanced Planning Module for Multi-Step Task Decomposition.

This module provides advanced planning capabilities including:
- Multi-step task decomposition
- Plan validation and feasibility checking
- Adaptive re-planning based on feedback
- Dependency analysis and sequencing
"""

from typing import Dict, Any, List, Optional, Tuple
import json
from dataclasses import dataclass, field, asdict
from enum import IntEnum, Enum
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.types import Command
from langgraph.graph import END
from azcore.core.base import BaseNode
import logging

logger = logging.getLogger(__name__)


class StepStatus(Enum):
    """Status of a plan step."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    BLOCKED = "blocked"
    SKIPPED = "skipped"


class PlanComplexity(IntEnum):
    """Complexity level of a plan (comparable using integer values)."""
    SIMPLE = 1  # 1-3 steps
    MODERATE = 2  # 4-7 steps
    COMPLEX = 3  # 8-15 steps
    VERY_COMPLEX = 4  # 16+ steps
    
    @property
    def name_str(self) -> str:
        """Get the string name of the complexity level."""
        return self.name.lower()


@dataclass
class PlanStep:
    """Represents a single step in an execution plan."""
    step_id: str
    description: str
    assigned_team: str
    dependencies: List[str] = field(default_factory=list)
    tools_required: List[str] = field(default_factory=list)
    expected_output: str = ""
    status: StepStatus = StepStatus.PENDING
    retry_count: int = 0
    max_retries: int = 3
    execution_time: Optional[float] = None
    error_message: Optional[str] = None
    actual_output: Optional[str] = None
    confidence_score: float = 1.0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        result = asdict(self)
        result['status'] = self.status.value
        return result
    
    def can_execute(self, completed_steps: List[str]) -> bool:
        """Check if all dependencies are met."""
        return all(dep in completed_steps for dep in self.dependencies)
    
    def mark_completed(self, output: str) -> None:
        """Mark step as completed."""
        self.status = StepStatus.COMPLETED
        self.actual_output = output
    
    def mark_failed(self, error: str) -> None:
        """Mark step as failed."""
        self.status = StepStatus.FAILED
        self.error_message = error
        self.retry_count += 1
    
    def can_retry(self) -> bool:
        """Check if step can be retried."""
        return self.retry_count < self.max_retries


@dataclass
class ExecutionPlan:
    """Represents a complete execution plan."""
    task_description: str
    steps: List[PlanStep]
    success_criteria: str
    complexity: PlanComplexity
    estimated_duration: Optional[float] = None
    alternative_approaches: List[str] = field(default_factory=list)
    risks: List[str] = field(default_factory=list)
    assumptions: List[str] = field(default_factory=list)
    validation_status: str = "pending"
    validation_issues: List[str] = field(default_factory=list)
    revision_count: int = 0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "task": self.task_description,
            "steps": [step.to_dict() for step in self.steps],
            "success_criteria": self.success_criteria,
            "complexity": self.complexity.name.lower(),  # Output as string name
            "estimated_duration": self.estimated_duration,
            "alternative_approaches": self.alternative_approaches,
            "risks": self.risks,
            "assumptions": self.assumptions,
            "validation_status": self.validation_status,
            "validation_issues": self.validation_issues,
            "revision_count": self.revision_count
        }
    
    def get_next_executable_steps(self) -> List[PlanStep]:
        """Get steps that can be executed now."""
        completed = [s.step_id for s in self.steps if s.status == StepStatus.COMPLETED]
        return [
            step for step in self.steps
            if step.status == StepStatus.PENDING and step.can_execute(completed)
        ]
    
    def get_failed_steps(self) -> List[PlanStep]:
        """Get failed steps that can be retried."""
        return [s for s in self.steps if s.status == StepStatus.FAILED and s.can_retry()]
    
    def is_complete(self) -> bool:
        """Check if plan is fully executed."""
        return all(s.status == StepStatus.COMPLETED for s in self.steps)
    
    def is_blocked(self) -> bool:
        """Check if plan is blocked."""
        return any(s.status == StepStatus.BLOCKED for s in self.steps)
    
    def get_progress(self) -> float:
        """Get completion percentage."""
        if not self.steps:
            return 0.0
        completed = sum(1 for s in self.steps if s.status == StepStatus.COMPLETED)
        return (completed / len(self.steps)) * 100


class AdvancedPlannerNode(BaseNode):
    """
    Advanced planner with multi-step planning and validation.
    
    Features:
    - Decomposes complex tasks into detailed steps
    - Validates plan feasibility before execution
    - Identifies dependencies and parallel execution opportunities
    - Estimates complexity and duration
    - Provides alternative approaches and risk assessment
    """
    
    def __init__(
        self,
        llm: BaseChatModel,
        system_prompt: Optional[str] = None,
        validate_plans: bool = True,
        max_complexity: PlanComplexity = PlanComplexity.VERY_COMPLEX,
        name: str = "advanced_planner"
    ):
        """
        Initialize advanced planner.
        
        Args:
            llm: Language model for planning
            system_prompt: Optional custom system prompt
            validate_plans: Whether to validate plans before execution
            max_complexity: Maximum allowed plan complexity
            name: Node name
        """
        super().__init__(name=name, description="Advanced multi-step planning")
        self.llm = llm
        self.validate_plans = validate_plans
        self.max_complexity = max_complexity
        self._custom_prompt = system_prompt
        self.system_prompt = self._build_system_prompt()
        
        self._logger.info(f"AdvancedPlannerNode '{name}' initialized")
    
    def _build_system_prompt(self) -> str:
        """Build the system prompt for planning."""
        base_prompt = """You are an expert multi-step task planner with advanced reasoning capabilities.

Your responsibilities:
1. Analyze complex tasks and break them into detailed, executable steps
2. Identify dependencies between steps and optimal sequencing
3. Determine which teams/agents should handle each step
4. Estimate complexity, duration, and resource requirements
5. Identify potential risks and alternative approaches
6. Validate plan feasibility before execution

Output Format (JSON):
{
    "task": "Detailed task description",
    "complexity": "simple|moderate|complex|very_complex",
    "estimated_duration": "Estimated time in minutes",
    "steps": [
        {
            "step_id": "unique_identifier",
            "description": "What needs to be done",
            "assigned_team": "team_name",
            "dependencies": ["step_ids that must complete first"],
            "tools_required": ["tool1", "tool2"],
            "expected_output": "What this step produces",
            "confidence_score": 0.95
        }
    ],
    "success_criteria": "How to measure success",
    "risks": ["potential issues or challenges"],
    "assumptions": ["assumptions made during planning"],
    "alternative_approaches": ["other ways to accomplish the task"]
}

Planning Principles:
- Break tasks into atomic, testable steps
- Identify parallelizable steps (no dependencies)
- Consider error handling and fallback options
- Be realistic about complexity and time estimates
- Ensure each step has clear inputs and outputs
- Validate dependencies form a valid DAG (no cycles)
"""
        
        if self._custom_prompt:
            base_prompt += f"\n\nAdditional Instructions:\n{self._custom_prompt}"
        
        return base_prompt
    
    def execute(self, state: Dict[str, Any]) -> Command:
        """
        Execute advanced planning logic.
        
        Args:
            state: Current workflow state
            
        Returns:
            Command with plan and routing decision
        """
        self._logger.info("Advanced planner generating execution plan")
        
        # Get user request
        messages = state.get("messages", [])
        if not messages:
            self._logger.error("No messages in state")
            return Command(goto=END)
        
        # Generate plan
        plan_result = self._generate_plan(messages, state)
        
        if not plan_result:
            self._logger.error("Failed to generate plan")
            return Command(goto=END)
        
        plan, raw_response = plan_result
        
        # Validate plan if enabled
        if self.validate_plans:
            validation_result = self._validate_plan(plan)
            plan.validation_status = "passed" if validation_result[0] else "failed"
            plan.validation_issues = validation_result[1]
            
            if not validation_result[0]:
                self._logger.warning(f"Plan validation failed: {validation_result[1]}")
                # Optionally attempt to fix the plan
                # For now, we'll continue but mark as validation failed
        
        # Store plan in state
        goto = state.get("next_node", "supervisor")
        
        return Command(
            update={
                "messages": [
                    HumanMessage(content=raw_response, name=self.name)
                ],
                "full_plan": json.dumps(plan.to_dict(), indent=2),
                "execution_plan": plan.to_dict(),
                "plan_object": plan,
                "context": {
                    **state.get("context", {}),
                    "plan_complexity": plan.complexity.name.lower(),
                    "plan_steps": len(plan.steps)
                }
            },
            goto=goto
        )
    
    def _generate_plan(
        self,
        messages: List[Any],
        state: Dict[str, Any]
    ) -> Optional[Tuple[ExecutionPlan, str]]:
        """Generate a detailed execution plan."""
        try:
            # Prepare context
            available_teams = state.get("available_teams", [])
            context_info = f"\n\nAvailable teams: {', '.join(available_teams)}" if available_teams else ""
            
            # Build messages
            planning_messages = [
                SystemMessage(content=self.system_prompt + context_info),
            ] + messages
            
            # Generate plan
            response = self.llm.invoke(planning_messages)
            raw_content = response.content
            
            # Clean and parse JSON
            cleaned = self._clean_json_response(raw_content)
            plan_data = json.loads(cleaned)
            
            # Convert to ExecutionPlan object
            plan = self._parse_plan_data(plan_data)
            
            self._logger.info(
                f"Generated plan with {len(plan.steps)} steps, "
                f"complexity: {plan.complexity.name.lower()}"
            )
            
            return plan, cleaned
            
        except json.JSONDecodeError as e:
            self._logger.error(f"Failed to parse plan JSON: {e}")
            return None
        except Exception as e:
            self._logger.error(f"Error generating plan: {e}")
            return None
    
    def _parse_plan_data(self, data: Dict[str, Any]) -> ExecutionPlan:
        """Parse plan data into ExecutionPlan object."""
        # Parse complexity - handle both string and integer values
        complexity_value = data.get("complexity", "moderate")
        complexity = PlanComplexity.MODERATE
        
        # Try to match by name (string)
        if isinstance(complexity_value, str):
            complexity_str = complexity_value.lower()
            name_mapping = {
                "simple": PlanComplexity.SIMPLE,
                "moderate": PlanComplexity.MODERATE,
                "complex": PlanComplexity.COMPLEX,
                "very_complex": PlanComplexity.VERY_COMPLEX,
            }
            complexity = name_mapping.get(complexity_str, PlanComplexity.MODERATE)
        elif isinstance(complexity_value, int):
            # Handle integer values
            try:
                complexity = PlanComplexity(complexity_value)
            except ValueError:
                complexity = PlanComplexity.MODERATE
        
        # Parse steps
        steps = []
        for i, step_data in enumerate(data.get("steps", [])):
            step = PlanStep(
                step_id=step_data.get("step_id", f"step_{i+1}"),
                description=step_data.get("description", ""),
                assigned_team=step_data.get("assigned_team", "default"),
                dependencies=step_data.get("dependencies", []),
                tools_required=step_data.get("tools_required", []),
                expected_output=step_data.get("expected_output", ""),
                confidence_score=step_data.get("confidence_score", 1.0)
            )
            steps.append(step)
        
        # Create plan
        plan = ExecutionPlan(
            task_description=data.get("task", ""),
            steps=steps,
            success_criteria=data.get("success_criteria", ""),
            complexity=complexity,
            estimated_duration=data.get("estimated_duration"),
            alternative_approaches=data.get("alternative_approaches", []),
            risks=data.get("risks", []),
            assumptions=data.get("assumptions", [])
        )
        
        return plan
    
    def _validate_plan(self, plan: ExecutionPlan) -> Tuple[bool, List[str]]:
        """
        Validate plan feasibility.
        
        Returns:
            Tuple of (is_valid, list_of_issues)
        """
        issues = []
        
        # Check complexity - compare integer values of IntEnum
        current_complexity = self._get_complexity_level(len(plan.steps))
        if current_complexity.value > self.max_complexity.value:
            issues.append(
                f"Plan exceeds maximum complexity: {len(plan.steps)} steps"
            )
        
        # Check for empty steps
        if not plan.steps:
            issues.append("Plan has no steps")
        
        # Validate dependencies
        step_ids = {step.step_id for step in plan.steps}
        for step in plan.steps:
            for dep in step.dependencies:
                if dep not in step_ids:
                    issues.append(
                        f"Step '{step.step_id}' has invalid dependency: '{dep}'"
                    )
        
        # Check for circular dependencies
        if self._has_circular_dependencies(plan.steps):
            issues.append("Plan has circular dependencies")
        
        # Validate assigned teams
        for step in plan.steps:
            if not step.assigned_team:
                issues.append(f"Step '{step.step_id}' has no assigned team")
        
        return len(issues) == 0, issues
    
    def _has_circular_dependencies(self, steps: List[PlanStep]) -> bool:
        """Check for circular dependencies using DFS."""
        graph = {step.step_id: step.dependencies for step in steps}
        visited = set()
        rec_stack = set()
        
        def has_cycle(node: str) -> bool:
            visited.add(node)
            rec_stack.add(node)
            
            for neighbor in graph.get(node, []):
                if neighbor not in visited:
                    if has_cycle(neighbor):
                        return True
                elif neighbor in rec_stack:
                    return True
            
            rec_stack.remove(node)
            return False
        
        for step_id in graph:
            if step_id not in visited:
                if has_cycle(step_id):
                    return True
        
        return False
    
    def _get_complexity_level(self, num_steps: int) -> PlanComplexity:
        """Determine complexity level based on number of steps."""
        if num_steps <= 3:
            return PlanComplexity.SIMPLE
        elif num_steps <= 7:
            return PlanComplexity.MODERATE
        elif num_steps <= 15:
            return PlanComplexity.COMPLEX
        else:
            return PlanComplexity.VERY_COMPLEX
    
    def _clean_json_response(self, response: str) -> str:
        """Clean JSON response by removing markdown formatting."""
        cleaned = response.strip()
        
        # Remove code fences
        if cleaned.startswith("```json"):
            cleaned = cleaned[7:]
        elif cleaned.startswith("```"):
            cleaned = cleaned[3:]
        
        if cleaned.endswith("```"):
            cleaned = cleaned[:-3]
        
        return cleaned.strip()


def create_advanced_planner(
    llm: BaseChatModel,
    system_prompt: Optional[str] = None,
    validate_plans: bool = True,
    max_complexity: PlanComplexity = PlanComplexity.VERY_COMPLEX,
    name: str = "advanced_planner"
) -> AdvancedPlannerNode:
    """
    Factory function to create an advanced planner node.
    
    Args:
        llm: Language model
        system_prompt: Optional custom prompt
        validate_plans: Whether to validate plans
        max_complexity: Maximum plan complexity
        name: Node name
        
    Returns:
        AdvancedPlannerNode instance
    """
    return AdvancedPlannerNode(
        llm=llm,
        system_prompt=system_prompt,
        validate_plans=validate_plans,
        max_complexity=max_complexity,
        name=name
    )
