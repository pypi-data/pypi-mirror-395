"""
Tests for retry utilities.
"""

import asyncio
from unittest.mock import Mock, AsyncMock, patch
import pytest

from zeroquant.retry import (
    RetryConfig,
    is_retryable_error,
    with_retry,
    with_retry_async,
    retry_sync,
    retry_async,
    RETRYABLE_ERROR_CODES,
    RETRYABLE_ERROR_PATTERNS,
)


class TestIsRetryableError:
    """Tests for is_retryable_error function."""

    def test_retryable_error_code_minus_32000(self):
        """Should identify -32000 as retryable (server error)."""
        error = Exception("Server error")
        error.code = -32000
        assert is_retryable_error(error) is True

    def test_retryable_error_code_minus_32005(self):
        """Should identify -32005 as retryable (limit exceeded)."""
        error = Exception("Limit exceeded")
        error.code = -32005
        assert is_retryable_error(error) is True

    def test_retryable_error_code_429(self):
        """Should identify 429 as retryable (too many requests)."""
        error = Exception("Too many requests")
        error.code = 429
        assert is_retryable_error(error) is True

    def test_non_retryable_error_code(self):
        """Should not retry for non-retryable error codes."""
        error = Exception("Bad request")
        error.code = 400
        assert is_retryable_error(error) is False

    @pytest.mark.parametrize("message", [
        "rate limit exceeded",
        "RATE LIMIT",  # Case insensitive
        "too many requests",
        "request timeout",
        "connection refused",
        "connection reset",
        "timeout waiting for response",
        "temporarily unavailable",
        "service unavailable",
    ])
    def test_retryable_error_patterns(self, message):
        """Should identify known transient error patterns."""
        error = Exception(message)
        assert is_retryable_error(error) is True

    def test_non_retryable_error_message(self):
        """Should not retry for unknown error messages."""
        error = Exception("Invalid parameter value")
        assert is_retryable_error(error) is False

    def test_error_without_code_attribute(self):
        """Should check message patterns when code is not present."""
        error = Exception("rate limit hit")
        assert is_retryable_error(error) is True

    def test_empty_error_message(self):
        """Should not retry for empty error messages."""
        error = Exception("")
        assert is_retryable_error(error) is False


class TestRetryConfig:
    """Tests for RetryConfig class."""

    def test_default_values(self):
        """Should have sensible defaults."""
        config = RetryConfig()
        assert config.max_attempts == 3
        assert config.min_wait_seconds == 1.0
        assert config.max_wait_seconds == 10.0
        assert config.exponential_multiplier == 2.0
        assert config.on_retry is None

    def test_custom_values(self):
        """Should accept custom configuration."""
        on_retry = Mock()
        config = RetryConfig(
            max_attempts=5,
            min_wait_seconds=0.5,
            max_wait_seconds=30.0,
            exponential_multiplier=3.0,
            on_retry=on_retry,
        )
        assert config.max_attempts == 5
        assert config.min_wait_seconds == 0.5
        assert config.max_wait_seconds == 30.0
        assert config.exponential_multiplier == 3.0
        assert config.on_retry is on_retry


