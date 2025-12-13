"""Middleware for long-term agent memory across sessions.

This middleware provides agents with automatic memory management that persists
important conversations, learnings, and context across sessions.
"""

from typing import Any, Callable
from datetime import datetime
from pathlib import Path

from azcore.middleware.base import MiddlewareBase
from azcore.backends.protocol import BackendProtocol
from azcore.backends.filesystem import FilesystemBackend


AGENT_MEMORY_SYSTEM_PROMPT = """## Long-Term Memory System

You have access to a long-term memory system stored in /memories/.

**Memory Guidelines:**

1. **Check memories at session start:**
   - Run `ls /memories/` to see what you remember
   - Read relevant memory files before answering questions
   
2. **Save important information:**
   - User preferences and habits
   - Project context and decisions
   - Important learnings and insights
   - Recurring patterns or frequent requests

3. **Organize memories:**
   - Use clear, descriptive filenames
   - Group related memories in subdirectories
   - Update existing memories rather than duplicating

4. **Memory structure suggestions:**
   - `/memories/preferences.md` - User preferences
   - `/memories/projects/` - Project-specific notes
   - `/memories/learnings/` - Important learnings
   - `/memories/contacts/` - People and relationships
   - `/memories/habits/` - User patterns and routines

5. **When to save memories:**
   - User explicitly asks you to remember something
   - User shares personal preferences
   - Important project decisions or context
   - Recurring patterns you notice
   - Context that would be useful in future sessions

6. **When asked "what do you know about X?":**
   - FIRST check `/memories/` for saved information
   - Read relevant memory files
   - Combine saved memories with general knowledge
   - Be clear about what's from memory vs. general knowledge

**Memory Best Practices:**
- Base answers on saved memories when available
- Keep memories organized and up-to-date
- Don't save trivial or temporary information
- Update existing memories rather than creating duplicates
- Use clear, searchable filenames

Your memories persist across all sessions, making you more helpful over time!"""


class SaveMemoryTool:
    """Tool for saving information to long-term memory."""
    
    def __init__(self, backend: BackendProtocol, memory_path: str = "/memories/"):
        """Initialize save_memory tool.
        
        Args:
            backend: Backend for persistent storage.
            memory_path: Base path for memory storage.
        """
        self.backend = backend
        self.memory_path = memory_path.rstrip("/") + "/"
        self.name = "save_memory"
        self.description = """Save information to long-term memory.

This persists important information across sessions. Use it to remember:
- User preferences and habits
- Project context and decisions
- Important learnings
- Recurring patterns

Args:
    filename: Name of memory file (e.g., "preferences.md", "projects/myproject.md")
    content: Content to save
    append: If True, append to existing file; if False, overwrite

Example:
    save_memory("preferences.md", "User prefers Python over JavaScript")
    save_memory("projects/website.md", "Project context...", append=True)
"""
    
    def __call__(
        self,
        filename: str,
        content: str,
        append: bool = False,
        runtime: Any = None,
    ) -> dict[str, Any]:
        """Save information to memory.
        
        Args:
            filename: Name of the memory file.
            content: Content to save.
            append: Whether to append to existing file.
            runtime: Runtime context.
            
        Returns:
            Result of the save operation.
        """
        # Ensure filename is within memory path
        if not filename.startswith("/"):
            full_path = self.memory_path + filename
        else:
            full_path = filename
        
        # Add timestamp to content
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        timestamped_content = f"[Saved: {timestamp}]\n\n{content}"
        
        # Handle append mode
        if append:
            # Read existing content
            existing = self.backend.read(full_path)
            if not existing.startswith("Error:"):
                # Extract content without line numbers
                lines = existing.split("\n")
                existing_content = "\n".join([
                    line.split("\t", 1)[1] if "\t" in line else line
                    for line in lines
                ])
                timestamped_content = existing_content + "\n\n---\n\n" + timestamped_content
                
                # Edit the file
                result = self.backend.edit(
                    full_path,
                    old_string=existing_content,
                    new_string=timestamped_content
                )
                
                if result.error:
                    return {"error": result.error}
                return {
                    "message": f"✓ Appended to memory: {full_path}",
                    "path": full_path
                }
        
        # Write new file
        result = self.backend.write(full_path, timestamped_content)
        
        if result.error:
            return {"error": result.error}
        
        return {
            "message": f"✓ Saved to memory: {full_path}",
            "path": full_path
        }


