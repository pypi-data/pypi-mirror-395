"""
Scenario generator for synthetic RL training data.

This module generates diverse task scenarios that represent
real-world agent use cases.
"""

import random
import logging
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from enum import Enum

logger = logging.getLogger(__name__)


class ScenarioDomain(Enum):
    """Domain categories for scenarios."""
    DATA_ANALYSIS = "data_analysis"
    WEB_SEARCH = "web_search"
    CODE_GENERATION = "code_generation"
    MATH_CALCULATION = "math_calculation"
    FILE_OPERATIONS = "file_operations"
    API_INTERACTION = "api_interaction"
    TEXT_PROCESSING = "text_processing"
    GENERAL_QUERY = "general_query"


class ComplexityLevel(Enum):
    """Complexity levels for scenarios."""
    SIMPLE = "simple"
    MEDIUM = "medium"
    COMPLEX = "complex"


@dataclass
class Scenario:
    """Represents a task scenario."""
    domain: ScenarioDomain
    complexity: ComplexityLevel
    description: str
    optimal_tools: List[str]
    expected_success_rate: float
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'domain': self.domain.value,
            'complexity': self.complexity.value,
            'description': self.description,
            'optimal_tools': self.optimal_tools,
            'expected_success_rate': self.expected_success_rate,
            'metadata': self.metadata
        }


