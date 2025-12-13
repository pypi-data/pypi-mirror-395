"""
Evolvishub Outlook Email Ingestor

A focused, production-ready library for ingesting emails from Microsoft Outlook
using Microsoft Graph API. Designed as a pure data ingestion library that can
be easily integrated into other applications and microservices.

Key Features:
- Complete Microsoft Graph email operations (CRUD, search, threading)
- Batch processing with progress tracking
- Multiple output formats (database connectors, JSON, CSV)
- Error handling and retry mechanisms
- Configurable data transformation
- Clean, simple integration interface
- Async/await support for high performance
- Comprehensive logging and monitoring

Example Usage:
    ```python
    from evolvishub_outlook_ingestor import EmailIngestor, ingest_emails_simple
    
    # Simple usage
    result = await ingest_emails_simple(
        client_id="your-client-id",
        client_secret="your-client-secret",
        tenant_id="your-tenant-id",
        output_format="json"
    )
    
    # Advanced usage
    ingestor = EmailIngestor(settings=settings, graph_adapter=adapter)
    await ingestor.initialize()
    
    result = await ingestor.ingest_emails(
        folder_ids=["inbox", "sent"],
        output_format="database"
    )
    ```
"""

# Version information
__version__ = "2.2.3"
__author__ = "Alban Maxhuni, PhD"
__email__ = "a.maxhuni@evolvis.ai"
__license__ = "Evolvis AI"

# Public API exports
from evolvishub_outlook_ingestor.core.config import Settings, get_settings
from evolvishub_outlook_ingestor.core.data_models import (
    EmailMessage,
    EmailAddress,
    EmailAttachment,
    OutlookFolder,
    ProcessingResult,
    ProcessingStatus,
    BatchProcessingConfig,
    UserProcessingResult,
    MultiUserProcessingResult,
    EmailImportance,
    AttachmentType,
)
from evolvishub_outlook_ingestor.core.exceptions import (
    OutlookIngestorError,
    ProtocolError,
    DatabaseError,
    ConfigurationError,
    AuthenticationError,
    ProcessingError,
    ValidationError,
    GraphAPIError,
)

# Main email ingestor classes
from evolvishub_outlook_ingestor.core.email_ingestor import EmailIngestor, ingest_emails_simple
from evolvishub_outlook_ingestor.protocols.email_ingestor_protocol import (
    EmailIngestorProtocol,
    IngestionConfig,
    IngestionProgress,
)

# Legacy support (for backward compatibility)
try:
    from evolvishub_outlook_ingestor.core.ingestor import OutlookIngestor
    from evolvishub_outlook_ingestor.protocols.microsoft_graph import GraphAPIAdapter
    _LEGACY_SUPPORT_AVAILABLE = True
except ImportError:
    _LEGACY_SUPPORT_AVAILABLE = False

# Database connectors (new interface)
try:
    from evolvishub_outlook_ingestor.connectors.database_connector import (
        DatabaseConnector,
        DatabaseConfig,
        create_database_connector
    )
    _DATABASE_CONNECTORS_AVAILABLE = True
except ImportError:
    _DATABASE_CONNECTORS_AVAILABLE = False

# Public API - focused on email ingestion
__all__ = [
    # Version info
    "__version__",
    "__author__",
    "__email__",
    "__license__",
    
    # Core email ingestor classes
    "EmailIngestor",
    "ingest_emails_simple",
    "EmailIngestorProtocol",
    "IngestionConfig", 
    "IngestionProgress",
    
    # Configuration
    "Settings",
    "get_settings",
    
    # Data models
    "EmailMessage",
    "EmailAddress",
    "EmailAttachment",
    "OutlookFolder",
    "ProcessingResult",
    "ProcessingStatus",
    "BatchProcessingConfig",
    "UserProcessingResult",
    "MultiUserProcessingResult",
    "EmailImportance",
    "AttachmentType",
    
    # Exceptions
    "OutlookIngestorError",
    "ProtocolError",
    "DatabaseError",
    "ConfigurationError",
    "AuthenticationError",
    "ProcessingError",
    "ValidationError",
    "GraphAPIError",
]

# Add legacy support if available
if _LEGACY_SUPPORT_AVAILABLE:
    __all__.extend([
        "OutlookIngestor",
        "GraphAPIAdapter",
    ])

# Add database connectors if available
if _DATABASE_CONNECTORS_AVAILABLE:
    __all__.extend([
        "DatabaseConnector",
        "DatabaseConfig",
        "create_database_connector",
    ])

# Package metadata
__package_name__ = "evolvishub-outlook-ingestor"
__description__ = "Focused email ingestion library for Microsoft Outlook using Microsoft Graph API"
__url__ = "https://github.com/evolvisai/metcal"
__classifiers__ = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "License :: Other/Proprietary License",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Topic :: Communications :: Email",
    "Topic :: Database",
    "Topic :: Software Development :: Libraries :: Python Modules",
    "Topic :: System :: Archiving",
    "Typing :: Typed",
]
