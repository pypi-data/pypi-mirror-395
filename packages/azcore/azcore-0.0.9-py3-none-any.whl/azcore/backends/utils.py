"""Utility functions for backend operations."""

import re
from datetime import datetime, timezone
from fnmatch import fnmatch
from typing import Any

from azcore.backends.protocol import FileInfo, GrepMatch


# Constants
EMPTY_CONTENT_WARNING = "System reminder: File exists but has empty contents"
MAX_LINE_LENGTH = 2000
LINE_NUMBER_WIDTH = 6


class FileData(dict):
    """File data structure with content, timestamps."""
    content: list[str]
    created_at: str
    modified_at: str


def create_file_data(content: str) -> dict[str, Any]:
    """Create file data dict from content string."""
    now = datetime.now(timezone.utc).isoformat()
    return {
        "content": content.splitlines(),
        "created_at": now,
        "modified_at": now,
    }


def update_file_data(file_data: dict[str, Any], new_content: str) -> dict[str, Any]:
    """Update file data with new content, preserving created_at."""
    return {
        "content": new_content.splitlines(),
        "created_at": file_data.get("created_at", datetime.now(timezone.utc).isoformat()),
        "modified_at": datetime.now(timezone.utc).isoformat(),
    }


def file_data_to_string(file_data: dict[str, Any]) -> str:
    """Convert file data to string."""
    return "\n".join(file_data.get("content", []))


def check_empty_content(content: str) -> str | None:
    """Check if content is empty and return warning if so."""
    if not content or content.strip() == "":
        return EMPTY_CONTENT_WARNING
    return None


def format_content_with_line_numbers(
    lines: list[str], start_line: int = 1
) -> str:
    """Format lines with line numbers."""
    formatted = []
    for i, line in enumerate(lines):
        line_num = start_line + i
        # Truncate long lines
        if len(line) > MAX_LINE_LENGTH:
            line = line[:MAX_LINE_LENGTH] + "..."
        formatted.append(f"{line_num:>{LINE_NUMBER_WIDTH}}\t{line}")
    return "\n".join(formatted)


def format_read_response(
    file_data: dict[str, Any], offset: int, limit: int
) -> str:
    """Format file content for read response."""
    content = file_data_to_string(file_data)
    empty_msg = check_empty_content(content)
    if empty_msg:
        return empty_msg

    lines = content.splitlines()
    start_idx = offset
    end_idx = min(start_idx + limit, len(lines))

    if start_idx >= len(lines):
        return f"Error: Line offset {offset} exceeds file length ({len(lines)} lines)"

    selected_lines = lines[start_idx:end_idx]
    return format_content_with_line_numbers(selected_lines, start_line=start_idx + 1)


def perform_string_replacement(
    content: str, old_string: str, new_string: str, replace_all: bool = False
) -> tuple[str, int] | str:
    """Perform string replacement in content.
    
    Returns:
        Either (new_content, occurrences) tuple on success, or error message string on failure.
    """
    if not old_string:
        return "Error: old_string cannot be empty"

    occurrences = content.count(old_string)

    if occurrences == 0:
        return f"Error: String not found in file"

    if not replace_all and occurrences > 1:
        return (
            f"Error: Found {occurrences} occurrences. "
            f"Use replace_all=True to replace all, or provide more context to make old_string unique."
        )

    if replace_all:
        new_content = content.replace(old_string, new_string)
    else:
        new_content = content.replace(old_string, new_string, 1)

    return new_content, occurrences


def _glob_search_files(
    files: dict[str, Any], pattern: str, path: str = "/"
) -> str:
    """Search files using glob pattern."""
    # Normalize pattern
    if pattern.startswith("/"):
        pattern = pattern.lstrip("/")

    matched_paths = []
    for file_path in files.keys():
        # Check if file is in the specified path
        if not file_path.startswith(path):
            continue

        # Get relative path from search path
        if path == "/":
            relative = file_path.lstrip("/")
        else:
            relative = file_path[len(path):].lstrip("/")

        # Match against pattern
        if fnmatch(relative, pattern) or fnmatch(file_path, pattern):
            matched_paths.append(file_path)

    if not matched_paths:
        return "No files found"

    return "\n".join(sorted(matched_paths))


def grep_matches_from_files(
    files: dict[str, Any],
    pattern: str,
    path: str = "/",
    glob: str | None = None,
) -> list[GrepMatch] | str:
    """Search for pattern in files."""
    # Validate regex
    try:
        regex = re.compile(pattern)
    except re.error as e:
        return f"Invalid regex pattern: {e}"

    matches: list[GrepMatch] = []

    for file_path, file_data in files.items():
        # Filter by path prefix
        if not file_path.startswith(path):
            continue

        # Filter by glob if provided
        if glob and not fnmatch(file_path, glob) and not fnmatch(file_path.split("/")[-1], glob):
            continue

        content = file_data_to_string(file_data)
        for line_num, line in enumerate(content.splitlines(), 1):
            if regex.search(line):
                matches.append({
                    "path": file_path,
                    "line": line_num,
                    "text": line,
                })

    return matches


def format_grep_matches(matches: list[GrepMatch], output_mode: str) -> str:
    """Format grep matches according to output mode."""
    if not matches:
        return "No matches found"

    if output_mode == "files_with_matches":
        # Return unique file paths
        files = sorted(set(m["path"] for m in matches))
        return "\n".join(files)
    elif output_mode == "count":
        # Count matches per file
        counts: dict[str, int] = {}
        for m in matches:
            counts[m["path"]] = counts.get(m["path"], 0) + 1
        lines = [f"{path}: {count}" for path, count in sorted(counts.items())]
        return "\n".join(lines)
    else:  # content
        # Show matching lines with context
        lines = []
        for m in matches:
            lines.append(f"{m['path']}:{m['line']}: {m['text']}")
        return "\n".join(lines)


def truncate_if_too_long(text: str, max_length: int = 50000) -> str:
    """Truncate text if too long."""
    if len(text) > max_length:
        return text[:max_length] + f"\n\n... (truncated, {len(text) - max_length} more characters)"
    return text


def sanitize_tool_call_id(tool_call_id: str) -> str:
    """Sanitize tool call ID for use in file paths."""
    # Replace invalid characters with underscores
    return re.sub(r'[^\w\-]', '_', tool_call_id)
