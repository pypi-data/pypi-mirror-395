"""
Oracle Database connector for Evolvishub Outlook Ingestor.

This module implements the Oracle database connector using cx_Oracle
for enterprise environments with existing Oracle infrastructure.

Features:
- Async database operations with cx_Oracle and asyncio
- Connection pooling for high throughput
- Proper database schema with indexes and partitioning
- Batch insert operations with MERGE statements
- Transaction support with isolation levels
- JSON fields for email metadata and headers (Oracle 12c+)
- Full-text search capabilities with Oracle Text
- Optimized for Oracle performance features
"""

import asyncio
import json
import os
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from uuid import UUID

try:
    import cx_Oracle
    ORACLE_AVAILABLE = True
except ImportError:
    ORACLE_AVAILABLE = False
    cx_Oracle = None

from evolvishub_outlook_ingestor.connectors.base_connector import BaseConnector
from evolvishub_outlook_ingestor.core.data_models import EmailMessage, EmailAttachment
from evolvishub_outlook_ingestor.core.exceptions import (
    ConnectionError,
    DatabaseError,
    QueryError,
    TransactionError,
)

# Import security utilities with lazy loading to avoid circular imports
def _get_security_utils():
    from evolvishub_outlook_ingestor.utils.security import (
        get_credential_manager,
        create_secure_dsn,
        mask_sensitive_data,
        sanitize_input,
    )
    return get_credential_manager, create_secure_dsn, mask_sensitive_data, sanitize_input


