"""
Encrypted Secrets Vault

Secure storage and management of sensitive configuration data.
"""

import os
import json
from pathlib import Path
from typing import Dict, Any, Optional
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import secrets
from datetime import datetime

from pydiscobasepro.core.logging import get_logger

logger = get_logger(__name__)

class SecretsVault:
    """Encrypted secrets vault for sensitive data storage."""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.vault_file = Path.home() / ".pydiscobasepro" / "secrets.vault"
        self.key_file = Path.home() / ".pydiscobasepro" / "vault_key.key"

        self._cipher = None
        self._secrets: Dict[str, Dict[str, Any]] = {}

        self.initialize_vault()

    def initialize_vault(self):
        """Initialize the encrypted vault."""
        self._cipher = self._load_or_generate_key()
        self.load_secrets()

    def _load_or_generate_key(self) -> Fernet:
        """Load or generate encryption key."""
        if self.key_file.exists():
            key = self.key_file.read_bytes()
        else:
            # Generate new key with PBKDF2
            salt = secrets.token_bytes(16)
            password = os.environ.get("PYDISCOBASEPRO_VAULT_PASSWORD",
                                    secrets.token_hex(32)).encode()

            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                iterations=100000,
            )
            key = base64.urlsafe_b64encode(kdf.derive(password))

            # Store key and salt
            key_data = {
                "key": key.decode(),
                "salt": base64.b64encode(salt).decode()
            }
            self.key_file.write_text(json.dumps(key_data))
            self.key_file.chmod(0o600)

        return Fernet(key)

    def load_secrets(self):
        """Load encrypted secrets from vault."""
        if self.vault_file.exists():
            try:
                encrypted_data = self.vault_file.read_bytes()
                decrypted_data = self._cipher.decrypt(encrypted_data)
                self._secrets = json.loads(decrypted_data.decode())
            except Exception as e:
                logger.error(f"Failed to load secrets vault: {e}")
                self._secrets = {}
        else:
            self._secrets = {}

    def save_secrets(self):
        """Save encrypted secrets to vault."""
        try:
            secrets_json = json.dumps(self._secrets, default=str)
            encrypted_data = self._cipher.encrypt(secrets_json.encode())
            self.vault_file.write_bytes(encrypted_data)
            self.vault_file.chmod(0o600)
        except Exception as e:
            logger.error(f"Failed to save secrets vault: {e}")

    def store_secret(self, key: str, value: Any, metadata: Optional[Dict[str, Any]] = None) -> bool:
        """Store a secret in the vault."""
        try:
            secret_entry = {
                "value": value,
                "created": datetime.now().isoformat(),
                "updated": datetime.now().isoformat(),
                "metadata": metadata or {}
            }

            self._secrets[key] = secret_entry
            self.save_secrets()

            logger.info(f"Secret stored: {key}")
            return True

        except Exception as e:
            logger.error(f"Failed to store secret {key}: {e}")
            return False

    def retrieve_secret(self, key: str) -> Optional[Any]:
        """Retrieve a secret from the vault."""
        if key not in self._secrets:
            return None

        try:
            secret_entry = self._secrets[key]
            return secret_entry["value"]

        except Exception as e:
            logger.error(f"Failed to retrieve secret {key}: {e}")
            return None

    def update_secret(self, key: str, value: Any, metadata: Optional[Dict[str, Any]] = None) -> bool:
        """Update an existing secret."""
        if key not in self._secrets:
            return False

        try:
            secret_entry = self._secrets[key]
            secret_entry["value"] = value
            secret_entry["updated"] = datetime.now().isoformat()

            if metadata:
                secret_entry["metadata"].update(metadata)

            self.save_secrets()

            logger.info(f"Secret updated: {key}")
            return True

        except Exception as e:
            logger.error(f"Failed to update secret {key}: {e}")
            return False

    def delete_secret(self, key: str) -> bool:
        """Delete a secret from the vault."""
        if key not in self._secrets:
            return False

        try:
            del self._secrets[key]
            self.save_secrets()

            logger.info(f"Secret deleted: {key}")
            return True

        except Exception as e:
            logger.error(f"Failed to delete secret {key}: {e}")
            return False

    def list_secrets(self) -> Dict[str, Dict[str, Any]]:
        """List all secrets (without values)."""
        secrets_info = {}
        for key, secret_entry in self._secrets.items():
            secrets_info[key] = {
                "created": secret_entry["created"],
                "updated": secret_entry["updated"],
                "metadata": secret_entry["metadata"]
            }
        return secrets_info

    def rotate_vault_key(self) -> bool:
        """Rotate the vault encryption key."""
        try:
            # Generate new key
            new_cipher = Fernet(Fernet.generate_key())

            # Re-encrypt all secrets with new key
            secrets_json = json.dumps(self._secrets, default=str)
            new_encrypted_data = new_cipher.encrypt(secrets_json.encode())

            # Save with new key
            self._cipher = new_cipher
            self.vault_file.write_bytes(new_encrypted_data)

            # Update key file
            key_data = {
                "key": self._cipher._signing_key.decode(),
                "salt": secrets.token_hex(16)  # New salt
            }
            self.key_file.write_text(json.dumps(key_data))

            logger.info("Vault key rotated successfully")
            return True

        except Exception as e:
            logger.error(f"Failed to rotate vault key: {e}")
            return False

    def backup_vault(self, backup_path: Optional[Path] = None) -> bool:
        """Create a backup of the secrets vault."""
        if not backup_path:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = Path.home() / ".pydiscobasepro" / "backups" / f"vault_backup_{timestamp}.vault"

        backup_path.parent.mkdir(parents=True, exist_ok=True)

        try:
            # Copy encrypted vault file
            backup_path.write_bytes(self.vault_file.read_bytes())
            logger.info(f"Vault backup created: {backup_path}")
            return True

        except Exception as e:
            logger.error(f"Failed to backup vault: {e}")
            return False

    def restore_vault(self, backup_path: Path) -> bool:
        """Restore vault from backup."""
        if not backup_path.exists():
            logger.error(f"Backup file not found: {backup_path}")
            return False

        try:
            # Restore encrypted vault file
            self.vault_file.write_bytes(backup_path.read_bytes())
            self.load_secrets()

            logger.info(f"Vault restored from: {backup_path}")
            return True

        except Exception as e:
            logger.error(f"Failed to restore vault: {e}")
            return False

    def get_secret_metadata(self, key: str) -> Optional[Dict[str, Any]]:
        """Get metadata for a secret."""
        if key not in self._secrets:
            return None

        secret_entry = self._secrets[key]
        return {
            "created": secret_entry["created"],
            "updated": secret_entry["updated"],
            "metadata": secret_entry["metadata"]
        }

    def search_secrets(self, query: str) -> Dict[str, Dict[str, Any]]:
        """Search secrets by key or metadata."""
        results = {}

        for key, secret_entry in self._secrets.items():
            if query.lower() in key.lower():
                results[key] = self.get_secret_metadata(key)
                continue

            # Search in metadata
            metadata = secret_entry.get("metadata", {})
            if any(query.lower() in str(value).lower() for value in metadata.values()):
                results[key] = self.get_secret_metadata(key)

        return results