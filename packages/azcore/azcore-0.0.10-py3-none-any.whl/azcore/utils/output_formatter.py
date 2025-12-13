"""
Output formatting utilities for the Azcore..

This module provides utilities for formatting agent outputs in various formats,
inspired by Swarms' output handling capabilities.
"""

import json
import logging
from typing import Any, Dict, List, Union, Literal
from datetime import datetime

logger = logging.getLogger(__name__)

OutputType = Literal["string", "dict", "list", "json", "all", "final"]


def history_output_formatter(
    history: List[Dict[str, Any]],
    output_type: OutputType = "all"
) -> Union[str, Dict, List]:
    """
    Format agent execution history based on output type.

    Args:
        history: List of agent execution history dictionaries
        output_type: Desired output format

    Returns:
        Formatted output based on output_type

    Example:
        >>> history = [
        ...     {"agent": "researcher", "output": "Research complete"},
        ...     {"agent": "writer", "output": "Article written"}
        ... ]
        >>> history_output_formatter(history, "string")
        'researcher: Research complete\\nwriter: Article written'
    """
    if not history:
        return "" if output_type == "string" else {}

    if output_type == "all":
        # Return complete history
        return history

    elif output_type == "final":
        # Return only the last output
        if isinstance(history[-1], dict):
            return history[-1].get("output", history[-1])
        return history[-1]

    elif output_type == "string":
        # Format as human-readable string
        lines = []
        for entry in history:
            if isinstance(entry, dict):
                agent = entry.get("agent", entry.get("agent_name", "Unknown"))
                output = entry.get("output", entry.get("content", str(entry)))
                lines.append(f"{agent}: {output}")
            else:
                lines.append(str(entry))
        return "\n".join(lines)

    elif output_type == "dict":
        # Return as dictionary mapping agent names to outputs
        result = {}
        for entry in history:
            if isinstance(entry, dict):
                agent = entry.get("agent", entry.get("agent_name", "Unknown"))
                output = entry.get("output", entry.get("content", str(entry)))
                result[agent] = output
        return result

    elif output_type == "list":
        # Return as list of outputs
        return [
            entry.get("output", entry.get("content", str(entry)))
            if isinstance(entry, dict) else str(entry)
            for entry in history
        ]

    elif output_type == "json":
        # Return as JSON string
        return json.dumps(history, indent=2, default=str)

    else:
        logger.warning(f"Unknown output_type: {output_type}, defaulting to 'all'")
        return history


def format_conversation_history(
    messages: List[Dict[str, str]],
    format_style: str = "chat",
    include_timestamps: bool = False
) -> str:
    """
    Format conversation messages into a readable string.

    Args:
        messages: List of message dictionaries with 'role' and 'content'
        format_style: Style of formatting ('chat', 'compact', 'detailed')
        include_timestamps: Include timestamps if available

    Returns:
        Formatted conversation string

    Example:
        >>> messages = [
        ...     {"role": "user", "content": "Hello"},
        ...     {"role": "assistant", "content": "Hi there!"}
        ... ]
        >>> print(format_conversation_history(messages))
    """
    if not messages:
        return ""

    lines = []

    if format_style == "chat":
        for msg in messages:
            role = msg.get("role", "").upper()
            content = msg.get("content", "")

            if include_timestamps and "timestamp" in msg:
                timestamp = msg["timestamp"]
                lines.append(f"[{timestamp}] {role}:")
            else:
                lines.append(f"{role}:")

            lines.append(content)
            lines.append("")  # Empty line between messages

    elif format_style == "compact":
        for msg in messages:
            role = msg.get("role", "")
            content = msg.get("content", "")
            lines.append(f"{role}: {content}")

    elif format_style == "detailed":
        for i, msg in enumerate(messages, 1):
            role = msg.get("role", "")
            content = msg.get("content", "")

            lines.append(f"--- Message {i} ---")
            lines.append(f"Role: {role}")

            if include_timestamps and "timestamp" in msg:
                lines.append(f"Time: {msg['timestamp']}")

            if "metadata" in msg:
                lines.append(f"Metadata: {json.dumps(msg['metadata'])}")

            lines.append(f"Content: {content}")
            lines.append("")

    else:
        logger.warning(f"Unknown format_style: {format_style}, using 'chat'")
        return format_conversation_history(messages, "chat", include_timestamps)

    return "\n".join(lines)


def format_agent_output(
    agent_name: str,
    output: Any,
    execution_time: float = None,
    metadata: Dict[str, Any] = None
) -> Dict[str, Any]:
    """
    Format a single agent's output into a standardized dictionary.

    Args:
        agent_name: Name of the agent
        output: Agent's output
        execution_time: Optional execution time in seconds
        metadata: Optional metadata dictionary

    Returns:
        Standardized output dictionary

    Example:
        >>> format_agent_output(
        ...     "researcher",
        ...     "Research findings...",
        ...     execution_time=2.5,
        ...     metadata={"sources": 3}
        ... )
    """
    result = {
        "agent_name": agent_name,
        "output": output,
        "timestamp": datetime.now().isoformat()
    }

    if execution_time is not None:
        result["execution_time"] = execution_time

    if metadata:
        result["metadata"] = metadata

    return result


