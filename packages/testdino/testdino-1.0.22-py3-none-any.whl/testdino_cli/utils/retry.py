"""
Retry utility with exponential backoff and circuit breaker
Handles network failures and temporary service unavailability
"""

import asyncio
from dataclasses import dataclass, field
from typing import Any, Callable, Optional, TypeVar

from testdino_cli.types import NetworkError

T = TypeVar("T")


@dataclass
class RetryOptions:
    """Configuration options for retry behavior"""

    max_attempts: int = 3
    """Maximum number of attempts (default: 3)"""

    base_delay: int = 1000
    """Base delay in milliseconds (default: 1000)"""

    max_delay: int = 30000
    """Maximum delay in milliseconds (default: 30000)"""

    factor: int = 2
    """Backoff factor (default: 2)"""

    timeout: int = 120000
    """Timeout per attempt in milliseconds (default: 120000 = 2 minutes)"""

    should_retry: Optional[Callable[[Exception], bool]] = None
    """Function to determine if error should trigger retry"""


def _default_should_retry(error: Exception) -> bool:
    """Default retry logic"""
    # Check if error is explicitly marked as non-retryable
    if hasattr(error, "retryable") and not error.retryable:  # type: ignore
        return False

    # Don't retry on conflict errors (409) - cache already exists
    if "already exists" in str(error):
        return False

    # Retry on network errors, timeouts, and 5xx server errors
    if isinstance(error, NetworkError):
        return True

    error_msg = str(error).lower()
    if "timeout" in error_msg:
        return True
    if "econnreset" in error_msg:
        return True
    if "enotfound" in error_msg:
        return True
    if "fetch failed" in error_msg:
        return True

    # Check for HTTP status codes that warrant retry
    import re

    if re.search(r"50[0-9]", str(error)):  # 500-509
        return True
    if "429" in str(error):  # Rate limiting
        return True

    return False


async def with_retry(
    operation: Callable[[], T], options: Optional[RetryOptions] = None
) -> T:
    """Execute an operation with retry logic and exponential backoff"""
    if options is None:
        options = RetryOptions()

    should_retry_fn = options.should_retry or _default_should_retry
    last_error: Optional[Exception] = None

    for attempt in range(1, options.max_attempts + 1):
        try:
            # Call the operation and check if it returns a coroutine
            result_or_coro = operation()

            # If it's a coroutine (async function result), await it with timeout
            if asyncio.iscoroutine(result_or_coro):
                result = await asyncio.wait_for(
                    result_or_coro,
                    timeout=options.timeout / 1000.0,  # Convert ms to seconds
                )
            else:
                # For sync functions, run in thread pool with timeout
                result = await asyncio.wait_for(
                    asyncio.to_thread(lambda: result_or_coro),  # type: ignore
                    timeout=options.timeout / 1000.0,
                )
            return result  # type: ignore

        except asyncio.TimeoutError as e:
            last_error = Exception(f"Operation timeout after {options.timeout}ms")
            if not should_retry_fn(last_error):
                raise last_error

        except Exception as error:
            last_error = error

            # Check if we should retry this error
            if not should_retry_fn(last_error):
                raise last_error

            # If this is the last attempt, throw the error
            if attempt == options.max_attempts:
                raise NetworkError(
                    f"Operation failed after {options.max_attempts} attempts: {last_error}",
                    last_error,
                )

            # Calculate delay with exponential backoff
            delay = min(
                options.base_delay * (options.factor ** (attempt - 1)), options.max_delay
            )

            print(
                f"⚠️  Attempt {attempt}/{options.max_attempts} failed: {last_error}"
            )
            print(f"   Retrying in {delay}ms...")

            # Wait before next attempt (convert ms to seconds)
            await asyncio.sleep(delay / 1000.0)

    # This should never be reached, but Python requires it
    if last_error:
        raise last_error
    raise Exception("Unexpected error in retry logic")


async def with_file_upload_retry(
    operation: Callable[[], T], file_name: Optional[str] = None
) -> T:
    """
    Specialized retry for file upload operations
    Uses different retry logic optimized for large file uploads
    """

    def file_upload_should_retry(error: Exception) -> bool:
        """More lenient retry for file uploads"""
        message = str(error).lower()

        # Retry on common file upload failures
        if "network" in message:
            return True
        if "timeout" in message:
            return True
        if "connection" in message:
            return True
        if "upload" in message:
            return True
        if "blob" in message:
            return True
        if "storage" in message:
            return True

        # Don't retry on authentication or permission errors
        if "unauthorized" in message or "403" in message:
            return False
        if "forbidden" in message:
            return False

        return _default_should_retry(error)

    return await with_retry(
        operation,
        RetryOptions(
            max_attempts=3,
            base_delay=2000,  # Longer initial delay for file operations
            max_delay=60000,  # Allow longer delays for large files
            timeout=300000,  # 5 minutes for file uploads
            should_retry=file_upload_should_retry,
        ),
    )
