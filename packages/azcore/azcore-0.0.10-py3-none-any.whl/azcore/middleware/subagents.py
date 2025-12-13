"""Middleware for spawning ephemeral subagents for isolated task handling.

This middleware allows agents to delegate complex, multi-step tasks to ephemeral
subagents that have isolated context windows. Subagents handle tasks autonomously
and return a single synthesized result back to the main agent.
"""

from typing import Any, Callable, TypedDict, NotRequired, Sequence
from collections.abc import Awaitable
import asyncio

from azcore.middleware.base import MiddlewareBase


class SubAgentSpec(TypedDict):
    """Specification for a subagent.
    
    Attributes:
        name: Unique name for the subagent.
        description: Description of subagent capabilities (for routing).
        system_prompt: System prompt to use for the subagent.
        tools: Tools available to the subagent.
        model: Optional model override for this subagent.
        middleware: Optional additional middleware for this subagent.
    """
    name: str
    description: str
    system_prompt: str
    tools: NotRequired[list[Any]]
    model: NotRequired[Any]
    middleware: NotRequired[list[Any]]


class CompiledSubAgent(TypedDict):
    """A pre-compiled subagent.
    
    Attributes:
        name: Unique name for the subagent.
        description: Description of subagent capabilities.
        runnable: The compiled agent graph/runnable.
    """
    name: str
    description: str
    runnable: Any


DEFAULT_SUBAGENT_PROMPT = """You are a specialized subagent that handles isolated tasks.
Complete the task given to you and return a comprehensive result."""

TASK_TOOL_DESCRIPTION = """Launch an ephemeral subagent to handle complex, multi-step independent tasks.

Available agent types:
{available_agents}

## When to use the task tool:
- Complex, multi-step tasks that can be fully delegated
- Tasks that are independent and can run in parallel
- Tasks requiring focused reasoning or heavy token usage
- When you need to isolate context to avoid bloating the main thread

## Usage notes:
1. Launch multiple agents in parallel when possible for better performance
2. Provide detailed task descriptions - the subagent cannot ask follow-up questions
3. Each subagent invocation is stateless and isolated
4. The subagent returns a single synthesized result
5. Clearly specify what information the subagent should return

## Example:
User: "Research Python, JavaScript, and Go, then compare them"
Assistant: *Launches 3 parallel task subagents, one for each language*
Assistant: *Synthesizes results from all 3 subagents*

The task tool is perfect for breaking down complex objectives into isolated,
parallel workstreams that can be processed independently and then combined."""

TASK_SYSTEM_PROMPT = """## task (subagent spawner)

You have access to a `task` tool to launch ephemeral subagents for isolated tasks.
These subagents are short-lived and return a single result.

When to use:
- Complex multi-step tasks that can be fully delegated
- Independent tasks that can run in parallel
- Heavy token/context usage that would bloat the main thread
- Isolating context for better focus

Lifecycle:
1. Spawn → Provide clear instructions and expected output
2. Run → Subagent completes task autonomously
3. Return → Subagent provides synthesized result
4. Reconcile → Incorporate result into main thread

When NOT to use:
- Trivial tasks (simple tool calls)
- When you need to see intermediate steps
- When task requires back-and-forth interaction

Remember to parallelize work whenever possible by launching multiple subagents
simultaneously."""


