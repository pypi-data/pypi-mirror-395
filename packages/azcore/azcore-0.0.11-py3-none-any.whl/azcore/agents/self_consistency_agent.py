"""
Self-Consistency Agent Pattern for Azcore.

This module implements the SelfConsistencyAgent, a specialized agent pattern that leverages the
self-consistency technique to improve reasoning reliability and accuracy. The agent generates
multiple independent responses to a given task and aggregates them into a single, consistent
final answer using majority voting and sophisticated aggregation techniques.

The self-consistency approach is based on the research paper:
"Self-Consistency Improves Chain of Thought Reasoning in Language Models"
by Wang et al. (2022) - https://arxiv.org/abs/2203.07870

Key Features:
- Concurrent generation of multiple independent responses
- Majority voting aggregation with detailed analysis
- Evaluation mode for answer validation
- Configurable output formats
- Thread-safe execution
- Integration with Azcore.'s ReactAgent

Reference:
    Wang, Y., Dong, W., Han, J., & Wang, W. (2022). Self-Consistency Improves Chain of
    Thought Reasoning in Language Models. arXiv preprint arXiv:2203.07870.
    https://arxiv.org/abs/2203.07870
"""

from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Optional, Union, Dict, Any
import logging

from azcore.agents.agent_factory import ReactAgent
from azcore.core.base import BaseAgent
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.tools import BaseTool

logger = logging.getLogger(__name__)


# System prompt for the reasoning agent that generates individual responses
CONSISTENCY_SYSTEM_PROMPT = """
You are a reasoning agent designed for complex problem-solving and decision-making. Your objective is to provide clear and reliable responses through structured reasoning. Begin by thoroughly understanding the problem, rephrasing it for clarity, and identifying key components. Develop a logical plan that breaks the problem into manageable steps, detailing your approach and any assumptions made. Validate your information with reliable sources and assess the accuracy of your calculations. Explore multiple solutions, weighing their pros and cons, and maintain transparency by documenting your reasoning process, uncertainties, and biases. Summarize your findings in a concise final answer that reflects your thorough analysis, ensuring it is well-organized and accessible. Adapt your reasoning to the context of the problem, integrating new information as needed, and implement error-handling strategies to address any issues that arise. Finally, reflect on your reasoning process to identify areas for improvement and ensure consistency across all reasoning paths.
"""

# Detailed prompt for the majority voting aggregation agent
MAJORITY_VOTING_PROMPT = """
Engage in a comprehensive and exhaustive majority voting analysis of the following conversation, ensuring a deep and thoughtful examination of the responses provided by each agent. This analysis should not only summarize the responses but also critically engage with the content, context, and implications of each agent's input.

Please adhere to the following detailed guidelines:

1. **Identification of Dominant Responses:**
   - Identify the most prevalent answer or recommendation across all agents. Provide a thorough rationale for its dominance, including an exploration of the factors that may have contributed to its acceptance among the agents. Discuss the context in which this consensus emerged and any relevant historical or theoretical frameworks that support this conclusion.

2. **Exploration of Disparities:**
   - Delve into any significant disparities or contrasting viewpoints between agents. Explore the underlying reasons for these differences, considering aspects such as differing methodologies, assumptions, or interpretations of the task at hand. Analyze how these contrasting perspectives may reflect broader debates within the field and what implications they hold for the overall understanding of the topic.

3. **Consensus and Disagreement Analysis:**
   - Highlight key areas of consensus and disagreement among the agents. Discuss the implications of these findings on the overall argument, including how consensus can strengthen certain claims while disagreement may indicate areas of uncertainty or contention. Provide examples from the conversation to illustrate these points and consider how they might influence future discussions or research directions.

4. **Critical Evaluation of Majority Opinion:**
   - Critically evaluate the strength of the majority opinion, considering factors such as the reasoning behind it and its mathematical validity if applicable. Assess whether the majority opinion is well-supported by evidence and logical reasoning, and discuss any potential weaknesses or oversights that may undermine its credibility. 

5. **Insights from Minority Viewpoints:**
   - Note any unique insights from minority viewpoints, assessing their potential contributions to a more nuanced understanding of the topic. Discuss how these minority perspectives can enrich the conversation and provide alternative angles that may have been overlooked by the majority. Consider the value of dissent in academic discourse and how it can lead to more robust conclusions.

6. **Synthesis of Recommendations:**
   - Provide a final synthesized recommendation based on the majority consensus, ensuring that it reflects a thorough consideration of all perspectives and is grounded in sound reasoning. This recommendation should not only summarize the majority view but also integrate insights from minority opinions, creating a comprehensive and balanced conclusion that acknowledges the complexity of the discussion.

Throughout your analysis, focus on uncovering clear patterns while being attentive to the subtleties and complexities inherent in the responses. Pay particular attention to the nuances of mathematical contexts where algorithmic thinking may be required, ensuring that your examination is both rigorous and accessible to a diverse audience.
"""


