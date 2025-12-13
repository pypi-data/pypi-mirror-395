"""
Custom exceptions for the Azcore..

This module provides a comprehensive exception hierarchy for better
error handling and debugging throughout the framework.
"""

from typing import Optional, List, Dict, Any
from difflib import get_close_matches


# Documentation base URL
DOCS_URL = "https://docs.azrienlabs.com"


class AzCoreException(Exception):
    """
    Base exception for all Azcore. errors.
    
    All custom exceptions in the framework inherit from this class,
    allowing for easy catching of all framework-specific errors.
    """
    
    def __init__(
        self,
        message: str,
        details: Optional[Dict[str, Any]] = None,
        solution: Optional[str] = None,
        doc_url: Optional[str] = None,
        examples: Optional[List[str]] = None
    ):
        """
        Initialize the exception with enhanced error information.
        
        Args:
            message: Human-readable error message
            details: Optional dictionary with additional error context
            solution: Suggested solution or fix for the error
            doc_url: Link to relevant documentation
            examples: List of code examples showing correct usage
        """
        super().__init__(message)
        self.message = message
        self.details = details or {}
        self.solution = solution
        self.doc_url = doc_url
        self.examples = examples or []
    
    def __str__(self) -> str:
        """Format error message with all available information."""
        parts = [f"\n{'='*70}"]
        parts.append(f"❌ {self.__class__.__name__}")
        parts.append('='*70)
        parts.append(f"\n{self.message}")
        
        # Add details if present
        if self.details:
            parts.append("\n\n📋 Details:")
            for key, value in self.details.items():
                parts.append(f"  • {key}: {value}")
        
        # Add solution if present
        if self.solution:
            parts.append(f"\n\n💡 Solution:")
            for line in self.solution.split('\n'):
                parts.append(f"  {line}" if line.strip() else "")
        
        # Add examples if present
        if self.examples:
            parts.append(f"\n\n📖 Examples:")
            for i, example in enumerate(self.examples, 1):
                parts.append(f"\n  Example {i}:")
                for line in example.split('\n'):
                    parts.append(f"    {line}")
        
        # Add documentation link if present
        if self.doc_url:
            parts.append(f"\n\n📚 Documentation: {self.doc_url}")
        
        parts.append(f"\n{'='*70}\n")
        
        return '\n'.join(parts)
    
    def get_short_message(self) -> str:
        """Get a short version of the error message without formatting."""
        if self.details:
            details_str = ", ".join(f"{k}={v}" for k, v in self.details.items())
            return f"{self.message} ({details_str})"
        return self.message


class ConfigurationError(AzCoreException):
    """
    Configuration-related errors.
    
    Raised when:
    - Configuration file is missing or invalid
    - Required configuration keys are missing
    - Configuration values are out of valid range
    - Environment variables are not set
    """
    pass


class ValidationError(AzCoreException):
    """
    Input/output validation errors.
    
    Raised when:
    - Input parameters fail validation
    - Output format is invalid
    - Schema validation fails
    - Type checking fails
    """
    pass


class LLMError(AzCoreException):
    """
    LLM invocation and response errors.
    
    Raised when:
    - LLM API call fails
    - Response parsing fails
    - Rate limits are exceeded
    - Model is unavailable
    """
    pass


class LLMTimeoutError(LLMError):
    """
    LLM request timeout error.
    
    Raised when an LLM request exceeds the configured timeout.
    """
    pass


class LLMRateLimitError(LLMError):
    """
    LLM rate limit exceeded error.
    
    Raised when LLM API rate limits are exceeded.
    """
    pass


class NodeExecutionError(AzCoreException):
    """
    Node execution errors.
    
    Raised when:
    - Node execution fails
    - Node returns invalid output
    - Node exceeds execution timeout
    - Node state is invalid
    """
    pass


class ToolExecutionError(AzCoreException):
    """
    Tool execution errors.
    
    Raised when:
    - Tool execution fails
    - Tool returns invalid output
    - Tool not found
    - Tool permission denied
    """
    pass


class ToolNotFoundError(ToolExecutionError):
    """
    Tool not found error.
    
    Raised when attempting to use a tool that doesn't exist.
    """
    pass


class StateError(AzCoreException):
    """
    State management errors.
    
    Raised when:
    - State is invalid or corrupted
    - State update fails
    - State validation fails
    - State size exceeds limits
    """
    pass


