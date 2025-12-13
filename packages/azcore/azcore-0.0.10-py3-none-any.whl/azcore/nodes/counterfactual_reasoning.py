"""
Counterfactual Reasoning Module for "What-If" Scenario Analysis.

This module provides counterfactual reasoning capabilities including:
- What-if scenario generation and analysis
- Alternative outcome exploration
- Decision impact assessment
- Counterfactual explanation generation
"""

from typing import Dict, Any, List, Optional, Tuple
import json
from dataclasses import dataclass, field
from enum import Enum
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.types import Command
from langgraph.graph import END
from azcore.core.base import BaseNode
import logging

logger = logging.getLogger(__name__)


class CounterfactualType(Enum):
    """Types of counterfactual scenarios."""
    ACTION_CHANGE = "action_change"  # What if we did X instead of Y
    RESOURCE_CHANGE = "resource_change"  # What if we had more/less resources
    TIMING_CHANGE = "timing_change"  # What if we acted earlier/later
    ORDERING_CHANGE = "ordering_change"  # What if we changed the order
    TOOL_CHANGE = "tool_change"  # What if we used different tools
    TEAM_CHANGE = "team_change"  # What if different team handled it
    CONDITION_CHANGE = "condition_change"  # What if conditions were different
    PREVENTION = "prevention"  # What if we prevented something
    ADDITION = "addition"  # What if we added something


class OutcomeComparison(Enum):
    """Comparison of counterfactual outcome vs actual."""
    MUCH_BETTER = "much_better"
    BETTER = "better"
    SIMILAR = "similar"
    WORSE = "worse"
    MUCH_WORSE = "much_worse"


@dataclass
class CounterfactualScenario:
    """Represents a counterfactual scenario."""
    scenario_id: str
    type: CounterfactualType
    description: str
    changes: List[str]
    predicted_outcome: str
    comparison: OutcomeComparison
    probability: float  # Likelihood scenario would have this outcome
    confidence: float  # Confidence in the prediction
    explanation: str
    advantages: List[str] = field(default_factory=list)
    disadvantages: List[str] = field(default_factory=list)
    risks: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "scenario_id": self.scenario_id,
            "type": self.type.value,
            "description": self.description,
            "changes": self.changes,
            "predicted_outcome": self.predicted_outcome,
            "comparison": self.comparison.value,
            "probability": self.probability,
            "confidence": self.confidence,
            "explanation": self.explanation,
            "advantages": self.advantages,
            "disadvantages": self.disadvantages,
            "risks": self.risks
        }


@dataclass
class CounterfactualAnalysis:
    """Complete counterfactual analysis results."""
    actual_situation: str
    actual_outcome: str
    scenarios: List[CounterfactualScenario]
    best_alternative: Optional[str] = None
    worst_alternative: Optional[str] = None
    insights: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "actual_situation": self.actual_situation,
            "actual_outcome": self.actual_outcome,
            "scenarios": [s.to_dict() for s in self.scenarios],
            "best_alternative": self.best_alternative,
            "worst_alternative": self.worst_alternative,
            "insights": self.insights,
            "recommendations": self.recommendations,
            "num_scenarios": len(self.scenarios)
        }
    
    def get_better_scenarios(self) -> List[CounterfactualScenario]:
        """Get scenarios with better outcomes."""
        return [
            s for s in self.scenarios
            if s.comparison in [OutcomeComparison.BETTER, OutcomeComparison.MUCH_BETTER]
        ]
    
    def get_high_confidence_scenarios(self, threshold: float = 0.7) -> List[CounterfactualScenario]:
        """Get high confidence scenarios."""
        return [s for s in self.scenarios if s.confidence >= threshold]


