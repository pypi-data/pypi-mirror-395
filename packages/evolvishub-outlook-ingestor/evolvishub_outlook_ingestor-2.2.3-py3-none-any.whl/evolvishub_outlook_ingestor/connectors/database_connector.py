"""
Database Connector Interface for Email Ingestion.

This module provides a simplified database connector interface specifically
designed for email ingestion operations. It abstracts the complexity of
different database types and provides a clean interface for storing emails.
"""

import asyncio
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Union
from dataclasses import dataclass

from evolvishub_outlook_ingestor.core.data_models import EmailMessage
from evolvishub_outlook_ingestor.core.exceptions import DatabaseError
from evolvishub_outlook_ingestor.core.logging import LoggerMixin


@dataclass
class DatabaseConfig:
    """Configuration for database connections."""
    database_type: str  # postgresql, mongodb, sqlite, etc.
    host: Optional[str] = None
    port: Optional[int] = None
    database: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
    connection_string: Optional[str] = None
    table_name: str = "emails"
    table_prefix: str = ""  # Prefix for all table names to avoid conflicts
    batch_size: int = 100
    max_connections: int = 10

    # Oracle-specific configurations
    service_name: Optional[str] = None
    encoding: str = "UTF-8"
    nencoding: str = "UTF-8"
    threaded: bool = True
    events: bool = False

    # ClickHouse-specific configurations
    secure: bool = False
    cluster: Optional[str] = None
    compression: bool = True
    session_timeout: int = 60
    send_receive_timeout: int = 300
    verify_ssl: bool = True
    ca_cert: Optional[str] = None
    client_cert: Optional[str] = None
    client_key: Optional[str] = None
    settings: Optional[Dict[str, Any]] = None

    # MS SQL Server-specific configurations
    driver: str = "ODBC Driver 17 for SQL Server"
    trusted_connection: bool = False
    encrypt: bool = True
    trust_server_certificate: bool = False

    # MariaDB/MySQL-specific configurations
    charset: str = "utf8mb4"
    autocommit: bool = False
    connect_timeout: int = 60

    # CockroachDB-specific configurations
    sslmode: str = "prefer"
    server_settings: Optional[Dict[str, str]] = None
    command_timeout: int = 60


