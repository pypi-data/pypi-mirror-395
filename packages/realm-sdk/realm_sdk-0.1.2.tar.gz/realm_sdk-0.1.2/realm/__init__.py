"""
Realm Python SDK

Simple SDK for tracking agent events and sending them to Realm.
"""

from .client import RealmClient
from .types import EventType

__version__ = "0.1.2"
__all__ = ["RealmClient", "EventType"]

# Optional LangChain integration (only available if langchain is installed)
try:
    from .langchain import RealmCallbackHandler
    __all__.append("RealmCallbackHandler")
except ImportError:
    # LangChain not installed, skip
    pass
