"""
Tamper Detection System

File integrity monitoring and tamper detection.
"""

import hashlib
import json
import time
from pathlib import Path
from typing import Dict, Any, List, Optional, Set
from dataclasses import dataclass
from datetime import datetime

from pydiscobasepro.core.logging import get_logger

logger = get_logger(__name__)

@dataclass
class FileIntegrityRecord:
    """Record of file integrity information."""
    path: Path
    hash_sha256: str
    size: int
    modified_time: float
    created_time: float
    last_checked: float
    tamper_detected: bool = False
    tamper_time: Optional[float] = None

class TamperDetectionSystem:
    """File integrity monitoring and tamper detection."""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.enabled = config.get("enabled", True)
        self.integrity_db_file = Path.home() / ".pydiscobasepro" / "integrity_db.json"
        self.alerts_file = Path.home() / ".pydiscobasepro" / "tamper_alerts.json"

        self.integrity_records: Dict[str, FileIntegrityRecord] = {}
        self.monitored_paths: Set[Path] = set()
        self.alerts: List[Dict[str, Any]] = []

        self.load_integrity_database()
        self.load_alerts()

    def load_integrity_database(self):
        """Load the integrity database."""
        if self.integrity_db_file.exists():
            try:
                with open(self.integrity_db_file, 'r') as f:
                    data = json.load(f)

                for path_str, record_data in data.items():
                    path = Path(path_str)
                    record = FileIntegrityRecord(
                        path=path,
                        hash_sha256=record_data["hash_sha256"],
                        size=record_data["size"],
                        modified_time=record_data["modified_time"],
                        created_time=record_data["created_time"],
                        last_checked=record_data["last_checked"],
                        tamper_detected=record_data.get("tamper_detected", False),
                        tamper_time=record_data.get("tamper_time")
                    )
                    self.integrity_records[path_str] = record

            except Exception as e:
                logger.error(f"Failed to load integrity database: {e}")

    def save_integrity_database(self):
        """Save the integrity database."""
        try:
            data = {}
            for path_str, record in self.integrity_records.items():
                data[path_str] = {
                    "hash_sha256": record.hash_sha256,
                    "size": record.size,
                    "modified_time": record.modified_time,
                    "created_time": record.created_time,
                    "last_checked": record.last_checked,
                    "tamper_detected": record.tamper_detected,
                    "tamper_time": record.tamper_time
                }

            with open(self.integrity_db_file, 'w') as f:
                json.dump(data, f, indent=2)

        except Exception as e:
            logger.error(f"Failed to save integrity database: {e}")

    def load_alerts(self):
        """Load tamper alerts."""
        if self.alerts_file.exists():
            try:
                with open(self.alerts_file, 'r') as f:
                    self.alerts = json.load(f)
            except Exception as e:
                logger.error(f"Failed to load tamper alerts: {e}")
                self.alerts = []

    def save_alerts(self):
        """Save tamper alerts."""
        try:
            with open(self.alerts_file, 'w') as f:
                json.dump(self.alerts, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save tamper alerts: {e}")

    def add_monitored_path(self, path: Union[str, Path], recursive: bool = True):
        """Add a path to integrity monitoring."""
        path = Path(path)

        if recursive and path.is_dir():
            for file_path in path.rglob('*'):
                if file_path.is_file():
                    self.monitored_paths.add(file_path)
        else:
            if path.is_file():
                self.monitored_paths.add(path)
            elif path.is_dir():
                for file_path in path.iterdir():
                    if file_path.is_file():
                        self.monitored_paths.add(file_path)

        logger.info(f"Added path to monitoring: {path}")

    def remove_monitored_path(self, path: Union[str, Path]):
        """Remove a path from integrity monitoring."""
        path = Path(path)
        paths_to_remove = {p for p in self.monitored_paths if p == path or path in p.parents}

        for p in paths_to_remove:
            self.monitored_paths.discard(p)
            self.integrity_records.pop(str(p), None)

        self.save_integrity_database()
        logger.info(f"Removed path from monitoring: {path}")

    def baseline_files(self):
        """Create baseline integrity records for monitored files."""
        for file_path in self.monitored_paths:
            if file_path.exists():
                record = self._calculate_integrity_record(file_path)
                self.integrity_records[str(file_path)] = record

        self.save_integrity_database()
        logger.info(f"Created baseline for {len(self.integrity_records)} files")

    def check_integrity(self) -> Dict[str, List[str]]:
        """Check integrity of all monitored files."""
        if not self.enabled:
            return {"tampered": [], "missing": [], "new": []}

        tampered = []
        missing = []
        new_files = []

        for file_path in self.monitored_paths.copy():
            path_str = str(file_path)

            if not file_path.exists():
                if path_str in self.integrity_records:
                    missing.append(path_str)
                    self._record_tamper_alert(path_str, "file_missing")
                continue

            # Check if file is new
            if path_str not in self.integrity_records:
                new_files.append(path_str)
                # Auto-baseline new files
                record = self._calculate_integrity_record(file_path)
                self.integrity_records[path_str] = record
                continue

            # Check existing file
            current_record = self._calculate_integrity_record(file_path)
            stored_record = self.integrity_records[path_str]

            if self._records_differ(current_record, stored_record):
                tampered.append(path_str)
                self._record_tamper_alert(path_str, "file_modified", current_record, stored_record)
                stored_record.tamper_detected = True
                stored_record.tamper_time = time.time()

            stored_record.last_checked = time.time()

        self.save_integrity_database()
        self.save_alerts()

        return {
            "tampered": tampered,
            "missing": missing,
            "new": new_files
        }

    def _calculate_integrity_record(self, file_path: Path) -> FileIntegrityRecord:
        """Calculate integrity record for a file."""
        stat = file_path.stat()

        # Calculate SHA256 hash
        hash_sha256 = self._calculate_file_hash(file_path)

        return FileIntegrityRecord(
            path=file_path,
            hash_sha256=hash_sha256,
            size=stat.st_size,
            modified_time=stat.st_mtime,
            created_time=getattr(stat, 'st_birthtime', stat.st_ctime),
            last_checked=time.time()
        )

    def _calculate_file_hash(self, file_path: Path) -> str:
        """Calculate SHA256 hash of file."""
        hash_obj = hashlib.sha256()

        try:
            with open(file_path, 'rb') as f:
                for chunk in iter(lambda: f.read(4096), b''):
                    hash_obj.update(chunk)
        except Exception as e:
            logger.error(f"Failed to hash file {file_path}: {e}")
            return ""

        return hash_obj.hexdigest()

    def _records_differ(self, current: FileIntegrityRecord, stored: FileIntegrityRecord) -> bool:
        """Check if two integrity records differ."""
        return (
            current.hash_sha256 != stored.hash_sha256 or
            current.size != stored.size or
            abs(current.modified_time - stored.modified_time) > 1  # Allow 1 second tolerance
        )

    def _record_tamper_alert(self, file_path: str, alert_type: str,
                           current_record: Optional[FileIntegrityRecord] = None,
                           stored_record: Optional[FileIntegrityRecord] = None):
        """Record a tamper alert."""
        alert = {
            "timestamp": datetime.now().isoformat(),
            "file_path": file_path,
            "alert_type": alert_type,
            "severity": "high" if alert_type == "file_modified" else "medium"
        }

        if current_record and stored_record:
            alert["details"] = {
                "stored_hash": stored_record.hash_sha256,
                "current_hash": current_record.hash_sha256,
                "stored_size": stored_record.size,
                "current_size": current_record.size,
                "stored_modified": stored_record.modified_time,
                "current_modified": current_record.modified_time
            }

        self.alerts.append(alert)

        # Keep only last 1000 alerts
        self.alerts = self.alerts[-1000:]

        logger.warning(f"Tamper alert: {alert_type} for {file_path}")

    def get_integrity_status(self) -> Dict[str, Any]:
        """Get overall integrity status."""
        integrity_check = self.check_integrity()

        return {
            "enabled": self.enabled,
            "monitored_files": len(self.monitored_paths),
            "baseline_records": len(self.integrity_records),
            "tampered_files": len(integrity_check["tampered"]),
            "missing_files": len(integrity_check["missing"]),
            "new_files": len(integrity_check["new"]),
            "total_alerts": len(self.alerts)
        }

    def get_file_integrity_info(self, file_path: Union[str, Path]) -> Optional[Dict[str, Any]]:
        """Get integrity information for a specific file."""
        path_str = str(file_path)
        record = self.integrity_records.get(path_str)

        if not record:
            return None

        return {
            "path": str(record.path),
            "hash_sha256": record.hash_sha256,
            "size": record.size,
            "modified_time": record.modified_time,
            "created_time": record.created_time,
            "last_checked": record.last_checked,
            "tamper_detected": record.tamper_detected,
            "tamper_time": record.tamper_time
        }

    def list_tamper_alerts(self, limit: int = 50) -> List[Dict[str, Any]]:
        """List recent tamper alerts."""
        return self.alerts[-limit:]

    def clear_tamper_alerts(self):
        """Clear all tamper alerts."""
        self.alerts.clear()
        self.save_alerts()
        logger.info("Tamper alerts cleared")

    def reset_file_baseline(self, file_path: Union[str, Path]):
        """Reset baseline for a specific file."""
        file_path = Path(file_path)
        if file_path.exists():
            record = self._calculate_integrity_record(file_path)
            self.integrity_records[str(file_path)] = record
            self.save_integrity_database()
            logger.info(f"Baseline reset for: {file_path}")

    def export_integrity_report(self, export_path: Path):
        """Export integrity report."""
        report = {
            "generated_at": datetime.now().isoformat(),
            "status": self.get_integrity_status(),
            "monitored_files": [str(p) for p in self.monitored_paths],
            "integrity_records": {
                path: self.get_file_integrity_info(path)
                for path in self.integrity_records.keys()
            },
            "recent_alerts": self.list_tamper_alerts(100)
        }

        try:
            with open(export_path, 'w') as f:
                json.dump(report, f, indent=2, default=str)

            logger.info(f"Integrity report exported to: {export_path}")

        except Exception as e:
            logger.error(f"Failed to export integrity report: {e}")

    def enable_monitoring(self):
        """Enable tamper detection."""
        self.enabled = True
        logger.info("Tamper detection enabled")

    def disable_monitoring(self):
        """Disable tamper detection."""
        self.enabled = False
        logger.info("Tamper detection disabled")