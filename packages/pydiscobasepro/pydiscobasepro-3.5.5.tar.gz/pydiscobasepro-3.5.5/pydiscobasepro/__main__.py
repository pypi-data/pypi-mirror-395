#!/usr/bin/env python3
"""
PyDiscoBasePro v3.0.0 - Enterprise-Grade Discord Bot Framework

Main entry point that delegates to the advanced CLI system.
"""

import sys
from pydiscobasepro.cli.app import create_cli_app

def main():
    """Main entry point for PyDiscoBasePro v3.0.0."""
    app = create_cli_app()
    app()

if __name__ == "__main__":
    main()