"""
Microsoft SQL Server database connector for Evolvishub Outlook Ingestor.

This module implements the SQL Server database connector using aioodbc
for Windows-centric environments and enterprise deployments with existing
SQL Server infrastructure.

Features:
- Async database operations with aioodbc
- Connection pooling for high throughput
- Proper database schema with indexes
- Batch insert operations with MERGE statements
- Transaction support with isolation levels
- JSON fields for email metadata and headers (SQL Server 2016+)
- Full-text search capabilities
- Optimized for SQL Server performance
"""

import asyncio
import json
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from uuid import UUID

import aioodbc
from aioodbc import Connection, Pool

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


class MSSQLConnector(BaseConnector):
    """Microsoft SQL Server database connector using aioodbc."""
    
    def __init__(self, name: str, config: Dict[str, Any], **kwargs):
        """
        Initialize SQL Server connector.
        
        Args:
            name: Connector name
            config: Configuration dictionary containing:
                - server: SQL Server instance (e.g., 'localhost' or 'server\\instance')
                - port: SQL Server port (default: 1433)
                - database: Database name
                - username: Database username
                - password: Database password
                - driver: ODBC driver (default: 'ODBC Driver 17 for SQL Server')
                - trusted_connection: Use Windows authentication (default: False)
                - encrypt: Encrypt connection (default: True)
                - trust_server_certificate: Trust server certificate (default: False)
                - connection_timeout: Connection timeout in seconds
                - command_timeout: Command timeout in seconds
                - pool_size: Connection pool size
                - max_overflow: Maximum pool overflow
        """
        super().__init__(name, config, **kwargs)

        # Get credential manager (lazy loading)
        get_credential_manager, create_secure_dsn, _, _ = _get_security_utils()
        self._credential_manager = get_credential_manager()
        self._create_secure_dsn = create_secure_dsn

        # SQL Server configuration
        self.server = config.get("server", "localhost")
        self.port = config.get("port", 1433)
        self.database = config.get("database", "outlook_data")
        self.username = config.get("username", "")
        self.driver = config.get("driver", "ODBC Driver 17 for SQL Server")
        self.trusted_connection = config.get("trusted_connection", False)
        self.encrypt = config.get("encrypt", True)
        self.trust_server_certificate = config.get("trust_server_certificate", False)
        self.connection_timeout = config.get("connection_timeout", 30)
        self.command_timeout = config.get("command_timeout", 30)

        # Secure password handling
        password_raw = config.get("password", "")
        password_env = config.get("password_env", "MSSQL_PASSWORD")

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
        self.pool: Optional[Pool] = None
        
        # Schema definitions
        self.schema_sql = self._get_schema_sql()
    
    async def _initialize_connection(self) -> None:
        """Initialize single SQL Server connection (not used with pooling)."""
        try:
            dsn = self._build_connection_string()
            
            self.logger.info(
                "Connecting to SQL Server",
                server=self.server,
                database=self.database,
                connector=self.name
            )
            
            self._connection = await aioodbc.connect(dsn=dsn)
            
            self.logger.info(
                "SQL Server connection established",
                server=self.server,
                database=self.database,
                connector=self.name
            )
            
        except Exception as e:
            raise ConnectionError(
                f"Failed to connect to SQL Server: {e}",
                database_type="mssql",
                cause=e
            )
    
    async def _initialize_pool(self) -> None:
        """Initialize SQL Server connection pool."""
        try:
            dsn = self._build_connection_string()
            
            self.logger.info(
                "Creating SQL Server connection pool",
                server=self.server,
                database=self.database,
                pool_size=self._pool_config.max_size,
                connector=self.name
            )
            
            self.pool = await aioodbc.create_pool(
                dsn=dsn,
                minsize=self._pool_config.min_size,
                maxsize=self._pool_config.max_size,
                timeout=self.connection_timeout
            )
            
            self.logger.info(
                "SQL Server connection pool created",
                server=self.server,
                database=self.database,
                connector=self.name
            )
            
        except Exception as e:
            raise ConnectionError(
                f"Failed to create SQL Server connection pool: {e}",
                database_type="mssql",
                cause=e
            )
    
    async def _cleanup_connection(self) -> None:
        """Cleanup SQL Server connection."""
        if self._connection:
            try:
                await self._connection.close()
                self.logger.info("SQL Server connection closed", connector=self.name)
            except Exception as e:
                self.logger.warning(
                    "Error closing SQL Server connection",
                    connector=self.name,
                    error=str(e)
                )
            finally:
                self._connection = None
    
    async def _cleanup_pool(self) -> None:
        """Cleanup SQL Server connection pool."""
        if self.pool:
            try:
                self.pool.close()
                await self.pool.wait_closed()
                self.logger.info("SQL Server connection pool closed", connector=self.name)
            except Exception as e:
                self.logger.warning(
                    "Error closing SQL Server connection pool",
                    connector=self.name,
                    error=str(e)
                )
            finally:
                self.pool = None
    
    async def _test_connection(self) -> None:
        """Test SQL Server connection."""
        try:
            if self.enable_connection_pooling:
                async with self.pool.acquire() as conn:
                    async with conn.cursor() as cursor:
                        await cursor.execute("SELECT 1")
                        result = await cursor.fetchone()
                        if result[0] != 1:
                            raise ConnectionError("SQL Server connection test failed")
            else:
                async with self._connection.cursor() as cursor:
                    await cursor.execute("SELECT 1")
                    result = await cursor.fetchone()
                    if result[0] != 1:
                        raise ConnectionError("SQL Server connection test failed")
                        
            self.logger.debug("SQL Server connection test passed", connector=self.name)
            
        except Exception as e:
            raise ConnectionError(f"SQL Server connection test failed: {e}")
    
    async def _initialize_schema(self) -> None:
        """Initialize SQL Server database schema."""
        try:
            self.logger.info("Initializing SQL Server schema", connector=self.name)
            
            if self.enable_connection_pooling:
                async with self.pool.acquire() as conn:
                    await self._execute_schema_statements(conn)
            else:
                await self._execute_schema_statements(self._connection)
            
            self.logger.info("SQL Server schema initialized", connector=self.name)
            
        except Exception as e:
            raise DatabaseError(
                f"Failed to initialize SQL Server schema: {e}",
                database_type="mssql",
                operation="initialize_schema",
                cause=e
            )
    
    async def _execute_schema_statements(self, connection: Connection) -> None:
        """Execute schema creation statements."""
        async with connection.cursor() as cursor:
            for statement in self.schema_sql:
                try:
                    await cursor.execute(statement)
                    await connection.commit()
                except Exception as e:
                    self.logger.warning(
                        "Schema statement failed (may already exist)",
                        statement=statement[:100] + "..." if len(statement) > 100 else statement,
                        error=str(e),
                        connector=self.name
                    )
    
    def _build_connection_string(self) -> str:
        """Build SQL Server connection string."""
        try:
            # Decrypt password for connection
            password = ""
            if self._encrypted_password:
                password = self._credential_manager.decrypt_credential(self._encrypted_password)
            
            # Build connection string components
            dsn_parts = [
                f"DRIVER={{{self.driver}}}",
                f"SERVER={self.server},{self.port}",
                f"DATABASE={self.database}",
                f"Encrypt={'yes' if self.encrypt else 'no'}",
                f"TrustServerCertificate={'yes' if self.trust_server_certificate else 'no'}",
                f"Connection Timeout={self.connection_timeout}",
                f"Command Timeout={self.command_timeout}"
            ]
            
            # Authentication
            if self.trusted_connection:
                dsn_parts.append("Trusted_Connection=yes")
            else:
                if self.username:
                    dsn_parts.append(f"UID={self.username}")
                if password:
                    dsn_parts.append(f"PWD={password}")
            
            dsn = ";".join(dsn_parts)
            
            # Use secure DSN creation if available
            return self._create_secure_dsn(dsn, mask_password=True)
            
        except Exception as e:
            raise ConnectionError(f"Failed to build SQL Server connection string: {e}")
    
    def _get_schema_sql(self) -> List[str]:
        """Get SQL Server schema SQL statements."""
        return [
            # Emails table
            """
            IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='emails' AND xtype='U')
            CREATE TABLE emails (
                id NVARCHAR(255) PRIMARY KEY,
                message_id NVARCHAR(255) UNIQUE,
                subject NVARCHAR(MAX),
                body NVARCHAR(MAX),
                body_preview NVARCHAR(MAX),
                sender_email NVARCHAR(255),
                sender_name NVARCHAR(255),
                received_date DATETIME2,
                sent_date DATETIME2,
                importance NVARCHAR(50),
                is_read BIT DEFAULT 0,
                has_attachments BIT DEFAULT 0,
                folder_id NVARCHAR(255),
                folder_name NVARCHAR(255),
                categories NVARCHAR(MAX),  -- JSON
                headers NVARCHAR(MAX),     -- JSON
                metadata NVARCHAR(MAX),    -- JSON
                created_at DATETIME2 DEFAULT GETUTCDATE(),
                updated_at DATETIME2 DEFAULT GETUTCDATE()
            )
            """,
            
            # Recipients table
            """
            IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='email_recipients' AND xtype='U')
            CREATE TABLE email_recipients (
                id INT IDENTITY(1,1) PRIMARY KEY,
                email_id NVARCHAR(255) NOT NULL,
                recipient_type NVARCHAR(10) NOT NULL,  -- to, cc, bcc
                email_address NVARCHAR(255) NOT NULL,
                display_name NVARCHAR(255),
                FOREIGN KEY (email_id) REFERENCES emails (id) ON DELETE CASCADE
            )
            """,
            
            # Attachments table
            """
            IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='email_attachments' AND xtype='U')
            CREATE TABLE email_attachments (
                id NVARCHAR(255) PRIMARY KEY,
                email_id NVARCHAR(255) NOT NULL,
                name NVARCHAR(255) NOT NULL,
                content_type NVARCHAR(255),
                size BIGINT,
                content VARBINARY(MAX),  -- For small attachments stored in database
                content_hash NVARCHAR(255),
                is_inline BIT DEFAULT 0,
                attachment_type NVARCHAR(50),
                extended_properties NVARCHAR(MAX),  -- JSON for storage info
                created_at DATETIME2 DEFAULT GETUTCDATE(),
                FOREIGN KEY (email_id) REFERENCES emails (id) ON DELETE CASCADE
            )
            """,

            # Folders table
            """
            IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='outlook_folders' AND xtype='U')
            CREATE TABLE outlook_folders (
                id NVARCHAR(255) PRIMARY KEY,
                name NVARCHAR(255) NOT NULL,
                parent_folder_id NVARCHAR(255),
                folder_type NVARCHAR(50),
                total_item_count INT DEFAULT 0,
                unread_item_count INT DEFAULT 0,
                created_at DATETIME2 DEFAULT GETUTCDATE(),
                updated_at DATETIME2 DEFAULT GETUTCDATE()
            )
            """,

            # Indexes for performance
            "CREATE NONCLUSTERED INDEX IX_emails_message_id ON emails (message_id)",
            "CREATE NONCLUSTERED INDEX IX_emails_sender ON emails (sender_email)",
            "CREATE NONCLUSTERED INDEX IX_emails_received_date ON emails (received_date)",
            "CREATE NONCLUSTERED INDEX IX_emails_folder ON emails (folder_id)",
            "CREATE NONCLUSTERED INDEX IX_emails_has_attachments ON emails (has_attachments)",
            "CREATE NONCLUSTERED INDEX IX_recipients_email_id ON email_recipients (email_id)",
            "CREATE NONCLUSTERED INDEX IX_recipients_type ON email_recipients (recipient_type)",
            "CREATE NONCLUSTERED INDEX IX_attachments_email_id ON email_attachments (email_id)",
            "CREATE NONCLUSTERED INDEX IX_attachments_hash ON email_attachments (content_hash)",
            "CREATE NONCLUSTERED INDEX IX_folders_parent ON outlook_folders (parent_folder_id)"
        ]

    async def _store_email_impl(
        self,
        email: EmailMessage,
        transaction: Optional[Any] = None,
        **kwargs
    ) -> str:
        """Store email in SQL Server database."""
        try:
            connection = transaction if transaction else (
                self.pool.acquire() if self.enable_connection_pooling else self._connection
            )

            if self.enable_connection_pooling and not transaction:
                async with connection as conn:
                    return await self._store_email_with_connection(email, conn)
            else:
                return await self._store_email_with_connection(email, connection)

        except Exception as e:
            raise DatabaseError(
                f"Failed to store email in SQL Server: {e}",
                database_type="mssql",
                operation="store_email",
                cause=e
            )

    async def _store_email_with_connection(self, email: EmailMessage, connection: Connection) -> str:
        """Store email with specific connection."""
        async with connection.cursor() as cursor:
            # Prepare email data
            email_data = self._prepare_email_data(email)

            # Use MERGE statement for upsert
            merge_sql = """
            MERGE emails AS target
            USING (VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)) AS source (
                id, message_id, subject, body, body_preview,
                sender_email, sender_name, received_date, sent_date,
                importance, is_read, has_attachments, folder_id, folder_name,
                categories, headers, metadata, updated_at
            )
            ON target.id = source.id
            WHEN MATCHED THEN
                UPDATE SET
                    message_id = source.message_id,
                    subject = source.subject,
                    body = source.body,
                    body_preview = source.body_preview,
                    sender_email = source.sender_email,
                    sender_name = source.sender_name,
                    received_date = source.received_date,
                    sent_date = source.sent_date,
                    importance = source.importance,
                    is_read = source.is_read,
                    has_attachments = source.has_attachments,
                    folder_id = source.folder_id,
                    folder_name = source.folder_name,
                    categories = source.categories,
                    headers = source.headers,
                    metadata = source.metadata,
                    updated_at = source.updated_at
            WHEN NOT MATCHED THEN
                INSERT (id, message_id, subject, body, body_preview,
                       sender_email, sender_name, received_date, sent_date,
                       importance, is_read, has_attachments, folder_id, folder_name,
                       categories, headers, metadata, updated_at)
                VALUES (source.id, source.message_id, source.subject, source.body, source.body_preview,
                       source.sender_email, source.sender_name, source.received_date, source.sent_date,
                       source.importance, source.is_read, source.has_attachments, source.folder_id, source.folder_name,
                       source.categories, source.headers, source.metadata, source.updated_at);
            """

            await cursor.execute(merge_sql, email_data)

            # Store recipients
            if email.recipients:
                await self._store_recipients_with_cursor(cursor, email.id, email.recipients)

            # Store attachments
            if email.attachments:
                await self._store_attachments_with_cursor(cursor, email.id, email.attachments)

            if not transaction:
                await connection.commit()

            return email.id

    async def _store_emails_batch_impl(
        self,
        emails: List[EmailMessage],
        transaction: Optional[Any] = None,
        **kwargs
    ) -> List[str]:
        """Store multiple emails in SQL Server database."""
        try:
            connection = transaction if transaction else (
                self.pool.acquire() if self.enable_connection_pooling else self._connection
            )

            if self.enable_connection_pooling and not transaction:
                async with connection as conn:
                    return await self._store_emails_batch_with_connection(emails, conn)
            else:
                return await self._store_emails_batch_with_connection(emails, connection)

        except Exception as e:
            raise DatabaseError(
                f"Failed to store emails batch in SQL Server: {e}",
                database_type="mssql",
                operation="store_emails_batch",
                cause=e
            )

    async def _store_emails_batch_with_connection(self, emails: List[EmailMessage], connection: Connection) -> List[str]:
        """Store emails batch with specific connection."""
        stored_ids = []

        async with connection.cursor() as cursor:
            # Prepare batch data
            email_data_batch = []
            recipients_batch = []
            attachments_batch = []

            for email in emails:
                email_data = self._prepare_email_data(email)
                email_data_batch.append(email_data)
                stored_ids.append(email.id)

                # Collect recipients
                if email.recipients:
                    for recipient_type, recipients in email.recipients.items():
                        for recipient in recipients:
                            recipients_batch.append((
                                email.id,
                                recipient_type,
                                recipient.email,
                                recipient.name
                            ))

                # Collect attachments
                if email.attachments:
                    for attachment in email.attachments:
                        attachment_data = self._prepare_attachment_data(email.id, attachment)
                        attachments_batch.append(attachment_data)

            # Batch insert emails using table-valued parameters (more efficient for SQL Server)
            if email_data_batch:
                # For simplicity, use individual MERGE statements in a loop
                # In production, consider using table-valued parameters for better performance
                for email_data in email_data_batch:
                    merge_sql = """
                    MERGE emails AS target
                    USING (VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)) AS source (
                        id, message_id, subject, body, body_preview,
                        sender_email, sender_name, received_date, sent_date,
                        importance, is_read, has_attachments, folder_id, folder_name,
                        categories, headers, metadata, updated_at
                    )
                    ON target.id = source.id
                    WHEN NOT MATCHED THEN
                        INSERT (id, message_id, subject, body, body_preview,
                               sender_email, sender_name, received_date, sent_date,
                               importance, is_read, has_attachments, folder_id, folder_name,
                               categories, headers, metadata, updated_at)
                        VALUES (source.id, source.message_id, source.subject, source.body, source.body_preview,
                               source.sender_email, source.sender_name, source.received_date, source.sent_date,
                               source.importance, source.is_read, source.has_attachments, source.folder_id, source.folder_name,
                               source.categories, source.headers, source.metadata, source.updated_at);
                    """
                    await cursor.execute(merge_sql, email_data)

            # Batch insert recipients
            if recipients_batch:
                await cursor.executemany(
                    """
                    INSERT INTO email_recipients (email_id, recipient_type, email_address, display_name)
                    VALUES (?, ?, ?, ?)
                    """,
                    recipients_batch
                )

            # Batch insert attachments
            if attachments_batch:
                await cursor.executemany(
                    """
                    MERGE email_attachments AS target
                    USING (VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)) AS source (
                        id, email_id, name, content_type, size, content,
                        content_hash, is_inline, attachment_type, extended_properties
                    )
                    ON target.id = source.id
                    WHEN NOT MATCHED THEN
                        INSERT (id, email_id, name, content_type, size, content,
                               content_hash, is_inline, attachment_type, extended_properties)
                        VALUES (source.id, source.email_id, source.name, source.content_type, source.size, source.content,
                               source.content_hash, source.is_inline, source.attachment_type, source.extended_properties);
                    """,
                    attachments_batch
                )

            if not transaction:
                await connection.commit()

            return stored_ids

    async def _get_email_impl(
        self,
        email_id: str,
        include_attachments: bool = True,
        **kwargs
    ) -> Optional[EmailMessage]:
        """Retrieve email from SQL Server database."""
        try:
            if self.enable_connection_pooling:
                async with self.pool.acquire() as connection:
                    return await self._get_email_with_connection(email_id, include_attachments, connection)
            else:
                return await self._get_email_with_connection(email_id, include_attachments, self._connection)

        except Exception as e:
            raise DatabaseError(
                f"Failed to retrieve email from SQL Server: {e}",
                database_type="mssql",
                operation="get_email",
                cause=e
            )

    async def _get_email_with_connection(
        self,
        email_id: str,
        include_attachments: bool,
        connection: Connection
    ) -> Optional[EmailMessage]:
        """Retrieve email with specific connection."""
        async with connection.cursor() as cursor:
            # Get email data
            await cursor.execute("SELECT * FROM emails WHERE id = ?", (email_id,))
            email_row = await cursor.fetchone()

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

    async def _search_emails_impl(
        self,
        filters: Dict[str, Any],
        limit: Optional[int] = None,
        offset: int = 0,
        sort_by: Optional[str] = None,
        sort_order: str = "desc",
        **kwargs
    ) -> List[EmailMessage]:
        """Search emails in SQL Server database."""
        try:
            if self.enable_connection_pooling:
                async with self.pool.acquire() as connection:
                    return await self._search_emails_with_connection(
                        filters, limit, offset, sort_by, sort_order, connection
                    )
            else:
                return await self._search_emails_with_connection(
                    filters, limit, offset, sort_by, sort_order, self._connection
                )

        except Exception as e:
            raise DatabaseError(
                f"Failed to search emails in SQL Server: {e}",
                database_type="mssql",
                operation="search_emails",
                cause=e
            )

    async def _search_emails_with_connection(
        self,
        filters: Dict[str, Any],
        limit: Optional[int],
        offset: int,
        sort_by: Optional[str],
        sort_order: str,
        connection: Connection
    ) -> List[EmailMessage]:
        """Search emails with specific connection."""
        async with connection.cursor() as cursor:
            # Build query
            query_parts = ["SELECT * FROM emails WHERE 1=1"]
            params = []

            # Add filters
            if "sender_email" in filters:
                query_parts.append("AND sender_email = ?")
                params.append(filters["sender_email"])

            if "subject_contains" in filters:
                query_parts.append("AND subject LIKE ?")
                params.append(f"%{filters['subject_contains']}%")

            if "date_from" in filters:
                query_parts.append("AND received_date >= ?")
                params.append(filters["date_from"])

            if "date_to" in filters:
                query_parts.append("AND received_date <= ?")
                params.append(filters["date_to"])

            if "folder_id" in filters:
                query_parts.append("AND folder_id = ?")
                params.append(filters["folder_id"])

            if "has_attachments" in filters:
                query_parts.append("AND has_attachments = ?")
                params.append(filters["has_attachments"])

            # Full-text search (if available)
            if "search_text" in filters:
                query_parts.append("AND (CONTAINS(subject, ?) OR CONTAINS(body, ?))")
                search_term = filters["search_text"]
                params.extend([search_term, search_term])

            # Add sorting
            if sort_by:
                query_parts.append(f"ORDER BY {sort_by} {sort_order.upper()}")
            else:
                query_parts.append("ORDER BY received_date DESC")

            # Add pagination
            if limit:
                query_parts.append(f"OFFSET {offset} ROWS FETCH NEXT {limit} ROWS ONLY")

            query = " ".join(query_parts)

            # Execute query
            await cursor.execute(query, params)
            rows = await cursor.fetchall()

            emails = []
            for row in rows:
                email = self._row_to_email(row)
                # Get recipients and attachments for each email
                email.recipients = await self._get_recipients_with_cursor(cursor, email.id)
                email.attachments = await self._get_attachments_with_cursor(cursor, email.id)
                emails.append(email)

            return emails

    async def _begin_transaction(self, isolation_level: Optional[str] = None) -> Any:
        """Begin SQL Server transaction."""
        try:
            if self.enable_connection_pooling:
                connection = await self.pool.acquire()
            else:
                connection = self._connection

            if isolation_level:
                await connection.execute(f"SET TRANSACTION ISOLATION LEVEL {isolation_level}")

            await connection.execute("BEGIN TRANSACTION")
            return connection
        except Exception as e:
            raise TransactionError(f"Failed to begin SQL Server transaction: {e}")

    async def _commit_transaction(self, transaction: Any) -> None:
        """Commit SQL Server transaction."""
        try:
            await transaction.commit()
            if self.enable_connection_pooling:
                self.pool.release(transaction)
        except Exception as e:
            raise TransactionError(f"Failed to commit SQL Server transaction: {e}")

    async def _rollback_transaction(self, transaction: Any) -> None:
        """Rollback SQL Server transaction."""
        try:
            await transaction.rollback()
            if self.enable_connection_pooling:
                self.pool.release(transaction)
        except Exception as e:
            raise TransactionError(f"Failed to rollback SQL Server transaction: {e}")

    def _prepare_email_data(self, email: EmailMessage) -> tuple:
        """Prepare email data for SQL Server insertion."""
        return (
            email.id,
            email.message_id,
            email.subject,
            email.body,
            email.body_preview,
            email.sender.email if email.sender else None,
            email.sender.name if email.sender else None,
            email.received_date,
            email.sent_date,
            email.importance,
            email.is_read,
            bool(email.attachments),
            email.folder.id if email.folder else None,
            email.folder.name if email.folder else None,
            json.dumps(email.categories) if email.categories else None,
            json.dumps(email.headers) if email.headers else None,
            json.dumps(email.metadata) if email.metadata else None,
            datetime.now(timezone.utc)
        )

    def _prepare_attachment_data(self, email_id: str, attachment: EmailAttachment) -> tuple:
        """Prepare attachment data for SQL Server insertion."""
        return (
            attachment.id,
            email_id,
            attachment.name,
            attachment.content_type,
            attachment.size,
            attachment.content,
            attachment.content_hash,
            attachment.is_inline,
            attachment.attachment_type,
            json.dumps(attachment.extended_properties) if attachment.extended_properties else None
        )

    def _row_to_email(self, row) -> EmailMessage:
        """Convert SQL Server row to EmailMessage."""
        from evolvishub_outlook_ingestor.core.data_models import EmailAddress, OutlookFolder

        # Create sender
        sender = None
        if row[5]:  # sender_email
            sender = EmailAddress(email=row[5], name=row[6])

        # Create folder
        folder = None
        if row[12]:  # folder_id
            folder = OutlookFolder(id=row[12], name=row[13])

        # Parse JSON fields
        categories = json.loads(row[14]) if row[14] else []
        headers = json.loads(row[15]) if row[15] else {}
        metadata = json.loads(row[16]) if row[16] else {}

        return EmailMessage(
            id=row[0],
            message_id=row[1],
            subject=row[2],
            body=row[3],
            body_preview=row[4],
            sender=sender,
            received_date=row[7],
            sent_date=row[8],
            importance=row[9],
            is_read=row[10],
            folder=folder,
            categories=categories,
            headers=headers,
            metadata=metadata
        )

    async def _store_recipients_with_cursor(self, cursor, email_id: str, recipients: Dict[str, List]) -> None:
        """Store email recipients with cursor."""
        recipient_data = []
        for recipient_type, recipient_list in recipients.items():
            for recipient in recipient_list:
                recipient_data.append((
                    email_id,
                    recipient_type,
                    recipient.email,
                    recipient.name
                ))

        if recipient_data:
            await cursor.executemany(
                """
                INSERT INTO email_recipients (email_id, recipient_type, email_address, display_name)
                VALUES (?, ?, ?, ?)
                """,
                recipient_data
            )

    async def _store_attachments_with_cursor(self, cursor, email_id: str, attachments: List[EmailAttachment]) -> None:
        """Store email attachments with cursor."""
        attachment_data = []
        for attachment in attachments:
            attachment_data.append(self._prepare_attachment_data(email_id, attachment))

        if attachment_data:
            await cursor.executemany(
                """
                MERGE email_attachments AS target
                USING (VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)) AS source (
                    id, email_id, name, content_type, size, content,
                    content_hash, is_inline, attachment_type, extended_properties
                )
                ON target.id = source.id
                WHEN NOT MATCHED THEN
                    INSERT (id, email_id, name, content_type, size, content,
                           content_hash, is_inline, attachment_type, extended_properties)
                    VALUES (source.id, source.email_id, source.name, source.content_type, source.size, source.content,
                           source.content_hash, source.is_inline, source.attachment_type, source.extended_properties);
                """,
                attachment_data
            )

    async def _get_recipients_with_cursor(self, cursor, email_id: str) -> Dict[str, List]:
        """Get email recipients with cursor."""
        from evolvishub_outlook_ingestor.core.data_models import EmailAddress

        recipients = {"to": [], "cc": [], "bcc": []}

        await cursor.execute(
            "SELECT recipient_type, email_address, display_name FROM email_recipients WHERE email_id = ?",
            (email_id,)
        )
        rows = await cursor.fetchall()

        for row in rows:
            recipient_type, email_address, display_name = row
            recipient = EmailAddress(email=email_address, name=display_name)
            if recipient_type in recipients:
                recipients[recipient_type].append(recipient)

        return recipients

    async def _get_attachments_with_cursor(self, cursor, email_id: str) -> List[EmailAttachment]:
        """Get email attachments with cursor."""
        attachments = []

        await cursor.execute(
            "SELECT * FROM email_attachments WHERE email_id = ?",
            (email_id,)
        )
        rows = await cursor.fetchall()

        for row in rows:
            extended_properties = json.loads(row[9]) if row[9] else {}

            attachment = EmailAttachment(
                id=row[0],
                name=row[2],
                content_type=row[3],
                size=row[4],
                content=row[5],
                content_hash=row[6],
                is_inline=row[7],
                attachment_type=row[8],
                extended_properties=extended_properties
            )
            attachments.append(attachment)

        return attachments


