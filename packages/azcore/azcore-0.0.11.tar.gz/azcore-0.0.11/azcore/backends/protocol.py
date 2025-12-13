"""Protocol definition for pluggable storage backends.

This module defines the BackendProtocol that all backend implementations
must follow. Backends can store files in different locations (state, filesystem,
database, etc.) and provide a uniform interface for file operations.
"""

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any, Protocol, TypeAlias, TypedDict, runtime_checkable


class FileInfo(TypedDict, total=False):
    """File information dictionary."""
    path: str
    """Absolute file path."""
    is_dir: bool
    """Whether the path is a directory."""
    size: int
    """File size in bytes."""
    modified_at: str
    """ISO 8601 timestamp of last modification."""


class GrepMatch(TypedDict):
    """Grep search match result."""
    path: str
    """File path where match was found."""
    line: int
    """Line number (1-indexed)."""
    text: str
    """Line content."""


@dataclass
class WriteResult:
    """Result from backend write operations.

    Attributes:
        error: Error message on failure, None on success.
        path: Absolute path of written file, None on failure.
        files_update: State update dict for checkpoint backends, None for external storage.
    """
    error: str | None = None
    path: str | None = None
    files_update: dict[str, Any] | None = None


@dataclass
class EditResult:
    """Result from backend edit operations.

    Attributes:
        error: Error message on failure, None on success.
        path: Absolute path of edited file, None on failure.
        files_update: State update dict for checkpoint backends, None for external storage.
        occurrences: Number of replacements made, None on failure.
    """
    error: str | None = None
    path: str | None = None
    files_update: dict[str, Any] | None = None
    occurrences: int | None = None


@runtime_checkable
class BackendProtocol(Protocol):
    """Protocol for pluggable storage backends.

    Backends can store files in different locations (state, filesystem, database, etc.)
    and provide a uniform interface for file operations.
    """

    def ls_info(self, path: str) -> list[FileInfo]:
        """List files and directories in specified directory (non-recursive)."""
        ...

    def read(
        self,
        file_path: str,
        offset: int = 0,
        limit: int = 2000,
    ) -> str:
        """Read file content with line numbers or an error string."""
        ...

    def grep_raw(
        self,
        pattern: str,
        path: str | None = None,
        glob: str | None = None,
    ) -> list[GrepMatch] | str:
        """Search for pattern in files, returns structured results or error."""
        ...

    def glob_info(self, pattern: str, path: str = "/") -> list[FileInfo]:
        """Find files matching glob pattern."""
        ...

    def write(
        self,
        file_path: str,
        content: str,
    ) -> WriteResult:
        """Create a new file. Returns WriteResult with error on failure."""
        ...

    def edit(
        self,
        file_path: str,
        old_string: str,
        new_string: str,
        replace_all: bool = False,
    ) -> EditResult:
        """Edit a file by replacing string occurrences."""
        ...


# Type alias for backend factory functions
BackendFactory: TypeAlias = Callable[[Any], BackendProtocol]