class SupervisorError(AzCoreException):
    """
    Supervisor routing and decision errors.
    
    Raised when:
    - Supervisor routing fails
    - Invalid routing decision
    - No valid route available
    - Supervisor response is malformed
    """
    pass


class TeamError(AzCoreException):
    """
    Team building and execution errors.
    
    Raised when:
    - Team building fails
    - Team execution fails
    - Team configuration is invalid
    - Required team component is missing
    """
    pass


class GraphError(AzCoreException):
    """
    Graph orchestration errors.
    
    Raised when:
    - Graph compilation fails
    - Graph execution fails
    - Invalid graph structure
    - Cycle detected in graph
    """
    pass


class GraphCycleError(GraphError):
    """
    Graph cycle detection error.
    
    Raised when a cycle is detected in the execution graph.
    """
    pass


class MaxIterationsExceededError(GraphError):
    """
    Maximum iterations exceeded error.
    
    Raised when graph execution exceeds the maximum iteration limit.
    """
    pass


class RLError(AzCoreException):
    """
    Reinforcement learning errors.
    
    Raised when:
    - RL manager initialization fails
    - Q-table loading/saving fails
    - Reward calculation fails
    - Invalid RL configuration
    """
    pass


class EmbeddingError(RLError):
    """
    Embedding generation and similarity errors.
    
    Raised when:
    - Embedding model loading fails
    - Embedding generation fails
    - Similarity computation fails
    """
    pass


class RewardCalculationError(RLError):
    """
    Reward calculation error.
    
    Raised when reward calculation fails for any reward calculator.
    """
    pass


class AgentError(AzCoreException):
    """
    Agent creation and execution errors.
    
    Raised when:
    - Agent initialization fails
    - Agent execution fails
    - Agent configuration is invalid
    """
    pass


class TimeoutError(AzCoreException):
    """
    Generic timeout error.
    
    Raised when an operation exceeds its configured timeout.
    """
    pass


# Convenience functions for creating detailed exceptions
def create_detailed_error(
    exception_class: type,
    message: str,
    solution: Optional[str] = None,
    doc_url: Optional[str] = None,
    examples: Optional[List[str]] = None,
    **details
) -> AzCoreException:
    """
    Create an exception with detailed context and helpful information.
    
    Args:
        exception_class: Exception class to instantiate
        message: Error message
        solution: Suggested fix or workaround
        doc_url: Link to relevant documentation
        examples: Code examples showing correct usage
        **details: Additional context as keyword arguments
        
    Returns:
        Exception instance with comprehensive error information
        
    Example:
        >>> raise create_detailed_error(
        ...     ConfigurationError,
        ...     "Invalid temperature value",
        ...     solution="Set temperature between 0.0 and 2.0",
        ...     key="llm.temperature",
        ...     value=2.5,
        ...     valid_range="0.0-2.0"
        ... )
    """
    return exception_class(
        message,
        details=details,
        solution=solution,
        doc_url=doc_url,
        examples=examples
    )


def suggest_similar(
    invalid_value: str,
    valid_options: List[str],
    threshold: float = 0.6
) -> Optional[str]:
    """
    Suggest similar valid options for typos using fuzzy matching.
    
    Args:
        invalid_value: The invalid input value
        valid_options: List of valid option values
        threshold: Similarity threshold (0-1)
        
    Returns:
        Formatted suggestion string or None
        
    Example:
        >>> suggest_similar("gp-4", ["gpt-3.5-turbo", "gpt-4", "gpt-4-turbo"])
        "Did you mean 'gpt-4'?"
    """
    matches = get_close_matches(
        invalid_value,
        valid_options,
        n=3,
        cutoff=threshold
    )
    
    if matches:
        if len(matches) == 1:
            return f"Did you mean '{matches[0]}'?"
        else:
            suggestions = "', '".join(matches)
            return f"Did you mean one of: '{suggestions}'?"
    
    return None


