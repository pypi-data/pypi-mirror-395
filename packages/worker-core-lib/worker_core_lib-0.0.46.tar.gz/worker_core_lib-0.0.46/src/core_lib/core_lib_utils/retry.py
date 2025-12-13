"""
Retry utilities with exponential backoff and jitter.

Provides decorators and helper functions for retrying operations that may fail
due to transient errors (network timeouts, connection issues, rate limits, etc.).

Features:
- Exponential backoff with configurable base delay and max delay
- Jitter to prevent thundering herd problem
- Configurable retry attempts and exception types
- Logging of retry attempts
"""

import asyncio
import functools
import logging
import random
import time
from typing import Any, Callable, List, Optional, Tuple, Type, TypeVar, Union

logger = logging.getLogger(__name__)

T = TypeVar('T')


def calculate_backoff_delay(
    attempt: int,
    base_delay: float = 1.0,
    max_delay: float = 60.0,
    exponential_base: float = 2.0,
    jitter: bool = True
) -> float:
    """
    Calculate delay for retry attempt using exponential backoff.
    
    Args:
        attempt: Current retry attempt (0-indexed)
        base_delay: Initial delay in seconds
        max_delay: Maximum delay in seconds
        exponential_base: Base for exponential calculation (default 2.0)
        jitter: Whether to add random jitter (default True)
    
    Returns:
        Delay in seconds to wait before next retry
    
    Example:
        attempt=0 -> ~1s
        attempt=1 -> ~2s
        attempt=2 -> ~4s
        attempt=3 -> ~8s
        attempt=4 -> ~16s
        attempt=5 -> ~32s
        attempt=6 -> ~60s (capped at max_delay)
    """
    # Calculate exponential delay: base_delay * (exponential_base ^ attempt)
    delay = base_delay * (exponential_base ** attempt)
    
    # Cap at max_delay
    delay = min(delay, max_delay)
    
    # Add jitter: randomize between 50% and 100% of calculated delay
    if jitter:
        delay = delay * (0.5 + random.random() * 0.5)
    
    return delay


def retry_sync(
    max_attempts: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 60.0,
    exponential_base: float = 2.0,
    jitter: bool = True,
    exceptions: Tuple[Type[Exception], ...] = (Exception,),
    on_retry: Optional[Callable[[Exception, int], None]] = None
) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """
    Decorator for retrying synchronous functions with exponential backoff.
    
    Args:
        max_attempts: Maximum number of retry attempts (default 3)
        base_delay: Initial delay in seconds (default 1.0)
        max_delay: Maximum delay in seconds (default 60.0)
        exponential_base: Base for exponential calculation (default 2.0)
        jitter: Whether to add random jitter (default True)
        exceptions: Tuple of exception types to catch and retry (default all Exception)
        on_retry: Optional callback function(exception, attempt) called before each retry
    
    Returns:
        Decorated function that retries on failure
    
    Example:
        @retry_sync(max_attempts=5, base_delay=2.0)
        def connect_to_sftp():
            # May fail with timeout on first try
            return sftp_client.connect()
    """
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            last_exception = None
            
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    
                    # Don't retry on last attempt
                    if attempt == max_attempts - 1:
                        logger.error(
                            f"Final retry attempt {attempt + 1}/{max_attempts} failed for {func.__name__}: {e}"
                        )
                        raise
                    
                    # Calculate backoff delay
                    delay = calculate_backoff_delay(
                        attempt, base_delay, max_delay, exponential_base, jitter
                    )
                    
                    logger.warning(
                        f"Retry attempt {attempt + 1}/{max_attempts} for {func.__name__} "
                        f"failed: {e}. Retrying in {delay:.2f}s..."
                    )
                    
                    # Call retry callback if provided
                    if on_retry:
                        try:
                            on_retry(e, attempt)
                        except Exception as callback_error:
                            logger.error(f"Retry callback failed: {callback_error}")
                    
                    # Wait before retry
                    time.sleep(delay)
            
            # Should never reach here, but for type safety
            if last_exception:
                raise last_exception
            raise RuntimeError(f"Retry loop exhausted for {func.__name__}")
        
        return wrapper
    return decorator


