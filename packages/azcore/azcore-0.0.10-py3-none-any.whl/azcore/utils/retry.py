"""
Retry and timeout utilities for the Azcore..

This module provides decorators and utilities for implementing
retry logic with exponential backoff and timeout handling.
"""

import asyncio
import time
import logging
from functools import wraps
from typing import Callable, Type, Tuple, Optional, Any

from azcore.exceptions import TimeoutError as RiseTimeoutError, LLMTimeoutError

logger = logging.getLogger(__name__)


def retry_with_timeout(
    max_retries: int = 3,
    timeout: float = 30.0,
    backoff_factor: float = 2.0,
    exceptions: Tuple[Type[Exception], ...] = (Exception,),
    on_retry: Optional[Callable[[Exception, int], None]] = None
):
    """
    Decorator that adds retry logic with exponential backoff and timeout.
    
    This decorator handles both synchronous and asynchronous functions,
    retrying them on failure with exponential backoff between attempts.
    
    Args:
        max_retries: Maximum number of retry attempts (default: 3)
        timeout: Timeout in seconds for each attempt (default: 30.0)
        backoff_factor: Multiplier for exponential backoff (default: 2.0)
        exceptions: Tuple of exception types to catch and retry
        on_retry: Optional callback function called on each retry
                 Signature: (exception, attempt_number) -> None
    
    Returns:
        Decorated function with retry and timeout logic
        
    Example:
        >>> @retry_with_timeout(max_retries=3, timeout=10.0)
        >>> def call_llm(prompt):
        ...     return llm.invoke(prompt)
        
        >>> @retry_with_timeout(
        ...     max_retries=5,
        ...     timeout=30.0,
        ...     exceptions=(ConnectionError, TimeoutError)
        ... )
        >>> async def async_call_llm(prompt):
        ...     return await llm.ainvoke(prompt)
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def async_wrapper(*args, **kwargs) -> Any:
            """Async wrapper with retry and timeout logic."""
            last_exception = None
            
            for attempt in range(max_retries):
                try:
                    # Execute with timeout
                    result = await asyncio.wait_for(
                        func(*args, **kwargs),
                        timeout=timeout
                    )
                    
                    # Success - log if this was a retry
                    if attempt > 0:
                        logger.info(
                            f"{func.__name__} succeeded on attempt {attempt + 1}/{max_retries}"
                        )
                    
                    return result
                    
                except asyncio.TimeoutError as e:
                    last_exception = LLMTimeoutError(
                        f"{func.__name__} timed out after {timeout}s",
                        details={"attempt": attempt + 1, "timeout": timeout}
                    )
                    logger.warning(
                        f"{func.__name__} timed out on attempt {attempt + 1}/{max_retries}"
                    )
                    
                except exceptions as e:
                    last_exception = e
                    logger.warning(
                        f"{func.__name__} failed on attempt {attempt + 1}/{max_retries}: {str(e)}"
                    )
                
                # Call retry callback if provided
                if on_retry and last_exception:
                    try:
                        on_retry(last_exception, attempt + 1)
                    except Exception as callback_error:
                        logger.error(f"Retry callback failed: {callback_error}")
                
                # If not last attempt, wait with exponential backoff
                if attempt < max_retries - 1:
                    wait_time = backoff_factor ** attempt
                    logger.debug(f"Waiting {wait_time}s before retry")
                    await asyncio.sleep(wait_time)
            
            # All retries exhausted
            logger.error(
                f"{func.__name__} failed after {max_retries} attempts"
            )
            raise last_exception
        
        @wraps(func)
        def sync_wrapper(*args, **kwargs) -> Any:
            """Synchronous wrapper with retry and timeout logic."""
            last_exception = None
            
            for attempt in range(max_retries):
                try:
                    # For sync functions, we can't easily enforce timeout
                    # but we can still retry
                    result = func(*args, **kwargs)
                    
                    # Success - log if this was a retry
                    if attempt > 0:
                        logger.info(
                            f"{func.__name__} succeeded on attempt {attempt + 1}/{max_retries}"
                        )
                    
                    return result
                    
                except exceptions as e:
                    last_exception = e
                    logger.warning(
                        f"{func.__name__} failed on attempt {attempt + 1}/{max_retries}: {str(e)}"
                    )
                
                # Call retry callback if provided
                if on_retry and last_exception:
                    try:
                        on_retry(last_exception, attempt + 1)
                    except Exception as callback_error:
                        logger.error(f"Retry callback failed: {callback_error}")
                
                # If not last attempt, wait with exponential backoff
                if attempt < max_retries - 1:
                    wait_time = backoff_factor ** attempt
                    logger.debug(f"Waiting {wait_time}s before retry")
                    time.sleep(wait_time)
            
            # All retries exhausted
            logger.error(
                f"{func.__name__} failed after {max_retries} attempts"
            )
            raise last_exception
        
        # Return appropriate wrapper based on function type
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper
    
    return decorator


def timeout(seconds: float, error_message: str = None):
    """
    Simple timeout decorator for async functions.
    
    Args:
        seconds: Timeout duration in seconds
        error_message: Optional custom error message
        
    Returns:
        Decorated function with timeout
        
    Example:
        >>> @timeout(30.0, "LLM call took too long")
        >>> async def call_llm(prompt):
        ...     return await llm.ainvoke(prompt)
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs) -> Any:
            try:
                return await asyncio.wait_for(func(*args, **kwargs), timeout=seconds)
            except asyncio.TimeoutError:
                msg = error_message or f"{func.__name__} timed out after {seconds}s"
                raise RiseTimeoutError(msg, details={"timeout": seconds})
        
        return wrapper
    
    return decorator


