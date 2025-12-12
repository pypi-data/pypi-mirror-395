"""
Signed Config Verification

Cryptographic verification of configuration files and data integrity.
"""

import hashlib
import json
from pathlib import Path
from typing import Dict, Any, Optional, Tuple
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.exceptions import InvalidSignature

from pydiscobasepro.core.logging import get_logger

logger = get_logger(__name__)

class SignedConfigVerifier:
    """Cryptographic verification of configuration files."""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.signatures_dir = Path.home() / ".pydiscobasepro" / "signatures"
        self.signatures_dir.mkdir(exist_ok=True)

        self.verification_enabled = config.get("enabled", True)
        self.key_store = None  # Will be injected

    def set_key_store(self, key_store):
        """Set the key store for signature verification."""
        self.key_store = key_store

    def sign_config(self, config_path: Path, key_name: str) -> bool:
        """Sign a configuration file."""
        if not self.key_store:
            logger.error("Key store not available for signing")
            return False

        try:
            # Read config file
            with open(config_path, 'rb') as f:
                config_data = f.read()

            # Calculate hash
            config_hash = hashlib.sha256(config_data).digest()

            # Sign hash
            signature = self.key_store.sign_data(key_name, config_hash)
            if not signature:
                logger.error(f"Failed to sign config with key {key_name}")
                return False

            # Save signature
            sig_file = self.signatures_dir / f"{config_path.name}.sig"
            with open(sig_file, 'wb') as f:
                f.write(signature)

            # Save metadata
            metadata = {
                "config_file": str(config_path),
                "signature_file": str(sig_file),
                "key_name": key_name,
                "signed_at": str(Path.cwd()),
                "config_hash": config_hash.hex()
            }

            metadata_file = self.signatures_dir / f"{config_path.name}.meta"
            with open(metadata_file, 'w') as f:
                json.dump(metadata, f, indent=2)

            logger.info(f"Config file signed: {config_path}")
            return True

        except Exception as e:
            logger.error(f"Failed to sign config {config_path}: {e}")
            return False

    def verify_config_signature(self, config_path: Path) -> Tuple[bool, Optional[str]]:
        """Verify the signature of a configuration file."""
        if not self.verification_enabled:
            return True, None

        if not self.key_store:
            return False, "Key store not available"

        try:
            # Read config file
            with open(config_path, 'rb') as f:
                config_data = f.read()

            # Calculate current hash
            current_hash = hashlib.sha256(config_data).digest()

            # Load metadata
            metadata_file = self.signatures_dir / f"{config_path.name}.meta"
            if not metadata_file.exists():
                return False, "No signature metadata found"

            with open(metadata_file, 'r') as f:
                metadata = json.load(f)

            # Check if hash matches
            stored_hash = bytes.fromhex(metadata["config_hash"])
            if current_hash != stored_hash:
                return False, "Configuration file has been modified"

            # Load signature
            sig_file = self.signatures_dir / f"{config_path.name}.sig"
            if not sig_file.exists():
                return False, "Signature file not found"

            with open(sig_file, 'rb') as f:
                signature = f.read()

            # Verify signature
            key_name = metadata["key_name"]
            is_valid = self.key_store.verify_signature(key_name, stored_hash, signature)

            if is_valid:
                return True, None
            else:
                return False, "Signature verification failed"

        except Exception as e:
            logger.error(f"Signature verification failed for {config_path}: {e}")
            return False, str(e)

    def sign_config_data(self, config_data: Dict[str, Any], key_name: str) -> Optional[bytes]:
        """Sign configuration data in memory."""
        if not self.key_store:
            return None

        try:
            # Serialize config
            config_json = json.dumps(config_data, sort_keys=True)
            config_bytes = config_json.encode()

            # Calculate hash
            config_hash = hashlib.sha256(config_bytes).digest()

            # Sign hash
            signature = self.key_store.sign_data(key_name, config_hash)
            return signature

        except Exception as e:
            logger.error(f"Failed to sign config data: {e}")
            return None

    def verify_config_data_signature(self, config_data: Dict[str, Any], signature: bytes, key_name: str) -> bool:
        """Verify signature of configuration data."""
        if not self.verification_enabled or not self.key_store:
            return True

        try:
            # Serialize config the same way
            config_json = json.dumps(config_data, sort_keys=True)
            config_bytes = config_json.encode()

            # Calculate hash
            config_hash = hashlib.sha256(config_bytes).digest()

            # Verify signature
            return self.key_store.verify_signature(key_name, config_hash, signature)

        except Exception as e:
            logger.error(f"Config data signature verification failed: {e}")
            return False

    def get_signature_info(self, config_path: Path) -> Optional[Dict[str, Any]]:
        """Get signature information for a config file."""
        metadata_file = self.signatures_dir / f"{config_path.name}.meta"
        if not metadata_file.exists():
            return None

        try:
            with open(metadata_file, 'r') as f:
                metadata = json.load(f)

            # Add verification status
            is_valid, error = self.verify_config_signature(config_path)
            metadata["verification_status"] = "valid" if is_valid else "invalid"
            metadata["verification_error"] = error

            return metadata

        except Exception as e:
            logger.error(f"Failed to read signature info for {config_path}: {e}")
            return None

    def list_signed_configs(self) -> Dict[str, Dict[str, Any]]:
        """List all signed configuration files."""
        signed_configs = {}

        for metadata_file in self.signatures_dir.glob("*.meta"):
            try:
                with open(metadata_file, 'r') as f:
                    metadata = json.load(f)

                config_name = metadata_file.stem
                signed_configs[config_name] = metadata

            except Exception as e:
                logger.error(f"Failed to read metadata {metadata_file}: {e}")

        return signed_configs

    def remove_signature(self, config_path: Path) -> bool:
        """Remove signature for a configuration file."""
        try:
            sig_file = self.signatures_dir / f"{config_path.name}.sig"
            meta_file = self.signatures_dir / f"{config_path.name}.meta"

            sig_file.unlink(missing_ok=True)
            meta_file.unlink(missing_ok=True)

            logger.info(f"Signature removed for: {config_path}")
            return True

        except Exception as e:
            logger.error(f"Failed to remove signature for {config_path}: {e}")
            return False

    def verify_all_configs(self) -> Dict[str, Tuple[bool, Optional[str]]]:
        """Verify signatures of all signed configuration files."""
        results = {}
        signed_configs = self.list_signed_configs()

        for config_name, metadata in signed_configs.items():
            config_path = Path(metadata["config_file"])
            is_valid, error = self.verify_config_signature(config_path)
            results[config_name] = (is_valid, error)

        return results

    def enable_verification(self):
        """Enable signature verification."""
        self.verification_enabled = True
        logger.info("Config signature verification enabled")

    def disable_verification(self):
        """Disable signature verification."""
        self.verification_enabled = False
        logger.info("Config signature verification disabled")

    def get_verification_stats(self) -> Dict[str, Any]:
        """Get verification statistics."""
        signed_configs = self.list_signed_configs()
        verification_results = self.verify_all_configs()

        valid_count = sum(1 for valid, _ in verification_results.values() if valid)
        invalid_count = len(verification_results) - valid_count

        return {
            "verification_enabled": self.verification_enabled,
            "total_signed_configs": len(signed_configs),
            "valid_signatures": valid_count,
            "invalid_signatures": invalid_count,
            "verification_results": verification_results
        }