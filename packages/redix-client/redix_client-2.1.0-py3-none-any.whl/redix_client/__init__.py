# redix_client/__init__.py
"""
Redix Universal Healthcare Conversion API - Python Client

A thin client that works with any API endpoint without requiring SDK updates.
"""

from .client import RedixClient
from .exceptions import RedixAPIError

__version__ = "2.1.0"
__all__ = ["RedixClient", "RedixAPIError"]
