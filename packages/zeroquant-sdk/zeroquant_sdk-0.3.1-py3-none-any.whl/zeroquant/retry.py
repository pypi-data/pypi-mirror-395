"""
Retry utilities for resilient RPC calls using tenacity.

Provides decorators and context managers for handling transient errors
when interacting with Ethereum nodes and other external services.
"""

import asyncio
from functools import wraps
from typing import Any, Callable, Optional, Set, Type, TypeVar, Union

from tenacity import (
    AsyncRetrying,
    RetryError,
    Retrying,
    retry_if_exception,
    stop_after_attempt,
    wait_exponential,
)

T = TypeVar("T")

# Common RPC error codes that should trigger a retry
RETRYABLE_ERROR_CODES: Set[int] = {
    -32000,  # Server error (rate limit, overloaded)
    -32005,  # Limit exceeded
    429,     # Too many requests (HTTP)
}

# Error message patterns that indicate transient failures
RETRYABLE_ERROR_PATTERNS: tuple[str, ...] = (
    "rate limit",
    "too many requests",
    "request timeout",
    "connection refused",
    "connection reset",
    "timeout",
    "temporarily unavailable",
    "service unavailable",
)


def is_retryable_error(exception: BaseException) -> bool:
    """
    Determine if an exception should trigger a retry.

    Args:
        exception: The exception to check

    Returns:
        True if the error is transient and should be retried
    """
    # Check for error code attribute (common in web3.py exceptions)
    error_code = getattr(exception, "code", None)
    if error_code is not None and error_code in RETRYABLE_ERROR_CODES:
        return True

    # Check error message for known patterns
    error_message = str(exception).lower()
    return any(pattern in error_message for pattern in RETRYABLE_ERROR_PATTERNS)


class RetryConfig:
    """Configuration for retry behavior."""

    def __init__(
        self,
        max_attempts: int = 3,
        min_wait_seconds: float = 1.0,
        max_wait_seconds: float = 10.0,
        exponential_multiplier: float = 2.0,
        on_retry: Optional[Callable[[Exception, int], None]] = None,
    ):
        """
        Initialize retry configuration.

        Args:
            max_attempts: Maximum number of retry attempts (default: 3)
            min_wait_seconds: Minimum wait time between retries (default: 1.0)
            max_wait_seconds: Maximum wait time between retries (default: 10.0)
            exponential_multiplier: Multiplier for exponential backoff (default: 2.0)
            on_retry: Optional callback called on each retry with (error, attempt_number)
        """
        self.max_attempts = max_attempts
        self.min_wait_seconds = min_wait_seconds
        self.max_wait_seconds = max_wait_seconds
        self.exponential_multiplier = exponential_multiplier
        self.on_retry = on_retry


DEFAULT_CONFIG = RetryConfig()


def with_retry(
    config: Optional[RetryConfig] = None,
) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """
    Decorator for adding retry logic to synchronous functions.

    Args:
        config: Optional RetryConfig, uses defaults if not provided

    Returns:
        Decorated function with retry behavior

    Example:
        ```python
        @with_retry(RetryConfig(max_attempts=5))
        def get_balance(address: str) -> int:
            return w3.eth.get_balance(address)
        ```
    """
    cfg = config or DEFAULT_CONFIG

    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            attempt = 0

            def before_retry(retry_state: Any) -> None:
                nonlocal attempt
                attempt += 1
                if cfg.on_retry:
                    cfg.on_retry(retry_state.outcome.exception(), attempt)

            retryer = Retrying(
                stop=stop_after_attempt(cfg.max_attempts),
                wait=wait_exponential(
                    multiplier=cfg.exponential_multiplier,
                    min=cfg.min_wait_seconds,
                    max=cfg.max_wait_seconds,
                ),
                retry=retry_if_exception(is_retryable_error),
                before_sleep=before_retry,
                reraise=True,
            )

            return retryer(func, *args, **kwargs)

        return wrapper

    return decorator


