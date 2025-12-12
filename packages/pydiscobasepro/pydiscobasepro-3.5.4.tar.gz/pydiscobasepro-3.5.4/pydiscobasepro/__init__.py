"""
PyDiscoBasePro - Enterprise-Grade Discord Bot Framework

A comprehensive framework for building advanced Discord bots with enterprise features.
"""

__version__ = "3.5.4"
__author__ = "PyDiscoBasePro Team"
__description__ = "Enterprise-Grade Discord Bot Framework"
__url__ = "https://github.com/code-xon/pydiscobasepro"

# Import main components for easy access
try:
    from .core import PyDiscoBasePro
except ImportError:
    # Core not available in CLI-only installations
    pass