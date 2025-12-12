"""
Core Logging System

Structured logging with encryption, rotation, and multiple outputs.
"""

import logging
import logging.handlers
import structlog
from pathlib import Path
from typing import Dict, Any, Optional
import json
import gzip
from datetime import datetime
from cryptography.fernet import Fernet

from pydiscobasepro.core.config import ConfigManager

class StructuredLogger:
    """Structured logging system with encryption and rotation."""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.logs_dir = Path("logs")
        self.logs_dir.mkdir(exist_ok=True)
        self.encryption_enabled = config.get("logging.encryption", False)
        self._cipher = None

        if self.encryption_enabled:
            self._cipher = Fernet(self._get_encryption_key())

    def _get_encryption_key(self) -> bytes:
        """Get encryption key for logs."""
        key_file = Path.home() / ".pydiscobasepro" / "log_encryption.key"
        if key_file.exists():
            return key_file.read_bytes()
        else:
            key = Fernet.generate_key()
            key_file.write_bytes(key)
            return key

    def setup_logging(self):
        """Setup structured logging."""
        # Configure structlog
        structlog.configure(
            processors=[
                structlog.stdlib.filter_by_level,
                structlog.stdlib.add_logger_name,
                structlog.stdlib.add_log_level,
                structlog.stdlib.PositionalArgumentsFormatter(),
                structlog.processors.TimeStamper(fmt="iso"),
                structlog.processors.StackInfoRenderer(),
                structlog.processors.format_exc_info,
                structlog.processors.UnicodeDecoder(),
                self._encrypt_processor if self.encryption_enabled else structlog.processors.JSONRenderer(),
            ],
            context_class=dict,
            logger_factory=structlog.stdlib.LoggerFactory(),
            wrapper_class=structlog.stdlib.BoundLogger,
            cache_logger_on_first_use=True,
        )

        # Setup standard logging
        logger = logging.getLogger()
        logger.setLevel(getattr(logging, self.config.get("logging.level", "INFO")))

        # File handler with rotation
        log_file = self.config.get("logging.file", "logs/bot.log")
        file_handler = logging.handlers.RotatingFileHandler(
            log_file,
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5
        )
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        ))
        logger.addHandler(file_handler)

        # Discord channel handler (if configured)
        discord_channel_id = self.config.get("logging.discord_channel_id")
        if discord_channel_id:
            try:
                from pydiscobasepro.core.discord_logger import DiscordLogHandler
                discord_handler = DiscordLogHandler(discord_channel_id)
                discord_handler.setLevel(logging.WARNING)  # Only warnings and above
                logger.addHandler(discord_handler)
            except ImportError:
                pass  # Discord logger not available

    def _encrypt_processor(self, logger, method_name, event_dict):
        """Processor to encrypt log entries."""
        if not self._cipher:
            return event_dict
        json_str = json.dumps(event_dict, default=str)
        encrypted = self._cipher.encrypt(json_str.encode())
        return {"encrypted_log": encrypted.hex()}

    def decrypt_log_entry(self, encrypted_hex: str) -> Dict[str, Any]:
        """Decrypt a log entry."""
        if not self._cipher:
            raise ValueError("Encryption not enabled")

        encrypted = bytes.fromhex(encrypted_hex)
        decrypted = self._cipher.decrypt(encrypted)
        return json.loads(decrypted.decode())

    def rotate_logs(self):
        """Manually rotate log files."""
        for log_file in self.logs_dir.glob("*.log"):
            if log_file.stat().st_size > 10*1024*1024:  # 10MB
                self._compress_log_file(log_file)

    def _compress_log_file(self, log_file: Path):
        """Compress a log file."""
        compressed_file = log_file.with_suffix(f".log.{datetime.now().strftime('%Y%m%d_%H%M%S')}.gz")

        with open(log_file, 'rb') as f_in:
            with gzip.open(compressed_file, 'wb') as f_out:
                f_out.writelines(f_in)

        # Clear original file
        log_file.write_text("")

def setup_structured_logging(config: Optional[Dict[str, Any]] = None, cli_mode: bool = False):
    """Setup structured logging system."""
    if config is None:
        if cli_mode:
            # For CLI, use minimal config without loading bot config
            config = {"logging": {"level": "INFO", "structured": True}}
        else:
            config_manager = ConfigManager()
            config = config_manager.load_config()

    logger = StructuredLogger(config.get("logging", {}))
    logger.setup_logging()

def get_logger(name: str) -> structlog.BoundLogger:
    """Get a structured logger instance."""
    return structlog.get_logger(name)