"""Middleware for providing filesystem tools to an agent."""

import os
from typing import Any, Callable, Literal
from pathlib import Path

from azcore.middleware.base import MiddlewareBase
from azcore.backends.protocol import BackendProtocol, BackendFactory
from azcore.backends.state import StateBackend
from azcore.backends.utils import (
    format_grep_matches,
    truncate_if_too_long,
    sanitize_tool_call_id,
    format_content_with_line_numbers,
)


# Tool descriptions
LIST_FILES_TOOL_DESCRIPTION = """Lists all files in the filesystem, filtering by directory.

Usage:
- The path parameter must be an absolute path, not a relative path
- Returns a list of all files in the specified directory
- Very useful for exploring the file system and finding the right file
- You should almost ALWAYS use this tool before using the Read or Edit tools"""

READ_FILE_TOOL_DESCRIPTION = """Reads a file from the filesystem.

Usage:
- The file_path parameter must be an absolute path
- By default, reads up to 500 lines from the beginning
- Use offset and limit parameters for pagination
- Results use cat -n format with line numbers starting at 1
- You should ALWAYS read a file before editing it"""

EDIT_FILE_TOOL_DESCRIPTION = """Performs exact string replacements in files.

Usage:
- You must use Read tool before editing
- Preserve exact indentation from the file
- The edit will FAIL if `old_string` is not unique
- Use `replace_all` to replace all instances
- Only use emojis if the user explicitly requests it"""

WRITE_FILE_TOOL_DESCRIPTION = """Writes to a new file in the filesystem.

Usage:
- The file_path parameter must be an absolute path
- Creates a new file with the specified content
- Prefer editing existing files over creating new ones"""

GLOB_TOOL_DESCRIPTION = """Find files matching a glob pattern.

Usage:
- Supports standard glob patterns: `*`, `**`, `?`
- Returns a list of absolute file paths
Examples:
- `**/*.py` - Find all Python files
- `*.txt` - Find all text files in root"""

GREP_TOOL_DESCRIPTION = """Search for a pattern in files.

Usage:
- The pattern parameter is the text to search for
- The path parameter filters which directory to search in
- The glob parameter filters which files to search
- The output_mode parameter controls the output format
Examples:
- Search all files: `grep(pattern="TODO")`
- Search Python files: `grep(pattern="import", glob="*.py")`"""

FILESYSTEM_SYSTEM_PROMPT = """## Filesystem Tools

You have access to a filesystem which you can interact with using these tools:
- ls: list files in a directory (requires absolute path)
- read_file: read a file from the filesystem
- write_file: write to a file in the filesystem
- edit_file: edit a file in the filesystem
- glob: find files matching a pattern (e.g., "**/*.py")
- grep: search for text within files

All file paths must start with a /."""


class FilesystemTool:
    """Base class for filesystem tools."""
    
    def __init__(self, backend: BackendProtocol | Callable, description: str = ""):
        self.backend = backend
        self.description = description
        self.name = ""

    def _get_backend(self, runtime: Any) -> BackendProtocol:
        """Get the resolved backend instance."""
        if callable(self.backend):
            return self.backend(runtime)
        return self.backend

    def __call__(self, **kwargs):
        """Execute the tool."""
        raise NotImplementedError


class LsTool(FilesystemTool):
    """List files tool."""
    
    def __init__(self, backend: BackendProtocol | Callable, description: str = ""):
        super().__init__(backend, description or LIST_FILES_TOOL_DESCRIPTION)
        self.name = "ls"

    def __call__(self, runtime: Any, path: str) -> list[str]:
        """List files in a directory."""
        resolved_backend = self._get_backend(runtime)
        infos = resolved_backend.ls_info(path)
        return [fi.get("path", "") for fi in infos]


class ReadFileTool(FilesystemTool):
    """Read file tool."""
    
    def __init__(self, backend: BackendProtocol | Callable, description: str = ""):
        super().__init__(backend, description or READ_FILE_TOOL_DESCRIPTION)
        self.name = "read_file"

    def __call__(
        self,
        file_path: str,
        runtime: Any,
        offset: int = 0,
        limit: int = 500,
    ) -> str:
        """Read file content."""
        resolved_backend = self._get_backend(runtime)
        # Validate path
        if ".." in file_path or file_path.startswith("~"):
            return "Error: Path traversal not allowed"
        normalized = os.path.normpath(file_path).replace("\\", "/")
        if not normalized.startswith("/"):
            normalized = f"/{normalized}"
        return resolved_backend.read(normalized, offset=offset, limit=limit)


