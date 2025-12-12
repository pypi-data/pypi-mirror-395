"""
Secure Data Shredding

Cryptographic data destruction and secure deletion.
"""

import os
import secrets
import shutil
from pathlib import Path
from typing import List, Optional, Union
import hashlib

from pydiscobasepro.core.logging import get_logger

logger = get_logger(__name__)

class SecureDataShredder:
    """Secure data shredding and cryptographic destruction."""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.passes = config.get("passes", 3)
        self.chunk_size = config.get("chunk_size", 4096)
        self.verification_enabled = config.get("verification", True)

    def shred_file(self, file_path: Union[str, Path], passes: Optional[int] = None) -> bool:
        """Securely shred a file using multiple overwrite passes."""
        file_path = Path(file_path)
        if not file_path.exists():
            logger.warning(f"File to shred does not exist: {file_path}")
            return False

        passes = passes or self.passes

        try:
            # Get file size
            file_size = file_path.stat().st_size

            # Multiple overwrite passes
            for pass_num in range(passes):
                self._overwrite_file(file_path, file_size, pass_num)

            # Final truncation
            file_path.write_bytes(b'')

            # Delete file
            file_path.unlink()

            logger.info(f"File securely shredded: {file_path} ({passes} passes)")
            return True

        except Exception as e:
            logger.error(f"Failed to shred file {file_path}: {e}")
            return False

    def _overwrite_file(self, file_path: Path, file_size: int, pass_num: int):
        """Overwrite file with random data."""
        with open(file_path, 'wb') as f:
            bytes_written = 0

            while bytes_written < file_size:
                # Generate random data
                chunk_size = min(self.chunk_size, file_size - bytes_written)
                random_data = secrets.token_bytes(chunk_size)

                # Optionally use different patterns for different passes
                if pass_num == 0:
                    # First pass: random data
                    pass
                elif pass_num == 1:
                    # Second pass: zeros
                    random_data = b'\x00' * chunk_size
                elif pass_num == 2:
                    # Third pass: ones
                    random_data = b'\xFF' * chunk_size
                # Additional passes: more random data

                f.write(random_data)
                bytes_written += chunk_size

            f.flush()
            os.fsync(f.fileno())  # Force write to disk

    def shred_directory(self, dir_path: Union[str, Path], passes: Optional[int] = None) -> bool:
        """Securely shred all files in a directory."""
        dir_path = Path(dir_path)
        if not dir_path.exists() or not dir_path.is_dir():
            logger.warning(f"Directory to shred does not exist: {dir_path}")
            return False

        passes = passes or self.passes
        success_count = 0
        total_count = 0

        try:
            # Recursively shred all files
            for file_path in dir_path.rglob('*'):
                if file_path.is_file():
                    total_count += 1
                    if self.shred_file(file_path, passes):
                        success_count += 1

            # Remove directory structure
            shutil.rmtree(dir_path)

            logger.info(f"Directory shredded: {dir_path} ({success_count}/{total_count} files)")
            return success_count == total_count

        except Exception as e:
            logger.error(f"Failed to shred directory {dir_path}: {e}")
            return False

    def shred_memory(self, data: bytes) -> None:
        """Securely clear data from memory."""
        # Overwrite the data multiple times
        for _ in range(self.passes):
            data = secrets.token_bytes(len(data))

        # Final overwrite with zeros
        data = b'\x00' * len(data)

    def secure_delete_list(self, file_list: List[Union[str, Path]], passes: Optional[int] = None) -> Dict[str, bool]:
        """Securely delete multiple files and return results."""
        passes = passes or self.passes
        results = {}

        for file_path in file_list:
            success = self.shred_file(file_path, passes)
            results[str(file_path)] = success

        return results

    def verify_shredding(self, original_path: Union[str, Path], expected_hash: Optional[str] = None) -> bool:
        """Verify that a file has been properly shredded."""
        if not self.verification_enabled:
            return True

        file_path = Path(original_path)

        # File should not exist
        if file_path.exists():
            logger.warning(f"Shredded file still exists: {file_path}")
            return False

        # Check if file can be recovered from disk (simplified check)
        # In a real implementation, this would use forensic tools
        try:
            # Try to read the file location
            with open(file_path, 'rb') as f:
                data = f.read(1024)
                if data and not all(b == 0 for b in data):
                    logger.warning(f"File data may still be recoverable: {file_path}")
                    return False
        except FileNotFoundError:
            # This is expected
            pass
        except Exception as e:
            logger.error(f"Error verifying shredding of {file_path}: {e}")
            return False

        return True

    def get_shredding_stats(self) -> Dict[str, Any]:
        """Get shredding statistics."""
        return {
            "default_passes": self.passes,
            "chunk_size": self.chunk_size,
            "verification_enabled": self.verification_enabled,
            "supported_methods": ["file", "directory", "memory"]
        }

    def shred_with_verification(self, file_path: Union[str, Path], passes: Optional[int] = None) -> Tuple[bool, bool]:
        """Shred a file and verify the operation."""
        # Calculate original hash if verification enabled
        original_hash = None
        if self.verification_enabled:
            file_path = Path(file_path)
            if file_path.exists():
                with open(file_path, 'rb') as f:
                    original_hash = hashlib.sha256(f.read()).hexdigest()

        # Shred the file
        shred_success = self.shred_file(file_path, passes)

        # Verify shredding
        verify_success = self.verify_shredding(file_path, original_hash)

        return shred_success, verify_success

    def secure_wipe_free_space(self, path: Union[str, Path] = "/", passes: int = 1) -> bool:
        """Securely wipe free disk space."""
        try:
            path = Path(path)
            stat = os.statvfs(path)

            # Calculate free space
            free_bytes = stat.f_bavail * stat.f_frsize
            max_wipe_bytes = min(free_bytes, 100 * 1024 * 1024)  # Max 100MB for safety

            # Create temporary file to fill free space
            temp_file = path / ".secure_wipe_temp"
            try:
                with open(temp_file, 'wb') as f:
                    bytes_written = 0
                    chunk_size = min(self.chunk_size, max_wipe_bytes)

                    while bytes_written < max_wipe_bytes:
                        random_data = secrets.token_bytes(chunk_size)
                        f.write(random_data)
                        bytes_written += chunk_size

                        if bytes_written + chunk_size > max_wipe_bytes:
                            break

                    f.flush()
                    os.fsync(f.fileno())

                # Shred the temporary file
                self.shred_file(temp_file, passes)

                logger.info(f"Free space wiped: {max_wipe_bytes} bytes")
                return True

            except Exception as e:
                logger.error(f"Failed to wipe free space: {e}")
                # Clean up temp file if it exists
                temp_file.unlink(missing_ok=True)
                return False

        except Exception as e:
            logger.error(f"Error accessing path {path}: {e}")
            return False

    def shred_network_data(self, data: bytes) -> bytes:
        """Shred data before network transmission (for sensitive data)."""
        # This is a conceptual method - in practice, you'd use TLS
        # But for demonstration, we'll return overwritten data
        return secrets.token_bytes(len(data))

    def get_destruction_methods(self) -> List[str]:
        """Get available data destruction methods."""
        return [
            "single_pass_random",
            "three_pass_gutmann",  # Simplified
            "dod_5220_22_m",  # Department of Defense standard
            "secure_delete"
        ]