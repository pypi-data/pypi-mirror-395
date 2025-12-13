"""
Base structure utilities for the Azcore..

This module provides operational utilities for agents and workflows including
async operations, batching, resource monitoring, and data compression.
Inspired by Swarm's BaseStructure pattern.
"""
import gzip
import json
import asyncio
from typing import Any, Dict, List, Optional, Callable
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
import logging

try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False
    logging.warning("psutil not available, resource monitoring disabled")

try:
    import yaml
    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False
    logging.warning("PyYAML not available, YAML export disabled")

from azcore.exceptions import ValidationError

logger = logging.getLogger(__name__)


class BaseStructure:
    """
    Base structure with operational utilities.

    Provides common functionality for agents, teams, and workflows including:
    - Async operations
    - Batch processing
    - Resource monitoring
    - Data persistence and compression
    - Configuration management
    - Metadata tracking

    Attributes:
        name: Structure identifier
        description: Structure description
        save_metadata_on: Enable metadata saving
        save_artifact_path: Path for saving artifacts
        save_metadata_path: Path for saving metadata
        save_error_path: Path for saving errors
        workspace_dir: Working directory

    Example:
        >>> class MyAgent(BaseStructure):
        ...     def __init__(self, name: str):
        ...         super().__init__(name=name)
        ...
        ...     def run(self, task: str):
        ...         # Agent logic here
        ...         return result
        >>>
        >>> agent = MyAgent("worker")
        >>> agent.save_metadata({"status": "initialized"})
        >>> agent.monitor_resources()
    """

    def __init__(
        self,
        name: Optional[str] = None,
        description: Optional[str] = None,
        save_metadata_on: bool = True,
        save_artifact_path: Optional[str] = "./artifacts",
        save_metadata_path: Optional[str] = "./metadata",
        save_error_path: Optional[str] = "./errors",
        workspace_dir: Optional[str] = "./workspace",
    ):
        """
        Initialize base structure.

        Args:
            name: Structure identifier
            description: Structure description
            save_metadata_on: Enable metadata saving
            save_artifact_path: Path for artifacts
            save_metadata_path: Path for metadata
            save_error_path: Path for errors
            workspace_dir: Working directory
        """
        self.name = name
        self.description = description
        self.save_metadata_on = save_metadata_on
        self.save_artifact_path = Path(save_artifact_path)
        self.save_metadata_path = Path(save_metadata_path)
        self.save_error_path = Path(save_error_path)
        self.workspace_dir = Path(workspace_dir)

        # Create directories
        for path in [
            self.save_artifact_path,
            self.save_metadata_path,
            self.save_error_path,
            self.workspace_dir
        ]:
            path.mkdir(parents=True, exist_ok=True)

    def run(self, *args, **kwargs):
        """Run the structure (to be overridden by subclasses)."""
        raise NotImplementedError("Subclasses must implement run()")

    # ============================================================================
    # File Operations
    # ============================================================================

    def save_to_file(self, data: Any, file_path: str) -> None:
        """
        Save data to JSON file.

        Args:
            data: Data to save
            file_path: Target file path
        """
        path = Path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)

        with open(path, "w") as f:
            json.dump(data, f, indent=2, default=str)

        logger.debug(f"Saved data to {file_path}")

    def load_from_file(self, file_path: str) -> Any:
        """
        Load data from JSON file.

        Args:
            file_path: Source file path

        Returns:
            Loaded data
        """
        with open(file_path) as f:
            return json.load(f)

    # ============================================================================
    # Metadata Operations
    # ============================================================================

    def save_metadata(self, metadata: Dict[str, Any]) -> None:
        """
        Save metadata to file.

        Args:
            metadata: Metadata dictionary
        """
        if not self.save_metadata_on:
            return

        file_path = self.save_metadata_path / f"{self.name}_metadata.json"
        metadata["saved_at"] = self._current_timestamp()
        self.save_to_file(metadata, str(file_path))

    def load_metadata(self) -> Dict[str, Any]:
        """
        Load metadata from file.

        Returns:
            Metadata dictionary
        """
        file_path = self.save_metadata_path / f"{self.name}_metadata.json"
        return self.load_from_file(str(file_path))

    # ============================================================================
    # Error Handling
    # ============================================================================

    def log_error(self, error_message: str) -> None:
        """
        Log error to file.

        Args:
            error_message: Error message to log
        """
        file_path = self.save_error_path / f"{self.name}_errors.log"
        timestamp = self._current_timestamp()

        with open(file_path, "a") as f:
            f.write(f"[{timestamp}] {error_message}\n")

        logger.error(f"{self.name}: {error_message}")

    # ============================================================================
    # Artifact Management
    # ============================================================================

    def save_artifact(self, artifact: Any, artifact_name: str) -> None:
        """
        Save artifact to file.

        Args:
            artifact: Artifact data
            artifact_name: Artifact identifier
        """
        file_path = self.save_artifact_path / f"{artifact_name}.json"
        self.save_to_file(artifact, str(file_path))
        logger.info(f"Saved artifact: {artifact_name}")

    def load_artifact(self, artifact_name: str) -> Any:
        """
        Load artifact from file.

        Args:
            artifact_name: Artifact identifier

        Returns:
            Artifact data
        """
        file_path = self.save_artifact_path / f"{artifact_name}.json"
        return self.load_from_file(str(file_path))

    # ============================================================================
    # Event Logging
    # ============================================================================

    def _current_timestamp(self) -> str:
        """Get current timestamp."""
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def log_event(self, event: str, event_type: str = "INFO") -> None:
        """
        Log event to file.

        Args:
            event: Event description
            event_type: Event type (INFO, WARNING, ERROR, etc.)
        """
        timestamp = self._current_timestamp()
        log_message = f"[{timestamp}] [{event_type}] {event}\n"

        file_path = self.save_metadata_path / f"{self.name}_events.log"
        with open(file_path, "a") as f:
            f.write(log_message)

    # ============================================================================
    # Async Operations
    # ============================================================================

    async def run_async(self, *args, **kwargs):
        """Run the structure asynchronously."""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.run, *args, **kwargs)

    async def save_metadata_async(self, metadata: Dict[str, Any]) -> None:
        """Save metadata asynchronously."""
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, self.save_metadata, metadata)

    async def load_metadata_async(self) -> Dict[str, Any]:
        """Load metadata asynchronously."""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.load_metadata)

    async def log_error_async(self, error_message: str) -> None:
        """Log error asynchronously."""
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, self.log_error, error_message)

    async def save_artifact_async(self, artifact: Any, artifact_name: str) -> None:
        """Save artifact asynchronously."""
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(
            None, self.save_artifact, artifact, artifact_name
        )

    async def load_artifact_async(self, artifact_name: str) -> Any:
        """Load artifact asynchronously."""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.load_artifact, artifact_name)

    async def log_event_async(self, event: str, event_type: str = "INFO") -> None:
        """Log event asynchronously."""
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, self.log_event, event, event_type)

    # ============================================================================
    # Thread-based Operations
    # ============================================================================

    def run_in_thread(self, *args, **kwargs):
        """Run the structure in a thread."""
        with ThreadPoolExecutor() as executor:
            return executor.submit(self.run, *args, **kwargs)

    def save_metadata_in_thread(self, metadata: Dict[str, Any]):
        """Save metadata in a thread."""
        with ThreadPoolExecutor() as executor:
            return executor.submit(self.save_metadata, metadata)

    def run_concurrent(self, *args, **kwargs):
        """Run the structure concurrently."""
        return asyncio.run(self.run_async(*args, **kwargs))

    # ============================================================================
    # Data Compression
    # ============================================================================

    def compress_data(self, data: Any) -> bytes:
        """
        Compress data using gzip.

        Args:
            data: Data to compress

        Returns:
            Compressed bytes
        """
        json_str = json.dumps(data, default=str)
        return gzip.compress(json_str.encode())

    def decompress_data(self, data: bytes) -> Any:
        """
        Decompress gzip data.

        Args:
            data: Compressed bytes

        Returns:
            Decompressed data
        """
        json_str = gzip.decompress(data).decode()
        return json.loads(json_str)

    # ============================================================================
    # Batch Processing
    # ============================================================================

    def run_batched(
        self,
        batched_data: List[Any],
        batch_size: int = 10,
        *args,
        **kwargs
    ) -> List[Any]:
        """
        Run batched data in parallel.

        Args:
            batched_data: List of data items to process
            batch_size: Maximum concurrent workers

        Returns:
            List of results
        """
        with ThreadPoolExecutor(max_workers=batch_size) as executor:
            futures = [
                executor.submit(self.run, data, *args, **kwargs)
                for data in batched_data
            ]
            return [future.result() for future in futures]

    def run_concurrent_batch(
        self,
        tasks: List[Any],
        max_workers: Optional[int] = None,
        *args,
        **kwargs
    ) -> List[Any]:
        """
        Run multiple tasks concurrently with better error handling.

        Args:
            tasks: List of tasks to process
            max_workers: Maximum number of concurrent workers (defaults to CPU count)

        Returns:
            List of results in completion order
        """
        if max_workers is None:
            import os
            max_workers = os.cpu_count()

        results = []
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_task = {
                executor.submit(self.run, task, *args, **kwargs): task
                for task in tasks
            }
            
            for future in as_completed(future_to_task):
                task = future_to_task[future]
                try:
                    result = future.result()
                    results.append(result)
                except Exception as e:
                    error_msg = f"Task {task} failed: {str(e)}"
                    self.log_error(error_msg)
                    logger.error(error_msg)
                    results.append({"error": str(e), "task": task})
        
        return results

    # ============================================================================
    # Configuration Management
    # ============================================================================

    def load_config(self, config_path: str) -> Dict[str, Any]:
        """
        Load configuration from file.

        Args:
            config_path: Path to config file (JSON or YAML)

        Returns:
            Configuration dictionary
        """
        path = Path(config_path)

        if path.suffix == ".json":
            return self.load_from_file(str(path))
        elif path.suffix in [".yaml", ".yml"]:
            if not YAML_AVAILABLE:
                raise ImportError("PyYAML required for YAML configs")
            with open(path) as f:
                return yaml.safe_load(f)
        else:
            logger.error(f"Unsupported config format: {path.suffix} for file {path}")
            raise ValidationError(
                f"Unsupported config format: {path.suffix}",
                details={
                    "file_path": str(path),
                    "format": path.suffix,
                    "supported_formats": [".json", ".yaml", ".yml"]
                }
            )

    # ============================================================================
    # Data Backup
    # ============================================================================

    def backup_data(self, data: Any, backup_path: Optional[str] = None) -> None:
        """
        Backup data to file with timestamp.

        Args:
            data: Data to backup
            backup_path: Backup directory (optional)
        """
        backup_dir = Path(backup_path) if backup_path else self.workspace_dir / "backups"
        backup_dir.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = backup_dir / f"{self.name}_{timestamp}.json"

        self.save_to_file(data, str(backup_file))
        logger.info(f"Backed up data to {backup_file}")

    # ============================================================================
    # Resource Monitoring
    # ============================================================================

    def monitor_resources(self) -> Dict[str, float]:
        """
        Monitor system resource usage.

        Returns:
            Dictionary with memory and CPU usage percentages
        """
        if not PSUTIL_AVAILABLE:
            logger.warning("psutil not available, skipping resource monitoring")
            return {"memory": 0.0, "cpu": 0.0}

        memory = psutil.virtual_memory().percent
        cpu_usage = psutil.cpu_percent(interval=1)

        self.log_event(
            f"Resource usage - Memory: {memory}%, CPU: {cpu_usage}%"
        )

        return {"memory": memory, "cpu": cpu_usage}

    def run_with_resources(self, *args, **kwargs):
        """Run the structure with resource monitoring."""
        self.monitor_resources()
        return self.run(*args, **kwargs)

    def run_with_resources_batched(
        self,
        batched_data: List[Any],
        batch_size: int = 10,
        *args,
        **kwargs
    ) -> List[Any]:
        """Run batched data with resource monitoring."""
        self.monitor_resources()
        return self.run_batched(batched_data, batch_size, *args, **kwargs)

    # ============================================================================
    # Serialization
    # ============================================================================

    def _serialize_callable(self, attr_value: Callable) -> Dict[str, Any]:
        """Serialize callable attributes."""
        return {
            "name": getattr(attr_value, "__name__", type(attr_value).__name__),
            "doc": getattr(attr_value, "__doc__", None),
        }

    def _serialize_attr(self, attr_name: str, attr_value: Any) -> Any:
        """Serialize an individual attribute."""
        try:
            if callable(attr_value):
                return self._serialize_callable(attr_value)
            elif hasattr(attr_value, "to_dict"):
                return attr_value.to_dict()
            else:
                # Test JSON serialization
                json.dumps(attr_value, default=str)
                return attr_value
        except (TypeError, ValueError):
            return f"<Non-serializable: {type(attr_value).__name__}>"

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert structure to dictionary.

        Returns:
            Dictionary representation
        """
        return {
            attr_name: self._serialize_attr(attr_name, attr_value)
            for attr_name, attr_value in self.__dict__.items()
        }

    def to_json(self, indent: int = 2) -> str:
        """Export to JSON string."""
        return json.dumps(self.to_dict(), indent=indent, default=str)

    def to_yaml(self) -> str:
        """Export to YAML string."""
        if not YAML_AVAILABLE:
            raise ImportError("PyYAML required for YAML export")
        return yaml.dump(self.to_dict(), default_flow_style=False)

    def __repr__(self) -> str:
        """
        Return a string representation of the structure.

        Returns:
            String representation
        """
        return f"{self.__class__.__name__}(name='{self.name}')"
