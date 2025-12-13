"""
Heavy Swarm for Azcore.

Five-phase comprehensive workflow with specialized agents for research,
analysis, alternatives, verification, and synthesis.

Use Cases:
- Complex research and analysis tasks
- Financial analysis and modeling
- Strategic planning
- Comprehensive reporting
- Multi-stage decision making
"""

import logging
from typing import List, Dict, Any, Optional, Callable, Union
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage
from azcore.core.base import BaseAgent
from azcore.exceptions import ValidationError

logger = logging.getLogger(__name__)


class HeavySwarm:
    """
    Five-phase comprehensive analysis workflow.
    
    Implements a structured five-phase approach:
    1. Research: Gather information and context
    2. Analysis: Deep analysis of findings
    3. Alternatives: Generate and evaluate options
    4. Verification: Validate and cross-check
    5. Synthesis: Final comprehensive report
    
    Attributes:
        name (str): Swarm identifier
        research_agent: Research phase agent
        analysis_agent: Analysis phase agent
        alternatives_agent: Alternatives generation agent
        verification_agent: Verification phase agent
        synthesis_agent: Final synthesis agent
    
    Example:
        >>> from azcore.workflows import HeavySwarm
        >>> 
        >>> # Create specialized agents for each phase
        >>> researcher = ReactAgent(name="Researcher", llm=llm, tools=research_tools,
        ...     prompt="You are a research specialist. Gather comprehensive information.")
        >>> 
        >>> analyst = ReactAgent(name="Analyst", llm=llm, tools=analysis_tools,
        ...     prompt="You are a data analyst. Perform deep analysis.")
        >>> 
        >>> strategist = ReactAgent(name="Strategist", llm=llm, tools=strategy_tools,
        ...     prompt="You are a strategist. Generate and evaluate alternatives.")
        >>> 
        >>> verifier = ReactAgent(name="Verifier", llm=llm, tools=verification_tools,
        ...     prompt="You are a fact-checker. Verify accuracy and validity.")
        >>> 
        >>> synthesizer = ReactAgent(name="Synthesizer", llm=llm,
        ...     prompt="You are a report writer. Create comprehensive synthesis.")
        >>> 
        >>> # Create heavy swarm
        >>> heavy_swarm = HeavySwarm(
        ...     name="ComprehensiveAnalysis",
        ...     research_agent=researcher,
        ...     analysis_agent=analyst,
        ...     alternatives_agent=strategist,
        ...     verification_agent=verifier,
        ...     synthesis_agent=synthesizer
        ... )
        >>> 
        >>> # Execute comprehensive analysis
        >>> result = heavy_swarm.run("Evaluate AI investment opportunities")
        >>> print(result['comprehensive_report'])
    """
    
    def __init__(
        self,
        name: str,
        research_agent: Union[BaseAgent, Callable],
        analysis_agent: Union[BaseAgent, Callable],
        alternatives_agent: Union[BaseAgent, Callable],
        verification_agent: Union[BaseAgent, Callable],
        synthesis_agent: Union[BaseAgent, Callable],
        enable_cross_validation: bool = True,
        description: str = ""
    ):
        """
        Initialize HeavySwarm.
        
        Args:
            name: Swarm identifier
            research_agent: Research phase agent
            analysis_agent: Analysis phase agent
            alternatives_agent: Alternatives generation agent
            verification_agent: Verification phase agent
            synthesis_agent: Final synthesis agent
            enable_cross_validation: Enable cross-validation between phases
            description: Swarm description
            
        Raises:
            ValidationError: If configuration is invalid
        """
        self.name = name
        self.research_agent = research_agent
        self.analysis_agent = analysis_agent
        self.alternatives_agent = alternatives_agent
        self.verification_agent = verification_agent
        self.synthesis_agent = synthesis_agent
        self.enable_cross_validation = enable_cross_validation
        self.description = description or f"Heavy Swarm: {name}"
        
        self._phase_outputs: Dict[str, Any] = {}
        
        self._logger = logging.getLogger(f"{self.__class__.__name__}.{name}")
        
        # Validation
        self._validate()
        
        self._logger.info(f"HeavySwarm '{name}' initialized with 5-phase workflow")
    
    def _validate(self):
        """Validate swarm configuration."""
        required_agents = [
            ("research_agent", self.research_agent),
            ("analysis_agent", self.analysis_agent),
            ("alternatives_agent", self.alternatives_agent),
            ("verification_agent", self.verification_agent),
            ("synthesis_agent", self.synthesis_agent)
        ]
        
        for agent_name, agent in required_agents:
            if not agent:
                raise ValidationError(f"HeavySwarm requires {agent_name}")
            
            if not (isinstance(agent, BaseAgent) or callable(agent)):
                raise ValidationError(f"{agent_name} must be BaseAgent or callable")
    
    def run(
        self,
        task: Union[str, Dict[str, Any]],
        config: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Execute five-phase comprehensive analysis.
        
        Args:
            task: Task or problem to analyze
            config: Optional configuration
            
        Returns:
            Dict containing:
                - comprehensive_report: Final synthesized report
                - research_findings: Phase 1 output
                - analysis_results: Phase 2 output
                - alternatives_evaluation: Phase 3 output
                - verification_results: Phase 4 output
                - phase_outputs: All phase outputs
                - metadata: Execution metadata
        """
        self._logger.info(f"Starting HeavySwarm '{self.name}' - 5-phase analysis")
        
        # Prepare initial task
        if isinstance(task, str):
            task_description = task
            initial_state = {"messages": [HumanMessage(content=task)]}
        else:
            task_description = self._extract_content(task.get('messages', [{}])[0])
            initial_state = task
        
        # Phase 1: Research
        self._logger.info("Phase 1/5: Research - Gathering information...")
        research_output = self._execute_phase(
            phase_name="research",
            agent=self.research_agent,
            task=task_description,
            context=initial_state,
            prompt_prefix="Conduct comprehensive research on the following:"
        )
        
        # Phase 2: Analysis
        self._logger.info("Phase 2/5: Analysis - Deep analysis...")
        analysis_output = self._execute_phase(
            phase_name="analysis",
            agent=self.analysis_agent,
            task=task_description,
            context=research_output,
            prompt_prefix="Based on the research findings, perform deep analysis:"
        )
        
        # Phase 3: Alternatives
        self._logger.info("Phase 3/5: Alternatives - Generating options...")
        alternatives_output = self._execute_phase(
            phase_name="alternatives",
            agent=self.alternatives_agent,
            task=task_description,
            context=analysis_output,
            prompt_prefix="Based on the analysis, generate and evaluate alternatives:"
        )
        
        # Phase 4: Verification
        self._logger.info("Phase 4/5: Verification - Validating findings...")
        verification_output = self._execute_phase(
            phase_name="verification",
            agent=self.verification_agent,
            task=task_description,
            context=self._combine_contexts([
                research_output,
                analysis_output,
                alternatives_output
            ]),
            prompt_prefix="Verify and validate the following findings:"
        )
        
        # Phase 5: Synthesis
        self._logger.info("Phase 5/5: Synthesis - Creating comprehensive report...")
        synthesis_output = self._execute_phase(
            phase_name="synthesis",
            agent=self.synthesis_agent,
            task=task_description,
            context=self._combine_contexts([
                research_output,
                analysis_output,
                alternatives_output,
                verification_output
            ]),
            prompt_prefix="Synthesize all findings into a comprehensive report:"
        )
        
        # Prepare final result
        result = {
            "comprehensive_report": synthesis_output.get('output', ''),
            "research_findings": research_output.get('output', ''),
            "analysis_results": analysis_output.get('output', ''),
            "alternatives_evaluation": alternatives_output.get('output', ''),
            "verification_results": verification_output.get('output', ''),
            "phase_outputs": {
                "phase_1_research": research_output,
                "phase_2_analysis": analysis_output,
                "phase_3_alternatives": alternatives_output,
                "phase_4_verification": verification_output,
                "phase_5_synthesis": synthesis_output
            },
            "metadata": {
                "workflow": self.name,
                "phases_completed": 5,
                "cross_validation": self.enable_cross_validation,
                "agents": {
                    "research": getattr(self.research_agent, 'name', 'Researcher'),
                    "analysis": getattr(self.analysis_agent, 'name', 'Analyst'),
                    "alternatives": getattr(self.alternatives_agent, 'name', 'Strategist'),
                    "verification": getattr(self.verification_agent, 'name', 'Verifier'),
                    "synthesis": getattr(self.synthesis_agent, 'name', 'Synthesizer')
                }
            }
        }
        
        self._logger.info(f"HeavySwarm '{self.name}' completed all 5 phases")
        
        return result
    
    def _execute_phase(
        self,
        phase_name: str,
        agent: Union[BaseAgent, Callable],
        task: str,
        context: Union[str, Dict[str, Any]],
        prompt_prefix: str
    ) -> Dict[str, Any]:
        """Execute a single phase."""
        agent_name = getattr(agent, 'name', phase_name.capitalize())
        
        # Prepare phase prompt
        if isinstance(context, dict) and 'output' in context:
            context_text = context['output']
        elif isinstance(context, str):
            context_text = context
        else:
            context_text = str(context)
        
        phase_prompt = f"""{prompt_prefix}

Original Task: {task}

Context from Previous Phases:
{context_text}

Provide your {phase_name} output:"""
        
        state = {"messages": [HumanMessage(content=phase_prompt)]}
        
        try:
            # Execute agent
            if hasattr(agent, 'invoke'):
                result = agent.invoke(state)
            else:
                result = agent(state)
            
            # Extract output
            if isinstance(result, dict) and 'messages' in result:
                output = self._extract_content(result['messages'][-1])
            else:
                output = str(result)
            
            phase_output = {
                "phase": phase_name,
                "agent": agent_name,
                "output": output,
                "status": "completed"
            }
            
            self._phase_outputs[phase_name] = phase_output
            self._logger.debug(f"Phase '{phase_name}' completed")
            
            return phase_output
            
        except Exception as e:
            self._logger.error(f"Phase '{phase_name}' failed: {e}")
            
            phase_output = {
                "phase": phase_name,
                "agent": agent_name,
                "output": f"ERROR: {e}",
                "status": "failed",
                "error": str(e)
            }
            
            self._phase_outputs[phase_name] = phase_output
            
            return phase_output
    
    def _combine_contexts(
        self,
        contexts: List[Union[str, Dict[str, Any]]]
    ) -> str:
        """Combine multiple contexts into single text."""
        combined_parts = []
        
        for i, context in enumerate(contexts, 1):
            if isinstance(context, dict) and 'output' in context:
                phase_name = context.get('phase', f'Phase_{i}')
                combined_parts.append(f"=== {phase_name.upper()} ===\n{context['output']}")
            elif isinstance(context, str):
                combined_parts.append(context)
            else:
                combined_parts.append(str(context))
        
        return "\n\n".join(combined_parts)
    
    def get_phase_summary(self) -> str:
        """
        Get a summary of all phases.
        
        Returns:
            Formatted summary of phase execution
        """
        lines = [
            f"Heavy Swarm: {self.name}",
            "=" * 60,
            ""
        ]
        
        phases = ["research", "analysis", "alternatives", "verification", "synthesis"]
        
        for phase in phases:
            output = self._phase_outputs.get(phase, {})
            status = output.get('status', 'not_executed')
            agent = output.get('agent', 'Unknown')
            
            lines.append(f"Phase: {phase.capitalize()}")
            lines.append(f"  Agent: {agent}")
            lines.append(f"  Status: {status}")
            
            if status == "completed":
                output_text = output.get('output', '')[:200]
                lines.append(f"  Output: {output_text}...")
            
            lines.append("")
        
        return "\n".join(lines)
    
    def _extract_content(self, message: Union[BaseMessage, Dict, str]) -> str:
        """Extract content from message."""
        if isinstance(message, str):
            return message
        if isinstance(message, dict):
            return message.get("content", str(message))
        return getattr(message, "content", str(message))
    
    def __repr__(self) -> str:
        """Return a string representation of the HeavySwarm instance.

        The string representation includes the name and number of phases.

        Returns:
            str: A string representation of the HeavySwarm instance."""
        return f"HeavySwarm(name='{self.name}', phases=5)"
