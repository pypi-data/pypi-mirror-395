"""
MariaDB database connector for Evolvishub Outlook Ingestor.

This module implements the MariaDB database connector using aiomysql
as an open-source MySQL alternative with enhanced features and performance.

Features:
- Async database operations with aiomysql
- Connection pooling for high throughput
- Proper database schema with indexes
- Batch insert operations with ON DUPLICATE KEY UPDATE
- Transaction support with isolation levels
- JSON fields for email metadata and headers (MariaDB 10.2+)
- Full-text search capabilities
- Optimized for MariaDB performance features
"""

import asyncio
import json
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from uuid import UUID

import aiomysql
from aiomysql import Connection, Pool

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


class MariaDBConnector(BaseConnector):
    """MariaDB database connector using aiomysql."""
    
    def __init__(self, name: str, config: Dict[str, Any], **kwargs):
        """
        Initialize MariaDB connector.
        
        Args:
            name: Connector name
            config: Configuration dictionary containing:
                - host: MariaDB host
                - port: MariaDB port (default: 3306)
                - database: Database name
                - username: Database username
                - password: Database password
                - charset: Character set (default: utf8mb4)
                - use_unicode: Use unicode (default: True)
                - autocommit: Auto commit mode (default: False)
                - connect_timeout: Connection timeout in seconds
                - read_timeout: Read timeout in seconds
                - write_timeout: Write timeout in seconds
                - pool_size: Connection pool size
                - max_overflow: Maximum pool overflow
                - ssl_disabled: Disable SSL (default: False)
                - sql_mode: SQL mode settings
        """
        super().__init__(name, config, **kwargs)

        # Get credential manager (lazy loading)
        get_credential_manager, create_secure_dsn, _, _ = _get_security_utils()
        self._credential_manager = get_credential_manager()
        self._create_secure_dsn = create_secure_dsn

        # MariaDB configuration
        self.host = config.get("host", "localhost")
        self.port = config.get("port", 3306)
        self.database = config.get("database", "outlook_data")
        self.username = config.get("username", "root")
        self.charset = config.get("charset", "utf8mb4")
        self.use_unicode = config.get("use_unicode", True)
        self.autocommit = config.get("autocommit", False)
        self.connect_timeout = config.get("connect_timeout", 30)
        self.read_timeout = config.get("read_timeout", 30)
        self.write_timeout = config.get("write_timeout", 30)
        self.ssl_disabled = config.get("ssl_disabled", False)
        self.sql_mode = config.get("sql_mode", "STRICT_TRANS_TABLES,NO_ZERO_DATE,NO_ZERO_IN_DATE,ERROR_FOR_DIVISION_BY_ZERO")

        # Secure password handling
        password_raw = config.get("password", "")
        password_env = config.get("password_env", "MARIADB_PASSWORD")

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
        """Initialize single MariaDB connection (not used with pooling)."""
        try:
            # Decrypt password for connection
            password = ""
            if self._encrypted_password:
                password = self._credential_manager.decrypt_credential(self._encrypted_password)
            
            self.logger.info(
                "Connecting to MariaDB",
                host=self.host,
                database=self.database,
                connector=self.name
            )
            
            self._connection = await aiomysql.connect(
                host=self.host,
                port=self.port,
                user=self.username,
                password=password,
                db=self.database,
                charset=self.charset,
                use_unicode=self.use_unicode,
                autocommit=self.autocommit,
                connect_timeout=self.connect_timeout,
                read_timeout=self.read_timeout,
                write_timeout=self.write_timeout,
                ssl_disabled=self.ssl_disabled
            )
            
            # Set SQL mode
            async with self._connection.cursor() as cursor:
                await cursor.execute(f"SET sql_mode = '{self.sql_mode}'")
                await self._connection.commit()
            
            self.logger.info(
                "MariaDB connection established",
                host=self.host,
                database=self.database,
                connector=self.name
            )
            
        except Exception as e:
            raise ConnectionError(
                f"Failed to connect to MariaDB: {e}",
                database_type="mariadb",
                cause=e
            )
    
    async def _initialize_pool(self) -> None:
        """Initialize MariaDB connection pool."""
        try:
            # Decrypt password for connection
            password = ""
            if self._encrypted_password:
                password = self._credential_manager.decrypt_credential(self._encrypted_password)
            
            self.logger.info(
                "Creating MariaDB connection pool",
                host=self.host,
                database=self.database,
                pool_size=self._pool_config.max_size,
                connector=self.name
            )
            
            self.pool = await aiomysql.create_pool(
                host=self.host,
                port=self.port,
                user=self.username,
                password=password,
                db=self.database,
                charset=self.charset,
                use_unicode=self.use_unicode,
                autocommit=self.autocommit,
                connect_timeout=self.connect_timeout,
                read_timeout=self.read_timeout,
                write_timeout=self.write_timeout,
                ssl_disabled=self.ssl_disabled,
                minsize=self._pool_config.min_size,
                maxsize=self._pool_config.max_size
            )
            
            # Set SQL mode for pool connections
            async with self.pool.acquire() as connection:
                async with connection.cursor() as cursor:
                    await cursor.execute(f"SET sql_mode = '{self.sql_mode}'")
                    await connection.commit()
            
            self.logger.info(
                "MariaDB connection pool created",
                host=self.host,
                database=self.database,
                connector=self.name
            )
            
        except Exception as e:
            raise ConnectionError(
                f"Failed to create MariaDB connection pool: {e}",
                database_type="mariadb",
                cause=e
            )
    
    async def _cleanup_connection(self) -> None:
        """Cleanup MariaDB connection."""
        if self._connection:
            try:
                self._connection.close()
                self.logger.info("MariaDB connection closed", connector=self.name)
            except Exception as e:
                self.logger.warning(
                    "Error closing MariaDB connection",
                    connector=self.name,
                    error=str(e)
                )
            finally:
                self._connection = None
    
    async def _cleanup_pool(self) -> None:
        """Cleanup MariaDB connection pool."""
        if self.pool:
            try:
                self.pool.close()
                await self.pool.wait_closed()
                self.logger.info("MariaDB connection pool closed", connector=self.name)
            except Exception as e:
                self.logger.warning(
                    "Error closing MariaDB connection pool",
                    connector=self.name,
                    error=str(e)
                )
            finally:
                self.pool = None
    
    async def _test_connection(self) -> None:
        """Test MariaDB connection."""
        try:
            if self.enable_connection_pooling:
                async with self.pool.acquire() as connection:
                    async with connection.cursor() as cursor:
                        await cursor.execute("SELECT 1")
                        result = await cursor.fetchone()
                        if result[0] != 1:
                            raise ConnectionError("MariaDB connection test failed")
            else:
                async with self._connection.cursor() as cursor:
                    await cursor.execute("SELECT 1")
                    result = await cursor.fetchone()
                    if result[0] != 1:
                        raise ConnectionError("MariaDB connection test failed")
                        
            self.logger.debug("MariaDB connection test passed", connector=self.name)
            
        except Exception as e:
            raise ConnectionError(f"MariaDB connection test failed: {e}")
    
    async def _initialize_schema(self) -> None:
        """Initialize MariaDB database schema."""
        try:
            self.logger.info("Initializing MariaDB schema", connector=self.name)
            
            if self.enable_connection_pooling:
                async with self.pool.acquire() as connection:
                    await self._execute_schema_statements(connection)
            else:
                await self._execute_schema_statements(self._connection)
            
            self.logger.info("MariaDB schema initialized", connector=self.name)
            
        except Exception as e:
            raise DatabaseError(
                f"Failed to initialize MariaDB schema: {e}",
                database_type="mariadb",
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
    
    def _get_schema_sql(self) -> List[str]:
        """Get MariaDB schema SQL statements."""
        return [
            # Emails table
            """
            CREATE TABLE IF NOT EXISTS emails (
                id VARCHAR(255) PRIMARY KEY,
                message_id VARCHAR(255) UNIQUE,
                subject TEXT,
                body LONGTEXT,
                body_preview TEXT,
                sender_email VARCHAR(255),
                sender_name VARCHAR(255),
                received_date DATETIME,
                sent_date DATETIME,
                importance VARCHAR(50),
                is_read BOOLEAN DEFAULT FALSE,
                has_attachments BOOLEAN DEFAULT FALSE,
                folder_id VARCHAR(255),
                folder_name VARCHAR(255),
                categories JSON,  -- JSON field for MariaDB 10.2+
                headers JSON,     -- JSON field for MariaDB 10.2+
                metadata JSON,    -- JSON field for MariaDB 10.2+
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """,
            
            # Recipients table
            """
            CREATE TABLE IF NOT EXISTS email_recipients (
                id INT AUTO_INCREMENT PRIMARY KEY,
                email_id VARCHAR(255) NOT NULL,
                recipient_type ENUM('to', 'cc', 'bcc') NOT NULL,
                email_address VARCHAR(255) NOT NULL,
                display_name VARCHAR(255),
                INDEX idx_email_id (email_id),
                FOREIGN KEY (email_id) REFERENCES emails (id) ON DELETE CASCADE
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """,

            # Attachments table
            """
            CREATE TABLE IF NOT EXISTS email_attachments (
                id VARCHAR(255) PRIMARY KEY,
                email_id VARCHAR(255) NOT NULL,
                name VARCHAR(255) NOT NULL,
                content_type VARCHAR(255),
                size BIGINT,
                content LONGBLOB,  -- For small attachments stored in database
                content_hash VARCHAR(255),
                is_inline BOOLEAN DEFAULT FALSE,
                attachment_type VARCHAR(50),
                extended_properties JSON,  -- JSON for storage info
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                INDEX idx_email_id (email_id),
                INDEX idx_content_hash (content_hash),
                FOREIGN KEY (email_id) REFERENCES emails (id) ON DELETE CASCADE
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """,

            # Folders table
            """
            CREATE TABLE IF NOT EXISTS outlook_folders (
                id VARCHAR(255) PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                parent_folder_id VARCHAR(255),
                folder_type VARCHAR(50),
                total_item_count INT DEFAULT 0,
                unread_item_count INT DEFAULT 0,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                INDEX idx_parent_folder (parent_folder_id)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """,

            # Additional indexes for performance
            "CREATE INDEX IF NOT EXISTS idx_emails_message_id ON emails (message_id)",
            "CREATE INDEX IF NOT EXISTS idx_emails_sender ON emails (sender_email)",
            "CREATE INDEX IF NOT EXISTS idx_emails_received_date ON emails (received_date)",
            "CREATE INDEX IF NOT EXISTS idx_emails_folder ON emails (folder_id)",
            "CREATE INDEX IF NOT EXISTS idx_emails_has_attachments ON emails (has_attachments)",
            "CREATE INDEX IF NOT EXISTS idx_recipients_type ON email_recipients (recipient_type)",

            # Full-text search indexes
            "CREATE FULLTEXT INDEX IF NOT EXISTS ft_emails_subject ON emails (subject)",
            "CREATE FULLTEXT INDEX IF NOT EXISTS ft_emails_body ON emails (body)",
            "CREATE FULLTEXT INDEX IF NOT EXISTS ft_emails_content ON emails (subject, body)"
        ]

    async def _store_email_impl(
        self,
        email: EmailMessage,
        transaction: Optional[Any] = None,
        **kwargs
    ) -> str:
        """Store email in MariaDB database."""
        try:
            connection = transaction if transaction else (
                self.pool.acquire() if self.enable_connection_pooling else self._connection
            )

            if self.enable_connection_pooling and not transaction:
                async with connection as conn:
                    return await self._store_email_with_connection(email, conn, transaction)
            else:
                return await self._store_email_with_connection(email, connection, transaction)

        except Exception as e:
            raise DatabaseError(
                f"Failed to store email in MariaDB: {e}",
                database_type="mariadb",
                operation="store_email",
                cause=e
            )

    async def _store_email_with_connection(self, email: EmailMessage, connection: Connection, transaction: Optional[Any] = None) -> str:
        """Store email with specific connection."""
        async with connection.cursor() as cursor:
            # Prepare email data
            email_data = self._prepare_email_data(email)

            # Use INSERT ... ON DUPLICATE KEY UPDATE for upsert
            insert_sql = """
            INSERT INTO emails (
                id, message_id, subject, body, body_preview,
                sender_email, sender_name, received_date, sent_date,
                importance, is_read, has_attachments, folder_id, folder_name,
                categories, headers, metadata, updated_at
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                message_id = VALUES(message_id),
                subject = VALUES(subject),
                body = VALUES(body),
                body_preview = VALUES(body_preview),
                sender_email = VALUES(sender_email),
                sender_name = VALUES(sender_name),
                received_date = VALUES(received_date),
                sent_date = VALUES(sent_date),
                importance = VALUES(importance),
                is_read = VALUES(is_read),
                has_attachments = VALUES(has_attachments),
                folder_id = VALUES(folder_id),
                folder_name = VALUES(folder_name),
                categories = VALUES(categories),
                headers = VALUES(headers),
                metadata = VALUES(metadata),
                updated_at = VALUES(updated_at)
            """

            await cursor.execute(insert_sql, email_data)

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
        """Store multiple emails in MariaDB database."""
        try:
            connection = transaction if transaction else (
                self.pool.acquire() if self.enable_connection_pooling else self._connection
            )

            if self.enable_connection_pooling and not transaction:
                async with connection as conn:
                    return await self._store_emails_batch_with_connection(emails, conn, transaction)
            else:
                return await self._store_emails_batch_with_connection(emails, connection, transaction)

        except Exception as e:
            raise DatabaseError(
                f"Failed to store emails batch in MariaDB: {e}",
                database_type="mariadb",
                operation="store_emails_batch",
                cause=e
            )

    async def _store_emails_batch_with_connection(self, emails: List[EmailMessage], connection: Connection, transaction: Optional[Any] = None) -> List[str]:
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

            # Batch insert emails
            if email_data_batch:
                insert_sql = """
                INSERT INTO emails (
                    id, message_id, subject, body, body_preview,
                    sender_email, sender_name, received_date, sent_date,
                    importance, is_read, has_attachments, folder_id, folder_name,
                    categories, headers, metadata, updated_at
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    message_id = VALUES(message_id),
                    subject = VALUES(subject),
                    body = VALUES(body),
                    updated_at = VALUES(updated_at)
                """
                await cursor.executemany(insert_sql, email_data_batch)

            # Batch insert recipients
            if recipients_batch:
                await cursor.executemany(
                    """
                    INSERT INTO email_recipients (email_id, recipient_type, email_address, display_name)
                    VALUES (%s, %s, %s, %s)
                    """,
                    recipients_batch
                )

            # Batch insert attachments
            if attachments_batch:
                await cursor.executemany(
                    """
                    INSERT INTO email_attachments (
                        id, email_id, name, content_type, size, content,
                        content_hash, is_inline, attachment_type, extended_properties
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE
                        name = VALUES(name),
                        content_type = VALUES(content_type),
                        size = VALUES(size),
                        content = VALUES(content)
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
        """Retrieve email from MariaDB database."""
        try:
            if self.enable_connection_pooling:
                async with self.pool.acquire() as connection:
                    return await self._get_email_with_connection(email_id, include_attachments, connection)
            else:
                return await self._get_email_with_connection(email_id, include_attachments, self._connection)

        except Exception as e:
            raise DatabaseError(
                f"Failed to retrieve email from MariaDB: {e}",
                database_type="mariadb",
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
            await cursor.execute("SELECT * FROM emails WHERE id = %s", (email_id,))
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
        """Search emails in MariaDB database."""
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
                f"Failed to search emails in MariaDB: {e}",
                database_type="mariadb",
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
                query_parts.append("AND sender_email = %s")
                params.append(filters["sender_email"])

            if "subject_contains" in filters:
                query_parts.append("AND subject LIKE %s")
                params.append(f"%{filters['subject_contains']}%")

            if "date_from" in filters:
                query_parts.append("AND received_date >= %s")
                params.append(filters["date_from"])

            if "date_to" in filters:
                query_parts.append("AND received_date <= %s")
                params.append(filters["date_to"])

            if "folder_id" in filters:
                query_parts.append("AND folder_id = %s")
                params.append(filters["folder_id"])

            if "has_attachments" in filters:
                query_parts.append("AND has_attachments = %s")
                params.append(filters["has_attachments"])

            # Full-text search
            if "search_text" in filters:
                query_parts.append("AND MATCH(subject, body) AGAINST(%s IN NATURAL LANGUAGE MODE)")
                params.append(filters["search_text"])

            # Add sorting
            if sort_by:
                query_parts.append(f"ORDER BY {sort_by} {sort_order.upper()}")
            else:
                query_parts.append("ORDER BY received_date DESC")

            # Add pagination
            if limit:
                query_parts.append(f"LIMIT {limit}")

            if offset > 0:
                query_parts.append(f"OFFSET {offset}")

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
        """Begin MariaDB transaction."""
        try:
            if self.enable_connection_pooling:
                connection = await self.pool.acquire()
            else:
                connection = self._connection

            if isolation_level:
                await connection.execute(f"SET TRANSACTION ISOLATION LEVEL {isolation_level}")

            await connection.begin()
            return connection
        except Exception as e:
            raise TransactionError(f"Failed to begin MariaDB transaction: {e}")

    async def _commit_transaction(self, transaction: Any) -> None:
        """Commit MariaDB transaction."""
        try:
            await transaction.commit()
            if self.enable_connection_pooling:
                self.pool.release(transaction)
        except Exception as e:
            raise TransactionError(f"Failed to commit MariaDB transaction: {e}")

    async def _rollback_transaction(self, transaction: Any) -> None:
        """Rollback MariaDB transaction."""
        try:
            await transaction.rollback()
            if self.enable_connection_pooling:
                self.pool.release(transaction)
        except Exception as e:
            raise TransactionError(f"Failed to rollback MariaDB transaction: {e}")

    def _prepare_email_data(self, email: EmailMessage) -> tuple:
        """Prepare email data for MariaDB insertion."""
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
        """Prepare attachment data for MariaDB insertion."""
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
        """Convert MariaDB row to EmailMessage."""
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
                VALUES (%s, %s, %s, %s)
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
                INSERT INTO email_attachments (
                    id, email_id, name, content_type, size, content,
                    content_hash, is_inline, attachment_type, extended_properties
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    name = VALUES(name),
                    content_type = VALUES(content_type),
                    size = VALUES(size),
                    content = VALUES(content)
                """,
                attachment_data
            )

    async def _get_recipients_with_cursor(self, cursor, email_id: str) -> Dict[str, List]:
        """Get email recipients with cursor."""
        from evolvishub_outlook_ingestor.core.data_models import EmailAddress

        recipients = {"to": [], "cc": [], "bcc": []}

        await cursor.execute(
            "SELECT recipient_type, email_address, display_name FROM email_recipients WHERE email_id = %s",
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
            "SELECT * FROM email_attachments WHERE email_id = %s",
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


# DatabaseConnector interface implementation for MariaDB
from evolvishub_outlook_ingestor.connectors.database_connector import (
    DatabaseConnector,
    DatabaseConfig,
)
from typing import Union


class MariaDBDatabaseConnector(DatabaseConnector):
    """
    Production-ready MariaDB database connector for email ingestion.

    This connector provides enterprise-grade MariaDB integration with:
    - Connection pooling for high performance
    - Proper schema management
    - Batch processing for efficiency
    - Comprehensive error handling
    - Transaction support with MySQL optimizations
    """

    def __init__(self, config: Union[DatabaseConfig, Dict[str, Any]]):
        """
        Initialize MariaDB connector.

        Args:
            config: Database configuration (DatabaseConfig or legacy dict format)
        """
        # Handle backward compatibility with old dict-based config
        if isinstance(config, dict):
            db_config = DatabaseConfig(
                database_type="mariadb",
                host=config.get('host'),
                port=config.get('port', 3306),
                database=config.get('database'),
                username=config.get('username'),
                password=config.get('password'),
                table_name=config.get('table_name', 'emails'),
                batch_size=config.get('batch_size', 100),
                max_connections=config.get('max_pool_size', 10),
                charset=config.get('charset', 'utf8mb4'),
                autocommit=config.get('autocommit', False),
                connect_timeout=config.get('connect_timeout', 60)
            )
        else:
            db_config = config

        super().__init__(db_config)
        self._pool = None
        self._validate_mariadb_config()

    def _validate_mariadb_config(self):
        """Validate MariaDB-specific configuration."""
        if not self.config.host:
            raise ValueError("MariaDB host is required")
        if not self.config.database:
            raise ValueError("MariaDB database name is required")
        if not self.config.username:
            raise ValueError("MariaDB username is required")

    async def _connect(self):
        """Establish MariaDB connection pool."""
        try:
            import aiomysql

            # Create connection pool
            self._pool = await aiomysql.create_pool(
                host=self.config.host,
                port=self.config.port or 3306,
                user=self.config.username,
                password=self.config.password or '',
                db=self.config.database,
                charset=self.config.charset,
                autocommit=self.config.autocommit,
                minsize=5,
                maxsize=self.config.max_connections,
                connect_timeout=self.config.connect_timeout,
                echo=False
            )

            self._connection = self._pool
            self.logger.info("MariaDB connection pool established")

        except Exception as e:
            self.logger.error(f"Failed to connect to MariaDB: {e}")
            raise DatabaseError(f"Failed to connect to MariaDB: {e}") from e

    async def _disconnect(self):
        """Close MariaDB connection pool."""
        try:
            if self._pool:
                self._pool.close()
                await self._pool.wait_closed()
                self._pool = None
                self._connection = None
            self.logger.info("MariaDB connection pool closed")

        except Exception as e:
            self.logger.error(f"Failed to disconnect from MariaDB: {e}")
            raise DatabaseError(f"Failed to disconnect from MariaDB: {e}") from e

    async def _create_schema(self):
        """Create MariaDB schema/tables if they don't exist."""
        try:
            async with self._pool.acquire() as connection:
                async with connection.cursor() as cursor:
                    # Create emails table with MariaDB optimizations
                    await cursor.execute(f"""
                        CREATE TABLE IF NOT EXISTS {self.config.table_name} (
                            id BIGINT AUTO_INCREMENT PRIMARY KEY,
                            message_id VARCHAR(255) UNIQUE NOT NULL,
                            subject TEXT,
                            sender_email VARCHAR(255),
                            sender_name VARCHAR(255),
                            received_datetime DATETIME(6),
                            sent_datetime DATETIME(6),
                            body_text LONGTEXT,
                            body_html LONGTEXT,
                            importance ENUM('low', 'normal', 'high') DEFAULT 'normal',
                            sensitivity ENUM('normal', 'personal', 'private', 'confidential') DEFAULT 'normal',
                            has_attachments BOOLEAN DEFAULT FALSE,
                            attachment_count INT DEFAULT 0,
                            folder_path VARCHAR(500),
                            categories JSON,
                            headers JSON,
                            metadata JSON,
                            created_at DATETIME(6) DEFAULT CURRENT_TIMESTAMP(6),
                            updated_at DATETIME(6) DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
                            INDEX idx_message_id (message_id),
                            INDEX idx_received_datetime (received_datetime DESC),
                            INDEX idx_sender_email (sender_email),
                            INDEX idx_folder_path (folder_path),
                            FULLTEXT INDEX idx_subject_body (subject, body_text)
                        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
                    """)

            self.logger.info("MariaDB schema created successfully")

        except Exception as e:
            self.logger.error(f"Failed to create MariaDB schema: {e}")
            raise DatabaseError(f"Failed to create MariaDB schema: {e}") from e

    async def _store_email_batch(self, emails: List[EmailMessage]) -> int:
        """Store a batch of emails in MariaDB."""
        if not emails:
            return 0

        try:
            async with self._pool.acquire() as connection:
                async with connection.cursor() as cursor:
                    stored_count = 0

                    for email in emails:
                        # Use INSERT ... ON DUPLICATE KEY UPDATE for MariaDB
                        sql = f"""
                            INSERT INTO {self.config.table_name} (
                                message_id, subject, sender_email, sender_name,
                                received_datetime, sent_datetime, body_text, body_html,
                                importance, sensitivity, has_attachments, attachment_count,
                                folder_path, categories, headers, metadata
                            ) VALUES (
                                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                            ) ON DUPLICATE KEY UPDATE
                                subject = VALUES(subject),
                                sender_email = VALUES(sender_email),
                                sender_name = VALUES(sender_name),
                                received_datetime = VALUES(received_datetime),
                                sent_datetime = VALUES(sent_datetime),
                                body_text = VALUES(body_text),
                                body_html = VALUES(body_html),
                                importance = VALUES(importance),
                                sensitivity = VALUES(sensitivity),
                                has_attachments = VALUES(has_attachments),
                                attachment_count = VALUES(attachment_count),
                                folder_path = VALUES(folder_path),
                                categories = VALUES(categories),
                                headers = VALUES(headers),
                                metadata = VALUES(metadata),
                                updated_at = CURRENT_TIMESTAMP(6)
                        """

                        values = (
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
                    self.logger.info(f"Stored {stored_count} emails in MariaDB batch")
                    return stored_count

        except Exception as e:
            self.logger.error(f"Failed to store email batch in MariaDB: {e}")
            raise DatabaseError(f"Failed to store email batch in MariaDB: {e}") from e

    async def _store_single_email(self, email: EmailMessage) -> bool:
        """Store a single email in MariaDB."""
        try:
            result = await self._store_email_batch([email])
            return result > 0

        except Exception as e:
            self.logger.error(f"Failed to store single email in MariaDB: {e}")
            raise DatabaseError(f"Failed to store single email in MariaDB: {e}") from e

    async def _check_email_exists(self, email_id: str) -> bool:
        """Check if email exists in MariaDB."""
        try:
            async with self._pool.acquire() as connection:
                async with connection.cursor() as cursor:
                    await cursor.execute(
                        f"SELECT 1 FROM {self.config.table_name} WHERE message_id = %s",
                        (email_id,)
                    )
                    result = await cursor.fetchone()
                    return result is not None

        except Exception as e:
            self.logger.error(f"Failed to check email existence in MariaDB: {e}")
            raise DatabaseError(f"Failed to check email existence in MariaDB: {e}") from e

    async def _get_total_email_count(self) -> int:
        """Get total email count from MariaDB."""
        try:
            async with self._pool.acquire() as connection:
                async with connection.cursor() as cursor:
                    await cursor.execute(f"SELECT COUNT(*) FROM {self.config.table_name}")
                    result = await cursor.fetchone()
                    return result[0] if result else 0

        except Exception as e:
            self.logger.error(f"Failed to get email count from MariaDB: {e}")
            raise DatabaseError(f"Failed to get email count from MariaDB: {e}") from e
