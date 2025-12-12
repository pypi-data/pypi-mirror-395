"""
Coverage Report Generator

Code coverage analysis and reporting.
"""

import coverage
import subprocess
import sys
from pathlib import Path
from typing import Dict, Any, Optional

class CoverageReportGenerator:
    """Code coverage analysis and reporting."""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.enabled = config.get("enabled", True)
        self.source_dirs = config.get("source_dirs", ["pydiscobasepro"])
        self.output_dir = Path(config.get("output_dir", "coverage_reports"))

    def generate_coverage_report(self) -> Dict[str, Any]:
        """Generate coverage report."""
        if not self.enabled:
            return {"status": "disabled"}

        # Run coverage
        cov = coverage.Coverage(source=self.source_dirs)
        cov.start()

        # Run tests
        result = subprocess.run([
            sys.executable, "-m", "pytest", "tests/", "-v"
        ], capture_output=True, text=True)

        cov.stop()
        cov.save()

        # Generate reports
        self.output_dir.mkdir(exist_ok=True)

        # HTML report
        html_report = self.output_dir / "htmlcov" / "index.html"
        cov.html_report(directory=str(self.output_dir / "htmlcov"))

        # XML report
        xml_report = self.output_dir / "coverage.xml"
        cov.xml_report(outfile=str(xml_report))

        # Text report
        text_report = self.output_dir / "coverage.txt"
        with open(text_report, 'w') as f:
            cov.report(file=f)

        return {
            "status": "completed",
            "test_result": result.returncode,
            "html_report": str(html_report),
            "xml_report": str(xml_report),
            "text_report": str(text_report)
        }