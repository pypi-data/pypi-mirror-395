"""
Query generator for synthetic RL training data.

This module converts scenarios into natural language queries.
"""

import random
import logging
from typing import List, Optional, Any
from azcore.rl.synthetic_data.scenario_generator import Scenario, ScenarioDomain

logger = logging.getLogger(__name__)


class QueryGenerator:
    """
    Generates natural language queries from scenarios.
    
    Example:
        >>> generator = QueryGenerator()
        >>> query = generator.generate_query(scenario)
    """
    
    def __init__(self, use_llm: bool = False, llm: Optional[Any] = None):
        """
        Initialize the query generator.
        
        Args:
            use_llm: Whether to use LLM for query generation
            llm: Optional LLM instance for generation
        """
        self.use_llm = use_llm
        self.llm = llm
        
        # Query templates for different domains
        self.templates = self._initialize_templates()
        
        logger.info("QueryGenerator initialized")
    
    def _initialize_templates(self) -> dict:
        """Initialize query templates."""
        return {
            ScenarioDomain.DATA_ANALYSIS: [
                "Analyze the {subject} and show me {result}",
                "Can you look at the {subject} and tell me {result}?",
                "I need to understand {subject}, specifically {result}",
                "Help me analyze {subject} to find {result}",
                "What can you tell me about {subject} in terms of {result}?"
            ],
            ScenarioDomain.WEB_SEARCH: [
                "Search for {subject}",
                "Find information about {subject}",
                "What can you tell me about {subject}?",
                "Look up {subject} online",
                "I need to know about {subject}"
            ],
            ScenarioDomain.CODE_GENERATION: [
                "Write code to {task}",
                "Can you create a function that {task}?",
                "I need a script to {task}",
                "Help me implement {task}",
                "Generate code for {task}"
            ],
            ScenarioDomain.MATH_CALCULATION: [
                "Calculate {expression}",
                "What is {expression}?",
                "Solve {expression}",
                "Can you compute {expression}?",
                "I need to know {expression}"
            ],
            ScenarioDomain.FILE_OPERATIONS: [
                "{action} the file {filename}",
                "Can you {action} {filename}?",
                "I need to {action} {filename}",
                "Help me {action} {filename}",
                "Please {action} {filename}"
            ],
            ScenarioDomain.TEXT_PROCESSING: [
                "{action} this text: {content}",
                "Can you {action} the following? {content}",
                "I need you to {action}: {content}",
                "Help me {action} this: {content}",
                "Please {action} {content}"
            ]
        }
    
    def generate_query(self, scenario: Scenario) -> str:
        """
        Generate a natural language query from a scenario.
        
        Args:
            scenario: Scenario to convert to query
            
        Returns:
            Natural language query string
        """
        if self.use_llm and self.llm:
            return self._generate_with_llm(scenario)
        else:
            return self._generate_from_template(scenario)
    
    def _generate_from_template(self, scenario: Scenario) -> str:
        """Generate query using templates."""
        # Use scenario description as base
        base_query = scenario.description
        
        # Add variations
        variations = [
            base_query,
            f"Please {base_query.lower()}",
            f"Can you {base_query.lower()}?",
            f"I need to {base_query.lower()}",
            f"Help me {base_query.lower()}",
            base_query.capitalize()
        ]
        
        return random.choice(variations)
    
    def _generate_with_llm(self, scenario: Scenario) -> str:
        """Generate query using LLM (if available)."""
        if not self.llm:
            return self._generate_from_template(scenario)
        
        try:
            prompt = f"""Generate a natural user query for the following task:
Domain: {scenario.domain.value}
Task: {scenario.description}

Generate a query that a user would naturally ask. Reply with just the query, nothing else."""
            
            response = self.llm.invoke(prompt)
            query = response.content if hasattr(response, 'content') else str(response)
            return query.strip()
        except Exception as e:
            logger.error(f"Error generating query with LLM: {e}")
            return self._generate_from_template(scenario)
    
    def generate_batch(self, scenarios: List[Scenario]) -> List[str]:
        """
        Generate queries for multiple scenarios.
        
        Args:
            scenarios: List of scenarios
            
        Returns:
            List of generated queries
        """
        queries = [self.generate_query(s) for s in scenarios]
        logger.info(f"Generated {len(queries)} queries")
        return queries