class DatabaseConnector(LoggerMixin, ABC):
    """
    Abstract base class for database connectors used in email ingestion.
    
    This provides a simplified interface focused on email storage operations.
    """
    
    def __init__(self, config: DatabaseConfig):
        """
        Initialize database connector.
        
        Args:
            config: Database configuration
        """
        self.config = config
        self._connection = None
        self._is_initialized = False
    
    async def initialize(self) -> bool:
        """
        Initialize the database connection.
        
        Returns:
            True if initialization successful
            
        Raises:
            DatabaseError: If initialization fails
        """
        try:
            await self._connect()
            #await self._create_schema()
            self._is_initialized = True
            self.logger.info(f"Database connector initialized", database_type=self.config.database_type)
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to initialize database connector: {e}")
            raise DatabaseError(f"Failed to initialize database connector: {e}") from e
    
    async def store_emails(self, emails: List[EmailMessage]) -> int:
        """
        Store a list of emails in the database.
        
        Args:
            emails: List of EmailMessage objects to store
            
        Returns:
            Number of emails successfully stored
            
        Raises:
            DatabaseError: If storage operation fails
        """
        if not self._is_initialized:
            raise DatabaseError("Database connector not initialized")
        
        try:
            stored_count = 0
            
            # Process emails in batches
            for i in range(0, len(emails), self.config.batch_size):
                batch = emails[i:i + self.config.batch_size]
                batch_count = await self._store_email_batch(batch)
                stored_count += batch_count
                
                self.logger.debug(f"Stored batch of {batch_count} emails")
            
            self.logger.info(f"Stored {stored_count} emails", total_emails=len(emails))
            return stored_count
            
        except Exception as e:
            self.logger.error(f"Failed to store emails: {e}")
            raise DatabaseError(f"Failed to store emails: {e}") from e
    
    async def store_email(self, email: EmailMessage) -> bool:
        """
        Store a single email in the database.
        
        Args:
            email: EmailMessage object to store
            
        Returns:
            True if storage successful
            
        Raises:
            DatabaseError: If storage operation fails
        """
        if not self._is_initialized:
            raise DatabaseError("Database connector not initialized")
        
        try:
            success = await self._store_single_email(email)
            if success:
                self.logger.debug(f"Stored email", email_id=email.id, subject=email.subject)
            return success
            
        except Exception as e:
            self.logger.error(f"Failed to store email: {e}", email_id=email.id)
            raise DatabaseError(f"Failed to store email: {e}") from e
    
    async def email_exists(self, email_id: str) -> bool:
        """
        Check if an email already exists in the database.
        
        Args:
            email_id: Email ID to check
            
        Returns:
            True if email exists
            
        Raises:
            DatabaseError: If check operation fails
        """
        if not self._is_initialized:
            raise DatabaseError("Database connector not initialized")
        
        try:
            exists = await self._check_email_exists(email_id)
            return exists
            
        except Exception as e:
            self.logger.error(f"Failed to check email existence: {e}", email_id=email_id)
            raise DatabaseError(f"Failed to check email existence: {e}") from e
    
    async def get_email_count(self) -> int:
        """
        Get the total number of emails in the database.
        
        Returns:
            Total number of emails
            
        Raises:
            DatabaseError: If count operation fails
        """
        if not self._is_initialized:
            raise DatabaseError("Database connector not initialized")
        
        try:
            count = await self._get_total_email_count()
            return count
            
        except Exception as e:
            self.logger.error(f"Failed to get email count: {e}")
            raise DatabaseError(f"Failed to get email count: {e}") from e
    
    async def cleanup(self):
        """Clean up database connections and resources."""
        try:
            if self._connection:
                await self._disconnect()
            self._is_initialized = False
            self.logger.info("Database connector cleanup completed")
            
        except Exception as e:
            self.logger.error(f"Failed to cleanup database connector: {e}")
    
    # Abstract methods that must be implemented by concrete connectors
    
    @abstractmethod
    async def _connect(self):
        """Establish database connection."""
        pass
    
    @abstractmethod
    async def _disconnect(self):
        """Close database connection."""
        pass
    
    @abstractmethod
    async def _create_schema(self):
        """Create database schema/tables if they don't exist."""
        pass
    
    @abstractmethod
    async def _store_email_batch(self, emails: List[EmailMessage]) -> int:
        """Store a batch of emails."""
        pass
    
    @abstractmethod
    async def _store_single_email(self, email: EmailMessage) -> bool:
        """Store a single email."""
        pass
    
    @abstractmethod
    async def _check_email_exists(self, email_id: str) -> bool:
        """Check if email exists."""
        pass
    
    @abstractmethod
    async def _get_total_email_count(self) -> int:
        """Get total email count."""
        pass


