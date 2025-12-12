"""
Audit Logging System

Comprehensive audit logging for security and compliance.
"""

import json
import threading
from pathlib import Path
from typing import Dict, Any, Optional, List
from datetime import datetime
from queue import Queue
import atexit

from pydiscobasepro.core.logging import get_logger

logger = get_logger(__name__)

class AuditLogger:
    """Comprehensive audit logging system."""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.audit_log_file = Path.home() / ".pydiscobasepro" / "audit.log"
        self.audit_archive_dir = Path.home() / ".pydiscobasepro" / "audit_archive"

        self.audit_archive_dir.mkdir(exist_ok=True)

        # Async logging queue
        self.log_queue = Queue()
        self.log_thread = threading.Thread(target=self._log_worker, daemon=True)
        self.log_thread.start()

        # Register cleanup
        atexit.register(self._cleanup)

        self.enabled = config.get("enabled", True)
        self.max_log_size = config.get("max_log_size", 10*1024*1024)  # 10MB
        self.retention_days = config.get("retention_days", 90)

    def _cleanup(self):
        """Cleanup on shutdown."""
        self.log_queue.put(None)  # Signal worker to stop
        self.log_thread.join(timeout=5)

    def log_event(
        self,
        event_type: str,
        user_id: str,
        action: str,
        resource: str,
        details: Optional[Dict[str, Any]] = None,
        ip_address: str = "unknown",
        user_agent: str = "unknown",
        success: bool = True,
        severity: str = "info"
    ):
        """Log an audit event."""
        if not self.enabled:
            return

        event = {
            "timestamp": datetime.now().isoformat(),
            "event_type": event_type,
            "user_id": user_id,
            "action": action,
            "resource": resource,
            "details": details or {},
            "ip_address": ip_address,
            "user_agent": user_agent,
            "success": success,
            "severity": severity,
            "session_id": getattr(self, '_current_session', 'unknown')
        }

        self.log_queue.put(event)

    def _log_worker(self):
        """Background worker for writing audit logs."""
        while True:
            event = self.log_queue.get()
            if event is None:  # Shutdown signal
                break

            try:
                self._write_audit_event(event)
                self._check_log_rotation()
            except Exception as e:
                logger.error(f"Audit logging error: {e}")

            self.log_queue.task_done()

    def _write_audit_event(self, event: Dict[str, Any]):
        """Write audit event to log file."""
        try:
            with open(self.audit_log_file, 'a') as f:
                json.dump(event, f, default=str)
                f.write('\n')
        except Exception as e:
            logger.error(f"Failed to write audit event: {e}")

    def _check_log_rotation(self):
        """Check if log rotation is needed."""
        if self.audit_log_file.exists() and self.audit_log_file.stat().st_size > self.max_log_size:
            self._rotate_audit_log()

    def _rotate_audit_log(self):
        """Rotate the audit log file."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        archive_file = self.audit_archive_dir / f"audit_{timestamp}.log"

        try:
            # Move current log to archive
            self.audit_log_file.rename(archive_file)

            # Compress old archives
            self._compress_old_archives()

            # Clean up old archives
            self._cleanup_old_archives()

            logger.info(f"Audit log rotated: {archive_file}")

        except Exception as e:
            logger.error(f"Log rotation failed: {e}")

    def _compress_old_archives(self):
        """Compress old archive files."""
        import gzip

        for archive_file in self.audit_archive_dir.glob("audit_*.log"):
            if not archive_file.name.endswith(".gz"):
                try:
                    compressed_file = archive_file.with_suffix(".log.gz")
                    with open(archive_file, 'rb') as f_in:
                        with gzip.open(compressed_file, 'wb') as f_out:
                            f_out.writelines(f_in)
                    archive_file.unlink()
                except Exception as e:
                    logger.error(f"Failed to compress {archive_file}: {e}")

    def _cleanup_old_archives(self):
        """Clean up archives older than retention period."""
        cutoff_date = datetime.now().timestamp() - (self.retention_days * 24 * 60 * 60)

        for archive_file in self.audit_archive_dir.glob("audit_*.log.gz"):
            if archive_file.stat().st_mtime < cutoff_date:
                try:
                    archive_file.unlink()
                    logger.debug(f"Deleted old audit archive: {archive_file}")
                except Exception as e:
                    logger.error(f"Failed to delete {archive_file}: {e}")

    def search_audit_logs(
        self,
        user_id: Optional[str] = None,
        event_type: Optional[str] = None,
        action: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """Search audit logs with filters."""
        results = []

        # Search current log
        if self.audit_log_file.exists():
            results.extend(self._search_file(
                self.audit_log_file, user_id, event_type, action, start_date, end_date, limit
            ))

        # Search archived logs if needed
        if len(results) < limit:
            for archive_file in sorted(self.audit_archive_dir.glob("audit_*.log.gz"), reverse=True):
                if len(results) >= limit:
                    break

                remaining_limit = limit - len(results)
                results.extend(self._search_file(
                    archive_file, user_id, event_type, action, start_date, end_date, remaining_limit
                ))

        return results[:limit]

    def _search_file(
        self,
        log_file: Path,
        user_id: Optional[str],
        event_type: Optional[str],
        action: Optional[str],
        start_date: Optional[datetime],
        end_date: Optional[datetime],
        limit: int
    ) -> List[Dict[str, Any]]:
        """Search a specific log file."""
        results = []

        try:
            import gzip
            open_func = gzip.open if log_file.suffix == ".gz" else open

            with open_func(log_file, 'rt') as f:
                for line in f:
                    if len(results) >= limit:
                        break

                    try:
                        event = json.loads(line.strip())

                        # Apply filters
                        if user_id and event.get("user_id") != user_id:
                            continue
                        if event_type and event.get("event_type") != event_type:
                            continue
                        if action and event.get("action") != action:
                            continue

                        event_timestamp = datetime.fromisoformat(event["timestamp"])
                        if start_date and event_timestamp < start_date:
                            continue
                        if end_date and event_timestamp > end_date:
                            continue

                        results.append(event)

                    except json.JSONDecodeError:
                        continue

        except Exception as e:
            logger.error(f"Error searching {log_file}: {e}")

        return results

    def get_audit_stats(self) -> Dict[str, Any]:
        """Get audit logging statistics."""
        stats = {
            "enabled": self.enabled,
            "current_log_size": 0,
            "archive_count": 0,
            "total_events": 0,
            "events_by_type": {},
            "events_by_user": {},
            "recent_failures": 0
        }

        if self.audit_log_file.exists():
            stats["current_log_size"] = self.audit_log_file.stat().st_size

        # Count archived logs
        stats["archive_count"] = len(list(self.audit_archive_dir.glob("audit_*.log.gz")))

        # Count events in current log
        if self.audit_log_file.exists():
            try:
                with open(self.audit_log_file, 'r') as f:
                    for line in f:
                        stats["total_events"] += 1
                        try:
                            event = json.loads(line.strip())
                            event_type = event.get("event_type", "unknown")
                            user_id = event.get("user_id", "unknown")

                            stats["events_by_type"][event_type] = stats["events_by_type"].get(event_type, 0) + 1
                            stats["events_by_user"][user_id] = stats["events_by_user"].get(user_id, 0) + 1

                            if not event.get("success", True):
                                stats["recent_failures"] += 1
                        except json.JSONDecodeError:
                            continue
            except Exception as e:
                logger.error(f"Error reading audit stats: {e}")

        return stats

    def export_audit_logs(self, export_path: Path, start_date: Optional[datetime] = None, end_date: Optional[datetime] = None):
        """Export audit logs to a file."""
        events = self.search_audit_logs(
            start_date=start_date,
            end_date=end_date,
            limit=10000  # Reasonable limit for export
        )

        try:
            with open(export_path, 'w') as f:
                json.dump(events, f, indent=2, default=str)

            logger.info(f"Audit logs exported to: {export_path}")

        except Exception as e:
            logger.error(f"Failed to export audit logs: {e}")

    def set_session_context(self, session_id: str):
        """Set current session context for audit logging."""
        self._current_session = session_id