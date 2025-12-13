"""
Summarization Middleware for Azcore.

This middleware automatically manages conversation history by compressing older
messages when token limits are approached. It preserves recent messages and
system messages while summarizing the middle portion to save tokens.
"""

from typing import Any, Dict, List, Optional, Protocol, TypedDict, Literal
from ..utils.logging import get_logger

logger = get_logger(__name__)


class Message(TypedDict, total=False):
    """Message structure."""
    role: str
    content: str
    name: Optional[str]
    tool_calls: Optional[List[Dict[str, Any]]]
    tool_call_id: Optional[str]


class Runtime(Protocol):
    """Runtime protocol for middleware."""
    state: Dict[str, Any]


class SummarizationMiddleware:
    """
    Middleware that automatically summarizes conversation history.
    
    This middleware monitors conversation length and automatically compresses
    older messages when approaching token limits. It preserves:
    - System messages
    - Recent messages (configurable window)
    - Important context markers
    
    The middle portion of the conversation is summarized to save tokens while
    maintaining context continuity.
    
    Example:
        ```python
        from azcore.middleware import SummarizationMiddleware
        from azcore.agents import AgentFactory
        
        middleware = SummarizationMiddleware(
            max_messages=50,
            keep_recent=10,
            summarize_threshold=40
        )
        
        agent = AgentFactory.create_agent(name="assistant")
        middleware.setup(agent)
        
        # Agent's conversation history will be automatically managed
        ```
    
    Attributes:
        max_messages: Maximum messages before triggering summarization
        keep_recent: Number of recent messages to preserve
        summarize_threshold: Message count that triggers summarization
        summarizer_prompt: Custom prompt for summarization (optional)
    """
    
    def __init__(
        self,
        max_messages: int = 50,
        keep_recent: int = 10,
        summarize_threshold: int = 40,
        summarizer_prompt: Optional[str] = None
    ):
        """
        Initialize summarization middleware.
        
        Args:
            max_messages: Maximum messages in history before summarization
            keep_recent: Number of recent messages to always preserve
            summarize_threshold: Trigger summarization at this message count
            summarizer_prompt: Custom prompt for the summarizer (optional)
        """
        self.max_messages = max_messages
        self.keep_recent = keep_recent
        self.summarize_threshold = summarize_threshold
        self.summarizer_prompt = summarizer_prompt or self._default_summarizer_prompt()
        self.agent = None
        self._summarization_count = 0
        
    def _default_summarizer_prompt(self) -> str:
        """Get default summarization prompt."""
        return """You are a conversation summarizer. Your task is to create a concise 
summary of the provided conversation history that preserves:
1. Key decisions and conclusions
2. Important context and facts
3. Action items and outcomes
4. Critical information for future reference

Keep the summary brief but comprehensive. Format as a bulleted list."""
    
    def setup(self, agent: Any) -> None:
        """
        Setup middleware on an agent.
        
        Args:
            agent: The agent to add summarization to
        """
        self.agent = agent
        logger.info(f"Summarization middleware configured for {agent.name}")
        logger.info(f"  Max messages: {self.max_messages}")
        logger.info(f"  Keep recent: {self.keep_recent}")
        logger.info(f"  Threshold: {self.summarize_threshold}")
    
    def should_summarize(self, messages: List[Message]) -> bool:
        """
        Check if conversation should be summarized.
        
        Args:
            messages: Current conversation messages
            
        Returns:
            True if summarization should occur
        """
        # Count non-system messages
        user_messages = [m for m in messages if m.get("role") != "system"]
        return len(user_messages) >= self.summarize_threshold
    
    def _extract_system_messages(self, messages: List[Message]) -> List[Message]:
        """Extract system messages from conversation."""
        return [m for m in messages if m.get("role") == "system"]
    
    def _extract_recent_messages(self, messages: List[Message]) -> List[Message]:
        """Extract recent messages to preserve."""
        non_system = [m for m in messages if m.get("role") != "system"]
        return non_system[-self.keep_recent:] if len(non_system) > self.keep_recent else non_system
    
    def _extract_middle_messages(self, messages: List[Message]) -> List[Message]:
        """Extract middle messages to summarize."""
        non_system = [m for m in messages if m.get("role") != "system"]
        if len(non_system) <= self.keep_recent:
            return []
        return non_system[:-self.keep_recent]
    
    def _create_summary_message(self, summary: str) -> Message:
        """Create a summary message."""
        return Message(
            role="assistant",
            content=f"[CONVERSATION SUMMARY]\n\n{summary}\n\n[END SUMMARY]"
        )
    
    def _format_messages_for_summary(self, messages: List[Message]) -> str:
        """Format messages for summarization."""
        formatted = []
        for msg in messages:
            role = msg.get("role", "unknown")
            content = msg.get("content", "")
            
            # Handle tool calls
            if msg.get("tool_calls"):
                tool_names = [tc.get("function", {}).get("name", "unknown") 
                            for tc in msg.get("tool_calls", [])]
                content = f"[Called tools: {', '.join(tool_names)}]"
            
            # Handle tool responses
            if role == "tool":
                name = msg.get("name", "unknown")
                content = f"[Tool {name} response: {content[:100]}...]"
            
            formatted.append(f"{role.upper()}: {content}")
        
        return "\n\n".join(formatted)
    
    async def _generate_summary(self, messages: List[Message]) -> str:
        """
        Generate summary of messages.
        
        Args:
            messages: Messages to summarize
            
        Returns:
            Summary text
        """
        # Format messages for summarization
        conversation_text = self._format_messages_for_summary(messages)
        
        # Create summarization prompt
        prompt = f"{self.summarizer_prompt}\n\nConversation to summarize:\n\n{conversation_text}"
        
        try:
            # Use agent's LLM if available
            if hasattr(self.agent, 'llm') and self.agent.llm:
                response = await self.agent.llm.ainvoke(prompt)
                summary = response.content if hasattr(response, 'content') else str(response)
            else:
                # Fallback: create basic summary
                summary = self._create_basic_summary(messages)
            
            return summary
            
        except Exception as e:
            logger.warning(f"Failed to generate AI summary: {e}. Using basic summary.")
            return self._create_basic_summary(messages)
    
    def _create_basic_summary(self, messages: List[Message]) -> str:
        """Create a basic summary without AI."""
        summary_parts = [
            f"Summary of {len(messages)} messages:",
            ""
        ]
        
        # Count message types
        roles = {}
        for msg in messages:
            role = msg.get("role", "unknown")
            roles[role] = roles.get(role, 0) + 1
        
        summary_parts.append("Message breakdown:")
        for role, count in roles.items():
            summary_parts.append(f"  • {role}: {count} messages")
        
        # Extract key topics (simple keyword extraction)
        all_content = " ".join(m.get("content", "") for m in messages if m.get("content"))
        words = all_content.lower().split()
        
        # Simple word frequency (excluding common words)
        stop_words = {"the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", "of", "with", "by"}
        word_freq = {}
        for word in words:
            if len(word) > 3 and word not in stop_words:
                word_freq[word] = word_freq.get(word, 0) + 1
        
        top_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:5]
        if top_words:
            summary_parts.append("")
            summary_parts.append("Key topics mentioned:")
            for word, _ in top_words:
                summary_parts.append(f"  • {word}")
        
        return "\n".join(summary_parts)
    
    async def summarize_conversation(self, messages: List[Message]) -> List[Message]:
        """
        Summarize conversation history.
        
        Args:
            messages: Full conversation history
            
        Returns:
            Compressed conversation with summary
        """
        if not self.should_summarize(messages):
            return messages
        
        logger.info("Triggering conversation summarization...")
        
        # Extract different parts
        system_messages = self._extract_system_messages(messages)
        middle_messages = self._extract_middle_messages(messages)
        recent_messages = self._extract_recent_messages(messages)
        
        # Generate summary of middle messages
        if middle_messages:
            summary = await self._generate_summary(middle_messages)
            summary_message = self._create_summary_message(summary)
            self._summarization_count += 1
            
            logger.info(f"Summarized {len(middle_messages)} messages into 1 summary")
            logger.info(f"Kept {len(recent_messages)} recent messages")
            
            # Reconstruct conversation: system + summary + recent
            new_messages = system_messages + [summary_message] + recent_messages
            
            return new_messages
        
        return messages
    
    def wrap_model_call(self, runtime: Runtime, messages: List[Message]) -> List[Message]:
        """
        Wrap model call to potentially summarize before sending.
        
        This is called before each LLM invocation to check if conversation
        history should be compressed.
        
        Args:
            runtime: Current runtime context
            messages: Messages to send to model
            
        Returns:
            Potentially summarized messages
        """
        # Check if summarization needed (synchronous check)
        if self.should_summarize(messages):
            # Store flag to trigger async summarization
            runtime.state["_needs_summarization"] = True
        
        return messages
    
    async def wrap_model_call_async(self, runtime: Runtime, messages: List[Message]) -> List[Message]:
        """
        Async version of wrap_model_call with actual summarization.
        
        Args:
            runtime: Current runtime context
            messages: Messages to send to model
            
        Returns:
            Summarized messages
        """
        if self.should_summarize(messages):
            messages = await self.summarize_conversation(messages)
            runtime.state["_needs_summarization"] = False
        
        return messages
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get summarization statistics.
        
        Returns:
            Dictionary with summarization stats
        """
        return {
            "summarization_count": self._summarization_count,
            "max_messages": self.max_messages,
            "keep_recent": self.keep_recent,
            "threshold": self.summarize_threshold
        }


# Export
__all__ = ["SummarizationMiddleware"]
