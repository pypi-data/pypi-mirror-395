"""
Training pipeline for synthetic RL data.

This module orchestrates end-to-end synthetic data generation and training.
"""

import logging
from typing import List, Dict, Any, Optional
from azcore.rl.synthetic_data.scenario_generator import ScenarioGenerator, Scenario
from azcore.rl.synthetic_data.query_generator import QueryGenerator
from azcore.rl.synthetic_data.outcome_simulator import OutcomeSimulator
from azcore.rl.synthetic_data.data_validator import DataValidator

logger = logging.getLogger(__name__)


class SyntheticDataPipeline:
    """
    Orchestrates synthetic data generation pipeline.
    
    Example:
        >>> pipeline = SyntheticDataPipeline(tool_names=["search", "calculator"])
        >>> training_data = pipeline.generate(num_samples=1000)
    """
    
    def __init__(
        self,
        tool_names: List[str],
        use_llm: bool = False,
        llm: Optional[Any] = None,
        min_quality_score: float = 0.6
    ):
        """
        Initialize the training pipeline.
        
        Args:
            tool_names: List of available tool names
            use_llm: Whether to use LLM for generation (auto-detected if llm is provided)
            llm: Optional LLM instance (if provided, use_llm is automatically set to True)
            min_quality_score: Minimum quality score for validation
        """
        self.tool_names = tool_names
        
        # Auto-detect LLM usage: if llm is provided, automatically use it
        if llm is not None:
            use_llm = True
            logger.info("LLM instance provided - automatically enabling LLM-based generation")
        
        # Initialize components
        self.scenario_generator = ScenarioGenerator(
            tool_names=tool_names,
            use_llm=use_llm,
            llm=llm
        )
        self.query_generator = QueryGenerator(use_llm=use_llm, llm=llm)
        self.outcome_simulator = OutcomeSimulator(tool_names=tool_names)
        self.data_validator = DataValidator(min_quality_score=min_quality_score)
        
        logger.info("SyntheticDataPipeline initialized")
    
    def generate(
        self,
        num_samples: int = 100,
        validate: bool = True
    ) -> List[Dict[str, Any]]:
        """
        Generate synthetic training data.
        
        Args:
            num_samples: Number of training samples to generate
            validate: Whether to validate generated data
            
        Returns:
            List of training samples with format:
            {
                'scenario': Scenario,
                'query': str,
                'state_key': str,
                'selected_tools': List[str],
                'outcome': Dict,
                'reward': float
            }
        """
        logger.info(f"Generating {num_samples} synthetic training samples")
        
        # Step 1: Generate scenarios
        scenarios = self.scenario_generator.generate(num_scenarios=num_samples)
        
        # Step 2: Validate scenarios
        if validate:
            scenarios, validation_stats = self.data_validator.validate_batch(scenarios)
            logger.info(f"Validation stats: {validation_stats}")
        
        # Step 3: Generate queries
        training_data = []
        for scenario in scenarios:
            query = self.query_generator.generate_query(scenario)
            
            # Use optimal tools for simulation
            selected_tools = scenario.optimal_tools[:3]  # Top 3 tools
            
            # Step 4: Simulate outcome
            outcome, reward = self.outcome_simulator.simulate(scenario, selected_tools)
            
            # Create training sample
            sample = {
                'scenario': scenario,
                'query': query,
                'state_key': query,  # Use query as state key
                'selected_tools': selected_tools,
                'outcome': outcome,
                'reward': reward
            }
            training_data.append(sample)
        
        logger.info(f"Generated {len(training_data)} training samples")
        return training_data
    
    def generate_for_tools(
        self,
        tool_name: str,
        num_samples: int = 50
    ) -> List[Dict[str, Any]]:
        """
        Generate training data focused on a specific tool.
        
        Args:
            tool_name: Tool to focus on
            num_samples: Number of samples to generate
            
        Returns:
            List of training samples
        """
        logger.info(f"Generating {num_samples} samples for tool: {tool_name}")
        
        # Generate scenarios
        all_scenarios = self.scenario_generator.generate(num_scenarios=num_samples * 2)
        
        # Filter scenarios where this tool is optimal
        relevant_scenarios = [
            s for s in all_scenarios
            if tool_name in s.optimal_tools
        ][:num_samples]
        
        if len(relevant_scenarios) < num_samples:
            logger.warning(
                f"Only found {len(relevant_scenarios)} relevant scenarios "
                f"for tool {tool_name}, requested {num_samples}"
            )
        
        # Generate training data
        training_data = []
        for scenario in relevant_scenarios:
            query = self.query_generator.generate_query(scenario)
            selected_tools = [tool_name]
            outcome, reward = self.outcome_simulator.simulate(scenario, selected_tools)
            
            sample = {
                'scenario': scenario,
                'query': query,
                'state_key': query,
                'selected_tools': selected_tools,
                'outcome': outcome,
                'reward': reward
            }
            training_data.append(sample)
        
        return training_data
