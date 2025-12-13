"""
Helper functions for the Azcore..

This module provides utility functions for validation, data processing,
and other common operations.
"""

import json
import re
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


def validate_state(state: Dict[str, Any]) -> bool:
    """
    Validate that a state dictionary has required fields.
    
    Args:
        state: State dictionary to validate
        
    Returns:
        True if valid, False otherwise
    """
    required_fields = ["messages"]
    
    for field in required_fields:
        if field not in state:
            logger.error(f"Missing required field in state: {field}")
            return False
    
    if not isinstance(state["messages"], list):
        logger.error("State 'messages' field must be a list")
        return False
    
    return True


def clean_json(text: str) -> str:
    """
    Clean JSON text by removing markdown formatting and extra whitespace.
    
    Args:
        text: Raw text that may contain JSON
        
    Returns:
        Cleaned JSON string
    """
    cleaned = text.strip()
    
    # Remove JSON code fences
    if cleaned.startswith("```json"):
        cleaned = cleaned.removeprefix("```json")
    elif cleaned.startswith("```"):
        cleaned = cleaned.removeprefix("```")
    elif cleaned.startswith("json"):
        cleaned = cleaned.removeprefix("json")
    
    if cleaned.endswith("```"):
        cleaned = cleaned.removesuffix("```")
    
    return cleaned.strip()


def parse_json_safe(text: str) -> Optional[Dict[str, Any]]:
    """
    Safely parse JSON text with error handling.
    
    Args:
        text: JSON text to parse
        
    Returns:
        Parsed dictionary or None if parsing fails
    """
    try:
        cleaned = clean_json(text)
        return json.loads(cleaned)
    except json.JSONDecodeError as e:
        logger.error(f"JSON parsing error: {e}")
        return None


def extract_code_blocks(text: str, language: Optional[str] = None) -> list[str]:
    """
    Extract code blocks from markdown text.
    
    Args:
        text: Markdown text containing code blocks
        language: Optional language to filter by
        
    Returns:
        List of code block contents
    """
    if language:
        pattern = f"```{language}\\n(.*?)```"
    else:
        pattern = r"```(?:\w+)?\n(.*?)```"
    
    matches = re.findall(pattern, text, re.DOTALL)
    return [match.strip() for match in matches]


def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """
    Truncate text to maximum length.
    
    Args:
        text: Text to truncate
        max_length: Maximum length
        suffix: Suffix to add if truncated
        
    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text
    
    return text[:max_length - len(suffix)] + suffix


def format_message_history(messages: list) -> str:
    """
    Format message history for display.
    
    Args:
        messages: List of messages
        
    Returns:
        Formatted string
    """
    formatted = []
    
    for msg in messages:
        role = getattr(msg, "name", None) or getattr(msg, "role", "unknown")
        content = getattr(msg, "content", str(msg))
        
        formatted.append(f"[{role}]: {truncate_text(content, 200)}")
    
    return "\n".join(formatted)


def merge_dicts(dict1: Dict, dict2: Dict) -> Dict:
    """
    Recursively merge two dictionaries.
    
    Args:
        dict1: First dictionary
        dict2: Second dictionary (takes precedence)
        
    Returns:
        Merged dictionary
    """
    result = dict1.copy()
    
    for key, value in dict2.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = merge_dicts(result[key], value)
        else:
            result[key] = value
    
    return result


def get_nested_value(data: Dict, path: str, default: Any = None) -> Any:
    """
    Get nested dictionary value using dot notation.
    
    Args:
        data: Dictionary to search
        path: Dot-separated path (e.g., "user.profile.name")
        default: Default value if path not found
        
    Returns:
        Value at path or default
    """
    keys = path.split('.')
    value = data
    
    for key in keys:
        if isinstance(value, dict) and key in value:
            value = value[key]
        else:
            return default
    
    return value


def set_nested_value(data: Dict, path: str, value: Any) -> None:
    """
    Set nested dictionary value using dot notation.
    
    Args:
        data: Dictionary to modify
        path: Dot-separated path (e.g., "user.profile.name")
        value: Value to set
    """
    keys = path.split('.')
    current = data
    
    for key in keys[:-1]:
        if key not in current:
            current[key] = {}
        current = current[key]
    
    current[keys[-1]] = value
