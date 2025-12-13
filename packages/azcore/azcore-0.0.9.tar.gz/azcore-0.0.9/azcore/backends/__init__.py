"""
Backend implementations for file storage and operations.

Provides pluggable backend protocols for different storage strategies:
- StateBackend: Ephemeral storage in LangGraph state
- FilesystemBackend: Direct filesystem access
- StoreBackend: Persistent storage via LangGraph's BaseStore
- CompositeBackend: Route operations to different backends by path
"""

from azcore.backends.protocol import (
    BackendProtocol,
    BackendFactory,
    WriteResult,
    EditResult,
    FileInfo,
    GrepMatch,
)
from azcore.backends.state import StateBackend
from azcore.backends.filesystem import FilesystemBackend
from azcore.backends.store import StoreBackend
from azcore.backends.composite import CompositeBackend

__all__ = [
    "BackendProtocol",
    "BackendFactory",
    "WriteResult",
    "EditResult",
    "FileInfo",
    "GrepMatch",
    "StateBackend",
    "FilesystemBackend",
    "StoreBackend",
    "CompositeBackend",
]
