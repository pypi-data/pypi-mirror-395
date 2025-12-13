"""
Resumable Shell Middleware for Azcore.

This middleware provides persistent shell sessions that maintain state across
multiple commands. It tracks working directory, environment variables, and
command history for a seamless shell experience.
"""

from typing import Any, Dict, List, Optional, Protocol, TypedDict, Literal, Union
import subprocess
import os
import sys
from pathlib import Path
from ..utils.logging import get_logger

logger = get_logger(__name__)


class Tool(TypedDict):
    """Tool definition."""
    name: str
    description: str
    parameters: Dict[str, Any]


class Runtime(Protocol):
    """Runtime protocol for middleware."""
    state: Dict[str, Any]


class ShellSession:
    """
    Represents a persistent shell session.
    
    Maintains state across multiple command executions including:
    - Working directory
    - Environment variables
    - Command history
    """
    
    def __init__(self, workspace_root: Optional[Path] = None):
        """
        Initialize shell session.
        
        Args:
            workspace_root: Root directory for the workspace
        """
        self.workspace_root = workspace_root or Path.cwd()
        self.working_dir = self.workspace_root
        self.env = dict(os.environ)
        self.history: List[Dict[str, Any]] = []
        
    def execute_command(
        self,
        command: str,
        timeout: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Execute a command in the shell session.
        
        Args:
            command: Command to execute
            timeout: Timeout in seconds (None = no timeout)
            
        Returns:
            Dictionary with stdout, stderr, returncode, and working_dir
        """
        try:
            # Handle cd commands specially to maintain state
            if command.strip().startswith("cd "):
                return self._handle_cd(command)
            
            # Handle environment variable exports
            if command.strip().startswith("export "):
                return self._handle_export(command)
            
            # Execute command
            result = subprocess.run(
                command,
                shell=True,
                cwd=str(self.working_dir),
                env=self.env,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            
            output = {
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode,
                "working_dir": str(self.working_dir),
                "command": command
            }
            
            # Add to history
            self.history.append({
                "command": command,
                "returncode": result.returncode,
                "working_dir": str(self.working_dir)
            })
            
            return output
            
        except subprocess.TimeoutExpired:
            return {
                "stdout": "",
                "stderr": f"Command timed out after {timeout} seconds",
                "returncode": -1,
                "working_dir": str(self.working_dir),
                "command": command
            }
        except Exception as e:
            return {
                "stdout": "",
                "stderr": f"Error executing command: {str(e)}",
                "returncode": -1,
                "working_dir": str(self.working_dir),
                "command": command
            }
    
    def _handle_cd(self, command: str) -> Dict[str, Any]:
        """Handle cd command to change working directory."""
        parts = command.strip().split(maxsplit=1)
        if len(parts) < 2:
            # cd with no args goes to home
            new_dir = Path.home()
        else:
            target = parts[1].strip()
            
            # Handle special cases
            if target == "~":
                new_dir = Path.home()
            elif target == "-":
                # Go back to previous directory (not implemented yet)
                return {
                    "stdout": "",
                    "stderr": "cd -: Previous directory tracking not implemented",
                    "returncode": 1,
                    "working_dir": str(self.working_dir),
                    "command": command
                }
            else:
                # Resolve relative to current working dir
                new_dir = (self.working_dir / target).resolve()
        
        # Check if directory exists
        if not new_dir.exists():
            return {
                "stdout": "",
                "stderr": f"cd: {new_dir}: No such file or directory",
                "returncode": 1,
                "working_dir": str(self.working_dir),
                "command": command
            }
        
        if not new_dir.is_dir():
            return {
                "stdout": "",
                "stderr": f"cd: {new_dir}: Not a directory",
                "returncode": 1,
                "working_dir": str(self.working_dir),
                "command": command
            }
        
        # Change directory
        old_dir = self.working_dir
        self.working_dir = new_dir
        
        self.history.append({
            "command": command,
            "returncode": 0,
            "working_dir": str(self.working_dir)
        })
        
        return {
            "stdout": f"Changed directory: {old_dir} → {new_dir}",
            "stderr": "",
            "returncode": 0,
            "working_dir": str(self.working_dir),
            "command": command
        }
    
    def _handle_export(self, command: str) -> Dict[str, Any]:
        """Handle export command for environment variables."""
        try:
            # Parse export command: export VAR=value
            parts = command.strip().split(maxsplit=1)
            if len(parts) < 2:
                return {
                    "stdout": "",
                    "stderr": "export: usage: export VAR=value",
                    "returncode": 1,
                    "working_dir": str(self.working_dir),
                    "command": command
                }
            
            assignment = parts[1].strip()
            if "=" not in assignment:
                return {
                    "stdout": "",
                    "stderr": f"export: invalid assignment: {assignment}",
                    "returncode": 1,
                    "working_dir": str(self.working_dir),
                    "command": command
                }
            
            var_name, var_value = assignment.split("=", 1)
            var_name = var_name.strip()
            var_value = var_value.strip().strip('"').strip("'")
            
            # Set environment variable
            self.env[var_name] = var_value
            
            self.history.append({
                "command": command,
                "returncode": 0,
                "working_dir": str(self.working_dir)
            })
            
            return {
                "stdout": f"Exported: {var_name}={var_value}",
                "stderr": "",
                "returncode": 0,
                "working_dir": str(self.working_dir),
                "command": command
            }
            
        except Exception as e:
            return {
                "stdout": "",
                "stderr": f"export: error: {str(e)}",
                "returncode": 1,
                "working_dir": str(self.working_dir),
                "command": command
            }


class ShellMiddleware:
    """
    Middleware that provides resumable shell session capabilities.
    
    This middleware adds shell execution tools that maintain persistent state
    across commands. Unlike one-off shell executions, this tracks:
    - Working directory (cd commands persist)
    - Environment variables (export commands persist)
    - Command history
    - Session state
    
    Example:
        ```python
        from azcore.middleware import ShellMiddleware
        from azcore.agents import AgentFactory
        from pathlib import Path
        
        middleware = ShellMiddleware(
            workspace_root=Path("/path/to/project")
        )
        
        agent = AgentFactory.create_agent(name="dev_agent")
        middleware.setup(agent)
        
        # Agent can now use: shell(command, timeout)
        # Commands maintain state (cd, export, etc.)
        ```
    
    Attributes:
        workspace_root: Root directory for shell sessions
    """
    
    def __init__(self, workspace_root: Optional[Union[str, Path]] = None):
        """
        Initialize shell middleware.

        Args:
            workspace_root: Root directory for the workspace (default: cwd)
                          Can be a string or Path object
        """
        # Convert string to Path if needed
        if workspace_root is not None:
            self.workspace_root = Path(workspace_root) if not isinstance(workspace_root, Path) else workspace_root
        else:
            self.workspace_root = Path.cwd()
        self.agent = None
        
    def setup(self, agent: Any) -> None:
        """
        Setup middleware on an agent.
        
        Args:
            agent: The agent to add shell capabilities to
        """
        self.agent = agent
        
        # Add shell tool
        shell_tool = self._create_shell_tool()
        
        if not hasattr(agent, 'tools'):
            agent.tools = []
        
        agent.tools.append(shell_tool)
        
        logger.info(f"Shell middleware configured for {agent.name}")
        logger.info(f"  Workspace root: {self.workspace_root}")
    
    def _create_shell_tool(self) -> Any:
        """Create the shell execution tool."""
        
        class ShellTool:
            """Tool for executing shell commands."""
            
            def __init__(self, middleware: 'ShellMiddleware'):
                self.middleware = middleware
                self.name = "shell"
                self.description = """Execute shell commands in a persistent session.
                
The shell maintains state across commands:
- cd commands change the working directory permanently
- export commands set environment variables permanently  
- Command history is tracked

Args:
    command: The shell command to execute
    timeout: Optional timeout in seconds (default: None)

Returns:
    Dictionary with stdout, stderr, returncode, and working_dir
    
Examples:
    shell("ls -la")
    shell("cd /path/to/dir")
    shell("export MY_VAR=value")
    shell("python script.py", timeout=30)
"""
                self.parameters = {
                    "type": "object",
                    "properties": {
                        "command": {
                            "type": "string",
                            "description": "The shell command to execute"
                        },
                        "timeout": {
                            "type": "integer",
                            "description": "Timeout in seconds (optional)",
                            "default": None
                        }
                    },
                    "required": ["command"]
                }
            
            def __call__(
                self,
                command: str,
                timeout: Optional[int] = None,
                runtime: Optional[Runtime] = None
            ) -> Dict[str, Any]:
                """Execute shell command."""
                return self.middleware.shell_tool(command, timeout, runtime)
        
        return ShellTool(self)
    
    def _get_session(self, runtime: Runtime) -> ShellSession:
        """Get or create shell session for runtime."""
        if "_shell_session" not in runtime.state:
            runtime.state["_shell_session"] = ShellSession(self.workspace_root)
        return runtime.state["_shell_session"]
    
    def shell_tool(
        self,
        command: str,
        timeout: Optional[int] = None,
        runtime: Optional[Runtime] = None
    ) -> Dict[str, Any]:
        """
        Execute a shell command in the persistent session.
        
        Args:
            command: The shell command to execute
            timeout: Optional timeout in seconds
            runtime: Runtime context (required)
            
        Returns:
            Dictionary with execution results
        """
        if not runtime:
            return {
                "error": "Runtime context required",
                "stdout": "",
                "stderr": "No runtime context provided",
                "returncode": -1
            }
        
        try:
            # Get session
            session = self._get_session(runtime)
            
            # Execute command
            result = session.execute_command(command, timeout)
            
            # Format response
            response = {
                "stdout": result["stdout"],
                "stderr": result["stderr"],
                "returncode": result["returncode"],
                "working_dir": result["working_dir"],
                "message": self._format_result(result)
            }
            
            return response
            
        except Exception as e:
            logger.error(f"Shell command failed: {e}")
            return {
                "error": str(e),
                "stdout": "",
                "stderr": str(e),
                "returncode": -1,
                "message": f"❌ Shell error: {str(e)}"
            }
    
    def _format_result(self, result: Dict[str, Any]) -> str:
        """Format shell execution result for display."""
        lines = []
        
        # Command info
        lines.append(f"📁 Working Dir: {result['working_dir']}")
        lines.append(f"🔧 Command: {result['command']}")
        
        # Output
        if result["stdout"]:
            lines.append("")
            lines.append("📤 Output:")
            lines.append(result["stdout"])
        
        if result["stderr"]:
            lines.append("")
            lines.append("⚠️  Errors:")
            lines.append(result["stderr"])
        
        # Status
        lines.append("")
        if result["returncode"] == 0:
            lines.append("✅ Command completed successfully")
        else:
            lines.append(f"❌ Command failed with exit code {result['returncode']}")
        
        return "\n".join(lines)
    
    def get_history(self, runtime: Runtime) -> List[Dict[str, Any]]:
        """
        Get command history for the session.
        
        Args:
            runtime: Runtime context
            
        Returns:
            List of executed commands with metadata
        """
        session = self._get_session(runtime)
        return session.history


# Export
__all__ = ["ShellMiddleware", "ShellSession"]
