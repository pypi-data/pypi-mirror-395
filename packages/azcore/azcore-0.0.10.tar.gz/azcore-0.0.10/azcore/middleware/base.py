"""Base middleware class for azcore."""

from abc import ABC, abstractmethod
from typing import Any, Callable


class MiddlewareBase(ABC):
    """Base class for middleware components.
    
    Middleware can wrap model calls, tool calls, and modify agent behavior.
    """

    @abstractmethod
    def setup(self, agent: Any) -> None:
        """Setup middleware with the agent.
        
        Args:
            agent: The agent instance to setup middleware for.
        """
        pass

    def wrap_model_call(
        self,
        request: dict[str, Any],
        handler: Callable[[dict[str, Any]], dict[str, Any]],
    ) -> dict[str, Any]:
        """Wrap a model call.
        
        Args:
            request: The model request.
            handler: The handler function to call.
            
        Returns:
            The model response.
        """
        return handler(request)

    def wrap_tool_call(
        self,
        request: dict[str, Any],
        handler: Callable[[dict[str, Any]], Any],
    ) -> Any:
        """Wrap a tool call.
        
        Args:
            request: The tool call request.
            handler: The handler function to call.
            
        Returns:
            The tool result.
        """
        return handler(request)
