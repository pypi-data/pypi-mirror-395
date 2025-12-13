"""
Decorator utilities for the Azcore..

This module provides decorators for async/sync conversion, caching,
and other common patterns.
"""

import asyncio
import functools
from typing import Callable
import logging

logger = logging.getLogger(__name__)


def async_to_sync(async_func: Callable) -> Callable:
    """
    Convert an async function to sync by running it in an event loop.
    
    Args:
        async_func: Async function to convert
        
    Returns:
        Sync wrapper function
        
    Example:
        >>> @async_to_sync
        ... async def my_async_func():
        ...     return await some_async_operation()
        >>> result = my_async_func()  # Can now be called synchronously
    """
    @functools.wraps(async_func)
    def wrapper(*args, **kwargs):
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            # No loop is running
            return asyncio.run(async_func(*args, **kwargs))
        else:
            # Loop is running, create task
            return loop.run_until_complete(async_func(*args, **kwargs))
    
    return wrapper


def sync_to_async(sync_func: Callable) -> Callable:
    """
    Convert a sync function to async.
    
    Args:
        sync_func: Sync function to convert
        
    Returns:
        Async wrapper function
        
    Example:
        >>> @sync_to_async
        ... def my_sync_func():
        ...     return some_operation()
        >>> result = await my_sync_func()  # Can now be awaited
    """
    @functools.wraps(sync_func)
    async def wrapper(*args, **kwargs):
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, lambda: sync_func(*args, **kwargs))
    
    return wrapper


def log_execution(func: Callable) -> Callable:
    """
    Decorator to log function execution.
    
    Args:
        func: Function to wrap
        
    Returns:
        Wrapped function with logging
        
    Example:
        >>> @log_execution
        ... def my_function(x):
        ...     return x * 2
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        func_name = func.__name__
        logger.debug(f"Executing {func_name}")
        try:
            result = func(*args, **kwargs)
            logger.debug(f"Completed {func_name}")
            return result
        except Exception as e:
            logger.error(f"Error in {func_name}: {e}")
            raise
    
    return wrapper


def log_async_execution(func: Callable) -> Callable:
    """
    Decorator to log async function execution.
    
    Args:
        func: Async function to wrap
        
    Returns:
        Wrapped async function with logging
    """
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        func_name = func.__name__
        logger.debug(f"Executing async {func_name}")
        try:
            result = await func(*args, **kwargs)
            logger.debug(f"Completed async {func_name}")
            return result
        except Exception as e:
            logger.error(f"Error in async {func_name}: {e}")
            raise
    
    return wrapper


def retry(max_attempts: int = 3, delay: float = 1.0):
    """
    Decorator to retry function on failure.
    
    Args:
        max_attempts: Maximum number of retry attempts
        delay: Delay between retries in seconds
        
    Returns:
        Decorator function
        
    Example:
        >>> @retry(max_attempts=3, delay=2.0)
        ... def unstable_function():
        ...     # Function that might fail
        ...     pass
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    logger.warning(
                        f"Attempt {attempt}/{max_attempts} failed for {func.__name__}: {e}"
                    )
                    if attempt < max_attempts:
                        import time
                        time.sleep(delay)
            
            logger.error(f"All {max_attempts} attempts failed for {func.__name__}")
            raise last_exception
        
        return wrapper
    
    return decorator


def cache_result(func: Callable) -> Callable:
    """
    Simple caching decorator for functions with hashable arguments.
    
    Args:
        func: Function to cache
        
    Returns:
        Wrapped function with caching
    """
    cache = {}
    
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Create cache key
        key = (args, tuple(sorted(kwargs.items())))
        
        if key in cache:
            logger.debug(f"Cache hit for {func.__name__}")
            return cache[key]
        
        result = func(*args, **kwargs)
        cache[key] = result
        logger.debug(f"Cached result for {func.__name__}")
        
        return result
    
    # Add method to clear cache
    wrapper.clear_cache = lambda: cache.clear()
    
    return wrapper
