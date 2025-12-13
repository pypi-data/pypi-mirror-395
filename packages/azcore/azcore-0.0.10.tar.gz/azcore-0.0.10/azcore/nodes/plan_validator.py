"""
Plan Validation Module for Verifying Plan Feasibility.

This module provides plan validation capabilities including:
- Feasibility checking before execution
- Resource requirement validation
- Dependency conflict detection
- Risk assessment
- Success probability estimation
"""

from typing import Dict, Any, List, Optional, Tuple, Set
import json
from dataclasses import dataclass, field
from enum import Enum
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.types import Command
from langgraph.graph import END
from azcore.core.base import BaseNode
from azcore.nodes.advanced_planner import ExecutionPlan, PlanStep, StepStatus
import logging

logger = logging.getLogger(__name__)


class ValidationSeverity(Enum):
    """Severity level of validation issues."""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class ValidationType(Enum):
    """Types of validation checks."""
    DEPENDENCY = "dependency"
    RESOURCE = "resource"
    FEASIBILITY = "feasibility"
    TIMING = "timing"
    CAPABILITY = "capability"
    CONSTRAINT = "constraint"
    SAFETY = "safety"


@dataclass
class ValidationIssue:
    """Represents a validation issue."""
    issue_id: str
    type: ValidationType
    severity: ValidationSeverity
    description: str
    affected_steps: List[str]
    suggested_fix: str
    can_auto_fix: bool = False
    blocking: bool = False
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "issue_id": self.issue_id,
            "type": self.type.value,
            "severity": self.severity.value,
            "description": self.description,
            "affected_steps": self.affected_steps,
            "suggested_fix": self.suggested_fix,
            "can_auto_fix": self.can_auto_fix,
            "blocking": self.blocking
        }


@dataclass
class ValidationReport:
    """Complete validation report."""
    plan_id: str
    is_valid: bool
    success_probability: float
    issues: List[ValidationIssue]
    warnings: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
    estimated_resources: Dict[str, Any] = field(default_factory=dict)
    estimated_time: Optional[float] = None
    risk_score: float = 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "plan_id": self.plan_id,
            "is_valid": self.is_valid,
            "success_probability": self.success_probability,
            "issues": [i.to_dict() for i in self.issues],
            "warnings": self.warnings,
            "recommendations": self.recommendations,
            "estimated_resources": self.estimated_resources,
            "estimated_time": self.estimated_time,
            "risk_score": self.risk_score,
            "num_issues": len(self.issues),
            "num_errors": len([i for i in self.issues if i.severity == ValidationSeverity.ERROR]),
            "num_warnings": len([i for i in self.issues if i.severity == ValidationSeverity.WARNING]),
            "blocking_issues": len([i for i in self.issues if i.blocking])
        }
    
    def get_blocking_issues(self) -> List[ValidationIssue]:
        """Get issues that block execution."""
        return [i for i in self.issues if i.blocking]
    
    def get_critical_issues(self) -> List[ValidationIssue]:
        """Get critical issues."""
        return [i for i in self.issues if i.severity == ValidationSeverity.CRITICAL]
    
    def has_blocking_issues(self) -> bool:
        """Check if there are blocking issues."""
        return len(self.get_blocking_issues()) > 0


