"""StoreBackend: Adapter for persistent storage (cross-thread).

This backend is designed to work with persistent storage systems
that maintain data across conversation threads.
"""

from typing import Any

from azcore.backends.protocol import EditResult, WriteResult, FileInfo, GrepMatch
from azcore.backends.utils import (
    _glob_search_files,
    create_file_data,
    file_data_to_string,
    format_read_response,
    grep_matches_from_files,
    perform_string_replacement,
    update_file_data,
)


class StoreBackend:
    """Backend that stores files persistently (implementation placeholder).

    This is a simplified version that stores files in a dictionary.
    In production, this would integrate with a database or persistent store.
    """

    def __init__(self, runtime: Any = None):
        """Initialize StoreBackend."""
        self.runtime = runtime
        # In-memory storage for this simplified version
        self._storage: dict[str, dict[str, Any]] = {}

    def ls_info(self, path: str) -> list[FileInfo]:
        """List files and directories in the specified directory (non-recursive)."""
        infos: list[FileInfo] = []
        subdirs: set[str] = set()

        # Normalize path to have trailing slash
        normalized_path = path if path.endswith("/") else path + "/"

        for k, fd in self._storage.items():
            if not k.startswith(normalized_path):
                continue

            relative = k[len(normalized_path):]
            if "/" in relative:
                subdir_name = relative.split("/")[0]
                subdirs.add(normalized_path + subdir_name + "/")
                continue

            size = len("\n".join(fd.get("content", [])))
            infos.append({
                "path": k,
                "is_dir": False,
                "size": int(size),
                "modified_at": fd.get("modified_at", ""),
            })

        for subdir in sorted(subdirs):
            infos.append({
                "path": subdir,
                "is_dir": True,
                "size": 0,
                "modified_at": "",
            })

        infos.sort(key=lambda x: x.get("path", ""))
        return infos

    def read(
        self,
        file_path: str,
        offset: int = 0,
        limit: int = 2000,
    ) -> str:
        """Read file content with line numbers."""
        file_data = self._storage.get(file_path)

        if file_data is None:
            return f"Error: File '{file_path}' not found"

        return format_read_response(file_data, offset, limit)

    def write(
        self,
        file_path: str,
        content: str,
    ) -> WriteResult:
        """Create a new file with content."""
        if file_path in self._storage:
            return WriteResult(
                error=f"Cannot write to {file_path} because it already exists. "
                "Read and then make an edit, or write to a new path."
            )

        new_file_data = create_file_data(content)
        self._storage[file_path] = new_file_data
        return WriteResult(path=file_path, files_update=None)

    def edit(
        self,
        file_path: str,
        old_string: str,
        new_string: str,
        replace_all: bool = False,
    ) -> EditResult:
        """Edit a file by replacing string occurrences."""
        file_data = self._storage.get(file_path)

        if file_data is None:
            return EditResult(error=f"Error: File '{file_path}' not found")

        content = file_data_to_string(file_data)
        result = perform_string_replacement(content, old_string, new_string, replace_all)

        if isinstance(result, str):
            return EditResult(error=result)

        new_content, occurrences = result
        new_file_data = update_file_data(file_data, new_content)
        self._storage[file_path] = new_file_data
        return EditResult(
            path=file_path,
            files_update=None,
            occurrences=int(occurrences)
        )

    def grep_raw(
        self,
        pattern: str,
        path: str = "/",
        glob: str | None = None,
    ) -> list[GrepMatch] | str:
        """Search for pattern in files."""
        return grep_matches_from_files(self._storage, pattern, path, glob)

    def glob_info(self, pattern: str, path: str = "/") -> list[FileInfo]:
        """Find files matching glob pattern."""
        result = _glob_search_files(self._storage, pattern, path)
        if result == "No files found":
            return []
        paths = result.split("\n")
        infos: list[FileInfo] = []
        for p in paths:
            fd = self._storage.get(p)
            size = len("\n".join(fd.get("content", []))) if fd else 0
            infos.append({
                "path": p,
                "is_dir": False,
                "size": int(size),
                "modified_at": fd.get("modified_at", "") if fd else "",
            })
        return infos