class OracleConnector(BaseConnector):
    """Oracle database connector using cx_Oracle."""
    
    def __init__(self, name: str, config: Dict[str, Any], **kwargs):
        """
        Initialize Oracle connector.
        
        Args:
            name: Connector name
            config: Configuration dictionary containing:
                - host: Oracle host
                - port: Oracle port (default: 1521)
                - service_name: Oracle service name
                - sid: Oracle SID (alternative to service_name)
                - username: Database username
                - password: Database password
                - wallet_location: Oracle Wallet location for SSL
                - wallet_password: Oracle Wallet password
                - encoding: Character encoding (default: UTF-8)
                - nencoding: National character encoding (default: UTF-8)
                - threaded: Use threaded mode (default: True)
                - events: Enable events (default: True)
                - pool_size: Connection pool size
                - max_overflow: Maximum pool overflow
                - pool_increment: Pool increment size
                - pool_timeout: Pool timeout in seconds
        """
        if not ORACLE_AVAILABLE:
            raise ImportError(
                "cx_Oracle is required for Oracle connector. "
                "Install with: pip install cx_Oracle"
            )
        
        super().__init__(name, config, **kwargs)

        # Get credential manager (lazy loading)
        get_credential_manager, create_secure_dsn, _, _ = _get_security_utils()
        self._credential_manager = get_credential_manager()
        self._create_secure_dsn = create_secure_dsn

        # Oracle configuration
        self.host = config.get("host", "localhost")
        self.port = config.get("port", 1521)
        self.service_name = config.get("service_name", "")
        self.sid = config.get("sid", "")
        self.username = config.get("username", "")
        self.wallet_location = config.get("wallet_location", "")
        self.wallet_password = config.get("wallet_password", "")
        self.encoding = config.get("encoding", "UTF-8")
        self.nencoding = config.get("nencoding", "UTF-8")
        self.threaded = config.get("threaded", True)
        self.events = config.get("events", True)
        self.pool_increment = config.get("pool_increment", 1)
        self.pool_timeout = config.get("pool_timeout", 30)

        # Secure password handling
        password_raw = config.get("password", "")
        password_env = config.get("password_env", "ORACLE_PASSWORD")

        # Try to get password from environment first, then from config
        self._password = (
            self._credential_manager.get_credential_from_env(password_env) or
            password_raw
        )

        # Encrypt password for storage
        if self._password:
            self._encrypted_password = self._credential_manager.encrypt_credential(self._password)
        else:
            self._encrypted_password = ""
        
        # Connection pool
        self.pool: Optional[cx_Oracle.SessionPool] = None
        
        # Schema definitions
        self.schema_sql = self._get_schema_sql()
        
        # Initialize Oracle client if needed
        self._init_oracle_client()
    
    def _init_oracle_client(self) -> None:
        """Initialize Oracle client."""
        try:
            # Set Oracle client library path if needed
            oracle_client_lib = os.environ.get("ORACLE_CLIENT_LIB")
            if oracle_client_lib and not cx_Oracle.clientversion():
                cx_Oracle.init_oracle_client(lib_dir=oracle_client_lib)
                
            # Set wallet location if provided
            if self.wallet_location:
                os.environ["TNS_ADMIN"] = self.wallet_location
                
        except Exception as e:
            self.logger.warning(
                "Failed to initialize Oracle client",
                error=str(e),
                connector=self.name
            )
    
    async def _initialize_connection(self) -> None:
        """Initialize single Oracle connection (not used with pooling)."""
        try:
            # Decrypt password for connection
            password = ""
            if self._encrypted_password:
                password = self._credential_manager.decrypt_credential(self._encrypted_password)
            
            dsn = self._build_dsn()
            
            self.logger.info(
                "Connecting to Oracle",
                host=self.host,
                service_name=self.service_name,
                connector=self.name
            )
            
            # Create connection in thread pool since cx_Oracle is synchronous
            loop = asyncio.get_event_loop()
            self._connection = await loop.run_in_executor(
                None,
                lambda: cx_Oracle.connect(
                    user=self.username,
                    password=password,
                    dsn=dsn,
                    encoding=self.encoding,
                    nencoding=self.nencoding,
                    threaded=self.threaded,
                    events=self.events
                )
            )
            
            self.logger.info(
                "Oracle connection established",
                host=self.host,
                service_name=self.service_name,
                connector=self.name
            )
            
        except Exception as e:
            raise ConnectionError(
                f"Failed to connect to Oracle: {e}",
                database_type="oracle",
                cause=e
            )
    
    async def _initialize_pool(self) -> None:
        """Initialize Oracle connection pool."""
        try:
            # Decrypt password for connection
            password = ""
            if self._encrypted_password:
                password = self._credential_manager.decrypt_credential(self._encrypted_password)
            
            dsn = self._build_dsn()
            
            self.logger.info(
                "Creating Oracle connection pool",
                host=self.host,
                service_name=self.service_name,
                pool_size=self._pool_config.max_size,
                connector=self.name
            )
            
            # Create pool in thread pool since cx_Oracle is synchronous
            loop = asyncio.get_event_loop()
            self.pool = await loop.run_in_executor(
                None,
                lambda: cx_Oracle.SessionPool(
                    user=self.username,
                    password=password,
                    dsn=dsn,
                    min=self._pool_config.min_size,
                    max=self._pool_config.max_size,
                    increment=self.pool_increment,
                    encoding=self.encoding,
                    nencoding=self.nencoding,
                    threaded=self.threaded,
                    getmode=cx_Oracle.SPOOL_ATTRVAL_WAIT,
                    timeout=self.pool_timeout
                )
            )
            
            self.logger.info(
                "Oracle connection pool created",
                host=self.host,
                service_name=self.service_name,
                connector=self.name
            )
            
        except Exception as e:
            raise ConnectionError(
                f"Failed to create Oracle connection pool: {e}",
                database_type="oracle",
                cause=e
            )
    
    async def _cleanup_connection(self) -> None:
        """Cleanup Oracle connection."""
        if self._connection:
            try:
                loop = asyncio.get_event_loop()
                await loop.run_in_executor(None, self._connection.close)
                self.logger.info("Oracle connection closed", connector=self.name)
            except Exception as e:
                self.logger.warning(
                    "Error closing Oracle connection",
                    connector=self.name,
                    error=str(e)
                )
            finally:
                self._connection = None
    
    async def _cleanup_pool(self) -> None:
        """Cleanup Oracle connection pool."""
        if self.pool:
            try:
                loop = asyncio.get_event_loop()
                await loop.run_in_executor(None, self.pool.close)
                self.logger.info("Oracle connection pool closed", connector=self.name)
            except Exception as e:
                self.logger.warning(
                    "Error closing Oracle connection pool",
                    connector=self.name,
                    error=str(e)
                )
            finally:
                self.pool = None
    
    async def _test_connection(self) -> None:
        """Test Oracle connection."""
        try:
            if self.enable_connection_pooling:
                loop = asyncio.get_event_loop()
                connection = await loop.run_in_executor(None, self.pool.acquire)
                try:
                    cursor = await loop.run_in_executor(None, connection.cursor)
                    await loop.run_in_executor(None, cursor.execute, "SELECT 1 FROM DUAL")
                    result = await loop.run_in_executor(None, cursor.fetchone)
                    if result[0] != 1:
                        raise ConnectionError("Oracle connection test failed")
                    await loop.run_in_executor(None, cursor.close)
                finally:
                    await loop.run_in_executor(None, self.pool.release, connection)
            else:
                loop = asyncio.get_event_loop()
                cursor = await loop.run_in_executor(None, self._connection.cursor)
                await loop.run_in_executor(None, cursor.execute, "SELECT 1 FROM DUAL")
                result = await loop.run_in_executor(None, cursor.fetchone)
                if result[0] != 1:
                    raise ConnectionError("Oracle connection test failed")
                await loop.run_in_executor(None, cursor.close)
                        
            self.logger.debug("Oracle connection test passed", connector=self.name)
            
        except Exception as e:
            raise ConnectionError(f"Oracle connection test failed: {e}")
    
    def _build_dsn(self) -> str:
        """Build Oracle DSN."""
        if self.service_name:
            return cx_Oracle.makedsn(
                host=self.host,
                port=self.port,
                service_name=self.service_name
            )
        elif self.sid:
            return cx_Oracle.makedsn(
                host=self.host,
                port=self.port,
                sid=self.sid
            )
        else:
            raise ConnectionError("Either service_name or sid must be provided for Oracle connection")
    
    def _get_schema_sql(self) -> List[str]:
        """Get Oracle schema SQL statements."""
        return [
            # Emails table
            """
            CREATE TABLE emails (
                id VARCHAR2(255) PRIMARY KEY,
                message_id VARCHAR2(255) UNIQUE,
                subject CLOB,
                body CLOB,
                body_preview CLOB,
                sender_email VARCHAR2(255),
                sender_name VARCHAR2(255),
                received_date TIMESTAMP,
                sent_date TIMESTAMP,
                importance VARCHAR2(50),
                is_read NUMBER(1) DEFAULT 0,
                has_attachments NUMBER(1) DEFAULT 0,
                folder_id VARCHAR2(255),
                folder_name VARCHAR2(255),
                categories CLOB CHECK (categories IS JSON),  -- JSON constraint for Oracle 12c+
                headers CLOB CHECK (headers IS JSON),        -- JSON constraint for Oracle 12c+
                metadata CLOB CHECK (metadata IS JSON),      -- JSON constraint for Oracle 12c+
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """,
            
            # Recipients table
            """
            CREATE TABLE email_recipients (
                id NUMBER GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
                email_id VARCHAR2(255) NOT NULL,
                recipient_type VARCHAR2(10) NOT NULL CHECK (recipient_type IN ('to', 'cc', 'bcc')),
                email_address VARCHAR2(255) NOT NULL,
                display_name VARCHAR2(255),
                CONSTRAINT fk_recipients_email FOREIGN KEY (email_id) REFERENCES emails (id) ON DELETE CASCADE
            )
            """,

            # Attachments table
            """
            CREATE TABLE email_attachments (
                id VARCHAR2(255) PRIMARY KEY,
                email_id VARCHAR2(255) NOT NULL,
                name VARCHAR2(255) NOT NULL,
                content_type VARCHAR2(255),
                size NUMBER,
                content BLOB,  -- For small attachments stored in database
                content_hash VARCHAR2(255),
                is_inline NUMBER(1) DEFAULT 0,
                attachment_type VARCHAR2(50),
                extended_properties CLOB CHECK (extended_properties IS JSON),  -- JSON for storage info
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                CONSTRAINT fk_attachments_email FOREIGN KEY (email_id) REFERENCES emails (id) ON DELETE CASCADE
            )
            """,

            # Folders table
            """
            CREATE TABLE outlook_folders (
                id VARCHAR2(255) PRIMARY KEY,
                name VARCHAR2(255) NOT NULL,
                parent_folder_id VARCHAR2(255),
                folder_type VARCHAR2(50),
                total_item_count NUMBER DEFAULT 0,
                unread_item_count NUMBER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """,

            # Indexes for performance
            "CREATE INDEX idx_emails_message_id ON emails (message_id)",
            "CREATE INDEX idx_emails_sender ON emails (sender_email)",
            "CREATE INDEX idx_emails_received_date ON emails (received_date)",
            "CREATE INDEX idx_emails_folder ON emails (folder_id)",
            "CREATE INDEX idx_emails_has_attachments ON emails (has_attachments)",
            "CREATE INDEX idx_recipients_email_id ON email_recipients (email_id)",
            "CREATE INDEX idx_recipients_type ON email_recipients (recipient_type)",
            "CREATE INDEX idx_attachments_email_id ON email_attachments (email_id)",
            "CREATE INDEX idx_attachments_hash ON email_attachments (content_hash)",
            "CREATE INDEX idx_folders_parent ON outlook_folders (parent_folder_id)",

            # Update trigger for emails table
            """
            CREATE OR REPLACE TRIGGER trg_emails_updated_at
            BEFORE UPDATE ON emails
            FOR EACH ROW
            BEGIN
                :NEW.updated_at := CURRENT_TIMESTAMP;
            END;
            """,

            # Update trigger for folders table
            """
            CREATE OR REPLACE TRIGGER trg_folders_updated_at
            BEFORE UPDATE ON outlook_folders
            FOR EACH ROW
            BEGIN
                :NEW.updated_at := CURRENT_TIMESTAMP;
            END;
            """
        ]

    async def _initialize_schema(self) -> None:
        """Initialize Oracle database schema."""
        try:
            self.logger.info("Initializing Oracle schema", connector=self.name)

            if self.enable_connection_pooling:
                loop = asyncio.get_event_loop()
                connection = await loop.run_in_executor(None, self.pool.acquire)
                try:
                    await self._execute_schema_statements(connection)
                finally:
                    await loop.run_in_executor(None, self.pool.release, connection)
            else:
                await self._execute_schema_statements(self._connection)

            self.logger.info("Oracle schema initialized", connector=self.name)

        except Exception as e:
            raise DatabaseError(
                f"Failed to initialize Oracle schema: {e}",
                database_type="oracle",
                operation="initialize_schema",
                cause=e
            )

    async def _execute_schema_statements(self, connection) -> None:
        """Execute schema creation statements."""
        loop = asyncio.get_event_loop()

        for statement in self.schema_sql:
            try:
                cursor = await loop.run_in_executor(None, connection.cursor)
                try:
                    await loop.run_in_executor(None, cursor.execute, statement)
                    await loop.run_in_executor(None, connection.commit)
                finally:
                    await loop.run_in_executor(None, cursor.close)
            except Exception as e:
                self.logger.warning(
                    "Schema statement failed (may already exist)",
                    statement=statement[:100] + "..." if len(statement) > 100 else statement,
                    error=str(e),
                    connector=self.name
                )

    async def _store_email_impl(
        self,
        email: EmailMessage,
        transaction: Optional[Any] = None,
        **kwargs
    ) -> str:
        """Store email in Oracle database."""
        try:
            if self.enable_connection_pooling:
                loop = asyncio.get_event_loop()
                connection = transaction if transaction else await loop.run_in_executor(None, self.pool.acquire)
                try:
                    return await self._store_email_with_connection(email, connection, transaction)
                finally:
                    if not transaction:
                        await loop.run_in_executor(None, self.pool.release, connection)
            else:
                return await self._store_email_with_connection(email, self._connection, transaction)

        except Exception as e:
            raise DatabaseError(
                f"Failed to store email in Oracle: {e}",
                database_type="oracle",
                operation="store_email",
                cause=e
            )

    async def _store_email_with_connection(self, email: EmailMessage, connection, transaction: Optional[Any] = None) -> str:
        """Store email with specific connection."""
        loop = asyncio.get_event_loop()
        cursor = await loop.run_in_executor(None, connection.cursor)

        try:
            # Prepare email data
            email_data = self._prepare_email_data(email)

            # Use MERGE statement for upsert
            merge_sql = """
            MERGE INTO emails e
            USING (SELECT :1 as id, :2 as message_id, :3 as subject, :4 as body, :5 as body_preview,
                          :6 as sender_email, :7 as sender_name, :8 as received_date, :9 as sent_date,
                          :10 as importance, :11 as is_read, :12 as has_attachments, :13 as folder_id, :14 as folder_name,
                          :15 as categories, :16 as headers, :17 as metadata, :18 as updated_at
                   FROM DUAL) s
            ON (e.id = s.id)
            WHEN MATCHED THEN
                UPDATE SET
                    message_id = s.message_id,
                    subject = s.subject,
                    body = s.body,
                    body_preview = s.body_preview,
                    sender_email = s.sender_email,
                    sender_name = s.sender_name,
                    received_date = s.received_date,
                    sent_date = s.sent_date,
                    importance = s.importance,
                    is_read = s.is_read,
                    has_attachments = s.has_attachments,
                    folder_id = s.folder_id,
                    folder_name = s.folder_name,
                    categories = s.categories,
                    headers = s.headers,
                    metadata = s.metadata,
                    updated_at = s.updated_at
            WHEN NOT MATCHED THEN
                INSERT (id, message_id, subject, body, body_preview,
                       sender_email, sender_name, received_date, sent_date,
                       importance, is_read, has_attachments, folder_id, folder_name,
                       categories, headers, metadata, updated_at)
                VALUES (s.id, s.message_id, s.subject, s.body, s.body_preview,
                       s.sender_email, s.sender_name, s.received_date, s.sent_date,
                       s.importance, s.is_read, s.has_attachments, s.folder_id, s.folder_name,
                       s.categories, s.headers, s.metadata, s.updated_at)
            """

            await loop.run_in_executor(None, cursor.execute, merge_sql, email_data)

            # Store recipients
            if email.recipients:
                await self._store_recipients_with_cursor(cursor, email.id, email.recipients)

            # Store attachments
            if email.attachments:
                await self._store_attachments_with_cursor(cursor, email.id, email.attachments)

            if not transaction:
                await loop.run_in_executor(None, connection.commit)

            return email.id

        finally:
            await loop.run_in_executor(None, cursor.close)

    async def _get_email_impl(
        self,
        email_id: str,
        include_attachments: bool = True,
        **kwargs
    ) -> Optional[EmailMessage]:
        """Retrieve email from Oracle database."""
        try:
            if self.enable_connection_pooling:
                loop = asyncio.get_event_loop()
                connection = await loop.run_in_executor(None, self.pool.acquire)
                try:
                    return await self._get_email_with_connection(email_id, include_attachments, connection)
                finally:
                    await loop.run_in_executor(None, self.pool.release, connection)
            else:
                return await self._get_email_with_connection(email_id, include_attachments, self._connection)

        except Exception as e:
            raise DatabaseError(
                f"Failed to retrieve email from Oracle: {e}",
                database_type="oracle",
                operation="get_email",
                cause=e
            )

    async def _get_email_with_connection(
        self,
        email_id: str,
        include_attachments: bool,
        connection
    ) -> Optional[EmailMessage]:
        """Retrieve email with specific connection."""
        loop = asyncio.get_event_loop()
        cursor = await loop.run_in_executor(None, connection.cursor)

        try:
            # Get email data
            await loop.run_in_executor(None, cursor.execute, "SELECT * FROM emails WHERE id = :1", (email_id,))
            email_row = await loop.run_in_executor(None, cursor.fetchone)

            if not email_row:
                return None

            # Convert row to EmailMessage
            email = self._row_to_email(email_row)

            # Get recipients
            email.recipients = await self._get_recipients_with_cursor(cursor, email_id)

            # Get attachments if requested
            if include_attachments:
                email.attachments = await self._get_attachments_with_cursor(cursor, email_id)

            return email

        finally:
            await loop.run_in_executor(None, cursor.close)


