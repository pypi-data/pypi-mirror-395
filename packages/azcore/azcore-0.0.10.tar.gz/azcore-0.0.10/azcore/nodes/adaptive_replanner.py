"""
Adaptive Re-planning Module for Dynamic Plan Adjustment.

This module provides adaptive re-planning capabilities including:
- Dynamic plan adjustment based on execution feedback
- Failure recovery and alternative path finding
- Real-time plan optimization
- Learning from execution outcomes
"""

from typing import Dict, Any, List, Optional, Tuple
import json
from dataclasses import dataclass
from enum import Enum
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.types import Command
from azcore.core.base import BaseNode
from azcore.nodes.advanced_planner import (
    ExecutionPlan, PlanStep, StepStatus, PlanComplexity
)
import logging

logger = logging.getLogger(__name__)


class ReplanTrigger(Enum):
    """Reasons for triggering re-planning."""
    STEP_FAILURE = "step_failure"
    BLOCKED_DEPENDENCY = "blocked_dependency"
    RESOURCE_UNAVAILABLE = "resource_unavailable"
    TIMEOUT = "timeout"
    QUALITY_ISSUE = "quality_issue"
    USER_FEEDBACK = "user_feedback"
    BETTER_PATH_FOUND = "better_path_found"
    CONTEXT_CHANGE = "context_change"


class ReplanStrategy(Enum):
    """Strategies for re-planning."""
    RETRY_FAILED = "retry_failed"  # Retry failed steps
    FIND_ALTERNATIVE = "find_alternative"  # Find alternative approach
    SKIP_AND_CONTINUE = "skip_and_continue"  # Skip problematic step
    DECOMPOSE_FURTHER = "decompose_further"  # Break step into smaller steps
    MERGE_STEPS = "merge_steps"  # Combine steps for efficiency
    REORDER_STEPS = "reorder_steps"  # Change execution order
    ADD_VALIDATION = "add_validation"  # Add validation steps
    FULL_REPLAN = "full_replan"  # Complete plan regeneration


@dataclass
class ReplanEvent:
    """Represents a re-planning event."""
    trigger: ReplanTrigger
    affected_steps: List[str]
    description: str
    timestamp: float
    context: Dict[str, Any]
    strategy_used: Optional[ReplanStrategy] = None
    success: bool = False