class TaskTool:
    """Tool for spawning subagents."""
    
    def __init__(
        self,
        subagents: dict[str, Any],
        default_model: Any = None,
        default_tools: list[Any] = None,
        default_middleware: list[Any] = None,
    ):
        """Initialize task tool.
        
        Args:
            subagents: Dictionary mapping subagent names to their runnables.
            default_model: Default model for subagents.
            default_tools: Default tools for subagents.
            default_middleware: Default middleware for subagents.
        """
        self.subagents = subagents
        self.default_model = default_model
        self.default_tools = default_tools or []
        self.default_middleware = default_middleware or []
        self.name = "task"
        self.description = TASK_TOOL_DESCRIPTION.format(
            available_agents="\n".join([
                f"- {name}: {agent.get('description', 'General purpose agent')}"
                for name, agent in subagents.items()
            ])
        )
    
    def __call__(
        self,
        description: str,
        subagent_type: str,
        runtime: Any = None,
        **kwargs
    ) -> dict[str, Any]:
        """Execute a task using a subagent.
        
        Args:
            description: Task description for the subagent.
            subagent_type: Type of subagent to use.
            runtime: Runtime context.
            **kwargs: Additional arguments.
            
        Returns:
            Task result from the subagent.
        """
        if subagent_type not in self.subagents:
            return {
                "error": f"Unknown subagent type: {subagent_type}. "
                         f"Available: {list(self.subagents.keys())}"
            }
        
        subagent = self.subagents[subagent_type]
        
        # Create isolated state for subagent
        subagent_state = {
            "messages": [{"role": "user", "content": description}],
        }
        
        # If runtime has state, copy relevant context (excluding messages)
        if runtime and hasattr(runtime, "state"):
            for key, value in runtime.state.items():
                if key not in ("messages", "todos"):
                    subagent_state[key] = value
        
        # Execute subagent
        try:
            if callable(subagent):
                result = subagent(subagent_state)
            elif hasattr(subagent, "invoke"):
                result = subagent.invoke(subagent_state)
            elif isinstance(subagent, dict) and "runnable" in subagent:
                result = subagent["runnable"].invoke(subagent_state)
            else:
                return {"error": f"Subagent {subagent_type} is not callable"}
            
            # Extract final message from result
            if isinstance(result, dict):
                messages = result.get("messages", [])
                if messages:
                    last_message = messages[-1]
                    if isinstance(last_message, dict):
                        content = last_message.get("content", str(last_message))
                    else:
                        content = getattr(last_message, "content", str(last_message))
                    return {"result": content}
                return {"result": str(result)}
            
            return {"result": str(result)}
            
        except Exception as e:
            return {"error": f"Subagent execution failed: {str(e)}"}
    
    async def __call_async__(
        self,
        description: str,
        subagent_type: str,
        runtime: Any = None,
        **kwargs
    ) -> dict[str, Any]:
        """Async execution of task.
        
        Args:
            description: Task description for the subagent.
            subagent_type: Type of subagent to use.
            runtime: Runtime context.
            **kwargs: Additional arguments.
            
        Returns:
            Task result from the subagent.
        """
        if subagent_type not in self.subagents:
            return {
                "error": f"Unknown subagent type: {subagent_type}. "
                         f"Available: {list(self.subagents.keys())}"
            }
        
        subagent = self.subagents[subagent_type]
        
        # Create isolated state
        subagent_state = {
            "messages": [{"role": "user", "content": description}],
        }
        
        if runtime and hasattr(runtime, "state"):
            for key, value in runtime.state.items():
                if key not in ("messages", "todos"):
                    subagent_state[key] = value
        
        # Execute subagent async
        try:
            if hasattr(subagent, "ainvoke"):
                result = await subagent.ainvoke(subagent_state)
            elif isinstance(subagent, dict) and "runnable" in subagent:
                if hasattr(subagent["runnable"], "ainvoke"):
                    result = await subagent["runnable"].ainvoke(subagent_state)
                else:
                    result = subagent["runnable"].invoke(subagent_state)
            else:
                # Fallback to sync
                result = self.__call__(description, subagent_type, runtime, **kwargs)
                return result
            
            # Extract final message
            if isinstance(result, dict):
                messages = result.get("messages", [])
                if messages:
                    last_message = messages[-1]
                    if isinstance(last_message, dict):
                        content = last_message.get("content", str(last_message))
                    else:
                        content = getattr(last_message, "content", str(last_message))
                    return {"result": content}
                return {"result": str(result)}
            
            return {"result": str(result)}
            
        except Exception as e:
            return {"error": f"Subagent execution failed: {str(e)}"}


