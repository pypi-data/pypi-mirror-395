"""File management and operations tools."""

import os
import shutil
from pathlib import Path
from typing import Dict, Any, List
from langchain_core.tools import tool
import json
from .utils import load_prompt


@tool
def read_file(file_path: str) -> Dict[str, Any]:
    """Read content from a file.

    Args:
        file_path: Path to the file to read

    Returns:
        Dict with file content and metadata
    """
    try:
        path = Path(file_path)
        if not path.exists():
            return {"status": "error", "message": "File not found"}
        
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        return {
            "status": "success",
            "file_path": str(path),
            "content": content,
            "size_bytes": path.stat().st_size,
            "extension": path.suffix
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


@tool
def write_file(file_path: str, content: str) -> Dict[str, Any]:
    """Write content to a file.

    Args:
        file_path: Path to the file to write
        content: Content to write to the file

    Returns:
        Dict with operation status
    """
    try:
        path = Path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return {
            "status": "success",
            "file_path": str(path),
            "bytes_written": len(content.encode('utf-8')),
            "message": f"Successfully wrote to {path.name}"
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


@tool
def list_directory(directory_path: str) -> Dict[str, Any]:
    """List contents of a directory.

    Args:
        directory_path: Path to the directory

    Returns:
        Dict with directory contents
    """
    try:
        path = Path(directory_path)
        if not path.exists():
            return {"status": "error", "message": "Directory not found"}
        
        if not path.is_dir():
            return {"status": "error", "message": "Path is not a directory"}
        
        files = []
        directories = []
        
        for item in path.iterdir():
            if item.is_file():
                files.append({
                    "name": item.name,
                    "size": item.stat().st_size,
                    "extension": item.suffix
                })
            elif item.is_dir():
                directories.append(item.name)
        
        return {
            "status": "success",
            "path": str(path),
            "files": files,
            "directories": directories,
            "total_files": len(files),
            "total_directories": len(directories)
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


@tool
def delete_file(file_path: str) -> Dict[str, Any]:
    """Delete a file.

    Args:
        file_path: Path to the file to delete

    Returns:
        Dict with operation status
    """
    try:
        path = Path(file_path)
        if not path.exists():
            return {"status": "error", "message": "File not found"}
        
        if path.is_dir():
            return {"status": "error", "message": "Cannot delete directory with this tool"}
        
        path.unlink()
        return {
            "status": "success",
            "message": f"Successfully deleted {path.name}"
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


@tool
def copy_file(source_path: str, destination_path: str) -> Dict[str, Any]:
    """Copy a file from source to destination.

    Args:
        source_path: Path to the source file
        destination_path: Path to the destination

    Returns:
        Dict with operation status
    """
    try:
        source = Path(source_path)
        destination = Path(destination_path)
        
        if not source.exists():
            return {"status": "error", "message": "Source file not found"}
        
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
        
        return {
            "status": "success",
            "source": str(source),
            "destination": str(destination),
            "message": f"Successfully copied {source.name} to {destination}"
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


@tool
def search_files(directory_path: str, pattern: str) -> Dict[str, Any]:
    """Search for files matching a pattern in a directory.

    Args:
        directory_path: Directory to search in
        pattern: File pattern to match (e.g., *.txt, *.py)

    Returns:
        Dict with matching files
    """
    try:
        path = Path(directory_path)
        if not path.exists():
            return {"status": "error", "message": "Directory not found"}
        
        matches = list(path.glob(f"**/{pattern}"))
        
        results = []
        for match in matches:
            if match.is_file():
                results.append({
                    "path": str(match),
                    "name": match.name,
                    "size": match.stat().st_size
                })
        
        return {
            "status": "success",
            "pattern": pattern,
            "directory": str(path),
            "matches": results,
            "count": len(results)
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


# Export tools list
file_tools = [
    read_file,
    write_file,
    list_directory,
    delete_file,
    copy_file,
    search_files
]

# Team configuration
file_team_config = {
    "name": "file_team",
    "prompt": load_prompt("file_team"),
    "description": "File system operations and management",
    "rl_config": {
        "q_table_path": "rl_data/file_q_table.pkl",
        "exploration_rate": 0.1,
        "use_embeddings": False,
        "success_reward": 1.0,
        "failure_reward": -0.5,
        "empty_penalty": -0.5,
    }
}
