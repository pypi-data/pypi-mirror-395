"""
Middleware components for enhanced agent capabilities.

Provides middleware for:
- Filesystem operations (ls, read, write, edit, glob, grep)
- Subagent spawning for isolated task handling
- Todo list management
- Conversation summarization
- Agent memory management
- Resumable shell sessions
- Human-in-the-loop approval
"""

from azcore.middleware.base import MiddlewareBase
from azcore.middleware.filesystem import FilesystemMiddleware, FILESYSTEM_TOOLS
from azcore.middleware.subagents import SubAgentMiddleware, SubAgentSpec, CompiledSubAgent
from azcore.middleware.todolist import TodoListMiddleware, TodoItem, TodoStatus
from azcore.middleware.agent_memory import AgentMemoryMiddleware
from azcore.middleware.summarization import SummarizationMiddleware
from azcore.middleware.shell import ShellMiddleware, ShellSession
from azcore.middleware.resumable_shell import ResumableShellToolMiddleware
from azcore.middleware.hitl import HITLMiddleware, ApprovalDecision, ApprovalRequest, ApprovalResponse
from azcore.middleware.patch_tool_calls import PatchToolCallsMiddleware

__all__ = [
    # Base
    "MiddlewareBase",
    
    # Filesystem
    "FilesystemMiddleware",
    "FILESYSTEM_TOOLS",
    
    # Subagents
    "SubAgentMiddleware",
    "SubAgentSpec",
    "CompiledSubAgent",
    
    # TodoList
    "TodoListMiddleware",
    "TodoItem",
    "TodoStatus",
    
    # Agent Memory
    "AgentMemoryMiddleware",
    
    # Summarization
    "SummarizationMiddleware",
    
    # Shell
    "ShellMiddleware",
    "ShellSession",
    "ResumableShellToolMiddleware",
    
    # Human-in-the-Loop
    "HITLMiddleware",
    "ApprovalDecision",
    "ApprovalRequest",
    "ApprovalResponse",
    
    # Patch Tool Calls
    "PatchToolCallsMiddleware",
]
