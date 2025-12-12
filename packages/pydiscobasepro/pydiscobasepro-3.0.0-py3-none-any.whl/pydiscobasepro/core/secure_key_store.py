"""
Secure Key Store

Hardware Security Module (HSM) integration and secure key management.
"""

import os
import secrets
from pathlib import Path
from typing import Dict, Any, Optional, List
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization
from cryptography.fernet import Fernet
import base64

from pydiscobasepro.core.logging import get_logger

logger = get_logger(__name__)

class SecureKeyStore:
    """Secure key store with HSM-like functionality."""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.keys_dir = Path.home() / ".pydiscobasepro" / "keys"
        self.keys_dir.mkdir(exist_ok=True, parents=True)

        self.master_key_file = self.keys_dir / "master.key"
        self.key_metadata_file = self.keys_dir / "key_metadata.json"

        # Key storage
        self.keys: Dict[str, Dict[str, Any]] = {}
        self.master_key = None

        # Initialize
        self._load_master_key()
        self._load_key_metadata()

    def _load_master_key(self):
        """Load or generate master encryption key."""
        if self.master_key_file.exists():
            try:
                encrypted_key = self.master_key_file.read_bytes()
                # In a real HSM, this would be protected by hardware
                # For simulation, we'll use environment variable
                password = os.environ.get("PYDISCOBASEPRO_MASTER_PASSWORD", "default_master_password")
                salt = encrypted_key[:16]
                key = self._derive_key(password.encode(), salt)
                fernet = Fernet(key)
                self.master_key = fernet.decrypt(encrypted_key[16:])
            except Exception as e:
                logger.error(f"Failed to load master key: {e}")
                self._generate_master_key()
        else:
            self._generate_master_key()

    def _generate_master_key(self):
        """Generate new master key."""
        self.master_key = secrets.token_bytes(32)

        # Encrypt and store
        password = os.environ.get("PYDISCOBASEPRO_MASTER_PASSWORD", "default_master_password")
        salt = secrets.token_bytes(16)
        key = self._derive_key(password.encode(), salt)

        fernet = Fernet(key)
        encrypted_key = salt + fernet.encrypt(self.master_key)

        self.master_key_file.write_bytes(encrypted_key)
        self.master_key_file.chmod(0o600)

        logger.info("New master key generated")

    def _derive_key(self, password: bytes, salt: bytes) -> bytes:
        """Derive encryption key from password."""
        from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        return base64.urlsafe_b64encode(kdf.derive(password))

    def _load_key_metadata(self):
        """Load key metadata."""
        if self.key_metadata_file.exists():
            try:
                with open(self.key_metadata_file, 'r') as f:
                    self.keys = json.load(f)
            except Exception as e:
                logger.error(f"Failed to load key metadata: {e}")
                self.keys = {}

    def _save_key_metadata(self):
        """Save key metadata."""
        try:
            with open(self.key_metadata_file, 'w') as f:
                json.dump(self.keys, f, indent=2, default=str)
        except Exception as e:
            logger.error(f"Failed to save key metadata: {e}")

    def generate_key_pair(self, key_name: str, key_size: int = 2048) -> bool:
        """Generate RSA key pair."""
        try:
            # Generate private key
            private_key = rsa.generate_private_key(
                public_exponent=65537,
                key_size=key_size
            )

            # Serialize private key
            private_pem = private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            )

            # Generate public key
            public_key = private_key.public_key()
            public_pem = public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )

            # Encrypt and store
            encrypted_private = self._encrypt_data(private_pem)
            encrypted_public = self._encrypt_data(public_pem)

            private_file = self.keys_dir / f"{key_name}_private.pem.enc"
            public_file = self.keys_dir / f"{key_name}_public.pem.enc"

            private_file.write_bytes(encrypted_private)
            public_file.write_bytes(encrypted_public)

            # Store metadata
            self.keys[key_name] = {
                "type": "rsa_key_pair",
                "key_size": key_size,
                "created": str(Path.cwd()),
                "private_file": str(private_file),
                "public_file": str(public_file)
            }

            self._save_key_metadata()
            logger.info(f"RSA key pair generated: {key_name}")

            return True

        except Exception as e:
            logger.error(f"Failed to generate key pair {key_name}: {e}")
            return False

    def generate_symmetric_key(self, key_name: str, key_length: int = 32) -> bool:
        """Generate symmetric encryption key."""
        try:
            key = secrets.token_bytes(key_length)
            encrypted_key = self._encrypt_data(key)

            key_file = self.keys_dir / f"{key_name}.key.enc"
            key_file.write_bytes(encrypted_key)

            # Store metadata
            self.keys[key_name] = {
                "type": "symmetric_key",
                "key_length": key_length,
                "created": str(Path.cwd()),
                "file": str(key_file)
            }

            self._save_key_metadata()
            logger.info(f"Symmetric key generated: {key_name}")

            return True

        except Exception as e:
            logger.error(f"Failed to generate symmetric key {key_name}: {e}")
            return False

    def get_private_key(self, key_name: str) -> Optional[rsa.RSAPrivateKey]:
        """Retrieve and decrypt private key."""
        if key_name not in self.keys or self.keys[key_name]["type"] != "rsa_key_pair":
            return None

        try:
            private_file = Path(self.keys[key_name]["private_file"])
            encrypted_data = private_file.read_bytes()
            decrypted_data = self._decrypt_data(encrypted_data)

            private_key = serialization.load_pem_private_key(
                decrypted_data,
                password=None
            )

            return private_key

        except Exception as e:
            logger.error(f"Failed to load private key {key_name}: {e}")
            return None

    def get_public_key(self, key_name: str) -> Optional[rsa.RSAPublicKey]:
        """Retrieve and decrypt public key."""
        if key_name not in self.keys or self.keys[key_name]["type"] != "rsa_key_pair":
            return None

        try:
            public_file = Path(self.keys[key_name]["public_file"])
            encrypted_data = public_file.read_bytes()
            decrypted_data = self._decrypt_data(encrypted_data)

            public_key = serialization.load_pem_public_key(decrypted_data)
            return public_key

        except Exception as e:
            logger.error(f"Failed to load public key {key_name}: {e}")
            return None

    def get_symmetric_key(self, key_name: str) -> Optional[bytes]:
        """Retrieve and decrypt symmetric key."""
        if key_name not in self.keys or self.keys[key_name]["type"] != "symmetric_key":
            return None

        try:
            key_file = Path(self.keys[key_name]["file"])
            encrypted_data = key_file.read_bytes()
            decrypted_data = self._decrypt_data(encrypted_data)

            return decrypted_data

        except Exception as e:
            logger.error(f"Failed to load symmetric key {key_name}: {e}")
            return None

    def sign_data(self, key_name: str, data: bytes) -> Optional[bytes]:
        """Sign data with private key."""
        private_key = self.get_private_key(key_name)
        if not private_key:
            return None

        try:
            signature = private_key.sign(
                data,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            return signature

        except Exception as e:
            logger.error(f"Failed to sign data with {key_name}: {e}")
            return None

    def verify_signature(self, key_name: str, data: bytes, signature: bytes) -> bool:
        """Verify signature with public key."""
        public_key = self.get_public_key(key_name)
        if not public_key:
            return False

        try:
            public_key.verify(
                signature,
                data,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            return True

        except Exception:
            return False

    def encrypt_data(self, key_name: str, data: bytes) -> Optional[bytes]:
        """Encrypt data with symmetric key."""
        key = self.get_symmetric_key(key_name)
        if not key:
            return None

        try:
            fernet = Fernet(base64.urlsafe_b64encode(key))
            return fernet.encrypt(data)

        except Exception as e:
            logger.error(f"Failed to encrypt data with {key_name}: {e}")
            return None

    def decrypt_data(self, key_name: str, encrypted_data: bytes) -> Optional[bytes]:
        """Decrypt data with symmetric key."""
        key = self.get_symmetric_key(key_name)
        if not key:
            return None

        try:
            fernet = Fernet(base64.urlsafe_b64encode(key))
            return fernet.decrypt(encrypted_data)

        except Exception as e:
            logger.error(f"Failed to decrypt data with {key_name}: {e}")
            return None

    def _encrypt_data(self, data: bytes) -> bytes:
        """Encrypt data with master key."""
        fernet = Fernet(base64.urlsafe_b64encode(self.master_key))
        return fernet.encrypt(data)

    def _decrypt_data(self, encrypted_data: bytes) -> bytes:
        """Decrypt data with master key."""
        fernet = Fernet(base64.urlsafe_b64encode(self.master_key))
        return fernet.decrypt(encrypted_data)

    def list_keys(self) -> Dict[str, Dict[str, Any]]:
        """List all stored keys."""
        return self.keys.copy()

    def delete_key(self, key_name: str) -> bool:
        """Delete a key and its files."""
        if key_name not in self.keys:
            return False

        try:
            key_info = self.keys[key_name]

            # Delete files
            if key_info["type"] == "rsa_key_pair":
                Path(key_info["private_file"]).unlink(missing_ok=True)
                Path(key_info["public_file"]).unlink(missing_ok=True)
            elif key_info["type"] == "symmetric_key":
                Path(key_info["file"]).unlink(missing_ok=True)

            # Remove from metadata
            del self.keys[key_name]
            self._save_key_metadata()

            logger.info(f"Key deleted: {key_name}")
            return True

        except Exception as e:
            logger.error(f"Failed to delete key {key_name}: {e}")
            return False

    def rotate_key(self, key_name: str) -> bool:
        """Rotate a key (generate new version)."""
        if key_name not in self.keys:
            return False

        key_info = self.keys[key_name]

        try:
            if key_info["type"] == "rsa_key_pair":
                # Generate new key pair
                old_private = self.get_private_key(key_name)
                old_public = self.get_public_key(key_name)

                # Generate new pair
                self.generate_key_pair(key_name, key_info["key_size"])

                logger.info(f"RSA key pair rotated: {key_name}")

            elif key_info["type"] == "symmetric_key":
                # Generate new symmetric key
                old_key = self.get_symmetric_key(key_name)

                # Generate new key
                self.generate_symmetric_key(key_name, key_info["key_length"])

                logger.info(f"Symmetric key rotated: {key_name}")

            return True

        except Exception as e:
            logger.error(f"Failed to rotate key {key_name}: {e}")
            return False

    def get_key_info(self, key_name: str) -> Optional[Dict[str, Any]]:
        """Get detailed information about a key."""
        return self.keys.get(key_name)