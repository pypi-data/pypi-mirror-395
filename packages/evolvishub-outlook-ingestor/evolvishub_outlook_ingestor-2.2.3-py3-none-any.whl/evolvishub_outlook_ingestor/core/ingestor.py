"""
Main Outlook Ingestor class for Evolvishub Outlook Ingestor.

This module provides the primary interface for the library, orchestrating
the interaction between protocol adapters, processors, and database connectors
to provide a seamless email ingestion experience.

The OutlookIngestor class serves as the main entry point and provides:
- High-level API for email ingestion
- Protocol and database abstraction
- Batch processing capabilities
- Error handling and retry mechanisms
- Progress tracking and monitoring
- Configuration management
"""

import asyncio
import warnings
from typing import Any, Dict, List, Optional, Union
from uuid import UUID, uuid4

from evolvishub_outlook_ingestor.core.base_processor import BaseProcessor
from evolvishub_outlook_ingestor.core.config import Settings
from evolvishub_outlook_ingestor.core.data_models import (
    BatchProcessingConfig,
    EmailMessage,
    ProcessingResult,
    ProcessingStatus,
)
from evolvishub_outlook_ingestor.core.exceptions import (
    ConfigurationError,
    OutlookIngestorError,
    ProcessingError,
)
from evolvishub_outlook_ingestor.core.logging import LoggerMixin, set_correlation_id