def create_config_error(
    key: str,
    value: Any,
    reason: str,
    valid_values: Optional[List[str]] = None,
    example_config: Optional[str] = None
) -> ConfigurationError:
    """
    Create a configuration error with helpful context.
    
    Args:
        key: Configuration key that caused the error
        value: Invalid value that was provided
        reason: Explanation of why the value is invalid
        valid_values: List of valid values (for suggestions)
        example_config: Example of correct configuration
        
    Returns:
        ConfigurationError with solutions and examples
    """
    message = f"Invalid configuration for '{key}': {reason}"
    details = {"key": key, "value": value}
    
    # Build solution
    solution_parts = []
    
    if valid_values:
        solution_parts.append(f"Valid options: {', '.join(map(str, valid_values))}")
        
        # Add "did you mean" suggestion
        if isinstance(value, str):
            suggestion = suggest_similar(value, valid_values)
            if suggestion:
                solution_parts.append(suggestion)
    
    solution_parts.append(f"\nUpdate your config.yml or use 'azcore validate config' to check for issues.")
    
    solution = "\n".join(solution_parts)
    
    # Add example if provided
    examples = []
    if example_config:
        examples.append(example_config)
    
    return ConfigurationError(
        message=message,
        details=details,
        solution=solution,
        doc_url=f"{DOCS_URL}/configuration",
        examples=examples
    )


def create_llm_error(
    error_message: str,
    model: Optional[str] = None,
    provider: Optional[str] = None,
    original_error: Optional[Exception] = None
) -> LLMError:
    """
    Create an LLM error with troubleshooting steps.
    
    Args:
        error_message: Description of the error
        model: Model name that failed
        provider: Provider name (e.g., 'openai', 'anthropic')
        original_error: Original exception that was caught
        
    Returns:
        LLMError with troubleshooting steps
    """
    details = {}
    if model:
        details["model"] = model
    if provider:
        details["provider"] = provider
    if original_error:
        details["original_error"] = str(original_error)
    
    # Check for common error patterns and provide specific solutions
    error_lower = error_message.lower()
    
    if "api key" in error_lower or "authentication" in error_lower:
        solution = """Check your API key configuration:
1. Verify OPENAI_API_KEY is set in your .env file
2. Run 'azcore doctor' to validate your environment
3. Ensure the API key is valid and has not expired
4. Check if you have sufficient credits/quota"""
        doc_url = f"{DOCS_URL}/setup/api-keys"
        
    elif "rate limit" in error_lower or "429" in error_lower:
        solution = """You've hit API rate limits. Try:
1. Add retry logic with exponential backoff
2. Reduce request frequency
3. Upgrade your API plan for higher limits
4. Use caching to reduce redundant calls"""
        doc_url = f"{DOCS_URL}/optimization/rate-limiting"
        
    elif "timeout" in error_lower:
        solution = """Request timed out. Try:
1. Increase timeout value in LLM configuration
2. Use a faster model (e.g., gpt-4o-mini)
3. Simplify your prompt
4. Check your network connection"""
        doc_url = f"{DOCS_URL}/troubleshooting/timeouts"
        
    elif "not found" in error_lower or "404" in error_lower:
        solution = """Model not found. Try:
1. Check the model name spelling
2. Verify the model is available in your region
3. Use 'azcore examples list' to see working examples
4. Check OpenAI's model availability"""
        doc_url = f"{DOCS_URL}/models"
        
    else:
        solution = """General troubleshooting steps:
1. Run 'azcore doctor' to check your setup
2. Verify your API keys and configuration
3. Check the model name and availability
4. Review logs for more details"""
        doc_url = f"{DOCS_URL}/troubleshooting"
    
    return LLMError(
        message=error_message,
        details=details,
        solution=solution,
        doc_url=doc_url
    )


def create_validation_error(
    field: str,
    value: Any,
    expected_type: str,
    constraints: Optional[str] = None
) -> ValidationError:
    """
    Create a validation error with clear expectations.
    
    Args:
        field: Field name that failed validation
        value: Invalid value provided
        expected_type: Expected type or format
        constraints: Additional constraints or requirements
        
    Returns:
        ValidationError with clear requirements
    """
    message = f"Validation failed for '{field}'"
    
    details = {
        "field": field,
        "value": value,
        "expected_type": expected_type
    }
    
    if constraints:
        details["constraints"] = constraints
    
    solution = f"""Provide a valid value for '{field}':
• Expected type: {expected_type}
• Received: {type(value).__name__} = {value}"""
    
    if constraints:
        solution += f"\n• Constraints: {constraints}"
    
    solution += "\n\nRun 'azcore validate config' to check all configuration values."
    
    return ValidationError(
        message=message,
        details=details,
        solution=solution,
        doc_url=f"{DOCS_URL}/configuration/validation"
    )
