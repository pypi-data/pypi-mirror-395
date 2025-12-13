"""
Base database connector for Evolvishub Outlook Ingestor.

This module defines the abstract base class that all database connectors
must implement. It provides a consistent interface for:
- Connection management with pooling
- Transaction support
- Email storage operations
- Batch operations
- Error handling
- Performance monitoring

All database connectors (PostgreSQL, MongoDB, MySQL) inherit from this
base class to ensure consistent behavior and easy interchangeability.
"""

import asyncio
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Dict, List, Optional, Union
from uuid import UUID

from evolvishub_outlook_ingestor.core.data_models import EmailMessage, EmailAttachment, OutlookFolder
from evolvishub_outlook_ingestor.core.exceptions import ConnectionError, DatabaseError, QueryError
from evolvishub_outlook_ingestor.core.logging import LoggerMixin


class ConnectionPool:
    """Connection pool management."""
    
    def __init__(
        self,
        min_size: int = 5,
        max_size: int = 20,
        max_idle_time: int = 300,  # 5 minutes
    ):
        self.min_size = min_size
        self.max_size = max_size
        self.max_idle_time = max_idle_time
        self.active_connections = 0
        self.idle_connections = []
        self.created_at = datetime.utcnow()
        self.last_cleanup = datetime.utcnow()


class TransactionContext:
    """Transaction context for database operations."""
    
    def __init__(self, connector: "BaseConnector", isolation_level: Optional[str] = None):
        self.connector = connector
        self.isolation_level = isolation_level
        self.transaction = None
        self.is_active = False
    
    async def __aenter__(self):
        """Start transaction."""
        self.transaction = await self.connector._begin_transaction(self.isolation_level)
        self.is_active = True
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """End transaction."""
        if self.is_active and self.transaction:
            try:
                if exc_type is None:
                    await self.connector._commit_transaction(self.transaction)
                else:
                    await self.connector._rollback_transaction(self.transaction)
            finally:
                self.is_active = False
                self.transaction = None


