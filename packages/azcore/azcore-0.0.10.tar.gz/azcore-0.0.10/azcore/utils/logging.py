"""
Logging utilities for the Azcore..

This module provides standardized logging setup and configuration.
"""

import logging
import sys
from pathlib import Path
from typing import Optional


def setup_logging(
    level: str | int = "INFO",
    log_file: Optional[str | Path] = None,
    format_string: Optional[str] = None
) -> None:
    """
    Set up logging for the Azcore..
    
    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Optional path to log file
        format_string: Optional custom format string
    """
    if isinstance(level, str):
        level = getattr(logging, level.upper())
    
    if format_string is None:
        format_string = (
            "%(asctime)s - %(name)s - %(levelname)s - "
            "[%(filename)s:%(lineno)d] - %(message)s"
        )
    
    # Configure root logger
    logging.basicConfig(
        level=level,
        format=format_string,
        handlers=[]
    )
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(logging.Formatter(format_string))
    logging.getLogger().addHandler(console_handler)
    
    # File handler if specified
    if log_file:
        log_file = Path(log_file)
        log_file.parent.mkdir(parents=True, exist_ok=True)
        
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(level)
        file_handler.setFormatter(logging.Formatter(format_string))
        logging.getLogger().addHandler(file_handler)
        
        logging.info(f"Logging to file: {log_file}")
    
    logging.info(f"Logging configured at level: {logging.getLevelName(level)}")


def get_logger(name: str, level: Optional[str | int] = None) -> logging.Logger:
    """
    Get a logger with the specified name.
    
    Args:
        name: Logger name
        level: Optional logging level
        
    Returns:
        Configured logger
    """
    logger = logging.getLogger(name)
    
    if level is not None:
        if isinstance(level, str):
            level = getattr(logging, level.upper())
        logger.setLevel(level)
    
    return logger


class LoggerMixin:
    """
    Mixin class that provides logging capabilities.
    
    Usage:
        >>> class MyClass(LoggerMixin):
        ...     def __init__(self):
        ...         self._setup_logger()
        ...         self.logger.info("Initialized")
    """
    
    def _setup_logger(self, name: Optional[str] = None):
        """
        Set up logger for the class.
        
        Args:
            name: Optional logger name (defaults to class name)
        """
        if name is None:
            name = self.__class__.__name__
        self.logger = get_logger(name)
