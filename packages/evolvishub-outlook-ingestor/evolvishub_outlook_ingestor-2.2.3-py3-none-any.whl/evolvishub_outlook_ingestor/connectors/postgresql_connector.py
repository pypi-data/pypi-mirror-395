"""
PostgreSQL database connector for Evolvishub Outlook Email Ingestor.

This module provides a production-ready PostgreSQL database connector
specifically designed for email ingestion operations using the new
DatabaseConnector interface.
"""

import asyncio
from typing import Any, Dict, List, Optional, Union
from datetime import datetime
import json

from evolvishub_outlook_ingestor.connectors.database_connector import (
    DatabaseConnector,
    DatabaseConfig,
)
from evolvishub_outlook_ingestor.core.data_models import (
    EmailMessage, EmailAttachment, OutlookFolder, ProcessingResult
)
from evolvishub_outlook_ingestor.core.exceptions import DatabaseError


class PostgreSQLConnector(DatabaseConnector):
    """
    Production-ready PostgreSQL database connector for email ingestion.

    This connector provides enterprise-grade PostgreSQL integration with:
    - Connection pooling for high performance
    - Proper schema management
    - Batch processing for efficiency
    - Comprehensive error handling
    - Transaction support
    """

    def __init__(self, config: Union[DatabaseConfig, Dict[str, Any]]):
        """
        Initialize PostgreSQL connector.

        Args:
            config: Database configuration (DatabaseConfig or legacy dict format)
        """
        # Handle backward compatibility with old dict-based config
        if isinstance(config, dict):
            db_config = DatabaseConfig(
                database_type="postgresql",
                host=config.get('host'),
                port=config.get('port', 5432),
                database=config.get('database'),
                username=config.get('username'),
                password=config.get('password'),
                table_name=config.get('table_name', 'emails'),
                table_prefix=config.get('table_prefix', ''),
                batch_size=config.get('batch_size', 100),
                max_connections=config.get('max_pool_size', 10)
            )
        else:
            db_config = config

        super().__init__(db_config)
        self._pool = None
        self._validate_postgresql_config()

        # Set up table names with prefix
        self._emails_table = f"{self.config.table_prefix}emails"
        self._attachments_table = f"{self.config.table_prefix}email_attachments"
        self._folders_table = f"{self.config.table_prefix}outlook_folders"

    def _validate_postgresql_config(self):
        """Validate PostgreSQL-specific configuration."""
        if not self.config.host:
            raise ValueError("PostgreSQL host is required")
        if not self.config.database:
            raise ValueError("PostgreSQL database name is required")
        if not self.config.username:
            raise ValueError("PostgreSQL username is required")
    
    async def _connect(self):
        """Establish PostgreSQL connection pool."""
        try:
            import asyncpg

            # Build connection string
            if self.config.connection_string:
                dsn = self.config.connection_string
            else:
                dsn = f"postgresql://{self.config.username}"
                if self.config.password:
                    dsn += f":{self.config.password}"
                dsn += f"@{self.config.host}:{self.config.port or 5432}/{self.config.database}"

            # Create connection pool
            self._pool = await asyncpg.create_pool(
                dsn,
                min_size=5,
                max_size=self.config.max_connections,
                command_timeout=60,
                server_settings={
                    'application_name': 'evolvishub-outlook-ingestor',
                    'timezone': 'UTC'
                }
            )

            self._connection = self._pool
            self.logger.info("PostgreSQL connection pool established")

        except ImportError:
            raise DatabaseError(
                "asyncpg library not installed. "
                "Install with: pip install asyncpg"
            )
        except Exception as e:
            raise DatabaseError(f"Failed to connect to PostgreSQL: {e}")

    async def _disconnect(self):
        """Close PostgreSQL connection pool."""
        if self._pool:
            await self._pool.close()
            self._pool = None
            self._connection = None
            self.logger.info("PostgreSQL connection pool closed")
    
    async def _create_schema(self):
        """Create database schema for email storage."""
        async with self._pool.acquire() as conn:
            # Create emails table
            await conn.execute(f"""
                CREATE TABLE IF NOT EXISTS {self._emails_table} (
                    id VARCHAR(255) PRIMARY KEY,
                    relevant_email BOOLEAN DEFAULT FALSE,
                    email_address_source VARCHAR(255),
                    message_id VARCHAR(255),
                    conversation_id VARCHAR(255),
                    conversation_index VARCHAR,
                    subject TEXT,
                    body TEXT,
                    body_html TEXT,
                    body_preview TEXT,
                    body_text TEXT,
                    body_type VARCHAR(50) DEFAULT 'text',
                    is_html BOOLEAN DEFAULT FALSE,
                    sender_email VARCHAR(255),
                    sender_name VARCHAR(255),
                    from_email VARCHAR(255),
                    from_name VARCHAR(255),
                    to_recipients JSONB DEFAULT '[]',
                    cc_recipients JSONB DEFAULT '[]',
                    bcc_recipients JSONB DEFAULT '[]',
                    reply_to JSONB DEFAULT '[]',
                    sent_date TIMESTAMP WITH TIME ZONE,
                    received_date TIMESTAMP WITH TIME ZONE,
                    created_date TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                    modified_date TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                    importance VARCHAR(20) DEFAULT 'normal',
                    sensitivity VARCHAR(20) DEFAULT 'normal',
                    priority VARCHAR(20),
                    is_read BOOLEAN DEFAULT FALSE,
                    is_draft BOOLEAN DEFAULT FALSE,
                    has_attachments BOOLEAN DEFAULT FALSE,
                    is_flagged BOOLEAN DEFAULT FALSE,
                    folder_id VARCHAR(255),
                    folder_path TEXT,
                    headers JSONB DEFAULT '{{}}',
                    internet_headers JSONB DEFAULT '{{}}',
                    categories JSONB DEFAULT '[]',
                    in_reply_to VARCHAR(255),
                    "references" JSONB DEFAULT '[]',
                    size INTEGER,
                    extended_properties JSONB DEFAULT '{{}}'
                )
            """)

            # Create attachments table
            await conn.execute(f"""
                CREATE TABLE IF NOT EXISTS {self._attachments_table} (
                    id VARCHAR(255) PRIMARY KEY,
                    email_id VARCHAR(255) REFERENCES {self._emails_table}(id) ON DELETE CASCADE,
                    name VARCHAR(255) NOT NULL,
                    content_type VARCHAR(255),
                    size INTEGER,
                    attachment_type VARCHAR(50) DEFAULT 'file',
                    is_inline BOOLEAN DEFAULT FALSE,
                    content_id VARCHAR(255),
                    content_location VARCHAR(255),
                    content_bytes BYTEA,
                    download_url TEXT,
                    created_date TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                    modified_date TIMESTAMP WITH TIME ZONE DEFAULT NOW()
                )
            """)
            
            # Create folders table
            await conn.execute(f"""
                CREATE TABLE IF NOT EXISTS {self._folders_table} (
                    id VARCHAR(255) PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    display_name VARCHAR(255),
                    parent_folder_id VARCHAR(255),
                    folder_path TEXT,
                    folder_type VARCHAR(50),
                    total_item_count INTEGER DEFAULT 0,
                    unread_item_count INTEGER DEFAULT 0,
                    child_folder_count INTEGER DEFAULT 0,
                    is_hidden BOOLEAN DEFAULT FALSE,
                    created_date TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                    modified_date TIMESTAMP WITH TIME ZONE DEFAULT NOW()
                )
            """)
            
            # Create indexes for better performance
            await conn.execute(f"CREATE INDEX IF NOT EXISTS idx_{self.config.table_prefix}emails_message_id ON {self._emails_table}(message_id)")
            await conn.execute(f"CREATE INDEX IF NOT EXISTS idx_{self.config.table_prefix}emails_conversation_id ON {self._emails_table}(conversation_id)")
            await conn.execute(f"CREATE INDEX IF NOT EXISTS idx_{self.config.table_prefix}emails_sent_date ON {self._emails_table}(sent_date)")
            await conn.execute(f"CREATE INDEX IF NOT EXISTS idx_{self.config.table_prefix}emails_received_date ON {self._emails_table}(received_date)")
            await conn.execute(f"CREATE INDEX IF NOT EXISTS idx_{self.config.table_prefix}emails_folder_id ON {self._emails_table}(folder_id)")
            await conn.execute(f"CREATE INDEX IF NOT EXISTS idx_{self.config.table_prefix}emails_sender_email ON {self._emails_table}(sender_email)")
            await conn.execute(f"CREATE INDEX IF NOT EXISTS idx_{self.config.table_prefix}attachments_email_id ON {self._attachments_table}(email_id)")
            await conn.execute(f"CREATE INDEX IF NOT EXISTS idx_{self.config.table_prefix}folders_parent_id ON {self._folders_table}(parent_folder_id)")

            self.logger.info("PostgreSQL schema created successfully")

    # Required abstract methods for DatabaseConnector interface

    async def _store_email_batch(self, emails: List[EmailMessage]) -> int:
        """Store a batch of emails in PostgreSQL."""
        if not emails:
            return 0

        stored_count = 0
        t = 0
        async with self._pool.acquire() as conn:
            async with conn.transaction():
                for email in emails:
                    try:
                        # Convert email to database format
                        email_data = self._email_to_db_format(email)

                        # Insert or update email
                        await conn.execute(f"""
                            INSERT INTO {self._emails_table} (
                                id,email_address_source,relevant_email, message_id, conversation_id, conversation_index, subject, body_html, body_preview, body_text, body_type, is_html,
                                sender_email, sender_name, from_email, from_name, to_recipients, cc_recipients, bcc_recipients, reply_to,
                                sent_date, received_date, created_date, modified_date, importance, sensitivity, priority,
                                is_read, is_draft, has_attachments, is_flagged, folder_id, folder_path, headers,
                                internet_headers, categories, in_reply_to, "references", size, extended_properties
                            ) VALUES (
                                $1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16,
                                $17, $18, $19, $20, $21, $22, $23, $24, $25, $26, $27, $28, $29, $30,
                                $31, $32, $33, $34, $35, $36, $37, $38, $39, $40
                            ) ON CONFLICT (id) DO UPDATE SET
                                subject = EXCLUDED.subject,
                                body = EXCLUDED.body,
                                is_read = EXCLUDED.is_read,
                                modified_date = EXCLUDED.modified_date
                        """, *email_data)

                        stored_count += 1

                    except Exception as e:
                        self.logger.warning(f"Failed to store email {email.id}: {e}")
                        continue

        return stored_count

    async def _store_single_email(self, email: EmailMessage) -> bool:
        """Store a single email in PostgreSQL."""
        try:
            result = await self._store_email_batch([email])
            return result > 0
        except Exception as e:
            self.logger.error(f"Failed to store single email: {e}")
            return False

    async def _check_email_exists(self, email_id: str) -> bool:
        """Check if email exists in PostgreSQL."""
        async with self._pool.acquire() as conn:
            result = await conn.fetchval(
                f"SELECT 1 FROM {self._emails_table} WHERE id = $1",
                email_id
            )
            return result is not None

    async def _get_total_email_count(self) -> int:
        """Get total email count from PostgreSQL."""
        async with self._pool.acquire() as conn:
            count = await conn.fetchval(f"SELECT COUNT(*) FROM {self._emails_table}")
            return count or 0

    def _email_to_db_format(self, email: EmailMessage) -> tuple:
        """Convert EmailMessage to database format for the new interface."""
        # Convert recipients to JSON
        to_recipients = [{"email": addr.email, "name": addr.name} for addr in email.to_recipients] if hasattr(email, 'to_recipients') and email.to_recipients else []
        cc_recipients = [{"email": addr.email, "name": addr.name} for addr in email.cc_recipients] if hasattr(email, 'cc_recipients') and email.cc_recipients else []
        bcc_recipients = [{"email": addr.email, "name": addr.name} for addr in email.bcc_recipients] if hasattr(email, 'bcc_recipients') and email.bcc_recipients else []
        reply_to = [{"email": addr.email, "name": addr.name} for addr in email.reply_to] if hasattr(email, 'reply_to') and email.reply_to else []

        return (
            email.id,
            email.email_address_source,
            email.is_valid_email,
            email.message_id,
            email.conversation_id,
            email.conversation_index,
            email.subject,
            getattr(email, 'body_html', ''),
            getattr(email, 'body_preview', ''),
            getattr(email, 'body_text', ''),
            getattr(email, 'body_type', 'text'),
            email.is_html,
            email.sender.email if email.sender else None,
            email.sender.name if email.sender else None,
            getattr(email, 'from_address', email.sender).email if getattr(email, 'from_address', email.sender) else None,
            getattr(email, 'from_address', email.sender).name if getattr(email, 'from_address', email.sender) else None,
            json.dumps(to_recipients),
            json.dumps(cc_recipients),
            json.dumps(bcc_recipients),
            json.dumps(reply_to),
            email.sent_date,
            email.received_date,
            getattr(email, 'created_date', None),
            getattr(email, 'modified_date', None),
            getattr(email, 'importance', 'normal'),
            getattr(email, 'sensitivity', 'normal'),
            getattr(email, 'priority', 'normal'),
            email.is_read,
            email.is_draft,
            email.has_attachments,
            getattr(email, 'is_flagged', False),
            getattr(email, 'folder_id', None),
            getattr(email, 'folder_path', ''),
            json.dumps(getattr(email, 'headers', {})),
            json.dumps(getattr(email, 'internet_headers', {})),
            json.dumps(getattr(email, 'categories', [])),
            getattr(email, 'in_reply_to', None),
            json.dumps(getattr(email, 'references', [])),
            getattr(email, 'size', 0),
            json.dumps(getattr(email, 'extended_properties', {}))
        )

    # Legacy methods for backward compatibility
    async def store_email(self, email: EmailMessage) -> bool:
        """Store an email message in the database (legacy method)."""
        return await self._store_single_email(email)

    async def initialize(self) -> None:
        """Initialize the PostgreSQL connector (legacy method)."""
        return await super().initialize()

    async def disconnect(self) -> None:
        """Disconnect from PostgreSQL (legacy method)."""
        return await self.cleanup()

    # Keep existing methods for backward compatibility but update to use new pool reference
    async def store_email_legacy(self, email: EmailMessage) -> bool:
        """Store an email message in the database (original implementation)."""
        try:
            async with self._pool.acquire() as conn:
                # Convert email addresses to JSON
                to_recipients = [{"email": addr.email, "name": addr.name} for addr in email.to_recipients] if hasattr(email, 'to_recipients') and email.to_recipients else []
                cc_recipients = [{"email": addr.email, "name": addr.name} for addr in email.cc_recipients] if hasattr(email, 'cc_recipients') and email.cc_recipients else []
                bcc_recipients = [{"email": addr.email, "name": addr.name} for addr in email.bcc_recipients] if hasattr(email, 'bcc_recipients') and email.bcc_recipients else []
                reply_to = [{"email": addr.email, "name": addr.name} for addr in email.reply_to] if hasattr(email, 'reply_to') and email.reply_to else []
                
                # Insert email
                await conn.execute(f"""
                    INSERT INTO {self._emails_table} (
                        id, message_id, conversation_id, subject, body, body_preview,
                        body_type, is_html, sender_email, sender_name, from_email, from_name,
                        to_recipients, cc_recipients, bcc_recipients, reply_to,
                        sent_date, received_date, importance, sensitivity, priority,
                        is_read, is_draft, has_attachments, is_flagged,
                        folder_id, folder_path, headers, internet_headers,
                        categories, in_reply_to, "references", size, extended_properties
                    ) VALUES (
                        $1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12,
                        $13, $14, $15, $16, $17, $18, $19, $20, $21,
                        $22, $23, $24, $25, $26, $27, $28, $29,
                        $30, $31, $32, $33, $34
                    ) ON CONFLICT (id) DO UPDATE SET
                        subject = EXCLUDED.subject,
                        body = EXCLUDED.body,
                        modified_date = NOW()
                """, 
                    email.id, email.message_id, email.conversation_id,
                    email.subject, email.body, email.body_preview,
                    email.body_type, email.is_html,
                    email.sender.email if email.sender else None,
                    email.sender.name if email.sender else None,
                    email.from_address.email if email.from_address else None,
                    email.from_address.name if email.from_address else None,
                    json.dumps(to_recipients), json.dumps(cc_recipients),
                    json.dumps(bcc_recipients), json.dumps(reply_to),
                    email.sent_date, email.received_date,
                    email.importance.value, email.sensitivity.value, email.priority,
                    email.is_read, email.is_draft, email.has_attachments, email.is_flagged,
                    email.folder_id, email.folder_path,
                    json.dumps(email.headers), json.dumps(email.internet_headers),
                    json.dumps(email.categories), email.in_reply_to,
                    json.dumps(email.references), email.size,
                    json.dumps(email.extended_properties)
                )
                
                # Store attachments
                for attachment in email.attachments:
                    await self.store_attachment(attachment, email.id, conn)
                
                return True
                
        except Exception as e:
            self.logger.error(f"Failed to store email {email.id}: {str(e)}")
            raise DatabaseError(f"Failed to store email: {str(e)}")
    
    async def store_attachment(self, attachment: EmailAttachment, email_id: str, conn=None) -> bool:
        """Store an email attachment."""
        try:
            if conn is None:
                async with self._pool.acquire() as conn:
                    return await self._store_attachment_with_conn(attachment, email_id, conn)
            else:
                return await self._store_attachment_with_conn(attachment, email_id, conn)
        except Exception as e:
            self.logger.error(f"Failed to store attachment {attachment.id}: {str(e)}")
            raise DatabaseError(f"Failed to store attachment: {str(e)}")
    
    async def _store_attachment_with_conn(self, attachment: EmailAttachment, email_id: str, conn) -> bool:
        """Store attachment with existing connection."""
        await conn.execute(f"""
            INSERT INTO {self._attachments_table} (
                id, email_id, name, content_type, size, attachment_type,
                is_inline, content_id, content_location, content_bytes, download_url
            ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11)
            ON CONFLICT (id) DO UPDATE SET
                name = EXCLUDED.name,
                content_type = EXCLUDED.content_type,
                modified_date = NOW()
        """,
            attachment.id, email_id, attachment.name, attachment.content_type,
            attachment.size, attachment.attachment_type.value, attachment.is_inline,
            attachment.content_id, attachment.content_location,
            attachment.content_bytes, attachment.download_url
        )
        return True

    async def get_email(self, email_id: str) -> Optional[EmailMessage]:
        """Retrieve an email by ID."""
        try:
            async with self._pool.acquire() as conn:
                row = await conn.fetchrow(f"SELECT * FROM {self._emails_table} WHERE id = $1", email_id)
                if not row:
                    return None

                # Get attachments
                attachment_rows = await conn.fetch(
                    f"SELECT * FROM {self._attachments_table} WHERE email_id = $1", email_id
                )

                return self._row_to_email(row, attachment_rows)

        except Exception as e:
            self.logger.error(f"Failed to get email {email_id}: {str(e)}")
            raise DatabaseError(f"Failed to get email: {str(e)}")

    async def get_emails_by_folder(self, folder_id: str, limit: int = 100, offset: int = 0) -> List[EmailMessage]:
        """Get emails from a specific folder."""
        try:
            async with self._pool.acquire() as conn:
                rows = await conn.fetch(f"""
                    SELECT * FROM {self._emails_table}
                    WHERE folder_id = $1
                    ORDER BY received_date DESC
                    LIMIT $2 OFFSET $3
                """, folder_id, limit, offset)

                emails = []
                for row in rows:
                    # Get attachments for this email
                    attachment_rows = await conn.fetch(
                        f"SELECT * FROM {self._attachments_table} WHERE email_id = $1", row['id']
                    )
                    emails.append(self._row_to_email(row, attachment_rows))

                return emails

        except Exception as e:
            self.logger.error(f"Failed to get emails from folder {folder_id}: {str(e)}")
            raise DatabaseError(f"Failed to get emails from folder: {str(e)}")

    async def store_folder(self, folder: OutlookFolder) -> bool:
        """Store an Outlook folder."""
        try:
            async with self._pool.acquire() as conn:
                await conn.execute(f"""
                    INSERT INTO {self._folders_table} (
                        id, name, display_name, parent_folder_id, folder_path,
                        folder_type, total_item_count, unread_item_count,
                        child_folder_count, is_hidden
                    ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)
                    ON CONFLICT (id) DO UPDATE SET
                        name = EXCLUDED.name,
                        display_name = EXCLUDED.display_name,
                        total_item_count = EXCLUDED.total_item_count,
                        unread_item_count = EXCLUDED.unread_item_count,
                        child_folder_count = EXCLUDED.child_folder_count,
                        modified_date = NOW()
                """,
                    folder.id, folder.name, folder.display_name,
                    folder.parent_folder_id, folder.folder_path,
                    folder.folder_type, folder.total_item_count,
                    folder.unread_item_count, folder.child_folder_count,
                    folder.is_hidden
                )
                return True

        except Exception as e:
            self.logger.error(f"Failed to store folder {folder.id}: {str(e)}")
            raise DatabaseError(f"Failed to store folder: {str(e)}")

    async def get_folder(self, folder_id: str) -> Optional[OutlookFolder]:
        """Get a folder by ID."""
        try:
            async with self._pool.acquire() as conn:
                row = await conn.fetchrow(f"SELECT * FROM {self._folders_table} WHERE id = $1", folder_id)
                if not row:
                    return None

                return self._row_to_folder(row)

        except Exception as e:
            self.logger.error(f"Failed to get folder {folder_id}: {str(e)}")
            raise DatabaseError(f"Failed to get folder: {str(e)}")

    async def delete_email(self, email_id: str) -> bool:
        """Delete an email and its attachments."""
        try:
            async with self._pool.acquire() as conn:
                # Delete attachments first (cascade should handle this, but being explicit)
                await conn.execute(f"DELETE FROM {self._attachments_table} WHERE email_id = $1", email_id)

                # Delete email
                result = await conn.execute(f"DELETE FROM {self._emails_table} WHERE id = $1", email_id)

                # Check if any rows were affected
                return "DELETE 1" in result

        except Exception as e:
            self.logger.error(f"Failed to delete email {email_id}: {str(e)}")
            raise DatabaseError(f"Failed to delete email: {str(e)}")

    async def search_emails(self, query: str, limit: int = 100) -> List[EmailMessage]:
        """Search emails by subject or body content."""
        try:
            async with self._pool.acquire() as conn:
                rows = await conn.fetch(f"""
                    SELECT * FROM {self._emails_table}
                    WHERE subject ILIKE $1 OR body ILIKE $1
                    ORDER BY received_date DESC
                    LIMIT $2
                """, f"%{query}%", limit)

                emails = []
                for row in rows:
                    # Get attachments for this email
                    attachment_rows = await conn.fetch(
                        f"SELECT * FROM {self._attachments_table} WHERE email_id = $1", row['id']
                    )
                    emails.append(self._row_to_email(row, attachment_rows))

                return emails

        except Exception as e:
            self.logger.error(f"Failed to search emails: {str(e)}")
            raise DatabaseError(f"Failed to search emails: {str(e)}")

    def _row_to_email(self, row: dict, attachment_rows: List[dict]) -> EmailMessage:
        """Convert database row to EmailMessage object."""
        from evolvishub_outlook_ingestor.core.data_models import EmailAddress, EmailImportance, EmailSensitivity

        # Convert JSON fields back to objects
        to_recipients = [EmailAddress(**addr) for addr in json.loads(row['to_recipients'] or '[]')]
        cc_recipients = [EmailAddress(**addr) for addr in json.loads(row['cc_recipients'] or '[]')]
        bcc_recipients = [EmailAddress(**addr) for addr in json.loads(row['bcc_recipients'] or '[]')]
        reply_to = [EmailAddress(**addr) for addr in json.loads(row['reply_to'] or '[]')]

        # Convert attachments
        attachments = []
        for att_row in attachment_rows:
            attachments.append(self._row_to_attachment(att_row))

        return EmailMessage(
            id=row['id'],
            message_id=row['message_id'],
            conversation_id=row['conversation_id'],
            conversation_index=row['conversation_index'],
            subject=row['subject'],
            body=row['body'],
            body_preview=row['body_preview'],
            body_type=row['body_type'],
            is_html=row['is_html'],
            sender=EmailAddress(email=row['sender_email'], name=row['sender_name']) if row['sender_email'] else None,
            from_address=EmailAddress(email=row['from_email'], name=row['from_name']) if row['from_email'] else None,
            to_recipients=to_recipients,
            cc_recipients=cc_recipients,
            bcc_recipients=bcc_recipients,
            reply_to=reply_to,
            sent_date=row['sent_date'],
            received_date=row['received_date'],
            created_date=row['created_date'],
            modified_date=row['modified_date'],
            importance=EmailImportance(row['importance']),
            sensitivity=EmailSensitivity(row['sensitivity']),
            priority=row['priority'],
            is_read=row['is_read'],
            is_draft=row['is_draft'],
            has_attachments=row['has_attachments'],
            is_flagged=row['is_flagged'],
            folder_id=row['folder_id'],
            folder_path=row['folder_path'],
            attachments=attachments,
            headers=json.loads(row['headers'] or '{}'),
            internet_headers=json.loads(row['internet_headers'] or '{}'),
            categories=json.loads(row['categories'] or '[]'),
            in_reply_to=row['in_reply_to'],
            references=json.loads(row['references'] or '[]'),
            size=row['size'],
            extended_properties=json.loads(row['extended_properties'] or '{}')
        )

    def _row_to_attachment(self, row: dict) -> EmailAttachment:
        """Convert database row to EmailAttachment object."""
        from evolvishub_outlook_ingestor.core.data_models import AttachmentType

        return EmailAttachment(
            id=row['id'],
            name=row['name'],
            content_type=row['content_type'],
            size=row['size'],
            attachment_type=AttachmentType(row['attachment_type']),
            is_inline=row['is_inline'],
            content_id=row['content_id'],
            content_location=row['content_location'],
            content_bytes=row['content_bytes'],
            download_url=row['download_url'],
            created_date=row['created_date'],
            modified_date=row['modified_date']
        )

    def _row_to_folder(self, row: dict) -> OutlookFolder:
        """Convert database row to OutlookFolder object."""
        return OutlookFolder(
            id=row['id'],
            name=row['name'],
            display_name=row['display_name'],
            parent_folder_id=row['parent_folder_id'],
            folder_path=row['folder_path'],
            folder_type=row['folder_type'],
            total_item_count=row['total_item_count'],
            unread_item_count=row['unread_item_count'],
            child_folder_count=row['child_folder_count'],
            is_hidden=row['is_hidden'],
            created_date=row['created_date'],
            modified_date=row['modified_date']
        )

    async def _begin_transaction(self, isolation_level: Optional[str] = None):
        """Begin a database transaction."""
        conn = await self._pool.acquire()
        if isolation_level:
            await conn.execute(f"SET TRANSACTION ISOLATION LEVEL {isolation_level}")
        return await conn.transaction()

    async def _commit_transaction(self, transaction):
        """Commit a database transaction."""
        await transaction.commit()

    async def _rollback_transaction(self, transaction):
        """Rollback a database transaction."""
        await transaction.rollback()

    def _validate_config(self, required_keys: List[str]) -> None:
        """Validate that required configuration keys are present."""
        missing_keys = [key for key in required_keys if key not in self.config]
        if missing_keys:
            raise ValueError(f"Missing required configuration keys: {missing_keys}")

    async def health_check(self) -> Dict[str, Any]:
        """Perform a health check on the database connection."""
        try:
            async with self._pool.acquire() as conn:
                result = await conn.fetchval("SELECT 1")
                return {
                    "status": "healthy",
                    "database": self.config.database,
                    "host": self.config.host,
                    "port": self.config.port,
                    "pool_size": self._pool.get_size() if self._pool else 0,
                    "test_query_result": result
                }
        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e),
                "database": self.database,
                "host": self.host,
                "port": self.port
            }