# DatabaseConnector interface implementation for MS SQL Server
from evolvishub_outlook_ingestor.connectors.database_connector import (
    DatabaseConnector,
    DatabaseConfig,
)
from typing import Union


class MSSQLDatabaseConnector(DatabaseConnector):
    """
    Production-ready MS SQL Server database connector for email ingestion.

    This connector provides enterprise-grade SQL Server integration with:
    - Connection pooling for high performance
    - Proper schema management
    - Batch processing for efficiency
    - Comprehensive error handling
    - Transaction support with SQL Server optimizations
    """

    def __init__(self, config: Union[DatabaseConfig, Dict[str, Any]]):
        """
        Initialize MS SQL Server connector.

        Args:
            config: Database configuration (DatabaseConfig or legacy dict format)
        """
        # Handle backward compatibility with old dict-based config
        if isinstance(config, dict):
            db_config = DatabaseConfig(
                database_type="mssql",
                host=config.get('host'),
                port=config.get('port', 1433),
                database=config.get('database'),
                username=config.get('username'),
                password=config.get('password'),
                table_name=config.get('table_name', 'emails'),
                batch_size=config.get('batch_size', 100),
                max_connections=config.get('max_pool_size', 10),
                driver=config.get('driver', 'ODBC Driver 17 for SQL Server'),
                trusted_connection=config.get('trusted_connection', False),
                encrypt=config.get('encrypt', True),
                trust_server_certificate=config.get('trust_server_certificate', False)
            )
        else:
            db_config = config

        super().__init__(db_config)
        self._pool = None
        self._validate_mssql_config()

    def _validate_mssql_config(self):
        """Validate MS SQL Server-specific configuration."""
        if not self.config.host:
            raise ValueError("MS SQL Server host is required")
        if not self.config.database:
            raise ValueError("MS SQL Server database name is required")
        if not self.config.username and not self.config.trusted_connection:
            raise ValueError("MS SQL Server username is required when not using trusted connection")

    async def _connect(self):
        """Establish MS SQL Server connection pool."""
        try:
            import aioodbc

            # Build connection string
            if self.config.connection_string:
                dsn = self.config.connection_string
            else:
                dsn = (
                    f"DRIVER={{{self.config.driver}}};"
                    f"SERVER={self.config.host},{self.config.port or 1433};"
                    f"DATABASE={self.config.database};"
                )

                if self.config.trusted_connection:
                    dsn += "Trusted_Connection=yes;"
                else:
                    dsn += f"UID={self.config.username};PWD={self.config.password or ''};"

                if self.config.encrypt:
                    dsn += "Encrypt=yes;"
                if self.config.trust_server_certificate:
                    dsn += "TrustServerCertificate=yes;"

            # Create connection pool
            self._pool = await aioodbc.create_pool(
                dsn=dsn,
                minsize=5,
                maxsize=self.config.max_connections,
                echo=False
            )

            self._connection = self._pool
            self.logger.info("MS SQL Server connection pool established")

        except Exception as e:
            self.logger.error(f"Failed to connect to MS SQL Server: {e}")
            raise DatabaseError(f"Failed to connect to MS SQL Server: {e}") from e

    async def _disconnect(self):
        """Close MS SQL Server connection pool."""
        try:
            if self._pool:
                self._pool.close()
                await self._pool.wait_closed()
                self._pool = None
                self._connection = None
            self.logger.info("MS SQL Server connection pool closed")

        except Exception as e:
            self.logger.error(f"Failed to disconnect from MS SQL Server: {e}")
            raise DatabaseError(f"Failed to disconnect from MS SQL Server: {e}") from e

    async def _create_schema(self):
        """Create MS SQL Server schema/tables if they don't exist."""
        try:
            async with self._pool.acquire() as connection:
                async with connection.cursor() as cursor:
                    # Create emails table with SQL Server optimizations
                    await cursor.execute(f"""
                        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='{self.config.table_name}' AND xtype='U')
                        CREATE TABLE {self.config.table_name} (
                            id BIGINT IDENTITY(1,1) PRIMARY KEY,
                            message_id NVARCHAR(255) UNIQUE NOT NULL,
                            subject NVARCHAR(MAX),
                            sender_email NVARCHAR(255),
                            sender_name NVARCHAR(255),
                            received_datetime DATETIME2(6),
                            sent_datetime DATETIME2(6),
                            body_text NVARCHAR(MAX),
                            body_html NVARCHAR(MAX),
                            importance NVARCHAR(10) DEFAULT 'normal',
                            sensitivity NVARCHAR(20) DEFAULT 'normal',
                            has_attachments BIT DEFAULT 0,
                            attachment_count INT DEFAULT 0,
                            folder_path NVARCHAR(500),
                            categories NVARCHAR(MAX),
                            headers NVARCHAR(MAX),
                            metadata NVARCHAR(MAX),
                            created_at DATETIME2(6) DEFAULT GETUTCDATE(),
                            updated_at DATETIME2(6) DEFAULT GETUTCDATE()
                        )
                    """)

                    # Create indexes
                    await cursor.execute(f"""
                        IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name='IX_{self.config.table_name}_message_id')
                        CREATE NONCLUSTERED INDEX IX_{self.config.table_name}_message_id
                        ON {self.config.table_name} (message_id)
                    """)

                    await cursor.execute(f"""
                        IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name='IX_{self.config.table_name}_received_datetime')
                        CREATE NONCLUSTERED INDEX IX_{self.config.table_name}_received_datetime
                        ON {self.config.table_name} (received_datetime DESC)
                    """)

                    await cursor.execute(f"""
                        IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name='IX_{self.config.table_name}_sender_email')
                        CREATE NONCLUSTERED INDEX IX_{self.config.table_name}_sender_email
                        ON {self.config.table_name} (sender_email)
                    """)

                    await connection.commit()

            self.logger.info("MS SQL Server schema created successfully")

        except Exception as e:
            self.logger.error(f"Failed to create MS SQL Server schema: {e}")
            raise DatabaseError(f"Failed to create MS SQL Server schema: {e}") from e

    async def _store_email_batch(self, emails: List[EmailMessage]) -> int:
        """Store a batch of emails in MS SQL Server."""
        if not emails:
            return 0

        try:
            async with self._pool.acquire() as connection:
                async with connection.cursor() as cursor:
                    stored_count = 0

                    for email in emails:
                        # Use MERGE statement for SQL Server
                        sql = f"""
                            MERGE {self.config.table_name} AS target
                            USING (SELECT ? AS message_id) AS source
                            ON target.message_id = source.message_id
                            WHEN MATCHED THEN
                                UPDATE SET
                                    subject = ?,
                                    sender_email = ?,
                                    sender_name = ?,
                                    received_datetime = ?,
                                    sent_datetime = ?,
                                    body_text = ?,
                                    body_html = ?,
                                    importance = ?,
                                    sensitivity = ?,
                                    has_attachments = ?,
                                    attachment_count = ?,
                                    folder_path = ?,
                                    categories = ?,
                                    headers = ?,
                                    metadata = ?,
                                    updated_at = GETUTCDATE()
                            WHEN NOT MATCHED THEN
                                INSERT (message_id, subject, sender_email, sender_name,
                                       received_datetime, sent_datetime, body_text, body_html,
                                       importance, sensitivity, has_attachments, attachment_count,
                                       folder_path, categories, headers, metadata)
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
                        """

                        values = (
                            email.message_id,  # For USING clause
                            email.subject,
                            email.sender.email if email.sender else None,
                            email.sender.name if email.sender else None,
                            email.received_datetime,
                            email.sent_datetime,
                            email.body_text,
                            email.body_html,
                            email.importance,
                            email.sensitivity,
                            bool(email.attachments),
                            len(email.attachments) if email.attachments else 0,
                            email.folder_path,
                            json.dumps(email.categories) if email.categories else None,
                            json.dumps(email.headers) if email.headers else None,
                            json.dumps(email.metadata) if email.metadata else None,
                            # For INSERT clause
                            email.message_id,
                            email.subject,
                            email.sender.email if email.sender else None,
                            email.sender.name if email.sender else None,
                            email.received_datetime,
                            email.sent_datetime,
                            email.body_text,
                            email.body_html,
                            email.importance,
                            email.sensitivity,
                            bool(email.attachments),
                            len(email.attachments) if email.attachments else 0,
                            email.folder_path,
                            json.dumps(email.categories) if email.categories else None,
                            json.dumps(email.headers) if email.headers else None,
                            json.dumps(email.metadata) if email.metadata else None
                        )

                        await cursor.execute(sql, values)
                        if cursor.rowcount > 0:
                            stored_count += 1

                    await connection.commit()
                    self.logger.info(f"Stored {stored_count} emails in MS SQL Server batch")
                    return stored_count

        except Exception as e:
            self.logger.error(f"Failed to store email batch in MS SQL Server: {e}")
            raise DatabaseError(f"Failed to store email batch in MS SQL Server: {e}") from e

    async def _store_single_email(self, email: EmailMessage) -> bool:
        """Store a single email in MS SQL Server."""
        try:
            result = await self._store_email_batch([email])
            return result > 0

        except Exception as e:
            self.logger.error(f"Failed to store single email in MS SQL Server: {e}")
            raise DatabaseError(f"Failed to store single email in MS SQL Server: {e}") from e

    async def _check_email_exists(self, email_id: str) -> bool:
        """Check if email exists in MS SQL Server."""
        try:
            async with self._pool.acquire() as connection:
                async with connection.cursor() as cursor:
                    await cursor.execute(
                        f"SELECT 1 FROM {self.config.table_name} WHERE message_id = ?",
                        (email_id,)
                    )
                    result = await cursor.fetchone()
                    return result is not None

        except Exception as e:
            self.logger.error(f"Failed to check email existence in MS SQL Server: {e}")
            raise DatabaseError(f"Failed to check email existence in MS SQL Server: {e}") from e

    async def _get_total_email_count(self) -> int:
        """Get total email count from MS SQL Server."""
        try:
            async with self._pool.acquire() as connection:
                async with connection.cursor() as cursor:
                    await cursor.execute(f"SELECT COUNT(*) FROM {self.config.table_name}")
                    result = await cursor.fetchone()
                    return result[0] if result else 0

        except Exception as e:
            self.logger.error(f"Failed to get email count from MS SQL Server: {e}")
            raise DatabaseError(f"Failed to get email count from MS SQL Server: {e}") from e