# DatabaseConnector interface implementation for Oracle
from evolvishub_outlook_ingestor.connectors.database_connector import (
    DatabaseConnector,
    DatabaseConfig,
)
from typing import Union


class OracleDatabaseConnector(DatabaseConnector):
    """
    Production-ready Oracle database connector for email ingestion.

    This connector provides enterprise-grade Oracle integration with:
    - Connection pooling for high performance
    - Proper schema management
    - Batch processing for efficiency
    - Comprehensive error handling
    - Oracle-specific optimizations and features
    """

    def __init__(self, config: Union[DatabaseConfig, Dict[str, Any]]):
        """
        Initialize Oracle connector.

        Args:
            config: Database configuration (DatabaseConfig or legacy dict format)
        """
        # Handle backward compatibility with old dict-based config
        if isinstance(config, dict):
            db_config = DatabaseConfig(
                database_type="oracle",
                host=config.get('host'),
                port=config.get('port', 1521),
                database=config.get('database'),
                username=config.get('username'),
                password=config.get('password'),
                table_name=config.get('table_name', 'emails'),
                batch_size=config.get('batch_size', 100),
                max_connections=config.get('max_pool_size', 10),
                service_name=config.get('service_name'),
                encoding=config.get('encoding', 'UTF-8'),
                nencoding=config.get('nencoding', 'UTF-8'),
                threaded=config.get('threaded', True),
                events=config.get('events', False)
            )
        else:
            db_config = config

        super().__init__(db_config)
        self.pool = None
        self._validate_oracle_config()

    def _validate_oracle_config(self):
        """Validate Oracle-specific configuration."""
        if not self.config.host:
            raise ValueError("Oracle host is required")
        if not self.config.database and not self.config.service_name:
            raise ValueError("Oracle database or service_name is required")
        if not self.config.username:
            raise ValueError("Oracle username is required")

    async def _connect(self):
        """Establish Oracle connection pool."""
        try:
            if not ORACLE_AVAILABLE:
                raise ImportError("Oracle dependencies not available")

            import cx_Oracle

            # Build DSN
            if self.config.service_name:
                dsn = cx_Oracle.makedsn(
                    self.config.host,
                    self.config.port or 1521,
                    service_name=self.config.service_name
                )
            else:
                dsn = cx_Oracle.makedsn(
                    self.config.host,
                    self.config.port or 1521,
                    sid=self.config.database
                )

            # Create connection pool in thread pool since cx_Oracle is synchronous
            loop = asyncio.get_event_loop()
            self.pool = await loop.run_in_executor(
                None,
                lambda: cx_Oracle.SessionPool(
                    user=self.config.username,
                    password=self.config.password or '',
                    dsn=dsn,
                    min=5,
                    max=self.config.max_connections,
                    increment=1,
                    encoding=self.config.encoding,
                    nencoding=self.config.nencoding,
                    threaded=self.config.threaded,
                    getmode=cx_Oracle.SPOOL_ATTRVAL_WAIT
                )
            )

            self._connection = self.pool
            self.logger.info("Oracle connection pool established")

        except Exception as e:
            self.logger.error(f"Failed to connect to Oracle: {e}")
            raise DatabaseError(f"Failed to connect to Oracle: {e}") from e

    async def _disconnect(self):
        """Close Oracle connection pool."""
        try:
            if self.pool:
                loop = asyncio.get_event_loop()
                await loop.run_in_executor(None, self.pool.close)
                self.pool = None
                self._connection = None
            self.logger.info("Oracle connection pool closed")

        except Exception as e:
            self.logger.error(f"Failed to disconnect from Oracle: {e}")
            raise DatabaseError(f"Failed to disconnect from Oracle: {e}") from e

    async def _create_schema(self):
        """Create Oracle schema/tables if they don't exist."""
        try:
            loop = asyncio.get_event_loop()
            connection = await loop.run_in_executor(None, self.pool.acquire)

            try:
                cursor = await loop.run_in_executor(None, connection.cursor)

                # Create emails table with Oracle optimizations
                create_table_sql = f"""
                    BEGIN
                        EXECUTE IMMEDIATE '
                            CREATE TABLE {self.config.table_name} (
                                id NUMBER GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
                                message_id VARCHAR2(255) UNIQUE NOT NULL,
                                subject CLOB,
                                sender_email VARCHAR2(255),
                                sender_name VARCHAR2(255),
                                received_datetime TIMESTAMP(6),
                                sent_datetime TIMESTAMP(6),
                                body_text CLOB,
                                body_html CLOB,
                                importance VARCHAR2(10) DEFAULT ''normal'',
                                sensitivity VARCHAR2(20) DEFAULT ''normal'',
                                has_attachments NUMBER(1) DEFAULT 0,
                                attachment_count NUMBER DEFAULT 0,
                                folder_path VARCHAR2(500),
                                categories CLOB CHECK (categories IS JSON),
                                headers CLOB CHECK (headers IS JSON),
                                metadata CLOB CHECK (metadata IS JSON),
                                created_at TIMESTAMP(6) DEFAULT CURRENT_TIMESTAMP,
                                updated_at TIMESTAMP(6) DEFAULT CURRENT_TIMESTAMP
                            )';
                    EXCEPTION
                        WHEN OTHERS THEN
                            IF SQLCODE != -955 THEN -- Table already exists
                                RAISE;
                            END IF;
                    END;
                """

                await loop.run_in_executor(None, cursor.execute, create_table_sql)

                # Create indexes
                index_sqls = [
                    f"CREATE INDEX idx_{self.config.table_name}_message_id ON {self.config.table_name} (message_id)",
                    f"CREATE INDEX idx_{self.config.table_name}_received_datetime ON {self.config.table_name} (received_datetime DESC)",
                    f"CREATE INDEX idx_{self.config.table_name}_sender_email ON {self.config.table_name} (sender_email)"
                ]

                for index_sql in index_sqls:
                    try:
                        await loop.run_in_executor(None, cursor.execute, index_sql)
                    except Exception:
                        # Index might already exist, continue
                        pass

                await loop.run_in_executor(None, connection.commit)

            finally:
                await loop.run_in_executor(None, cursor.close)
                await loop.run_in_executor(None, self.pool.release, connection)

            self.logger.info("Oracle schema created successfully")

        except Exception as e:
            self.logger.error(f"Failed to create Oracle schema: {e}")
            raise DatabaseError(f"Failed to create Oracle schema: {e}") from e

    async def _store_email_batch(self, emails: List[EmailMessage]) -> int:
        """Store a batch of emails in Oracle."""
        if not emails:
            return 0

        try:
            loop = asyncio.get_event_loop()
            connection = await loop.run_in_executor(None, self.pool.acquire)

            try:
                cursor = await loop.run_in_executor(None, connection.cursor)
                stored_count = 0

                for email in emails:
                    # Use MERGE statement for Oracle
                    merge_sql = f"""
                        MERGE INTO {self.config.table_name} target
                        USING (SELECT :message_id AS message_id FROM dual) source
                        ON (target.message_id = source.message_id)
                        WHEN MATCHED THEN
                            UPDATE SET
                                subject = :subject,
                                sender_email = :sender_email,
                                sender_name = :sender_name,
                                received_datetime = :received_datetime,
                                sent_datetime = :sent_datetime,
                                body_text = :body_text,
                                body_html = :body_html,
                                importance = :importance,
                                sensitivity = :sensitivity,
                                has_attachments = :has_attachments,
                                attachment_count = :attachment_count,
                                folder_path = :folder_path,
                                categories = :categories,
                                headers = :headers,
                                metadata = :metadata,
                                updated_at = CURRENT_TIMESTAMP
                        WHEN NOT MATCHED THEN
                            INSERT (message_id, subject, sender_email, sender_name,
                                   received_datetime, sent_datetime, body_text, body_html,
                                   importance, sensitivity, has_attachments, attachment_count,
                                   folder_path, categories, headers, metadata)
                            VALUES (:message_id, :subject, :sender_email, :sender_name,
                                   :received_datetime, :sent_datetime, :body_text, :body_html,
                                   :importance, :sensitivity, :has_attachments, :attachment_count,
                                   :folder_path, :categories, :headers, :metadata)
                    """

                    params = {
                        'message_id': email.message_id,
                        'subject': email.subject,
                        'sender_email': email.sender.email if email.sender else None,
                        'sender_name': email.sender.name if email.sender else None,
                        'received_datetime': email.received_datetime,
                        'sent_datetime': email.sent_datetime,
                        'body_text': email.body_text,
                        'body_html': email.body_html,
                        'importance': email.importance,
                        'sensitivity': email.sensitivity,
                        'has_attachments': 1 if email.attachments else 0,
                        'attachment_count': len(email.attachments) if email.attachments else 0,
                        'folder_path': email.folder_path,
                        'categories': json.dumps(email.categories) if email.categories else None,
                        'headers': json.dumps(email.headers) if email.headers else None,
                        'metadata': json.dumps(email.metadata) if email.metadata else None
                    }

                    await loop.run_in_executor(None, cursor.execute, merge_sql, params)
                    if cursor.rowcount > 0:
                        stored_count += 1

                await loop.run_in_executor(None, connection.commit)

            finally:
                await loop.run_in_executor(None, cursor.close)
                await loop.run_in_executor(None, self.pool.release, connection)

            self.logger.info(f"Stored {stored_count} emails in Oracle batch")
            return stored_count

        except Exception as e:
            self.logger.error(f"Failed to store email batch in Oracle: {e}")
            raise DatabaseError(f"Failed to store email batch in Oracle: {e}") from e

    async def _store_single_email(self, email: EmailMessage) -> bool:
        """Store a single email in Oracle."""
        try:
            result = await self._store_email_batch([email])
            return result > 0

        except Exception as e:
            self.logger.error(f"Failed to store single email in Oracle: {e}")
            raise DatabaseError(f"Failed to store single email in Oracle: {e}") from e

    async def _check_email_exists(self, email_id: str) -> bool:
        """Check if email exists in Oracle."""
        try:
            loop = asyncio.get_event_loop()
            connection = await loop.run_in_executor(None, self.pool.acquire)

            try:
                cursor = await loop.run_in_executor(None, connection.cursor)

                await loop.run_in_executor(
                    None,
                    cursor.execute,
                    f"SELECT 1 FROM {self.config.table_name} WHERE message_id = :message_id",
                    {'message_id': email_id}
                )

                result = await loop.run_in_executor(None, cursor.fetchone)
                return result is not None

            finally:
                await loop.run_in_executor(None, cursor.close)
                await loop.run_in_executor(None, self.pool.release, connection)

        except Exception as e:
            self.logger.error(f"Failed to check email existence in Oracle: {e}")
            raise DatabaseError(f"Failed to check email existence in Oracle: {e}") from e

    async def _get_total_email_count(self) -> int:
        """Get total email count from Oracle."""
        try:
            loop = asyncio.get_event_loop()
            connection = await loop.run_in_executor(None, self.pool.acquire)

            try:
                cursor = await loop.run_in_executor(None, connection.cursor)

                await loop.run_in_executor(
                    None,
                    cursor.execute,
                    f"SELECT COUNT(*) FROM {self.config.table_name}"
                )

                result = await loop.run_in_executor(None, cursor.fetchone)
                return result[0] if result else 0

            finally:
                await loop.run_in_executor(None, cursor.close)
                await loop.run_in_executor(None, self.pool.release, connection)

        except Exception as e:
            self.logger.error(f"Failed to get email count from Oracle: {e}")
            raise DatabaseError(f"Failed to get email count from Oracle: {e}") from e
