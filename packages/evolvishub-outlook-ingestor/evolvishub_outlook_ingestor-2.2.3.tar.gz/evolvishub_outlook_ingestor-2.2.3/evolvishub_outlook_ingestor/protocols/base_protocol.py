"""
Base protocol adapter for Evolvishub Outlook Ingestor.

This module defines the abstract base class that all protocol adapters
must implement. It provides a consistent interface for:
- Connection management
- Authentication
- Email fetching
- Folder operations
- Error handling
- Rate limiting

All protocol adapters (EWS, Graph API, IMAP/POP3) inherit from this base
class to ensure consistent behavior and easy interchangeability.
"""

import asyncio
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, AsyncGenerator, Dict, List, Optional, Union

from evolvishub_outlook_ingestor.core.data_models import EmailMessage, OutlookFolder
from evolvishub_outlook_ingestor.core.exceptions import AuthenticationError, ProtocolError
from evolvishub_outlook_ingestor.core.logging import LoggerMixin
from evolvishub_outlook_ingestor.protocols.mixins import (
    AuthenticationCapability,
    RateLimitingCapability,
    ErrorHandlingCapability,
    ConnectionCapability,
    HealthCheckCapability,
)


class ConnectionStatus:
    """Connection status tracking."""
    
    def __init__(self):
        self.is_connected = False
        self.is_authenticated = False
        self.last_activity = None
        self.connection_time = None
        self.error_count = 0
        self.last_error = None