class BaseConnector(ABC, LoggerMixin):
    """
    Abstract base class for database connectors in the Evolvishub Outlook Ingestor.

    This class provides a unified interface for all database connectors, ensuring
    consistent behavior across different database systems including PostgreSQL,
    MongoDB, and MySQL. It implements common patterns for connection management,
    transaction handling, and data operations.

    The connector supports both individual and pooled connections, automatic
    retry logic, comprehensive error handling, and performance monitoring.
    All database operations are asynchronous for optimal performance.

    Attributes:
        name (str): Unique identifier for this connector instance
        config (Dict[str, Any]): Configuration dictionary containing connection parameters
        enable_connection_pooling (bool): Whether to use connection pooling
        pool_size (int): Maximum number of connections in the pool
        logger (logging.Logger): Logger instance for this connector

    Example:
        ```python
        # Initialize a PostgreSQL connector
        config = {
            "host": "localhost",
            "port": 5432,
            "database": "emails",
            "username": "user",
            "password": "pass",
            "enable_connection_pooling": True,
            "pool_size": 10
        }

        connector = PostgreSQLConnector("main_db", config)

        # Use as async context manager (recommended)
        async with connector:
            email_id = await connector.store_email(email_message)
            retrieved_email = await connector.get_email(email_id)
        ```

    Note:
        This is an abstract base class and cannot be instantiated directly.
        Use concrete implementations like PostgreSQLConnector or MongoDBConnector.

    See Also:
        - PostgreSQLConnector: PostgreSQL-specific implementation
        - MongoDBConnector: MongoDB-specific implementation
        - EmailMessage: Data model for email objects
    """
    
    def __init__(
        self,
        name: str,
        config: Dict[str, Any],
        enable_connection_pooling: bool = True,
        pool_min_size: int = 5,
        pool_max_size: int = 20,
    ):
        """
        Initialize the database connector.
        
        Args:
            name: Connector name
            config: Configuration dictionary
            enable_connection_pooling: Enable connection pooling
            pool_min_size: Minimum pool size
            pool_max_size: Maximum pool size
        """
        self.name = name
        self.config = config
        self.enable_connection_pooling = enable_connection_pooling
        
        # Connection management
        self._connection_pool = None
        self._connection = None
        self._is_connected = False
        
        # Pool configuration
        if enable_connection_pooling:
            self._pool_config = ConnectionPool(
                min_size=pool_min_size,
                max_size=pool_max_size
            )
        
        # Performance tracking
        self._operation_count = 0
        self._error_count = 0
        self._last_operation = None
    
    async def initialize(self) -> None:
        """
        Initialize the database connector and establish connections.

        This method sets up the database connection or connection pool,
        initializes the database schema if needed, and performs any
        necessary setup operations. It should be called before using
        any other connector methods.

        The initialization process includes:
        - Establishing database connection(s)
        - Setting up connection pooling if enabled
        - Testing the connection
        - Initializing database schema/tables
        - Setting up monitoring and logging

        Raises:
            ConnectionError: If unable to establish database connection
            DatabaseError: If database setup or schema initialization fails
            ConfigurationError: If configuration is invalid or incomplete

        Example:
            ```python
            connector = PostgreSQLConnector("main_db", config)
            await connector.initialize()

            # Now ready to use
            await connector.store_email(email)
            ```

        Note:
            This method is automatically called when using the connector
            as an async context manager.
        """
        self.logger.info("Initializing database connector", connector=self.name)
        
        try:
            if self.enable_connection_pooling:
                await self._initialize_pool()
            else:
                await self._initialize_connection()
            
            # Test connection
            await self._test_connection()
            
            # Initialize schema if needed
            await self._initialize_schema()
            
            self._is_connected = True
            
            self.logger.info("Database connector initialized successfully", connector=self.name)
            
        except Exception as e:
            self._error_count += 1
            
            self.logger.error(
                "Failed to initialize database connector",
                connector=self.name,
                error=str(e)
            )
            
            raise ConnectionError(
                f"Failed to initialize {self.name} connector: {e}",
                database_type=self.name,
                cause=e
            )
    
    async def cleanup(self) -> None:
        """Cleanup database connector resources."""
        self.logger.info("Cleaning up database connector", connector=self.name)
        
        try:
            if self.enable_connection_pooling and self._connection_pool:
                await self._cleanup_pool()
            elif self._connection:
                await self._cleanup_connection()
            
            self._is_connected = False
            
            self.logger.info("Database connector cleanup completed", connector=self.name)
            
        except Exception as e:
            self.logger.warning(
                "Error during database connector cleanup",
                connector=self.name,
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
                "Exception occurred in connector context",
                connector=self.name,
                exception_type=exc_type.__name__,
                exception_message=str(exc_val)
            )

        # Don't suppress exceptions
        return False

    async def store_email(
        self,
        email: EmailMessage,
        transaction: Optional[Any] = None,
        **kwargs
    ) -> str:
        """
        Store a single email message in the database.

        This method persists an EmailMessage object to the database,
        including all associated metadata, attachments, and relationships.
        The operation is atomic and will either succeed completely or
        fail without partial data corruption.

        Args:
            email (EmailMessage): The email message to store. Must be a valid
                EmailMessage instance with required fields populated.
            transaction (Optional[Any]): Database transaction context to use.
                If provided, the operation will be part of the existing transaction.
                If None, a new transaction will be created automatically.
            **kwargs: Additional database-specific parameters that may be
                passed to the underlying storage implementation.

        Returns:
            str: The unique identifier assigned to the stored email.
                This ID can be used to retrieve the email later.

        Raises:
            DatabaseError: If the email cannot be stored due to database issues
            ValidationError: If the email data is invalid or incomplete
            DuplicateError: If an email with the same ID already exists
            ConnectionError: If the database connection is not available

        Example:
            ```python
            email = EmailMessage(
                id="msg_001",
                subject="Test Email",
                body="Hello World",
                sender=EmailAddress(email="sender@example.com"),
                # ... other required fields
            )

            # Store with automatic transaction
            email_id = await connector.store_email(email)
            print(f"Stored email with ID: {email_id}")

            # Store within existing transaction
            async with connector.transaction() as tx:
                email_id = await connector.store_email(email, transaction=tx)
                # Other operations in same transaction...
            ```

        Note:
            - The email ID should be unique across the database
            - Large attachments may be stored separately for performance
            - The operation includes automatic retry logic for transient failures
            - All sensitive data is properly sanitized before storage
        """
        if not self._is_connected:
            await self.initialize()
        
        self.logger.debug("Storing email", email_id=email.id, connector=self.name)
        
        try:
            self._operation_count += 1
            self._last_operation = datetime.utcnow()
            
            email_id = await self._store_email_impl(email, transaction, **kwargs)
            
            self.logger.debug(
                "Email stored successfully",
                email_id=email_id,
                connector=self.name
            )
            
            return email_id
            
        except Exception as e:
            self._error_count += 1
            
            self.logger.error(
                "Failed to store email",
                email_id=email.id,
                connector=self.name,
                error=str(e)
            )
            
            raise DatabaseError(
                f"Failed to store email: {e}",
                database_type=self.name,
                operation="store_email",
                cause=e
            )
    
    async def store_emails_batch(
        self,
        emails: List[EmailMessage],
        batch_size: int = 100,
        transaction: Optional[Any] = None,
        **kwargs
    ) -> List[str]:
        """
        Store multiple emails in batches.
        
        Args:
            emails: List of EmailMessage objects to store
            batch_size: Number of emails per batch
            transaction: Optional transaction context
            **kwargs: Additional parameters
            
        Returns:
            List of stored email IDs
        """
        if not self._is_connected:
            await self.initialize()
        
        self.logger.info(
            "Storing emails in batches",
            total_emails=len(emails),
            batch_size=batch_size,
            connector=self.name
        )
        
        try:
            stored_ids = []
            
            # Process in batches
            for i in range(0, len(emails), batch_size):
                batch = emails[i:i + batch_size]
                
                self.logger.debug(
                    f"Processing batch {i // batch_size + 1}",
                    batch_size=len(batch),
                    connector=self.name
                )
                
                batch_ids = await self._store_emails_batch_impl(batch, transaction, **kwargs)
                stored_ids.extend(batch_ids)
                
                self._operation_count += len(batch)
            
            self._last_operation = datetime.utcnow()
            
            self.logger.info(
                "Emails stored successfully",
                total_stored=len(stored_ids),
                connector=self.name
            )
            
            return stored_ids
            
        except Exception as e:
            self._error_count += 1
            
            self.logger.error(
                "Failed to store emails batch",
                total_emails=len(emails),
                connector=self.name,
                error=str(e)
            )
            
            raise DatabaseError(
                f"Failed to store emails batch: {e}",
                database_type=self.name,
                operation="store_emails_batch",
                cause=e
            )
    
    async def get_email(
        self,
        email_id: str,
        include_attachments: bool = True,
        **kwargs
    ) -> Optional[EmailMessage]:
        """
        Retrieve an email by ID.
        
        Args:
            email_id: Email ID to retrieve
            include_attachments: Whether to include attachments
            **kwargs: Additional parameters
            
        Returns:
            EmailMessage if found, None otherwise
        """
        if not self._is_connected:
            await self.initialize()
        
        self.logger.debug("Retrieving email", email_id=email_id, connector=self.name)
        
        try:
            self._operation_count += 1
            self._last_operation = datetime.utcnow()
            
            email = await self._get_email_impl(email_id, include_attachments, **kwargs)
            
            if email:
                self.logger.debug(
                    "Email retrieved successfully",
                    email_id=email_id,
                    connector=self.name
                )
            else:
                self.logger.debug(
                    "Email not found",
                    email_id=email_id,
                    connector=self.name
                )
            
            return email
            
        except Exception as e:
            self._error_count += 1
            
            self.logger.error(
                "Failed to retrieve email",
                email_id=email_id,
                connector=self.name,
                error=str(e)
            )
            
            raise DatabaseError(
                f"Failed to retrieve email: {e}",
                database_type=self.name,
                operation="get_email",
                cause=e
            )
    
    async def search_emails(
        self,
        filters: Dict[str, Any],
        limit: Optional[int] = None,
        offset: int = 0,
        sort_by: Optional[str] = None,
        sort_order: str = "desc",
        **kwargs
    ) -> List[EmailMessage]:
        """
        Search emails based on filters.
        
        Args:
            filters: Search filters
            limit: Maximum number of results
            offset: Result offset for pagination
            sort_by: Field to sort by
            sort_order: Sort order (asc/desc)
            **kwargs: Additional parameters
            
        Returns:
            List of matching EmailMessage objects
        """
        if not self._is_connected:
            await self.initialize()
        
        self.logger.debug(
            "Searching emails",
            filters=filters,
            limit=limit,
            connector=self.name
        )
        
        try:
            self._operation_count += 1
            self._last_operation = datetime.utcnow()
            
            emails = await self._search_emails_impl(
                filters, limit, offset, sort_by, sort_order, **kwargs
            )
            
            self.logger.debug(
                "Email search completed",
                results_count=len(emails),
                connector=self.name
            )
            
            return emails
            
        except Exception as e:
            self._error_count += 1
            
            self.logger.error(
                "Failed to search emails",
                filters=filters,
                connector=self.name,
                error=str(e)
            )
            
            raise DatabaseError(
                f"Failed to search emails: {e}",
                database_type=self.name,
                operation="search_emails",
                cause=e
            )
    
    def transaction(self, isolation_level: Optional[str] = None) -> TransactionContext:
        """
        Create a transaction context.
        
        Args:
            isolation_level: Transaction isolation level
            
        Returns:
            TransactionContext for use with async with
        """
        return TransactionContext(self, isolation_level)
    
    def get_status(self) -> Dict[str, Any]:
        """Get connector status information."""
        return {
            "connector": self.name,
            "is_connected": self._is_connected,
            "operation_count": self._operation_count,
            "error_count": self._error_count,
            "last_operation": self._last_operation,
            "error_rate": self._error_count / max(self._operation_count, 1),
        }
    
    # Abstract methods that must be implemented by subclasses
    
    @abstractmethod
    async def _initialize_connection(self) -> None:
        """Initialize database connection."""
        pass
    
    @abstractmethod
    async def _initialize_pool(self) -> None:
        """Initialize connection pool."""
        pass
    
    @abstractmethod
    async def _cleanup_connection(self) -> None:
        """Cleanup database connection."""
        pass
    
    @abstractmethod
    async def _cleanup_pool(self) -> None:
        """Cleanup connection pool."""
        pass
    
    @abstractmethod
    async def _test_connection(self) -> None:
        """Test database connection."""
        pass
    
    @abstractmethod
    async def _initialize_schema(self) -> None:
        """Initialize database schema if needed."""
        pass
    
    @abstractmethod
    async def _store_email_impl(
        self,
        email: EmailMessage,
        transaction: Optional[Any] = None,
        **kwargs
    ) -> str:
        """Implementation-specific email storage."""
        pass
    
    @abstractmethod
    async def _store_emails_batch_impl(
        self,
        emails: List[EmailMessage],
        transaction: Optional[Any] = None,
        **kwargs
    ) -> List[str]:
        """Implementation-specific batch email storage."""
        pass
    
    @abstractmethod
    async def _get_email_impl(
        self,
        email_id: str,
        include_attachments: bool = True,
        **kwargs
    ) -> Optional[EmailMessage]:
        """Implementation-specific email retrieval."""
        pass
    
    @abstractmethod
    async def _search_emails_impl(
        self,
        filters: Dict[str, Any],
        limit: Optional[int] = None,
        offset: int = 0,
        sort_by: Optional[str] = None,
        sort_order: str = "desc",
        **kwargs
    ) -> List[EmailMessage]:
        """Implementation-specific email search."""
        pass
    
    @abstractmethod
    async def _begin_transaction(self, isolation_level: Optional[str] = None) -> Any:
        """Begin database transaction."""
        pass
    
    @abstractmethod
    async def _commit_transaction(self, transaction: Any) -> None:
        """Commit database transaction."""
        pass
    
    @abstractmethod
    async def _rollback_transaction(self, transaction: Any) -> None:
        """Rollback database transaction."""
        pass