class SubAgentMiddleware(MiddlewareBase):
    """Middleware for spawning ephemeral subagents.
    
    This middleware adds a `task` tool that allows agents to delegate complex
    tasks to isolated subagents. Subagents run with their own context and
    return synthesized results.
    
    Args:
        default_model: Default model for subagents.
        default_tools: Default tools for subagents.
        default_middleware: Default middleware to apply to all subagents.
        subagents: List of custom subagent specifications.
        system_prompt: Custom system prompt override.
        general_purpose_agent: Whether to include a general-purpose subagent.
        task_description: Custom task tool description.
    
    Example:
        ```python
        from azcore.middleware import SubAgentMiddleware
        from azcore.agents import AgentFactory
        
        # Create subagent middleware
        middleware = SubAgentMiddleware(
            default_model="gpt-4",
            general_purpose_agent=True,
            subagents=[
                {
                    "name": "researcher",
                    "description": "Research specialist for deep analysis",
                    "system_prompt": "You are a research specialist...",
                    "tools": []
                }
            ]
        )
        
        # Apply to agent
        agent = AgentFactory.create_agent(name="orchestrator")
        middleware.setup(agent)
        
        # Agent can now use task tool to spawn subagents
        ```
    """
    
    def __init__(
        self,
        *,
        default_model: Any = None,
        default_tools: list[Any] | None = None,
        default_middleware: list[Any] | None = None,
        subagents: list[SubAgentSpec | CompiledSubAgent] | None = None,
        system_prompt: str | None = None,
        general_purpose_agent: bool = True,
        task_description: str | None = None,
    ):
        """Initialize subagent middleware."""
        self.default_model = default_model
        self.default_tools = default_tools or []
        self.default_middleware = default_middleware or []
        self.subagents_specs = subagents or []
        self.system_prompt = system_prompt if system_prompt is not None else TASK_SYSTEM_PROMPT
        self.general_purpose_agent = general_purpose_agent
        self.task_description = task_description
        
        # Build subagents dictionary
        self.compiled_subagents = self._compile_subagents()
        
        # Create task tool
        self.task_tool = TaskTool(
            subagents=self.compiled_subagents,
            default_model=default_model,
            default_tools=default_tools,
            default_middleware=default_middleware,
        )
        if task_description:
            self.task_tool.description = task_description
    
    def _compile_subagents(self) -> dict[str, Any]:
        """Compile subagent specifications into runnable subagents."""
        compiled = {}
        
        # Add general purpose agent if enabled
        if self.general_purpose_agent:
            from azcore.agents import AgentFactory

            factory = AgentFactory()
            general_agent = factory.create_react_agent(
                name="general-purpose",
                llm=self.default_model,
                tools=self.default_tools,
                prompt="You are a general purpose assistant. Complete the assigned task efficiently.",
            )

            compiled["general-purpose"] = {
                "description": "General-purpose agent for any task",
                "runnable": general_agent,
            }
        
        # Compile custom subagents
        for spec in self.subagents_specs:
            if "runnable" in spec:
                # Pre-compiled subagent
                compiled[spec["name"]] = spec
            else:
                # Specification - need to compile
                from azcore.agents import AgentFactory

                factory = AgentFactory()
                subagent = factory.create_react_agent(
                    name=spec["name"],
                    llm=spec.get("model", self.default_model),
                    tools=spec.get("tools", self.default_tools),
                    prompt=spec.get("system_prompt", DEFAULT_SUBAGENT_PROMPT),
                    description=spec.get("description", ""),
                )

                compiled[spec["name"]] = {
                    "description": spec.get("description", ""),
                    "runnable": subagent,
                }
        
        return compiled
    
    def setup(self, agent: Any) -> None:
        """Setup middleware with agent."""
        # Add task tool to agent
        if hasattr(agent, "tools"):
            # Get existing tool names, handling both tool objects and functions
            existing_tool_names = []
            for t in agent.tools:
                if hasattr(t, 'name'):
                    existing_tool_names.append(t.name)
                elif callable(t) and hasattr(t, '__name__'):
                    existing_tool_names.append(t.__name__)

            if self.task_tool.name not in existing_tool_names:
                agent.tools.append(self.task_tool)
    
    def wrap_model_call(
        self,
        request: dict[str, Any],
        handler: Callable[[dict[str, Any]], dict[str, Any]],
    ) -> dict[str, Any]:
        """Update system prompt to include task tool instructions."""
        if self.system_prompt is not None:
            existing_prompt = request.get("system_prompt", "")
            if existing_prompt:
                request["system_prompt"] = existing_prompt + "\n\n" + self.system_prompt
            else:
                request["system_prompt"] = self.system_prompt
        return handler(request)
