"""
Resumable Shell Middleware for Azcore.

This middleware extends ShellMiddleware to handle checkpointing and restoration
when using Human-in-the-Loop (HITL) workflows. It ensures shell sessions survive
HITL pauses by lazily recreating resources when needed.
"""

from typing import Any, Dict, Optional, Union
from pathlib import Path
from .shell import ShellMiddleware, ShellSession
from .base import MiddlewareBase
from ..utils.logging import get_logger

logger = get_logger(__name__)


class ResumableShellToolMiddleware(ShellMiddleware):
    """
    Shell middleware that recreates session resources after human interrupts.
    
    Standard ShellMiddleware stores shell sessions in runtime state. When a run
    pauses for human approval (HITL), the session may not be properly checkpointed.
    Upon resuming, the state is restored without the shell resources, causing
    "Shell session resources unavailable" errors.
    
    This subclass lazily recreates the shell session the first time a resumed run
    needs it, keeping behavior identical for uninterrupted runs while allowing
    HITL pauses to succeed.
    
    Key Features:
    - Automatic session recreation after HITL pauses
    - Preserves session state (working dir, env vars) when possible
    - Clean shutdown only when session is actually active
    - Drop-in replacement for ShellMiddleware
    
    Example:
        ```python
        from azcore.middleware import ResumableShellToolMiddleware, HITLMiddleware
        from azcore.agents import AgentFactory
        from pathlib import Path
        
        # Create agent with both HITL and resumable shell
        agent = AgentFactory.create_agent(name="dev_agent")
        
        # Add HITL middleware first
        hitl = HITLMiddleware(
            should_approve=lambda tool, args: tool not in ["shell"]
        )
        hitl.setup(agent)
        
        # Add resumable shell middleware
        shell = ResumableShellToolMiddleware(
            workspace_root=Path("/path/to/project")
        )
        shell.setup(agent)
        
        # Now agent can handle HITL pauses during shell operations
        # Shell session will be recreated automatically after approval
        ```
    
    Technical Details:
        When HITL pauses execution:
        1. LangGraph checkpoints the state
        2. Shell session handle may be lost (UntrackedValue in state)
        3. On resume, state is restored without session
        4. First shell tool call detects missing session
        5. Session is recreated with preserved state if available
        6. Execution continues normally
    
    Attributes:
        workspace_root: Root directory for shell sessions
        preserve_state: Whether to preserve working dir/env vars across recreation
    """
    
    def __init__(
        self,
        workspace_root: Optional[Union[str, Path]] = None,
        preserve_state: bool = True,
        execution_policy: Optional[Any] = None
    ):
        """
        Initialize resumable shell middleware.

        Args:
            workspace_root: Root directory for the workspace (default: cwd)
                          Can be a string or Path object
            preserve_state: Whether to preserve working dir/env vars when
                          recreating sessions (default: True)
            execution_policy: Optional execution policy for command approval
                            (for compatibility with langchain-based implementations)
        """
        super().__init__(workspace_root)
        self.preserve_state = preserve_state
        self.execution_policy = execution_policy
        
    def _get_session(self, runtime: Any) -> ShellSession:
        """
        Get or lazily create shell session for runtime.
        
        This overrides the parent implementation to add lazy recreation logic.
        If the session is missing (e.g., after HITL pause), it's recreated
        automatically.
        
        Args:
            runtime: Runtime context with state
            
        Returns:
            Active shell session (existing or newly created)
        """
        # Check if session exists
        if "_shell_session" in runtime.state:
            session = runtime.state["_shell_session"]
            
            # Verify it's a valid session object
            if isinstance(session, ShellSession):
                return session
            
            # Session exists but is invalid (shouldn't happen, but be defensive)
            logger.warning(
                "Found invalid shell session in state, recreating..."
            )
        
        # Session missing - recreate it
        logger.info("Shell session missing, recreating (likely after HITL pause)")
        
        # Try to preserve state if requested
        if self.preserve_state and "_shell_session_state" in runtime.state:
            return self._recreate_session_with_state(runtime)
        else:
            return self._create_fresh_session(runtime)
    
    def _create_fresh_session(self, runtime: Any) -> ShellSession:
        """
        Create a fresh shell session with default state.
        
        Args:
            runtime: Runtime context
            
        Returns:
            New shell session
        """
        session = ShellSession(self.workspace_root)
        runtime.state["_shell_session"] = session
        
        logger.debug(f"Created fresh shell session at {self.workspace_root}")
        return session
    
    def _recreate_session_with_state(self, runtime: Any) -> ShellSession:
        """
        Recreate shell session with preserved state.
        
        This attempts to restore the working directory and environment variables
        from a previous session.
        
        Args:
            runtime: Runtime context with preserved state
            
        Returns:
            New shell session with restored state
        """
        preserved = runtime.state["_shell_session_state"]
        
        # Create new session
        session = ShellSession(self.workspace_root)
        
        # Restore working directory
        if "working_dir" in preserved:
            try:
                working_dir = Path(preserved["working_dir"])
                if working_dir.exists() and working_dir.is_dir():
                    session.working_dir = working_dir
                    logger.debug(f"Restored working directory: {working_dir}")
                else:
                    logger.warning(
                        f"Cannot restore working dir {working_dir} (doesn't exist)"
                    )
            except Exception as e:
                logger.warning(f"Failed to restore working directory: {e}")
        
        # Restore environment variables
        if "env" in preserved:
            try:
                # Merge preserved env vars (don't overwrite system vars completely)
                for key, value in preserved["env"].items():
                    session.env[key] = value
                logger.debug(
                    f"Restored {len(preserved['env'])} environment variables"
                )
            except Exception as e:
                logger.warning(f"Failed to restore environment variables: {e}")
        
        # Store session
        runtime.state["_shell_session"] = session
        
        logger.info(
            f"Recreated shell session with preserved state at {session.working_dir}"
        )
        return session
    
    def _preserve_session_state(self, runtime: Any) -> None:
        """
        Preserve session state for potential recreation.
        
        This saves the session's working directory and environment variables
        so they can be restored if the session needs to be recreated.
        
        Args:
            runtime: Runtime context
        """
        if "_shell_session" not in runtime.state:
            return
        
        session = runtime.state["_shell_session"]
        if not isinstance(session, ShellSession):
            return
        
        # Save state that we want to preserve
        runtime.state["_shell_session_state"] = {
            "working_dir": str(session.working_dir),
            "env": dict(session.env),
            "history_count": len(session.history)
        }
        
        logger.debug("Preserved shell session state for potential recreation")
    
    def before_agent(self, state: Dict[str, Any], runtime: Any) -> Optional[Dict[str, Any]]:
        """
        Hook called before agent execution.
        
        This ensures the session exists before any shell commands are executed.
        Useful for pre-warming the session after a resume.
        
        Args:
            state: Agent state
            runtime: Runtime context
            
        Returns:
            Optional state updates
        """
        # Pre-create session if needed (lazy initialization)
        # This ensures session is ready before any tool calls
        if self.preserve_state:
            self._preserve_session_state(runtime)
        
        return None
    
    def after_agent(self, state: Dict[str, Any], runtime: Any) -> Optional[Dict[str, Any]]:
        """
        Hook called after agent execution.
        
        This preserves session state for potential recreation after HITL pauses.
        
        Args:
            state: Agent state
            runtime: Runtime context
            
        Returns:
            Optional state updates
        """
        # Preserve state for potential recreation
        if self.preserve_state:
            self._preserve_session_state(runtime)
        
        return None
    
    def cleanup(self, runtime: Any) -> None:
        """
        Clean up shell session resources.
        
        Only performs cleanup if a session actually exists. This prevents
        errors when cleanup is called after HITL pause (when session might
        be missing).
        
        Args:
            runtime: Runtime context
        """
        if "_shell_session" in runtime.state:
            session = runtime.state["_shell_session"]
            if isinstance(session, ShellSession):
                logger.debug("Cleaning up shell session")
                # Shell session cleanup (if needed in future)
                # For now, just remove from state
                del runtime.state["_shell_session"]
            
        # Also clean up preserved state
        if "_shell_session_state" in runtime.state:
            del runtime.state["_shell_session_state"]
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get middleware statistics.

        Returns:
            Dictionary with middleware statistics
        """
        return {
            "middleware": "ResumableShellToolMiddleware",
            "workspace_root": str(self.workspace_root),
            "preserve_state": self.preserve_state,
            "execution_policy": str(self.execution_policy) if self.execution_policy else None,
            "description": "Shell middleware with HITL resume support"
        }


# Export
__all__ = ["ResumableShellToolMiddleware"]
