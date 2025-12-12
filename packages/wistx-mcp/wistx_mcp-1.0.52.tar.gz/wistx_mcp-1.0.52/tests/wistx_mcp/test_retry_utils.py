"""Unit tests for retry utilities."""

import asyncio
import pytest

from wistx_mcp.tools.lib.retry_utils import (
    with_timeout,
    with_retry,
    with_timeout_and_retry,
)


@pytest.mark.asyncio
async def test_with_timeout_success():
    """Test timeout wrapper with successful operation."""
    async def quick_operation():
        await asyncio.sleep(0.1)
        return "success"

    result = await with_timeout(quick_operation, timeout_seconds=1.0)

    assert result == "success"


@pytest.mark.asyncio
async def test_with_timeout_failure():
    """Test timeout wrapper with timeout."""
    async def slow_operation():
        await asyncio.sleep(2.0)
        return "success"

    with pytest.raises(RuntimeError, match="Operation timed out"):
        await with_timeout(slow_operation, timeout_seconds=0.5)


@pytest.mark.asyncio
async def test_with_retry_success_first_attempt():
    """Test retry wrapper with success on first attempt."""
    call_count = 0

    async def operation():
        nonlocal call_count
        call_count += 1
        return "success"

    result = await with_retry(operation, max_attempts=3)

    assert result == "success"
    assert call_count == 1


@pytest.mark.asyncio
async def test_with_retry_success_after_retries():
    """Test retry wrapper with success after retries."""
    call_count = 0

    async def operation():
        nonlocal call_count
        call_count += 1
        if call_count < 3:
            raise ConnectionError("Temporary failure")
        return "success"

    result = await with_retry(
        operation,
        max_attempts=3,
        retryable_exceptions=(ConnectionError,),
    )

    assert result == "success"
    assert call_count == 3


@pytest.mark.asyncio
async def test_with_retry_failure_after_all_attempts():
    """Test retry wrapper with failure after all attempts."""
    async def operation():
        raise ConnectionError("Persistent failure")

    with pytest.raises(RuntimeError, match="Operation failed after"):
        await with_retry(
            operation,
            max_attempts=3,
            retryable_exceptions=(ConnectionError,),
        )


@pytest.mark.asyncio
async def test_with_retry_exponential_backoff():
    """Test retry wrapper with exponential backoff."""
    call_times = []

    async def operation():
        call_times.append(asyncio.get_event_loop().time())
        raise ConnectionError("Failure")

    start_time = asyncio.get_event_loop().time()

    with pytest.raises(RuntimeError):
        await with_retry(
            operation,
            max_attempts=3,
            initial_delay=0.1,
            retryable_exceptions=(ConnectionError,),
        )

    assert len(call_times) == 3

    delay1 = call_times[1] - call_times[0]
    delay2 = call_times[2] - call_times[1]

    assert delay1 >= 0.1
    assert delay2 >= delay1


@pytest.mark.asyncio
async def test_with_timeout_and_retry_success():
    """Test combined timeout and retry with success."""
    call_count = 0

    async def operation():
        nonlocal call_count
        call_count += 1
        if call_count < 2:
            raise ConnectionError("Temporary failure")
        await asyncio.sleep(0.1)
        return "success"

    result = await with_timeout_and_retry(
        operation,
        timeout_seconds=1.0,
        max_attempts=3,
        retryable_exceptions=(ConnectionError,),
    )

    assert result == "success"
    assert call_count == 2


@pytest.mark.asyncio
async def test_with_timeout_and_retry_timeout():
    """Test combined timeout and retry with timeout."""
    async def slow_operation():
        await asyncio.sleep(2.0)
        return "success"

    with pytest.raises(RuntimeError, match="Operation timed out"):
        await with_timeout_and_retry(
            slow_operation,
            timeout_seconds=0.5,
            max_attempts=3,
        )


@pytest.mark.asyncio
async def test_with_retry_non_retryable_exception():
    """Test retry wrapper with non-retryable exception."""
    async def operation():
        raise ValueError("Non-retryable error")

    with pytest.raises(ValueError, match="Non-retryable error"):
        await with_retry(
            operation,
            max_attempts=3,
            retryable_exceptions=(ConnectionError,),
        )

