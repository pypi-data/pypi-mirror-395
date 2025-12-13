"""
Enhanced Agent Factory for Azcore.

This module provides a convenience function for creating fully-equipped agents
with all standard middleware pre-configured. It's inspired by best practices
for agent composition and provides sensible defaults while remaining flexible.
"""

from typing import Any, Callable, Dict, List, Optional, Sequence, Union
from pathlib import Path
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.tools import BaseTool

from ..core.base import BaseAgent
from ..agents.agent_factory import AgentFactory, ReactAgent
from ..middleware import (
    MiddlewareBase,
    TodoListMiddleware,
    FilesystemMiddleware,
    SubAgentMiddleware,
    SubAgentSpec,
    SummarizationMiddleware,
    AgentMemoryMiddleware,
    PatchToolCallsMiddleware,
    ResumableShellToolMiddleware,
    HITLMiddleware,
)
from ..backends import BackendProtocol, CompositeBackend, StateBackend, FilesystemBackend
from ..utils.logging import get_logger

logger = get_logger(__name__)


# Base system prompt for enhanced agents
BASE_ENHANCED_PROMPT = """You are an enhanced AI agent with access to powerful capabilities:

1. **Task Management**: Use `write_todos` to track your progress on complex tasks
2. **File Operations**: Use file tools (ls, read_file, write_file, edit_file, glob, grep) for filesystem access
3. **Memory**: Use `save_memory` and `recall_memory` for long-term information storage
4. **Delegation**: Use `task` to delegate subtasks to specialized subagents
5. **Shell Access**: Use `shell` for command execution with persistent session state

Plan your approach, break down complex problems, and use your tools strategically."""


