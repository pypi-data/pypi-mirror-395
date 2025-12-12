"""
System Watchdog

Monitors system health and automatically recovers from failures.
"""

import asyncio
import time
import psutil
from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass
from enum import Enum

from pydiscobasepro.core.logging import get_logger

logger = get_logger(__name__)

class WatchdogState(Enum):
    """Watchdog monitoring states."""
    HEALTHY = "healthy"
    WARNING = "warning"
    CRITICAL = "critical"
    RECOVERING = "recovering"

@dataclass
class HealthCheck:
    """Represents a health check configuration."""
    name: str
    check_function: Callable[[], bool]
    interval: float
    max_failures: int
    recovery_action: Optional[Callable] = None

class SystemWatchdog:
    """System watchdog for monitoring and automatic recovery."""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.enabled = config.get("enabled", True)
        self.check_interval = config.get("check_interval", 60)
        self.auto_restart = config.get("auto_restart", True)

        self.state = WatchdogState.HEALTHY
        self.health_checks: List[HealthCheck] = []
        self.failure_counts: Dict[str, int] = {}
        self.last_check_time = 0
        self.monitoring_task: Optional[asyncio.Task] = None

        self._setup_default_checks()

    def _setup_default_checks(self):
        """Setup default health checks."""
        self.add_health_check(
            "cpu_usage",
            self._check_cpu_usage,
            interval=30,
            max_failures=3,
            recovery_action=self._recover_high_cpu
        )

        self.add_health_check(
            "memory_usage",
            self._check_memory_usage,
            interval=30,
            max_failures=3,
            recovery_action=self._recover_high_memory
        )

        self.add_health_check(
            "disk_space",
            self._check_disk_space,
            interval=300,  # 5 minutes
            max_failures=2,
            recovery_action=self._recover_low_disk
        )

        self.add_health_check(
            "process_health",
            self._check_process_health,
            interval=60,
            max_failures=5,
            recovery_action=self._recover_process_failure
        )

    def add_health_check(
        self,
        name: str,
        check_function: Callable[[], bool],
        interval: float = 60,
        max_failures: int = 3,
        recovery_action: Optional[Callable] = None
    ):
        """Add a custom health check."""
        health_check = HealthCheck(
            name=name,
            check_function=check_function,
            interval=interval,
            max_failures=max_failures,
            recovery_action=recovery_action
        )
        self.health_checks.append(health_check)
        self.failure_counts[name] = 0

    async def start(self):
        """Start the watchdog monitoring."""
        if not self.enabled:
            logger.info("System watchdog disabled")
            return

        self.monitoring_task = asyncio.create_task(self._monitoring_loop())
        logger.info("System watchdog started")

    async def stop(self):
        """Stop the watchdog monitoring."""
        if self.monitoring_task:
            self.monitoring_task.cancel()
            try:
                await self.monitoring_task
            except asyncio.CancelledError:
                pass
        logger.info("System watchdog stopped")

    async def _monitoring_loop(self):
        """Main monitoring loop."""
        while True:
            try:
                current_time = time.time()

                # Run health checks
                for check in self.health_checks:
                    if current_time - getattr(check, '_last_run', 0) >= check.interval:
                        await self._run_health_check(check)
                        check._last_run = current_time

                # Update overall state
                await self._update_overall_state()

                # Wait before next cycle
                await asyncio.sleep(self.check_interval)

            except Exception as e:
                logger.error(f"Watchdog monitoring error: {e}")
                await asyncio.sleep(self.check_interval)

    async def _run_health_check(self, check: HealthCheck):
        """Run a single health check."""
        try:
            healthy = await check.check_function()

            if healthy:
                # Reset failure count on success
                self.failure_counts[check.name] = 0
                logger.debug(f"Health check '{check.name}' passed")
            else:
                # Increment failure count
                self.failure_counts[check.name] += 1
                logger.warning(f"Health check '{check.name}' failed ({self.failure_counts[check.name]}/{check.max_failures})")

                # Check if max failures reached
                if self.failure_counts[check.name] >= check.max_failures:
                    await self._trigger_recovery(check)

        except Exception as e:
            logger.error(f"Health check '{check.name}' error: {e}")
            self.failure_counts[check.name] += 1

    async def _trigger_recovery(self, check: HealthCheck):
        """Trigger recovery action for failed health check."""
        logger.warning(f"Triggering recovery for '{check.name}'")

        if check.recovery_action:
            try:
                await check.recovery_action()
                # Reset failure count after successful recovery
                self.failure_counts[check.name] = 0
                logger.info(f"Recovery action completed for '{check.name}'")
            except Exception as e:
                logger.error(f"Recovery action failed for '{check.name}': {e}")
        else:
            logger.warning(f"No recovery action defined for '{check.name}'")

    async def _update_overall_state(self):
        """Update the overall system state based on health checks."""
        critical_failures = sum(
            1 for check in self.health_checks
            if self.failure_counts[check.name] >= check.max_failures
        )

        if critical_failures > 0:
            new_state = WatchdogState.CRITICAL
        elif any(self.failure_counts[check.name] > 0 for check in self.health_checks):
            new_state = WatchdogState.WARNING
        else:
            new_state = WatchdogState.HEALTHY

        if new_state != self.state:
            logger.info(f"Watchdog state changed: {self.state.value} -> {new_state.value}")
            self.state = new_state

    # Default health check implementations

    async def _check_cpu_usage(self) -> bool:
        """Check CPU usage is within acceptable limits."""
        cpu_percent = psutil.cpu_percent(interval=1)
        return cpu_percent < 90  # 90% threshold

    async def _check_memory_usage(self) -> bool:
        """Check memory usage is within acceptable limits."""
        memory = psutil.virtual_memory()
        return memory.percent < 85  # 85% threshold

    async def _check_disk_space(self) -> bool:
        """Check disk space is sufficient."""
        disk = psutil.disk_usage('/')
        return disk.percent < 90  # 90% threshold

    async def _check_process_health(self) -> bool:
        """Check main process is healthy."""
        try:
            process = psutil.Process()
            # Check if process is still running and not zombie
            return process.is_running() and process.status() != psutil.STATUS_ZOMBIE
        except psutil.NoSuchProcess:
            return False

    # Recovery actions

    async def _recover_high_cpu(self):
        """Recovery action for high CPU usage."""
        logger.info("Attempting CPU usage recovery")
        # Force garbage collection
        import gc
        gc.collect()

        # Could also implement process priority changes or alerts

    async def _recover_high_memory(self):
        """Recovery action for high memory usage."""
        logger.info("Attempting memory usage recovery")
        import gc
        gc.collect()

        # Clear any caches if available
        # This would integrate with the cache manager

    async def _recover_low_disk(self):
        """Recovery action for low disk space."""
        logger.warning("Low disk space detected - manual intervention required")
        # Could implement log rotation or cleanup

    async def _recover_process_failure(self):
        """Recovery action for process failure."""
        if self.auto_restart:
            logger.warning("Process failure detected - attempting restart")
            # This would integrate with the main application restart logic
            # For now, just log the issue
        else:
            logger.critical("Process failure detected - auto-restart disabled")

    def get_status(self) -> Dict[str, Any]:
        """Get current watchdog status."""
        return {
            "enabled": self.enabled,
            "state": self.state.value,
            "health_checks": [
                {
                    "name": check.name,
                    "failures": self.failure_counts[check.name],
                    "max_failures": check.max_failures,
                    "interval": check.interval
                }
                for check in self.health_checks
            ],
            "last_check": self.last_check_time
        }

    def reset_failure_count(self, check_name: str):
        """Manually reset failure count for a health check."""
        if check_name in self.failure_counts:
            self.failure_counts[check_name] = 0
            logger.info(f"Failure count reset for '{check_name}'")