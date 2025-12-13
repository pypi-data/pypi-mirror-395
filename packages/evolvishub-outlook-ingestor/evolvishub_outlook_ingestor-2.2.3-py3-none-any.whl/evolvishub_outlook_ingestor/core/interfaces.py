"""
Core interfaces and abstract base classes for advanced features.

This module defines the interfaces that all advanced feature components must implement
to ensure consistency and interoperability across the email data platform.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Union, AsyncIterator, Callable
from datetime import datetime
from enum import Enum

from evolvishub_outlook_ingestor.core.data_models import EmailMessage, EmailAttachment, OutlookFolder


class ProcessingStatus(Enum):
    """Status of data processing operations."""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


class CacheStrategy(Enum):
    """Caching strategies for different data types."""
    LRU = "lru"
    LFU = "lfu"
    TTL = "ttl"
    WRITE_THROUGH = "write_through"
    WRITE_BACK = "write_back"
    REFRESH_AHEAD = "refresh_ahead"


class DataQualityLevel(Enum):
    """Data quality assessment levels."""
    EXCELLENT = "excellent"
    GOOD = "good"
    FAIR = "fair"
    POOR = "poor"
    CRITICAL = "critical"


class IStreamingService(ABC):
    """Interface for real-time streaming services."""
    
    @abstractmethod
    async def start_streaming(self) -> None:
        """Start the streaming service."""
        pass
    
    @abstractmethod
    async def stop_streaming(self) -> None:
        """Stop the streaming service."""
        pass
    
    @abstractmethod
    async def stream_emails(self, callback: Callable[[EmailMessage], None]) -> AsyncIterator[EmailMessage]:
        """Stream emails in real-time."""
        pass
    
    @abstractmethod
    async def subscribe_to_folder(self, folder_id: str, callback: Callable[[EmailMessage], None]) -> str:
        """Subscribe to email updates from a specific folder."""
        pass


class ICDCService(ABC):
    """Interface for Change Data Capture services."""
    
    @abstractmethod
    async def get_changes_since(self, timestamp: datetime, entity_type: str) -> List[Dict[str, Any]]:
        """Get all changes since a specific timestamp."""
        pass
    
    @abstractmethod
    async def track_change(self, entity_id: str, entity_type: str, change_type: str, data: Dict[str, Any]) -> None:
        """Track a change to an entity."""
        pass
    
    @abstractmethod
    async def get_latest_timestamp(self, entity_type: str) -> Optional[datetime]:
        """Get the latest change timestamp for an entity type."""
        pass


class IDataTransformer(ABC):
    """Interface for data transformation services."""
    
    @abstractmethod
    async def transform_email(self, email: EmailMessage) -> EmailMessage:
        """Transform an email message."""
        pass
    
    @abstractmethod
    async def extract_entities(self, text: str) -> Dict[str, List[str]]:
        """Extract entities from text."""
        pass
    
    @abstractmethod
    async def analyze_sentiment(self, text: str) -> Dict[str, float]:
        """Analyze sentiment of text."""
        pass
    
    @abstractmethod
    async def detect_language(self, text: str) -> str:
        """Detect the language of text."""
        pass


class IAnalyticsEngine(ABC):
    """Interface for analytics and insights engines."""
    
    @abstractmethod
    async def analyze_communication_patterns(self, emails: List[EmailMessage]) -> Dict[str, Any]:
        """Analyze communication patterns."""
        pass
    
    @abstractmethod
    async def generate_insights(self, emails: List[EmailMessage]) -> Dict[str, Any]:
        """Generate insights from emails."""
        pass
    
    @abstractmethod
    async def detect_anomalies(self, emails: List[EmailMessage]) -> List[Dict[str, Any]]:
        """Detect anomalies in email data."""
        pass


class IDataQualityValidator(ABC):
    """Interface for data quality validation services."""
    
    @abstractmethod
    async def validate_email(self, email: EmailMessage) -> Dict[str, Any]:
        """Validate an email message."""
        pass
    
    @abstractmethod
    async def check_completeness(self, data: Dict[str, Any]) -> float:
        """Check data completeness score (0-1)."""
        pass
    
    @abstractmethod
    async def detect_duplicates(self, emails: List[EmailMessage]) -> List[str]:
        """Detect duplicate emails."""
        pass
    
    @abstractmethod
    async def assess_quality_level(self, validation_results: Dict[str, Any]) -> DataQualityLevel:
        """Assess overall data quality level."""
        pass


class ICacheManager(ABC):
    """Interface for intelligent caching services."""
    
    @abstractmethod
    async def get(self, key: str, default: Any = None) -> Any:
        """Get value from cache."""
        pass
    
    @abstractmethod
    async def set(self, key: str, value: Any, ttl: Optional[int] = None, strategy: CacheStrategy = CacheStrategy.LRU) -> None:
        """Set value in cache."""
        pass
    
    @abstractmethod
    async def invalidate(self, pattern: str) -> int:
        """Invalidate cache entries matching pattern."""
        pass
    
    @abstractmethod
    async def warm_cache(self, keys: List[str]) -> None:
        """Warm cache with specified keys."""
        pass


class ITenantManager(ABC):
    """Interface for multi-tenant management services."""
    
    @abstractmethod
    async def get_tenant_config(self, tenant_id: str) -> Dict[str, Any]:
        """Get configuration for a tenant."""
        pass
    
    @abstractmethod
    async def isolate_data(self, tenant_id: str, data: Any) -> Any:
        """Apply tenant isolation to data."""
        pass
    
    @abstractmethod
    async def check_permissions(self, tenant_id: str, resource: str, action: str) -> bool:
        """Check tenant permissions."""
        pass


class IGovernanceService(ABC):
    """Interface for data governance and lineage services."""
    
    @abstractmethod
    async def track_lineage(self, entity_id: str, operation: str, metadata: Dict[str, Any]) -> None:
        """Track data lineage."""
        pass
    
    @abstractmethod
    async def get_lineage(self, entity_id: str) -> Dict[str, Any]:
        """Get data lineage for an entity."""
        pass
    
    @abstractmethod
    async def apply_retention_policy(self, policy_name: str, entities: List[str]) -> None:
        """Apply data retention policy."""
        pass


class IMLService(ABC):
    """Interface for machine learning services."""
    
    @abstractmethod
    async def classify_email(self, email: EmailMessage) -> Dict[str, float]:
        """Classify email content."""
        pass
    
    @abstractmethod
    async def extract_features(self, email: EmailMessage) -> Dict[str, Any]:
        """Extract ML features from email."""
        pass
    
    @abstractmethod
    async def predict_priority(self, email: EmailMessage) -> float:
        """Predict email priority score."""
        pass
    
    @abstractmethod
    async def detect_spam(self, email: EmailMessage) -> float:
        """Detect spam probability."""
        pass


class IMonitoringService(ABC):
    """Interface for advanced monitoring and observability services."""
    
    @abstractmethod
    async def record_metric(self, name: str, value: float, tags: Optional[Dict[str, str]] = None) -> None:
        """Record a metric."""
        pass
    
    @abstractmethod
    async def start_trace(self, operation_name: str) -> str:
        """Start a distributed trace."""
        pass
    
    @abstractmethod
    async def end_trace(self, trace_id: str, status: str = "success") -> None:
        """End a distributed trace."""
        pass
    
    @abstractmethod
    async def log_event(self, level: str, message: str, metadata: Optional[Dict[str, Any]] = None) -> None:
        """Log an event with metadata."""
        pass


class ServiceRegistry:
    """Registry for managing service instances."""
    
    def __init__(self):
        self._services: Dict[str, Any] = {}
    
    def register(self, service_name: str, service_instance: Any) -> None:
        """Register a service instance."""
        self._services[service_name] = service_instance
    
    def get(self, service_name: str) -> Optional[Any]:
        """Get a service instance."""
        return self._services.get(service_name)
    
    def unregister(self, service_name: str) -> None:
        """Unregister a service."""
        self._services.pop(service_name, None)
    
    def list_services(self) -> List[str]:
        """List all registered services."""
        return list(self._services.keys())


# Global service registry instance
service_registry = ServiceRegistry()
