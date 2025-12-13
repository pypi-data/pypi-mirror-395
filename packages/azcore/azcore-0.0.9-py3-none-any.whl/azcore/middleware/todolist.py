"""Middleware for task management with todo lists.

This middleware provides agents with a `write_todos` tool to manage complex
multi-step tasks. Agents can create, update, and track todo items with
status indicators.
"""

from typing import Any, Callable, Literal
from enum import Enum

from azcore.middleware.base import MiddlewareBase


class TodoStatus(str, Enum):
    """Status of a todo item."""
    NOT_STARTED = "not-started"
    IN_PROGRESS = "in-progress"
    COMPLETED = "completed"


class TodoItem:
    """A single todo item.
    
    Attributes:
        id: Unique identifier for the todo.
        title: Short title (3-7 words).
        description: Detailed description with context.
        status: Current status of the todo.
    """
    
    def __init__(
        self,
        id: int,
        title: str,
        description: str,
        status: TodoStatus = TodoStatus.NOT_STARTED,
    ):
        """Initialize a todo item."""
        self.id = id
        self.title = title
        self.description = description
        self.status = status
    
    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "status": self.status.value,
        }
    
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "TodoItem":
        """Create from dictionary."""
        return cls(
            id=data["id"],
            title=data["title"],
            description=data["description"],
            status=TodoStatus(data.get("status", "not-started")),
        )
    
    def __repr__(self) -> str:
        """String representation."""
        status_symbols = {
            TodoStatus.NOT_STARTED: "⭕",
            TodoStatus.IN_PROGRESS: "🔄",
            TodoStatus.COMPLETED: "✅",
        }
        symbol = status_symbols.get(self.status, "•")
        return f"{symbol} {self.id}. {self.title} [{self.status.value}]"


WRITE_TODOS_TOOL_DESCRIPTION = """Create or update a todo list for tracking complex tasks.

Usage Guidelines:
1. **Keep it MINIMAL**: Aim for 3-6 items maximum
2. **When to create todos**:
   - Complex multi-step tasks requiring tracking
   - Break down work into clear, actionable items
3. **When NOT to create todos**:
   - Simple 1-2 step tasks (just do them!)
   - Trivial operations
4. **Before starting work**:
   - Create the todo list
   - ALWAYS ask the user: "Does this plan look good?"
   - Wait for approval before marking first item as in-progress
5. **Update promptly**: Mark items completed as you finish them

Todo Status Values:
- "not-started": Todo not yet begun
- "in-progress": Currently working (only ONE at a time!)
- "completed": Finished successfully

Example:
```python
write_todos([
    {
        "id": 1,
        "title": "Analyze requirements",
        "description": "Review user requirements and identify key features",
        "status": "not-started"
    },
    {
        "id": 2,
        "title": "Design solution",
        "description": "Create architecture diagram and API design",
        "status": "not-started"
    }
])
```

Remember: The todo list is a planning tool - use it wisely to avoid overwhelming
the user with excessive task tracking."""

TODO_SYSTEM_PROMPT = """## write_todos (task management)

You have access to a `write_todos` tool for managing complex tasks.

When to use:
- Complex multi-step tasks requiring clear tracking
- Breaking down objectives into 3-6 actionable items
- Providing visibility into your work plan

Best practices:
1. Keep the list minimal (3-6 items)
2. Create todos BEFORE starting work on complex tasks
3. ALWAYS ask "Does this plan look good?" after creating todos
4. Wait for user approval before starting
5. Mark only ONE todo as in-progress at a time
6. Update status immediately when completing items

When NOT to use:
- Simple 1-2 step tasks
- Trivial operations
- When the task is already clear and straightforward

Status Management:
- not-started: Default for new todos
- in-progress: Currently working (only one at a time!)
- completed: Mark immediately upon completion

The todo list helps users understand your plan and progress. Use it to improve
transparency and collaboration."""


