"""Tests for rate limit retry logic."""

import pytest

from datamammoth._rate_limit import with_retry
from datamammoth.exceptions import RateLimitError


def test_retry_succeeds_on_second_attempt():
    call_count = 0

    def flaky():
        nonlocal call_count
        call_count += 1
        if call_count < 2:
            raise RateLimitError("RATE_LIMITED", "Too fast", 429, retry_after=0)
        return "ok"

    result = with_retry(flaky, max_retries=3, backoff_base=0.01)
    assert result == "ok"
    assert call_count == 2


def test_retry_exhausted():
    def always_fail():
        raise RateLimitError("RATE_LIMITED", "Too fast", 429, retry_after=0)

    with pytest.raises(RateLimitError):
        with_retry(always_fail, max_retries=2, backoff_base=0.01)


def test_no_retry_on_other_errors():
    def bad():
        raise ValueError("not a rate limit")

    with pytest.raises(ValueError):
        with_retry(bad, max_retries=3, backoff_base=0.01)