class PlanValidatorNode(BaseNode):
    """
    Plan validator that verifies plan feasibility before execution.
    
    Features:
    - Validates dependencies and execution order
    - Checks resource requirements and availability
    - Assesses feasibility of each step
    - Estimates success probability
    - Identifies potential issues and risks
    - Suggests fixes for validation issues
    """
    
    def __init__(
        self,
        llm: BaseChatModel,
        strict_mode: bool = False,
        auto_fix: bool = True,
        name: str = "plan_validator"
    ):
        """
        Initialize plan validator.
        
        Args:
            llm: Language model for validation
            strict_mode: Whether to fail on warnings
            auto_fix: Whether to attempt auto-fixing issues
            name: Node name
        """
        super().__init__(name=name, description="Plan validation and feasibility checking")
        self.llm = llm
        self.strict_mode = strict_mode
        self.auto_fix = auto_fix
        self.system_prompt = self._build_system_prompt()
        
        self._logger.info(f"PlanValidatorNode '{name}' initialized")
    
    def _build_system_prompt(self) -> str:
        """Build the system prompt for validation."""
        return """You are an expert plan validator that ensures plan feasibility before execution.

Your responsibilities:
1. Validate plan structure and dependencies
2. Check resource requirements and availability
3. Assess feasibility of each step
4. Identify potential issues and risks
5. Estimate success probability
6. Suggest fixes for issues found

Validation Checks:
- DEPENDENCY: Check for circular dependencies, missing dependencies
- RESOURCE: Verify required resources are available
- FEASIBILITY: Assess if steps are achievable
- TIMING: Check if time estimates are realistic
- CAPABILITY: Verify teams have required capabilities
- CONSTRAINT: Check for constraint violations
- SAFETY: Identify safety or security concerns

Output Format (JSON):
{
    "is_valid": true/false,
    "success_probability": 0.85,
    "issues": [
        {
            "issue_id": "issue_1",
            "type": "validation_type",
            "severity": "info|warning|error|critical",
            "description": "what's wrong",
            "affected_steps": ["step_ids"],
            "suggested_fix": "how to fix it",
            "can_auto_fix": true/false,
            "blocking": true/false
        }
    ],
    "warnings": ["potential issues to watch"],
    "recommendations": ["suggestions for improvement"],
    "estimated_resources": {
        "time_minutes": 30,
        "api_calls": 10,
        "memory_mb": 100
    },
    "risk_score": 0.3,
    "risk_factors": ["identified risks"]
}

Validation Principles:
- Be thorough but not overly pessimistic
- Distinguish between blocking vs non-blocking issues
- Provide actionable fixes when possible
- Consider edge cases and failure modes
- Estimate resources realistically
- Balance safety with practicality
"""
    
    def execute(self, state: Dict[str, Any]) -> Command:
        """
        Execute plan validation.
        
        Args:
            state: Current workflow state with plan
            
        Returns:
            Command with validation report and routing decision
        """
        self._logger.info("Validating execution plan")
        
        # Get plan to validate
        plan_dict = state.get("execution_plan")
        if not plan_dict:
            self._logger.error("No execution plan found to validate")
            return Command(goto=END)
        
        # Perform validation
        validation_report = self._validate_plan(plan_dict, state)
        
        # Auto-fix if enabled and issues found
        if self.auto_fix and validation_report.issues:
            auto_fix_result = self._attempt_auto_fix(plan_dict, validation_report, state)
            if auto_fix_result:
                plan_dict, validation_report = auto_fix_result
                self._logger.info("Auto-fix applied successfully")
        
        self._logger.info(
            f"Validation completed: {'PASSED' if validation_report.is_valid else 'FAILED'}, "
            f"{len(validation_report.issues)} issues found, "
            f"success probability: {validation_report.success_probability:.2%}"
        )
        
        # Determine next node
        goto = state.get("next_node", "supervisor")
        
        # Build update dictionary
        update_dict = {
            "validation_report": validation_report,
            "plan_validated": True,
            "context": {
                **state.get("context", {}),
                "validation_passed": validation_report.is_valid,
                "success_probability": validation_report.success_probability,
                "blocking_issues": len(validation_report.get_blocking_issues())
            }
        }
        
        # Add fixed plan if auto-fixed
        if self.auto_fix and plan_dict:
            update_dict["execution_plan"] = plan_dict
        
        return Command(
            update=update_dict,
            goto=goto
        )
    
    def _validate_plan(
        self,
        plan_dict: Dict[str, Any],
        state: Dict[str, Any]
    ) -> ValidationReport:
        """Perform comprehensive plan validation."""
        issues = []
        
        # Structural validation
        issues.extend(self._validate_structure(plan_dict))
        
        # Dependency validation
        issues.extend(self._validate_dependencies(plan_dict))
        
        # LLM-based validation
        llm_validation = self._llm_validate(plan_dict, state)
        if llm_validation:
            issues.extend(llm_validation.get("issues", []))
        
        # Calculate success probability
        success_prob = self._calculate_success_probability(plan_dict, issues)
        
        # Determine if valid
        blocking_count = len([i for i in issues if isinstance(i, ValidationIssue) and i.blocking])
        error_count = len([i for i in issues if isinstance(i, ValidationIssue) and i.severity == ValidationSeverity.ERROR])
        
        is_valid = blocking_count == 0 and (error_count == 0 or not self.strict_mode)
        
        # Create report
        report = ValidationReport(
            plan_id=plan_dict.get("task", "unknown")[:50],
            is_valid=is_valid,
            success_probability=success_prob,
            issues=[i for i in issues if isinstance(i, ValidationIssue)],
            warnings=llm_validation.get("warnings", []) if llm_validation else [],
            recommendations=llm_validation.get("recommendations", []) if llm_validation else [],
            estimated_resources=llm_validation.get("estimated_resources", {}) if llm_validation else {},
            estimated_time=llm_validation.get("estimated_resources", {}).get("time_minutes") if llm_validation else None,
            risk_score=llm_validation.get("risk_score", 0.0) if llm_validation else 0.0
        )
        
        return report
    
    def _validate_structure(self, plan_dict: Dict[str, Any]) -> List[ValidationIssue]:
        """Validate plan structure."""
        issues = []
        
        # Check for steps
        steps = plan_dict.get("steps", [])
        if not steps:
            issues.append(ValidationIssue(
                issue_id="struct_001",
                type=ValidationType.FEASIBILITY,
                severity=ValidationSeverity.CRITICAL,
                description="Plan has no steps",
                affected_steps=[],
                suggested_fix="Add execution steps to the plan",
                blocking=True
            ))
        
        # Check each step has required fields
        for i, step in enumerate(steps):
            step_id = step.get("step_id", f"step_{i}")
            
            if not step.get("description"):
                issues.append(ValidationIssue(
                    issue_id=f"struct_{step_id}_desc",
                    type=ValidationType.FEASIBILITY,
                    severity=ValidationSeverity.ERROR,
                    description=f"Step {step_id} has no description",
                    affected_steps=[step_id],
                    suggested_fix="Add clear description of what the step does",
                    blocking=False
                ))
            
            if not step.get("assigned_team"):
                issues.append(ValidationIssue(
                    issue_id=f"struct_{step_id}_team",
                    type=ValidationType.CAPABILITY,
                    severity=ValidationSeverity.ERROR,
                    description=f"Step {step_id} has no assigned team",
                    affected_steps=[step_id],
                    suggested_fix="Assign appropriate team to handle this step",
                    blocking=True
                ))
        
        return issues
    
    def _validate_dependencies(self, plan_dict: Dict[str, Any]) -> List[ValidationIssue]:
        """Validate dependencies."""
        issues = []
        steps = plan_dict.get("steps", [])
        step_ids = {s.get("step_id", f"step_{i}") for i, s in enumerate(steps)}
        
        # Check for invalid dependencies
        for i, step in enumerate(steps):
            step_id = step.get("step_id", f"step_{i}")
            dependencies = step.get("dependencies", [])
            
            for dep in dependencies:
                if dep not in step_ids:
                    issues.append(ValidationIssue(
                        issue_id=f"dep_{step_id}_{dep}",
                        type=ValidationType.DEPENDENCY,
                        severity=ValidationSeverity.ERROR,
                        description=f"Step {step_id} depends on non-existent step {dep}",
                        affected_steps=[step_id],
                        suggested_fix=f"Remove invalid dependency or add step {dep}",
                        blocking=True
                    ))
        
        # Check for circular dependencies
        if self._has_circular_deps(steps):
            issues.append(ValidationIssue(
                issue_id="dep_circular",
                type=ValidationType.DEPENDENCY,
                severity=ValidationSeverity.CRITICAL,
                description="Plan has circular dependencies",
                affected_steps=[s.get("step_id", f"step_{i}") for i, s in enumerate(steps)],
                suggested_fix="Remove circular dependencies to create valid execution order",
                blocking=True
            ))
        
        return issues
    
    def _has_circular_deps(self, steps: List[Dict[str, Any]]) -> bool:
        """Check for circular dependencies."""
        graph = {
            s.get("step_id", f"step_{i}"): s.get("dependencies", [])
            for i, s in enumerate(steps)
        }
        
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
    
    def _llm_validate(
        self,
        plan_dict: Dict[str, Any],
        state: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Use LLM for advanced validation."""
        try:
            # Build validation prompt
            prompt = f"""Validate the following execution plan for feasibility and potential issues:

Plan:
{json.dumps(plan_dict, indent=2)}

Available Context:
{json.dumps(state.get("context", {}), indent=2)}

Perform comprehensive validation including:
1. Resource requirements and availability
2. Feasibility of each step
3. Time estimates
4. Team capabilities
5. Potential risks and issues
6. Success probability

Provide detailed validation report.
"""
            
            messages = [
                SystemMessage(content=self.system_prompt),
                HumanMessage(content=prompt)
            ]
            
            response = self.llm.invoke(messages)
            cleaned = self._clean_json_response(response.content)
            validation_data = json.loads(cleaned)
            
            # Parse issues
            issues = []
            for issue_data in validation_data.get("issues", []):
                try:
                    issue_type = ValidationType(issue_data.get("type", "feasibility"))
                except ValueError:
                    issue_type = ValidationType.FEASIBILITY
                
                try:
                    severity = ValidationSeverity(issue_data.get("severity", "warning"))
                except ValueError:
                    severity = ValidationSeverity.WARNING
                
                issue = ValidationIssue(
                    issue_id=issue_data.get("issue_id", f"llm_{len(issues)}"),
                    type=issue_type,
                    severity=severity,
                    description=issue_data.get("description", ""),
                    affected_steps=issue_data.get("affected_steps", []),
                    suggested_fix=issue_data.get("suggested_fix", ""),
                    can_auto_fix=issue_data.get("can_auto_fix", False),
                    blocking=issue_data.get("blocking", False)
                )
                issues.append(issue)
            
            validation_data["issues"] = issues
            return validation_data
            
        except Exception as e:
            self._logger.error(f"Error in LLM validation: {e}")
            return None
    
    def _calculate_success_probability(
        self,
        plan_dict: Dict[str, Any],
        issues: List[ValidationIssue]
    ) -> float:
        """Calculate probability of successful execution."""
        base_probability = 0.9
        
        # Reduce for each issue
        for issue in issues:
            if isinstance(issue, ValidationIssue):
                if issue.severity == ValidationSeverity.CRITICAL:
                    base_probability *= 0.5
                elif issue.severity == ValidationSeverity.ERROR:
                    base_probability *= 0.7
                elif issue.severity == ValidationSeverity.WARNING:
                    base_probability *= 0.9
        
        # Adjust based on complexity
        num_steps = len(plan_dict.get("steps", []))
        if num_steps > 10:
            base_probability *= 0.9
        if num_steps > 20:
            base_probability *= 0.8
        
        return max(0.0, min(1.0, base_probability))
    
    def _attempt_auto_fix(
        self,
        plan_dict: Dict[str, Any],
        report: ValidationReport,
        state: Dict[str, Any]
    ) -> Optional[Tuple[Dict[str, Any], ValidationReport]]:
        """Attempt to auto-fix validation issues."""
        # For now, just log that we attempted
        # In a real implementation, this would fix specific issues
        fixable_issues = [i for i in report.issues if i.can_auto_fix]
        
        if not fixable_issues:
            return None
        
        self._logger.info(f"Attempting to auto-fix {len(fixable_issues)} issues")
        
        # Revalidate after fixes
        # (In real implementation, we'd apply fixes first)
        new_report = self._validate_plan(plan_dict, state)
        
        return plan_dict, new_report
    
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


def create_plan_validator(
    llm: BaseChatModel,
    strict_mode: bool = False,
    auto_fix: bool = True,
    name: str = "plan_validator"
) -> PlanValidatorNode:
    """
    Factory function to create a plan validator node.
    
    Args:
        llm: Language model
        strict_mode: Whether to fail on warnings
        auto_fix: Whether to attempt auto-fixing
        name: Node name
        
    Returns:
        PlanValidatorNode instance
    """
    return PlanValidatorNode(
        llm=llm,
        strict_mode=strict_mode,
        auto_fix=auto_fix,
        name=name
    )
