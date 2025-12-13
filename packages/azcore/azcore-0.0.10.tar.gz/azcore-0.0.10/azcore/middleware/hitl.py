"""
Human-in-the-Loop (HITL) Middleware for Azcore.

This middleware adds approval workflows for tool executions, allowing humans
to review and approve/reject tool calls before they are executed. Useful for
sensitive operations or learning/debugging scenarios.
"""

from typing import Any, Dict, List, Optional, Protocol, TypedDict, Literal, Callable
from enum import Enum
from ..utils.logging import get_logger

logger = get_logger(__name__)


class ApprovalDecision(str, Enum):
    """Approval decision enum."""
    APPROVE = "approve"
    REJECT = "reject"
    MODIFY = "modify"


class ToolCall(TypedDict):
    """Tool call information."""
    name: str
    args: Dict[str, Any]
    description: Optional[str]


class ApprovalRequest(TypedDict):
    """Approval request structure."""
    tool_call: ToolCall
    context: Dict[str, Any]
    custom_message: Optional[str]


class ApprovalResponse(TypedDict):
    """Approval response structure."""
    decision: ApprovalDecision
    modified_args: Optional[Dict[str, Any]]
    reason: Optional[str]


class Runtime(Protocol):
    """Runtime protocol for middleware."""
    state: Dict[str, Any]


