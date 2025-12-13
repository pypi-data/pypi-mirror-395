"""
Protocol adapters for Evolvishub Outlook Email Ingestor.

This module contains protocol adapters focused on email ingestion:
- Microsoft Graph API (primary) - RECOMMENDED
- Exchange Web Services (EWS) (legacy support)
- IMAP/POP3 (legacy support)
- Email Ingestor Protocol (DEPRECATED - use GraphAPIAdapter directly)

All protocol adapters implement a common interface defined by BaseProtocol
with standardized mixins for authentication, rate limiting, error handling,
and health monitoring.

Note: EmailIngestorProtocol is deprecated. Use GraphAPIAdapter directly for
better performance and consistency.
"""

from evolvishub_outlook_ingestor.protocols.base_protocol import BaseProtocol
from evolvishub_outlook_ingestor.protocols.microsoft_graph import GraphAPIAdapter
from evolvishub_outlook_ingestor.protocols.mixins import (
    AuthenticationCapability,
    RateLimitingCapability,
    ErrorHandlingCapability,
    ConnectionCapability,
    HealthCheckCapability,
    AuthenticationConfig,
    RateLimitConfig,
    # Backward compatibility aliases
    AuthenticationMixin,
    RateLimitingMixin,
    ErrorHandlingMixin,
    ConnectionMixin,
    HealthCheckMixin,
)
from evolvishub_outlook_ingestor.protocols.email_ingestor_protocol import (
    EmailIngestorProtocol,
    IngestionConfig,
    IngestionProgress,
)

# Legacy protocol support
try:
    from evolvishub_outlook_ingestor.protocols.exchange_web_services import ExchangeWebServicesAdapter
    from evolvishub_outlook_ingestor.protocols.imap_pop3 import IMAPAdapter
    _LEGACY_PROTOCOLS_AVAILABLE = True
except ImportError:
    _LEGACY_PROTOCOLS_AVAILABLE = False

__all__ = [
    # Core protocols
    "BaseProtocol",
    "GraphAPIAdapter",  # RECOMMENDED

    # Legacy protocols (deprecated)
    "EmailIngestorProtocol",  # DEPRECATED - use GraphAPIAdapter

    # Configuration and progress tracking
    "IngestionConfig",
    "IngestionProgress",

    # Capabilities for custom protocol development (new naming)
    "AuthenticationCapability",
    "RateLimitingCapability",
    "ErrorHandlingCapability",
    "ConnectionCapability",
    "HealthCheckCapability",

    # Backward compatibility aliases (deprecated)
    "AuthenticationMixin",
    "RateLimitingMixin",
    "ErrorHandlingMixin",
    "ConnectionMixin",
    "HealthCheckMixin",

    # Configuration classes
    "AuthenticationConfig",
    "RateLimitConfig",
]

# Add legacy protocols if available
if _LEGACY_PROTOCOLS_AVAILABLE:
    __all__.extend([
        "ExchangeWebServicesAdapter",  # Legacy
        "IMAPAdapter",  # Legacy
    ])