class BaseProtocol(
    AuthenticationCapability,
    RateLimitingCapability,
    ErrorHandlingCapability,
    ConnectionCapability,
    HealthCheckCapability,
    LoggerMixin,
    ABC
):
    """
    Abstract base class for all protocol adapters.

    This class defines the interface that all protocol adapters must implement
    to provide consistent behavior across different Outlook connection methods.

    Includes standardized mixins for:
    - Authentication management (OAuth2, tokens, credentials)
    - Rate limiting (requests per minute, burst control)
    - Error handling (retry logic, standardized logging)
    - Connection management (connection state, cleanup)
    - Health checking (comprehensive status monitoring)
    """
    
    def __init__(
        self,
        name: str,
        config: Dict[str, Any],
        enable_rate_limiting: bool = True,
        max_retries: int = 3,
        retry_delay: float = 1.0,
    ):
        """
        Initialize the protocol adapter.

        Args:
            name: Protocol adapter name
            config: Configuration dictionary
            enable_rate_limiting: Enable rate limiting
            max_retries: Maximum retry attempts
            retry_delay: Delay between retries in seconds
        """
        # Initialize all mixins
        super().__init__()

        self.name = name
        self.config = config
        self.enable_rate_limiting = enable_rate_limiting
        self.max_retries = max_retries
        self.retry_delay = retry_delay

        # Legacy connection status (deprecated - use ConnectionMixin instead)
        self.status = ConnectionStatus()
        self._connection = None
        self._session = None
        
        # Rate limiting
        self._rate_limiter = None
        if enable_rate_limiting:
            self._setup_rate_limiter()
        
        # Caching
        self._folder_cache: Dict[str, OutlookFolder] = {}
        self._cache_ttl = 300  # 5 minutes
        self._last_cache_update = None
    
    async def initialize(self) -> None:
        """Initialize the protocol adapter."""
        self.logger.info("Initializing protocol adapter", protocol=self.name)
        
        try:
            await self._initialize_connection()
            await self._authenticate()
            
            self.status.is_connected = True
            self.status.is_authenticated = True
            self.status.connection_time = datetime.utcnow()
            
            self.logger.info("Protocol adapter initialized successfully", protocol=self.name)
            
        except Exception as e:
            self.status.error_count += 1
            self.status.last_error = str(e)
            
            self.logger.error(
                "Failed to initialize protocol adapter",
                protocol=self.name,
                error=str(e)
            )
            raise ProtocolError(
                f"Failed to initialize {self.name} protocol: {e}",
                protocol=self.name,
                cause=e
            )
    
    async def cleanup(self) -> None:
        """Cleanup protocol adapter resources."""
        self.logger.info("Cleaning up protocol adapter", protocol=self.name)
        
        try:
            await self._cleanup_connection()
            
            self.status.is_connected = False
            self.status.is_authenticated = False
            
            self.logger.info("Protocol adapter cleanup completed", protocol=self.name)
            
        except Exception as e:
            self.logger.warning(
                "Error during protocol adapter cleanup",
                protocol=self.name,
                error=str(e)
            )

    async def __aenter__(self):
        """Async context manager entry."""
        await self.initialize()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.cleanup()

        # Log any exceptions that occurred
        if exc_type is not None:
            self.logger.error(
                "Exception occurred in protocol context",
                protocol=self.name,
                exception_type=exc_type.__name__,
                exception_message=str(exc_val)
            )

        # Don't suppress exceptions
        return False

    async def fetch_emails(
        self,
        folder_filters: Optional[List[str]] = None,
        date_range: Optional[Dict[str, datetime]] = None,
        limit: Optional[int] = None,
        include_attachments: bool = True,
        **kwargs
    ) -> List[EmailMessage]:
        """
        Fetch emails from the server.
        
        Args:
            folder_filters: List of folder names to include
            date_range: Date range filter with 'start' and 'end' keys
            limit: Maximum number of emails to fetch
            include_attachments: Whether to include attachments
            **kwargs: Additional protocol-specific parameters
            
        Returns:
            List of EmailMessage objects
        """
        if not self.status.is_connected or not self.status.is_authenticated:
            await self.initialize()
        
        self.logger.info(
            "Fetching emails",
            protocol=self.name,
            folder_filters=folder_filters,
            limit=limit
        )
        
        try:
            # Apply rate limiting
            if self._rate_limiter:
                await self._rate_limiter.acquire()
            
            emails = await self._fetch_emails_impl(
                folder_filters=folder_filters,
                date_range=date_range,
                limit=limit,
                include_attachments=include_attachments,
                **kwargs
            )
            
            self.status.last_activity = datetime.utcnow()
            
            self.logger.info(
                "Emails fetched successfully",
                protocol=self.name,
                count=len(emails)
            )
            
            return emails
            
        except Exception as e:
            self.status.error_count += 1
            self.status.last_error = str(e)
            
            self.logger.error(
                "Failed to fetch emails",
                protocol=self.name,
                error=str(e)
            )
            
            raise ProtocolError(
                f"Failed to fetch emails: {e}",
                protocol=self.name,
                cause=e
            )
    
    async def fetch_emails_stream(
        self,
        folder_filters: Optional[List[str]] = None,
        date_range: Optional[Dict[str, datetime]] = None,
        batch_size: int = 100,
        include_attachments: bool = True,
        **kwargs
    ) -> AsyncGenerator[List[EmailMessage], None]:
        """
        Fetch emails as a stream for memory-efficient processing.
        
        Args:
            folder_filters: List of folder names to include
            date_range: Date range filter
            batch_size: Number of emails per batch
            include_attachments: Whether to include attachments
            **kwargs: Additional parameters
            
        Yields:
            Batches of EmailMessage objects
        """
        if not self.status.is_connected or not self.status.is_authenticated:
            await self.initialize()
        
        self.logger.info(
            "Starting email stream",
            protocol=self.name,
            batch_size=batch_size
        )
        
        try:
            async for batch in self._fetch_emails_stream_impl(
                folder_filters=folder_filters,
                date_range=date_range,
                batch_size=batch_size,
                include_attachments=include_attachments,
                **kwargs
            ):
                # Apply rate limiting
                if self._rate_limiter:
                    await self._rate_limiter.acquire()
                
                self.status.last_activity = datetime.utcnow()
                yield batch
                
        except Exception as e:
            self.status.error_count += 1
            self.status.last_error = str(e)
            
            self.logger.error(
                "Email stream failed",
                protocol=self.name,
                error=str(e)
            )
            
            raise ProtocolError(
                f"Email stream failed: {e}",
                protocol=self.name,
                cause=e
            )
    
    async def get_folders(self, refresh_cache: bool = False, user_identifier: Optional[str] = None) -> List[OutlookFolder]:
        """
        Get list of available folders.

        Args:
            refresh_cache: Force refresh of folder cache
            user_identifier: User email or ID (implementation-specific)

        Returns:
            List of OutlookFolder objects
        """
        if not self.status.is_connected or not self.status.is_authenticated:
            await self.initialize()

        # Check cache (only use cache if no specific user is requested)
        if not refresh_cache and not user_identifier and self._folder_cache and self._is_cache_valid():
            return list(self._folder_cache.values())

        self.logger.debug("Fetching folder list", protocol=self.name, user=user_identifier)

        try:
            folders = await self._get_folders_impl(user_identifier=user_identifier)

            # Update cache (only if fetching for default user)
            if not user_identifier:
                self._folder_cache = {folder.id: folder for folder in folders}
                self._last_cache_update = datetime.utcnow()

            self.status.last_activity = datetime.utcnow()

            self.logger.debug(
                "Folders fetched successfully",
                protocol=self.name,
                count=len(folders)
            )

            return folders

        except Exception as e:
            self.status.error_count += 1
            self.status.last_error = str(e)

            self.logger.error(
                "Failed to fetch folders",
                protocol=self.name,
                error=str(e)
            )

            raise ProtocolError(
                f"Failed to fetch folders: {e}",
                protocol=self.name,
                cause=e
            )
    
    async def test_connection(self) -> bool:
        """
        Test the connection to the server.
        
        Returns:
            True if connection is successful, False otherwise
        """
        try:
            await self.initialize()
            return self.status.is_connected and self.status.is_authenticated
        except Exception:
            return False
    
    def get_status(self) -> Dict[str, Any]:
        """Get connection status information."""
        return {
            "protocol": self.name,
            "is_connected": self.status.is_connected,
            "is_authenticated": self.status.is_authenticated,
            "last_activity": self.status.last_activity,
            "connection_time": self.status.connection_time,
            "error_count": self.status.error_count,
            "last_error": self.status.last_error,
        }
    
    # Abstract methods that must be implemented by subclasses
    
    @abstractmethod
    async def _initialize_connection(self) -> None:
        """Initialize the connection to the server."""
        pass
    
    @abstractmethod
    async def _authenticate(self) -> None:
        """Authenticate with the server."""
        pass
    
    @abstractmethod
    async def _cleanup_connection(self) -> None:
        """Cleanup connection resources."""
        pass
    
    @abstractmethod
    async def _fetch_emails_impl(
        self,
        folder_filters: Optional[List[str]] = None,
        date_range: Optional[Dict[str, datetime]] = None,
        limit: Optional[int] = None,
        include_attachments: bool = True,
        **kwargs
    ) -> List[EmailMessage]:
        """Implementation-specific email fetching."""
        pass
    
    @abstractmethod
    async def _fetch_emails_stream_impl(
        self,
        folder_filters: Optional[List[str]] = None,
        date_range: Optional[Dict[str, datetime]] = None,
        batch_size: int = 100,
        include_attachments: bool = True,
        **kwargs
    ) -> AsyncGenerator[List[EmailMessage], None]:
        """Implementation-specific email streaming."""
        pass
    
    @abstractmethod
    async def _get_folders_impl(self, user_identifier: Optional[str] = None) -> List[OutlookFolder]:
        """Implementation-specific folder fetching."""
        pass
    
    # Helper methods
    
    def _setup_rate_limiter(self) -> None:
        """Setup rate limiting based on configuration."""
        # This would be implemented with a proper rate limiter
        # For now, we'll use a simple semaphore
        rate_limit = self.config.get("rate_limit", 100)  # requests per minute
        self._rate_limiter = asyncio.Semaphore(rate_limit)
    
    def _is_cache_valid(self) -> bool:
        """Check if folder cache is still valid."""
        if not self._last_cache_update:
            return False
        
        age = (datetime.utcnow() - self._last_cache_update).total_seconds()
        return age < self._cache_ttl
