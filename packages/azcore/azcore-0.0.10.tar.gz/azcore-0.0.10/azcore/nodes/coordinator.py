"""
Coordinator node implementation.

The coordinator acts as the front-line agent that communicates with users
and decides whether to hand off to the planner or finish the conversation.
"""

from typing import Literal, Dict, Any
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import HumanMessage
from langgraph.types import Command
from langgraph.graph import END
from azcore.core.base import BaseNode
from azcore.exceptions import NodeExecutionError, ValidationError
from azcore.utils.retry import retry_with_timeout
import logging

logger = logging.getLogger(__name__)


class CoordinatorNode(BaseNode):
    """
    Coordinator node for user interaction and task triage.
    
    The coordinator:
    1. Communicates directly with users
    2. Understands user requests
    3. Decides if complex planning is needed
    4. Routes to planner or ends conversation
    
    Attributes:
        llm: Language model for coordinator
        system_prompt: System prompt defining coordinator behavior
        handoff_keyword: Keyword to trigger handoff to planner
    """
    
    def __init__(
        self,
        llm: BaseChatModel,
        system_prompt: str | None = None,
        handoff_keyword: str = "handoff_to_planner",
        name: str = "coordinator"
    ):
        """
        Initialize the coordinator node.
        
        Args:
            llm: Language model for the coordinator
            system_prompt: Optional custom system prompt
            handoff_keyword: Keyword to detect planner handoff
            name: Node name
        """
        super().__init__(name=name, description="Coordinates user interactions")
        
        self.llm = llm
        self.handoff_keyword = handoff_keyword
        self.system_prompt = system_prompt or self._default_prompt()
        
        self._logger.info(f"CoordinatorNode '{name}' initialized")
    
    def _default_prompt(self) -> str:
        """
        Get default coordinator prompt.
        
        Returns:
            Default system prompt
        """
        return """You are a friendly and helpful coordinator agent.
                Your responsibilities:
                1. Greet users warmly and understand their requests
                "No matter the complexity and nature of the request if not small talk delegate to planner"
                2. you only should handle the greetings and every other requests please  delegate to planner 
                3. always  delegate the task to the planner by responsing as  "handoff_to_planner"
                4. Be conversational and professional
                5. Clarify ambiguous requests before proceeding

                Guidelines:
                - Keep responses concise and clear
                - Ask clarifying questions when needed

                

                Remember: You are the user's first point of contact. Make a good impression!
            """
    
    @retry_with_timeout(max_retries=2, timeout=30.0)
    def execute(self, state: Dict[str, Any]) -> Command[Literal["planner", "__end__"]]:
        """
        Execute coordinator logic with error handling.
        
        Args:
            state: Current workflow state
            
        Returns:
            Command with routing decision
            
        Raises:
            NodeExecutionError: If execution fails
            ValidationError: If state is invalid
        """
        try:
            # Validate state
            if not state or "messages" not in state:
                raise ValidationError(
                    "Invalid state: missing 'messages' key",
                    details={"state_keys": list(state.keys()) if state else []}
                )
            
            self._logger.info("Coordinator processing request")
            
            messages = [
                {"role": "system", "content": self.system_prompt},
            ] + state.get("messages", [])
            
            # Get coordinator response
            response = self.llm.invoke(messages)
            
            # Validate response
            if not response or not hasattr(response, 'content'):
                raise NodeExecutionError(
                    "Invalid LLM response from coordinator",
                    details={"response": str(response)}
                )
            
            self._logger.debug(f"Coordinator response: {response.content[:100]}...")
            
            # Determine next node
            goto = END
            if self.handoff_keyword in response.content:
                goto = "planner"
                self._logger.info("Coordinator handing off to planner")
            else:
                self._logger.info("Coordinator ending conversation")
            
            return Command(
                update={
                    "messages": [
                        HumanMessage(content=response.content, name=self.name)
                    ]
                },
                goto=goto
            )
            
        except (ValidationError, NodeExecutionError):
            # Re-raise our custom exceptions
            raise
        except Exception as e:
            self._logger.error(f"Coordinator execution failed: {str(e)}")
            raise NodeExecutionError(
                f"Coordinator node failed: {str(e)}",
                details={"node": self.name, "error": str(e)}
            )
    
    def set_prompt(self, prompt: str) -> None:
        """
        Update the system prompt.
        
        Args:
            prompt: New system prompt
        """
        self.system_prompt = prompt
        self._logger.info("Updated coordinator system prompt")
    
    def set_handoff_keyword(self, keyword: str) -> None:
        """
        Update the handoff keyword.
        
        Args:
            keyword: New handoff keyword
        """
        self.handoff_keyword = keyword
        self._logger.info(f"Updated handoff keyword to: {keyword}")


def create_coordinator_node(
    llm: BaseChatModel,
    system_prompt: str | None = None,
    name: str = "coordinator"
) -> CoordinatorNode:
    """
    Factory function to create a coordinator node.
    
    Args:
        llm: Language model
        system_prompt: Optional system prompt
        name: Node name
        
    Returns:
        CoordinatorNode instance
    """
    return CoordinatorNode(llm=llm, system_prompt=system_prompt, name=name)
