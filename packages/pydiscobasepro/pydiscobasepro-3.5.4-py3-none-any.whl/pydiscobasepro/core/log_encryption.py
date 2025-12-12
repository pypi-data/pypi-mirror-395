"""
Log Encryption

Encrypt sensitive log data.
"""

from cryptography.fernet import Fernet
from pathlib import Path
from typing import Dict, Any, Optional
import base64

class LogEncryption:
    """Log encryption for sensitive data."""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.enabled = config.get("enabled", False)
        self.key_file = Path.home() / ".pydiscobasepro" / "log_key.key"

        self._cipher = None
        if self.enabled:
            self._cipher = self._load_or_generate_key()

    def _load_or_generate_key(self) -> Fernet:
        """Load or generate encryption key."""
        if self.key_file.exists():
            key = self.key_file.read_bytes()
        else:
            key = Fernet.generate_key()
            self.key_file.write_bytes(key)
            self.key_file.chmod(0o600)
        return Fernet(key)

    def encrypt_log_entry(self, log_data: str) -> str:
        """Encrypt log entry."""
        if not self.enabled or not self._cipher:
            return log_data

        encrypted = self._cipher.encrypt(log_data.encode())
        return f"ENCRYPTED:{encrypted.hex()}"

    def decrypt_log_entry(self, encrypted_log: str) -> str:
        """Decrypt log entry."""
        if not encrypted_log.startswith("ENCRYPTED:"):
            return encrypted_log

        if not self._cipher:
            return "[ENCRYPTED - NO KEY]"

        try:
            encrypted_hex = encrypted_log[10:]  # Remove "ENCRYPTED:" prefix
            encrypted = bytes.fromhex(encrypted_hex)
            decrypted = self._cipher.decrypt(encrypted)
            return decrypted.decode()
        except Exception:
            return "[DECRYPTION FAILED]"