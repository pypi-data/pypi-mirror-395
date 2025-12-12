"""
Rate Limiting Engine

Advanced rate limiting with multiple algorithms and distributed support.
"""

import asyncio
import time
from collections import defaultdict, deque
from typing import Dict, Any, List, Optional, Tuple
import redis
import json

from pydiscobasepro.core.logging import get_logger

logger = get_logger(__name__)

class RateLimiter:
    """Advanced rate limiting engine with multiple algorithms."""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.enabled = config.get("enabled", True)

        # Rate limit rules
        self.rules: Dict[str, Dict[str, Any]] = {}
        self._load_default_rules()

        # Tracking data
        self.request_counts: Dict[str, deque] = defaultdict(lambda: deque(maxlen=1000))
        self.burst_counts: Dict[str, int] = defaultdict(int)
        self.last_request_times: Dict[str, float] = {}

        # Redis support for distributed rate limiting
        self.redis_client = None
        redis_url = config.get("redis_url")
        if redis_url:
            try:
                self.redis_client = redis.from_url(redis_url)
                logger.info("Redis enabled for distributed rate limiting")
            except Exception as e:
                logger.error(f"Redis connection failed: {e}")

    def _load_default_rules(self):
        """Load default rate limiting rules."""
        self.rules = {
            "api_requests": {
                "algorithm": "sliding_window",
                "max_requests": 100,
                "window_seconds": 60,
                "burst_limit": 20
            },
            "authentication": {
                "algorithm": "fixed_window",
                "max_requests": 5,
                "window_seconds": 300,
                "burst_limit": 2
            },
            "file_uploads": {
                "algorithm": "token_bucket",
                "capacity": 10,
                "refill_rate": 1,  # tokens per second
                "burst_limit": 5
            }
        }

    def add_rule(
        self,
        rule_name: str,
        algorithm: str,
        max_requests: int = 100,
        window_seconds: int = 60,
        burst_limit: Optional[int] = None,
        capacity: Optional[int] = None,
        refill_rate: Optional[float] = None
    ):
        """Add a custom rate limiting rule."""
        rule = {
            "algorithm": algorithm,
            "max_requests": max_requests,
            "window_seconds": window_seconds,
            "burst_limit": burst_limit,
            "capacity": capacity,
            "refill_rate": refill_rate
        }
        self.rules[rule_name] = rule
        logger.info(f"Rate limit rule added: {rule_name}")

    def remove_rule(self, rule_name: str):
        """Remove a rate limiting rule."""
        if rule_name in self.rules:
            del self.rules[rule_name]
            logger.info(f"Rate limit rule removed: {rule_name}")

    async def check_limit(self, identifier: str, rule_name: str = "api_requests") -> Tuple[bool, Optional[float]]:
        """Check if request is within rate limits."""
        if not self.enabled:
            return True, None

        if rule_name not in self.rules:
            logger.warning(f"Rate limit rule not found: {rule_name}")
            return True, None

        rule = self.rules[rule_name]

        if self.redis_client:
            return await self._check_limit_redis(identifier, rule_name, rule)
        else:
            return self._check_limit_local(identifier, rule)

    def _check_limit_local(self, identifier: str, rule: Dict[str, Any]) -> Tuple[bool, Optional[float]]:
        """Check rate limit using local storage."""
        algorithm = rule["algorithm"]
        current_time = time.time()

        if algorithm == "sliding_window":
            return self._check_sliding_window(identifier, rule, current_time)
        elif algorithm == "fixed_window":
            return self._check_fixed_window(identifier, rule, current_time)
        elif algorithm == "token_bucket":
            return self._check_token_bucket(identifier, rule, current_time)
        else:
            logger.error(f"Unknown rate limiting algorithm: {algorithm}")
            return True, None

    def _check_sliding_window(self, identifier: str, rule: Dict[str, Any], current_time: float) -> Tuple[bool, Optional[float]]:
        """Check sliding window rate limit."""
        window_seconds = rule["window_seconds"]
        max_requests = rule["max_requests"]

        requests = self.request_counts[identifier]

        # Remove old requests outside the window
        while requests and current_time - requests[0] > window_seconds:
            requests.popleft()

        # Add current request
        requests.append(current_time)

        # Check limit
        if len(requests) > max_requests:
            # Calculate wait time until oldest request expires
            oldest_request = requests[0]
            wait_time = window_seconds - (current_time - oldest_request)
            return False, wait_time

        return True, None

    def _check_fixed_window(self, identifier: str, rule: Dict[str, Any], current_time: float) -> Tuple[bool, Optional[float]]:
        """Check fixed window rate limit."""
        window_seconds = rule["window_seconds"]
        max_requests = rule["max_requests"]

        window_key = f"{identifier}:{int(current_time / window_seconds)}"
        count = self.burst_counts.get(window_key, 0)

        if count >= max_requests:
            # Calculate wait time until next window
            next_window = (int(current_time / window_seconds) + 1) * window_seconds
            wait_time = next_window - current_time
            return False, wait_time

        self.burst_counts[window_key] = count + 1
        return True, None

    def _check_token_bucket(self, identifier: str, rule: Dict[str, Any], current_time: float) -> Tuple[bool, Optional[float]]:
        """Check token bucket rate limit."""
        capacity = rule["capacity"]
        refill_rate = rule["refill_rate"]

        # Get current tokens
        last_time = self.last_request_times.get(identifier, current_time)
        time_passed = current_time - last_time

        current_tokens = getattr(self, f'_tokens_{identifier}', capacity)
        current_tokens = min(capacity, current_tokens + (time_passed * refill_rate))

        if current_tokens < 1:
            # Calculate wait time for next token
            wait_time = (1 - current_tokens) / refill_rate
            return False, wait_time

        # Consume token
        current_tokens -= 1
        setattr(self, f'_tokens_{identifier}', current_tokens)
        self.last_request_times[identifier] = current_time

        return True, None

    async def _check_limit_redis(self, identifier: str, rule_name: str, rule: Dict[str, Any]) -> Tuple[bool, Optional[float]]:
        """Check rate limit using Redis for distributed limiting."""
        try:
            current_time = time.time()
            algorithm = rule["algorithm"]

            if algorithm == "sliding_window":
                return await self._check_sliding_window_redis(identifier, rule_name, rule, current_time)
            elif algorithm == "fixed_window":
                return await self._check_fixed_window_redis(identifier, rule_name, rule, current_time)
            elif algorithm == "token_bucket":
                return await self._check_token_bucket_redis(identifier, rule_name, rule, current_time)
            else:
                logger.error(f"Unknown rate limiting algorithm: {algorithm}")
                return True, None

        except Exception as e:
            logger.error(f"Redis rate limit check error: {e}")
            # Fallback to local checking
            return self._check_limit_local(identifier, rule)

    async def _check_sliding_window_redis(self, identifier: str, rule_name: str, rule: Dict[str, Any], current_time: float) -> Tuple[bool, Optional[float]]:
        """Redis-based sliding window rate limiting."""
        window_seconds = rule["window_seconds"]
        max_requests = rule["max_requests"]

        key = f"ratelimit:{rule_name}:{identifier}"

        # Add current request with score as timestamp
        self.redis_client.zadd(key, {str(current_time): current_time})

        # Remove old requests
        self.redis_client.zremrangebyscore(key, 0, current_time - window_seconds)

        # Count requests in window
        count = self.redis_client.zcard(key)

        if count > max_requests:
            # Get oldest request to calculate wait time
            oldest = self.redis_client.zrange(key, 0, 0, withscores=True)
            if oldest:
                oldest_time = oldest[0][1]
                wait_time = window_seconds - (current_time - oldest_time)
                return False, wait_time

        # Set expiry on the key
        self.redis_client.expire(key, window_seconds)
        return True, None

    async def _check_fixed_window_redis(self, identifier: str, rule_name: str, rule: Dict[str, Any], current_time: float) -> Tuple[bool, Optional[float]]:
        """Redis-based fixed window rate limiting."""
        window_seconds = rule["window_seconds"]
        max_requests = rule["max_requests"]

        window_key = f"{int(current_time / window_seconds)}"
        key = f"ratelimit:{rule_name}:{identifier}:{window_key}"

        # Increment counter
        count = self.redis_client.incr(key)

        # Set expiry if first request in window
        if count == 1:
            self.redis_client.expire(key, window_seconds)

        if count > max_requests:
            # Calculate wait time until next window
            next_window = (int(current_time / window_seconds) + 1) * window_seconds
            wait_time = next_window - current_time
            return False, wait_time

        return True, None

    async def _check_token_bucket_redis(self, identifier: str, rule_name: str, rule: Dict[str, Any], current_time: float) -> Tuple[bool, Optional[float]]:
        """Redis-based token bucket rate limiting."""
        capacity = rule["capacity"]
        refill_rate = rule["refill_rate"]

        tokens_key = f"ratelimit:{rule_name}:{identifier}:tokens"
        last_time_key = f"ratelimit:{rule_name}:{identifier}:last_time"

        # Get current tokens and last time
        tokens = self.redis_client.get(tokens_key)
        last_time = self.redis_client.get(last_time_key)

        if tokens is None:
            tokens = capacity
        else:
            tokens = float(tokens)

        if last_time is None:
            last_time = current_time
        else:
            last_time = float(last_time)

        # Refill tokens
        time_passed = current_time - last_time
        tokens = min(capacity, tokens + (time_passed * refill_rate))

        if tokens < 1:
            # Calculate wait time
            wait_time = (1 - tokens) / refill_rate
            return False, wait_time

        # Consume token
        tokens -= 1

        # Update Redis
        self.redis_client.set(tokens_key, tokens)
        self.redis_client.set(last_time_key, current_time)

        # Set expiry
        self.redis_client.expire(tokens_key, int(capacity / refill_rate) * 2)
        self.redis_client.expire(last_time_key, int(capacity / refill_rate) * 2)

        return True, None

    def get_limit_status(self, identifier: str, rule_name: str = "api_requests") -> Dict[str, Any]:
        """Get current rate limit status for an identifier."""
        if rule_name not in self.rules:
            return {"error": "Rule not found"}

        rule = self.rules[rule_name]

        if self.redis_client:
            return self._get_limit_status_redis(identifier, rule_name, rule)
        else:
            return self._get_limit_status_local(identifier, rule)

    def _get_limit_status_local(self, identifier: str, rule: Dict[str, Any]) -> Dict[str, Any]:
        """Get rate limit status from local storage."""
        algorithm = rule["algorithm"]
        current_time = time.time()

        if algorithm == "sliding_window":
            requests = self.request_counts[identifier]
            # Clean old requests
            while requests and current_time - requests[0] > rule["window_seconds"]:
                requests.popleft()
            current_requests = len(requests)
        else:
            current_requests = getattr(self, f'_count_{identifier}', 0)

        return {
            "current_requests": current_requests,
            "max_requests": rule["max_requests"],
            "remaining": max(0, rule["max_requests"] - current_requests),
            "reset_time": current_time + rule["window_seconds"]
        }

    def _get_limit_status_redis(self, identifier: str, rule_name: str, rule: Dict[str, Any]) -> Dict[str, Any]:
        """Get rate limit status from Redis."""
        try:
            algorithm = rule["algorithm"]

            if algorithm == "sliding_window":
                key = f"ratelimit:{rule_name}:{identifier}"
                count = self.redis_client.zcard(key)
                current_requests = count
            else:
                # Simplified for other algorithms
                current_requests = 0

            return {
                "current_requests": current_requests,
                "max_requests": rule["max_requests"],
                "remaining": max(0, rule["max_requests"] - current_requests),
                "reset_time": time.time() + rule["window_seconds"]
            }

        except Exception as e:
            logger.error(f"Redis status check error: {e}")
            return {"error": "Redis error"}

    def reset_limits(self, identifier: str):
        """Reset rate limits for an identifier."""
        # Clear local tracking
        if identifier in self.request_counts:
            self.request_counts[identifier].clear()
        if identifier in self.burst_counts:
            keys_to_remove = [k for k in self.burst_counts.keys() if k.startswith(f"{identifier}:")]
            for k in keys_to_remove:
                del self.burst_counts[k]

        # Clear Redis tracking
        if self.redis_client:
            try:
                pattern = f"ratelimit:*:{identifier}*"
                keys = self.redis_client.keys(pattern)
                if keys:
                    self.redis_client.delete(*keys)
            except Exception as e:
                logger.error(f"Redis reset error: {e}")

        logger.info(f"Rate limits reset for: {identifier}")

    def get_stats(self) -> Dict[str, Any]:
        """Get rate limiting statistics."""
        return {
            "enabled": self.enabled,
            "rules_count": len(self.rules),
            "tracked_identifiers": len(self.request_counts),
            "redis_enabled": self.redis_client is not None,
            "rules": list(self.rules.keys())
        }