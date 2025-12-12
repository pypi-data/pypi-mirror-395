"""
Core Cache Manager

Hybrid in-memory and disk caching system with Redis support.
"""

import asyncio
import pickle
import hashlib
from typing import Any, Dict, Optional, Union
from pathlib import Path
from datetime import datetime, timedelta
import threading
import time

from pydiscobasepro.core.logging import get_logger

logger = get_logger(__name__)

class CacheManager:
    """Hybrid caching system with memory, disk, and Redis support."""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.enabled = config.get("enabled", True)
        self.ttl = config.get("ttl", 3600)
        self.max_memory_items = config.get("max_memory_items", 1000)

        # Memory cache
        self._memory_cache: Dict[str, Dict[str, Any]] = {}
        self._memory_lock = threading.Lock()

        # Disk cache
        self._disk_cache_dir = Path.home() / ".pydiscobasepro" / "cache"
        self._disk_cache_dir.mkdir(exist_ok=True, parents=True)

        # Redis cache
        self._redis_enabled = False
        self._redis_client = None
        redis_url = config.get("redis_url")
        if redis_url:
            self._setup_redis(redis_url)

        # Cleanup task
        self._cleanup_task = None

    def _setup_redis(self, redis_url: str):
        """Setup Redis connection."""
        try:
            import redis
            self._redis_client = redis.from_url(redis_url)
            self._redis_client.ping()  # Test connection
            self._redis_enabled = True
            logger.info("Redis cache enabled")
        except ImportError:
            logger.warning("redis package not installed, Redis cache disabled")
        except Exception as e:
            logger.error(f"Redis connection failed: {e}")

    async def initialize(self):
        """Initialize cache system."""
        if not self.enabled:
            return

        # Start cleanup task
        self._cleanup_task = asyncio.create_task(self._cleanup_loop())
        logger.info("Cache system initialized")

    async def shutdown(self):
        """Shutdown cache system."""
        if self._cleanup_task:
            self._cleanup_task.cancel()
            try:
                await self._cleanup_task
            except asyncio.CancelledError:
                pass

    def _generate_key(self, key: str) -> str:
        """Generate cache key with optional hashing."""
        if len(key) > 250:  # Redis key length limit
            return hashlib.md5(key.encode()).hexdigest()
        return key

    async def get(self, key: str) -> Optional[Any]:
        """Get value from cache."""
        if not self.enabled:
            return None

        cache_key = self._generate_key(key)

        # Try Redis first
        if self._redis_enabled:
            try:
                value = self._redis_client.get(cache_key)
                if value:
                    return pickle.loads(value)
            except Exception as e:
                logger.error(f"Redis get error: {e}")

        # Try memory cache
        with self._memory_lock:
            if cache_key in self._memory_cache:
                entry = self._memory_cache[cache_key]
                if self._is_expired(entry):
                    del self._memory_cache[cache_key]
                else:
                    return entry["value"]

        # Try disk cache
        disk_value = await self._get_from_disk(cache_key)
        if disk_value is not None:
            # Promote to memory cache
            await self.set(key, disk_value, ttl=self.ttl)
            return disk_value

        return None

    async def set(self, key: str, value: Any, ttl: Optional[int] = None):
        """Set value in cache."""
        if not self.enabled:
            return

        cache_key = self._generate_key(key)
        expiry = time.time() + (ttl or self.ttl)

        entry = {
            "value": value,
            "expiry": expiry,
            "created": time.time()
        }

        # Store in Redis
        if self._redis_enabled:
            try:
                pickled_value = pickle.dumps(value)
                self._redis_client.setex(cache_key, ttl or self.ttl, pickled_value)
            except Exception as e:
                logger.error(f"Redis set error: {e}")

        # Store in memory
        with self._memory_lock:
            self._memory_cache[cache_key] = entry

            # Enforce memory limit
            if len(self._memory_cache) > self.max_memory_items:
                self._evict_oldest_memory_item()

        # Store on disk (for persistence)
        await self._save_to_disk(cache_key, entry)

    async def delete(self, key: str):
        """Delete value from cache."""
        cache_key = self._generate_key(key)

        # Delete from Redis
        if self._redis_enabled:
            try:
                self._redis_client.delete(cache_key)
            except Exception as e:
                logger.error(f"Redis delete error: {e}")

        # Delete from memory
        with self._memory_lock:
            self._memory_cache.pop(cache_key, None)

        # Delete from disk
        disk_file = self._disk_cache_dir / f"{cache_key}.pkl"
        if disk_file.exists():
            disk_file.unlink()

    async def clear(self):
        """Clear all cache entries."""
        # Clear Redis
        if self._redis_enabled:
            try:
                self._redis_client.flushdb()
            except Exception as e:
                logger.error(f"Redis clear error: {e}")

        # Clear memory
        with self._memory_lock:
            self._memory_cache.clear()

        # Clear disk
        for cache_file in self._disk_cache_dir.glob("*.pkl"):
            cache_file.unlink()

        logger.info("Cache cleared")

    def _is_expired(self, entry: Dict[str, Any]) -> bool:
        """Check if cache entry is expired."""
        return time.time() > entry["expiry"]

    def _evict_oldest_memory_item(self):
        """Evict oldest item from memory cache."""
        if not self._memory_cache:
            return

        oldest_key = min(
            self._memory_cache.keys(),
            key=lambda k: self._memory_cache[k]["created"]
        )
        del self._memory_cache[oldest_key]

    async def _get_from_disk(self, key: str) -> Optional[Any]:
        """Get value from disk cache."""
        disk_file = self._disk_cache_dir / f"{key}.pkl"
        if not disk_file.exists():
            return None

        try:
            with open(disk_file, 'rb') as f:
                entry = pickle.load(f)

            if self._is_expired(entry):
                disk_file.unlink()
                return None

            return entry["value"]

        except Exception as e:
            logger.error(f"Disk cache read error: {e}")
            return None

    async def _save_to_disk(self, key: str, entry: Dict[str, Any]):
        """Save entry to disk cache."""
        disk_file = self._disk_cache_dir / f"{key}.pkl"
        try:
            with open(disk_file, 'wb') as f:
                pickle.dump(entry, f)
        except Exception as e:
            logger.error(f"Disk cache write error: {e}")

    async def _cleanup_loop(self):
        """Periodic cleanup of expired entries."""
        while True:
            try:
                await asyncio.sleep(300)  # Clean every 5 minutes

                # Clean memory cache
                with self._memory_lock:
                    expired_keys = [
                        k for k, v in self._memory_cache.items()
                        if self._is_expired(v)
                    ]
                    for k in expired_keys:
                        del self._memory_cache[k]

                # Clean disk cache
                for cache_file in self._disk_cache_dir.glob("*.pkl"):
                    try:
                        with open(cache_file, 'rb') as f:
                            entry = pickle.load(f)
                        if self._is_expired(entry):
                            cache_file.unlink()
                    except Exception:
                        # Remove corrupted files
                        cache_file.unlink()

            except Exception as e:
                logger.error(f"Cache cleanup error: {e}")

    async def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        stats = {
            "memory_items": len(self._memory_cache),
            "redis_enabled": self._redis_enabled,
            "disk_cache_size": sum(
                f.stat().st_size for f in self._disk_cache_dir.glob("*.pkl")
            )
        }

        if self._redis_enabled:
            try:
                stats["redis_keys"] = self._redis_client.dbsize()
                stats["redis_memory"] = self._redis_client.info()["used_memory"]
            except Exception as e:
                logger.error(f"Redis stats error: {e}")

        return stats