class RecallMemoryTool:
    """Tool for recalling information from long-term memory."""
    
    def __init__(self, backend: BackendProtocol, memory_path: str = "/memories/"):
        """Initialize recall_memory tool.
        
        Args:
            backend: Backend for persistent storage.
            memory_path: Base path for memory storage.
        """
        self.backend = backend
        self.memory_path = memory_path.rstrip("/") + "/"
        self.name = "recall_memory"
        self.description = """Recall information from long-term memory.

Search and retrieve saved memories. Use this to:
- Find what you know about a topic
- Retrieve user preferences
- Access project context
- Review past learnings

Args:
    query: Search query (optional, returns all memories if omitted)
    filename: Specific file to read (optional)

Example:
    recall_memory(query="preferences")  # Search for preferences
    recall_memory(filename="projects/website.md")  # Read specific file
"""
    
    def __call__(
        self,
        query: str | None = None,
        filename: str | None = None,
        runtime: Any = None,
    ) -> dict[str, Any]:
        """Recall information from memory.
        
        Args:
            query: Optional search query.
            filename: Optional specific file to read.
            runtime: Runtime context.
            
        Returns:
            Recalled memory content.
        """
        # If filename specified, read that file directly
        if filename:
            if not filename.startswith("/"):
                full_path = self.memory_path + filename
            else:
                full_path = filename
            
            content = self.backend.read(full_path)
            if content.startswith("Error:"):
                return {"error": content}
            
            return {
                "message": f"📖 Memory from {full_path}",
                "content": content,
                "path": full_path
            }
        
        # Otherwise, search memories
        if query:
            matches = self.backend.grep_raw(query, path=self.memory_path)
            
            if isinstance(matches, str):
                return {"error": matches}
            
            if not matches:
                return {"message": f"No memories found matching: {query}"}
            
            # Format results
            results = []
            for match in matches[:10]:  # Limit to top 10
                results.append(f"• {match['path']}:{match['line']} - {match['text'][:100]}")
            
            return {
                "message": f"Found {len(matches)} memory entries matching '{query}':",
                "results": "\n".join(results),
                "matches": matches
            }
        
        # No query or filename - list all memories
        files = self.backend.ls_info(self.memory_path)
        if not files:
            return {"message": "No memories saved yet. Use save_memory to create some!"}
        
        file_list = []
        for file_info in files:
            if file_info.get("is_dir"):
                file_list.append(f"📁 {file_info['path']}")
            else:
                size = file_info.get("size", 0)
                file_list.append(f"📄 {file_info['path']} ({size} bytes)")
        
        return {
            "message": f"📋 Available memories ({len(files)} items):",
            "files": "\n".join(file_list)
        }


