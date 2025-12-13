"""
State management for the Azcore..

This module provides state management capabilities including state definition,
validation, and manipulation throughout the agent workflow.
"""

from typing import Annotated, Any, Dict, List, Optional
from typing_extensions import TypedDict
from langgraph.graph import MessagesState
from langgraph.graph.message import add_messages
from langchain_core.messages import AnyMessage
import logging

logger = logging.getLogger(__name__)


class State(MessagesState):
    """
    Enhanced state class for the Azcore..
    
    Extends LangGraph's MessagesState to include additional fields
    for workflow management, team coordination, and planning.
    
    Attributes:
        messages: List of messages in the conversation
        next: Next node to visit in the graph
        full_plan: Complete execution plan from planner
        context: Additional context data
        metadata: Metadata for tracking and logging
        rl_metadata: RL-specific metadata (state keys, selected tools, rewards)
    """
    
    next: str = ""
    full_plan: str = ""
    context: Dict[str, Any] = {}
    metadata: Dict[str, Any] = {}
    rl_metadata: Dict[str, Any] = {}
    
    def __init__(self, **kwargs):
        """Initialize state with default values."""
        super().__init__(**kwargs)
        if not hasattr(self, 'context'):
            self.context = {}
        if not hasattr(self, 'metadata'):
            self.metadata = {}
        if not hasattr(self, 'rl_metadata'):
            self.rl_metadata = {}


class StateManager:
    """
    Manager for state operations and validation.
    
    Provides utilities for state manipulation, validation, and tracking
    throughout the workflow execution.
    """
    
    def __init__(self):
        """Initialize the state manager."""
        self._logger = logging.getLogger(self.__class__.__name__)
    
    def create_initial_state(
        self,
        messages: Optional[List[AnyMessage]] = None,
        context: Optional[Dict[str, Any]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        rl_metadata: Optional[Dict[str, Any]] = None
    ) -> State:
        """
        Create an initial state with given parameters.
        
        Args:
            messages: Initial messages
            context: Initial context data
            metadata: Initial metadata
            rl_metadata: RL-specific metadata
            
        Returns:
            New State instance
        """
        state_dict = {
            "messages": messages or [],
            "next": "",
            "full_plan": "",
            "context": context or {},
            "metadata": metadata or {},
            "rl_metadata": rl_metadata or {}
        }
        
        self._logger.debug(f"Created initial state with {len(state_dict['messages'])} messages")
        return state_dict
    
    def update_state(
        self,
        state: State,
        updates: Dict[str, Any]
    ) -> State:
        """
        Update state with new values.
        
        Args:
            state: Current state
            updates: Dictionary of updates to apply
            
        Returns:
            Updated state
        """
        updated_state = {**state, **updates}
        self._logger.debug(f"Updated state with keys: {list(updates.keys())}")
        return updated_state
    
    def add_context(
        self,
        state: State,
        key: str,
        value: Any
    ) -> State:
        """
        Add or update a context value.
        
        Args:
            state: Current state
            key: Context key
            value: Context value
            
        Returns:
            Updated state
        """
        context = state.get("context", {}).copy()
        context[key] = value
        return self.update_state(state, {"context": context})
    
    def get_context(
        self,
        state: State,
        key: str,
        default: Any = None
    ) -> Any:
        """
        Get a context value.
        
        Args:
            state: Current state
            key: Context key
            default: Default value if key not found
            
        Returns:
            Context value or default
        """
        return state.get("context", {}).get(key, default)
    
    def add_metadata(
        self,
        state: State,
        key: str,
        value: Any
    ) -> State:
        """
        Add or update metadata.
        
        Args:
            state: Current state
            key: Metadata key
            value: Metadata value
            
        Returns:
            Updated state
        """
        metadata = state.get("metadata", {}).copy()
        metadata[key] = value
        return self.update_state(state, {"metadata": metadata})
    
    def validate_state(self, state: State) -> bool:
        """
        Validate state structure and required fields.
        
        Args:
            state: State to validate
            
        Returns:
            True if valid, False otherwise
        """
        required_fields = ["messages", "next", "full_plan", "context", "metadata", "rl_metadata"]
        
        for field in required_fields:
            if field not in state:
                self._logger.error(f"Missing required field: {field}")
                return False
        
        if not isinstance(state["messages"], list):
            self._logger.error("Messages field must be a list")
            return False
        
        if not isinstance(state["context"], dict):
            self._logger.error("Context field must be a dictionary")
            return False
        
        if not isinstance(state["metadata"], dict):
            self._logger.error("Metadata field must be a dictionary")
            return False
        
        if not isinstance(state["rl_metadata"], dict):
            self._logger.error("RL metadata field must be a dictionary")
            return False
        
        return True
    
    def clear_state(self, state: State) -> State:
        """
        Clear state while preserving structure.
        
        Args:
            state: State to clear
            
        Returns:
            Cleared state
        """
        return self.create_initial_state()
    
    def get_message_history(self, state: State) -> List[AnyMessage]:
        """
        Get message history from state.
        
        Args:
            state: Current state
            
        Returns:
            List of messages
        """
        return state.get("messages", [])
    
    def get_last_message(self, state: State) -> Optional[AnyMessage]:
        """
        Get the last message from state.
        
        Args:
            state: Current state
            
        Returns:
            Last message or None
        """
        messages = self.get_message_history(state)
        return messages[-1] if messages else None
    
    def add_rl_metadata(
        self,
        state: State,
        key: str,
        value: Any
    ) -> State:
        """
        Add or update RL metadata.
        
        Args:
            state: Current state
            key: RL metadata key
            value: RL metadata value
            
        Returns:
            Updated state
        """
        rl_metadata = state.get("rl_metadata", {}).copy()
        rl_metadata[key] = value
        return self.update_state(state, {"rl_metadata": rl_metadata})
    
    def get_rl_metadata(
        self,
        state: State,
        key: str,
        default: Any = None
    ) -> Any:
        """
        Get RL metadata value.
        
        Args:
            state: Current state
            key: RL metadata key
            default: Default value if key not found
            
        Returns:
            RL metadata value or default
        """
        return state.get("rl_metadata", {}).get(key, default)
