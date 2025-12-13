"""
Patch Tool Calls Middleware for Azcore.

This middleware handles dangling tool calls in the message history by automatically
adding ToolMessages for any tool calls that were cancelled or interrupted before
completion. This prevents errors from incomplete tool execution chains.
"""

from typing import Any, Dict, List, Optional, Protocol
from ..utils.logging import get_logger

logger = get_logger(__name__)


class Message(Protocol):
    """Message protocol."""
    type: str
    content: Optional[str]
    tool_calls: Optional[List[Dict[str, Any]]]
    tool_call_id: Optional[str]
    
    def __getitem__(self, key: str) -> Any:
        ...


class Runtime(Protocol):
    """Runtime protocol for middleware."""
    state: Dict[str, Any]


class PatchToolCallsMiddleware:
    """
    Middleware to patch dangling tool calls in message history.
    
    When an agent makes a tool call but the execution is interrupted (e.g., by
    a human-in-the-loop pause, error, or cancellation), the message history
    can be left with an AIMessage containing tool_calls but no corresponding
    ToolMessage responses. This causes errors when the conversation resumes.
    
    This middleware automatically detects such dangling tool calls and adds
    appropriate ToolMessages to complete the execution chain.
    
    Example:
        ```python
        from azcore.middleware import PatchToolCallsMiddleware
        from azcore.agents import AgentFactory
        
        middleware = PatchToolCallsMiddleware()
        agent = AgentFactory.create_agent(name="robust_agent")
        middleware.setup(agent)
        
        # Agent now handles interrupted tool calls gracefully
        ```
    
    Use Cases:
        - Human-in-the-loop workflows where tools may be rejected
        - Error recovery scenarios
        - Checkpointing/restoration flows
        - Any situation where tool execution may be interrupted
    
    Attributes:
        cancel_message_template: Template for cancellation messages
    """
    
    def __init__(self, cancel_message_template: Optional[str] = None):
        """
        Initialize patch tool calls middleware.
        
        Args:
            cancel_message_template: Template for cancellation message.
                Available placeholders: {tool_name}, {tool_id}
                Default: "Tool call {tool_name} with id {tool_id} was cancelled..."
        """
        self.cancel_message_template = cancel_message_template or (
            "Tool call {tool_name} with id {tool_id} was cancelled - "
            "another message came in before it could be completed."
        )
        self.agent = None
        self._patches_applied = 0
        
    def setup(self, agent: Any) -> None:
        """
        Setup middleware on an agent.
        
        Args:
            agent: The agent to add patch functionality to
        """
        self.agent = agent
        logger.info(f"PatchToolCalls middleware configured for {agent.name}")
    
    def _has_tool_response(
        self,
        messages: List[Any],
        tool_call_id: str,
        start_index: int
    ) -> bool:
        """
        Check if a tool call has a corresponding ToolMessage response.
        
        Args:
            messages: List of messages to search
            tool_call_id: The tool call ID to look for
            start_index: Index to start searching from
            
        Returns:
            True if a ToolMessage with matching tool_call_id exists
        """
        for msg in messages[start_index:]:
            # Check if it's a tool message with matching ID
            if hasattr(msg, 'type') and msg.type == "tool":
                if hasattr(msg, 'tool_call_id') and msg.tool_call_id == tool_call_id:
                    return True
            # Also check dict-like access
            elif isinstance(msg, dict):
                if msg.get('type') == "tool" and msg.get('tool_call_id') == tool_call_id:
                    return True
        return False
    
    def _create_tool_message(self, tool_call: Dict[str, Any]) -> Any:
        """
        Create a ToolMessage for a cancelled tool call.
        
        Args:
            tool_call: The tool call dictionary
            
        Returns:
            ToolMessage instance
        """
        tool_name = tool_call.get('name', 'unknown')
        tool_id = tool_call.get('id', 'unknown')
        
        # Format cancellation message
        content = self.cancel_message_template.format(
            tool_name=tool_name,
            tool_id=tool_id
        )
        
        # Try to import ToolMessage from langchain
        try:
            from langchain_core.messages import ToolMessage
            return ToolMessage(
                content=content,
                name=tool_name,
                tool_call_id=tool_id
            )
        except ImportError:
            # Fallback: create a dict-based message
            logger.warning("langchain_core not available, using dict-based ToolMessage")
            return {
                'type': 'tool',
                'content': content,
                'name': tool_name,
                'tool_call_id': tool_id
            }
    
    def patch_messages(self, messages: List[Any]) -> List[Any]:
        """
        Patch message history by adding ToolMessages for dangling tool calls.
        
        Args:
            messages: Original message history
            
        Returns:
            Patched message history with completed tool execution chains
        """
        if not messages or len(messages) == 0:
            return messages
        
        patched_messages = []
        patches_in_batch = 0
        
        # Iterate through messages
        for i, msg in enumerate(messages):
            # Add the original message
            patched_messages.append(msg)
            
            # Check if this is an AI message with tool calls
            is_ai_msg = False
            tool_calls = None
            
            # Try attribute access
            if hasattr(msg, 'type') and hasattr(msg, 'tool_calls'):
                is_ai_msg = msg.type == "ai"
                tool_calls = msg.tool_calls
            # Try dict access
            elif isinstance(msg, dict):
                is_ai_msg = msg.get('type') == "ai"
                tool_calls = msg.get('tool_calls')
            
            # If AI message with tool calls, check for dangling calls
            if is_ai_msg and tool_calls:
                for tool_call in tool_calls:
                    # Get tool call ID
                    tool_call_id = tool_call.get('id')
                    if not tool_call_id:
                        continue
                    
                    # Check if there's a corresponding ToolMessage
                    if not self._has_tool_response(messages, tool_call_id, i):
                        # Dangling tool call found - add cancellation message
                        tool_msg = self._create_tool_message(tool_call)
                        patched_messages.append(tool_msg)
                        patches_in_batch += 1
                        
                        logger.debug(
                            f"Added cancellation message for tool call "
                            f"{tool_call.get('name')} (id: {tool_call_id})"
                        )
        
        if patches_in_batch > 0:
            self._patches_applied += patches_in_batch
            logger.info(f"Patched {patches_in_batch} dangling tool calls")
        
        return patched_messages
    
    def before_agent(self, state: Dict[str, Any], runtime: Runtime) -> Optional[Dict[str, Any]]:
        """
        Hook called before agent execution.
        
        Scans message history and patches any dangling tool calls.
        
        Args:
            state: Current agent state
            runtime: Runtime context
            
        Returns:
            Updated state with patched messages, or None if no changes
        """
        messages = state.get("messages", [])
        
        if not messages:
            return None
        
        # Patch the messages
        patched_messages = self.patch_messages(messages)
        
        # Only return update if we actually patched something
        if len(patched_messages) > len(messages):
            return {"messages": patched_messages}
        
        return None
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get patching statistics.
        
        Returns:
            Dictionary with patch statistics
        """
        return {
            "total_patches_applied": self._patches_applied
        }


# Export
__all__ = ["PatchToolCallsMiddleware"]
