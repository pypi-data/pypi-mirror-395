"""
Log Rotation System

Automatic log rotation and archival.
"""

import logging.handlers
import gzip
import shutil
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime

class LogRotationSystem:
    """Log rotation and archival system."""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.enabled = config.get("enabled", True)
        self.max_size = config.get("max_size", 10*1024*1024)  # 10MB
        self.backup_count = config.get("backup_count", 5)
        self.compress = config.get("compress", True)

        self.logs_dir = Path("logs")
        self.archive_dir = self.logs_dir / "archive"
        self.archive_dir.mkdir(exist_ok=True)

    def setup_rotation(self, logger: logging.Logger, log_file: Path):
        """Setup log rotation for logger."""
        if not self.enabled:
            return

        handler = logging.handlers.RotatingFileHandler(
            log_file,
            maxBytes=self.max_size,
            backupCount=self.backup_count
        )

        if self.compress:
            handler.rotator = self._compress_rotator
            handler.namer = self._compressed_namer

        handler.setFormatter(logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        ))

        logger.addHandler(handler)

    def _compress_rotator(self, source, dest):
        """Compress rotated log file."""
        with open(source, 'rb') as f_in:
            with gzip.open(dest, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        Path(source).unlink()  # Remove original

    def _compressed_namer(self, name):
        """Name compressed log files."""
        return name + ".gz"

    def cleanup_old_logs(self, days: int = 30):
        """Clean up logs older than specified days."""
        cutoff = datetime.now().timestamp() - (days * 24 * 60 * 60)

        for log_file in self.archive_dir.glob("*.gz"):
            if log_file.stat().st_mtime < cutoff:
                log_file.unlink()