class WriteFileTool(FilesystemTool):
    """Write file tool."""
    
    def __init__(self, backend: BackendProtocol | Callable, description: str = ""):
        super().__init__(backend, description or WRITE_FILE_TOOL_DESCRIPTION)
        self.name = "write_file"

    def __call__(
        self,
        file_path: str,
        content: str,
        runtime: Any,
    ) -> dict[str, Any] | str:
        """Write file content."""
        resolved_backend = self._get_backend(runtime)
        # Validate path
        if ".." in file_path or file_path.startswith("~"):
            return "Error: Path traversal not allowed"
        normalized = os.path.normpath(file_path).replace("\\", "/")
        if not normalized.startswith("/"):
            normalized = f"/{normalized}"
        
        res = resolved_backend.write(normalized, content)
        if res.error:
            return res.error
        # Return state update if available, otherwise success message
        if res.files_update is not None:
            return {
                "files": res.files_update,
                "message": f"Updated file {res.path}",
            }
        return f"Updated file {res.path}"


class EditFileTool(FilesystemTool):
    """Edit file tool."""
    
    def __init__(self, backend: BackendProtocol | Callable, description: str = ""):
        super().__init__(backend, description or EDIT_FILE_TOOL_DESCRIPTION)
        self.name = "edit_file"

    def __call__(
        self,
        file_path: str,
        old_string: str,
        new_string: str,
        runtime: Any,
        replace_all: bool = False,
    ) -> dict[str, Any] | str:
        """Edit file by replacing strings."""
        resolved_backend = self._get_backend(runtime)
        # Validate path
        if ".." in file_path or file_path.startswith("~"):
            return "Error: Path traversal not allowed"
        normalized = os.path.normpath(file_path).replace("\\", "/")
        if not normalized.startswith("/"):
            normalized = f"/{normalized}"
        
        res = resolved_backend.edit(normalized, old_string, new_string, replace_all=replace_all)
        if res.error:
            return res.error
        if res.files_update is not None:
            return {
                "files": res.files_update,
                "message": f"Successfully replaced {res.occurrences} instance(s) in '{res.path}'",
            }
        return f"Successfully replaced {res.occurrences} instance(s) in '{res.path}'"


class GlobTool(FilesystemTool):
    """Glob search tool."""
    
    def __init__(self, backend: BackendProtocol | Callable, description: str = ""):
        super().__init__(backend, description or GLOB_TOOL_DESCRIPTION)
        self.name = "glob"

    def __call__(self, pattern: str, runtime: Any, path: str = "/") -> list[str]:
        """Find files matching a glob pattern."""
        resolved_backend = self._get_backend(runtime)
        infos = resolved_backend.glob_info(pattern, path=path)
        return [fi.get("path", "") for fi in infos]


class GrepTool(FilesystemTool):
    """Grep search tool."""
    
    def __init__(self, backend: BackendProtocol | Callable, description: str = ""):
        super().__init__(backend, description or GREP_TOOL_DESCRIPTION)
        self.name = "grep"

    def __call__(
        self,
        pattern: str,
        runtime: Any,
        path: str | None = None,
        glob: str | None = None,
        output_mode: Literal["files_with_matches", "content", "count"] = "files_with_matches",
    ) -> str:
        """Search for pattern in files."""
        resolved_backend = self._get_backend(runtime)
        raw = resolved_backend.grep_raw(pattern, path=path, glob=glob)
        if isinstance(raw, str):
            return raw
        formatted = format_grep_matches(raw, output_mode)
        return truncate_if_too_long(formatted)


# Collection of all filesystem tools
FILESYSTEM_TOOLS = {
    "ls": LsTool,
    "read_file": ReadFileTool,
    "write_file": WriteFileTool,
    "edit_file": EditFileTool,
    "glob": GlobTool,
    "grep": GrepTool,
}


