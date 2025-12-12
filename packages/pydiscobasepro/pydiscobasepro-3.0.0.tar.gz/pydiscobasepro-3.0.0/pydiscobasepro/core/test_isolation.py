"""
Test Environment Isolation

Isolated test environments for reliable testing.
"""

import tempfile
import os
from pathlib import Path
from typing import Dict, Any, Optional
import shutil

class TestEnvironmentIsolation:
    """Test environment isolation system."""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.enabled = config.get("enabled", True)

    def create_isolated_environment(self) -> Dict[str, Any]:
        """Create isolated test environment."""
        if not self.enabled:
            return {"status": "disabled"}

        # Create temporary directory
        temp_dir = Path(tempfile.mkdtemp(prefix="pydiscobasepro_test_"))

        # Copy necessary files
        source_dir = Path(".")
        for item in ["pydiscobasepro", "tests", "requirements.txt"]:
            src = source_dir / item
            dst = temp_dir / item
            if src.exists():
                if src.is_file():
                    shutil.copy2(src, dst)
                else:
                    shutil.copytree(src, dst, ignore=shutil.ignore_patterns('__pycache__', '.git'))

        # Set environment variables
        env = os.environ.copy()
        env["PYDISCOBASEPRO_TEST_MODE"] = "1"
        env["PYTHONPATH"] = str(temp_dir)

        return {
            "temp_dir": temp_dir,
            "env": env,
            "cleanup": lambda: shutil.rmtree(temp_dir, ignore_errors=True)
        }