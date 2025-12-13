"""
Group Chat for Azcore.

Conversational agent collaboration with turn-based communication.
Agents make decisions through a conversational interface.

Use Cases:
- Real-time collaborative decision-making
- Negotiations and consensus building
- Brainstorming sessions
- Multi-agent discussions
"""

import logging
from typing import List, Dict, Any, Optional, Callable, Union
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from langchain_core.language_models.chat_models import BaseChatModel
from azcore.core.base import BaseAgent
from azcore.exceptions import ValidationError

logger = logging.getLogger(__name__)


class GroupChat:
    """
    Conversational multi-agent collaboration workflow.
    
    Agents take turns communicating in a group chat format. A speaker
    selection mechanism determines which agent speaks next based on
    conversation context.
    
    Attributes:
        name (str): Chat group identifier
        agents (List): List of participating agents
        max_rounds (int): Maximum conversation rounds
        speaker_selection_mode (str): How to select next speaker
    
    Example:
        >>> from azcore.workflows import GroupChat
        >>> 
        >>> # Create agents with different roles
        >>> researcher = ReactAgent(name="Researcher", llm=llm, 
        ...     prompt="You are a research specialist")
        >>> analyst = ReactAgent(name="Analyst", llm=llm,
        ...     prompt="You are a data analyst")
        >>> writer = ReactAgent(name="Writer", llm=llm,
        ...     prompt="You are a content writer")
        >>> 
        >>> # Create group chat
        >>> chat = GroupChat(
        ...     name="ProjectDiscussion",
        ...     agents=[researcher, analyst, writer],
        ...     max_rounds=10,
        ...     speaker_selection_mode="auto"
        ... )
        >>> 
        >>> # Start discussion
        >>> result = chat.run("Let's discuss the AI market report")
        >>> print(result['conversation_history'])
    """
    
    def __init__(
        self,
        name: str,
        agents: List[Union[BaseAgent, Callable]],
        max_rounds: int = 10,
        speaker_selection_mode: str = "auto",
        admin_agent: Optional[Union[BaseAgent, BaseChatModel]] = None,
        allow_repeat_speaker: bool = True,
        description: str = ""
    ):
        """
        Initialize GroupChat workflow.
        
        Args:
            name: Chat group identifier
            agents: List of participating agents
            max_rounds: Maximum conversation rounds (default: 10)
            speaker_selection_mode: Speaker selection method
                - "auto": Automatic based on context (default)
                - "round_robin": Take turns in order
                - "random": Random selection
                - "manual": Manual specification
            admin_agent: Optional admin agent for speaker selection
            allow_repeat_speaker: Allow same agent to speak consecutively
            description: Chat description
            
        Raises:
            ValidationError: If configuration is invalid
        """
        self.name = name
        self.agents = agents
        self.max_rounds = max_rounds
        self.speaker_selection_mode = speaker_selection_mode
        self.admin_agent = admin_agent
        self.allow_repeat_speaker = allow_repeat_speaker
        self.description = description or f"Group chat: {name}"
        
        self._conversation_history: List[Dict[str, Any]] = []
        self._current_round = 0
        self._last_speaker_idx: Optional[int] = None
        
        self._logger = logging.getLogger(f"{self.__class__.__name__}.{name}")
        
        # Validation
        self._validate()
        
        self._logger.info(
            f"GroupChat '{name}' initialized with {len(agents)} agents "
            f"(max_rounds={max_rounds}, mode={speaker_selection_mode})"
        )
    
    def _validate(self):
        """Validate chat configuration."""
        if not self.agents:
            raise ValidationError("GroupChat requires at least one agent")
        
        if len(self.agents) < 2:
            self._logger.warning("GroupChat works best with 2+ agents")
        
        if self.max_rounds < 1:
            raise ValidationError("max_rounds must be >= 1")
        
        valid_modes = ["auto", "round_robin", "random", "manual"]
        if self.speaker_selection_mode not in valid_modes:
            raise ValidationError(
                f"Invalid speaker_selection_mode '{self.speaker_selection_mode}'. "
                f"Must be one of: {valid_modes}"
            )
        
        # Validate agents
        for i, agent in enumerate(self.agents):
            if not (isinstance(agent, BaseAgent) or callable(agent)):
                raise ValidationError(
                    f"Agent at index {i} must be BaseAgent or callable"
                )
    
    def run(
        self,
        initial_message: Union[str, Dict[str, Any]],
        config: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Start and run the group chat.
        
        Args:
            initial_message: Initial message to start discussion
            config: Optional configuration
            
        Returns:
            Dict containing:
                - final_output: Summary or last message
                - conversation_history: Full conversation log
                - participants: List of participating agents
                - rounds_completed: Number of rounds completed
                - metadata: Chat metadata
        """
        self._logger.info(f"Starting GroupChat '{self.name}'")
        
        # Initialize conversation
        if isinstance(initial_message, str):
            self._conversation_history = [{
                "speaker": "User",
                "message": initial_message,
                "round": 0
            }]
            current_context = initial_message
        else:
            self._conversation_history = [initial_message]
            current_context = str(initial_message)
        
        # Run conversation rounds
        self._current_round = 0
        
        while self._current_round < self.max_rounds:
            self._current_round += 1
            self._logger.debug(f"Round {self._current_round}/{self.max_rounds}")
            
            # Select next speaker
            speaker_idx = self._select_next_speaker(current_context)
            
            if speaker_idx is None:
                self._logger.info("No more speakers available, ending chat")
                break
            
            agent = self.agents[speaker_idx]
            agent_name = getattr(agent, 'name', f'Agent_{speaker_idx}')
            
            self._logger.debug(f"Speaker: {agent_name}")
            
            # Prepare state with conversation history
            state = self._prepare_agent_state(current_context)
            
            # Get agent response
            try:
                if hasattr(agent, 'invoke'):
                    result = agent.invoke(state)
                else:
                    result = agent(state)
                
                # Extract message
                if isinstance(result, dict) and 'messages' in result:
                    message = self._extract_content(result['messages'][-1])
                else:
                    message = str(result)
                
                # Add to conversation history
                self._conversation_history.append({
                    "speaker": agent_name,
                    "message": message,
                    "round": self._current_round
                })
                
                current_context = message
                self._last_speaker_idx = speaker_idx
                
                self._logger.debug(f"{agent_name}: {message[:100]}...")
                
                # Check for termination conditions
                if self._should_terminate(message):
                    self._logger.info("Termination condition met")
                    break
                
            except Exception as e:
                self._logger.error(f"Error with agent {agent_name}: {e}")
                self._conversation_history.append({
                    "speaker": agent_name,
                    "message": f"[ERROR: {e}]",
                    "round": self._current_round
                })
                break
        
        # Generate final output
        final_output = self._generate_summary()
        
        result = {
            "final_output": final_output,
            "conversation_history": self._conversation_history,
            "participants": [getattr(a, 'name', f'Agent_{i}') for i, a in enumerate(self.agents)],
            "rounds_completed": self._current_round,
            "metadata": {
                "workflow": self.name,
                "total_agents": len(self.agents),
                "max_rounds": self.max_rounds,
                "speaker_mode": self.speaker_selection_mode
            }
        }
        
        self._logger.info(
            f"GroupChat '{self.name}' completed "
            f"({self._current_round} rounds, {len(self._conversation_history)} messages)"
        )
        
        return result
    
    def _select_next_speaker(self, context: str) -> Optional[int]:
        """Select the next speaker based on selection mode."""
        if self.speaker_selection_mode == "round_robin":
            return self._select_round_robin()
        
        elif self.speaker_selection_mode == "random":
            return self._select_random()
        
        elif self.speaker_selection_mode == "auto":
            return self._select_auto(context)
        
        elif self.speaker_selection_mode == "manual":
            # Manual mode requires external specification
            return self._last_speaker_idx or 0
        
        else:
            return 0
    
    def _select_round_robin(self) -> int:
        """Select next speaker in round-robin fashion."""
        if self._last_speaker_idx is None:
            return 0
        
        next_idx = (self._last_speaker_idx + 1) % len(self.agents)
        return next_idx
    
    def _select_random(self) -> int:
        """Select random speaker."""
        import random
        
        if not self.allow_repeat_speaker and self._last_speaker_idx is not None:
            # Exclude last speaker
            available = [i for i in range(len(self.agents)) if i != self._last_speaker_idx]
            if available:
                return random.choice(available)
        
        return random.randint(0, len(self.agents) - 1)
    
    def _select_auto(self, context: str) -> int:
        """Auto-select next speaker based on context."""
        # Simple heuristic: use admin agent if available, otherwise round-robin
        if self.admin_agent and isinstance(self.admin_agent, BaseChatModel):
            # Use LLM to select next speaker
            try:
                agent_names = [getattr(a, 'name', f'Agent_{i}') for i, a in enumerate(self.agents)]
                prompt = f"""Based on the conversation context, select the most appropriate next speaker.

Context: {context}

Available speakers: {', '.join(agent_names)}

Respond with just the speaker name, nothing else."""
                
                response = self.admin_agent.invoke([HumanMessage(content=prompt)])
                selected_name = response.content.strip()
                
                # Find agent by name
                for i, agent in enumerate(self.agents):
                    if getattr(agent, 'name', '') == selected_name:
                        return i
                
            except Exception as e:
                self._logger.debug(f"Auto-selection failed, using round-robin: {e}")
        
        # Fallback to round-robin
        return self._select_round_robin()
    
    def _prepare_agent_state(self, current_context: str) -> Dict[str, Any]:
        """Prepare state with conversation history for agent."""
        # Build message history
        messages = []
        
        # Add system context if first round
        if self._current_round == 1:
            system_msg = SystemMessage(content=f"You are participating in a group chat: {self.name}")
            messages.append(system_msg)
        
        # Add recent conversation history (last 5 messages)
        recent_history = self._conversation_history[-5:]
        for entry in recent_history:
            content = f"{entry['speaker']}: {entry['message']}"
            messages.append(HumanMessage(content=content))
        
        return {"messages": messages}
    
    def _should_terminate(self, message: str) -> bool:
        """Check if conversation should terminate."""
        # Termination keywords
        termination_keywords = [
            "TERMINATE",
            "END_CHAT",
            "CONVERSATION_COMPLETE",
            "[DONE]"
        ]
        
        message_upper = message.upper()
        return any(keyword in message_upper for keyword in termination_keywords)
    
    def _generate_summary(self) -> str:
        """Generate summary of the conversation."""
        if not self._conversation_history:
            return "No conversation occurred"
        
        # Return last message as final output
        last_entry = self._conversation_history[-1]
        return f"{last_entry['speaker']}: {last_entry['message']}"
    
    def add_agent(self, agent: Union[BaseAgent, Callable]) -> 'GroupChat':
        """
        Add an agent to the chat.
        
        Args:
            agent: Agent to add
            
        Returns:
            Self for method chaining
        """
        if not (isinstance(agent, BaseAgent) or callable(agent)):
            raise ValidationError("Agent must be BaseAgent or callable")
        
        self.agents.append(agent)
        self._logger.info(f"Added agent to chat (total: {len(self.agents)})")
        
        return self
    
    def get_conversation_summary(self) -> str:
        """
        Get a formatted summary of the conversation.
        
        Returns:
            Formatted conversation history
        """
        lines = [
            f"Group Chat: {self.name}",
            "=" * 60,
            ""
        ]
        
        for entry in self._conversation_history:
            round_info = f"[Round {entry.get('round', 0)}]"
            lines.append(f"{round_info} {entry['speaker']}:")
            lines.append(f"  {entry['message']}")
            lines.append("")
        
        lines.append("=" * 60)
        lines.append(f"Total rounds: {self._current_round}")
        lines.append(f"Total messages: {len(self._conversation_history)}")
        
        return "\n".join(lines)
    
    def _extract_content(self, message: Union[BaseMessage, Dict, str]) -> str:
        """Extract content from message."""
        if isinstance(message, str):
            return message
        if isinstance(message, dict):
            return message.get("content", str(message))
        return getattr(message, "content", str(message))
    
    def __repr__(self) -> str:
        """Return a string representation of the GroupChat object.

        The string representation includes the chat name, the number of agents, and the maximum number of rounds.

        Returns:
            str: A string representation of the GroupChat object.
        """
        return (
            f"GroupChat(name='{self.name}', "
            f"agents={len(self.agents)}, "
            f"max_rounds={self.max_rounds})"
        )
