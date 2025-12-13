"""
Data validator for synthetic RL training data.

This module ensures synthetic data quality.
"""

import logging
from typing import List, Dict, Any, Tuple
from azcore.rl.synthetic_data.scenario_generator import Scenario

logger = logging.getLogger(__name__)


class DataValidator:
    """
    Validates synthetic training data quality.
    
    Example:
        >>> validator = DataValidator()
        >>> is_valid, score = validator.validate_scenario(scenario)
    """
    
    def __init__(
        self,
        min_quality_score: float = 0.6,
        check_duplicates: bool = True
    ):
        """
        Initialize the data validator.
        
        Args:
            min_quality_score: Minimum quality score to accept
            check_duplicates: Whether to check for duplicates
        """
        self.min_quality_score = min_quality_score
        self.check_duplicates = check_duplicates
        self._seen_descriptions = set()
        
        logger.info("DataValidator initialized")
    
    def validate_scenario(self, scenario: Scenario) -> Tuple[bool, float]:
        """
        Validate a single scenario.
        
        Args:
            scenario: Scenario to validate
            
        Returns:
            Tuple of (is_valid, quality_score)
        """
        quality_score = 1.0
        
        # Check if description is not empty
        if not scenario.description or len(scenario.description) < 5:
            logger.debug(f"Invalid scenario: empty or too short description")
            return False, 0.0
        
        # Check if optimal tools are specified
        if not scenario.optimal_tools:
            quality_score -= 0.2
            logger.debug(f"Scenario has no optimal tools: {scenario.description[:50]}")
        
        # Check expected success rate is reasonable
        if not (0.0 <= scenario.expected_success_rate <= 1.0):
            logger.debug(f"Invalid success rate: {scenario.expected_success_rate}")
            return False, 0.0
        
        # Check for duplicates
        if self.check_duplicates:
            if scenario.description in self._seen_descriptions:
                logger.debug(f"Duplicate scenario detected: {scenario.description[:50]}")
                return False, 0.0
            self._seen_descriptions.add(scenario.description)
        
        # Quality checks passed
        is_valid = quality_score >= self.min_quality_score
        return is_valid, quality_score
    
    def validate_batch(
        self,
        scenarios: List[Scenario]
    ) -> Tuple[List[Scenario], Dict[str, Any]]:
        """
        Validate a batch of scenarios.
        
        Args:
            scenarios: List of scenarios to validate
            
        Returns:
            Tuple of (valid_scenarios, validation_stats)
        """
        valid_scenarios = []
        quality_scores = []
        
        for scenario in scenarios:
            is_valid, score = self.validate_scenario(scenario)
            if is_valid:
                valid_scenarios.append(scenario)
                quality_scores.append(score)
        
        stats = {
            'total': len(scenarios),
            'valid': len(valid_scenarios),
            'invalid': len(scenarios) - len(valid_scenarios),
            'pass_rate': len(valid_scenarios) / len(scenarios) if scenarios else 0.0,
            'avg_quality_score': sum(quality_scores) / len(quality_scores) if quality_scores else 0.0
        }
        
        logger.info(
            f"Validated {stats['total']} scenarios: "
            f"{stats['valid']} valid, {stats['invalid']} invalid "
            f"(pass rate: {stats['pass_rate']:.2%})"
        )
        
        return valid_scenarios, stats
    
    def reset(self):
        """Reset validation state (clears seen descriptions)."""
        self._seen_descriptions.clear()
        logger.debug("DataValidator state reset")