def format_swarm_output(
    swarm_name: str,
    agents_output: List[Dict[str, Any]],
    total_time: float = None,
    metadata: Dict[str, Any] = None
) -> Dict[str, Any]:
    """
    Format the complete output of a swarm execution.

    Args:
        swarm_name: Name of the swarm
        agents_output: List of agent output dictionaries
        total_time: Total execution time
        metadata: Optional swarm metadata

    Returns:
        Formatted swarm output dictionary
    """
    result = {
        "swarm_name": swarm_name,
        "timestamp": datetime.now().isoformat(),
        "agents_count": len(agents_output),
        "agents_output": agents_output
    }

    if total_time is not None:
        result["total_execution_time"] = total_time

    if metadata:
        result["metadata"] = metadata

    # Add final output (last agent's output)
    if agents_output:
        result["final_output"] = agents_output[-1].get("output", "")

    return result


def format_error_output(
    agent_name: str,
    error: Exception,
    context: Dict[str, Any] = None
) -> Dict[str, Any]:
    """
    Format error information from agent execution.

    Args:
        agent_name: Name of the agent that errored
        error: The exception that occurred
        context: Optional context information

    Returns:
        Formatted error dictionary
    """
    result = {
        "agent_name": agent_name,
        "error_type": type(error).__name__,
        "error_message": str(error),
        "timestamp": datetime.now().isoformat(),
        "success": False
    }

    if context:
        result["context"] = context

    return result


def aggregate_outputs(
    outputs: List[Dict[str, Any]],
    aggregation_method: str = "concat"
) -> str:
    """
    Aggregate multiple agent outputs into a single output.

    Args:
        outputs: List of agent output dictionaries
        aggregation_method: Method for aggregation ('concat', 'summarize', 'last')

    Returns:
        Aggregated output string

    Example:
        >>> outputs = [
        ...     {"output": "Part 1"},
        ...     {"output": "Part 2"}
        ... ]
        >>> aggregate_outputs(outputs, "concat")
        'Part 1\\n\\nPart 2'
    """
    if not outputs:
        return ""

    if aggregation_method == "last":
        # Return only the last output
        return str(outputs[-1].get("output", ""))

    elif aggregation_method == "concat":
        # Concatenate all outputs
        result_parts = []
        for output_dict in outputs:
            if isinstance(output_dict, dict):
                output = output_dict.get("output", "")
            else:
                output = str(output_dict)

            if output:
                result_parts.append(output)

        return "\n\n".join(result_parts)

    elif aggregation_method == "summarize":
        # Create a structured summary
        lines = ["=== Agent Outputs Summary ===\n"]
        for i, output_dict in enumerate(outputs, 1):
            agent_name = output_dict.get("agent_name", f"Agent {i}")
            output = output_dict.get("output", "")
            lines.append(f"{agent_name}:")
            lines.append(f"{output}\n")

        return "\n".join(lines)

    else:
        logger.warning(f"Unknown aggregation_method: {aggregation_method}, using 'concat'")
        return aggregate_outputs(outputs, "concat")


def format_to_json(data: Any, pretty: bool = True) -> str:
    """
    Format any data structure to JSON string.

    Args:
        data: Data to format
        pretty: Use pretty printing

    Returns:
        JSON string
    """
    indent = 2 if pretty else None
    return json.dumps(data, indent=indent, default=str)


def format_execution_summary(
    workflow_name: str,
    agents_executed: List[str],
    total_time: float,
    success: bool,
    final_output: str,
    errors: List[Dict[str, Any]] = None
) -> str:
    """
    Format a comprehensive execution summary.

    Args:
        workflow_name: Name of the workflow
        agents_executed: List of agent names that executed
        total_time: Total execution time
        success: Whether execution was successful
        final_output: Final output from workflow
        errors: Optional list of errors

    Returns:
        Formatted summary string
    """
    lines = [
        "=" * 60,
        f"Workflow Execution Summary: {workflow_name}",
        "=" * 60,
        f"Status: {'SUCCESS' if success else 'FAILED'}",
        f"Agents Executed: {', '.join(agents_executed)}",
        f"Total Execution Time: {total_time:.2f} seconds",
        ""
    ]

    if errors:
        lines.append("Errors:")
        for error in errors:
            agent = error.get("agent_name", "Unknown")
            error_msg = error.get("error_message", "")
            lines.append(f"  - {agent}: {error_msg}")
        lines.append("")

    lines.extend([
        "Final Output:",
        "-" * 60,
        final_output,
        "-" * 60
    ])

    return "\n".join(lines)
