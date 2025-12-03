"""Tests for rate limiter"""

import time

from app.services.rate_limiter import RateLimiter


def test_rate_limiter_basic():
    """Test basic rate limiter functionality"""
    limiter = RateLimiter(max_calls=2, time_window=1)

    # First call should proceed immediately
    start = time.time()
    limiter.wait_if_needed()
    elapsed = time.time() - start
    assert elapsed < 0.1  # Should be fast

    # Second call should also proceed
    limiter.wait_if_needed()

    # Third call should wait
    start = time.time()
    limiter.wait_if_needed()
    elapsed = time.time() - start
    assert elapsed >= 0.9  # Should wait almost the full window


def test_rate_limiter_can_proceed():
    """Test can_proceed method"""
    limiter = RateLimiter(max_calls=2, time_window=1)

    assert limiter.can_proceed() == True
    limiter.wait_if_needed()
    assert limiter.can_proceed() == True
    limiter.wait_if_needed()
    assert limiter.can_proceed() == False


def test_rate_limiter_resets():
    """Test that rate limiter resets after time window"""
    limiter = RateLimiter(max_calls=1, time_window=1)

    limiter.wait_if_needed()
    assert limiter.can_proceed() == False

    # Wait for window to expire
    time.sleep(1.1)
    assert limiter.can_proceed() == True
