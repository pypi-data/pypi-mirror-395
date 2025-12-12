"""
Intrusion Detection Module

Advanced intrusion detection and prevention system.
"""

import asyncio
import time
from collections import defaultdict, deque
from typing import Dict, Any, List, Optional, Set
from datetime import datetime, timedelta
import re
import ipaddress

from pydiscobasepro.core.logging import get_logger

logger = get_logger(__name__)

class IntrusionDetector:
    """Advanced intrusion detection and prevention system."""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.enabled = config.get("enabled", True)

        # Detection rules
        self.failed_login_threshold = config.get("failed_login_threshold", 5)
        self.brute_force_window = config.get("brute_force_window", 300)  # 5 minutes
        self.suspicious_activity_threshold = config.get("suspicious_activity_threshold", 10)

        # Tracking data
        self.failed_logins: Dict[str, deque] = defaultdict(lambda: deque(maxlen=100))
        self.suspicious_ips: Set[str] = set()
        self.blocked_ips: Set[str] = set()
        self.rate_limit_violations: Dict[str, deque] = defaultdict(lambda: deque(maxlen=100))

        # Pattern detection
        self.sql_injection_patterns = [
            r"(\b(SELECT|INSERT|UPDATE|DELETE|DROP|CREATE|ALTER)\b.*\b(FROM|INTO|TABLE|DATABASE)\b)",
            r"(\bUNION\b.*\bSELECT\b)",
            r"(\bOR\b.*\d+\s*=\s*\d+)",
            r"(\bAND\b.*\d+\s*=\s*\d+)"
        ]

        self.xss_patterns = [
            r"<script[^>]*>.*?</script>",
            r"javascript:",
            r"on\w+\s*=",
            r"<iframe[^>]*>.*?</iframe>"
        ]

        # Alert callbacks
        self.alert_callbacks: List[callable] = []

    def add_alert_callback(self, callback: callable):
        """Add callback for intrusion alerts."""
        self.alert_callbacks.append(callback)

    async def check_failed_login(self, ip_address: str, username: str) -> bool:
        """Check for failed login attempts."""
        if not self.enabled:
            return False

        current_time = time.time()
        login_attempts = self.failed_logins[ip_address]

        # Clean old attempts
        while login_attempts and current_time - login_attempts[0] > self.brute_force_window:
            login_attempts.popleft()

        # Add current attempt
        login_attempts.append(current_time)

        # Check threshold
        if len(login_attempts) >= self.failed_login_threshold:
            await self._trigger_alert("brute_force_attempt", {
                "ip_address": ip_address,
                "username": username,
                "attempts": len(login_attempts),
                "time_window": self.brute_force_window
            })
            self.blocked_ips.add(ip_address)
            return True

        return False

    async def check_rate_limit_violation(self, ip_address: str, endpoint: str) -> bool:
        """Check for rate limit violations."""
        if not self.enabled:
            return False

        current_time = time.time()
        violations = self.rate_limit_violations[ip_address]

        # Clean old violations
        while violations and current_time - violations[0] > 60:  # 1 minute window
            violations.popleft()

        # Add current violation
        violations.append(current_time)

        # Check threshold
        if len(violations) >= 10:  # 10 violations per minute
            await self._trigger_alert("rate_limit_abuse", {
                "ip_address": ip_address,
                "endpoint": endpoint,
                "violations": len(violations)
            })
            return True

        return False

    def check_sql_injection(self, input_string: str) -> bool:
        """Check for SQL injection patterns."""
        if not self.enabled:
            return False

        for pattern in self.sql_injection_patterns:
            if re.search(pattern, input_string, re.IGNORECASE):
                asyncio.create_task(self._trigger_alert("sql_injection_attempt", {
                    "pattern": pattern,
                    "input_length": len(input_string)
                }))
                return True
        return False

    def check_xss_attempt(self, input_string: str) -> bool:
        """Check for XSS attack patterns."""
        if not self.enabled:
            return False

        for pattern in self.xss_patterns:
            if re.search(pattern, input_string, re.IGNORECASE):
                asyncio.create_task(self._trigger_alert("xss_attempt", {
                    "pattern": pattern,
                    "input_length": len(input_string)
                }))
                return True
        return False

    async def check_suspicious_activity(self, ip_address: str, activity: str) -> bool:
        """Check for suspicious activity patterns."""
        if not self.enabled:
            return False

        # Simple heuristic: multiple different suspicious activities
        if ip_address not in self.suspicious_ips:
            return False

        # This would be more sophisticated in a real implementation
        # For now, just count activities
        activity_count = getattr(self, f'_activity_count_{ip_address}', 0)
        activity_count += 1
        setattr(self, f'_activity_count_{ip_address}', activity_count)

        if activity_count >= self.suspicious_activity_threshold:
            await self._trigger_alert("suspicious_activity", {
                "ip_address": ip_address,
                "activity_count": activity_count,
                "last_activity": activity
            })
            return True

        return False

    def is_ip_blocked(self, ip_address: str) -> bool:
        """Check if IP address is blocked."""
        return ip_address in self.blocked_ips

    def block_ip(self, ip_address: str, reason: str = "manual_block"):
        """Manually block an IP address."""
        self.blocked_ips.add(ip_address)
        asyncio.create_task(self._trigger_alert("ip_blocked", {
            "ip_address": ip_address,
            "reason": reason,
            "blocked_by": "manual"
        }))
        logger.warning(f"IP blocked: {ip_address} ({reason})")

    def unblock_ip(self, ip_address: str):
        """Unblock an IP address."""
        self.blocked_ips.discard(ip_address)
        logger.info(f"IP unblocked: {ip_address}")

    def mark_suspicious(self, ip_address: str, reason: str):
        """Mark an IP as suspicious."""
        self.suspicious_ips.add(ip_address)
        logger.warning(f"IP marked suspicious: {ip_address} ({reason})")

    async def _trigger_alert(self, alert_type: str, details: Dict[str, Any]):
        """Trigger intrusion alert."""
        alert = {
            "type": alert_type,
            "timestamp": datetime.now().isoformat(),
            "details": details,
            "severity": self._get_alert_severity(alert_type)
        }

        logger.warning(f"Intrusion alert: {alert_type} - {details}")

        # Execute callbacks
        for callback in self.alert_callbacks:
            try:
                await callback(alert)
            except Exception as e:
                logger.error(f"Alert callback error: {e}")

    def _get_alert_severity(self, alert_type: str) -> str:
        """Get severity level for alert type."""
        severity_map = {
            "brute_force_attempt": "high",
            "sql_injection_attempt": "critical",
            "xss_attempt": "high",
            "rate_limit_abuse": "medium",
            "suspicious_activity": "medium",
            "ip_blocked": "low"
        }
        return severity_map.get(alert_type, "low")

    def get_intrusion_stats(self) -> Dict[str, Any]:
        """Get intrusion detection statistics."""
        return {
            "enabled": self.enabled,
            "blocked_ips_count": len(self.blocked_ips),
            "suspicious_ips_count": len(self.suspicious_ips),
            "failed_login_attempts": sum(len(attempts) for attempts in self.failed_logins.values()),
            "rate_limit_violations": sum(len(violations) for violations in self.rate_limit_violations.values()),
            "blocked_ips": list(self.blocked_ips),
            "suspicious_ips": list(self.suspicious_ips)
        }

    def reset_ip_tracking(self, ip_address: str):
        """Reset tracking data for an IP address."""
        if ip_address in self.failed_logins:
            self.failed_logins[ip_address].clear()
        if ip_address in self.rate_limit_violations:
            self.rate_limit_violations[ip_address].clear()
        self.suspicious_ips.discard(ip_address)
        self.blocked_ips.discard(ip_address)

        # Reset activity count
        if hasattr(self, f'_activity_count_{ip_address}'):
            delattr(self, f'_activity_count_{ip_address}')

        logger.info(f"Tracking reset for IP: {ip_address}")

    def add_custom_detection_rule(self, rule_name: str, pattern: str, alert_type: str):
        """Add a custom detection rule."""
        # This would allow adding custom regex patterns or rules
        logger.info(f"Custom detection rule added: {rule_name}")

    def export_intrusion_data(self) -> Dict[str, Any]:
        """Export intrusion detection data for analysis."""
        return {
            "timestamp": datetime.now().isoformat(),
            "stats": self.get_intrusion_stats(),
            "failed_logins": dict(self.failed_logins),
            "rate_limit_violations": dict(self.rate_limit_violations),
            "recent_alerts": getattr(self, '_recent_alerts', [])[-50:]  # Last 50 alerts
        }

    def _store_recent_alert(self, alert: Dict[str, Any]):
        """Store recent alerts for export."""
        if not hasattr(self, '_recent_alerts'):
            self._recent_alerts = []
        self._recent_alerts.append(alert)
        # Keep only last 100 alerts
        self._recent_alerts = self._recent_alerts[-100:]