class ScenarioGenerator:
    """
    Generates diverse task scenarios for RL training.
    
    Example:
        >>> generator = ScenarioGenerator(tool_names=["search", "calculator", "code_executor"])
        >>> scenarios = generator.generate(num_scenarios=100)
    """
    
    def __init__(
        self,
        tool_names: List[str],
        use_llm: bool = False,
        llm: Optional[Any] = None
    ):
        """
        Initialize the scenario generator.
        
        Args:
            tool_names: List of available tool names
            use_llm: Whether to use LLM for scenario generation
            llm: Optional LLM instance for generation
        """
        self.tool_names = tool_names
        self.use_llm = use_llm
        self.llm = llm
        
        # Define scenario templates
        self.templates = self._initialize_templates()
        
        logger.info(f"ScenarioGenerator initialized with {len(tool_names)} tools")
    
    def _initialize_templates(self) -> Dict[ScenarioDomain, List[Dict[str, Any]]]:
        """Initialize scenario templates for each domain."""
        return {
            ScenarioDomain.DATA_ANALYSIS: [
                {
                    'description': 'Analyze sales data for trends',
                    'complexity': ComplexityLevel.MEDIUM,
                    'tools': ['data_analyzer', 'python_executor'],
                    'success_rate': 0.85
                },
                {
                    'description': 'Calculate statistical metrics from dataset',
                    'complexity': ComplexityLevel.SIMPLE,
                    'tools': ['calculator', 'data_analyzer'],
                    'success_rate': 0.90
                },
                {
                    'description': 'Generate visualization from complex data',
                    'complexity': ComplexityLevel.COMPLEX,
                    'tools': ['data_analyzer', 'python_executor', 'file_writer'],
                    'success_rate': 0.75
                }
            ],
            ScenarioDomain.WEB_SEARCH: [
                {
                    'description': 'Search for current weather information',
                    'complexity': ComplexityLevel.SIMPLE,
                    'tools': ['web_search', 'api_caller'],
                    'success_rate': 0.95
                },
                {
                    'description': 'Find and summarize recent news articles',
                    'complexity': ComplexityLevel.MEDIUM,
                    'tools': ['web_search', 'text_summarizer'],
                    'success_rate': 0.80
                },
                {
                    'description': 'Research topic and compile information',
                    'complexity': ComplexityLevel.COMPLEX,
                    'tools': ['web_search', 'text_processor', 'file_writer'],
                    'success_rate': 0.70
                }
            ],
            ScenarioDomain.CODE_GENERATION: [
                {
                    'description': 'Write a simple function',
                    'complexity': ComplexityLevel.SIMPLE,
                    'tools': ['code_generator', 'python_executor'],
                    'success_rate': 0.88
                },
                {
                    'description': 'Debug and fix code snippet',
                    'complexity': ComplexityLevel.MEDIUM,
                    'tools': ['code_analyzer', 'code_generator'],
                    'success_rate': 0.75
                },
                {
                    'description': 'Implement complex algorithm with optimization',
                    'complexity': ComplexityLevel.COMPLEX,
                    'tools': ['code_generator', 'python_executor', 'code_analyzer'],
                    'success_rate': 0.65
                }
            ],
            ScenarioDomain.MATH_CALCULATION: [
                {
                    'description': 'Perform basic arithmetic calculation',
                    'complexity': ComplexityLevel.SIMPLE,
                    'tools': ['calculator'],
                    'success_rate': 0.98
                },
                {
                    'description': 'Solve algebraic equation',
                    'complexity': ComplexityLevel.MEDIUM,
                    'tools': ['calculator', 'math_solver'],
                    'success_rate': 0.85
                },
                {
                    'description': 'Calculate complex mathematical expression',
                    'complexity': ComplexityLevel.COMPLEX,
                    'tools': ['calculator', 'python_executor', 'math_solver'],
                    'success_rate': 0.80
                }
            ],
            ScenarioDomain.FILE_OPERATIONS: [
                {
                    'description': 'Read content from a file',
                    'complexity': ComplexityLevel.SIMPLE,
                    'tools': ['file_reader'],
                    'success_rate': 0.95
                },
                {
                    'description': 'Process and modify file content',
                    'complexity': ComplexityLevel.MEDIUM,
                    'tools': ['file_reader', 'text_processor', 'file_writer'],
                    'success_rate': 0.82
                },
                {
                    'description': 'Batch process multiple files',
                    'complexity': ComplexityLevel.COMPLEX,
                    'tools': ['file_reader', 'python_executor', 'file_writer'],
                    'success_rate': 0.70
                }
            ],
            ScenarioDomain.TEXT_PROCESSING: [
                {
                    'description': 'Summarize a text document',
                    'complexity': ComplexityLevel.SIMPLE,
                    'tools': ['text_summarizer'],
                    'success_rate': 0.90
                },
                {
                    'description': 'Extract key information from text',
                    'complexity': ComplexityLevel.MEDIUM,
                    'tools': ['text_processor', 'text_analyzer'],
                    'success_rate': 0.83
                },
                {
                    'description': 'Analyze sentiment and generate report',
                    'complexity': ComplexityLevel.COMPLEX,
                    'tools': ['text_processor', 'text_analyzer', 'file_writer'],
                    'success_rate': 0.75
                }
            ]
        }
    
    def generate(
        self,
        num_scenarios: int = 100,
        domain_distribution: Optional[Dict[ScenarioDomain, float]] = None
    ) -> List[Scenario]:
        """
        Generate scenarios.
        
        Args:
            num_scenarios: Number of scenarios to generate
            domain_distribution: Optional distribution across domains
            
        Returns:
            List of generated scenarios
        """
        scenarios = []
        
        # Use uniform distribution if not specified
        if domain_distribution is None:
            domains = list(ScenarioDomain)
            per_domain = num_scenarios // len(domains)
            domain_distribution = {d: per_domain for d in domains}
            # Add remainder to first domain
            domain_distribution[domains[0]] += num_scenarios % len(domains)
        
        # Generate scenarios for each domain
        for domain, count in domain_distribution.items():
            if domain not in self.templates:
                logger.warning(f"No templates for domain {domain}")
                continue
            
            for _ in range(count):
                scenario = self._generate_scenario(domain)
                if scenario:
                    scenarios.append(scenario)
        
        logger.info(f"Generated {len(scenarios)} scenarios")
        return scenarios
    
    def _generate_scenario(self, domain: ScenarioDomain) -> Optional[Scenario]:
        """Generate a single scenario for a domain."""
        templates = self.templates.get(domain, [])
        if not templates:
            return None
        
        # Select random template
        template = random.choice(templates)
        
        # Filter tools to only available ones
        optimal_tools = [t for t in template['tools'] if t in self.tool_names]
        if not optimal_tools:
            # Use random available tool as fallback
            optimal_tools = [random.choice(self.tool_names)] if self.tool_names else []
        
        # Create scenario
        scenario = Scenario(
            domain=domain,
            complexity=template['complexity'],
            description=template['description'],
            optimal_tools=optimal_tools,
            expected_success_rate=template['success_rate']
        )
        
        return scenario
    
    def generate_variations(self, scenario: Scenario, num_variations: int = 5) -> List[Scenario]:
        """
        Generate variations of a scenario.
        
        Args:
            scenario: Base scenario
            num_variations: Number of variations to create
            
        Returns:
            List of scenario variations
        """
        variations = [scenario]
        
        for _ in range(num_variations - 1):
            # Slightly modify the scenario
            variation = Scenario(
                domain=scenario.domain,
                complexity=scenario.complexity,
                description=self._vary_description(scenario.description),
                optimal_tools=scenario.optimal_tools.copy(),
                expected_success_rate=scenario.expected_success_rate + random.uniform(-0.05, 0.05)
            )
            variations.append(variation)
        
        return variations
    
    def _vary_description(self, description: str) -> str:
        """Create a variation of a description."""
        # Simple variation by adding prefixes/suffixes
        prefixes = ["Please ", "I need to ", "Help me ", "Can you ", ""]
        suffixes = [" for me", " quickly", " please", " now", ""]
        
        prefix = random.choice(prefixes)
        suffix = random.choice(suffixes)
        
        return f"{prefix}{description}{suffix}"