class FilesystemMiddleware(MiddlewareBase):
    """Middleware for providing filesystem tools to an agent.

    This middleware adds six filesystem tools: ls, read_file, write_file,
    edit_file, glob, and grep. Files can be stored using any backend.
    
    Args:
        backend: Backend for file storage. Defaults to StateBackend if not provided.
        system_prompt: Optional custom system prompt override.
        custom_tool_descriptions: Optional custom tool descriptions.
        tool_token_limit_before_evict: Token limit before evicting large tool results.
    
    Example:
        ```python
        from azcore.middleware import FilesystemMiddleware
        from azcore.backends import StateBackend, CompositeBackend
        
        # Ephemeral storage only
        middleware = FilesystemMiddleware()
        
        # With hybrid storage
        backend = CompositeBackend(
            default=StateBackend(),
            routes={"/memories/": StoreBackend()}
        )
        middleware = FilesystemMiddleware(backend=backend)
        ```
    """

    def __init__(
        self,
        *,
        backend: BackendProtocol | BackendFactory | None = None,
        system_prompt: str | None = None,
        custom_tool_descriptions: dict[str, str] | None = None,
        tool_token_limit_before_evict: int | None = 20000,
    ) -> None:
        """Initialize the filesystem middleware."""
        self.tool_token_limit_before_evict = tool_token_limit_before_evict
        
        # Use provided backend or default to StateBackend factory
        self.backend = backend if backend is not None else (lambda rt: StateBackend(rt))
        
        # Set system prompt
        self.system_prompt = system_prompt if system_prompt is not None else FILESYSTEM_SYSTEM_PROMPT
        
        # Create tools
        self.tools = self._create_tools(custom_tool_descriptions or {})

    def _create_tools(self, custom_descriptions: dict[str, str]) -> dict[str, FilesystemTool]:
        """Create filesystem tool instances."""
        tools = {}
        for tool_name, tool_class in FILESYSTEM_TOOLS.items():
            description = custom_descriptions.get(tool_name, "")
            tools[tool_name] = tool_class(self.backend, description)
        return tools

    def setup(self, agent: Any) -> None:
        """Setup middleware with the agent."""
        # Add filesystem tools to agent
        if hasattr(agent, "tools"):
            # Get existing tool names, handling both tool objects and functions
            existing_tool_names = []
            for t in agent.tools:
                if hasattr(t, 'name'):
                    existing_tool_names.append(t.name)
                elif callable(t) and hasattr(t, '__name__'):
                    existing_tool_names.append(t.__name__)

            for tool in self.tools.values():
                if tool.name not in existing_tool_names:
                    agent.tools.append(tool)

    def wrap_model_call(
        self,
        request: dict[str, Any],
        handler: Callable[[dict[str, Any]], dict[str, Any]],
    ) -> dict[str, Any]:
        """Update the system prompt to include filesystem instructions."""
        if self.system_prompt is not None:
            existing_prompt = request.get("system_prompt", "")
            if existing_prompt:
                request["system_prompt"] = existing_prompt + "\n\n" + self.system_prompt
            else:
                request["system_prompt"] = self.system_prompt
        return handler(request)

    def _process_large_message(
        self,
        message: Any,
        resolved_backend: BackendProtocol,
    ) -> tuple[Any, dict[str, Any] | None]:
        """Process large tool result messages."""
        content = getattr(message, "content", None)
        if not isinstance(content, str) or len(content) <= 4 * self.tool_token_limit_before_evict:
            return message, None

        # Save large result to filesystem
        tool_call_id = getattr(message, "tool_call_id", "unknown")
        sanitized_id = sanitize_tool_call_id(tool_call_id)
        file_path = f"/large_tool_results/{sanitized_id}"
        result = resolved_backend.write(file_path, content)
        
        if result.error:
            return message, None
        
        # Create truncated message
        content_sample = format_content_with_line_numbers(content.splitlines()[:10], start_line=1)
        new_content = (
            f"Tool result too large, saved to filesystem at: {file_path}\n"
            f"Read the result using the read_file tool with offset and limit parameters.\n\n"
            f"First 10 lines:\n{content_sample}"
        )
        
        # Create new message with truncated content
        processed_message = type(message)(
            content=new_content,
            tool_call_id=tool_call_id
        )
        return processed_message, result.files_update
