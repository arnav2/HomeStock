"""Rate limiter for NSE API calls"""

import time
from collections import deque
from threading import Lock


class RateLimiter:
    """Rate limiter to prevent overwhelming NSE servers

    Implements token bucket algorithm
    """

    def __init__(self, max_calls: int = 5, time_window: int = 60):
        """Initialize rate limiter

        Args:
            max_calls: Maximum number of calls allowed
            time_window: Time window in seconds
        """
        self.max_calls = max_calls
        self.time_window = time_window
        self.calls = deque()
        self.lock = Lock()

    def wait_if_needed(self):
        """Wait if rate limit would be exceeded"""
        with self.lock:
            now = time.time()

            # Remove old calls outside the time window
            while self.calls and self.calls[0] < now - self.time_window:
                self.calls.popleft()

            # If we've hit the limit, wait
            if len(self.calls) >= self.max_calls:
                sleep_time = self.time_window - (now - self.calls[0])
                if sleep_time > 0:
                    time.sleep(sleep_time)
                    # Clean up again after sleep
                    now = time.time()
                    while self.calls and self.calls[0] < now - self.time_window:
                        self.calls.popleft()

            # Record this call
            self.calls.append(time.time())

    def can_proceed(self) -> bool:
        """Check if we can make a call without waiting"""
        with self.lock:
            now = time.time()
            # Remove old calls
            while self.calls and self.calls[0] < now - self.time_window:
                self.calls.popleft()
            return len(self.calls) < self.max_calls


# Global rate limiter instance (5 calls per 60 seconds)
nse_rate_limiter = RateLimiter(max_calls=5, time_window=60)
