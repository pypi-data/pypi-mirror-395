"""
Causal Reasoning Module for Understanding Cause-Effect Relationships.

This module provides causal reasoning capabilities including:
- Causal chain analysis
- Cause-effect relationship identification
- Impact assessment and propagation
- Root cause analysis
"""

from typing import Dict, Any, List, Optional, Set, Tuple
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


class CausalRelationType(Enum):
    """Types of causal relationships."""
    DIRECT_CAUSE = "direct_cause"  # A directly causes B
    INDIRECT_CAUSE = "indirect_cause"  # A causes B through intermediary
    CONTRIBUTING_FACTOR = "contributing_factor"  # A contributes to B
    NECESSARY_CONDITION = "necessary_condition"  # A is necessary for B
    SUFFICIENT_CONDITION = "sufficient_condition"  # A is sufficient for B
    PREVENTIVE = "preventive"  # A prevents B
    ENABLING = "enabling"  # A enables B to occur


class CausalStrength(Enum):
    """Strength of causal relationship."""
    WEAK = "weak"  # 0.0 - 0.3
    MODERATE = "moderate"  # 0.3 - 0.7
    STRONG = "strong"  # 0.7 - 0.9
    CERTAIN = "certain"  # 0.9 - 1.0


@dataclass
class CausalRelation:
    """Represents a causal relationship between two events/actions."""
    cause: str
    effect: str
    relation_type: CausalRelationType
    strength: float  # 0.0 to 1.0
    confidence: float  # 0.0 to 1.0
    explanation: str
    intermediate_factors: List[str] = field(default_factory=list)
    conditions: List[str] = field(default_factory=list)
    time_delay: Optional[str] = None
    
    def get_strength_category(self) -> CausalStrength:
        """Get categorical strength."""
        if self.strength < 0.3:
            return CausalStrength.WEAK
        elif self.strength < 0.7:
            return CausalStrength.MODERATE
        elif self.strength < 0.9:
            return CausalStrength.STRONG
        else:
            return CausalStrength.CERTAIN
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "cause": self.cause,
            "effect": self.effect,
            "relation_type": self.relation_type.value,
            "strength": self.strength,
            "strength_category": self.get_strength_category().value,
            "confidence": self.confidence,
            "explanation": self.explanation,
            "intermediate_factors": self.intermediate_factors,
            "conditions": self.conditions,
            "time_delay": self.time_delay
        }


@dataclass
class CausalChain:
    """Represents a chain of causal relationships."""
    chain_id: str
    events: List[str]
    relations: List[CausalRelation]
    overall_strength: float
    description: str
    
    def get_length(self) -> int:
        """Get length of causal chain."""
        return len(self.events)
    
    def get_root_cause(self) -> str:
        """Get the root cause (first event)."""
        return self.events[0] if self.events else ""
    
    def get_final_effect(self) -> str:
        """Get the final effect (last event)."""
        return self.events[-1] if self.events else ""
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "chain_id": self.chain_id,
            "events": self.events,
            "relations": [r.to_dict() for r in self.relations],
            "overall_strength": self.overall_strength,
            "description": self.description,
            "length": self.get_length(),
            "root_cause": self.get_root_cause(),
            "final_effect": self.get_final_effect()
        }


@dataclass
class CausalGraph:
    """Represents a complete causal graph."""
    nodes: List[str]  # Events/actions
    relations: List[CausalRelation]
    chains: List[CausalChain]
    root_causes: List[str]
    final_effects: List[str]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "nodes": self.nodes,
            "relations": [r.to_dict() for r in self.relations],
            "chains": [c.to_dict() for c in self.chains],
            "root_causes": self.root_causes,
            "final_effects": self.final_effects,
            "num_nodes": len(self.nodes),
            "num_relations": len(self.relations),
            "num_chains": len(self.chains)
        }