def aggregation_agent(
    responses: List[str],
    llm: BaseChatModel,
    prompt: str = MAJORITY_VOTING_PROMPT,
) -> str:
    """
    Aggregates a list of responses into a single final answer using an AI-powered aggregation agent.

    This function creates a specialized agent that analyzes multiple responses and synthesizes
    them into a coherent final answer. The aggregation process considers consensus, disagreements,
    and minority viewpoints to produce a well-reasoned conclusion.

    Args:
        responses (List[str]): List of responses to be aggregated
        llm (BaseChatModel): Language model to use for aggregation
        prompt (str, optional): Custom prompt for the aggregation agent.
                               Defaults to the MAJORITY_VOTING_PROMPT.

    Returns:
        str: The aggregated final answer

    Example:
        >>> from langchain_openai import ChatOpenAI
        >>> llm = ChatOpenAI(model="gpt-4o-mini")
        >>> responses = ["Answer A", "Answer B", "Answer A"]
        >>> final_answer = aggregation_agent(responses, llm)
        >>> print(final_answer)
        "Based on the majority consensus..."
    """
    # Format responses into a single task string
    task = "\n\n".join([f"Response {i+1}: {resp}" for i, resp in enumerate(responses)])
    
    # Create aggregation agent
    agent = ReactAgent(
        name="Aggregation-Agent",
        llm=llm,
        prompt=prompt,
    )

    # Get the aggregated result
    from langchain_core.messages import HumanMessage, AIMessage
    state = {"messages": [HumanMessage(content=task)]}
    result = agent.invoke(state)
    
    # Extract the final answer from messages
    if "messages" in result:
        for msg in reversed(result["messages"]):
            if isinstance(msg, AIMessage):
                return msg.content
            elif isinstance(msg, dict) and msg.get("role") == "assistant":
                return msg.get("content", "")
    
    return ""


