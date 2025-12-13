"""
Planner node implementation.

The planner creates comprehensive execution plans for complex tasks,
breaking them down into steps and determining which teams to involve.
"""

from typing import Literal, Dict, Any
import json
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import HumanMessage
from langgraph.types import Command
from langgraph.graph import END
from azcore.core.base import BaseNode
import logging

logger = logging.getLogger(__name__)


class PlannerNode(BaseNode):
    """
    Planner node for task decomposition and planning.
    
    The planner:
    1. Analyzes complex user requests
    2. Breaks them into executable steps
    3. Determines which teams/agents to involve
    4. Creates a structured execution plan
    5. Routes to supervisor for execution
    
    Attributes:
        llm: Language model for planning
        system_prompt: System prompt defining planner behavior
        validate_json: Whether to validate plan as JSON
    """
    
    def __init__(
        self,
        llm: BaseChatModel,
        system_prompt: str | None = None,
        validate_json: bool = True,
        name: str = "planner"
    ):
        """
        Initialize a planner node.
        
        Args:
            llm: Language model for planning
            system_prompt: Optional system prompt
            validate_json: Whether to validate plan as JSON
            name: Node name
        """
        super().__init__(name=name, description="Plans task execution")
        
        self.llm = llm
        self.validate_json = validate_json
        # Set custom prompt first if provided, otherwise it will be None
        self._custom_prompt = system_prompt
        # Now call _default_prompt which will use _custom_prompt if available
        self.system_prompt = self._default_prompt()
        
        self._logger.info(f"PlannerNode '{name}' initialized")

    def _default_prompt(self) -> str:
        """
        Get default planner prompt.
        
        Returns:
            Default system prompt
        """
        # Use custom prompt if provided, otherwise empty string
        custom_section = f"\n{self._custom_prompt}\n" if self._custom_prompt else ""
        
        return f"""You are an expert task planner for multi-agent systems.
            
            Your responsibilities:
            1. Analyze complex user requests thoroughly
            2. Break tasks into clear, executable steps
            3. Identify which specialized teams should handle each step
            4. Create a structured JSON execution plan
            5. Consider dependencies and sequencing
            6.  make sure the plan to be consise and what needs to be done with the highlevel agents 
            {custom_section}
            Output Format (JSON):
            {{
                "task": "High-level task description",
                "steps": [
                    {{
                        "step": 1,
                        "description": "Detailed step description",
                        "assigned_team": "team_name",
                        "dependencies": [],
                        "tool selection": ["tool1", "tool2"],
                        "expected_output": "What this step should produce"
                    }}
                ],
                "success_criteria": "How to know when task is complete"
            }}

            Guidelines:
            - Be thorough but concise
            - Ensure each step is actionable
            - Assign appropriate teams based on their specializations
            - Consider error handling and edge cases
            - Make plans flexible enough to adapt

            Available teams will be provided in the conversation context.
            """
    
    def execute(self, state: Dict[str, Any]) -> Command[Literal["supervisor", "__end__"]]:
        """
        Execute planner logic.
        
        Args:
            state: Current workflow state
            
        Returns:
            Command with plan and routing decision
        """
        self._logger.info("Planner generating execution plan")
        
        messages = [
            {"role": "system", "content": self.system_prompt},
        ] + state.get("messages", [])
        
        # Stream response for better performance
        stream = self.llm.stream(messages)
        full_response = ""
        for chunk in stream:
            full_response += chunk.content
        
        self._logger.debug(f"Raw planner response: {full_response[:200]}...")
        
        # Clean up JSON formatting
        cleaned_response = self._clean_json_response(full_response)
        
        #logger.debug(cleaned_response)
        
        print("planner response",cleaned_response)
        
        # Validate if requested
        goto = "supervisor"
        if self.validate_json:
            if not self._validate_plan(cleaned_response):
                self._logger.warning("Planner produced invalid JSON, ending workflow")
                goto = END
        
        return Command(
            update={
                "messages": [
                    HumanMessage(content=cleaned_response, name=self.name)
                ],
                "full_plan": cleaned_response
            },
            goto=goto
        )
    
    def _clean_json_response(self, response: str) -> str:
        """
        Clean JSON response by removing markdown formatting.
        
        Args:
            response: Raw response string
            
        Returns:
            Cleaned response
        """
        cleaned = response
        
        # Remove JSON code fences
        if cleaned.startswith("```json"):
            cleaned = cleaned.removeprefix("```json")
        elif cleaned.startswith("```"):
            cleaned = cleaned.removeprefix("```")
        elif cleaned.startswith("json"):
            cleaned = cleaned.removeprefix("json")
        
        if cleaned.endswith("```"):
            cleaned = cleaned.removesuffix("```")
        
        return cleaned.strip()
    
    def _validate_plan(self, plan: str) -> bool:
        """
        Validate that plan is valid JSON.
        
        Args:
            plan: Plan string to validate
            
        Returns:
            True if valid, False otherwise
        """
        try:
            json.loads(plan)
            self._logger.debug("Plan validated successfully")
            return True
        except json.JSONDecodeError as e:
            self._logger.error(f"Plan validation failed: {e}")
            return False
    
    def set_prompt(self, prompt: str) -> None:
        """
        Update the system prompt.
        
        Args:
            prompt: New system prompt
        """
        self.system_prompt = prompt
        self._logger.info("Updated planner system prompt")
    
    def set_validation(self, validate: bool) -> None:
        """
        Enable or disable JSON validation.
        
        Args:
            validate: Whether to validate JSON
        """
        self.validate_json = validate
        self._logger.info(f"JSON validation set to: {validate}")


def create_planner_node(
    llm: BaseChatModel,
    system_prompt: str | None = None,
    validate_json: bool = True,
    name: str = "planner"
) -> PlannerNode:
    """
    Factory function to create a planner node.
    
    Args:
        llm: Language model
        system_prompt: Optional system prompt
        validate_json: Whether to validate JSON output
        name: Node name
        
    Returns:
        PlannerNode instance
    """
    return PlannerNode(
        llm=llm,
        system_prompt=system_prompt,
        validate_json=validate_json,
        name=name
    )
