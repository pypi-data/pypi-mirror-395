"""
Response Generator node implementation.

The generator synthesizes final responses from team outputs,
creating coherent, user-friendly responses.
"""

from typing import Literal, Dict, Any
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import HumanMessage
from langgraph.types import Command
from langgraph.graph import END
from azcore.core.base import BaseNode
import logging

logger = logging.getLogger(__name__)


class ResponseGeneratorNode(BaseNode):
    """
    Response generator node for synthesizing final outputs.
    
    The generator:
    1. Analyzes conversation history and team outputs
    2. Synthesizes information into coherent responses
    3. Formats responses for user consumption
    4. Ensures completeness and accuracy
    
    Attributes:
        llm: Language model for generation
        system_prompt: System prompt defining generator behavior
    """
    
    def __init__(
        self,
        llm: BaseChatModel,
        system_prompt: str | None = None,
        name: str = "response_generator"
    ):
        """
        Initialize the response generator node.
        
        Args:
            llm: Language model for generation
            system_prompt: Optional custom system prompt
            name: Node name
        """
        super().__init__(name=name, description="Generates final responses")
        
        self.llm = llm
        self.system_prompt = system_prompt or self._default_prompt()
        
        self._logger.info(f"ResponseGeneratorNode '{name}' initialized")
    
    def _default_prompt(self) -> str:
        """
        Get default generator prompt.
        
        Returns:
            Default system prompt
        """
        return """You are an expert response generator for multi-agent systems.

Your responsibilities:
1. Analyze the complete conversation history
2. Review outputs from all specialized teams
3. Synthesize information into a coherent, comprehensive response
4. Format the response in a user-friendly manner
5. Ensure accuracy and completeness

Guidelines:
- Be clear and concise
- Present information logically
- Include relevant details from team outputs
- Cite specific data or findings when available
- Use appropriate formatting (lists, sections, etc.)
- Maintain a professional yet friendly tone
- Address the original user query completely
- Acknowledge limitations or uncertainties

Quality Standards:
- Accuracy: All information must be correct
- Completeness: Address all aspects of the query
- Clarity: Easy to understand
- Relevance: Focus on what the user needs
- Actionability: Provide next steps when appropriate

Remember: You are creating the final response the user will see. Make it count!
"""
    
    def execute(self, state: Dict[str, Any]) -> Command[Literal["__end__"]]:
        """
        Execute response generator logic.
        
        Args:
            state: Current workflow state with conversation history
            
        Returns:
            Command with final response
        """
        self._logger.info("Generator creating final response")
        
        messages = [
            {"role": "system", "content": self.system_prompt},
        ] + state.get("messages", [])
        
        # Generate response
        response = self.llm.invoke(messages)
        
        self._logger.debug(f"Generated response: {response.content[:100]}...")
        self._logger.info("Generator completed response")
        
        return Command(
            update={
                "messages": [
                    HumanMessage(content=response.content, name=self.name)
                ]
            },
            goto=END
        )
    
    def set_prompt(self, prompt: str) -> None:
        """
        Update the system prompt.
        
        Args:
            prompt: New system prompt
        """
        self.system_prompt = prompt
        self._logger.info("Updated generator system prompt")


def create_generator_node(
    llm: BaseChatModel,
    system_prompt: str | None = None,
    name: str = "response_generator"
) -> ResponseGeneratorNode:
    """
    Factory function to create a response generator node.
    
    Args:
        llm: Language model
        system_prompt: Optional system prompt
        name: Node name
        
    Returns:
        ResponseGeneratorNode instance
    """
    return ResponseGeneratorNode(
        llm=llm,
        system_prompt=system_prompt,
        name=name
    )



# """
# Response Generator node implementation.

# The response generator acts as the front-line agent that communicates with users
# and decides whether to hand off to the planner or finish the conversation.
# """

# from typing import Literal, Dict, Any
# from langchain_core.language_models.chat_models import BaseChatModel
# from langchain_core.messages import HumanMessage
# from langgraph.types import Command
# from langgraph.graph import END
# from azcore.core.base import BaseNode
# import logging

# logger = logging.getLogger(__name__)


# class ResponseGeneratorNode(BaseNode):
#     """
#     Response generator node for user interaction and task triage.
    
#     The Response Generator:
#     1. Communicates directly with users
#     2. Understands user requests
#     3. Decides if complex planning is needed
#     4. Routes to planner or ends conversation
    
