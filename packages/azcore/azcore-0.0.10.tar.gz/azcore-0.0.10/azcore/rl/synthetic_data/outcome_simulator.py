"""
Outcome simulator for synthetic RL training data.

This module simulates agent execution outcomes without running real agents.
"""

import random
import logging
from typing import List, Dict, Any, Tuple
from azcore.rl.synthetic_data.scenario_generator import Scenario
from azcore.exceptions import ValidationError

logger = logging.getLogger(__name__)


class OutcomeSimulator:
    """
    Simulates agent execution outcomes.
    
    Example:
        >>> simulator = OutcomeSimulator(tool_names=["search", "calculator"])
        >>> outcome, reward = simulator.simulate(scenario, selected_tools)
    """
    
    def __init__(
        self,
        tool_names: List[str],
        base_error_rate: float = 0.1,
        noise_level: float = 0.05
    ):
        """
        Initialize the outcome simulator.
        
        Args:
            tool_names: List of available tool names
            base_error_rate: Base probability of errors
            noise_level: Amount of noise in rewards
        """
        self.tool_names = tool_names
        self.base_error_rate = base_error_rate
        self.noise_level = noise_level
        
        # Define tool success probabilities
        self.tool_success_rates = {tool: 0.85 for tool in tool_names}
        
        logger.info("OutcomeSimulator initialized")
    
    def simulate(
        self,
        scenario: Scenario,
        selected_tools: List[str]
    ) -> Tuple[Dict[str, Any], float]:
        """
        Simulate execution outcome.
        
        Args:
            scenario: The scenario being executed
            selected_tools: Tools selected by the agent
            
        Returns:
            Tuple of (outcome_dict, reward)
        """
        # Check if optimal tools were selected
        optimal_tools = set(scenario.optimal_tools)
        selected_tools_set = set(selected_tools)
        
        # Calculate tool match score
        if not optimal_tools:
            tool_match_score = 0.5
        else:
            intersection = optimal_tools & selected_tools_set
            union = optimal_tools | selected_tools_set
            tool_match_score = len(intersection) / len(union) if union else 0.0
        
        # Simulate success/failure
        success_prob = scenario.expected_success_rate * tool_match_score
        success_prob = max(0.1, min(0.95, success_prob))  # Clamp
        
        is_success = random.random() < success_prob
        
        # Generate outcome
        if is_success:
            outcome = self._generate_success_outcome(scenario, selected_tools)
            base_reward = 0.7 + (tool_match_score * 0.3)  # 0.7 to 1.0
        else:
            outcome = self._generate_failure_outcome(scenario, selected_tools)
            base_reward = -0.5 - (0.5 * (1 - tool_match_score))  # -1.0 to -0.5
        
        # Add noise to reward
        reward = base_reward + random.uniform(-self.noise_level, self.noise_level)
        reward = max(-1.0, min(1.0, reward))  # Clamp to [-1, 1]
        
        return outcome, reward
    
    def _generate_success_outcome(
        self,
        scenario: Scenario,
        selected_tools: List[str]
    ) -> Dict[str, Any]:
        """Generate a successful outcome."""
        return {
            'status': 'success',
            'result': f"Successfully completed: {scenario.description}",
            'tools_used': selected_tools,
            'execution_time': random.uniform(0.5, 3.0),
            'domain': scenario.domain.value,
            'complexity': scenario.complexity.value
        }
    
    def _generate_failure_outcome(
        self,
        scenario: Scenario,
        selected_tools: List[str]
    ) -> Dict[str, Any]:
        """Generate a failure outcome."""
        error_messages = [
            "Tool execution failed",
            "Unable to complete task",
            "Insufficient information",
            "Tool not applicable to task",
            "Timeout occurred",
            "Invalid tool selection"
        ]
        
        return {
            'status': 'failure',
            'error': random.choice(error_messages),
            'tools_used': selected_tools,
            'execution_time': random.uniform(0.2, 1.5),
            'domain': scenario.domain.value,
            'complexity': scenario.complexity.value
        }
    
    def simulate_batch(
        self,
        scenarios: List[Scenario],
        selected_tools_list: List[List[str]]
    ) -> List[Tuple[Dict[str, Any], float]]:
        """
        Simulate outcomes for multiple scenarios.
        
        Args:
            scenarios: List of scenarios
            selected_tools_list: List of tool selections for each scenario
            
        Returns:
            List of (outcome, reward) tuples
        """
        if len(scenarios) != len(selected_tools_list):
            logger.error(
                f"Scenario count mismatch: {len(scenarios)} scenarios vs "
                f"{len(selected_tools_list)} tool selections"
            )
            raise ValidationError(
                "Number of scenarios must match number of tool selections",
                details={
                    "scenarios_count": len(scenarios),
                    "tool_selections_count": len(selected_tools_list)
                }
            )
        
        results = []
        for scenario, selected_tools in zip(scenarios, selected_tools_list):
            outcome, reward = self.simulate(scenario, selected_tools)
            results.append((outcome, reward))
        
        logger.info(f"Simulated {len(results)} outcomes")
        return results
