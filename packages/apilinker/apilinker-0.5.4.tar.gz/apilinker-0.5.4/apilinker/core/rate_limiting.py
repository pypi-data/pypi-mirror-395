"""
Rate limiting module for APILinker.

This module provides various rate limiting strategies to control the flow of requests
to external APIs, preventing bans and ensuring fair usage.
"""

import logging
import time
import threading
from abc import ABC, abstractmethod
from enum import Enum
from typing import Dict, Optional, Any

logger = logging.getLogger(__name__)


class RateLimitStrategy(Enum):
    """Available rate limiting strategies."""

    TOKEN_BUCKET = "TOKEN_BUCKET"
    LEAKY_BUCKET = "LEAKY_BUCKET"
    ADAPTIVE = "ADAPTIVE"
    NONE = "NONE"


class RateLimiter(ABC):
    """Abstract base class for rate limiters."""

    @abstractmethod
    def acquire(self, tokens: int = 1) -> float:
        """
        Acquire tokens from the limiter.

        Args:
            tokens: Number of tokens to acquire.

        Returns:
            Number of seconds to wait before proceeding.
        """
        pass

    @abstractmethod
    def update_from_headers(self, headers: Dict[str, str]) -> None:
        """
        Update limiter state based on response headers.

        Args:
            headers: Response headers.
        """
        pass


class TokenBucketRateLimiter(RateLimiter):
    """
    Token Bucket algorithm implementation.

    Tokens are added to the bucket at a fixed rate. Requests consume tokens.
    If the bucket is empty, requests must wait.
    """

    def __init__(self, rate: float, burst: int = 1):
        """
        Initialize TokenBucketRateLimiter.

        Args:
            rate: Tokens per second.
            burst: Maximum number of tokens in the bucket.
        """
        self.rate = rate
        self.capacity = burst
        self.tokens = float(burst)
        self.last_update = time.time()
        self.lock = threading.RLock()

    def acquire(self, tokens: int = 1) -> float:
        with self.lock:
            now = time.time()

            # Refill tokens based on time passed
            elapsed = now - self.last_update
            self.tokens = min(self.capacity, self.tokens + elapsed * self.rate)
            self.last_update = now

            if self.tokens >= tokens:
                self.tokens -= tokens
                return 0.0
            else:
                # Calculate wait time
                deficit = tokens - self.tokens
                wait_time = deficit / self.rate
                # We don't consume tokens here if we have to wait,
                # effectively we are reserving them or just telling the caller to wait.
                # A strict implementation might block here, but we return wait time
                # to allow async handling or sleep by caller.
                # For simplicity in this sync context, we'll consume the future tokens
                # by updating last_update to the future.
                self.last_update += wait_time
                self.tokens = 0
                return wait_time

    def update_from_headers(self, headers: Dict[str, str]) -> None:
        # Token bucket is usually static, but could be adjusted if needed.
        pass


class LeakyBucketRateLimiter(RateLimiter):
    """
    Leaky Bucket algorithm implementation.

    Requests enter a queue (bucket) and are processed at a constant rate.
    This smooths out bursts.
    """

    def __init__(self, rate: float):
        """
        Initialize LeakyBucketRateLimiter.

        Args:
            rate: Requests per second allowed.
        """
        self.rate = rate
        self.interval = 1.0 / rate
        self.last_request_time = 0.0
        self.lock = threading.RLock()

    def acquire(self, tokens: int = 1) -> float:
        # Note: Leaky bucket usually processes 1 item at a time at fixed rate.
        # 'tokens' > 1 implies a batch which takes more time.
        with self.lock:
            now = time.time()

            # Calculate when we can next process a request
            next_allowed_time = max(
                now, self.last_request_time + (self.interval * tokens)
            )

            wait_time = max(0.0, next_allowed_time - now)

            self.last_request_time = next_allowed_time

            return wait_time

    def update_from_headers(self, headers: Dict[str, str]) -> None:
        pass


