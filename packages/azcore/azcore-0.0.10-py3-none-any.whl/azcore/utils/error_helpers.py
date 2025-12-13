"""
Error formatting and helper utilities for Az-Core.

This module provides utilities for creating user-friendly error messages,
suggestions, and helpful error handling throughout the framework.
"""

from typing import List, Optional, Dict, Any, Tuple
from difflib import get_close_matches
import sys
import traceback


def format_error_context(
    error: Exception,
    show_traceback: bool = False,
    color: bool = True
) -> str:
    """
    Format error with context and color coding.
    
    Args:
        error: Exception to format
        show_traceback: Include full traceback
        color: Use ANSI color codes
        
    Returns:
        Formatted error string
    """
    from azcore.exceptions import AzCoreException
    
    # Use exception's __str__ if it's an AzCoreException
    if isinstance(error, AzCoreException):
        formatted = str(error)
        
        # Add traceback if requested
        if show_traceback:
            formatted += "\n\nTraceback:\n"
            formatted += ''.join(traceback.format_tb(error.__traceback__))
        
        return formatted
    
    # For other exceptions, create a simple format
    parts = [
        "\n" + "="*70,
        f"❌ {type(error).__name__}",
        "="*70,
        f"\n{str(error)}"
    ]
    
    if show_traceback:
        parts.append("\n\nTraceback:")
        parts.append(''.join(traceback.format_tb(error.__traceback__)))
    
    parts.append("\n" + "="*70 + "\n")
    
    return '\n'.join(parts)


def suggest_command_fix(
    invalid_command: str,
    valid_commands: List[str],
    threshold: float = 0.6
) -> Optional[str]:
    """
    Suggest similar valid commands for typos.
    
    Args:
        invalid_command: The invalid command entered
        valid_commands: List of valid commands
        threshold: Similarity threshold
        
    Returns:
        Suggestion message or None
    """
    matches = get_close_matches(
        invalid_command,
        valid_commands,
        n=3,
        cutoff=threshold
    )
    
    if matches:
        if len(matches) == 1:
            return f"\n💡 Did you mean: azcore {matches[0]}"
        else:
            suggestions = '\n   • azcore '.join(matches)
            return f"\n💡 Did you mean one of:\n   • azcore {suggestions}"
    
    return None