def create_enhanced_agent(
    name: str = "enhanced_agent",
    llm: Optional[BaseChatModel] = None,
    tools: Optional[Sequence[BaseTool]] = None,
    system_prompt: Optional[str] = None,
    middleware: Optional[Sequence[MiddlewareBase]] = None,
    subagents: Optional[List[SubAgentSpec]] = None,
    backend: Optional[Union[BackendProtocol, Callable]] = None,
    workspace_root: Optional[Path] = None,
    enable_filesystem: bool = True,
    enable_todolist: bool = True,
    enable_memory: bool = True,
    enable_subagents: bool = True,
    enable_shell: bool = True,
    enable_summarization: bool = True,
    enable_hitl: bool = False,
    enable_patch_tool_calls: bool = True,
    hitl_approval_func: Optional[Callable] = None,
    auto_approve_tools: Optional[List[str]] = None,
    interrupt_on: Optional[Dict[str, Any]] = None,
    enable_caching: bool = True,
    cache_type: str = "exact",
    description: str = "",
    **kwargs
) -> ReactAgent:
    """
    Create an enhanced agent with all standard middleware pre-configured.
    
    This is a convenience function that creates a fully-equipped agent with:
    - TodoList management for task tracking
    - Filesystem operations for file manipulation
    - Long-term memory for information persistence
    - Subagent delegation for complex task breakdown
    - Shell execution for system commands
    - Conversation summarization for long interactions
    - Optional Human-in-the-Loop approval
    - Tool call patching for robustness
    
    All features can be individually disabled if not needed.
    
    Args:
        name: Agent name (default: "enhanced_agent")
        llm: Language model to use (required)
        tools: Additional custom tools beyond middleware-provided tools
        system_prompt: Custom system prompt (will be combined with base prompt)
        middleware: Additional custom middleware to add after standard middleware
        subagents: List of subagent specifications for delegation
        backend: Storage backend (auto-configured if None)
        workspace_root: Root directory for file operations (default: cwd)
        
        Feature Toggles:
        enable_filesystem: Enable file operation tools (default: True)
        enable_todolist: Enable todo list management (default: True)
        enable_memory: Enable long-term memory (default: True)
        enable_subagents: Enable subagent delegation (default: True)
        enable_shell: Enable shell command execution (default: True)
        enable_summarization: Enable conversation summarization (default: True)
        enable_hitl: Enable human-in-the-loop approval (default: False)
        enable_patch_tool_calls: Enable tool call patching (default: True)
        
        HITL Configuration:
        hitl_approval_func: Custom approval function (tool_name, args) -> bool
        auto_approve_tools: List of tool names to auto-approve
        interrupt_on: Dict mapping tool names to interrupt configs (enables HITL)
        
        LLM Configuration:
        enable_caching: Enable LLM response caching (default: True)
        cache_type: Cache type - "exact" or "semantic" (default: "exact")
        
        description: Human-readable agent description
        **kwargs: Additional arguments passed to ReactAgent
        
    Returns:
        Fully configured ReactAgent instance
        
    Raises:
        ValueError: If llm is not provided
        
    Example:
        ```python
        from azcore.agents import create_enhanced_agent
        from langchain_openai import ChatOpenAI
        
        # Create a basic enhanced agent
        agent = create_enhanced_agent(
            name="my_agent",
            llm=ChatOpenAI(model="gpt-4"),
            system_prompt="You are a helpful coding assistant."
        )
        
        # Create with subagents and HITL
        agent = create_enhanced_agent(
            name="secure_agent",
            llm=ChatOpenAI(model="gpt-4"),
            subagents=[
                SubAgentSpec(
                    name="researcher",
                    description="Research and gather information",
                    system_prompt="You are a research specialist."
                ),
                SubAgentSpec(
                    name="coder",
                    description="Write and debug code",
                    system_prompt="You are an expert programmer."
                )
            ],
            enable_hitl=True,
            auto_approve_tools=["ls", "read_file", "recall_memory"]
        )
        
        # Minimal agent (disable most features)
        agent = create_enhanced_agent(
            name="simple_agent",
            llm=ChatOpenAI(model="gpt-4"),
            enable_filesystem=False,
            enable_subagents=False,
            enable_shell=False,
            enable_memory=False
        )
        ```
    
    Configuration Philosophy:
        This function follows the "batteries included" principle - provide
        sensible defaults that work well together, but allow customization
        at every level. Users can:
        - Use all defaults for quick setup
        - Disable unwanted features individually
        - Override any middleware with custom implementations
        - Add additional tools and middleware
        
    Middleware Order:
        The middleware is applied in a specific order for optimal functionality:
        1. PatchToolCallsMiddleware - Fix dangling tool calls first
        2. TodoListMiddleware - Task tracking
        3. FilesystemMiddleware - File operations
        4. AgentMemoryMiddleware - Long-term memory
        5. SubAgentMiddleware - Delegation (includes nested middleware)
        6. ResumableShellToolMiddleware - Shell with HITL support
        7. SummarizationMiddleware - Compress long conversations
        8. HITLMiddleware - Human approval (last, controls all tools)
        9. Custom middleware - User-provided extensions
    """
    if llm is None:
        raise ValueError(
            "llm parameter is required. Please provide a language model instance."
        )
    
    # Set workspace root
    workspace_root = workspace_root or Path.cwd()
    
    # Configure backend
    if backend is None:
        backend = _create_default_backend(workspace_root)
    elif callable(backend):
        # Backend factory function
        backend_factory = backend
        backend = None  # Will be created per-runtime
        logger.info("Using custom backend factory")
    
    # Build system prompt
    final_prompt = BASE_ENHANCED_PROMPT
    if system_prompt:
        final_prompt = f"{system_prompt}\n\n{BASE_ENHANCED_PROMPT}"
    
    # Create base agent using AgentFactory
    factory = AgentFactory()
    agent = factory.create_react_agent(
        name=name,
        llm=llm,
        tools=list(tools) if tools else [],
        prompt=final_prompt,
        description=description or "Enhanced agent with full middleware stack",
        enable_caching=enable_caching,
        cache_type=cache_type,
        **kwargs
    )
    
    logger.info(f"Creating enhanced agent '{name}'")
    
    # Apply middleware in optimal order
    middleware_stack: List[MiddlewareBase] = []
    
    # 1. PatchToolCallsMiddleware - Fix dangling tool calls first
    if enable_patch_tool_calls:
        middleware_stack.append(PatchToolCallsMiddleware())
        logger.debug("Added PatchToolCallsMiddleware")
    
    # 2. TodoListMiddleware - Task tracking
    if enable_todolist:
        middleware_stack.append(TodoListMiddleware())
        logger.debug("Added TodoListMiddleware")
    
    # 3. FilesystemMiddleware - File operations
    if enable_filesystem:
        fs_middleware = FilesystemMiddleware(
            backend=backend
        )
        middleware_stack.append(fs_middleware)
        logger.debug(f"Added FilesystemMiddleware")
    
    # 4. AgentMemoryMiddleware - Long-term memory
    if enable_memory:
        memory_middleware = AgentMemoryMiddleware(
            backend=backend
        )
        middleware_stack.append(memory_middleware)
        logger.debug("Added AgentMemoryMiddleware")
    
    # 5. SubAgentMiddleware - Delegation with nested middleware
    if enable_subagents:
        # Configure default subagent middleware
        default_subagent_middleware = []
        if enable_todolist:
            default_subagent_middleware.append(TodoListMiddleware())
        if enable_filesystem:
            default_subagent_middleware.append(
                FilesystemMiddleware(backend=backend)
            )
        if enable_summarization:
            default_subagent_middleware.append(
                SummarizationMiddleware(
                    max_messages=30,
                    keep_recent=5,
                    summarize_threshold=25
                )
            )
        if enable_patch_tool_calls:
            default_subagent_middleware.append(PatchToolCallsMiddleware())
        
        subagent_middleware = SubAgentMiddleware(
            subagents=subagents or [],
            default_model=llm,
            default_tools=list(tools) if tools else None,
            default_middleware=default_subagent_middleware,
            general_purpose_agent=True  # Allow delegation to general subagent
        )
        middleware_stack.append(subagent_middleware)
        logger.debug(f"Added SubAgentMiddleware ({len(subagents or [])} subagents)")
    
    # 6. ResumableShellToolMiddleware - Shell with HITL support
    if enable_shell:
        shell_middleware = ResumableShellToolMiddleware(
            workspace_root=workspace_root,
            preserve_state=True
        )
        middleware_stack.append(shell_middleware)
        logger.debug("Added ResumableShellToolMiddleware")
    
    # 7. SummarizationMiddleware - Compress long conversations
    if enable_summarization:
        summarization_middleware = SummarizationMiddleware(
            max_messages=50,
            keep_recent=10,
            summarize_threshold=40
        )
        middleware_stack.append(summarization_middleware)
        logger.debug("Added SummarizationMiddleware")
    
    # 8. HITLMiddleware - Human approval (last, controls all tools)
    # Enable HITL if explicitly enabled OR if interrupt_on is provided
    if enable_hitl or interrupt_on is not None:
        # Configure tools requiring approval
        if interrupt_on is not None:
            # Use tools from interrupt_on dict
            require_approval_for = list(interrupt_on.keys())
        else:
            require_approval_for = None

        # Configure auto-approve list (only if interrupt_on is not used)
        if interrupt_on is None and auto_approve_tools is None:
            # Safe default tools that don't modify state
            auto_approve_tools = [
                "ls", "read_file", "glob", "grep",
                "recall_memory", "write_todos"
            ]

        hitl_middleware = HITLMiddleware(
            approval_function=hitl_approval_func,
            require_approval_for=require_approval_for,
            auto_approve_safe=auto_approve_tools is not None,
            safe_tools=auto_approve_tools
        )
        middleware_stack.append(hitl_middleware)
        logger.debug(f"Added HITLMiddleware (approval for: {require_approval_for or 'all tools'})")
    
    # 9. Custom middleware - User-provided extensions
    if middleware:
        middleware_stack.extend(middleware)
        logger.debug(f"Added {len(middleware)} custom middleware")
    
    # Apply all middleware to agent
    for mw in middleware_stack:
        mw.setup(agent)
    
    # Log final configuration
    total_tools = len(agent.tools) if hasattr(agent, 'tools') else 0
    logger.info(
        f"Enhanced agent '{name}' created with {len(middleware_stack)} middleware "
        f"and {total_tools} total tools"
    )
    
    return agent


