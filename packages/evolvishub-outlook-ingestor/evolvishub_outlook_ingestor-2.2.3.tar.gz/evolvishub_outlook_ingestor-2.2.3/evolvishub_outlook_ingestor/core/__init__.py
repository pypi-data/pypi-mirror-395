"""
Core module for Evolvishub Outlook Ingestor.

This module contains the fundamental components of the library including:
- Configuration management
- Base processor classes
- Data models and schemas
- Exception definitions
- Logging utilities
- Modern email ingestor functionality

The core module provides the foundation for all other components and ensures
consistent behavior across the entire library.

Note: OutlookIngestor is deprecated. Use EmailIngestor for new projects.
"""

from evolvishub_outlook_ingestor.core.config import Settings, get_settings
from evolvishub_outlook_ingestor.core.data_models import (
    EmailMessage,
    EmailAddress,
    EmailAttachment,
    OutlookFolder,
    ProcessingResult,
    ProcessingStatus,
)
from evolvishub_outlook_ingestor.core.exceptions import (
    OutlookIngestorError,
    ProtocolError,
    DatabaseError,
    ConfigurationError,
    AuthenticationError,
)
from evolvishub_outlook_ingestor.core.thread_builder import (
    ThreadBuilder,
    ConversationThread,
)

__all__ = [
    "Settings",
    "get_settings",
    "EmailMessage",
    "EmailAddress",
    "EmailAttachment",
    "OutlookFolder",
    "ProcessingResult",
    "ProcessingStatus",
    "OutlookIngestorError",
    "ProtocolError",
    "DatabaseError",
    "ConfigurationError",
    "AuthenticationError",
    "ThreadBuilder",
    "ConversationThread",
]
