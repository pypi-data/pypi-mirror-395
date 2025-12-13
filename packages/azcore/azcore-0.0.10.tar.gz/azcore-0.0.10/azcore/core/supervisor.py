"""
Supervisor implementation for the Azcore..

This module provides the Supervisor class which manages team member routing
and workflow coordination using LLM-based decision making.
"""

from typing import List, Callable, Literal, Dict, Any
from typing_extensions import TypedDict
from langchain_core.language_models.chat_models import BaseChatModel
from langgraph.types import Command
from langgraph.graph import END
from azcore.exceptions import SupervisorError, LLMError, ValidationError
from azcore.utils.retry import retry_with_timeout
import logging

logger = logging.getLogger(__name__)


class Supervisor:
    """
    LLM-based supervisor for routing requests to team members.
    
    The supervisor analyzes the current state and decides which team member
    should handle the next task, or if the workflow should finish.
    
    Attributes:
        llm: Language model for decision making
        members: List of team member names
        system_prompt: System prompt for the supervisor
    """
    
    def __init__(
        self,
        llm: BaseChatModel,
        members: List[str] | None = None,
        system_prompt: str | None = None,
    ):
        """
        Initialize a supervisor.
        
        Args:
            llm: Language model for routing decisions
            members: Initial list of team members
            system_prompt: Optional custom system prompt
        """
        self.llm = llm
        self.members: List[str] = list(members) if members else []
        self.system_prompt = system_prompt or self._default_prompt()
        
        self._logger = logging.getLogger(self.__class__.__name__)
        
        self._logger.info(f"Supervisor initialized with {len(self.members)} members")
    
    def _default_prompt(self) -> str:
        """
        Get default supervisor prompt.
        
        Returns:
            Default system prompt for the supervisor
        """
        return """You are a supervisor tasked with managing a team of specialized workers.
        Your responsibilities:
        1. Analyze the current task and conversation context
        2. Determine which team member is best suited to handle the request
        3. Route to the appropriate worker or finish if the task is complete

        Available team members will be provided in each routing decision.
        Respond with the name of the next worker to involve, or 'FINISH' when done.

        Guidelines:
        - Choose the most appropriate team member based on their specialization
        - Consider the conversation history and current task requirements
        - Only route to FINISH when the task is genuinely complete
        - Be decisive and avoid unnecessary routing loops
        """
    
    def add_member(self, member_name: str) -> None:
        """
        Add a team member to the supervisor's roster.
        
        Args:
            member_name: Name of the team member to add
        """
        if member_name not in self.members:
            self.members.append(member_name)
            self._logger.info(f"Added member '{member_name}' to supervisor")
        else:
            self._logger.warning(f"Member '{member_name}' already exists")
    
    def remove_member(self, member_name: str) -> bool:
        """
        Remove a team member from the supervisor's roster.
        
        Args:
            member_name: Name of the team member to remove
            
        Returns:
            True if member was removed, False if not found
        """
        if member_name in self.members:
            self.members.remove(member_name)
            self._logger.info(f"Removed member '{member_name}' from supervisor")
            return True
        else:
            self._logger.warning(f"Member '{member_name}' not found")
            return False
    
    def set_members(self, members: List[str]) -> None:
        """
        Set the complete list of team members.
        
        Args:
            members: List of team member names
        """
        self.members = list(members)
        self._logger.info(f"Set {len(self.members)} members")
    
    def get_members(self) -> List[str]:
        """
        Get the list of team members.
        
        Returns:
            List of team member names
        """
        return self.members.copy()
    
    def create_node(self) -> Callable:
        """
        Create a supervisor node callable for use in StateGraph.
        
        Returns:
            Callable node function that can be added to a graph
        """
        return self._make_supervisor_node(self.llm, self.members, self.system_prompt)
    
    def _make_supervisor_node(
        self,
        llm: BaseChatModel,
        members: List[str],
        system_prompt: str
    ) -> Callable:
        """
        Internal method to construct the supervisor node.
        
        Args:
            llm: Language model for routing
            members: List of team members
            system_prompt: System prompt for the supervisor
            
        Returns:
            Supervisor node callable
        """
        # Validate members
        if not members:
            raise ValidationError("Supervisor must have at least one member")
        
        options = ["FINISH"] + list(members)
        
        # Create a proper Literal type dynamically
        from typing import get_args
        NextType = Literal[tuple(options)]  # type: ignore
        
        class Router(TypedDict):
            """Worker to route to next. If no workers needed, route to FINISH."""
            next: str  # Changed from Literal to str to avoid unpacking issue
        
        @retry_with_timeout(max_retries=2, timeout=30.0)
        def supervisor_node(state: Dict[str, Any]) -> Command:
            """
            LLM-based supervisor routing node with error handling.
            
            Args:
                state: Current workflow state
                
            Returns:
                Command with routing decision
                
            Raises:
                SupervisorError: If routing decision fails
            """
            try:
                messages = [
                    {"role": "system", "content": system_prompt},
                ] + state.get("messages", [])
                
                self._logger.debug(f"Supervisor evaluating with {len(members)} members")
                
                # Get structured routing decision from LLM
                response = llm.with_structured_output(Router).invoke(messages)
                goto = response.get("next", "FINISH")
                
                # Validate routing decision
                if goto not in options:
                    self._logger.warning(
                        f"Invalid routing decision '{goto}', defaulting to FINISH. "
                        f"Valid options: {options}"
                    )
                    goto = "FINISH"
                
                if goto == "FINISH":
                    goto = END
                    self._logger.info("Supervisor decided to FINISH")
                else:
                    self._logger.info(f"Supervisor routing to: {goto}")
                
                return Command(goto=goto, update={"next": goto})
                
            except Exception as e:
                self._logger.error(f"Supervisor routing failed: {str(e)}")
                raise SupervisorError(
                    f"Failed to route request: {str(e)}",
                    details={"members": members, "error": str(e)}
                )
        
        return supervisor_node
    
    def node(self) -> Callable:
        """
        Get a supervisor node reflecting current members.
        
        This is a convenience method that calls create_node().
        
        Returns:
            Callable supervisor node
        """
        return self.create_node()
    
    def update_prompt(self, new_prompt: str) -> None:
        """
        Update the supervisor's system prompt.
        
        Args:
            new_prompt: New system prompt to use
        """
        self.system_prompt = new_prompt
        self._logger.info("Updated supervisor system prompt")
    
    def __repr__(self) -> str:
        return f"Supervisor(members={len(self.members)})"
    
    def __str__(self) -> str:
        return f"Supervisor with members: {', '.join(self.members)}"