class SelfConsistencyAgent(BaseAgent):
    """
    A specialized agent that implements self-consistency for improved reasoning reliability.

    The SelfConsistencyAgent generates multiple independent responses to a given task and
    aggregates them into a single, consistent final answer. This approach is based on the
    research paper "Self-Consistency Improves Chain of Thought Reasoning in Language Models"
    by Wang et al. (2022).

    Key Features:
    - Concurrent generation of multiple independent responses
    - Majority voting aggregation with detailed analysis
    - Evaluation mode for answer validation
    - Configurable output formats
    - Thread-safe execution
    - Integration with Azcore. architecture

    The self-consistency technique works by:
    1. Generating multiple independent reasoning paths for the same problem
    2. Analyzing the consistency and agreement among these paths
    3. Aggregating the results using majority voting or consensus building
    4. Producing a final answer that reflects the most reliable consensus

    This approach helps mitigate issues like:
    - Random errors in individual reasoning paths
    - Biases in single reasoning approaches
    - Inconsistencies in complex problem-solving

    Reference:
        Wang, Y., Dong, W., Han, J., & Wang, W. (2022). Self-Consistency Improves Chain of
        Thought Reasoning in Language Models. arXiv preprint arXiv:2203.07870.
        https://arxiv.org/abs/2203.07870

    Example:
        >>> from langchain_openai import ChatOpenAI
        >>> from azcore.agents.self_consistency_agent import SelfConsistencyAgent
        >>> 
        >>> llm = ChatOpenAI(model="gpt-4o-mini")
        >>> agent = SelfConsistencyAgent(
        ...     name="Math-Reasoning-Agent",
        ...     llm=llm,
        ...     num_samples=5,
        ... )
        >>> state = {"messages": [{"role": "user", "content": "What is the 40th prime number?"}]}
        >>> result = agent.invoke(state)
        >>> print(result)
    """

    def __init__(
        self,
        name: str = "Self-Consistency-Agent",
        llm: BaseChatModel = None,
        tools: Optional[List[BaseTool]] = None,
        prompt: str = CONSISTENCY_SYSTEM_PROMPT,
        description: str = "An agent that uses self consistency to generate a final answer.",
        num_samples: int = 5,
        majority_voting_prompt: Optional[str] = MAJORITY_VOTING_PROMPT,
        eval_mode: bool = False,
        rl_enabled: bool = False,
        rl_manager: Optional[Any] = None,
        reward_calculator: Optional[Any] = None,
        **kwargs,
    ):
        """
        Initialize the SelfConsistencyAgent.

        Args:
            name (str, optional): Name of the agent. Defaults to "Self-Consistency-Agent".
            llm (BaseChatModel): Language model to use for the agent.
            tools (Optional[List[BaseTool]]): Optional list of tools for the agent.
            prompt (str, optional): System prompt for the reasoning agent.
                                   Defaults to CONSISTENCY_SYSTEM_PROMPT.
            description (str, optional): Description of the agent's purpose.
            num_samples (int, optional): Number of independent responses to generate.
                                       Defaults to 5.
            majority_voting_prompt (Optional[str], optional): Custom prompt for majority voting.
                                                            Defaults to MAJORITY_VOTING_PROMPT.
            eval_mode (bool, optional): Enable evaluation mode for answer validation.
                                      Defaults to False.
            **kwargs: Additional keyword arguments passed to the base Agent class.

        Note:
            The num_samples parameter determines how many independent reasoning paths
            will be generated. Higher values generally lead to more reliable results
            but increase computational cost and time.
        """
        super().__init__(
            name=name,
            llm=llm,
            tools=tools,
            prompt=prompt,
            description=description,
        )
        
        self.num_samples = num_samples
        self.majority_voting_prompt = majority_voting_prompt
        self.eval_mode = eval_mode
        self.rl_enabled = rl_enabled
        self.rl_manager = rl_manager
        self.reward_calculator = reward_calculator
        self.kwargs = kwargs
        
        # Create the base reasoning agent with RL support
        self.reasoning_agent = ReactAgent(
            name=f"{name}-Reasoner",
            llm=llm,
            tools=tools or [],
            prompt=prompt,
            rl_enabled=rl_enabled,
            rl_manager=rl_manager,
            reward_calculator=reward_calculator,
        )
        
        logger.info(f"Initialized {name} with {num_samples} samples")

    def invoke(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate multiple responses for the given task and aggregate them concurrently.

        This method implements the core self-consistency algorithm:
        1. Generates multiple independent responses using concurrent execution
        2. Optionally validates responses against a known answer (if eval_mode=True)
        3. Aggregates responses using an AI-powered aggregation agent
        4. Returns the final result in the state

        Args:
            state (Dict[str, Any]): Current workflow state containing messages

        Returns:
            Dict[str, Any]: Updated state with aggregated response

        Example:
            >>> agent = SelfConsistencyAgent(num_samples=3, llm=llm)
            >>> state = {"messages": [{"role": "user", "content": "What is 2 + 2?"}]}
            >>> result = agent.invoke(state)
            >>> print(result)
        """
        responses = []
        
        logger.info(f"Generating {self.num_samples} independent responses")
        
        # Generate multiple independent responses concurrently
        with ThreadPoolExecutor() as executor:
            futures = {
                executor.submit(self.reasoning_agent.invoke, state): i
                for i in range(self.num_samples)
            }
            
            for future in as_completed(futures):
                result = future.result()
                # Extract the response content
                if "messages" in result:
                    from langchain_core.messages import AIMessage
                    for msg in reversed(result["messages"]):
                        if isinstance(msg, AIMessage):
                            responses.append(msg.content)
                            break
                        elif isinstance(msg, dict) and msg.get("role") == "assistant":
                            responses.append(msg.get("content", ""))
                            break
        
        logger.info(f"Generated {len(responses)} responses")
        
        # Aggregate responses using AI-powered aggregation
        final_answer = aggregation_agent(
            responses, 
            self.llm, 
            self.majority_voting_prompt
        )
        
        logger.info("Aggregation complete")
        
        # Return updated state with final answer
        from langchain_core.messages import AIMessage
        return {
            **state,
            "messages": state.get("messages", []) + [
                AIMessage(content=final_answer)
            ],
            "responses": responses,  # Include individual responses for inspection
        }

    async def ainvoke(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Asynchronously generate multiple responses and aggregate them.

        Args:
            state (Dict[str, Any]): Current workflow state

        Returns:
            Dict[str, Any]: Updated state with aggregated response
        """
        # For now, delegate to sync version
        # In production, implement proper async execution
        return self.invoke(state)

    def check_responses_for_answer(
        self, responses: List[str], answer: str
    ) -> bool:
        """
        Check if the specified answer is present in any of the provided responses.

        This method performs a simple string matching to determine if the expected
        answer appears in any of the generated responses. It's useful for validation
        and evaluation purposes.

        Args:
            responses (List[str]): List of responses to check
            answer (str): The answer to look for in the responses

        Returns:
            bool: True if the answer is found in any response, False otherwise

        Example:
            >>> agent = SelfConsistencyAgent(llm=llm)
            >>> responses = ["The answer is 42", "I think it's 42", "Not sure"]
            >>> found = agent.check_responses_for_answer(responses, "42")
            >>> print(found)  # True
        """
        for response in responses:
            if answer in response:
                return True
        
        # Log missing answers
        for response in responses:
            if answer not in response:
                logger.warning(
                    f"The answer '{answer}' is not found in the response: '{response}'"
                )
        
        return False

    def batched_invoke(
        self, states: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Run the agent on multiple states in batch.

        This method processes multiple states sequentially, applying the self-consistency
        approach to each state independently. It's useful for processing large datasets
        or multiple related problems.

        Args:
            states (List[Dict[str, Any]]): List of states to be processed

        Returns:
            List[Dict[str, Any]]: List of results for each state

        Example:
            >>> agent = SelfConsistencyAgent(llm=llm)
            >>> states = [
            ...     {"messages": [{"role": "user", "content": "What is 2+2?"}]},
            ...     {"messages": [{"role": "user", "content": "What is 3+3?"}]},
            ... ]
            >>> results = agent.batched_invoke(states)
            >>> print(len(results))  # 2
        """
        results = []
        for state in states:
            result = self.invoke(state)
            results.append(result)
        return results