class AdaptiveRateLimiter(RateLimiter):
    """
    Adaptive rate limiter that adjusts based on server headers.

    Parses X-RateLimit-* and Retry-After headers to dynamically adjust
    wait times.
    """

    def __init__(self, default_rate: float = 10.0):
        self.rate_limiter = TokenBucketRateLimiter(
            rate=default_rate, burst=int(default_rate)
        )
        self.lock = threading.RLock()
        self.blocked_until = 0.0

    def acquire(self, tokens: int = 1) -> float:
        with self.lock:
            now = time.time()

            # Check if we are globally blocked (e.g. from a 429 Retry-After)
            if now < self.blocked_until:
                return self.blocked_until - now

            # Otherwise delegate to the internal token bucket
            return self.rate_limiter.acquire(tokens)

    def update_from_headers(self, headers: Dict[str, str]) -> None:
        with self.lock:
            # Handle standard RateLimit headers
            # X-RateLimit-Remaining: The number of requests left for the time window.
            # X-RateLimit-Reset: The timestamp at which the current rate limit window resets.

            remaining = headers.get("X-RateLimit-Remaining") or headers.get(
                "x-ratelimit-remaining"
            )
            reset = headers.get("X-RateLimit-Reset") or headers.get("x-ratelimit-reset")

            if remaining is not None and reset is not None:
                try:
                    rem = int(remaining)
                    res = float(reset)
                    now = time.time()

                    # If we are running low on tokens, slow down
                    if rem < 5 and res > now:
                        # Adjust internal rate to spread remaining requests over remaining time
                        # This is a simple heuristic
                        new_rate = rem / (res - now)
                        # Don't go too slow, but ensure we don't hit 0
                        new_rate = max(0.1, new_rate)

                        # Update the internal limiter's rate
                        if isinstance(self.rate_limiter, TokenBucketRateLimiter):
                            self.rate_limiter.rate = new_rate
                            logger.debug(
                                f"AdaptiveRateLimiter: Adjusted rate to {new_rate:.2f} req/s based on headers"
                            )

                except (ValueError, TypeError):
                    pass

    def handle_429(self, retry_after: Optional[str] = None) -> None:
        """
        Handle a 429 Too Many Requests response.

        Args:
            retry_after: Value of Retry-After header (seconds or timestamp).
        """
        with self.lock:
            wait_time = 5.0  # Default backoff

            if retry_after:
                try:
                    # Try parsing as integer seconds
                    wait_time = float(retry_after)
                except ValueError:
                    # Try parsing as HTTP date
                    try:
                        # TODO: Implement proper HTTP date parsing if needed
                        # For now, fallback to default if not simple integer
                        pass
                    except Exception:
                        pass

            self.blocked_until = time.time() + wait_time
            logger.warning(
                f"AdaptiveRateLimiter: Blocking requests for {wait_time:.2f}s due to 429"
            )


class RateLimitManager:
    """Manages rate limiters for different endpoints."""

    def __init__(self):
        self.limiters: Dict[str, RateLimiter] = {}
        self.lock = threading.RLock()

    def get_limiter(self, endpoint_name: str) -> Optional[RateLimiter]:
        with self.lock:
            return self.limiters.get(endpoint_name)

    def create_limiter(self, endpoint_name: str, config: Dict[str, Any]) -> RateLimiter:
        """
        Create and register a rate limiter for an endpoint.

        Args:
            endpoint_name: Name of the endpoint.
            config: Rate limit configuration dictionary.
                    Expected keys: 'strategy', 'rate', 'burst'.
        """
        strategy_str = config.get("strategy", "TOKEN_BUCKET").upper()
        try:
            strategy = RateLimitStrategy(strategy_str)
        except ValueError:
            strategy = RateLimitStrategy.TOKEN_BUCKET
            logger.warning(
                f"Unknown rate limit strategy '{strategy_str}', defaulting to TOKEN_BUCKET"
            )

        rate = float(config.get("rate", 10.0))

        limiter: RateLimiter
        if strategy == RateLimitStrategy.TOKEN_BUCKET:
            burst = int(config.get("burst", max(1, int(rate))))
            limiter = TokenBucketRateLimiter(rate, burst)
        elif strategy == RateLimitStrategy.LEAKY_BUCKET:
            limiter = LeakyBucketRateLimiter(rate)
        elif strategy == RateLimitStrategy.ADAPTIVE:
            limiter = AdaptiveRateLimiter(default_rate=rate)
        else:
            # Fallback or NONE
            limiter = TokenBucketRateLimiter(
                rate=1000.0, burst=1000
            )  # Effectively unlimited

        with self.lock:
            self.limiters[endpoint_name] = limiter

        return limiter

    def acquire(self, endpoint_name: str, tokens: int = 1) -> None:
        """
        Acquire tokens for an endpoint, blocking if necessary.
        """
        limiter = self.get_limiter(endpoint_name)
        if limiter:
            wait_time = limiter.acquire(tokens)
            if wait_time > 0:
                logger.debug(
                    f"Rate limit: Waiting {wait_time:.3f}s for endpoint '{endpoint_name}'"
                )
                time.sleep(wait_time)

    def update_from_response(self, endpoint_name: str, response: Any) -> None:
        """
        Update limiter based on response headers and status.
        """
        limiter = self.get_limiter(endpoint_name)
        if not limiter:
            return

        # Extract headers if available
        headers = getattr(response, "headers", {})
        if headers:
            limiter.update_from_headers(dict(headers))

        # Handle 429 specifically for AdaptiveRateLimiter
        if isinstance(limiter, AdaptiveRateLimiter):
            status_code = getattr(response, "status_code", 0)
            if status_code == 429:
                retry_after = headers.get("Retry-After") or headers.get("retry-after")
                limiter.handle_429(retry_after)