class CausalReasoningNode(BaseNode):
    """
    Causal reasoning node for understanding cause-effect relationships.
    
    Features:
    - Identifies causal relationships in plans and executions
    - Builds causal chains and graphs
    - Performs root cause analysis
    - Assesses impact propagation
    - Predicts downstream effects of actions
    """
    
    def __init__(
        self,
        llm: BaseChatModel,
        min_confidence: float = 0.5,
        max_chain_length: int = 10,
        name: str = "causal_reasoner"
    ):
        """
        Initialize causal reasoning node.
        
        Args:
            llm: Language model for reasoning
            min_confidence: Minimum confidence threshold
            max_chain_length: Maximum causal chain length
            name: Node name
        """
        super().__init__(name=name, description="Causal reasoning and analysis")
        self.llm = llm
        self.min_confidence = min_confidence
        self.max_chain_length = max_chain_length
        self.system_prompt = self._build_system_prompt()
        
        self._logger.info(f"CausalReasoningNode '{name}' initialized")
    
    def _build_system_prompt(self) -> str:
        """Build the system prompt for causal reasoning."""
        return """You are an expert in causal reasoning and analysis.

Your responsibilities:
1. Identify cause-effect relationships in scenarios
2. Determine the type and strength of causal relationships
3. Build causal chains showing how effects propagate
4. Perform root cause analysis for failures or issues
5. Predict downstream effects of actions

Causal Relationship Types:
- direct_cause: A directly causes B
- indirect_cause: A causes B through intermediaries
- contributing_factor: A contributes to but doesn't fully cause B
- necessary_condition: B cannot occur without A
- sufficient_condition: A alone is enough to cause B
- preventive: A prevents B from occurring
- enabling: A enables B to occur (but doesn't cause it)

Output Format (JSON):
{
    "analysis": "Overall causal analysis",
    "relations": [
        {
            "cause": "event or action",
            "effect": "resulting event or outcome",
            "relation_type": "type of relationship",
            "strength": 0.85,
            "confidence": 0.9,
            "explanation": "why this causal relationship exists",
            "intermediate_factors": ["factors between cause and effect"],
            "conditions": ["conditions required for causation"],
            "time_delay": "immediate|short|medium|long"
        }
    ],
    "causal_chains": [
        {
            "chain_id": "chain_1",
            "events": ["event1", "event2", "event3"],
            "description": "description of causal chain",
            "overall_strength": 0.75
        }
    ],
    "root_causes": ["fundamental causes"],
    "final_effects": ["ultimate outcomes"],
    "insights": ["key insights from causal analysis"]
}

Analysis Principles:
- Distinguish correlation from causation
- Consider confounding factors
- Identify necessary vs sufficient conditions
- Account for time delays between cause and effect
- Recognize feedback loops and cycles
- Consider alternative explanations
"""
    
    def execute(self, state: Dict[str, Any]) -> Command:
        """
        Execute causal reasoning analysis.
        
        Args:
            state: Current workflow state
            
        Returns:
            Command with causal analysis and routing decision
        """
        self._logger.info("Performing causal reasoning analysis")
        
        # Get context for analysis
        analysis_context = self._prepare_context(state)
        
        # Perform causal analysis
        causal_graph = self._analyze_causality(analysis_context, state)
        
        if not causal_graph:
            self._logger.warning("Causal analysis produced no results")
            return Command(goto=state.get("next_node", END))
        
        self._logger.info(
            f"Causal analysis completed: {len(causal_graph.nodes)} nodes, "
            f"{len(causal_graph.relations)} relations, {len(causal_graph.chains)} chains"
        )
        
        # Return Command with update
        return Command(
            update={
                "causal_analysis": causal_graph,
                "messages": [
                    HumanMessage(
                        content=f"Causal analysis identified {len(causal_graph.nodes)} causal factors",
                        name=self.name
                    )
                ],
                "context": {
                    **state.get("context", {}),
                    "causal_nodes_count": len(causal_graph.nodes),
                    "causal_relations_count": len(causal_graph.relations)
                }
            },
            goto=state.get("next_node", "supervisor")
        )
    
    def _prepare_context(self, state: Dict[str, Any]) -> str:
        """Prepare context for causal analysis."""
        context_parts = []
        
        # Add plan if available
        plan = state.get("execution_plan")
        if plan:
            context_parts.append(f"Execution Plan:\n{json.dumps(plan, indent=2)}")
        
        # Add execution feedback
        feedback = state.get("execution_feedback", {})
        if feedback:
            context_parts.append(f"\nExecution Feedback:\n{json.dumps(feedback, indent=2)}")
        
        # Add messages
        messages = state.get("messages", [])
        if messages:
            recent_messages = messages[-5:]  # Last 5 messages
            msg_text = "\n".join([
                f"{msg.name if hasattr(msg, 'name') else 'unknown'}: {msg.content}"
                for msg in recent_messages
            ])
            context_parts.append(f"\nRecent Messages:\n{msg_text}")
        
        # Add any failures or issues
        failures = state.get("failures", [])
        if failures:
            context_parts.append(f"\nFailures:\n{json.dumps(failures, indent=2)}")
        
        return "\n\n".join(context_parts)
    
    def _analyze_causality(
        self,
        context: str,
        state: Dict[str, Any]
    ) -> Optional[CausalGraph]:
        """Perform causal analysis."""
        try:
            # Build analysis prompt
            prompt = f"""Analyze the following scenario to identify causal relationships:

{context}

Please provide a comprehensive causal analysis including:
1. All significant cause-effect relationships
2. Causal chains showing how effects propagate
3. Root causes of any issues or outcomes
4. Final effects and their causes

Focus on actionable insights that can improve planning and execution.
"""
            
            # Get analysis from LLM
            messages = [
                SystemMessage(content=self.system_prompt),
                HumanMessage(content=prompt)
            ]
            
            response = self.llm.invoke(messages)
            cleaned = self._clean_json_response(response.content)
            analysis_data = json.loads(cleaned)
            
            # Build causal graph
            causal_graph = self._build_causal_graph(analysis_data)
            
            return causal_graph
            
        except Exception as e:
            self._logger.error(f"Error in causal analysis: {e}")
            return None
    
    def _build_causal_graph(self, data: Dict[str, Any]) -> CausalGraph:
        """Build causal graph from analysis data."""
        # Parse relations
        relations = []
        for rel_data in data.get("relations", []):
            try:
                relation_type = CausalRelationType(rel_data.get("relation_type", "direct_cause"))
            except ValueError:
                relation_type = CausalRelationType.DIRECT_CAUSE
            
            relation = CausalRelation(
                cause=rel_data.get("cause", ""),
                effect=rel_data.get("effect", ""),
                relation_type=relation_type,
                strength=rel_data.get("strength", 0.5),
                confidence=rel_data.get("confidence", 0.5),
                explanation=rel_data.get("explanation", ""),
                intermediate_factors=rel_data.get("intermediate_factors", []),
                conditions=rel_data.get("conditions", []),
                time_delay=rel_data.get("time_delay")
            )
            
            # Filter by confidence
            if relation.confidence >= self.min_confidence:
                relations.append(relation)
        
        # Extract nodes
        nodes = set()
        for rel in relations:
            nodes.add(rel.cause)
            nodes.add(rel.effect)
        
        # Parse causal chains
        chains = []
        for chain_data in data.get("causal_chains", []):
            chain_relations = [
                r for r in relations
                if r.cause in chain_data.get("events", [])
                and r.effect in chain_data.get("events", [])
            ]
            
            chain = CausalChain(
                chain_id=chain_data.get("chain_id", f"chain_{len(chains)}"),
                events=chain_data.get("events", []),
                relations=chain_relations,
                overall_strength=chain_data.get("overall_strength", 0.5),
                description=chain_data.get("description", "")
            )
            chains.append(chain)
        
        # Create graph
        graph = CausalGraph(
            nodes=list(nodes),
            relations=relations,
            chains=chains,
            root_causes=data.get("root_causes", []),
            final_effects=data.get("final_effects", [])
        )
        
        return graph
    
    def analyze_root_cause(
        self,
        issue: str,
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Perform root cause analysis for a specific issue.
        
        Args:
            issue: Description of the issue
            context: Context information
            
        Returns:
            Root cause analysis results
        """
        try:
            prompt = f"""Perform root cause analysis for the following issue:

Issue: {issue}

Context:
{json.dumps(context, indent=2)}

Identify:
1. The root cause(s) of this issue
2. Contributing factors
3. Causal chain leading to the issue
4. How to prevent similar issues

Provide detailed analysis with causal relationships.
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
            self._logger.error(f"Error in root cause analysis: {e}")
            return {"error": str(e)}
    
    def predict_effects(
        self,
        action: str,
        context: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Predict downstream effects of an action.
        
        Args:
            action: Action to analyze
            context: Context information
            
        Returns:
            List of predicted effects
        """
        try:
            prompt = f"""Predict the downstream effects of the following action:

Action: {action}

Context:
{json.dumps(context, indent=2)}

Identify:
1. Direct effects
2. Indirect effects
3. Potential unintended consequences
4. Timeline of effects

Provide detailed causal analysis.
"""
            
            messages = [
                SystemMessage(content=self.system_prompt),
                HumanMessage(content=prompt)
            ]
            
            response = self.llm.invoke(messages)
            cleaned = self._clean_json_response(response.content)
            effects = json.loads(cleaned)
            
            return effects.get("relations", [])
            
        except Exception as e:
            self._logger.error(f"Error predicting effects: {e}")
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


def create_causal_reasoner(
    llm: BaseChatModel,
    min_confidence: float = 0.5,
    max_chain_length: int = 10,
    name: str = "causal_reasoner"
) -> CausalReasoningNode:
    """
    Factory function to create a causal reasoning node.
    
    Args:
        llm: Language model
        min_confidence: Minimum confidence threshold
        max_chain_length: Maximum causal chain length
        name: Node name
        
    Returns:
        CausalReasoningNode instance
    """
    return CausalReasoningNode(
        llm=llm,
        min_confidence=min_confidence,
        max_chain_length=max_chain_length,
        name=name
    )
