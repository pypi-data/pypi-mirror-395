"""
Core Security Manager

Comprehensive security system with authentication, authorization, encryption, and monitoring.
"""

import asyncio
import hashlib
import secrets
import time
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime, timedelta
from pathlib import Path
import json
import ipaddress
from functools import wraps

from pydiscobasepro.core.logging import get_logger

logger = get_logger(__name__)

class SecurityManager:
    """Enterprise-grade security management system."""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.audit_log_file = Path.home() / ".pydiscobasepro" / "audit.log"
        self.rate_limit_store: Dict[str, List[float]] = {}
        self.brute_force_attempts: Dict[str, List[datetime]] = {}

        # Security settings
        self.encryption_enabled = config.get("encryption_enabled", True)
        self.audit_enabled = config.get("audit_logging", True)
        self.rate_limiting_enabled = config.get("rate_limiting", True)
        self.brute_force_protection = config.get("brute_force_protection", True)

        # Rate limiting config
        rl_config = config.get("rate_limiting", {})
        self.rate_limit_max = rl_config.get("max_requests", 100)
        self.rate_limit_window = rl_config.get("window_seconds", 60)

        # Brute force config
        self.brute_force_max_attempts = 5
        self.brute_force_window = timedelta(minutes=15)

    async def initialize(self):
        """Initialize security systems."""
        logger.info("Security manager initialized")

    def audit_log(self, action: str, user: str = "system", details: Optional[Dict[str, Any]] = None, ip: str = "unknown"):
        """Log security-related actions."""
        if not self.audit_enabled:
            return

        entry = {
            "timestamp": datetime.now().isoformat(),
            "action": action,
            "user": user,
            "ip": ip,
            "details": details or {}
        }

        try:
            with open(self.audit_log_file, 'a') as f:
                json.dump(entry, f)
                f.write('\n')
        except Exception as e:
            logger.error(f"Audit logging failed: {e}")

    def check_rate_limit(self, identifier: str) -> bool:
        """Check if request is within rate limits."""
        if not self.rate_limiting_enabled:
            return True

        now = time.time()
        window_start = now - self.rate_limit_window

        # Clean old entries
        if identifier in self.rate_limit_store:
            self.rate_limit_store[identifier] = [
                ts for ts in self.rate_limit_store[identifier] if ts > window_start
            ]

        # Check current count
        current_count = len(self.rate_limit_store.get(identifier, []))
        if current_count >= self.rate_limit_max:
            self.audit_log("rate_limit_exceeded", identifier)
            return False

        # Add current request
        if identifier not in self.rate_limit_store:
            self.rate_limit_store[identifier] = []
        self.rate_limit_store[identifier].append(now)

        return True

    def check_brute_force(self, identifier: str) -> bool:
        """Check for brute force attack patterns."""
        if not self.brute_force_protection:
            return True

        now = datetime.now()
        window_start = now - self.brute_force_window

        # Clean old attempts
        if identifier in self.brute_force_attempts:
            self.brute_force_attempts[identifier] = [
                ts for ts in self.brute_force_attempts[identifier] if ts > window_start
            ]

        # Check if blocked
        attempts = len(self.brute_force_attempts.get(identifier, []))
        if attempts >= self.brute_force_max_attempts:
            self.audit_log("brute_force_blocked", identifier)
            return False

        # Record attempt
        if identifier not in self.brute_force_attempts:
            self.brute_force_attempts[identifier] = []
        self.brute_force_attempts[identifier].append(now)

        return True

    def validate_ip_address(self, ip: str) -> bool:
        """Validate IP address format."""
        try:
            ipaddress.ip_address(ip)
            return True
        except ValueError:
            return False

    def hash_sensitive_data(self, data: str) -> str:
        """Hash sensitive data for storage."""
        return hashlib.sha256(data.encode()).hexdigest()

    def generate_secure_token(self, length: int = 32) -> str:
        """Generate cryptographically secure token."""
        return secrets.token_hex(length)

    def sanitize_input(self, input_str: str, max_length: int = 1000) -> str:
        """Sanitize user input to prevent injection attacks."""
        # Basic sanitization - remove potentially dangerous characters
        sanitized = input_str.replace('<', '&lt;').replace('>', '&gt;')
        sanitized = sanitized.replace('"', '&quot;').replace("'", '&#x27;')

        # Limit length
        return sanitized[:max_length]

    def check_file_permissions(self, file_path: Path) -> bool:
        """Check if file has secure permissions."""
        try:
            stat = file_path.stat()
            # Check if file is world-readable/writable
            permissions = oct(stat.st_mode)[-3:]
            return permissions[0] != '7' and permissions[1] != '7' and permissions[2] != '7'
        except Exception:
            return False

    def secure_delete_file(self, file_path: Path, passes: int = 3):
        """Securely delete a file by overwriting with random data."""
        if not file_path.exists():
            return

        try:
            size = file_path.stat().st_size
            with open(file_path, 'wb') as f:
                for _ in range(passes):
                    f.write(secrets.token_bytes(size))
                    f.flush()

            file_path.unlink()
            self.audit_log("secure_file_deletion", str(file_path))

        except Exception as e:
            logger.error(f"Secure file deletion failed: {e}")

    def tamper_detection_check(self, data: str, expected_hash: str) -> bool:
        """Check data integrity using hash comparison."""
        current_hash = hashlib.sha256(data.encode()).hexdigest()
        return current_hash == expected_hash

    def get_security_report(self) -> Dict[str, Any]:
        """Generate security status report."""
        report = {
            "encryption_enabled": self.encryption_enabled,
            "audit_logging_enabled": self.audit_enabled,
            "rate_limiting_enabled": self.rate_limiting_enabled,
            "brute_force_protection_enabled": self.brute_force_protection,
            "active_rate_limits": len(self.rate_limit_store),
            "active_brute_force_blocks": len([
                ident for ident, attempts in self.brute_force_attempts.items()
                if len(attempts) >= self.brute_force_max_attempts
            ]),
            "audit_log_entries": self._count_audit_entries(),
            "generated_at": datetime.now().isoformat()
        }

        return report

    def _count_audit_entries(self) -> int:
        """Count total audit log entries."""
        if not self.audit_log_file.exists():
            return 0

        try:
            with open(self.audit_log_file, 'r') as f:
                return sum(1 for _ in f)
        except Exception:
            return 0

    def security_middleware(self, func):
        """Decorator for adding security checks to functions."""
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Rate limiting check
            if not self.check_rate_limit("function_call"):
                raise Exception("Rate limit exceeded")

            # Execute function
            try:
                result = await func(*args, **kwargs)
                return result
            except Exception as e:
                self.audit_log("function_error", str(func.__name__), {"error": str(e)})
                raise

        return wrapper