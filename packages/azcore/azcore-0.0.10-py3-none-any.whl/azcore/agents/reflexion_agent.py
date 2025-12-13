"""
Reflexion Agent Pattern for Azcore.

An advanced agent that implements the Reflexion framework to improve through self-reflection.
The agent follows a process of:
1. Acting on tasks
2. Evaluating its performance
3. Generating self-reflections
4. Using these reflections to improve future responses

This implementation integrates with the Azcore.'s existing architecture and patterns.
"""

from typing import List, Dict, Any, Tuple, Optional
import time
from datetime import datetime
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
        return msg.get("role") == "user"
    return False


def _is_assistant_message(msg: Any) -> bool:
    """Check if message is from assistant (handles both LangChain messages and dicts)."""
    if isinstance(msg, AIMessage):
        return True
    elif isinstance(msg, dict):
        return _is_assistant_message(msg)
    return False


# Define Reflexion prompt with detailed instructions
REFLEXION_PROMPT = """
You are Reflexion, an advanced AI assistant designed to generate high-quality responses and continuously improve through self-reflection.

CAPABILITIES:
- Deep reasoning: Break down complex problems step-by-step
- Self-evaluation: Critically assess your own responses
- Self-reflection: Generate insights about your performance and areas for improvement
- Memory utilization: Learn from past experiences and build upon previous knowledge

PROCESS:
1. UNDERSTAND the user's query thoroughly
2. GENERATE a detailed, thoughtful response
3. EVALUATE your response against these criteria:
   - Accuracy: Is all information factually correct?
   - Completeness: Does it address all aspects of the query?
   - Clarity: Is it well-structured and easy to understand?
   - Relevance: Does it focus on what the user needs?
   - Actionability: Does it provide practical, implementable solutions?
4. REFLECT on your performance and identify improvements
5. REFINE your response based on self-reflection

KEY PRINCIPLES:
- Be thorough but concise
- Prioritize practical, actionable advice
- Maintain awareness of your limitations
- Be transparent about uncertainty
- Learn continuously from each interaction

Always maintain your role as a helpful assistant focused on providing valuable information and solutions.
"""

EVALUATOR_PROMPT = """You are an expert evaluator of text quality. 
Your job is to thoroughly assess responses against these criteria:
1. Accuracy: Is all information factually correct?
2. Completeness: Does it address all aspects of the query?
3. Clarity: Is it well-structured and easy to understand?
4. Relevance: Does it focus on what the user needs?
5. Actionability: Does it provide practical, implementable solutions?

For each criterion, provide:
- A score from 1-10
- Specific examples of what was done well or poorly
- Concrete suggestions for improvement

Be precise, objective, and constructive in your criticism. 
Your goal is to help improve responses, not just criticize them.
End with an overall assessment and a final score from 1-10.
"""

REFLECTOR_PROMPT = """You are an expert at generating insightful self-reflections.

Given a task, a response to that task, and an evaluation of that response, your job is to create a thoughtful self-reflection that will help improve future responses to similar tasks.

Your reflection should:
1. Identify key strengths and weaknesses in the response
2. Analyze why certain approaches worked or didn't work
3. Extract general principles and lessons learned
4. Provide specific strategies for handling similar tasks better in the future
5. Be concrete and actionable, not vague or general

Focus on extracting lasting insights that will be valuable for improving future performance. Be honest about shortcomings while maintaining a constructive, improvement-oriented tone.
"""