def _create_default_backend(workspace_root: Path) -> BackendProtocol:
    """
    Create a default composite backend with sensible defaults.
    
    This creates a hybrid backend that:
    - Uses StateBackend for /state/* paths (ephemeral, LangGraph checkpointed)
    - Uses FilesystemBackend for everything else (real filesystem)
    
    Args:
        workspace_root: Root directory for filesystem operations
        
    Returns:
        Configured CompositeBackend
    """
    backends = {
        "/state": StateBackend(),
        "/": FilesystemBackend(workspace_root=workspace_root)
    }
    
    backend = CompositeBackend(backends=backends)
    logger.debug(f"Created default CompositeBackend (workspace: {workspace_root})")
    
    return backend


def create_simple_agent(
    name: str = "simple_agent",
    llm: Optional[BaseChatModel] = None,
    tools: Optional[Sequence[BaseTool]] = None,
    system_prompt: Optional[str] = None,
    workspace_root: Optional[Path] = None,
    **kwargs
) -> ReactAgent:
    """
    Create a simple agent with minimal middleware.
    
    This is a lightweight version that only includes:
    - PatchToolCallsMiddleware (robustness)
    - FilesystemMiddleware (file operations)
    - TodoListMiddleware (task tracking)
    
    Use this when you want basic functionality without the overhead
    of memory, subagents, summarization, etc.
    
    Args:
        name: Agent name
        llm: Language model (required)
        tools: Additional custom tools
        system_prompt: Custom system prompt
        workspace_root: Root directory for file operations
        **kwargs: Additional arguments passed to ReactAgent
        
    Returns:
        ReactAgent with minimal middleware
        
    Example:
        ```python
        from azcore.agents import create_simple_agent
        from langchain_openai import ChatOpenAI
        
        agent = create_simple_agent(
            name="quick_agent",
            llm=ChatOpenAI(model="gpt-4"),
            system_prompt="You are a quick assistant."
        )
        ```
    """
    return create_enhanced_agent(
        name=name,
        llm=llm,
        tools=tools,
        system_prompt=system_prompt,
        workspace_root=workspace_root,
        enable_memory=False,
        enable_subagents=False,
        enable_shell=False,
        enable_summarization=False,
        enable_hitl=False,
        **kwargs
    )


# Export
__all__ = [
    "create_enhanced_agent",
    "create_simple_agent",
    "BASE_ENHANCED_PROMPT",
]