def simple_retry(max_retries: int = 3, delay: float = 1.0):
    """
    Simple retry decorator without timeout (for backwards compatibility).
    
    Args:
        max_retries: Maximum number of retry attempts
        delay: Fixed delay between retries in seconds
        
    Returns:
        Decorated function with simple retry logic
        
    Example:
        >>> @simple_retry(max_retries=3, delay=2.0)
        >>> def unstable_operation():
        ...     # might fail occasionally
        ...     pass
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_retries - 1:
                        raise
                    logger.debug(
                        f"{func.__name__} failed on attempt {attempt + 1}, "
                        f"retrying in {delay}s"
                    )
                    time.sleep(delay)
        
        return wrapper
    
    return decorator


class RetryConfig:
    """
    Configuration class for retry behavior.
    
    This can be used to create reusable retry configurations.
    
    Example:
        >>> llm_retry_config = RetryConfig(
        ...     max_retries=5,
        ...     timeout=30.0,
        ...     backoff_factor=2.0,
        ...     exceptions=(ConnectionError, TimeoutError)
        ... )
        >>> 
        >>> @llm_retry_config.apply()
        >>> def call_llm(prompt):
        ...     return llm.invoke(prompt)
    """
    
    def __init__(
        self,
        max_retries: int = 3,
        timeout: float = 30.0,
        backoff_factor: float = 2.0,
        exceptions: Tuple[Type[Exception], ...] = (Exception,),
        on_retry: Optional[Callable[[Exception, int], None]] = None
    ):
        """Initialize retry configuration."""
        self.max_retries = max_retries
        self.timeout = timeout
        self.backoff_factor = backoff_factor
        self.exceptions = exceptions
        self.on_retry = on_retry
    
    def apply(self):
        """Apply this configuration as a decorator."""
        return retry_with_timeout(
            max_retries=self.max_retries,
            timeout=self.timeout,
            backoff_factor=self.backoff_factor,
            exceptions=self.exceptions,
            on_retry=self.on_retry
        )


# Predefined retry configurations for common use cases
LLM_RETRY_CONFIG = RetryConfig(
    max_retries=3,
    timeout=30.0,
    backoff_factor=2.0,
    exceptions=(Exception,)
)

TOOL_RETRY_CONFIG = RetryConfig(
    max_retries=2,
    timeout=60.0,
    backoff_factor=1.5,
    exceptions=(Exception,)
)

FAST_RETRY_CONFIG = RetryConfig(
    max_retries=2,
    timeout=10.0,
    backoff_factor=1.5,
    exceptions=(Exception,)
)
