"""
Rotating Secrets System

Automatic rotation of secrets and cryptographic keys.
"""

import asyncio
import secrets
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List, Callable
from pathlib import Path
import json

from pydiscobasepro.core.logging import get_logger

logger = get_logger(__name__)

class SecretsRotator:
    """Automatic rotation of secrets and cryptographic keys."""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.rotation_schedule_file = Path.home() / ".pydiscobasepro" / "rotation_schedule.json"
        self.rotation_history_file = Path.home() / ".pydiscobasepro" / "rotation_history.json"

        self.rotation_tasks: Dict[str, Dict[str, Any]] = {}
        self.rotation_callbacks: Dict[str, List[Callable]] = {}
        self.running = False

        self.load_rotation_schedule()
        self.load_rotation_history()

    def load_rotation_schedule(self):
        """Load rotation schedule from file."""
        if self.rotation_schedule_file.exists():
            try:
                with open(self.rotation_schedule_file, 'r') as f:
                    self.rotation_tasks = json.load(f)
            except Exception as e:
                logger.error(f"Failed to load rotation schedule: {e}")
                self.rotation_tasks = {}

    def save_rotation_schedule(self):
        """Save rotation schedule to file."""
        try:
            with open(self.rotation_schedule_file, 'w') as f:
                json.dump(self.rotation_tasks, f, indent=2, default=str)
        except Exception as e:
            logger.error(f"Failed to save rotation schedule: {e}")

    def load_rotation_history(self):
        """Load rotation history from file."""
        if self.rotation_history_file.exists():
            try:
                with open(self.rotation_history_file, 'r') as f:
                    self.rotation_history = json.load(f)
            except Exception as e:
                logger.error(f"Failed to load rotation history: {e}")
                self.rotation_history = []

    def save_rotation_history(self):
        """Save rotation history to file."""
        try:
            with open(self.rotation_history_file, 'w') as f:
                json.dump(self.rotation_history[-1000:], f, indent=2, default=str)  # Keep last 1000 entries
        except Exception as e:
            logger.error(f"Failed to save rotation history: {e}")

    def register_rotation_task(
        self,
        task_id: str,
        rotation_function: Callable,
        interval_days: int,
        description: str = "",
        max_age_days: Optional[int] = None
    ):
        """Register a secret rotation task."""
        self.rotation_tasks[task_id] = {
            "function": rotation_function.__name__,
            "interval_days": interval_days,
            "description": description,
            "max_age_days": max_age_days,
            "last_rotation": None,
            "next_rotation": datetime.now().isoformat(),
            "enabled": True
        }

        self.save_rotation_schedule()
        logger.info(f"Rotation task registered: {task_id}")

    def unregister_rotation_task(self, task_id: str):
        """Unregister a rotation task."""
        if task_id in self.rotation_tasks:
            del self.rotation_tasks[task_id]
            self.save_rotation_schedule()
            logger.info(f"Rotation task unregistered: {task_id}")

    def add_rotation_callback(self, task_id: str, callback: Callable):
        """Add a callback to be executed after rotation."""
        if task_id not in self.rotation_callbacks:
            self.rotation_callbacks[task_id] = []
        self.rotation_callbacks[task_id].append(callback)

    async def start_rotation_scheduler(self):
        """Start the automatic rotation scheduler."""
        if self.running:
            return

        self.running = True
        logger.info("Secrets rotation scheduler started")

        while self.running:
            try:
                await self._check_and_rotate_secrets()
                await asyncio.sleep(3600)  # Check every hour

            except Exception as e:
                logger.error(f"Rotation scheduler error: {e}")
                await asyncio.sleep(3600)

    async def stop_rotation_scheduler(self):
        """Stop the rotation scheduler."""
        self.running = False
        logger.info("Secrets rotation scheduler stopped")

    async def _check_and_rotate_secrets(self):
        """Check and rotate secrets that are due."""
        now = datetime.now()

        for task_id, task_config in self.rotation_tasks.items():
            if not task_config.get("enabled", True):
                continue

            next_rotation = datetime.fromisoformat(task_config["next_rotation"])

            if now >= next_rotation:
                await self._rotate_secret(task_id, task_config)

    async def _rotate_secret(self, task_id: str, task_config: Dict[str, Any]):
        """Rotate a specific secret."""
        try:
            logger.info(f"Starting rotation for task: {task_id}")

            # Import and call rotation function
            # This assumes rotation functions are in a specific module
            # In practice, you'd want more sophisticated function resolution
            rotation_function = getattr(self, f"_rotate_{task_config['function']}", None)
            if rotation_function:
                await rotation_function(task_id)
            else:
                logger.error(f"Rotation function not found: {task_config['function']}")

            # Update task schedule
            now = datetime.now()
            interval_days = task_config["interval_days"]
            next_rotation = now + timedelta(days=interval_days)

            task_config["last_rotation"] = now.isoformat()
            task_config["next_rotation"] = next_rotation.isoformat()

            self.save_rotation_schedule()

            # Record in history
            self._record_rotation_history(task_id, "success", task_config["description"])

            # Execute callbacks
            await self._execute_rotation_callbacks(task_id)

            logger.info(f"Rotation completed for task: {task_id}")

        except Exception as e:
            logger.error(f"Rotation failed for task {task_id}: {e}")
            self._record_rotation_history(task_id, "failed", str(e))

    def _record_rotation_history(self, task_id: str, status: str, details: str):
        """Record rotation event in history."""
        self.rotation_history.append({
            "task_id": task_id,
            "timestamp": datetime.now().isoformat(),
            "status": status,
            "details": details
        })
        self.save_rotation_history()

    async def _execute_rotation_callbacks(self, task_id: str):
        """Execute callbacks for a rotation task."""
        if task_id in self.rotation_callbacks:
            for callback in self.rotation_callbacks[task_id]:
                try:
                    await callback(task_id)
                except Exception as e:
                    logger.error(f"Rotation callback error for {task_id}: {e}")

    # Specific rotation implementations

    async def _rotate_jwt_secret(self, task_id: str):
        """Rotate JWT secret key."""
        from pydiscobasepro.core.token_auth import TokenAuth
        # This would need access to the TokenAuth instance
        # Implementation depends on how TokenAuth is structured
        logger.info("JWT secret rotation not yet implemented")

    async def _rotate_encryption_key(self, task_id: str):
        """Rotate encryption keys."""
        from pydiscobasepro.core.secrets_vault import SecretsVault
        # This would need access to the SecretsVault instance
        logger.info("Encryption key rotation not yet implemented")

    async def _rotate_api_keys(self, task_id: str):
        """Rotate API keys."""
        # Generate new API key
        new_key = secrets.token_hex(32)

        # Store in secrets vault
        from pydiscobasepro.core.secrets_vault import SecretsVault
        vault = SecretsVault({})
        vault.store_secret(f"api_key_{task_id}", new_key, {"rotated": True})

        logger.info(f"API key rotated for {task_id}")

    async def _rotate_database_credentials(self, task_id: str):
        """Rotate database credentials."""
        # This would integrate with database credential rotation
        logger.info("Database credential rotation not yet implemented")

    def get_rotation_status(self) -> Dict[str, Any]:
        """Get status of all rotation tasks."""
        status = {}
        now = datetime.now()

        for task_id, task_config in self.rotation_tasks.items():
            next_rotation = datetime.fromisoformat(task_config["next_rotation"])
            days_until_rotation = (next_rotation - now).days

            status[task_id] = {
                "description": task_config["description"],
                "enabled": task_config["enabled"],
                "last_rotation": task_config["last_rotation"],
                "next_rotation": task_config["next_rotation"],
                "days_until_rotation": max(0, days_until_rotation),
                "overdue": days_until_rotation < 0
            }

        return status

    def force_rotate(self, task_id: str) -> bool:
        """Force immediate rotation of a secret."""
        if task_id not in self.rotation_tasks:
            return False

        # Reset next rotation to now
        self.rotation_tasks[task_id]["next_rotation"] = datetime.now().isoformat()
        self.save_rotation_schedule()

        logger.info(f"Forced rotation scheduled for: {task_id}")
        return True

    def enable_rotation_task(self, task_id: str) -> bool:
        """Enable a rotation task."""
        if task_id in self.rotation_tasks:
            self.rotation_tasks[task_id]["enabled"] = True
            self.save_rotation_schedule()
            return True
        return False

    def disable_rotation_task(self, task_id: str) -> bool:
        """Disable a rotation task."""
        if task_id in self.rotation_tasks:
            self.rotation_tasks[task_id]["enabled"] = False
            self.save_rotation_schedule()
            return True
        return False

    def get_rotation_history(self, task_id: Optional[str] = None, limit: int = 50) -> List[Dict[str, Any]]:
        """Get rotation history."""
        history = self.rotation_history

        if task_id:
            history = [entry for entry in history if entry["task_id"] == task_id]

        return history[-limit:]