class ReflexionMemory:
    """
    A memory system for the Reflexion agent to store past experiences, reflections, and feedback.

    Attributes:
        short_term_memory (List[Dict]): Recent interactions and their evaluations
        long_term_memory (List[Dict]): Persistent storage of important reflections and patterns
        memory_capacity (int): Maximum number of entries in long-term memory
    """

    def __init__(self, memory_capacity: int = 100):
        """
        Initialize the memory system.

        Args:
            memory_capacity (int): Maximum number of entries in long-term memory
        """
        self.short_term_memory = []
        self.long_term_memory = []
        self.memory_capacity = memory_capacity

    def add_short_term_memory(self, entry: Dict[str, Any]) -> None:
        """
        Add an entry to short-term memory.

        Args:
            entry (Dict[str, Any]): Memory entry containing task, response, evaluation, etc.
        """
        entry["timestamp"] = datetime.now().isoformat()
        self.short_term_memory.append(entry)

        # Keep only the most recent 10 entries in short-term memory
        if len(self.short_term_memory) > 10:
            self.short_term_memory.pop(0)

    def add_long_term_memory(self, entry: Dict[str, Any]) -> None:
        """
        Add an important entry to long-term memory.

        Args:
            entry (Dict[str, Any]): Memory entry containing task, response, evaluation, etc.
        """
        entry["timestamp"] = datetime.now().isoformat()

        # Check if similar entry exists to avoid duplication
        for existing in self.long_term_memory:
            if self._similarity(existing, entry) > 0.8:
                logger.debug("Similar entry already exists in long-term memory")
                return

        self.long_term_memory.append(entry)

        # If exceeded capacity, remove oldest entry
        if len(self.long_term_memory) > self.memory_capacity:
            self.long_term_memory.pop(0)

    def get_relevant_memories(
        self, task: str, limit: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Retrieve memories relevant to the current task.

        Args:
            task (str): The current task
            limit (int): Maximum number of memories to retrieve

        Returns:
            List[Dict[str, Any]]: Relevant memories
        """
        scored_memories = []

        # Score and combine memories from both short and long-term
        all_memories = self.short_term_memory + self.long_term_memory
        for memory in all_memories:
            relevance = self._calculate_relevance(memory, task)
            scored_memories.append((memory, relevance))

        # Sort by relevance score (descending)
        scored_memories.sort(key=lambda x: x[1], reverse=True)

        # Return the top 'limit' memories
        return [memory for memory, score in scored_memories[:limit]]

    def _calculate_relevance(
        self, memory: Dict[str, Any], task: str
    ) -> float:
        """
        Calculate relevance of a memory to the current task.

        Args:
            memory (Dict[str, Any]): The memory entry
            task (str): The current task

        Returns:
            float: Relevance score between 0 and 1
        """
        memory_task = memory.get("task", "")
        memory_reflection = memory.get("reflection", "")

        task_words = set(task.lower().split())
        memory_words = set(
            (memory_task + " " + memory_reflection).lower().split()
        )

        if not task_words or not memory_words:
            return 0.0

        intersection = task_words.intersection(memory_words)
        return len(intersection) / min(
            len(task_words), len(memory_words)
        )

    def _similarity(
        self, entry1: Dict[str, Any], entry2: Dict[str, Any]
    ) -> float:
        """
        Calculate similarity between two memory entries.

        Args:
            entry1 (Dict[str, Any]): First memory entry
            entry2 (Dict[str, Any]): Second memory entry

        Returns:
            float: Similarity score between 0 and 1
        """
        task1 = entry1.get("task", "")
        task2 = entry2.get("task", "")
        reflection1 = entry1.get("reflection", "")
        reflection2 = entry2.get("reflection", "")

        words1 = set((task1 + " " + reflection1).lower().split())
        words2 = set((task2 + " " + reflection2).lower().split())

        if not words1 or not words2:
            return 0.0

        intersection = words1.intersection(words2)
        return len(intersection) / (
            len(words1) + len(words2) - len(intersection)
        )


class ReflexionAgent(BaseAgent):
    """
    An advanced agent that implements the Reflexion framework to improve through self-reflection.

    The agent follows a process of:
    1. Acting on tasks
    2. Evaluating its performance
    3. Generating self-reflections
    4. Using these reflections to improve future responses

    Attributes:
        name (str): The name of the agent
        llm (BaseChatModel): The language model used
        max_loops (int): Maximum number of reflection iterations per task
        memory (ReflexionMemory): Memory system to store experiences and reflections
        actor (ReactAgent): The agent that generates initial responses
        evaluator (ReactAgent): The agent that evaluates responses
        reflector (ReactAgent): The agent that generates self-reflections
    """

    def __init__(
        self,
        name: str = "reflexion-agent",
        llm: BaseChatModel = None,
        tools: Optional[List[BaseTool]] = None,
        prompt: str = REFLEXION_PROMPT,
        description: str = "An agent that improves through self-reflection",
        max_loops: int = 3,
        memory_capacity: int = 100,
        rl_enabled: bool = False,
        rl_manager: Optional[Any] = None,
        reward_calculator: Optional[Any] = None,
        **kwargs,
    ) -> None:
        """
        Initializes the ReflexionAgent with specified parameters.

        Args:
            name (str): The name of the agent
            llm (BaseChatModel): The language model to use
            tools (Optional[List[BaseTool]]): Optional list of tools
            prompt (str): The system prompt for the agent
            description (str): Description of the agent
            max_loops (int): Maximum number of reflection iterations per task
            memory_capacity (int): Maximum capacity of long-term memory
        """
        super().__init__(
            name=name,
            llm=llm,
            tools=tools,
            prompt=prompt,
            description=description,
        )
        
        self.max_loops = max_loops
        self.memory = ReflexionMemory(memory_capacity=memory_capacity)
        self.rl_enabled = rl_enabled
        self.rl_manager = rl_manager
        self.reward_calculator = reward_calculator

        # Actor agent - generates initial responses with RL
        self.actor = ReactAgent(
            name=f"{name}-actor",
            llm=llm,
            tools=tools or [],
            prompt=prompt,
            rl_enabled=rl_enabled,
            rl_manager=rl_manager,
            reward_calculator=reward_calculator,
        )

        # Evaluator agent - evaluates responses (no tools/RL needed)
        self.evaluator = ReactAgent(
            name=f"{name}-evaluator",
            llm=llm,
            tools=[],
            prompt=EVALUATOR_PROMPT,
        )

        # Reflector agent - generates self-reflections (no tools/RL needed)
        self.reflector = ReactAgent(
            name=f"{name}-reflector",
            llm=llm,
            tools=[],
            prompt=REFLECTOR_PROMPT,
        )

        logger.info(f"Initialized {name} with max_loops={max_loops}")

    def act(
        self,
        task: str,
        relevant_memories: List[Dict[str, Any]] = None,
    ) -> str:
        """
        Generate a response to the given task using the actor agent.

        Args:
            task (str): The task to respond to
            relevant_memories (List[Dict[str, Any]]): Relevant past memories to consider

        Returns:
            str: The generated response
        """
        # Construct prompt with relevant memories if available
        prompt = task
        if relevant_memories and len(relevant_memories) > 0:
            memories_text = "\n\n".join(
                [
                    f"PAST REFLECTION: {memory.get('reflection', 'No reflection available')}"
                    for memory in relevant_memories
                ]
            )
            prompt = f"""TASK: {task}

RELEVANT PAST REFLECTIONS:
{memories_text}

Based on the task and relevant past reflections, provide a comprehensive response."""

        logger.debug(f"Actor generating response for task: {task[:100]}...")

        # Generate response
        start_time = time.time()
        state = {"messages": [{"role": "user", "content": prompt}]}
        result = self.actor.invoke(state)
        end_time = time.time()

        logger.debug(f"Actor generated response in {end_time - start_time:.2f}s")

        # Extract response
        response = ""
        if "messages" in result:
            for msg in reversed(result["messages"]):
                if _is_assistant_message(msg):
                    response = _extract_content(msg)
                    break

        return response

    def evaluate(self, task: str, response: str) -> Tuple[str, float]:
        """
        Evaluate the quality of a response to a task.

        Args:
            task (str): The original task
            response (str): The response to evaluate

        Returns:
            Tuple[str, float]: Evaluation feedback and numerical score
        """
        prompt = f"""TASK: {task}

RESPONSE:
{response}

Evaluate this response thoroughly according to the criteria in your instructions. Be specific and constructive."""

        logger.debug(f"Evaluating response for task: {task[:100]}...")

        state = {"messages": [{"role": "user", "content": prompt}]}
        result = self.evaluator.invoke(state)

        # Extract evaluation
        evaluation = ""
        if "messages" in result:
            for msg in reversed(result["messages"]):
                if _is_assistant_message(msg):
                    evaluation = _extract_content(msg)
                    break

        # Extract numerical score
        try:
            import re
            score_matches = re.findall(
                r"(?:final|overall)\s+score:?\s*(\d+(?:\.\d+)?)",
                evaluation.lower(),
            )
            score = float(score_matches[-1]) if score_matches else 5.0
            normalized_score = score / 10.0
        except Exception as e:
            logger.error(f"Failed to extract score: {e}")
            normalized_score = 0.5

        logger.debug(f"Evaluation complete. Score: {normalized_score:.2f}")

        return evaluation, normalized_score

    def reflect(
        self, task: str, response: str, evaluation: str
    ) -> str:
        """
        Generate a self-reflection based on the task, response, and evaluation.

        Args:
            task (str): The original task
            response (str): The generated response
            evaluation (str): The evaluation feedback

        Returns:
            str: The self-reflection
        """
        prompt = f"""TASK: {task}

RESPONSE:
{response}

EVALUATION:
{evaluation}

Based on this task, response, and evaluation, generate a thoughtful self-reflection that identifies key lessons and strategies for improving future responses to similar tasks."""

        logger.debug(f"Generating reflection for task: {task[:100]}...")

        state = {"messages": [{"role": "user", "content": prompt}]}
        result = self.reflector.invoke(state)

        # Extract reflection
        reflection = ""
        if "messages" in result:
            for msg in reversed(result["messages"]):
                if _is_assistant_message(msg):
                    reflection = _extract_content(msg)
                    break

        logger.debug(f"Reflection generated: {reflection[:100]}...")

        return reflection

    def refine(
        self,
        task: str,
        original_response: str,
        evaluation: str,
        reflection: str,
    ) -> str:
        """
        Refine the original response based on evaluation and reflection.

        Args:
            task (str): The original task
            original_response (str): The original response
            evaluation (str): The evaluation feedback
            reflection (str): The self-reflection

        Returns:
            str: The refined response
        """
        prompt = f"""TASK: {task}

ORIGINAL RESPONSE:
{original_response}

EVALUATION:
{evaluation}

REFLECTION:
{reflection}

Based on the original response, evaluation, and reflection, provide an improved response to the task. Focus on addressing the weaknesses identified while maintaining the strengths."""

        logger.debug(f"Refining response for task: {task[:100]}...")

        state = {"messages": [{"role": "user", "content": prompt}]}
        result = self.actor.invoke(state)

        # Extract refined response
        refined_response = ""
        if "messages" in result:
            for msg in reversed(result["messages"]):
                if _is_assistant_message(msg):
                    refined_response = _extract_content(msg)
                    break

        logger.debug(f"Response refined: {refined_response[:100]}...")

        return refined_response

    def invoke(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the Reflexion process on the provided task.

        Args:
            state (Dict[str, Any]): Current workflow state containing messages

        Returns:
            Dict[str, Any]: Updated state with final response and metadata
        """
        # Extract task from state
        task = ""
        if "messages" in state:
            for msg in state["messages"]:
                if _is_user_message(msg):
                    task = _extract_content(msg)
                    break

        logger.info(f"Starting Reflexion process for task: {task[:100]}...")

        best_response = None
        best_score = -1
        iterations = []

        for iteration in range(self.max_loops):
            logger.debug(f"Starting iteration {iteration+1}/{self.max_loops}")

            # Retrieve relevant memories
            relevant_memories = []
            if iteration > 0:
                relevant_memories = self.memory.get_relevant_memories(task)
                logger.debug(f"Retrieved {len(relevant_memories)} relevant memories")

            # Generate or refine response
            if iteration == 0:
                response = self.act(task, relevant_memories)
            else:
                prev_result = iterations[-1]
                response = self.refine(
                    task,
                    prev_result["response"],
                    prev_result["evaluation"],
                    prev_result["reflection"],
                )

            # Evaluate and reflect
            evaluation, score = self.evaluate(task, response)
            reflection = self.reflect(task, response, evaluation)

            # Store in memory
            memory_entry = {
                "task": task,
                "response": response,
                "evaluation": evaluation,
                "reflection": reflection,
                "score": score,
                "iteration": iteration,
            }

            self.memory.add_short_term_memory(memory_entry)

            # Add high-quality reflections to long-term memory
            if score > 0.8 or iteration == self.max_loops - 1:
                self.memory.add_long_term_memory(memory_entry)

            iterations.append(memory_entry)

            # Track best response
            if score > best_score:
                best_response = response
                best_score = score

            # Early stopping if score is very high
            if score > 0.9:
                logger.debug(f"Score {score} exceeds threshold. Stopping early.")
                break

        logger.info(f"Reflexion process complete. Best score: {best_score:.2f}")

        # Return updated state
        return {
            **state,
            "messages": state.get("messages", []) + [
                {"role": "assistant", "content": best_response}
            ],
            "iterations": iterations,
            "best_score": best_score,
        }

    async def ainvoke(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Asynchronously execute the Reflexion process.

        Args:
            state (Dict[str, Any]): Current workflow state

        Returns:
            Dict[str, Any]: Updated state
        """
        # For now, delegate to sync version
        return self.invoke(state)