# Main Supervisor - To be utilized as the primary Orchestrator Supervisor
class MainSupervisor:
    """
    LLM-based supervisor for routing requests to team members.
    
    The supervisor analyzes the current state and decides which team member
    should handle the next task, or if the workflow should finish.
    
    Attributes:
        llm: Language model for decision making
        members: List of team member names
        system_prompt: System prompt for the supervisor
    """
    
    def __init__(
        self,
        llm: BaseChatModel,
        members: List[str] | None = None,
        system_prompt: str | None = None
    ):
        """
        Initialize a supervisor.
        
        Args:
            llm: Language model for routing decisions
            members: Initial list of team members
            system_prompt: Optional custom system prompt
        """
        self.llm = llm
        self.members: List[str] = list(members) if members else []
        self.system_prompt = system_prompt or self._default_prompt()
        self._logger = logging.getLogger(self.__class__.__name__)
        
        self._logger.info(f"Supervisor initialized with {len(self.members)} members")
    
    def _default_prompt(self) -> str:
        """
        Get default supervisor prompt.
        
        Returns:
            Default system prompt for the supervisor
        """
        return """You are a supervisor tasked with managing a team of specialized workers.
            Your responsibilities:
            1. Analyze the current task and conversation context
            2. Determine which team member is best suited to handle the request
            3. Route to the appropriate worker or finish if the task is complete

            Available team members will be provided in each routing decision.
            Respond with the name of the next worker to involve, or 'FINISH' when done.

            Guidelines:
            - Choose the most appropriate team member based on their specialization
            - Consider the conversation history and current task requirements
            - Only route to FINISH when the task is genuinely complete
            - Be decisive and avoid unnecessary routing loops
            """
    
    def add_member(self, member_name: str) -> None:
        """
        Add a team member to the supervisor's roster.
        
        Args:
            member_name: Name of the team member to add
        """
        if member_name not in self.members:
            self.members.append(member_name)
            self._logger.info(f"Added member '{member_name}' to supervisor")
        else:
            self._logger.warning(f"Member '{member_name}' already exists")
    
    def remove_member(self, member_name: str) -> bool:
        """
        Remove a team member from the supervisor's roster.
        
        Args:
            member_name: Name of the team member to remove
            
        Returns:
            True if member was removed, False if not found
        """
        if member_name in self.members:
            self.members.remove(member_name)
            self._logger.info(f"Removed member '{member_name}' from supervisor")
            return True
        else:
            self._logger.warning(f"Member '{member_name}' not found")
            return False
    
    def set_members(self, members: List[str]) -> None:
        """
        Set the complete list of team members.
        
        Args:
            members: List of team member names
        """
        self.members = list(members)
        self._logger.info(f"Set {len(self.members)} members")
    
    def get_members(self) -> List[str]:
        """
        Get the list of team members.
        
        Returns:
            List of team member names
        """
        return self.members.copy()
    
    def create_node(self) -> Callable:
        """
        Create a supervisor node callable for use in StateGraph.
        
        Returns:
            Callable node function that can be added to a graph
        """
        return self._make_supervisor_node(self.llm, self.members, self.system_prompt)
    
    def _make_supervisor_node(
        self,
        llm: BaseChatModel,
        members: List[str],
        system_prompt: str
    ) -> Callable:
        """
        Internal method to construct the supervisor node.
        
        Args:
            llm: Language model for routing
            members: List of team members
            system_prompt: System prompt for the supervisor
            
        Returns:
            Supervisor node callable
        """
        # Validate members
        if not members:
            raise ValidationError("MainSupervisor must have at least one member")
        
        options = ["response_generator"] + list(members)
        
        class Router(TypedDict):
            """Worker to route to next. If no workers needed, route to FINISH."""
            next: str  # Changed from Literal to str to avoid unpacking issue
        
        @retry_with_timeout(max_retries=2, timeout=30.0)
        def supervisor_node(state: Dict[str, Any]) -> Command:
            """
            LLM-based supervisor routing node with error handling.
            
            Args:
                state: Current workflow state
                
            Returns:
                Command with routing decision
                
            Raises:
                SupervisorError: If routing decision fails
            """
            try:
                messages = [
                    {"role": "system", "content": system_prompt},
                ] + state.get("messages", [])
                
                self._logger.debug(f"Supervisor evaluating with {len(members)} members")
                
                # Get structured routing decision from LLM
                response = llm.with_structured_output(Router).invoke(messages)
                goto = response.get("next", "FINISH")
                
                # Validate routing decision
                if goto not in options:
                    self._logger.warning(
                        f"Invalid routing decision '{goto}', defaulting to response_generator. "
                        f"Valid options: {options}"
                    )
                    goto = "response_generator"
                
                if goto == "FINISH":
                    goto = "response_generator"
                    self._logger.info("Supervisor decided to FINISH")
                else:
                    self._logger.info(f"Supervisor routing to: {goto}")
                
                return Command(goto=goto, update={"next": goto})
                
            except Exception as e:
                self._logger.error(f"Supervisor routing failed: {str(e)}")
                raise SupervisorError(
                    f"Failed to route request: {str(e)}",
                    details={"members": members, "error": str(e)}
                )
        
        return supervisor_node
    
    def node(self) -> Callable:
        """
        Get a supervisor node reflecting current members.
        
        This is a convenience method that calls create_node().
        
        Returns:
            Callable supervisor node
        """
        return self.create_node()
    
    def update_prompt(self, new_prompt: str) -> None:
        """
        Update the supervisor's system prompt.
        
        Args:
            new_prompt: New system prompt to use
        """
        self.system_prompt = new_prompt
        self._logger.info("Updated supervisor system prompt")
    
    def __repr__(self) -> str:
        return f"Supervisor(members={len(self.members)})"
    
    def __str__(self) -> str:
        return f"Supervisor with members: {', '.join(self.members)}"


def create_supervisor_node(
    llm: BaseChatModel,
    members: List[str],
    system_prompt: str | None = None
) -> Callable:
    """
    Utility function to create a supervisor node directly.
    
    Args:
        llm: Language model for routing
        members: List of team member names
        system_prompt: Optional custom system prompt
        
    Returns:
        Callable supervisor node
    """
    supervisor = Supervisor(llm, members, system_prompt)
    return supervisor.create_node()