class OutlookIngestor(LoggerMixin):
    """
    Main Outlook Ingestor class.

    .. deprecated:: 1.2.0
        OutlookIngestor is deprecated and will be removed in version 2.0.0.
        Use EmailIngestor instead for a cleaner, more focused API.

    This class provides the primary interface for ingesting emails from
    Outlook servers and storing them in databases. It orchestrates the
    interaction between protocol adapters, processors, and connectors.

    For new code, use EmailIngestor which provides:
    - Cleaner, more focused API
    - Better type safety
    - Simplified configuration
    - Modern async patterns
    """

    def __init__(
        self,
        settings: Optional[Settings] = None,
        protocol_adapters: Optional[Dict[str, Any]] = None,
        database_connectors: Optional[Dict[str, Any]] = None,
        processors: Optional[Dict[str, Any]] = None,
    ):
        """
        Initialize the Outlook Ingestor.

        .. deprecated:: 1.2.0
            Use EmailIngestor instead. This class will be removed in version 2.0.0.

        Args:
            settings: Configuration settings
            protocol_adapters: Protocol adapter instances
            database_connectors: Database connector instances
            processors: Processor instances
        """
        # Issue deprecation warning
        warnings.warn(
            "OutlookIngestor is deprecated and will be removed in version 2.0.0. "
            "Use EmailIngestor instead for a cleaner, more focused API. "
            "See migration guide: https://docs.evolvishub.com/migration/outlook-to-email-ingestor",
            DeprecationWarning,
            stacklevel=2
        )

        self.settings = settings
        self.protocol_adapters = protocol_adapters or {}
        self.database_connectors = database_connectors or {}
        self.processors = processors or {}

        # State management
        self._is_initialized = False
        self._active_operations: Dict[UUID, ProcessingResult] = {}

        self.logger.info("Outlook Ingestor initialized (DEPRECATED - use EmailIngestor instead)")
    
    async def initialize(self) -> None:
        """Initialize the ingestor and all components."""
        if self._is_initialized:
            return
        
        self.logger.info("Initializing Outlook Ingestor")
        
        try:
            # Initialize protocol adapters
            for name, adapter in self.protocol_adapters.items():
                if hasattr(adapter, 'initialize'):
                    await adapter.initialize()
                self.logger.debug("Protocol adapter initialized", adapter=name)
            
            # Initialize database connectors
            for name, connector in self.database_connectors.items():
                if hasattr(connector, 'initialize'):
                    await connector.initialize()
                self.logger.debug("Database connector initialized", connector=name)
            
            # Initialize processors
            for name, processor in self.processors.items():
                if hasattr(processor, 'initialize'):
                    await processor.initialize()
                self.logger.debug("Processor initialized", processor=name)
            
            self._is_initialized = True
            self.logger.info("Outlook Ingestor initialization completed")
            
        except Exception as e:
            self.logger.error("Failed to initialize Outlook Ingestor", error=str(e))
            raise OutlookIngestorError(f"Initialization failed: {e}", cause=e)
    
    async def cleanup(self) -> None:
        """Cleanup all resources."""
        self.logger.info("Cleaning up Outlook Ingestor")
        
        # Cleanup processors
        for name, processor in self.processors.items():
            try:
                if hasattr(processor, 'cleanup'):
                    await processor.cleanup()
                self.logger.debug("Processor cleaned up", processor=name)
            except Exception as e:
                self.logger.warning("Error cleaning up processor", processor=name, error=str(e))
        
        # Cleanup database connectors
        for name, connector in self.database_connectors.items():
            try:
                if hasattr(connector, 'cleanup'):
                    await connector.cleanup()
                self.logger.debug("Database connector cleaned up", connector=name)
            except Exception as e:
                self.logger.warning("Error cleaning up connector", connector=name, error=str(e))
        
        # Cleanup protocol adapters
        for name, adapter in self.protocol_adapters.items():
            try:
                if hasattr(adapter, 'cleanup'):
                    await adapter.cleanup()
                self.logger.debug("Protocol adapter cleaned up", adapter=name)
            except Exception as e:
                self.logger.warning("Error cleaning up adapter", adapter=name, error=str(e))
        
        self._is_initialized = False
        self.logger.info("Outlook Ingestor cleanup completed")
    
    async def process_emails(
        self,
        protocol: str,
        database: str,
        batch_config: Optional[BatchProcessingConfig] = None,
        folder_filters: Optional[List[str]] = None,
        date_range: Optional[Dict[str, Any]] = None,
        operation_id: Optional[UUID] = None,
        correlation_id: Optional[str] = None,
        **kwargs
    ) -> ProcessingResult:
        """
        Process emails from Outlook server to database.
        
        Args:
            protocol: Protocol adapter name (e.g., 'exchange', 'graph_api', 'imap')
            database: Database connector name (e.g., 'postgresql', 'mongodb')
            batch_config: Batch processing configuration
            folder_filters: List of folders to process
            date_range: Date range filter
            operation_id: Operation ID for tracking
            correlation_id: Correlation ID for request tracking
            **kwargs: Additional parameters
            
        Returns:
            ProcessingResult with operation details
        """
        if not self._is_initialized:
            await self.initialize()
        
        # Setup operation tracking
        operation_id = operation_id or uuid4()
        correlation_id = correlation_id or set_correlation_id()
        
        result = ProcessingResult(
            operation_id=operation_id,
            correlation_id=correlation_id,
            status=ProcessingStatus.PENDING
        )
        
        self._active_operations[operation_id] = result
        
        self.logger.info(
            "Starting email processing operation",
            operation_id=str(operation_id),
            protocol=protocol,
            database=database
        )
        
        try:
            # Validate components
            protocol_adapter = self._get_protocol_adapter(protocol)
            database_connector = self._get_database_connector(database)
            email_processor = self._get_processor("email")
            
            result.status = ProcessingStatus.RUNNING
            
            # Fetch emails from protocol adapter
            emails = await self._fetch_emails(
                protocol_adapter,
                folder_filters=folder_filters,
                date_range=date_range,
                **kwargs
            )
            
            result.total_items = len(emails)
            
            # Process emails in batches
            if batch_config:
                processed_result = await self._process_emails_batch(
                    emails,
                    email_processor,
                    database_connector,
                    batch_config,
                    result
                )
            else:
                processed_result = await self._process_emails_sequential(
                    emails,
                    email_processor,
                    database_connector,
                    result
                )
            
            result.status = ProcessingStatus.COMPLETED
            result.calculate_duration()
            result.calculate_rate()
            
            self.logger.info(
                "Email processing operation completed",
                operation_id=str(operation_id),
                total_items=result.total_items,
                successful_items=result.successful_items,
                failed_items=result.failed_items,
                duration=result.duration_seconds
            )
            
            return processed_result
            
        except Exception as e:
            result.status = ProcessingStatus.FAILED
            result.error_message = str(e)
            result.calculate_duration()
            
            self.logger.error(
                "Email processing operation failed",
                operation_id=str(operation_id),
                error=str(e)
            )
            
            raise ProcessingError(
                f"Email processing failed: {e}",
                processor="email_ingestor",
                cause=e
            )
        
        finally:
            self._active_operations.pop(operation_id, None)
    
    def _get_protocol_adapter(self, protocol: str) -> Any:
        """Get protocol adapter by name."""
        if protocol not in self.protocol_adapters:
            raise ConfigurationError(
                f"Protocol adapter '{protocol}' not found",
                config_key="protocol",
                config_value=protocol
            )
        return self.protocol_adapters[protocol]
    
    def _get_database_connector(self, database: str) -> Any:
        """Get database connector by name."""
        if database not in self.database_connectors:
            raise ConfigurationError(
                f"Database connector '{database}' not found",
                config_key="database",
                config_value=database
            )
        return self.database_connectors[database]
    
    def _get_processor(self, processor_type: str) -> Any:
        """Get processor by type."""
        if processor_type not in self.processors:
            raise ConfigurationError(
                f"Processor '{processor_type}' not found",
                config_key="processor",
                config_value=processor_type
            )
        return self.processors[processor_type]
    
    async def _fetch_emails(
        self,
        protocol_adapter: Any,
        folder_filters: Optional[List[str]] = None,
        date_range: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> List[EmailMessage]:
        """Fetch emails from protocol adapter."""
        self.logger.debug("Fetching emails from protocol adapter")
        
        # This would be implemented by the specific protocol adapter
        if hasattr(protocol_adapter, 'fetch_emails'):
            return await protocol_adapter.fetch_emails(
                folder_filters=folder_filters,
                date_range=date_range,
                **kwargs
            )
        else:
            raise ProcessingError(
                "Protocol adapter does not support email fetching",
                processor="protocol_adapter"
            )
    
    async def _process_emails_batch(
        self,
        emails: List[EmailMessage],
        processor: Any,
        connector: Any,
        batch_config: BatchProcessingConfig,
        result: ProcessingResult
    ) -> ProcessingResult:
        """Process emails in batches."""
        self.logger.debug(
            "Processing emails in batches",
            total_emails=len(emails),
            batch_size=batch_config.batch_size
        )
        
        # Split emails into batches
        batches = [
            emails[i:i + batch_config.batch_size]
            for i in range(0, len(emails), batch_config.batch_size)
        ]
        
        # Process batches
        for i, batch in enumerate(batches):
            self.logger.debug(f"Processing batch {i + 1}/{len(batches)}")
            
            try:
                # Process batch
                batch_result = await processor.process_batch(batch)
                
                # Store in database
                await connector.store_emails(batch_result.results)
                
                result.successful_items += len(batch)
                
            except Exception as e:
                self.logger.error(f"Batch {i + 1} processing failed", error=str(e))
                result.failed_items += len(batch)
                result.warnings.append(f"Batch {i + 1} failed: {e}")
        
        return result
    
    async def _process_emails_sequential(
        self,
        emails: List[EmailMessage],
        processor: Any,
        connector: Any,
        result: ProcessingResult
    ) -> ProcessingResult:
        """Process emails sequentially."""
        self.logger.debug("Processing emails sequentially", total_emails=len(emails))
        
        for i, email in enumerate(emails):
            try:
                # Process email
                processed_email = await processor.process(email)
                
                # Store in database
                await connector.store_email(processed_email)
                
                result.successful_items += 1
                
                if (i + 1) % 100 == 0:
                    self.logger.debug(f"Processed {i + 1}/{len(emails)} emails")
                
            except Exception as e:
                self.logger.warning(f"Email processing failed", email_id=email.id, error=str(e))
                result.failed_items += 1
                result.warnings.append(f"Email {email.id} failed: {e}")
        
        return result
    
    def get_active_operations(self) -> Dict[UUID, ProcessingResult]:
        """Get currently active operations."""
        return self._active_operations.copy()
    
    def get_operation_status(self, operation_id: UUID) -> Optional[ProcessingResult]:
        """Get status of specific operation."""
        return self._active_operations.get(operation_id)
