from typing import TypedDict, Annotated, Sequence, NotRequired, Union, Callable, Any, Optional
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable, RunnableConfig
from langchain_core.messages import ToolMessage, BaseMessage
from langgraph.managed import RemainingSteps
from langgraph.graph.message import add_messages
from langchain_core.runnables import RunnableLambda
from langgraph.types import Checkpointer
from langchain_core.language_models.chat_models import BaseChatModel
from langgraph.graph import StateGraph, START
from langchain_core.tools import BaseTool
from langgraph.prebuilt import ToolNode, tools_condition


class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
    remaining_steps: NotRequired[RemainingSteps] # May use this at future
    


    
def handle_tool_error(state) -> dict:
    """
    Function to handle tool errors. When a tool raises an error, this function gets called
    with the current state. It returns a dictionary with the key "messages", which is a list
    of ToolMessage objects. The content of each message is the error message of the tool
    that raised the error and the tool call id is the id of the tool call that raised the
    error. This function is used as a fallback for tool nodes in the state graph, so that
    if a tool raises an error, the error is propagated back to the user.
    """
    error = state.get("error")
    tool_calls = state["messages"][-1].tool_calls
    return {
        "messages": [
            ToolMessage(
                content=f"Error: {repr(error)}\n please fix your mistakes.",
                tool_call_id=tc["id"],
            )
            for tc in tool_calls
        ]
    }


def create_tool_node_with_fallback(tools: list) -> dict:
    """
    Create a tool node with a fallback to handle tool errors.

    :param tools: the list of tools to include in the tool node
    :type tools: list
    :return: a tool node with a fallback to handle tool errors
    :rtype: dict
    """
    return ToolNode(tools).with_fallbacks(
        [RunnableLambda(handle_tool_error)], exception_key="error"
    )


 
class Assistant:
    def __init__(self, runnable: Runnable):
        """
        Initialize an Assistant object.

        :param runnable: the runnable that will be executed
        :type runnable: Runnable
        """
        self.runnable = runnable

    def __call__(self, state: AgentState, config: RunnableConfig):
        """
        Invoke the runnable with the given state and configuration.

        This function is a simple wrapper around the invoke method of the
        runnable. It adds the passenger_id to the state and breaks the loop
        if the result of the invoke method is not empty.

        :param state: the state of the conversation
        :type state: State
        :param config: the configuration of the runnable
        :type config: RunnableConfig
        :return: a dictionary with the result of the invoke method
        :rtype: dict
        """

        while True:
            configuration = config.get("configurable", {})
            passenger_id = configuration.get("passenger_id", None)
            state = {**state, "user_info": passenger_id}
            result = self.runnable.invoke(state)
            
            if not result.tool_calls and (
                not result.content
                or isinstance(result.content, list)
                and not result.content[0].get("text")
            ):
                messages = state["messages"] + [("user", "Respond with a real output.")]
                state = {**state, "messages": messages}
            else:
                break
        return {"messages": result}


def _print_event(event: dict, _printed: set, max_length=1500):
    """
    Print the event in a human-readable format.

    :param event: a dictionary containing information about the event
    :param _printed: a set of message IDs that have already been printed
    :param max_length: the maximum length of the message to be printed
    :type event: dict
    :type _printed: set
    :type max_length: int
    """
    current_state = event.get("dialog_state")
    if current_state:
        print("Currently in: ", current_state[-1])
    message = event.get("messages")
    if message:
        if isinstance(message, list):
            message = message[-1]
        if message.id not in _printed:
            msg_repr = message.pretty_repr(html=True)
            if len(msg_repr) > max_length:
                msg_repr = msg_repr[:max_length] + " ... (truncated)"
            print(msg_repr)
            _printed.add(message.id)


def create_thinkat_agent(
    model: BaseChatModel, 
    prompt: str,
    tools: Union[Sequence[Union[BaseTool, Callable, dict[str, Any]]], ToolNode],
    checkpointer: Optional[Checkpointer]=None
):
    """
    Create a think-at agent.

    The think-at agent is a state graph that is responsible for generating responses
    based on the user's messages. It uses a language model to generate responses
    and tools to generate more specific responses.

    :param model: the language model to use for generating responses
    :type model: BaseChatModel
    :param prompt: the system prompt to use for generating responses
    :type prompt: str
    :param tools: the tools to use for generating more specific responses
    :type tools: Union[Sequence[Union[BaseTool, Callable, dict[str, Any]]], ToolNode]
    :param checkpointer: the checkpointer to use for compiling the state graph
    :type checkpointer: Optional[Checkpointer]
    :return: the compiled think-at agent state graph
    :rtype: StateGraph
    """
    thinkat_agent_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
                prompt
        ),
        ("placeholder", "{messages}"),
    ]
    )



    thinkat_agent_runnable = thinkat_agent_prompt | model.bind_tools(tools)


    builder = StateGraph(AgentState)


    builder.add_node("assistant", Assistant(thinkat_agent_runnable))
    builder.add_node("tools", create_tool_node_with_fallback(tools))
    builder.add_edge(START, "assistant")
    builder.add_conditional_edges(
        "assistant",
        tools_condition,
    )
    builder.add_edge("tools", "assistant")


    thinkat_agent_graph = builder.compile(checkpointer=checkpointer)
    
    return thinkat_agent_graph