class WriteTodosTool:
    """Tool for creating and updating todo lists."""
    
    def __init__(self):
        """Initialize write_todos tool."""
        self.name = "write_todos"
        self.description = WRITE_TODOS_TOOL_DESCRIPTION
    
    def __call__(
        self,
        todos: list[dict[str, Any]],
        runtime: Any = None,
    ) -> dict[str, Any]:
        """Create or update todo list.
        
        Args:
            todos: List of todo items with id, title, description, status.
            runtime: Runtime context.
            
        Returns:
            Result with updated todos in state.
        """
        # Validate todos
        if not todos:
            return {"error": "Todo list cannot be empty"}
        
        if len(todos) > 10:
            return {
                "warning": "Todo list is quite long (>10 items). Consider breaking "
                          "into smaller, more manageable chunks."
            }
        
        # Convert to TodoItem objects
        todo_items = []
        in_progress_count = 0
        
        for todo_data in todos:
            try:
                todo = TodoItem.from_dict(todo_data)
                todo_items.append(todo)
                if todo.status == TodoStatus.IN_PROGRESS:
                    in_progress_count += 1
            except Exception as e:
                return {"error": f"Invalid todo item: {str(e)}"}
        
        # Validate: Only one in-progress at a time
        if in_progress_count > 1:
            return {
                "error": "Only one todo can be 'in-progress' at a time. "
                        "Please complete current task before starting another."
            }
        
        # Format output
        output_lines = ["📋 Todo List:"]
        for todo in todo_items:
            output_lines.append(f"   {todo}")
        
        result = {
            "message": "\n".join(output_lines),
            "todos": [t.to_dict() for t in todo_items],
        }
        
        # Update runtime state if available
        if runtime and hasattr(runtime, "state"):
            runtime.state["todos"] = result["todos"]
        
        return result
    
    def format_todos(self, todos: list[dict[str, Any]]) -> str:
        """Format todos for display.
        
        Args:
            todos: List of todo dictionaries.
            
        Returns:
            Formatted string representation.
        """
        if not todos:
            return "📋 No todos"
        
        lines = ["📋 Todo List:"]
        for todo_data in todos:
            todo = TodoItem.from_dict(todo_data)
            lines.append(f"   {todo}")
        
        return "\n".join(lines)


class TodoListMiddleware(MiddlewareBase):
    """Middleware for task management with todo lists.
    
    This middleware adds a `write_todos` tool that allows agents to create
    and manage todo lists for complex multi-step tasks.
    
    Args:
        system_prompt: Custom system prompt override.
        max_todos: Maximum number of todos allowed (default: 10).
        auto_display: Whether to auto-display todos after updates.
    
    Example:
        ```python
        from azcore.middleware import TodoListMiddleware
        from azcore.agents import AgentFactory
        
        # Create todo list middleware
        middleware = TodoListMiddleware()
        
        # Apply to agent
        agent = AgentFactory.create_agent(name="planner")
        middleware.setup(agent)
        
        # Agent can now create and manage todo lists
        # agent.write_todos([
        #     {"id": 1, "title": "Task 1", "description": "...", "status": "not-started"},
        #     {"id": 2, "title": "Task 2", "description": "...", "status": "not-started"}
        # ])
        ```
    """
    
    def __init__(
        self,
        *,
        system_prompt: str | None = None,
        max_todos: int = 10,
        auto_display: bool = True,
    ):
        """Initialize todo list middleware."""
        self.system_prompt = system_prompt if system_prompt is not None else TODO_SYSTEM_PROMPT
        self.max_todos = max_todos
        self.auto_display = auto_display
        
        # Create write_todos tool
        self.write_todos_tool = WriteTodosTool()
    
    def setup(self, agent: Any) -> None:
        """Setup middleware with agent."""
        # Add write_todos tool to agent
        if hasattr(agent, "tools"):
            # Get existing tool names, handling both tool objects and functions
            existing_tool_names = []
            for t in agent.tools:
                if hasattr(t, 'name'):
                    existing_tool_names.append(t.name)
                elif callable(t) and hasattr(t, '__name__'):
                    existing_tool_names.append(t.__name__)

            if self.write_todos_tool.name not in existing_tool_names:
                agent.tools.append(self.write_todos_tool)
    
    def wrap_model_call(
        self,
        request: dict[str, Any],
        handler: Callable[[dict[str, Any]], dict[str, Any]],
    ) -> dict[str, Any]:
        """Update system prompt to include todo list instructions."""
        if self.system_prompt is not None:
            existing_prompt = request.get("system_prompt", "")
            if existing_prompt:
                request["system_prompt"] = existing_prompt + "\n\n" + self.system_prompt
            else:
                request["system_prompt"] = self.system_prompt
        return handler(request)
    
    def get_current_todos(self, runtime: Any) -> list[dict[str, Any]]:
        """Get current todos from runtime state.
        
        Args:
            runtime: Runtime context.
            
        Returns:
            List of current todos.
        """
        if runtime and hasattr(runtime, "state"):
            return runtime.state.get("todos", [])
        return []
    
    def format_todos_display(self, runtime: Any) -> str:
        """Format current todos for display.
        
        Args:
            runtime: Runtime context.
            
        Returns:
            Formatted todo list string.
        """
        todos = self.get_current_todos(runtime)
        return self.write_todos_tool.format_todos(todos)
