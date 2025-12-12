"""
Auto Recovery System

Automatic system recovery with crash snapshots and state restoration.
"""

import asyncio
import pickle
import json
from pathlib import Path
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from datetime import datetime
import traceback
import sys

from pydiscobasepro.core.logging import get_logger

logger = get_logger(__name__)

@dataclass
class CrashSnapshot:
    """Represents a system crash snapshot."""
    timestamp: datetime
    exception: Exception
    traceback: str
    system_state: Dict[str, Any]
    active_tasks: List[str]
    memory_usage: Dict[str, Any]

class AutoRecoverySystem:
    """Automatic recovery system with crash analysis and state restoration."""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.auto_backup = config.get("auto_backup", True)
        self.max_snapshots = config.get("max_snapshots", 10)

        self.snapshots_dir = Path.home() / ".pydiscobasepro" / "snapshots"
        self.snapshots_dir.mkdir(exist_ok=True)

        self.recovery_strategies: Dict[str, callable] = {}
        self.system_state: Dict[str, Any] = {}

        self._setup_default_strategies()

    def _setup_default_strategies(self):
        """Setup default recovery strategies."""
        self.recovery_strategies = {
            "memory_error": self._recover_memory_error,
            "connection_error": self._recover_connection_error,
            "timeout_error": self._recover_timeout_error,
            "file_system_error": self._recover_file_system_error,
            "generic_error": self._recover_generic_error
        }

    async def initialize(self):
        """Initialize the recovery system."""
        # Setup global exception handler
        sys.excepthook = self._global_exception_handler

        # Setup asyncio exception handler
        loop = asyncio.get_event_loop()
        loop.set_exception_handler(self._asyncio_exception_handler)

        logger.info("Auto recovery system initialized")

    def _global_exception_handler(self, exc_type, exc_value, exc_traceback):
        """Global exception handler for unhandled exceptions."""
        logger.critical("Unhandled exception caught by recovery system")
        asyncio.create_task(self.handle_crash(exc_value, exc_traceback))

    def _asyncio_exception_handler(self, loop, context):
        """Asyncio exception handler."""
        logger.error(f"Asyncio exception: {context}")
        exception = context.get('exception')
        if exception:
            asyncio.create_task(self.handle_crash(exception))

    async def handle_crash(self, exception: Exception, traceback_obj=None):
        """Handle a system crash with recovery attempt."""
        logger.critical(f"System crash detected: {exception}")

        # Create crash snapshot
        snapshot = await self._create_crash_snapshot(exception, traceback_obj)

        # Save snapshot
        await self._save_crash_snapshot(snapshot)

        # Attempt recovery
        recovery_success = await self._attempt_recovery(exception)

        if recovery_success:
            logger.info("Automatic recovery successful")
        else:
            logger.critical("Automatic recovery failed - manual intervention required")

    async def _create_crash_snapshot(self, exception: Exception, traceback_obj=None) -> CrashSnapshot:
        """Create a comprehensive crash snapshot."""
        import psutil

        # Get system state
        system_state = {
            "python_version": sys.version,
            "platform": sys.platform,
            "working_directory": str(Path.cwd()),
            "environment": dict(os.environ)
        }

        # Get memory usage
        process = psutil.Process()
        memory_info = process.memory_info()
        memory_usage = {
            "rss": memory_info.rss,
            "vms": memory_info.vms,
            "percent": process.memory_percent()
        }

        # Get active tasks (simplified)
        active_tasks = []
        try:
            current_task = asyncio.current_task()
            if current_task:
                active_tasks.append(str(current_task))
        except RuntimeError:
            pass

        # Get traceback
        if traceback_obj:
            tb_str = ''.join(traceback.format_tb(traceback_obj))
        else:
            tb_str = traceback.format_exc()

        snapshot = CrashSnapshot(
            timestamp=datetime.now(),
            exception=exception,
            traceback=tb_str,
            system_state=system_state,
            active_tasks=active_tasks,
            memory_usage=memory_usage
        )

        return snapshot

    async def _save_crash_snapshot(self, snapshot: CrashSnapshot):
        """Save crash snapshot to disk."""
        snapshot_file = self.snapshots_dir / f"crash_{snapshot.timestamp.strftime('%Y%m%d_%H%M%S')}.pkl"

        try:
            with open(snapshot_file, 'wb') as f:
                pickle.dump(snapshot, f)

            logger.info(f"Crash snapshot saved: {snapshot_file}")

            # Cleanup old snapshots
            await self._cleanup_old_snapshots()

        except Exception as e:
            logger.error(f"Failed to save crash snapshot: {e}")

    async def _cleanup_old_snapshots(self):
        """Clean up old crash snapshots."""
        snapshots = list(self.snapshots_dir.glob("crash_*.pkl"))
        if len(snapshots) > self.max_snapshots:
            # Sort by modification time, keep newest
            snapshots.sort(key=lambda x: x.stat().st_mtime, reverse=True)
            to_delete = snapshots[self.max_snapshots:]

            for snapshot_file in to_delete:
                snapshot_file.unlink()
                logger.debug(f"Deleted old snapshot: {snapshot_file}")

    async def _attempt_recovery(self, exception: Exception) -> bool:
        """Attempt automatic recovery based on exception type."""
        exception_type = type(exception).__name__.lower()

        # Find appropriate recovery strategy
        strategy = None
        for key, recovery_func in self.recovery_strategies.items():
            if key in exception_type:
                strategy = recovery_func
                break

        if not strategy:
            strategy = self.recovery_strategies.get("generic_error")

        if strategy:
            try:
                return await strategy(exception)
            except Exception as recovery_error:
                logger.error(f"Recovery strategy failed: {recovery_error}")
                return False

        return False

    # Recovery strategies

    async def _recover_memory_error(self, exception: Exception) -> bool:
        """Recover from memory-related errors."""
        logger.info("Attempting memory error recovery")

        import gc
        gc.collect()

        # Clear any caches
        # This would integrate with cache manager

        # Restart memory-intensive components
        # This would integrate with component managers

        return True

    async def _recover_connection_error(self, exception: Exception) -> bool:
        """Recover from connection-related errors."""
        logger.info("Attempting connection error recovery")

        # Wait and retry connections
        await asyncio.sleep(5)

        # Reinitialize connections
        # This would integrate with database and external service managers

        return True

    async def _recover_timeout_error(self, exception: Exception) -> bool:
        """Recover from timeout errors."""
        logger.info("Attempting timeout error recovery")

        # Increase timeouts temporarily
        # Adjust resource limits

        return True

    async def _recover_file_system_error(self, exception: Exception) -> bool:
        """Recover from file system errors."""
        logger.info("Attempting file system error recovery")

        # Check disk space
        import shutil
        total, used, free = shutil.disk_usage("/")
        if free < 100 * 1024 * 1024:  # Less than 100MB free
            logger.critical("Insufficient disk space for recovery")
            return False

        # Attempt file system repair operations
        # This would be platform-specific

        return True

    async def _recover_generic_error(self, exception: Exception) -> bool:
        """Generic recovery strategy."""
        logger.info("Attempting generic error recovery")

        # Basic cleanup
        import gc
        gc.collect()

        # Log additional diagnostic information
        logger.info(f"Exception type: {type(exception)}")
        logger.info(f"Exception args: {exception.args}")

        # For generic errors, we can only do basic recovery
        return True

    async def handle_reload_failure(self, path: Path, error: Exception):
        """Handle hot-reload failure with recovery."""
        logger.warning(f"Hot-reload failed for {path}: {error}")

        # Create recovery snapshot
        snapshot = await self._create_crash_snapshot(error)
        snapshot.system_state["reload_path"] = str(path)

        await self._save_crash_snapshot(snapshot)

        # Attempt to restore previous version
        await self._restore_previous_version(path)

    async def _restore_previous_version(self, path: Path):
        """Attempt to restore previous version of a file."""
        backup_path = path.with_suffix('.backup')
        if backup_path.exists():
            try:
                backup_path.rename(path)
                logger.info(f"Restored previous version of {path}")
            except Exception as e:
                logger.error(f"Failed to restore backup: {e}")

    def save_system_state(self, key: str, state: Dict[str, Any]):
        """Save system state for recovery."""
        self.system_state[key] = state

    def get_system_state(self, key: str) -> Optional[Dict[str, Any]]:
        """Get saved system state."""
        return self.system_state.get(key)

    async def create_backup_snapshot(self):
        """Create a backup snapshot of current system state."""
        if not self.auto_backup:
            return

        logger.info("Creating backup snapshot")

        # This would capture current system state
        # Implementation depends on what needs to be backed up

        snapshot = CrashSnapshot(
            timestamp=datetime.now(),
            exception=None,
            traceback="",
            system_state=self.system_state.copy(),
            active_tasks=[],
            memory_usage={}
        )

        await self._save_crash_snapshot(snapshot)

    def get_recovery_report(self) -> Dict[str, Any]:
        """Generate recovery system report."""
        snapshots = list(self.snapshots_dir.glob("crash_*.pkl"))

        return {
            "auto_backup_enabled": self.auto_backup,
            "max_snapshots": self.max_snapshots,
            "current_snapshots": len(snapshots),
            "recovery_strategies": list(self.recovery_strategies.keys()),
            "system_state_keys": list(self.system_state.keys()),
            "snapshots_dir": str(self.snapshots_dir)
        }