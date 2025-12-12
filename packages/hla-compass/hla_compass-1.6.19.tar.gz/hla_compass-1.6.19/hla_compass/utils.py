"""Utility functions for HLA-Compass SDK"""

import json
import time
import logging
from typing import Any
from collections import deque
from threading import Lock

logger = logging.getLogger(__name__)


def parse_api_error(response: Any, default_message: str) -> str:
    """
    Parse error message from API response.

    Args:
        response: HTTP response object
        default_message: Default message if parsing fails

    Returns:
        Sanitized error message
    """
    try:
        if hasattr(response, 'json') and response.text:
            error_data = response.json()
            # Look for standard error structure
            if isinstance(error_data, dict):
                # Try different error message locations
                error_msg = (
                    error_data.get("error", {}).get("message") or
                    error_data.get("message") or
                    error_data.get("detail")
                )
                if error_msg:
                    # Sanitize error message to prevent info disclosure
                    if len(error_msg) > 500:
                        error_msg = error_msg[:500] + "..."
                    return error_msg
    except (json.JSONDecodeError, ValueError, AttributeError):
        pass

    # Return a generic message with status code if available
    if hasattr(response, 'status_code'):
        return f"{default_message} (status: {response.status_code})"
    return default_message


class RateLimiter:
    """Simple rate limiter using a token bucket algorithm"""

    def __init__(self, max_requests: int = 100, time_window: int = 60):
        """
        Initialize rate limiter.

        Args:
            max_requests: Maximum number of requests allowed
            time_window: Time window in seconds
        """
        self.max_requests = max_requests
        self.time_window = time_window
        self.requests = deque()
        self.lock = Lock()
        self.last_wait: float = 0.0

    def acquire(self, wait: bool = True) -> bool:
        """
        Acquire permission to make a request.

        Args:
            wait: If True, wait until the request can be made

        Returns:
            True if the request can proceed, False otherwise
        """
        while True:
            with self.lock:
                now = time.time()

                # Remove old requests outside the time window
                while self.requests and self.requests[0] <= now - self.time_window:
                    self.requests.popleft()

                # Check if we can make a request
                if len(self.requests) < self.max_requests:
                    self.requests.append(now)
                    self.last_wait = 0.0
                    return True

                if not wait:
                    return False

                # Calculate remaining sleep time outside the critical section
                sleep_time = self.time_window - (now - self.requests[0]) + 0.1
                self.last_wait = max(sleep_time, 0.0)

            # Allow other threads to acquire while we sleep
            if sleep_time > 0:
                time.sleep(sleep_time)
            else:
                # If the queue is stale, loop again without sleeping
                time.sleep(0)