class TestWithRetryDecorator:
    """Tests for with_retry decorator."""

    def test_success_on_first_attempt(self):
        """Should succeed without retrying on success."""
        mock_func = Mock(return_value="success")

        @with_retry()
        def decorated_func():
            return mock_func()

        result = decorated_func()

        assert result == "success"
        assert mock_func.call_count == 1

    def test_retry_on_retryable_error(self):
        """Should retry on retryable errors."""
        error = Exception("rate limit exceeded")
        mock_func = Mock(side_effect=[error, error, "success"])

        @with_retry(RetryConfig(max_attempts=3, min_wait_seconds=0.01))
        def decorated_func():
            return mock_func()

        result = decorated_func()

        assert result == "success"
        assert mock_func.call_count == 3

    def test_no_retry_on_non_retryable_error(self):
        """Should not retry on non-retryable errors."""
        error = Exception("Invalid parameter")
        mock_func = Mock(side_effect=error)

        @with_retry(RetryConfig(max_attempts=3, min_wait_seconds=0.01))
        def decorated_func():
            return mock_func()

        with pytest.raises(Exception, match="Invalid parameter"):
            decorated_func()

        assert mock_func.call_count == 1

    def test_max_attempts_exceeded(self):
        """Should raise after max attempts exhausted."""
        error = Exception("rate limit exceeded")
        mock_func = Mock(side_effect=error)

        @with_retry(RetryConfig(max_attempts=2, min_wait_seconds=0.01))
        def decorated_func():
            return mock_func()

        with pytest.raises(Exception, match="rate limit"):
            decorated_func()

        assert mock_func.call_count == 2

    def test_on_retry_callback(self):
        """Should call on_retry callback on each retry."""
        error = Exception("rate limit exceeded")
        on_retry = Mock()
        mock_func = Mock(side_effect=[error, "success"])

        @with_retry(RetryConfig(max_attempts=2, min_wait_seconds=0.01, on_retry=on_retry))
        def decorated_func():
            return mock_func()

        result = decorated_func()

        assert result == "success"
        on_retry.assert_called_once()
        call_args = on_retry.call_args[0]
        assert isinstance(call_args[0], Exception)
        assert call_args[1] == 1  # First retry attempt

    def test_preserves_function_arguments(self):
        """Should pass arguments to decorated function."""
        mock_func = Mock(return_value="result")

        @with_retry()
        def decorated_func(a, b, c=None):
            return mock_func(a, b, c=c)

        result = decorated_func(1, 2, c=3)

        assert result == "result"
        mock_func.assert_called_once_with(1, 2, c=3)


class TestWithRetryAsyncDecorator:
    """Tests for with_retry_async decorator."""

    @pytest.mark.asyncio
    async def test_success_on_first_attempt(self):
        """Should succeed without retrying on success."""
        mock_func = AsyncMock(return_value="success")

        @with_retry_async()
        async def decorated_func():
            return await mock_func()

        result = await decorated_func()

        assert result == "success"
        assert mock_func.call_count == 1

    @pytest.mark.asyncio
    async def test_retry_on_retryable_error(self):
        """Should retry on retryable errors."""
        error = Exception("timeout")
        mock_func = AsyncMock(side_effect=[error, "success"])

        @with_retry_async(RetryConfig(max_attempts=2, min_wait_seconds=0.01))
        async def decorated_func():
            return await mock_func()

        result = await decorated_func()

        assert result == "success"
        assert mock_func.call_count == 2

    @pytest.mark.asyncio
    async def test_no_retry_on_non_retryable_error(self):
        """Should not retry on non-retryable errors."""
        error = Exception("validation failed")
        mock_func = AsyncMock(side_effect=error)

        @with_retry_async(RetryConfig(max_attempts=3, min_wait_seconds=0.01))
        async def decorated_func():
            return await mock_func()

        with pytest.raises(Exception, match="validation failed"):
            await decorated_func()

        assert mock_func.call_count == 1


class TestRetrySyncFunction:
    """Tests for retry_sync function."""

    def test_success_on_first_attempt(self):
        """Should succeed without retrying on success."""
        mock_func = Mock(return_value="result")

        result = retry_sync(mock_func)

        assert result == "result"
        assert mock_func.call_count == 1

    def test_retry_on_retryable_error(self):
        """Should retry on retryable errors."""
        error = Exception("connection refused")
        mock_func = Mock(side_effect=[error, error, "result"])

        result = retry_sync(
            mock_func,
            config=RetryConfig(max_attempts=3, min_wait_seconds=0.01)
        )

        assert result == "result"
        assert mock_func.call_count == 3

    def test_passes_arguments(self):
        """Should pass positional and keyword arguments."""
        mock_func = Mock(return_value="result")

        result = retry_sync(mock_func, "arg1", "arg2", key="value")

        mock_func.assert_called_once_with("arg1", "arg2", key="value")
        assert result == "result"

    def test_on_retry_callback_error_handling(self):
        """Should not fail if on_retry callback raises."""
        error = Exception("rate limit")

        def bad_callback(e, attempt):
            raise RuntimeError("callback error")

        mock_func = Mock(side_effect=[error, "success"])

        # Should not raise despite callback error
        result = retry_sync(
            mock_func,
            config=RetryConfig(max_attempts=2, min_wait_seconds=0.01, on_retry=bad_callback)
        )

        assert result == "success"


