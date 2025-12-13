"""
Exception definitions for Evolvishub Outlook Ingestor.

This module defines a comprehensive hierarchy of exceptions used throughout
the library. All exceptions include error codes, detailed messages, and
contextual information to aid in debugging and error handling.

Exception Hierarchy:
- OutlookIngestorError (base)
  - ConfigurationError
  - AuthenticationError
  - ProtocolError
    - ExchangeError
    - GraphAPIError
    - IMAPError
  - DatabaseError
    - ConnectionError
    - QueryError
    - TransactionError
  - ProcessingError
    - ValidationError
    - TimeoutError
    - MemoryError
    - RateLimitError
"""

from typing import Any, Dict, Optional


class OutlookIngestorError(Exception):
    """
    Base exception for all Outlook Ingestor errors.
    
    This is the root exception class that all other exceptions inherit from.
    It provides common functionality for error codes, context, and formatting.
    """
    
    def __init__(
        self,
        message: str,
        error_code: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None,
        cause: Optional[Exception] = None,
    ):
        """
        Initialize the exception.
        
        Args:
            message: Human-readable error message
            error_code: Machine-readable error code
            context: Additional context information
            cause: Original exception that caused this error
        """
        super().__init__(message)
        self.message = message
        self.error_code = error_code or self.__class__.__name__.upper()
        self.context = context or {}
        self.cause = cause
    
    def __str__(self) -> str:
        """String representation of the exception."""
        parts = [f"[{self.error_code}] {self.message}"]
        
        if self.context:
            context_str = ", ".join(f"{k}={v}" for k, v in self.context.items())
            parts.append(f"Context: {context_str}")
        
        if self.cause:
            parts.append(f"Caused by: {self.cause}")
        
        return " | ".join(parts)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert exception to dictionary for serialization."""
        return {
            "error_type": self.__class__.__name__,
            "error_code": self.error_code,
            "message": self.message,
            "context": self.context,
            "cause": str(self.cause) if self.cause else None,
        }


class ConfigurationError(OutlookIngestorError):
    """Raised when there are configuration-related errors."""
    
    def __init__(
        self,
        message: str,
        config_key: Optional[str] = None,
        config_value: Optional[Any] = None,
        **kwargs
    ):
        context = kwargs.get("context", {})
        if config_key:
            context["config_key"] = config_key
        if config_value is not None:
            context["config_value"] = str(config_value)
        
        super().__init__(
            message,
            error_code="CONFIGURATION_ERROR",
            context=context,
            **kwargs
        )


class AuthenticationError(OutlookIngestorError):
    """Raised when authentication fails."""
    
    def __init__(
        self,
        message: str,
        auth_method: Optional[str] = None,
        username: Optional[str] = None,
        **kwargs
    ):
        context = kwargs.get("context", {})
        if auth_method:
            context["auth_method"] = auth_method
        if username:
            context["username"] = username
        
        super().__init__(
            message,
            error_code="AUTHENTICATION_ERROR",
            context=context,
            **kwargs
        )


class ProtocolError(OutlookIngestorError):
    """Base class for protocol-related errors."""
    
    def __init__(
        self,
        message: str,
        protocol: Optional[str] = None,
        server: Optional[str] = None,
        **kwargs
    ):
        context = kwargs.get("context", {})
        if protocol:
            context["protocol"] = protocol
        if server:
            context["server"] = server
        
        super().__init__(
            message,
            error_code="PROTOCOL_ERROR",
            context=context,
            **kwargs
        )


class ExchangeError(ProtocolError):
    """Raised when Exchange Web Services operations fail."""
    
    def __init__(
        self,
        message: str,
        response_code: Optional[str] = None,
        **kwargs
    ):
        context = kwargs.get("context", {})
        if response_code:
            context["response_code"] = response_code
        
        super().__init__(
            message,
            protocol="EWS",
            error_code="EXCHANGE_ERROR",
            context=context,
            **kwargs
        )


class GraphAPIError(ProtocolError):
    """Raised when Microsoft Graph API operations fail."""
    
    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        error_code: Optional[str] = None,
        **kwargs
    ):
        context = kwargs.get("context", {})
        if status_code:
            context["status_code"] = status_code
        if error_code:
            context["api_error_code"] = error_code
        
        super().__init__(
            message,
            protocol="Graph API",
            error_code="GRAPH_API_ERROR",
            context=context,
            **kwargs
        )


class IMAPError(ProtocolError):
    """Raised when IMAP/POP3 operations fail."""
    
    def __init__(
        self,
        message: str,
        imap_response: Optional[str] = None,
        **kwargs
    ):
        context = kwargs.get("context", {})
        if imap_response:
            context["imap_response"] = imap_response
        
        super().__init__(
            message,
            protocol="IMAP",
            error_code="IMAP_ERROR",
            context=context,
            **kwargs
        )


class DatabaseError(OutlookIngestorError):
    """Base class for database-related errors."""
    
    def __init__(
        self,
        message: str,
        database_type: Optional[str] = None,
        operation: Optional[str] = None,
        **kwargs
    ):
        context = kwargs.pop("context", {})
        if database_type:
            context["database_type"] = database_type
        if operation:
            context["operation"] = operation

        super().__init__(
            message,
            error_code="DATABASE_ERROR",
            context=context,
            **kwargs
        )


class ConnectionError(DatabaseError):
    """Raised when database connection fails."""
    
    def __init__(
        self,
        message: str,
        host: Optional[str] = None,
        port: Optional[int] = None,
        **kwargs
    ):
        context = kwargs.pop("context", {})
        if host:
            context["host"] = host
        if port:
            context["port"] = port

        super().__init__(
            message,
            database_type=kwargs.pop("database_type", None),
            operation="connect",
            **kwargs
        )


class QueryError(DatabaseError):
    """Raised when database query execution fails."""
    
    def __init__(
        self,
        message: str,
        query: Optional[str] = None,
        **kwargs
    ):
        context = kwargs.get("context", {})
        if query:
            # Truncate long queries for logging
            context["query"] = query[:200] + "..." if len(query) > 200 else query
        
        super().__init__(
            message,
            operation="query",
            error_code="QUERY_ERROR",
            context=context,
            **kwargs
        )


class TransactionError(DatabaseError):
    """Raised when database transaction fails."""
    
    def __init__(
        self,
        message: str,
        transaction_id: Optional[str] = None,
        **kwargs
    ):
        context = kwargs.get("context", {})
        if transaction_id:
            context["transaction_id"] = transaction_id
        
        super().__init__(
            message,
            operation="transaction",
            error_code="TRANSACTION_ERROR",
            context=context,
            **kwargs
        )


class ProcessingError(OutlookIngestorError):
    """Base class for processing-related errors."""
    
    def __init__(
        self,
        message: str,
        processor: Optional[str] = None,
        item_id: Optional[str] = None,
        **kwargs
    ):
        context = kwargs.get("context", {})
        if processor:
            context["processor"] = processor
        if item_id:
            context["item_id"] = item_id
        
        super().__init__(
            message,
            error_code="PROCESSING_ERROR",
            context=context,
            **kwargs
        )


class ValidationError(ProcessingError):
    """Raised when data validation fails."""
    
    def __init__(
        self,
        message: str,
        field_name: Optional[str] = None,
        field_value: Optional[Any] = None,
        **kwargs
    ):
        context = kwargs.get("context", {})
        if field_name:
            context["field_name"] = field_name
        if field_value is not None:
            context["field_value"] = str(field_value)
        
        super().__init__(
            message,
            error_code="VALIDATION_ERROR",
            context=context,
            **kwargs
        )


class TimeoutError(ProcessingError):
    """Raised when operations timeout."""
    
    def __init__(
        self,
        message: str,
        timeout_seconds: Optional[float] = None,
        **kwargs
    ):
        context = kwargs.get("context", {})
        if timeout_seconds:
            context["timeout_seconds"] = timeout_seconds
        
        super().__init__(
            message,
            error_code="TIMEOUT_ERROR",
            context=context,
            **kwargs
        )


class MemoryError(ProcessingError):
    """Raised when memory limits are exceeded."""
    
    def __init__(
        self,
        message: str,
        memory_usage_mb: Optional[float] = None,
        memory_limit_mb: Optional[float] = None,
        **kwargs
    ):
        context = kwargs.get("context", {})
        if memory_usage_mb:
            context["memory_usage_mb"] = memory_usage_mb
        if memory_limit_mb:
            context["memory_limit_mb"] = memory_limit_mb
        
        super().__init__(
            message,
            error_code="MEMORY_ERROR",
            context=context,
            **kwargs
        )


class StreamingError(OutlookIngestorError):
    """Raised when streaming operations fail."""

    def __init__(
        self,
        message: str,
        stream_type: Optional[str] = None,
        **kwargs
    ):
        context = {"stream_type": stream_type}
        super().__init__(
            message,
            error_code="STREAMING_ERROR",
            context=context,
            **kwargs
        )


class TransformationError(ProcessingError):
    """Raised when data transformation fails."""

    def __init__(
        self,
        message: str,
        transformation_type: Optional[str] = None,
        **kwargs
    ):
        context = {"transformation_type": transformation_type}
        super().__init__(
            message,
            processor="transformer",
            context=context,
            **kwargs
        )


class AnalyticsError(OutlookIngestorError):
    """Raised when analytics operations fail."""

    def __init__(
        self,
        message: str,
        analytics_type: Optional[str] = None,
        **kwargs
    ):
        context = {"analytics_type": analytics_type}
        super().__init__(
            message,
            error_code="ANALYTICS_ERROR",
            context=context,
            **kwargs
        )


class QualityError(OutlookIngestorError):
    """Raised when data quality operations fail."""

    def __init__(
        self,
        message: str,
        quality_type: Optional[str] = None,
        **kwargs
    ):
        context = {"quality_type": quality_type}
        super().__init__(
            message,
            error_code="QUALITY_ERROR",
            context=context,
            **kwargs
        )


class CacheError(OutlookIngestorError):
    """Raised when cache operations fail."""

    def __init__(
        self,
        message: str,
        cache_backend: Optional[str] = None,
        **kwargs
    ):
        context = {"cache_backend": cache_backend}
        super().__init__(
            message,
            error_code="CACHE_ERROR",
            context=context,
            **kwargs
        )


class TenantError(OutlookIngestorError):
    """Raised when tenant operations fail."""

    def __init__(
        self,
        message: str,
        tenant_id: Optional[str] = None,
        **kwargs
    ):
        context = {"tenant_id": tenant_id}
        super().__init__(
            message,
            error_code="TENANT_ERROR",
            context=context,
            **kwargs
        )


class PermissionError(OutlookIngestorError):
    """Raised when permission checks fail."""

    def __init__(
        self,
        message: str,
        resource: Optional[str] = None,
        **kwargs
    ):
        context = {"resource": resource}
        super().__init__(
            message,
            error_code="PERMISSION_ERROR",
            context=context,
            **kwargs
        )


class MLError(OutlookIngestorError):
    """Raised when machine learning operations fail."""

    def __init__(
        self,
        message: str,
        model_type: Optional[str] = None,
        **kwargs
    ):
        context = {"model_type": model_type}
        super().__init__(
            message,
            error_code="ML_ERROR",
            context=context,
            **kwargs
        )


class GovernanceError(OutlookIngestorError):
    """Raised when governance operations fail."""

    def __init__(
        self,
        message: str,
        governance_type: Optional[str] = None,
        **kwargs
    ):
        context = {"governance_type": governance_type}
        super().__init__(
            message,
            error_code="GOVERNANCE_ERROR",
            context=context,
            **kwargs
        )


class MonitoringError(OutlookIngestorError):
    """Raised when monitoring operations fail."""

    def __init__(
        self,
        message: str,
        monitoring_type: Optional[str] = None,
        **kwargs
    ):
        context = {"monitoring_type": monitoring_type}
        super().__init__(
            message,
            error_code="MONITORING_ERROR",
            context=context,
            **kwargs
        )


class RateLimitError(ProtocolError):
    """
    Exception raised when rate limits are exceeded.

    This exception is raised when API rate limits are hit or when
    request throttling is applied to prevent overwhelming services.
    """

    def __init__(
        self,
        message: str,
        retry_after: Optional[int] = None,
        requests_remaining: Optional[int] = None,
        reset_time: Optional[str] = None,
        **kwargs
    ):
        context = {
            "retry_after": retry_after,
            "requests_remaining": requests_remaining,
            "reset_time": reset_time
        }
        super().__init__(
            message,
            error_code="RATE_LIMIT_EXCEEDED",
            context=context,
            **kwargs
        )