def with_retry_async(
    config: Optional[RetryConfig] = None,
) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """
    Decorator for adding retry logic to async functions.

    Args:
        config: Optional RetryConfig, uses defaults if not provided

    Returns:
        Decorated async function with retry behavior

    Example:
        ```python
        @with_retry_async(RetryConfig(max_attempts=5))
        async def get_balance(address: str) -> int:
            return await w3.eth.get_balance(address)
        ```
    """
    cfg = config or DEFAULT_CONFIG

    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> T:
            attempt = 0

            def before_retry(retry_state: Any) -> None:
                nonlocal attempt
                attempt += 1
                if cfg.on_retry:
                    cfg.on_retry(retry_state.outcome.exception(), attempt)

            async for attempt_result in AsyncRetrying(
                stop=stop_after_attempt(cfg.max_attempts),
                wait=wait_exponential(
                    multiplier=cfg.exponential_multiplier,
                    min=cfg.min_wait_seconds,
                    max=cfg.max_wait_seconds,
                ),
                retry=retry_if_exception(is_retryable_error),
                before_sleep=before_retry,
                reraise=True,
            ):
                with attempt_result:
                    return await func(*args, **kwargs)

            # Should not reach here, but satisfy type checker
            raise RuntimeError("Retry loop exited unexpectedly")

        return wrapper  # type: ignore

    return decorator


async def retry_async(
    func: Callable[..., T],
    *args: Any,
    config: Optional[RetryConfig] = None,
    **kwargs: Any,
) -> T:
    """
    Execute an async function with retry logic.

    Args:
        func: The async function to execute
        *args: Positional arguments to pass to the function
        config: Optional RetryConfig, uses defaults if not provided
        **kwargs: Keyword arguments to pass to the function

    Returns:
        The function result

    Example:
        ```python
        balance = await retry_async(
            w3.eth.get_balance,
            address,
            config=RetryConfig(max_attempts=5)
        )
        ```
    """
    cfg = config or DEFAULT_CONFIG
    attempt_count = 0

    def before_retry(retry_state: Any) -> None:
        nonlocal attempt_count
        attempt_count += 1
        if cfg.on_retry:
            try:
                cfg.on_retry(retry_state.outcome.exception(), attempt_count)
            except Exception:
                pass  # Don't let callback errors suppress the retry

    async for attempt in AsyncRetrying(
        stop=stop_after_attempt(cfg.max_attempts),
        wait=wait_exponential(
            multiplier=cfg.exponential_multiplier,
            min=cfg.min_wait_seconds,
            max=cfg.max_wait_seconds,
        ),
        retry=retry_if_exception(is_retryable_error),
        before_sleep=before_retry,
        reraise=True,
    ):
        with attempt:
            return await func(*args, **kwargs)

    raise RuntimeError("Retry loop exited unexpectedly")


def retry_sync(
    func: Callable[..., T],
    *args: Any,
    config: Optional[RetryConfig] = None,
    **kwargs: Any,
) -> T:
    """
    Execute a synchronous function with retry logic.

    Args:
        func: The function to execute
        *args: Positional arguments to pass to the function
        config: Optional RetryConfig, uses defaults if not provided
        **kwargs: Keyword arguments to pass to the function

    Returns:
        The function result

    Example:
        ```python
        balance = retry_sync(
            w3.eth.get_balance,
            address,
            config=RetryConfig(max_attempts=5)
        )
        ```
    """
    cfg = config or DEFAULT_CONFIG
    attempt_count = 0

    def before_retry(retry_state: Any) -> None:
        nonlocal attempt_count
        attempt_count += 1
        if cfg.on_retry:
            try:
                cfg.on_retry(retry_state.outcome.exception(), attempt_count)
            except Exception:
                pass  # Don't let callback errors suppress the retry

    for attempt in Retrying(
        stop=stop_after_attempt(cfg.max_attempts),
        wait=wait_exponential(
            multiplier=cfg.exponential_multiplier,
            min=cfg.min_wait_seconds,
            max=cfg.max_wait_seconds,
        ),
        retry=retry_if_exception(is_retryable_error),
        before_sleep=before_retry,
        reraise=True,
    ):
        with attempt:
            return func(*args, **kwargs)

    raise RuntimeError("Retry loop exited unexpectedly")


__all__ = [
    "RetryConfig",
    "with_retry",
    "with_retry_async",
    "retry_async",
    "retry_sync",
    "is_retryable_error",
    "RETRYABLE_ERROR_CODES",
    "RETRYABLE_ERROR_PATTERNS",
]