class CounterfactualReasoningNode(BaseNode):
    """
    Counterfactual reasoning node for what-if scenario analysis.
    
    Features:
    - Generates alternative scenarios for decisions
    - Predicts outcomes of different choices
    - Compares actual vs counterfactual outcomes
    - Identifies better alternative approaches
    - Provides insights for future decision-making
    """
    
    def __init__(
        self,
        llm: BaseChatModel,
        num_scenarios: int = 5,
        min_confidence: float = 0.5,
        name: str = "counterfactual_reasoner"
    ):
        """
        Initialize counterfactual reasoning node.
        
        Args:
            llm: Language model for reasoning
            num_scenarios: Number of scenarios to generate
            min_confidence: Minimum confidence threshold
            name: Node name
        """
        super().__init__(name=name, description="Counterfactual what-if analysis")
        self.llm = llm
        self.num_scenarios = num_scenarios
        self.min_confidence = min_confidence
        self.system_prompt = self._build_system_prompt()
        
        self._logger.info(f"CounterfactualReasoningNode '{name}' initialized")
    
    def _build_system_prompt(self) -> str:
        """Build the system prompt for counterfactual reasoning."""
        return """You are an expert in counterfactual reasoning and what-if analysis.

Your responsibilities:
1. Generate alternative scenarios for decisions and actions
2. Predict outcomes of different choices
3. Compare actual vs counterfactual outcomes
4. Identify which alternatives would have been better/worse
5. Provide insights for improving future decisions

Counterfactual Types:
- action_change: Different action taken
- resource_change: Different resource allocation
- timing_change: Different timing of actions
- ordering_change: Different sequence of steps
- tool_change: Different tools or methods used
- team_change: Different team assignment
- condition_change: Different initial conditions
- prevention: Preventing something from happening
- addition: Adding something that wasn't done

Output Format (JSON):
{
    "actual_situation": "description of what actually happened",
    "actual_outcome": "actual result achieved",
    "scenarios": [
        {
            "scenario_id": "cf_1",
            "type": "counterfactual_type",
            "description": "what if scenario description",
            "changes": ["specific changes from actual"],
            "predicted_outcome": "expected result",
            "comparison": "much_better|better|similar|worse|much_worse",
            "probability": 0.75,
            "confidence": 0.85,
            "explanation": "why this outcome would occur",
            "advantages": ["benefits of this approach"],
            "disadvantages": ["drawbacks of this approach"],
            "risks": ["potential risks"]
        }
    ],
    "best_alternative": "description of best alternative found",
    "worst_alternative": "description of worst alternative",
    "insights": ["key learnings from analysis"],
    "recommendations": ["actionable recommendations"]
}

Analysis Principles:
- Be realistic about alternative outcomes
- Consider both intended and unintended consequences
- Account for constraints and limitations
- Distinguish correlation from causation
- Consider probability and confidence separately
- Identify transferable lessons
"""
    
    def execute(self, state: Dict[str, Any]) -> Command:
        """
        Execute counterfactual reasoning analysis.
        
        Args:
            state: Current workflow state
            
        Returns:
            Command with counterfactual analysis and routing decision
        """
        self._logger.info("Performing counterfactual reasoning analysis")
        
        # Get context for analysis
        context = self._prepare_context(state)
        
        # Perform counterfactual analysis
        analysis = self._analyze_counterfactuals(context, state)
        
        if not analysis:
            self._logger.warning("Counterfactual analysis produced no results")
            return Command(goto=state.get("next_node", END))
        
        self._logger.info(
            f"Counterfactual analysis completed: {len(analysis.scenarios)} scenarios, "
            f"{len(analysis.get_better_scenarios())} better alternatives found"
        )
        
        # Return Command with update
        return Command(
            update={
                "counterfactual_analysis": analysis,
                "messages": [
                    HumanMessage(
                        content=f"Counterfactual analysis explored {len(analysis.scenarios)} alternative scenarios",
                        name=self.name
                    )
                ],
                "context": {
                    **state.get("context", {}),
                    "counterfactual_scenarios_count": len(analysis.scenarios),
                    "better_alternatives_count": len(analysis.get_better_scenarios())
                }
            },
            goto=state.get("next_node", "supervisor")
        )
    
    def _prepare_context(self, state: Dict[str, Any]) -> str:
        """Prepare context for counterfactual analysis."""
        context_parts = []
        
        # Add plan
        plan = state.get("execution_plan")
        if plan:
            context_parts.append(f"Execution Plan:\n{json.dumps(plan, indent=2)}")
        
        # Add execution results
        feedback = state.get("execution_feedback", {})
        if feedback:
            context_parts.append(f"\nExecution Results:\n{json.dumps(feedback, indent=2)}")
        
        # Add decisions made
        decisions = state.get("decisions", [])
        if decisions:
            context_parts.append(f"\nDecisions Made:\n{json.dumps(decisions, indent=2)}")
        
        # Add any issues or failures
        issues = state.get("issues", [])
        if issues:
            context_parts.append(f"\nIssues Encountered:\n{json.dumps(issues, indent=2)}")
        
        return "\n\n".join(context_parts)
    
    def _analyze_counterfactuals(
        self,
        context: str,
        state: Dict[str, Any]
    ) -> Optional[CounterfactualAnalysis]:
        """Perform counterfactual analysis."""
        try:
            # Build analysis prompt
            prompt = f"""Analyze the following situation and generate {self.num_scenarios} counterfactual scenarios:

{context}

Generate diverse what-if scenarios exploring:
1. What if different actions were taken?
2. What if resources were allocated differently?
3. What if timing or sequencing changed?
4. What if different tools or teams were used?
5. What if certain events were prevented or added?

For each scenario, predict the likely outcome and compare to actual results.
Focus on scenarios that provide actionable insights.
"""
            
            # Get analysis from LLM
            messages = [
                SystemMessage(content=self.system_prompt),
                HumanMessage(content=prompt)
            ]
            
            response = self.llm.invoke(messages)
            cleaned = self._clean_json_response(response.content)
            analysis_data = json.loads(cleaned)
            
            # Build analysis object
            analysis = self._parse_analysis(analysis_data)
            
            return analysis
            
        except Exception as e:
            self._logger.error(f"Error in counterfactual analysis: {e}")
            return None
    
    def _parse_analysis(self, data: Dict[str, Any]) -> CounterfactualAnalysis:
        """Parse analysis data into CounterfactualAnalysis object."""
        scenarios = []
        
        for scenario_data in data.get("scenarios", []):
            try:
                cf_type = CounterfactualType(scenario_data.get("type", "action_change"))
            except ValueError:
                cf_type = CounterfactualType.ACTION_CHANGE
            
            try:
                comparison = OutcomeComparison(scenario_data.get("comparison", "similar"))
            except ValueError:
                comparison = OutcomeComparison.SIMILAR
            
            scenario = CounterfactualScenario(
                scenario_id=scenario_data.get("scenario_id", f"cf_{len(scenarios)}"),
                type=cf_type,
                description=scenario_data.get("description", ""),
                changes=scenario_data.get("changes", []),
                predicted_outcome=scenario_data.get("predicted_outcome", ""),
                comparison=comparison,
                probability=scenario_data.get("probability", 0.5),
                confidence=scenario_data.get("confidence", 0.5),
                explanation=scenario_data.get("explanation", ""),
                advantages=scenario_data.get("advantages", []),
                disadvantages=scenario_data.get("disadvantages", []),
                risks=scenario_data.get("risks", [])
            )
            
            # Filter by confidence
            if scenario.confidence >= self.min_confidence:
                scenarios.append(scenario)
        
        analysis = CounterfactualAnalysis(
            actual_situation=data.get("actual_situation", ""),
            actual_outcome=data.get("actual_outcome", ""),
            scenarios=scenarios,
            best_alternative=data.get("best_alternative"),
            worst_alternative=data.get("worst_alternative"),
            insights=data.get("insights", []),
            recommendations=data.get("recommendations", [])
        )
        
        return analysis
    
    def analyze_decision(
        self,
        decision: str,
        context: Dict[str, Any],
        outcome: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Analyze a specific decision with counterfactual reasoning.
        
        Args:
            decision: The decision made
            context: Context information
            outcome: Actual outcome if available
            
        Returns:
            Counterfactual analysis results
        """
        try:
            prompt = f"""Analyze the following decision using counterfactual reasoning:

Decision: {decision}
Actual Outcome: {outcome or 'Not yet known'}

Context:
{json.dumps(context, indent=2)}

Generate alternative decisions and predict their outcomes.
Compare with the actual decision to identify if better options existed.
"""
            
            messages = [
                SystemMessage(content=self.system_prompt),
                HumanMessage(content=prompt)
            ]
            
            response = self.llm.invoke(messages)
            cleaned = self._clean_json_response(response.content)
            analysis = json.loads(cleaned)
            
            return analysis
            
        except Exception as e:
            self._logger.error(f"Error analyzing decision: {e}")
            return {"error": str(e)}
    
    def suggest_improvements(
        self,
        plan: Dict[str, Any],
        execution_feedback: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Suggest improvements based on counterfactual analysis.
        
        Args:
            plan: The original plan
            execution_feedback: Results of execution
            
        Returns:
            List of suggested improvements
        """
        try:
            prompt = f"""Based on counterfactual analysis, suggest improvements for this plan:

Original Plan:
{json.dumps(plan, indent=2)}

Execution Feedback:
{json.dumps(execution_feedback, indent=2)}

Generate specific, actionable improvements that would likely lead to better outcomes.
For each improvement, explain:
1. What to change
2. Why it would be better
3. What outcome to expect
4. What risks to consider
"""
            
            messages = [
                SystemMessage(content=self.system_prompt),
                HumanMessage(content=prompt)
            ]
            
            response = self.llm.invoke(messages)
            cleaned = self._clean_json_response(response.content)
            improvements = json.loads(cleaned)
            
            return improvements.get("scenarios", [])
            
        except Exception as e:
            self._logger.error(f"Error suggesting improvements: {e}")
            return []
    
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


def create_counterfactual_reasoner(
    llm: BaseChatModel,
    num_scenarios: int = 5,
    min_confidence: float = 0.5,
    name: str = "counterfactual_reasoner"
) -> CounterfactualReasoningNode:
    """
    Factory function to create a counterfactual reasoning node.
    
    Args:
        llm: Language model
        num_scenarios: Number of scenarios to generate
        min_confidence: Minimum confidence threshold
        name: Node name
        
    Returns:
        CounterfactualReasoningNode instance
    """
    return CounterfactualReasoningNode(
        llm=llm,
        num_scenarios=num_scenarios,
        min_confidence=min_confidence,
        name=name
    )