# Factory function for creating database connectors
def create_database_connector(config: DatabaseConfig) -> DatabaseConnector:
    """
    Create a database connector based on configuration.

    This factory function creates enterprise-ready database connectors
    for production use. Mock implementations are not supported in production
    and should be used only in test environments.

    Args:
        config: Database configuration with connection details

    Returns:
        DatabaseConnector instance ready for production use

    Raises:
        ValueError: If database type is not supported or configuration is invalid
        ImportError: If required database driver is not installed
    """
    database_type = config.database_type.lower()

    # Use lazy imports to avoid circular dependencies
    if database_type == "postgresql":
        try:
            # Lazy import to avoid circular dependency
            import importlib
            module = importlib.import_module("evolvishub_outlook_ingestor.connectors.postgresql_connector")
            PostgreSQLConnector = getattr(module, "PostgreSQLConnector")
            return PostgreSQLConnector(config)
        except ImportError as e:
            raise ValueError(
                "PostgreSQL connector not available. "
                "Install with: pip install 'evolvishub-outlook-ingestor[postgresql]' "
                "or pip install asyncpg"
            ) from e

    elif database_type == "mongodb":
        try:
            # Lazy import to avoid circular dependency
            import importlib
            module = importlib.import_module("evolvishub_outlook_ingestor.connectors.mongodb_connector")
            MongoDBConnector = getattr(module, "MongoDBConnector")
            return MongoDBConnector(config)
        except ImportError as e:
            raise ValueError(
                "MongoDB connector not available. "
                "Install with: pip install 'evolvishub-outlook-ingestor[mongodb]' "
                "or pip install motor"
            ) from e

    elif database_type == "sqlite":
        try:
            # Lazy import to avoid circular dependency
            import importlib
            module = importlib.import_module("evolvishub_outlook_ingestor.connectors.sqlite_connector")
            SQLiteConnector = getattr(module, "SQLiteConnector")
            return SQLiteConnector(config)
        except ImportError as e:
            raise ValueError(
                "SQLite connector not available. "
                "Install with: pip install 'evolvishub-outlook-ingestor[sqlite]' "
                "or pip install aiosqlite"
            ) from e

    elif database_type == "cockroachdb":
        try:
            # Lazy import to avoid circular dependency
            import importlib
            module = importlib.import_module("evolvishub_outlook_ingestor.connectors.cockroachdb_connector")
            CockroachDBDatabaseConnector = getattr(module, "CockroachDBDatabaseConnector")
            return CockroachDBDatabaseConnector(config)
        except ImportError as e:
            raise ValueError(
                "CockroachDB connector not available. "
                "Install with: pip install 'evolvishub-outlook-ingestor[cockroachdb]' "
                "or pip install asyncpg"
            ) from e

    elif database_type == "mssql" or database_type == "sqlserver":
        try:
            # Lazy import to avoid circular dependency
            import importlib
            module = importlib.import_module("evolvishub_outlook_ingestor.connectors.mssql_connector")
            MSSQLDatabaseConnector = getattr(module, "MSSQLDatabaseConnector")
            return MSSQLDatabaseConnector(config)
        except ImportError as e:
            raise ValueError(
                "MS SQL Server connector not available. "
                "Install with: pip install 'evolvishub-outlook-ingestor[mssql]' "
                "or pip install aioodbc pyodbc"
            ) from e

    elif database_type == "mariadb":
        try:
            # Lazy import to avoid circular dependency
            import importlib
            module = importlib.import_module("evolvishub_outlook_ingestor.connectors.mariadb_connector")
            MariaDBDatabaseConnector = getattr(module, "MariaDBDatabaseConnector")
            return MariaDBDatabaseConnector(config)
        except ImportError as e:
            raise ValueError(
                "MariaDB connector not available. "
                "Install with: pip install 'evolvishub-outlook-ingestor[mariadb]' "
                "or pip install aiomysql"
            ) from e

    elif database_type == "oracle":
        try:
            # Lazy import to avoid circular dependency
            import importlib
            module = importlib.import_module("evolvishub_outlook_ingestor.connectors.oracle_connector")
            OracleDatabaseConnector = getattr(module, "OracleDatabaseConnector")
            return OracleDatabaseConnector(config)
        except ImportError as e:
            raise ValueError(
                "Oracle connector not available. "
                "Install with: pip install 'evolvishub-outlook-ingestor[oracle]' "
                "or pip install cx_Oracle"
            ) from e

    elif database_type == "clickhouse":
        try:
            # Lazy import to avoid circular dependency
            import importlib
            module = importlib.import_module("evolvishub_outlook_ingestor.connectors.clickhouse_connector")
            ClickHouseDatabaseConnector = getattr(module, "ClickHouseDatabaseConnector")
            return ClickHouseDatabaseConnector(config)
        except ImportError as e:
            raise ValueError(
                "ClickHouse connector not available. "
                "Install with: pip install 'evolvishub-outlook-ingestor[clickhouse]' "
                "or pip install clickhouse-connect"
            ) from e

    else:
        supported_types = [
            "postgresql", "mongodb", "sqlite", "cockroachdb",
            "mssql", "sqlserver", "mariadb", "oracle", "clickhouse"
        ]
        raise ValueError(
            f"Unsupported database type: '{config.database_type}'. "
            f"Supported types: {', '.join(supported_types)}"
        )