def suggest_config_key_fix(
    invalid_key: str,
    valid_keys: List[str],
    threshold: float = 0.6
) -> Optional[str]:
    """
    Suggest similar valid configuration keys.
    
    Args:
        invalid_key: The invalid key used
        valid_keys: List of valid configuration keys
        threshold: Similarity threshold
        
    Returns:
        Suggestion message or None
    """
    matches = get_close_matches(
        invalid_key,
        valid_keys,
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


def create_config_example(
    key: str,
    value: Any,
    description: Optional[str] = None
) -> str:
    """
    Create a configuration example snippet.
    
    Args:
        key: Configuration key
        value: Example value
        description: Optional description
        
    Returns:
        Formatted YAML example
    """
    lines = []
    
    if description:
        lines.append(f"# {description}")
    
    if isinstance(value, dict):
        lines.append(f"{key}:")
        for k, v in value.items():
            if isinstance(v, str):
                lines.append(f"  {k}: {v}")
            else:
                lines.append(f"  {k}: {v}")
    else:
        if isinstance(value, str):
            lines.append(f"{key}: {value}")
        else:
            lines.append(f"{key}: {value}")
    
    return '\n'.join(lines)


def get_common_solutions(error_type: str) -> List[str]:
    """
    Get common solutions for error types.
    
    Args:
        error_type: Type of error (e.g., 'api_key', 'rate_limit', 'timeout')
        
    Returns:
        List of solution steps
    """
    solutions = {
        'api_key': [
            "Check that OPENAI_API_KEY is set in your .env file",
            "Run 'azcore doctor' to validate your environment",
            "Verify the API key is valid and active",
            "Ensure you have API credits/quota available"
        ],
        'rate_limit': [
            "Wait a moment before retrying",
            "Reduce request frequency",
            "Implement exponential backoff",
            "Upgrade your API plan for higher limits",
            "Use caching to reduce API calls"
        ],
        'timeout': [
            "Increase timeout value in configuration",
            "Use a faster model (e.g., gpt-4o-mini)",
            "Simplify your prompt or request",
            "Check network connectivity"
        ],
        'config': [
            "Run 'azcore validate config' to check configuration",
            "Review example configs with 'azcore examples list'",
            "Use 'azcore init' to create a template",
            "Check YAML syntax (indentation, colons, quotes)"
        ],
        'dependency': [
            "Install required dependencies: pip install azcore",
            "Check Python version (3.12+ required)",
            "Run 'azcore doctor' for full diagnostics",
            "Try reinstalling: pip install --upgrade azcore"
        ],
        'model': [
            "Check model name spelling",
            "Verify model availability in your region",
            "See available models: https://platform.openai.com/docs/models",
            "Use a known working model (e.g., gpt-4o-mini)"
        ]
    }
    
    return solutions.get(error_type, [
        "Run 'azcore doctor' for diagnostics",
        "Check documentation: https://docs.azrienlabs.com",
        "Review examples: azcore examples list",
        "Validate configuration: azcore validate config"
    ])


def format_validation_error(
    field: str,
    value: Any,
    expected: str,
    constraints: Optional[List[str]] = None
) -> str:
    """
    Format a validation error message.
    
    Args:
        field: Field that failed validation
        value: Invalid value
        expected: Expected type or format
        constraints: Additional constraints
        
    Returns:
        Formatted error message
    """
    lines = [
        f"Validation failed for field '{field}'",
        "",
        f"Value provided: {value} (type: {type(value).__name__})",
        f"Expected: {expected}",
    ]
    
    if constraints:
        lines.append("")
        lines.append("Constraints:")
        for constraint in constraints:
            lines.append(f"  • {constraint}")
    
    return '\n'.join(lines)


def create_helpful_error(
    error_type: str,
    message: str,
    context: Optional[Dict[str, Any]] = None,
    solutions: Optional[List[str]] = None
) -> str:
    """
    Create a comprehensive helpful error message.
    
    Args:
        error_type: Type of error for icon selection
        message: Main error message
        context: Additional context information
        solutions: List of solution steps
        
    Returns:
        Formatted error message with all helpful information
    """
    icons = {
        'error': '❌',
        'warning': '⚠️',
        'info': 'ℹ️',
        'config': '⚙️',
        'api': '🔑',
        'network': '🌐',
        'file': '📄',
        'validation': '✓'
    }
    
    icon = icons.get(error_type, '❌')
    
    lines = [
        "",
        "="*70,
        f"{icon} {error_type.upper()} ERROR",
        "="*70,
        "",
        message,
    ]
    
    if context:
        lines.append("")
        lines.append("📋 Context:")
        for key, value in context.items():
            lines.append(f"  • {key}: {value}")
    
    if solutions:
        lines.append("")
        lines.append("💡 Solutions:")
        for i, solution in enumerate(solutions, 1):
            lines.append(f"  {i}. {solution}")
    
    lines.append("")
    lines.append("="*70)
    lines.append("")
    
    return '\n'.join(lines)


def wrap_error_with_context(func):
    """
    Decorator to wrap function errors with helpful context.
    
    Usage:
        @wrap_error_with_context
        def my_function():
            ...
    """
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            from azcore.exceptions import AzCoreException
            
            # If already an AzCoreException, just re-raise
            if isinstance(e, AzCoreException):
                raise
            
            # Otherwise, wrap with context
            print(format_error_context(e, show_traceback=False))
            raise
    
    return wrapper


def check_common_mistakes(config: Dict[str, Any]) -> List[Tuple[str, str, str]]:
    """
    Check for common configuration mistakes.
    
    Args:
        config: Configuration dictionary
        
    Returns:
        List of (severity, field, message) tuples
    """
    issues = []
    
    # Check temperature values
    for key in ['llm', 'fast_llm', 'coordinator_llm']:
        if key in config and isinstance(config[key], dict):
            temp = config[key].get('temperature')
            if temp is not None:
                if not isinstance(temp, (int, float)):
                    issues.append((
                        'error',
                        f'{key}.temperature',
                        f'Temperature must be a number, got {type(temp).__name__}'
                    ))
                elif temp < 0 or temp > 2:
                    issues.append((
                        'error',
                        f'{key}.temperature',
                        f'Temperature must be between 0 and 2, got {temp}'
                    ))
                elif temp > 1.5:
                    issues.append((
                        'warning',
                        f'{key}.temperature',
                        f'High temperature ({temp}) may produce inconsistent results'
                    ))
    
    # Check for missing model specifications
    for key in ['llm', 'fast_llm']:
        if key in config and isinstance(config[key], dict):
            if 'model' not in config[key]:
                issues.append((
                    'warning',
                    f'{key}.model',
                    'Model not specified, will use default'
                ))
    
    # Check for common typos
    common_keys = ['llm', 'fast_llm', 'coordinator_llm', 'embedding_model']
    for key in config.keys():
        if key not in common_keys:
            suggestion = suggest_config_key_fix(key, common_keys)
            if suggestion:
                issues.append((
                    'warning',
                    key,
                    f'Unknown configuration key. {suggestion}'
                ))
    
    return issues


def print_error_summary(errors: List[str], warnings: List[str]):
    """
    Print a summary of errors and warnings.
    
    Args:
        errors: List of error messages
        warnings: List of warning messages
    """
    if errors:
        print("\n" + "="*70)
        print(f"❌ {len(errors)} Error(s) Found")
        print("="*70)
        for i, error in enumerate(errors, 1):
            print(f"\n{i}. {error}")
    
    if warnings:
        print("\n" + "="*70)
        print(f"⚠️  {len(warnings)} Warning(s)")
        print("="*70)
        for i, warning in enumerate(warnings, 1):
            print(f"\n{i}. {warning}")
    
    if not errors and not warnings:
        print("\n✅ No issues found!")
    
    print("\n" + "="*70 + "\n")
