"""
CI/CD Pipeline Templates

GitHub Actions and GitLab CI templates.
"""

from typing import Dict, Any
from pathlib import Path

class CICDPipelineTemplates:
    """CI/CD pipeline templates for different platforms."""

    def __init__(self, config: Dict[str, Any]):
        self.config = config

    def generate_github_actions(self) -> str:
        """Generate GitHub Actions workflow."""
        return """
name: PyDiscoBasePro CI/CD

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.9, 3.10, 3.11]

    steps:
    - uses: actions/checkout@v3
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install pytest pytest-cov
    - name: Run tests
      run: pytest --cov=pydiscobasepro --cov-report=xml
    - name: Upload coverage
      uses: codecov/codecov-action@v3

  lint:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    - name: Install linting tools
      run: pip install flake8 black isort
    - name: Run linting
      run: |
        flake8 pydiscobasepro --count --select=E9,F63,F7,F82 --show-source --statistics
        black --check pydiscobasepro
        isort --check-only pydiscobasepro
"""

    def generate_gitlab_ci(self) -> str:
        """Generate GitLab CI pipeline."""
        return """
stages:
  - test
  - deploy

test:
  stage: test
  image: python:3.11
  before_script:
    - pip install -r requirements.txt
    - pip install pytest pytest-cov
  script:
    - pytest --cov=pydiscobasepro --cov-report=xml
  coverage: '/(?i)total.*? (100(?:\.0+)?\%|[1-9]?\d(?:\.\d+)?\%)$/'
  artifacts:
    reports:
      coverage_report:
        coverage_format: cobertura
        path: coverage.xml

deploy:
  stage: deploy
  image: python:3.11
  script:
    - echo "Deploying to production..."
  only:
    - main
"""

    def save_templates(self, output_dir: Path):
        """Save pipeline templates to files."""
        output_dir.mkdir(exist_ok=True)

        # GitHub Actions
        github_file = output_dir / ".github" / "workflows" / "ci.yml"
        github_file.parent.mkdir(parents=True, exist_ok=True)
        github_file.write_text(self.generate_github_actions())

        # GitLab CI
        gitlab_file = output_dir / ".gitlab-ci.yml"
        gitlab_file.write_text(self.generate_gitlab_ci())