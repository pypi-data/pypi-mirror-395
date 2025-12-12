"""
Structured Logging Engine

Advanced logging with structured data and multiple outputs.
"""

import structlog
import logging
import logging.handlers
from pathlib import Path
from typing import Dict, Any, Optional
import json
from datetime import datetime

class StructuredLoggingEngine:
    """Structured logging engine with multiple outputs."""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.enabled = config.get("enabled", True)
        self.level = config.get("level", "INFO")
        self.structured = config.get("structured", True)

        self.log_file = Path(config.get("file", "logs/bot.log"))
        self.log_file.parent.mkdir(exist_ok=True)

        self._setup_logging()

    def _setup_logging(self):
        """Setup structured logging."""
        if not self.enabled:
            return

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
                self._json_processor if self.structured else structlog.processors.JSONRenderer(),
            ],
            context_class=dict,
            logger_factory=structlog.stdlib.LoggerFactory(),
            wrapper_class=structlog.stdlib.BoundLogger,
            cache_logger_on_first_use=True,
        )

        # Setup standard logging
        logger = logging.getLogger()
        logger.setLevel(getattr(logging, self.level))

        # File handler
        file_handler = logging.handlers.RotatingFileHandler(
            self.log_file, maxBytes=10*1024*1024, backupCount=5
        )
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        ))
        logger.addHandler(file_handler)

    def _json_processor(self, logger, method_name, event_dict):
        """JSON processor for structured logs."""
        return json.dumps(event_dict, default=str)

    def get_logger(self, name: str) -> structlog.BoundLogger:
        """Get structured logger."""
        return structlog.get_logger(name)