def retry_async(
    max_attempts: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 60.0,
    exponential_base: float = 2.0,
    jitter: bool = True,
    exceptions: Tuple[Type[Exception], ...] = (Exception,),
    on_retry: Optional[Callable[[Exception, int], Any]] = None
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """
    Decorator for retrying asynchronous functions with exponential backoff.
    
    Args:
        max_attempts: Maximum number of retry attempts (default 3)
        base_delay: Initial delay in seconds (default 1.0)
        max_delay: Maximum delay in seconds (default 60.0)
        exponential_base: Base for exponential calculation (default 2.0)
        jitter: Whether to add random jitter (default True)
        exceptions: Tuple of exception types to catch and retry (default all Exception)
        on_retry: Optional async/sync callback function(exception, attempt) called before each retry
    
    Returns:
        Decorated async function that retries on failure
    
    Example:
        @retry_async(max_attempts=5, base_delay=2.0)
        async def fetch_api_data():
            # May fail with timeout or rate limit
            return await api_client.get('/data')
    """
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @functools.wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            last_exception = None
            
            for attempt in range(max_attempts):
                try:
                    return await func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    
                    # Don't retry on last attempt
                    if attempt == max_attempts - 1:
                        logger.error(
                            f"Final retry attempt {attempt + 1}/{max_attempts} failed for {func.__name__}: {e}"
                        )
                        raise
                    
                    # Calculate backoff delay
                    delay = calculate_backoff_delay(
                        attempt, base_delay, max_delay, exponential_base, jitter
                    )
                    
                    logger.warning(
                        f"Retry attempt {attempt + 1}/{max_attempts} for {func.__name__} "
                        f"failed: {e}. Retrying in {delay:.2f}s..."
                    )
                    
                    # Call retry callback if provided
                    if on_retry:
                        try:
                            result = on_retry(e, attempt)
                            # Support both sync and async callbacks
                            if asyncio.iscoroutine(result):
                                await result
                        except Exception as callback_error:
                            logger.error(f"Retry callback failed: {callback_error}")
                    
                    # Wait before retry
                    await asyncio.sleep(delay)
            
            # Should never reach here, but for type safety
            if last_exception:
                raise last_exception
            raise RuntimeError(f"Retry loop exhausted for {func.__name__}")
        
        return wrapper
    return decorator


def execute_with_retry_sync(
    func: Callable[..., T],
    *args: Any,
    max_attempts: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 60.0,
    exponential_base: float = 2.0,
    jitter: bool = True,
    exceptions: Tuple[Type[Exception], ...] = (Exception,),
    on_retry: Optional[Callable[[Exception, int], None]] = None,
    **kwargs: Any
) -> T:
    """
    Execute a synchronous function with retry logic (non-decorator version).
    
    Useful for one-off retry operations without decorating the function.
    
    Args:
        func: Function to execute
        *args: Positional arguments for func
        max_attempts: Maximum number of retry attempts
        base_delay: Initial delay in seconds
        max_delay: Maximum delay in seconds
        exponential_base: Base for exponential calculation
        jitter: Whether to add random jitter
        exceptions: Tuple of exception types to catch and retry
        on_retry: Optional callback function(exception, attempt) called before each retry
        **kwargs: Keyword arguments for func
    
    Returns:
        Result of func(*args, **kwargs)
    
    Example:
        result = execute_with_retry_sync(
            sftp_client.connect,
            host='example.com',
            max_attempts=5,
            base_delay=2.0
        )
    """
    @retry_sync(
        max_attempts=max_attempts,
        base_delay=base_delay,
        max_delay=max_delay,
        exponential_base=exponential_base,
        jitter=jitter,
        exceptions=exceptions,
        on_retry=on_retry
    )
    def _wrapper() -> T:
        return func(*args, **kwargs)
    
    return _wrapper()


async def execute_with_retry_async(
    func: Callable[..., Any],
    *args: Any,
    max_attempts: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 60.0,
    exponential_base: float = 2.0,
    jitter: bool = True,
    exceptions: Tuple[Type[Exception], ...] = (Exception,),
    on_retry: Optional[Callable[[Exception, int], Any]] = None,
    **kwargs: Any
) -> Any:
    """
    Execute an asynchronous function with retry logic (non-decorator version).
    
    Useful for one-off retry operations without decorating the function.
    
    Args:
        func: Async function to execute
        *args: Positional arguments for func
        max_attempts: Maximum number of retry attempts
        base_delay: Initial delay in seconds
        max_delay: Maximum delay in seconds
        exponential_base: Base for exponential calculation
        jitter: Whether to add random jitter
        exceptions: Tuple of exception types to catch and retry
        on_retry: Optional async/sync callback function(exception, attempt) called before each retry
        **kwargs: Keyword arguments for func
    
    Returns:
        Result of await func(*args, **kwargs)
    
    Example:
        result = await execute_with_retry_async(
            api_client.fetch,
            url='/data',
            max_attempts=5,
            base_delay=2.0
        )
    """
    @retry_async(
        max_attempts=max_attempts,
        base_delay=base_delay,
        max_delay=max_delay,
        exponential_base=exponential_base,
        jitter=jitter,
        exceptions=exceptions,
        on_retry=on_retry
    )
    async def _wrapper() -> Any:
        return await func(*args, **kwargs)
    
    return await _wrapper()