#     Attributes:
#         llm: Language model for Response Generator
#         system_prompt: System prompt defining response generator behavior
#         handoff_keyword: Keyword to trigger handoff to planner
#     """
    
#     def __init__(
#         self,
#         llm: BaseChatModel,
#         system_prompt: str | None = None,
#         handoff_keyword: str = "handoff_to_planner",
#         name: str = "response_generator"
#     ):
#         """
#         Initialize the response generator node.
        
#         Args:
#             llm: Language model for the response generator
#             system_prompt: Optional custom system prompt
#             handoff_keyword: Keyword to detect planner handoff
#             name: Node name
#         """
#         super().__init__(name=name, description="Generates responses for user interactions")
        
#         self.llm = llm
#         self.handoff_keyword = handoff_keyword
#         self.system_prompt = system_prompt or self._default_prompt()

#         self._logger.info(f"Coordinator Node: GeneratorNode '{name}' initialized")

#     def _default_prompt(self) -> str:
#         """
#         Get default generator prompt.
        
#         Returns:
#             Default system prompt
#         """
#         return """You are an expert response generator for multi-agent systems.
#     Your task: Review the complete conversation history and the outputs from subagents, then produce a clear, concise report.

#     Responsibilities:
#     1. Read and synthesize the entire conversation history provided in the context.
#     2. Review outputs from all subagents and extract key facts, decisions, and artifacts.
#     3. Summarize findings in a concise, structured report.
#     4. List actions taken by subagents and the results of those actions.
#     5. Identify uncertainties, missing information, or potential errors.
#     6. Provide clear, prioritized recommendations and next steps.
#     7. Keep the report brief, professional, and actionable.

#     Preferred Report Structure:
#     Title: Short descriptive title
#     Summary: 1-3 sentence concise overview of the outcome
#     Findings:
#     - Bullet points of key findings (include specific data points or quotes when relevant)
#     Actions:
#     - Bullet points of actions taken with responsible subagent names
#     Results:
#     - Bullet points summarizing outputs, artifacts, or measurable outcomes
#     Uncertainties / Limitations:
#     - Bullet points describing what is unknown or any reliability concerns
#     Recommendations / Next Steps:
#     1. Numbered, prioritized next steps or handoffs
#     2. Who should take them and expected outputs

#     Formatting and Tone:
#     - Use short sentences and bullets for clarity.
#     - Be factual and avoid speculation; if you must note uncertainty, label it clearly.
#     - Cite exact subagent outputs or conversation excerpts when they support a finding.
#     - Target a one-page concise report; only expand sections when necessary.

#     If subagent outputs or conversation history are missing or incomplete, state what is missing and provide a short plan to obtain the missing information.

#     Return only the report text as the message content; do not include meta-comments or extra system instructions.
#     """
#     def execute(self, state: Dict[str, Any]) -> Command[Literal["planner", "__end__"]]:
#         """
#         Execute coordinator logic.
        
#         Args:
#             state: Current workflow state
            
#         Returns:
#             Command with routing decision
#         """
#         self._logger.info("Coordinator processing request")
        
#         messages = [
#             {"role": "system", "content": self.system_prompt},
#         ] + state.get("messages", [])
        
#         # Get coordinator response
#         response = self.llm.invoke(messages)

#         self._logger.debug(f"Response Generator response: {response.content[:100]}...")
        
#         # Determine next node
#         goto = END

        
#         return Command(
#             update={
#                 "messages": [
#                     HumanMessage(content=response.content, name=self.name)
#                 ]
#             },
#             goto=goto
#         )
    
#     def set_prompt(self, prompt: str) -> None:
#         """
#         Update the system prompt.
        
#         Args:
#             prompt: New system prompt
#         """
#         self.system_prompt = prompt
#         self._logger.info("Updated coordinator system prompt")
    
#     def set_handoff_keyword(self, keyword: str) -> None:
#         """
#         Update the handoff keyword.
        
#         Args:
#             keyword: New handoff keyword
#         """
#         self.handoff_keyword = keyword
#         self._logger.info(f"Updated handoff keyword to: {keyword}")


# def create_response_generator_node(
#     llm: BaseChatModel,
#     system_prompt: str | None = None,
#     name: str = "response_generator"
# ) -> ResponseGeneratorNode:
#     """
#     Factory function to create a response generator  node.
    
#     Args:
#         llm: Language model
#         system_prompt: Optional system prompt
#         name: Node name
        
#     Returns:
#         ResponseGeneratorNode instance
#     """
#     return ResponseGeneratorNode(llm=llm, system_prompt=system_prompt, name=name)
