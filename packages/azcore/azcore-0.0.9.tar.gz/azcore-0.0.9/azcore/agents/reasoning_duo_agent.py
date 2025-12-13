"""
Reasoning Duo Agent Pattern for Azcore.

A collaborative agent pattern that uses two agents working together:
1. A reasoning agent that analyzes and breaks down problems
2. A main agent that provides final answers

This pattern is based on the observation that explicit reasoning steps
improve the quality and accuracy of final outputs.
"""

from typing import Dict, Any, Optional, List
import logging

from azcore.agents.agent_factory import ReactAgent
from azcore.core.base import BaseAgent
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.tools import BaseTool
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage

logger = logging.getLogger(__name__)


def _extract_content(msg: Any) -> str:
    """Helper to extract content from message (handles both LangChain messages and dicts)."""
    if isinstance(msg, BaseMessage):
        return msg.content
    elif isinstance(msg, dict):
        return _extract_content(msg)
    return str(msg)


def _is_user_message(msg: Any) -> bool:
    """Check if message is from user (handles both LangChain messages and dicts)."""
    if isinstance(msg, HumanMessage):
        return True
    elif isinstance(msg, dict):
        return _is_user_message(msg)
    return False


def _is_assistant_message(msg: Any) -> bool:
    """Check if message is from assistant (handles both LangChain messages and dicts)."""
    if isinstance(msg, AIMessage):
        return True
    elif isinstance(msg, dict):
        return _is_assistant_message(msg)
    return False


REASONING_PROMPT = """You are an expert reasoning agent. Your job is to think deeply about the problem and provide comprehensive reasoning steps.

Follow this process:
1. **Understand**: Carefully read and understand the problem
2. **Analyze**: Break down the problem into components
3. **Reason**: Think through potential approaches and solutions
4. **Structure**: Organize your thoughts in a clear, logical manner
5. **Explain**: Articulate your reasoning process clearly

Provide detailed step-by-step reasoning that will help another agent provide an accurate final answer.
"""


class ReasoningDuoAgent(BaseAgent):
    """
    A collaborative agent that uses two agents working together for better results.

    The ReasoningDuoAgent consists of:
    - A reasoning agent that provides detailed analysis and reasoning
    - A main agent that synthesizes the reasoning into a final answer

    This pattern is particularly effective for complex problems that benefit from
    explicit reasoning steps.

    Example:
        >>> from langchain_openai import ChatOpenAI
        >>> from azcore.agents.reasoning_duo_agent import ReasoningDuoAgent
        >>> 
        >>> llm = ChatOpenAI(model="gpt-4o-mini")
        >>> agent = ReasoningDuoAgent(
        ...     name="reasoning-duo",
        ...     llm=llm,
        ... )
        >>> state = {"messages": [{"role": "user", "content": "Explain quantum entanglement"}]}
        >>> result = agent.invoke(state)
    """

    def __init__(
        self,
        name: str = "reasoning-duo-agent",
        llm: BaseChatModel = None,
        tools: Optional[List[BaseTool]] = None,
        prompt: str = "You are a helpful assistant that provides accurate and well-reasoned answers.",
        description: str = "A collaborative agent using reasoning and main agents",
        max_loops: int = 1,
        rl_enabled: bool = False,
        rl_manager: Optional[Any] = None,
        reward_calculator: Optional[Any] = None,
        **kwargs,
    ):
        """
        Initialize the ReasoningDuoAgent.

        Args:
            name (str): Name of the agent
            llm (BaseChatModel): Language model to use
            tools (Optional[List[BaseTool]]): Optional list of tools
            prompt (str): System prompt for the main agent
            description (str): Description of the agent
            max_loops (int): Maximum number of reasoning iterations
        """
        super().__init__(
            name=name,
            llm=llm,
            tools=tools,
            prompt=prompt,
            description=description,
        )
        
        self.max_loops = max_loops
        self.rl_enabled = rl_enabled
        self.rl_manager = rl_manager
        self.reward_calculator = reward_calculator

        # Reasoning agent - provides detailed reasoning (no tools/RL needed)
        self.reasoning_agent = ReactAgent(
            name=f"{name}-reasoner",
            llm=llm,
            tools=[],
            prompt=REASONING_PROMPT,
        )

        # Main agent - provides final answer with RL support
        self.main_agent = ReactAgent(
            name=f"{name}-main",
            llm=llm,
            tools=tools or [],
            prompt=prompt,
            rl_enabled=rl_enabled,
            rl_manager=rl_manager,
            reward_calculator=reward_calculator,
        )

        logger.info(f"Initialized {name} with max_loops={max_loops}")

    def invoke(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the reasoning duo process.

        Args:
            state (Dict[str, Any]): Current workflow state

        Returns:
            Dict[str, Any]: Updated state with final answer
        """
        # Extract task from state
        task = ""
        if "messages" in state:
            for msg in state["messages"]:
                if _is_user_message(msg):
                    task = _extract_content(msg)
                    break

        logger.info(f"Processing task with reasoning duo: {task[:100]}...")

        # Build conversation context
        conversation = []
        
        for loop in range(self.max_loops):
            logger.debug(f"Loop {loop+1}/{self.max_loops}")

            # Step 1: Reasoning agent analyzes the problem
            if loop == 0:
                reasoning_task = task
            else:
                reasoning_task = f"Continue reasoning about: {task}\n\nPrevious context:\n{self._format_conversation(conversation)}"

            reasoning_state = {"messages": [{"role": "user", "content": reasoning_task}]}
            reasoning_result = self.reasoning_agent.invoke(reasoning_state)

            # Extract reasoning
            reasoning = ""
            if "messages" in reasoning_result:
                for msg in reversed(reasoning_result["messages"]):
                    if _is_assistant_message(msg):
                        reasoning = _extract_content(msg)
                        break

            conversation.append({"role": "reasoner", "content": reasoning})

            # Step 2: Main agent synthesizes final answer
            main_task = f"Original task: {task}\n\nReasoning from analysis agent:\n{reasoning}\n\nProvide a clear, concise final answer based on this reasoning."
            main_state = {"messages": [{"role": "user", "content": main_task}]}
            main_result = self.main_agent.invoke(main_state)

            # Extract answer
            answer = ""
            if "messages" in main_result:
                for msg in reversed(main_result["messages"]):
                    if _is_assistant_message(msg):
                        answer = _extract_content(msg)
                        break

            conversation.append({"role": "main", "content": answer})

        logger.info("Reasoning duo process complete")

        # Return final state with last answer
        return {
            **state,
            "messages": state.get("messages", []) + [
                {"role": "assistant", "content": answer}
            ],
            "conversation": conversation,
        }

    async def ainvoke(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Asynchronously execute the reasoning duo process.

        Args:
            state (Dict[str, Any]): Current workflow state

        Returns:
            Dict[str, Any]: Updated state
        """
        return self.invoke(state)

    def _format_conversation(self, conversation: List[Dict[str, str]]) -> str:
        """Format conversation history as a string."""
        return "\n\n".join([
            f"{entry['role'].upper()}: {entry['content']}"
            for entry in conversation
        ])