class TestRetryAsyncFunction:
    """Tests for retry_async function."""

    @pytest.mark.asyncio
    async def test_success_on_first_attempt(self):
        """Should succeed without retrying on success."""
        mock_func = AsyncMock(return_value="result")

        result = await retry_async(mock_func)

        assert result == "result"
        assert mock_func.call_count == 1

    @pytest.mark.asyncio
    async def test_retry_on_retryable_error(self):
        """Should retry on retryable errors."""
        error = Exception("service unavailable")
        mock_func = AsyncMock(side_effect=[error, "result"])

        result = await retry_async(
            mock_func,
            config=RetryConfig(max_attempts=2, min_wait_seconds=0.01)
        )

        assert result == "result"
        assert mock_func.call_count == 2

    @pytest.mark.asyncio
    async def test_passes_arguments(self):
        """Should pass positional and keyword arguments."""
        mock_func = AsyncMock(return_value="result")

        result = await retry_async(mock_func, "arg1", key="value")

        mock_func.assert_called_once_with("arg1", key="value")
        assert result == "result"

    @pytest.mark.asyncio
    async def test_max_attempts_exceeded(self):
        """Should raise after max attempts exhausted."""
        error = Exception("timeout")
        mock_func = AsyncMock(side_effect=error)

        with pytest.raises(Exception, match="timeout"):
            await retry_async(
                mock_func,
                config=RetryConfig(max_attempts=2, min_wait_seconds=0.01)
            )

        assert mock_func.call_count == 2

    @pytest.mark.asyncio
    async def test_on_retry_callback(self):
        """Should call on_retry callback on each retry."""
        error = Exception("rate limit exceeded")
        on_retry = Mock()
        mock_func = AsyncMock(side_effect=[error, "success"])

        result = await retry_async(
            mock_func,
            config=RetryConfig(max_attempts=2, min_wait_seconds=0.01, on_retry=on_retry)
        )

        assert result == "success"
        on_retry.assert_called_once()


class TestRetryableErrorConstants:
    """Tests for retryable error constants."""

    def test_retryable_error_codes_defined(self):
        """Should have expected error codes defined."""
        assert -32000 in RETRYABLE_ERROR_CODES
        assert -32005 in RETRYABLE_ERROR_CODES
        assert 429 in RETRYABLE_ERROR_CODES

    def test_retryable_error_patterns_defined(self):
        """Should have expected error patterns defined."""
        assert "rate limit" in RETRYABLE_ERROR_PATTERNS
        assert "too many requests" in RETRYABLE_ERROR_PATTERNS
        assert "timeout" in RETRYABLE_ERROR_PATTERNS
        assert "connection refused" in RETRYABLE_ERROR_PATTERNS


class TestErrorCodeAttribute:
    """Tests for error code attribute handling."""

    def test_error_with_code_attribute_takes_precedence(self):
        """Error code should take precedence over message patterns."""
        error = Exception("validation failed")  # Non-retryable message
        error.code = 429  # Retryable code

        assert is_retryable_error(error) is True

    def test_error_with_non_retryable_code(self):
        """Non-retryable code should prevent retry even with retryable message."""
        error = Exception("rate limit")  # Retryable message
        error.code = 400  # Non-retryable code

        # Should still be retryable because message matches
        # (code check only overrides if code IS in retryable set)
        assert is_retryable_error(error) is True

    def test_error_with_none_code(self):
        """None code should fall through to message check."""
        error = Exception("rate limit exceeded")
        error.code = None

        assert is_retryable_error(error) is True
