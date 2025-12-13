"""
Overcast SDK for Python
Simple incident detection and monitoring for your applications.

Usage:
    from overcast import Overcast
    
    overcast = Overcast(api_key="your_api_key")
    overcast.error("Database connection failed", service="user-service")
"""

from .client import OvercastClient
from .exceptions import OvercastError, OvercastAuthError, OvercastConnectionError
# Import handler lazily or just expose module? 
# Exposing module is safer to avoid circular imports if any, but handler depends on client, client doesn't depend on handler.
from .logging import OvercastHandler

__version__ = "1.0.1"
__all__ = ["OvercastClient", "OvercastHandler", "OvercastError", "OvercastAuthError", "OvercastConnectionError"]

# Convenience alias for cleaner imports
Overcast = OvercastClient
