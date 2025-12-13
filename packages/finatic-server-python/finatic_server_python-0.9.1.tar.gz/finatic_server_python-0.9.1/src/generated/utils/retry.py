"""
Retry utility with tenacity package (Phase 2B).

Generated - do not edit directly.
"""

from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
    retry_if_result,
    RetryCallState,
)
from typing import Callable, TypeVar, Optional, List, Any, Awaitable
from ..config import SdkConfig

T = TypeVar('T')


def _should_retry_on_status(error: Exception, retry_on_status: List[int]) -> bool:
    """Check if error status code matches retry list."""
    status_code = getattr(error, 'status_code', None) or getattr(error, 'status', None)
    return status_code in retry_on_status if status_code else False


async def retry_api_call(
    fn: Callable[[], Awaitable[T]],
    config: Optional[SdkConfig] = None,
    max_retries: Optional[int] = None,
    retry_delay: Optional[float] = None,
    retry_max_delay: Optional[float] = None,
    retry_multiplier: Optional[float] = None,
    retry_on_status: Optional[List[int]] = None,
    retry_on_network_error: Optional[bool] = None,
) -> T:
    """Retry an async function with exponential backoff using tenacity.
    
    Args:
        fn: Async function to retry
        config: SDK configuration (optional)
        max_retries: Maximum number of retry attempts
        retry_delay: Initial delay in seconds
        retry_max_delay: Maximum delay in seconds
        retry_multiplier: Exponential backoff multiplier
        retry_on_status: List of HTTP status codes to retry on
        retry_on_network_error: Enable retry on network errors
    
    Returns:
        Result of the function call
    
    Raises:
        Last exception if all retries fail
    """
    # Use config values if provided, otherwise use parameters or defaults
    max_attempts = max_retries or (config.retry_count if config else 3)
    min_wait = retry_delay or (config.retry_delay if config else 1.0)
    max_wait = retry_max_delay or (config.retry_max_delay if config else 10.0)
    multiplier = retry_multiplier or (config.retry_multiplier if config else 2.0)
    status_list = retry_on_status or (config.retry_on_status if config else [429, 500, 502, 503, 504])
    network_retry = retry_on_network_error if retry_on_network_error is not None else (config.retry_on_network_error if config else True)
    
    # Build retry decorator conditionally
    if network_retry:
        @retry(
            stop=stop_after_attempt(max_attempts),
            wait=wait_exponential(multiplier=multiplier, min=min_wait, max=max_wait),
            retry=retry_if_exception_type(Exception),
            reraise=True,
        )
        async def _retry_wrapper() -> T:
            try:
                result = await fn()
                return result
            except Exception as error:
                # Check if we should retry based on status code
                if _should_retry_on_status(error, status_list):
                    raise  # Re-raise to trigger retry
                # Don't retry if status code doesn't match
                raise
    else:
        @retry(
            stop=stop_after_attempt(max_attempts),
            wait=wait_exponential(multiplier=multiplier, min=min_wait, max=max_wait),
            retry=retry_if_result(lambda r: False),  # Never retry on result, only on exceptions
            reraise=True,
        )
        async def _retry_wrapper() -> T:
            try:
                result = await fn()
                return result
            except Exception as error:
                # Check if we should retry based on status code
                if _should_retry_on_status(error, status_list):
                    raise  # Re-raise to trigger retry
                # Don't retry if status code doesn't match
                raise
    
    return await _retry_wrapper()