class AgentMemoryMiddleware(MiddlewareBase):
    """Middleware for long-term agent memory across sessions.
    
    This middleware provides agents with automatic memory management using
    persistent storage. Agents can save and recall important information
    that persists across sessions.
    
    Args:
        backend: Backend for persistent storage (e.g., FilesystemBackend).
        memory_path: Base path for memory storage (default: /memories/).
        auto_save_threshold: Auto-save important messages after N exchanges.
        system_prompt: Custom system prompt override.
    
    Example:
        ```python
        from azcore.middleware import AgentMemoryMiddleware
        from azcore.backends import FilesystemBackend
        from azcore.agents import AgentFactory
        from pathlib import Path
        
        # Setup persistent memory backend
        memory_dir = Path.home() / ".azcore" / "agent_memories"
        memory_dir.mkdir(parents=True, exist_ok=True)
        
        backend = FilesystemBackend(
            root_dir=memory_dir,
            virtual_mode=True
        )
        
        # Create memory middleware
        middleware = AgentMemoryMiddleware(
            backend=backend,
            memory_path="/memories/"
        )
        
        # Apply to agent
        agent = AgentFactory.create_agent(name="assistant")
        middleware.setup(agent)
        
        # Agent now has long-term memory!
        # Can use: save_memory(), recall_memory()
        ```
    """
    
    def __init__(
        self,
        *,
        backend: BackendProtocol | None = None,
        memory_path: str = "/memories/",
        auto_save_threshold: int | None = None,
        system_prompt: str | None = None,
    ):
        """Initialize agent memory middleware."""
        # Use provided backend or create default
        if backend is None:
            from pathlib import Path
            default_dir = Path.home() / ".azcore" / "memories"
            default_dir.mkdir(parents=True, exist_ok=True)
            backend = FilesystemBackend(root_dir=default_dir, virtual_mode=True)
        
        self.backend = backend
        self.memory_path = memory_path
        self.auto_save_threshold = auto_save_threshold
        self.system_prompt = system_prompt if system_prompt is not None else AGENT_MEMORY_SYSTEM_PROMPT
        
        # Create memory tools
        self.save_memory_tool = SaveMemoryTool(backend, memory_path)
        self.recall_memory_tool = RecallMemoryTool(backend, memory_path)
        
        # Track conversation for auto-save
        self.conversation_count = 0
    
    def setup(self, agent: Any) -> None:
        """Setup middleware with agent."""
        # Add memory tools to agent
        if hasattr(agent, "tools"):
            # Get existing tool names, handling both tool objects and functions
            existing_tool_names = []
            for t in agent.tools:
                if hasattr(t, 'name'):
                    existing_tool_names.append(t.name)
                elif callable(t) and hasattr(t, '__name__'):
                    existing_tool_names.append(t.__name__)

            if self.save_memory_tool.name not in existing_tool_names:
                agent.tools.append(self.save_memory_tool)
            if self.recall_memory_tool.name not in existing_tool_names:
                agent.tools.append(self.recall_memory_tool)
    
    def wrap_model_call(
        self,
        request: dict[str, Any],
        handler: Callable[[dict[str, Any]], dict[str, Any]],
    ) -> dict[str, Any]:
        """Update system prompt to include memory instructions."""
        if self.system_prompt is not None:
            existing_prompt = request.get("system_prompt", "")
            if existing_prompt:
                request["system_prompt"] = existing_prompt + "\n\n" + self.system_prompt
            else:
                request["system_prompt"] = self.system_prompt
        
        # Handle auto-save if enabled
        if self.auto_save_threshold:
            self.conversation_count += 1
            if self.conversation_count >= self.auto_save_threshold:
                self._auto_save_conversation(request)
                self.conversation_count = 0
        
        return handler(request)
    
    def _auto_save_conversation(self, request: dict[str, Any]) -> None:
        """Auto-save important conversation context."""
        messages = request.get("messages", [])
        if len(messages) > 2:
            # Extract key information from recent messages
            recent = messages[-5:]  # Last 5 messages
            summary = self._summarize_messages(recent)
            
            if summary:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"auto_save_{timestamp}.md"
                
                self.save_memory_tool(
                    filename=f"conversations/{filename}",
                    content=summary,
                    append=False
                )
    
    def _summarize_messages(self, messages: list[Any]) -> str:
        """Create a summary of messages for auto-save.
        
        Args:
            messages: List of message objects or dicts.
            
        Returns:
            Summary string.
        """
        lines = ["# Conversation Summary\n"]
        
        for msg in messages:
            if isinstance(msg, dict):
                role = msg.get("role", "unknown")
                content = msg.get("content", "")
            else:
                role = getattr(msg, "role", "unknown")
                content = getattr(msg, "content", "")
            
            if content and len(content) > 20:
                lines.append(f"**{role.title()}:** {content[:200]}...")
        
        return "\n\n".join(lines) if len(lines) > 1 else ""