class HITLMiddleware:
    """
    Human-in-the-Loop middleware for tool approval.
    
    This middleware intercepts tool calls and requests human approval before
    execution. It supports:
    - Approve: Execute tool as requested
    - Reject: Cancel tool execution
    - Modify: Change tool arguments before execution
    
    Example:
        ```python
        from azcore.middleware import HITLMiddleware
        from azcore.agents import AgentFactory
        
        # Custom approval function
        def my_approver(request):
            print(f"Tool: {request['tool_call']['name']}")
            print(f"Args: {request['tool_call']['args']}")
            
            decision = input("Approve? (y/n/m): ").lower()
            if decision == 'y':
                return {"decision": "approve"}
            elif decision == 'm':
                # Modify args
                return {
                    "decision": "modify",
                    "modified_args": {...}
                }
            else:
                return {"decision": "reject", "reason": "User rejected"}
        
        middleware = HITLMiddleware(
            approval_function=my_approver,
            require_approval_for=["write_file", "shell"]
        )
        
        agent = AgentFactory.create_agent(name="careful_agent")
        middleware.setup(agent)
        
        # All write_file and shell calls will require approval
        ```
    
    Attributes:
        approval_function: Function to call for approvals
        require_approval_for: List of tool names requiring approval
        auto_approve_safe: Auto-approve "safe" operations
    """
    
    def __init__(
        self,
        approval_function: Optional[Callable[[ApprovalRequest], ApprovalResponse]] = None,
        require_approval_for: Optional[List[str]] = None,
        auto_approve_safe: bool = False,
        safe_tools: Optional[List[str]] = None
    ):
        """
        Initialize HITL middleware.
        
        Args:
            approval_function: Function to handle approval requests
            require_approval_for: List of tool names requiring approval (None = all)
            auto_approve_safe: Automatically approve safe tools
            safe_tools: List of tools considered safe (for auto-approval)
        """
        self.approval_function = approval_function or self._default_approval_function
        self.require_approval_for = require_approval_for  # None means all tools
        self.auto_approve_safe = auto_approve_safe
        self.safe_tools = safe_tools or ["ls", "read_file", "glob", "grep", "recall_memory"]
        self.agent = None
        self._approval_history: List[Dict[str, Any]] = []
        
    def _default_approval_function(self, request: ApprovalRequest) -> ApprovalResponse:
        """
        Default CLI-based approval function.
        
        Args:
            request: Approval request
            
        Returns:
            Approval response
        """
        tool_call = request["tool_call"]
        
        print("\n" + "=" * 70)
        print("🔔 TOOL APPROVAL REQUIRED")
        print("=" * 70)
        print(f"\n📋 Tool: {tool_call['name']}")
        
        if tool_call.get('description'):
            print(f"📝 Description: {tool_call['description']}")
        
        print("\n🔧 Arguments:")
        for key, value in tool_call['args'].items():
            # Truncate long values
            value_str = str(value)
            if len(value_str) > 100:
                value_str = value_str[:97] + "..."
            print(f"  • {key}: {value_str}")
        
        if request.get('custom_message'):
            print(f"\n💬 {request['custom_message']}")
        
        print("\n" + "-" * 70)
        print("Options:")
        print("  [y] Approve - Execute tool as requested")
        print("  [n] Reject  - Cancel tool execution")
        print("  [m] Modify  - Change tool arguments")
        print("-" * 70)
        
        while True:
            choice = input("\nYour decision (y/n/m): ").lower().strip()
            
            if choice == 'y':
                print("✅ Approved")
                return ApprovalResponse(
                    decision=ApprovalDecision.APPROVE,
                    modified_args=None,
                    reason=None
                )
            
            elif choice == 'n':
                reason = input("Reason for rejection (optional): ").strip()
                print("❌ Rejected")
                return ApprovalResponse(
                    decision=ApprovalDecision.REJECT,
                    modified_args=None,
                    reason=reason or "User rejected"
                )
            
            elif choice == 'm':
                print("\n⚠️  Argument modification not implemented in CLI")
                print("Please approve or reject.")
                continue
            
            else:
                print("Invalid choice. Please enter y, n, or m.")
    
    def setup(self, agent: Any) -> None:
        """
        Setup middleware on an agent.
        
        Args:
            agent: The agent to add HITL to
        """
        self.agent = agent
        
        # Wrap existing tools
        if hasattr(agent, 'tools') and agent.tools:
            wrapped_tools = []
            for tool in agent.tools:
                wrapped_tool = self._wrap_tool(tool)
                wrapped_tools.append(wrapped_tool)
            agent.tools = wrapped_tools
        
        logger.info(f"HITL middleware configured for {agent.name}")
        if self.require_approval_for:
            logger.info(f"  Requires approval for: {', '.join(self.require_approval_for)}")
        else:
            logger.info(f"  Requires approval for: ALL tools")
        logger.info(f"  Auto-approve safe: {self.auto_approve_safe}")
    
    def _should_request_approval(self, tool_name: str) -> bool:
        """Check if tool requires approval."""
        # If auto-approve safe is enabled and tool is safe, skip approval
        if self.auto_approve_safe and tool_name in self.safe_tools:
            return False
        
        # If specific tools list provided, check if tool is in it
        if self.require_approval_for is not None:
            return tool_name in self.require_approval_for
        
        # Otherwise, require approval for all tools
        return True
    
    def _wrap_tool(self, tool: Any) -> Any:
        """Wrap a tool with approval logic."""
        
        class WrappedTool:
            """Wrapped tool with approval."""
            
            def __init__(self, original_tool: Any, middleware: 'HITLMiddleware'):
                self.original_tool = original_tool
                self.middleware = middleware
                
                # Copy attributes from original tool
                self.name = getattr(original_tool, 'name', str(original_tool))
                self.description = getattr(original_tool, 'description', '')
                self.parameters = getattr(original_tool, 'parameters', {})
            
            def __call__(self, *args, **kwargs) -> Any:
                """Execute tool with approval check."""
                # Check if approval needed
                if not self.middleware._should_request_approval(self.name):
                    # No approval needed, execute directly
                    return self.original_tool(*args, **kwargs)
                
                # Request approval
                request = ApprovalRequest(
                    tool_call=ToolCall(
                        name=self.name,
                        args=kwargs,
                        description=self.description
                    ),
                    context={},
                    custom_message=None
                )
                
                response = self.middleware.approval_function(request)
                
                # Record approval
                self.middleware._approval_history.append({
                    "tool": self.name,
                    "args": kwargs,
                    "decision": response["decision"],
                    "reason": response.get("reason")
                })
                
                # Handle decision
                if response["decision"] == ApprovalDecision.APPROVE:
                    return self.original_tool(*args, **kwargs)
                
                elif response["decision"] == ApprovalDecision.MODIFY:
                    # Use modified args
                    modified_args = response.get("modified_args", {})
                    merged_kwargs = {**kwargs, **modified_args}
                    return self.original_tool(*args, **merged_kwargs)
                
                else:  # REJECT
                    reason = response.get("reason", "User rejected")
                    return {
                        "error": "Tool execution rejected",
                        "reason": reason,
                        "message": f"❌ Tool '{self.name}' was rejected: {reason}"
                    }
        
        return WrappedTool(tool, self)
    
    def get_approval_history(self) -> List[Dict[str, Any]]:
        """
        Get approval history.
        
        Returns:
            List of approval decisions
        """
        return self._approval_history
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get approval statistics.
        
        Returns:
            Dictionary with approval stats
        """
        total = len(self._approval_history)
        if total == 0:
            return {
                "total_requests": 0,
                "approved": 0,
                "rejected": 0,
                "modified": 0
            }
        
        approved = sum(1 for h in self._approval_history if h["decision"] == ApprovalDecision.APPROVE)
        rejected = sum(1 for h in self._approval_history if h["decision"] == ApprovalDecision.REJECT)
        modified = sum(1 for h in self._approval_history if h["decision"] == ApprovalDecision.MODIFY)
        
        return {
            "total_requests": total,
            "approved": approved,
            "rejected": rejected,
            "modified": modified,
            "approval_rate": approved / total if total > 0 else 0
        }


# Export
__all__ = ["HITLMiddleware", "ApprovalDecision", "ApprovalRequest", "ApprovalResponse"]