class AdaptiveReplannerNode(BaseNode):
    """
    Adaptive re-planner that adjusts plans based on execution feedback.
    
    Features:
    - Monitors plan execution and detects issues
    - Automatically triggers re-planning when needed
    - Applies different strategies based on failure type
    - Learns from past failures to improve future plans
    - Maintains plan history for rollback if needed
    """
    
    def __init__(
        self,
        llm: BaseChatModel,
        max_replan_attempts: int = 3,
        enable_learning: bool = True,
        name: str = "adaptive_replanner"
    ):
        """
        Initialize adaptive re-planner.
        
        Args:
            llm: Language model for re-planning
            max_replan_attempts: Maximum re-planning attempts
            enable_learning: Whether to learn from failures
            name: Node name
        """
        super().__init__(name=name, description="Adaptive plan re-planning")
        self.llm = llm
        self.max_replan_attempts = max_replan_attempts
        self.enable_learning = enable_learning
        self.replan_history: List[ReplanEvent] = []
        self.system_prompt = self._build_system_prompt()
        
        self._logger.info(f"AdaptiveReplannerNode '{name}' initialized")
    
    def _build_system_prompt(self) -> str:
        """Build the system prompt for re-planning."""
        return """You are an expert adaptive planner that adjusts execution plans based on feedback and failures.

Your responsibilities:
1. Analyze plan execution status and identify issues
2. Determine root cause of failures or blockages
3. Select appropriate re-planning strategy
4. Generate modified plan that addresses the issues
5. Ensure the revised plan maintains the original goal

Re-planning Strategies:
- RETRY_FAILED: Retry failed steps with adjustments
- FIND_ALTERNATIVE: Find completely different approach
- SKIP_AND_CONTINUE: Skip problematic step if non-critical
- DECOMPOSE_FURTHER: Break complex step into smaller ones
- MERGE_STEPS: Combine steps to reduce overhead
- REORDER_STEPS: Change execution order to avoid issues
- ADD_VALIDATION: Add checks to prevent similar failures
- FULL_REPLAN: Regenerate entire plan from scratch

Output Format (JSON):
{
    "analysis": "Analysis of what went wrong and why",
    "strategy": "chosen_strategy",
    "modifications": [
        {
            "action": "add|remove|modify",
            "step_id": "affected_step",
            "changes": "description of changes",
            "rationale": "why this change helps"
        }
    ],
    "revised_steps": [
        {
            "step_id": "unique_id",
            "description": "what to do",
            "assigned_team": "team_name",
            "dependencies": [],
            "tools_required": [],
            "expected_output": "expected result"
        }
    ],
    "risk_mitigation": ["steps taken to prevent similar failures"],
    "confidence": 0.85
}

Principles:
- Preserve completed work when possible
- Minimize disruption to running steps
- Learn from failures to prevent recurrence
- Balance between retrying and finding alternatives
- Consider cost and time when re-planning
"""
    
    def execute(self, state: Dict[str, Any]) -> Command:
        """
        Execute adaptive re-planning logic.
        
        Args:
            state: Current workflow state with execution feedback
            
        Returns:
            Command with revised plan
        """
        self._logger.info("Analyzing execution status for potential re-planning")
        
        # Get current plan
        plan_dict = state.get("execution_plan")
        if not plan_dict:
            self._logger.error("No execution plan found in state")
            return Command(goto="supervisor")
        
        # Get execution feedback
        feedback = state.get("execution_feedback", {})
        
        # Check if re-planning is needed
        trigger = self._check_replan_triggers(plan_dict, feedback)
        
        if not trigger:
            self._logger.info("No re-planning needed, continuing execution")
            return Command(goto=state.get("next_node", "supervisor"))
        
        # Perform re-planning
        replan_result = self._replan(plan_dict, feedback, trigger, state)
        
        if not replan_result:
            self._logger.error("Re-planning failed")
            return Command(goto="supervisor")
        
        revised_plan, strategy = replan_result
        
        # Record re-planning event
        event = ReplanEvent(
            trigger=trigger,
            affected_steps=[s.step_id for s in revised_plan.steps],
            description=f"Re-planned due to {trigger.value}",
            timestamp=self._get_timestamp(),
            context=feedback,
            strategy_used=strategy,
            success=True
        )
        self.replan_history.append(event)
        
        # Update state
        return Command(
            update={
                "execution_plan": revised_plan.to_dict(),
                "plan_object": revised_plan,
                "messages": [
                    HumanMessage(
                        content=f"Plan revised using {strategy.value} strategy",
                        name=self.name
                    )
                ],
                "context": {
                    **state.get("context", {}),
                    "replan_count": state.get("context", {}).get("replan_count", 0) + 1,
                    "last_replan_trigger": trigger.value
                }
            },
            goto=state.get("next_node", "supervisor")
        )
    
    def _check_replan_triggers(
        self,
        plan_dict: Dict[str, Any],
        feedback: Dict[str, Any]
    ) -> Optional[ReplanTrigger]:
        """
        Check if re-planning should be triggered.
        
        Returns:
            ReplanTrigger if re-planning needed, None otherwise
        """
        # Check for failed steps
        if feedback.get("has_failures", False):
            return ReplanTrigger.STEP_FAILURE
        
        # Check for blocked dependencies
        if feedback.get("is_blocked", False):
            return ReplanTrigger.BLOCKED_DEPENDENCY
        
        # Check for resource issues
        if feedback.get("resource_unavailable", False):
            return ReplanTrigger.RESOURCE_UNAVAILABLE
        
        # Check for timeout
        if feedback.get("timeout_exceeded", False):
            return ReplanTrigger.TIMEOUT
        
        # Check for quality issues
        if feedback.get("quality_score", 1.0) < 0.5:
            return ReplanTrigger.QUALITY_ISSUE
        
        # Check for user feedback
        if feedback.get("user_intervention", False):
            return ReplanTrigger.USER_FEEDBACK
        
        # Check for context changes
        if feedback.get("context_changed", False):
            return ReplanTrigger.CONTEXT_CHANGE
        
        return None
    
    def _replan(
        self,
        plan_dict: Dict[str, Any],
        feedback: Dict[str, Any],
        trigger: ReplanTrigger,
        state: Dict[str, Any]
    ) -> Optional[Tuple[ExecutionPlan, ReplanStrategy]]:
        """
        Perform re-planning based on feedback.
        
        Returns:
            Tuple of (revised_plan, strategy_used) or None
        """
        try:
            # Determine strategy
            strategy = self._select_strategy(trigger, feedback, plan_dict)
            
            # Build re-planning prompt
            replan_prompt = self._build_replan_prompt(
                plan_dict, feedback, trigger, strategy
            )
            
            # Generate revised plan
            messages = [
                SystemMessage(content=self.system_prompt),
                HumanMessage(content=replan_prompt)
            ]
            
            response = self.llm.invoke(messages)
            cleaned = self._clean_json_response(response.content)
            replan_data = json.loads(cleaned)
            
            # Apply modifications to plan
            revised_plan = self._apply_modifications(
                plan_dict, replan_data, strategy
            )
            
            self._logger.info(
                f"Re-planning completed using {strategy.value} strategy, "
                f"{len(revised_plan.steps)} steps in revised plan"
            )
            
            return revised_plan, strategy
            
        except Exception as e:
            self._logger.error(f"Error during re-planning: {e}")
            return None
    
    def _select_strategy(
        self,
        trigger: ReplanTrigger,
        feedback: Dict[str, Any],
        plan_dict: Dict[str, Any]
    ) -> ReplanStrategy:
        """Select appropriate re-planning strategy."""
        # Map triggers to strategies
        strategy_map = {
            ReplanTrigger.STEP_FAILURE: ReplanStrategy.RETRY_FAILED,
            ReplanTrigger.BLOCKED_DEPENDENCY: ReplanStrategy.REORDER_STEPS,
            ReplanTrigger.RESOURCE_UNAVAILABLE: ReplanStrategy.FIND_ALTERNATIVE,
            ReplanTrigger.TIMEOUT: ReplanStrategy.DECOMPOSE_FURTHER,
            ReplanTrigger.QUALITY_ISSUE: ReplanStrategy.ADD_VALIDATION,
            ReplanTrigger.USER_FEEDBACK: ReplanStrategy.FULL_REPLAN,
            ReplanTrigger.CONTEXT_CHANGE: ReplanStrategy.FULL_REPLAN,
        }
        
        # Check if we should do full replan based on history
        replan_count = len([e for e in self.replan_history if e.trigger == trigger])
        if replan_count >= 2:
            return ReplanStrategy.FULL_REPLAN
        
        return strategy_map.get(trigger, ReplanStrategy.FIND_ALTERNATIVE)
    
    def _build_replan_prompt(
        self,
        plan_dict: Dict[str, Any],
        feedback: Dict[str, Any],
        trigger: ReplanTrigger,
        strategy: ReplanStrategy
    ) -> str:
        """Build prompt for re-planning."""
        prompt = f"""Current Plan:
{json.dumps(plan_dict, indent=2)}

Execution Feedback:
{json.dumps(feedback, indent=2)}

Re-planning Trigger: {trigger.value}
Recommended Strategy: {strategy.value}

Please analyze the situation and generate a revised plan that addresses the issues.
Focus on:
1. Understanding what went wrong
2. Applying the recommended strategy
3. Maintaining the original goal
4. Preventing similar failures

Provide a complete revised plan with all necessary modifications.
"""
        
        # Add learning from history
        if self.enable_learning and self.replan_history:
            similar_events = [
                e for e in self.replan_history
                if e.trigger == trigger and e.success
            ]
            if similar_events:
                prompt += f"\n\nPrevious successful approaches for {trigger.value}:\n"
                for event in similar_events[-3:]:  # Last 3 successful
                    prompt += f"- Used {event.strategy_used.value}\n"
        
        return prompt
    
    def _apply_modifications(
        self,
        original_plan: Dict[str, Any],
        replan_data: Dict[str, Any],
        strategy: ReplanStrategy
    ) -> ExecutionPlan:
        """Apply modifications to create revised plan."""
        # For now, use the revised steps from replan_data
        # In a more sophisticated version, we could selectively apply changes
        
        revised_steps = []
        for step_data in replan_data.get("revised_steps", []):
            step = PlanStep(
                step_id=step_data.get("step_id", ""),
                description=step_data.get("description", ""),
                assigned_team=step_data.get("assigned_team", ""),
                dependencies=step_data.get("dependencies", []),
                tools_required=step_data.get("tools_required", []),
                expected_output=step_data.get("expected_output", "")
            )
            revised_steps.append(step)
        
        # Preserve completed steps from original plan if possible
        if strategy != ReplanStrategy.FULL_REPLAN:
            original_steps = original_plan.get("steps", [])
            completed_steps = [
                s for s in original_steps
                if s.get("status") == StepStatus.COMPLETED.value
            ]
            # Add completed steps that aren't in revised plan
            completed_ids = {s["step_id"] for s in completed_steps}
            revised_ids = {s.step_id for s in revised_steps}
            
            for comp_step in completed_steps:
                if comp_step["step_id"] not in revised_ids:
                    step = PlanStep(
                        step_id=comp_step["step_id"],
                        description=comp_step["description"],
                        assigned_team=comp_step["assigned_team"],
                        dependencies=comp_step["dependencies"],
                        tools_required=comp_step.get("tools_required", []),
                        expected_output=comp_step.get("expected_output", ""),
                        status=StepStatus.COMPLETED
                    )
                    revised_steps.insert(0, step)
        
        # Create revised plan
        revised_plan = ExecutionPlan(
            task_description=original_plan.get("task", ""),
            steps=revised_steps,
            success_criteria=original_plan.get("success_criteria", ""),
            complexity=PlanComplexity.MODERATE,
            revision_count=original_plan.get("revision_count", 0) + 1
        )
        
        return revised_plan
    
    def _clean_json_response(self, response: str) -> str:
        """Clean JSON response."""
        cleaned = response.strip()
        if cleaned.startswith("```json"):
            cleaned = cleaned[7:]
        elif cleaned.startswith("```"):
            cleaned = cleaned[3:]
        if cleaned.endswith("```"):
            cleaned = cleaned[:-3]
        return cleaned.strip()
    
    def _get_timestamp(self) -> float:
        """Get current timestamp."""
        import time
        return time.time()
    
    def get_replan_history(self) -> List[ReplanEvent]:
        """Get re-planning history."""
        return self.replan_history.copy()
    
    def reset_history(self) -> None:
        """Reset re-planning history."""
        self.replan_history.clear()
        self._logger.info("Re-planning history reset")


def create_adaptive_replanner(
    llm: BaseChatModel,
    max_replan_attempts: int = 3,
    enable_learning: bool = True,
    name: str = "adaptive_replanner"
) -> AdaptiveReplannerNode:
    """
    Factory function to create an adaptive re-planner node.
    
    Args:
        llm: Language model
        max_replan_attempts: Maximum re-planning attempts
        enable_learning: Whether to learn from failures
        name: Node name
        
    Returns:
        AdaptiveReplannerNode instance
    """
    return AdaptiveReplannerNode(
        llm=llm,
        max_replan_attempts=max_replan_attempts,
        enable_learning=enable_learning,
        name=name
    )
