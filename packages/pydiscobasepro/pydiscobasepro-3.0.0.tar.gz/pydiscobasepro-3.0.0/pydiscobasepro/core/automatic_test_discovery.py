"""
Automatic Test Discovery

Automatic discovery and execution of tests.
"""

import unittest
import pytest
from pathlib import Path
from typing import Dict, Any, List, Optional
import importlib.util
import inspect

class AutomaticTestDiscovery:
    """Automatic test discovery and execution system."""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.enabled = config.get("enabled", True)
        self.test_dirs = config.get("test_dirs", ["tests", "test"])
        self.patterns = config.get("patterns", ["test_*.py", "*_test.py"])

    def discover_tests(self) -> List[str]:
        """Discover all test files."""
        if not self.enabled:
            return []

        test_files = []

        for test_dir in self.test_dirs:
            dir_path = Path(test_dir)
            if dir_path.exists():
                for pattern in self.patterns:
                    test_files.extend(dir_path.glob(pattern))

        return [str(f) for f in test_files]

    def run_discovered_tests(self) -> Dict[str, Any]:
        """Run all discovered tests."""
        test_files = self.discover_tests()

        if not test_files:
            return {"status": "no_tests_found"}

        # Use pytest for running tests
        import subprocess
        import sys

        cmd = [sys.executable, "-m", "pytest"] + test_files + ["-v", "--tb=short"]
        result = subprocess.run(cmd, capture_output=True, text=True)

        return {
            "status": "completed",
            "return_code": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "test_files": test_files
        }