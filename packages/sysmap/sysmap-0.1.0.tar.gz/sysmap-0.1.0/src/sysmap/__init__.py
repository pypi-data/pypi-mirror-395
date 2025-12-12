"""
SysMap - A comprehensive system inventory tool.

Track installed software, versions, and configurations across multiple platforms.
"""

__version__ = "0.1.0"
__author__ = "Lorenzo Uriel"
__license__ = "MIT"

from .core.scanner import SystemScanner
from .core.config import Config

__all__ = ["SystemScanner", "Config"]
