"""
Token-based Authentication System

JWT token management with refresh tokens and secure storage.
"""

import jwt
import secrets
from datetime import datetime, timedelta
from typing import Dict, Optional, Any, Tuple
import bcrypt
from cryptography.fernet import Fernet
from pathlib import Path

from pydiscobasepro.core.logging import get_logger

logger = get_logger(__name__)

class TokenAuth:
    """Token-based authentication with JWT and refresh tokens."""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.secret_key = self._load_or_generate_secret()
        self.encryption_key = self._load_or_generate_encryption_key()
        self.cipher = Fernet(self.encryption_key)

        self.tokens_file = Path.home() / ".pydiscobasepro" / "tokens.enc"
        self.refresh_tokens: Dict[str, Dict[str, Any]] = {}

        self.token_expiry = config.get("token_expiry", 3600)  # 1 hour
        self.refresh_token_expiry = config.get("refresh_token_expiry", 604800)  # 7 days

        self.load_refresh_tokens()

    def _load_or_generate_secret(self) -> str:
        """Load or generate JWT secret key."""
        secret_file = Path.home() / ".pydiscobasepro" / "jwt_secret.key"
        if secret_file.exists():
            return secret_file.read_text().strip()
        else:
            secret = secrets.token_hex(32)
            secret_file.write_text(secret)
            secret_file.chmod(0o600)
            return secret

    def _load_or_generate_encryption_key(self) -> bytes:
        """Load or generate encryption key."""
        key_file = Path.home() / ".pydiscobasepro" / "token_encryption.key"
        if key_file.exists():
            return key_file.read_bytes()
        else:
            key = Fernet.generate_key()
            key_file.write_bytes(key)
            key_file.chmod(0o600)
            return key

    def load_refresh_tokens(self):
        """Load encrypted refresh tokens."""
        if self.tokens_file.exists():
            try:
                encrypted_data = self.tokens_file.read_bytes()
                decrypted_data = self.cipher.decrypt(encrypted_data)
                self.refresh_tokens = jwt.decode(decrypted_data, options={"verify_signature": False})
            except Exception as e:
                logger.error(f"Failed to load refresh tokens: {e}")
                self.refresh_tokens = {}

    def save_refresh_tokens(self):
        """Save encrypted refresh tokens."""
        try:
            tokens_json = jwt.encode(self.refresh_tokens, "secret", algorithm="HS256")
            encrypted_data = self.cipher.encrypt(tokens_json.encode())
            self.tokens_file.write_bytes(encrypted_data)
        except Exception as e:
            logger.error(f"Failed to save refresh tokens: {e}")

    def generate_access_token(self, user_id: str, roles: Optional[list] = None) -> str:
        """Generate JWT access token."""
        now = datetime.utcnow()
        payload = {
            "user_id": user_id,
            "roles": roles or [],
            "type": "access",
            "iat": now,
            "exp": now + timedelta(seconds=self.token_expiry)
        }

        token = jwt.encode(payload, self.secret_key, algorithm="HS256")
        return token

    def generate_refresh_token(self, user_id: str) -> str:
        """Generate refresh token."""
        token_id = secrets.token_hex(16)
        now = datetime.utcnow()

        refresh_token = {
            "token_id": token_id,
            "user_id": user_id,
            "created": now.isoformat(),
            "expires": (now + timedelta(seconds=self.refresh_token_expiry)).isoformat()
        }

        self.refresh_tokens[token_id] = refresh_token
        self.save_refresh_tokens()

        return token_id

    def validate_access_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Validate JWT access token."""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=["HS256"])

            if payload.get("type") != "access":
                return None

            return payload

        except jwt.ExpiredSignatureError:
            logger.warning("Access token expired")
            return None
        except jwt.InvalidTokenError:
            logger.warning("Invalid access token")
            return None
        except Exception as e:
            logger.error(f"Token validation error: {e}")
            return None

    def validate_refresh_token(self, refresh_token: str) -> Optional[str]:
        """Validate refresh token and return user_id."""
        if refresh_token not in self.refresh_tokens:
            return None

        token_data = self.refresh_tokens[refresh_token]
        expires = datetime.fromisoformat(token_data["expires"])

        if datetime.utcnow() > expires:
            # Token expired, remove it
            del self.refresh_tokens[refresh_token]
            self.save_refresh_tokens()
            return None

        return token_data["user_id"]

    def refresh_access_token(self, refresh_token: str) -> Optional[Tuple[str, str]]:
        """Refresh access token using refresh token."""
        user_id = self.validate_refresh_token(refresh_token)
        if not user_id:
            return None

        # Generate new tokens
        new_access_token = self.generate_access_token(user_id)
        new_refresh_token = self.generate_refresh_token(user_id)

        # Remove old refresh token
        del self.refresh_tokens[refresh_token]
        self.save_refresh_tokens()

        return new_access_token, new_refresh_token

    def revoke_refresh_token(self, refresh_token: str):
        """Revoke a refresh token."""
        if refresh_token in self.refresh_tokens:
            del self.refresh_tokens[refresh_token]
            self.save_refresh_tokens()
            logger.info(f"Refresh token revoked: {refresh_token}")

    def revoke_all_user_tokens(self, user_id: str):
        """Revoke all refresh tokens for a user."""
        tokens_to_remove = [
            token_id for token_id, token_data in self.refresh_tokens.items()
            if token_data["user_id"] == user_id
        ]

        for token_id in tokens_to_remove:
            del self.refresh_tokens[token_id]

        self.save_refresh_tokens()
        logger.info(f"All tokens revoked for user: {user_id}")

    def get_token_info(self, token: str) -> Optional[Dict[str, Any]]:
        """Get information about a token without validating."""
        try:
            # Decode without verification for info purposes
            payload = jwt.decode(token, options={"verify_signature": False})
            return payload
        except Exception:
            return None

    def list_user_tokens(self, user_id: str) -> List[Dict[str, Any]]:
        """List all active refresh tokens for a user."""
        user_tokens = []
        for token_data in self.refresh_tokens.values():
            if token_data["user_id"] == user_id:
                user_tokens.append({
                    "token_id": token_data["token_id"],
                    "created": token_data["created"],
                    "expires": token_data["expires"]
                })
        return user_tokens

    def cleanup_expired_tokens(self):
        """Clean up expired refresh tokens."""
        now = datetime.utcnow()
        expired_tokens = []

        for token_id, token_data in self.refresh_tokens.items():
            expires = datetime.fromisoformat(token_data["expires"])
            if now > expires:
                expired_tokens.append(token_id)

        for token_id in expired_tokens:
            del self.refresh_tokens[token_id]

        if expired_tokens:
            self.save_refresh_tokens()
            logger.info(f"Cleaned up {len(expired_tokens)} expired tokens")

    def authenticate_with_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Authenticate user with access token."""
        payload = self.validate_access_token(token)
        if payload:
            return {
                "user_id": payload["user_id"],
                "roles": payload.get("roles", []),
                "authenticated": True
            }
        return None