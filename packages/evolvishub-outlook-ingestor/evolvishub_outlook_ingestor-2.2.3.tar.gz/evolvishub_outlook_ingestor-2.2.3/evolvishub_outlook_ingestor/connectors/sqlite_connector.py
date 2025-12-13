"""
SQLite database connector for Evolvishub Outlook Email Ingestor.

This module provides a production-ready SQLite database connector
specifically designed for email ingestion operations using the new
DatabaseConnector interface.
"""

import asyncio
import sqlite3
from typing import Any, Dict, List, Optional, Union
from datetime import datetime
import json
import os

from evolvishub_outlook_ingestor.connectors.database_connector import (
    DatabaseConnector,
    DatabaseConfig,
)
from evolvishub_outlook_ingestor.core.data_models import (
    EmailMessage, EmailAttachment, OutlookFolder, ProcessingResult
)
from evolvishub_outlook_ingestor.core.exceptions import DatabaseError


class SQLiteConnector(DatabaseConnector):
    """
    Production-ready SQLite database connector for email ingestion.

    This connector provides enterprise-grade SQLite integration with:
    - Async aiosqlite driver for performance
    - Proper schema management with WAL mode
    - Batch processing with transactions
    - Comprehensive error handling
    - Index optimization
    """

    def __init__(self, config: Union[DatabaseConfig, Dict[str, Any]]):
        """
        Initialize SQLite connector.

        Args:
            config: Database configuration (DatabaseConfig or legacy dict format)
        """
        # Handle backward compatibility with old dict-based config
        if isinstance(config, dict):
            db_config = DatabaseConfig(
                database_type="sqlite",
                database=config.get('database'),
                table_name=config.get('table_name', 'emails'),
                batch_size=config.get('batch_size', 100),
                max_connections=1  # SQLite doesn't support multiple connections
            )
        else:
            db_config = config

        super().__init__(db_config)
        self._connection = None
        self._validate_sqlite_config()

    def _validate_sqlite_config(self):
        """Validate SQLite-specific configuration."""
        if not self.config.database:
            raise ValueError("SQLite database path is required")
    
    async def _connect(self):
        """Establish SQLite connection."""
        try:
            import aiosqlite

            # Ensure directory exists
            db_path = self.config.database
            if self.config.connection_string:
                db_path = self.config.connection_string

            os.makedirs(os.path.dirname(os.path.abspath(db_path)), exist_ok=True)

            # Create connection
            self._connection = await aiosqlite.connect(
                db_path,
                timeout=30.0,
                check_same_thread=False
            )

            # Enable WAL mode for better concurrency
            await self._connection.execute("PRAGMA journal_mode=WAL")

            # Enable foreign keys
            await self._connection.execute("PRAGMA foreign_keys=ON")

            # Set synchronous mode for better performance
            await self._connection.execute("PRAGMA synchronous=NORMAL")

            # Set cache size (in KB)
            await self._connection.execute("PRAGMA cache_size=10000")

            await self._connection.commit()

            self.logger.info(f"SQLite connection established: {db_path}")

        except ImportError:
            raise DatabaseError(
                "aiosqlite library not installed. "
                "Install with: pip install aiosqlite"
            )
        except Exception as e:
            raise DatabaseError(f"Failed to connect to SQLite: {e}")

    async def _disconnect(self):
        """Close SQLite connection."""
        if self._connection:
            await self._connection.close()
            self._connection = None
            self.logger.info("SQLite connection closed")
    
    async def _create_schema(self):
        """Create SQLite schema for email storage."""
        try:
            # Create emails table
            await self._connection.execute("""
            CREATE TABLE IF NOT EXISTS emails (
                id TEXT PRIMARY KEY,
                message_id TEXT,
                conversation_id TEXT,
                subject TEXT,
                body TEXT,
                body_preview TEXT,
                body_type TEXT DEFAULT 'text',
                is_html INTEGER DEFAULT 0,
                sender_email TEXT,
                sender_name TEXT,
                from_email TEXT,
                from_name TEXT,
                to_recipients TEXT DEFAULT '[]',
                cc_recipients TEXT DEFAULT '[]',
                bcc_recipients TEXT DEFAULT '[]',
                reply_to TEXT DEFAULT '[]',
                sent_date TEXT,
                received_date TEXT,
                created_date TEXT DEFAULT CURRENT_TIMESTAMP,
                modified_date TEXT DEFAULT CURRENT_TIMESTAMP,
                importance TEXT DEFAULT 'normal',
                sensitivity TEXT DEFAULT 'normal',
                priority TEXT,
                is_read INTEGER DEFAULT 0,
                is_draft INTEGER DEFAULT 0,
                has_attachments INTEGER DEFAULT 0,
                is_flagged INTEGER DEFAULT 0,
                folder_id TEXT,
                folder_path TEXT,
                headers TEXT DEFAULT '{}',
                internet_headers TEXT DEFAULT '{}',
                categories TEXT DEFAULT '[]',
                in_reply_to TEXT,
                references TEXT DEFAULT '[]',
                size INTEGER,
                extended_properties TEXT DEFAULT '{}'
            )
        """)

            # Create attachments table
            await self._connection.execute("""
            CREATE TABLE IF NOT EXISTS email_attachments (
                id TEXT PRIMARY KEY,
                email_id TEXT REFERENCES emails(id) ON DELETE CASCADE,
                name TEXT NOT NULL,
                content_type TEXT,
                size INTEGER,
                attachment_type TEXT DEFAULT 'file',
                is_inline INTEGER DEFAULT 0,
                content_id TEXT,
                content_location TEXT,
                content_bytes BLOB,
                download_url TEXT,
                created_date TEXT DEFAULT CURRENT_TIMESTAMP,
                modified_date TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)

            # Create folders table
            await self._connection.execute("""
            CREATE TABLE IF NOT EXISTS outlook_folders (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                display_name TEXT,
                parent_folder_id TEXT,
                folder_path TEXT,
                folder_type TEXT,
                total_item_count INTEGER DEFAULT 0,
                unread_item_count INTEGER DEFAULT 0,
                child_folder_count INTEGER DEFAULT 0,
                is_hidden INTEGER DEFAULT 0,
                created_date TEXT DEFAULT CURRENT_TIMESTAMP,
                modified_date TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)

            # Create indexes for better performance
            await self._connection.execute("CREATE INDEX IF NOT EXISTS idx_emails_message_id ON emails(message_id)")
            await self._connection.execute("CREATE INDEX IF NOT EXISTS idx_emails_conversation_id ON emails(conversation_id)")
            await self._connection.execute("CREATE INDEX IF NOT EXISTS idx_emails_sent_date ON emails(sent_date)")
            await self._connection.execute("CREATE INDEX IF NOT EXISTS idx_emails_received_date ON emails(received_date)")
            await self._connection.execute("CREATE INDEX IF NOT EXISTS idx_emails_folder_id ON emails(folder_id)")
            await self._connection.execute("CREATE INDEX IF NOT EXISTS idx_emails_sender_email ON emails(sender_email)")
            await self._connection.execute("CREATE INDEX IF NOT EXISTS idx_attachments_email_id ON email_attachments(email_id)")
            await self._connection.execute("CREATE INDEX IF NOT EXISTS idx_folders_parent_id ON outlook_folders(parent_folder_id)")

            await self._connection.commit()
            self.logger.info("SQLite schema created successfully")

        except Exception as e:
            await self._connection.rollback()
            raise DatabaseError(f"Failed to create SQLite schema: {e}")

    # Required abstract methods for DatabaseConnector interface

    async def _store_email_batch(self, emails: List[EmailMessage]) -> int:
        """Store a batch of emails in SQLite."""
        if not emails:
            return 0

        stored_count = 0

        try:
            # Start transaction
            await self._connection.execute("BEGIN TRANSACTION")

            for email in emails:
                try:
                    # Convert email to database format
                    email_data = self._email_to_db_format(email)

                    # Insert or replace email
                    await self._connection.execute("""
                        INSERT OR REPLACE INTO emails (
                            id, message_id, conversation_id, subject, body, is_html,
                            sender_email, sender_name, recipients, cc_recipients, bcc_recipients,
                            sent_date, received_date, created_date, last_modified_date,
                            is_read, is_draft, has_attachments, importance, categories, folder_id
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, email_data)

                    stored_count += 1

                except Exception as e:
                    self.logger.warning(f"Failed to store email {email.id}: {e}")
                    continue

            # Commit transaction
            await self._connection.commit()

        except Exception as e:
            await self._connection.rollback()
            self.logger.error(f"Failed to store email batch in SQLite: {e}")
            return 0

        return stored_count

    async def _store_single_email(self, email: EmailMessage) -> bool:
        """Store a single email in SQLite."""
        try:
            result = await self._store_email_batch([email])
            return result > 0
        except Exception as e:
            self.logger.error(f"Failed to store single email: {e}")
            return False

    async def _check_email_exists(self, email_id: str) -> bool:
        """Check if email exists in SQLite."""
        try:
            cursor = await self._connection.execute(
                "SELECT 1 FROM emails WHERE id = ? LIMIT 1",
                (email_id,)
            )
            result = await cursor.fetchone()
            await cursor.close()
            return result is not None
        except Exception as e:
            self.logger.error(f"Failed to check email existence in SQLite: {e}")
            return False

    async def _get_total_email_count(self) -> int:
        """Get total email count from SQLite."""
        try:
            cursor = await self._connection.execute("SELECT COUNT(*) FROM emails")
            result = await cursor.fetchone()
            await cursor.close()
            return result[0] if result else 0
        except Exception as e:
            self.logger.error(f"Failed to get email count from SQLite: {e}")
            return 0

    def _email_to_db_format(self, email: EmailMessage) -> tuple:
        """Convert EmailMessage to SQLite database format."""
        # Convert recipients to JSON strings
        recipients = json.dumps([
            {"address": r.address, "name": r.name}
            for r in email.recipients
        ]) if email.recipients else "[]"

        cc_recipients = json.dumps([
            {"address": r.address, "name": r.name}
            for r in email.cc_recipients
        ]) if email.cc_recipients else "[]"

        bcc_recipients = json.dumps([
            {"address": r.address, "name": r.name}
            for r in email.bcc_recipients
        ]) if email.bcc_recipients else "[]"

        # Convert dates to ISO format strings
        sent_date = email.sent_date.isoformat() if email.sent_date else None
        received_date = email.received_date.isoformat() if email.received_date else None
        created_date = getattr(email, 'created_date', None)
        created_date = created_date.isoformat() if created_date else None
        last_modified_date = getattr(email, 'last_modified_date', None)
        last_modified_date = last_modified_date.isoformat() if last_modified_date else None

        return (
            email.id,
            email.message_id,
            email.conversation_id,
            email.subject,
            email.body,
            1 if email.is_html else 0,
            email.sender.address if email.sender else None,
            email.sender.name if email.sender else None,
            recipients,
            cc_recipients,
            bcc_recipients,
            sent_date,
            received_date,
            created_date,
            last_modified_date,
            1 if email.is_read else 0,
            1 if email.is_draft else 0,
            1 if email.has_attachments else 0,
            getattr(email, 'importance', 'normal'),
            json.dumps(getattr(email, 'categories', [])),
            getattr(email, 'folder_id', None)
        )

    # Legacy methods for backward compatibility
    async def initialize(self) -> None:
        """Initialize the SQLite connector (legacy method)."""
        return await super().initialize()

    async def disconnect(self) -> None:
        """Disconnect from SQLite (legacy method)."""
        return await self.cleanup()

    async def store_email(self, email: EmailMessage) -> bool:
        """Store an email message in the database (legacy method)."""
        return await self._store_single_email(email)

    # Keep existing methods for backward compatibility but update to use new connection reference
    async def store_email_legacy(self, email: EmailMessage) -> bool:
        """Store an email message in the database (original implementation)."""
        try:
            # Convert email addresses to JSON
            to_recipients = json.dumps([{"email": addr.email, "name": addr.name} for addr in email.to_recipients]) if hasattr(email, 'to_recipients') and email.to_recipients else "[]"
            cc_recipients = json.dumps([{"email": addr.email, "name": addr.name} for addr in email.cc_recipients]) if hasattr(email, 'cc_recipients') and email.cc_recipients else "[]"
            bcc_recipients = json.dumps([{"email": addr.email, "name": addr.name} for addr in email.bcc_recipients]) if hasattr(email, 'bcc_recipients') and email.bcc_recipients else "[]"
            reply_to = json.dumps([{"email": addr.email, "name": addr.name} for addr in email.reply_to]) if hasattr(email, 'reply_to') and email.reply_to else "[]"
            
            # Convert datetime to string
            sent_date = email.sent_date.isoformat() if email.sent_date else None
            received_date = email.received_date.isoformat() if email.received_date else None
            
            # Insert or replace email
            await self._connection.execute("""
                INSERT OR REPLACE INTO emails (
                    id, message_id, conversation_id, subject, body, body_preview,
                    body_type, is_html, sender_email, sender_name, from_email, from_name,
                    to_recipients, cc_recipients, bcc_recipients, reply_to,
                    sent_date, received_date, importance, sensitivity, priority,
                    is_read, is_draft, has_attachments, is_flagged,
                    folder_id, folder_path, headers, internet_headers,
                    categories, in_reply_to, references, size, extended_properties,
                    modified_date
                ) VALUES (
                    ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                    ?, ?, ?, ?, ?, ?, ?, ?, ?,
                    ?, ?, ?, ?, ?, ?, ?, ?,
                    ?, ?, ?, ?, ?, CURRENT_TIMESTAMP
                )
            """, (
                email.id, email.message_id, email.conversation_id,
                email.subject, email.body, email.body_preview,
                email.body_type, int(email.is_html),
                email.sender.email if email.sender else None,
                email.sender.name if email.sender else None,
                email.from_address.email if email.from_address else None,
                email.from_address.name if email.from_address else None,
                to_recipients, cc_recipients, bcc_recipients, reply_to,
                sent_date, received_date,
                email.importance.value, email.sensitivity.value, email.priority,
                int(email.is_read), int(email.is_draft), int(email.has_attachments), int(email.is_flagged),
                email.folder_id, email.folder_path,
                json.dumps(email.headers), json.dumps(email.internet_headers),
                json.dumps(email.categories), email.in_reply_to,
                json.dumps(email.references), email.size,
                json.dumps(email.extended_properties)
            ))
            
            # Store attachments
            for attachment in email.attachments:
                await self.store_attachment(attachment, email.id)
            
            await self._connection.commit()
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to store email {email.id}: {str(e)}")
            raise DatabaseError(f"Failed to store email: {str(e)}")
    
    async def store_attachment(self, attachment: EmailAttachment, email_id: str) -> bool:
        """Store an email attachment."""
        try:
            created_date = attachment.created_date.isoformat() if attachment.created_date else None
            modified_date = attachment.modified_date.isoformat() if attachment.modified_date else None
            
            await self._connection.execute("""
                INSERT OR REPLACE INTO email_attachments (
                    id, email_id, name, content_type, size, attachment_type,
                    is_inline, content_id, content_location, content_bytes, download_url,
                    created_date, modified_date
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
            """, (
                attachment.id, email_id, attachment.name, attachment.content_type,
                attachment.size, attachment.attachment_type.value, int(attachment.is_inline),
                attachment.content_id, attachment.content_location,
                attachment.content_bytes, attachment.download_url, created_date
            ))
            
            await self._connection.commit()
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to store attachment {attachment.id}: {str(e)}")
            raise DatabaseError(f"Failed to store attachment: {str(e)}")
    
    async def get_email(self, email_id: str) -> Optional[EmailMessage]:
        """Retrieve an email by ID."""
        try:
            # Get email
            cursor = await self._connection.execute("SELECT * FROM emails WHERE id = ?", (email_id,))
            row = await cursor.fetchone()
            if not row:
                return None
            
            # Get attachments
            cursor = await self._connection.execute(
                "SELECT * FROM email_attachments WHERE email_id = ?", (email_id,)
            )
            attachment_rows = await cursor.fetchall()
            
            return self._row_to_email(row, attachment_rows)
            
        except Exception as e:
            self.logger.error(f"Failed to get email {email_id}: {str(e)}")
            raise DatabaseError(f"Failed to get email: {str(e)}")

    async def get_emails_by_folder(self, folder_id: str, limit: int = 100, offset: int = 0) -> List[EmailMessage]:
        """Get emails from a specific folder."""
        try:
            cursor = await self._connection.execute("""
                SELECT * FROM emails
                WHERE folder_id = ?
                ORDER BY received_date DESC
                LIMIT ? OFFSET ?
            """, (folder_id, limit, offset))

            rows = await cursor.fetchall()

            emails = []
            for row in rows:
                # Get attachments for this email
                cursor = await self._connection.execute(
                    "SELECT * FROM email_attachments WHERE email_id = ?", (row[0],)  # row[0] is id
                )
                attachment_rows = await cursor.fetchall()
                emails.append(self._row_to_email(row, attachment_rows))

            return emails

        except Exception as e:
            self.logger.error(f"Failed to get emails from folder {folder_id}: {str(e)}")
            raise DatabaseError(f"Failed to get emails from folder: {str(e)}")

    async def store_folder(self, folder: OutlookFolder) -> bool:
        """Store an Outlook folder."""
        try:
            created_date = folder.created_date.isoformat() if folder.created_date else None
            modified_date = folder.modified_date.isoformat() if folder.modified_date else None

            await self._connection.execute("""
                INSERT OR REPLACE INTO outlook_folders (
                    id, name, display_name, parent_folder_id, folder_path,
                    folder_type, total_item_count, unread_item_count,
                    child_folder_count, is_hidden, created_date, modified_date
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
            """, (
                folder.id, folder.name, folder.display_name,
                folder.parent_folder_id, folder.folder_path,
                folder.folder_type, folder.total_item_count,
                folder.unread_item_count, folder.child_folder_count,
                int(folder.is_hidden), created_date
            ))

            await self._connection.commit()
            return True

        except Exception as e:
            self.logger.error(f"Failed to store folder {folder.id}: {str(e)}")
            raise DatabaseError(f"Failed to store folder: {str(e)}")

    async def get_folder(self, folder_id: str) -> Optional[OutlookFolder]:
        """Get a folder by ID."""
        try:
            cursor = await self._connection.execute("SELECT * FROM outlook_folders WHERE id = ?", (folder_id,))
            row = await cursor.fetchone()
            if not row:
                return None

            return self._row_to_folder(row)

        except Exception as e:
            self.logger.error(f"Failed to get folder {folder_id}: {str(e)}")
            raise DatabaseError(f"Failed to get folder: {str(e)}")

    async def delete_email(self, email_id: str) -> bool:
        """Delete an email and its attachments."""
        try:
            # Delete attachments first
            await self._connection.execute("DELETE FROM email_attachments WHERE email_id = ?", (email_id,))

            # Delete email
            cursor = await self._connection.execute("DELETE FROM emails WHERE id = ?", (email_id,))

            await self._connection.commit()
            return cursor.rowcount > 0

        except Exception as e:
            self.logger.error(f"Failed to delete email {email_id}: {str(e)}")
            raise DatabaseError(f"Failed to delete email: {str(e)}")

    async def search_emails(self, query: str, limit: int = 100) -> List[EmailMessage]:
        """Search emails by subject or body content."""
        try:
            cursor = await self._connection.execute("""
                SELECT * FROM emails
                WHERE subject LIKE ? OR body LIKE ?
                ORDER BY received_date DESC
                LIMIT ?
            """, (f"%{query}%", f"%{query}%", limit))

            rows = await cursor.fetchall()

            emails = []
            for row in rows:
                # Get attachments for this email
                cursor = await self._connection.execute(
                    "SELECT * FROM email_attachments WHERE email_id = ?", (row[0],)  # row[0] is id
                )
                attachment_rows = await cursor.fetchall()
                emails.append(self._row_to_email(row, attachment_rows))

            return emails

        except Exception as e:
            self.logger.error(f"Failed to search emails: {str(e)}")
            raise DatabaseError(f"Failed to search emails: {str(e)}")

    def _row_to_email(self, row: tuple, attachment_rows: List[tuple]) -> EmailMessage:
        """Convert database row to EmailMessage object."""
        from evolvishub_outlook_ingestor.core.data_models import EmailAddress, EmailImportance, EmailSensitivity
        from datetime import datetime

        # Parse JSON fields
        to_recipients = [EmailAddress(**addr) for addr in json.loads(row[12] or '[]')]
        cc_recipients = [EmailAddress(**addr) for addr in json.loads(row[13] or '[]')]
        bcc_recipients = [EmailAddress(**addr) for addr in json.loads(row[14] or '[]')]
        reply_to = [EmailAddress(**addr) for addr in json.loads(row[15] or '[]')]

        # Parse datetime fields
        sent_date = datetime.fromisoformat(row[16]) if row[16] else None
        received_date = datetime.fromisoformat(row[17]) if row[17] else None
        created_date = datetime.fromisoformat(row[18]) if row[18] else None
        modified_date = datetime.fromisoformat(row[19]) if row[19] else None

        # Convert attachments
        attachments = []
        for att_row in attachment_rows:
            attachments.append(self._row_to_attachment(att_row))

        return EmailMessage(
            id=row[0],
            message_id=row[1],
            conversation_id=row[2],
            subject=row[3],
            body=row[4],
            body_preview=row[5],
            body_type=row[6],
            is_html=bool(row[7]),
            sender=EmailAddress(email=row[8], name=row[9]) if row[8] else None,
            from_address=EmailAddress(email=row[10], name=row[11]) if row[10] else None,
            to_recipients=to_recipients,
            cc_recipients=cc_recipients,
            bcc_recipients=bcc_recipients,
            reply_to=reply_to,
            sent_date=sent_date,
            received_date=received_date,
            created_date=created_date,
            modified_date=modified_date,
            importance=EmailImportance(row[20]),
            sensitivity=EmailSensitivity(row[21]),
            priority=row[22],
            is_read=bool(row[23]),
            is_draft=bool(row[24]),
            has_attachments=bool(row[25]),
            is_flagged=bool(row[26]),
            folder_id=row[27],
            folder_path=row[28],
            attachments=attachments,
            headers=json.loads(row[29] or '{}'),
            internet_headers=json.loads(row[30] or '{}'),
            categories=json.loads(row[31] or '[]'),
            in_reply_to=row[32],
            references=json.loads(row[33] or '[]'),
            size=row[34],
            extended_properties=json.loads(row[35] or '{}')
        )

    def _row_to_attachment(self, row: tuple) -> EmailAttachment:
        """Convert database row to EmailAttachment object."""
        from evolvishub_outlook_ingestor.core.data_models import AttachmentType
        from datetime import datetime

        created_date = datetime.fromisoformat(row[11]) if row[11] else None
        modified_date = datetime.fromisoformat(row[12]) if row[12] else None

        return EmailAttachment(
            id=row[0],
            name=row[2],
            content_type=row[3],
            size=row[4],
            attachment_type=AttachmentType(row[5]),
            is_inline=bool(row[6]),
            content_id=row[7],
            content_location=row[8],
            content_bytes=row[9],
            download_url=row[10],
            created_date=created_date,
            modified_date=modified_date
        )

    def _row_to_folder(self, row: tuple) -> OutlookFolder:
        """Convert database row to OutlookFolder object."""
        from datetime import datetime

        created_date = datetime.fromisoformat(row[10]) if row[10] else None
        modified_date = datetime.fromisoformat(row[11]) if row[11] else None

        return OutlookFolder(
            id=row[0],
            name=row[1],
            display_name=row[2],
            parent_folder_id=row[3],
            folder_path=row[4],
            folder_type=row[5],
            total_item_count=row[6],
            unread_item_count=row[7],
            child_folder_count=row[8],
            is_hidden=bool(row[9]),
            created_date=created_date,
            modified_date=modified_date
        )

    def _validate_config(self, required_keys: List[str]) -> None:
        """Validate that required configuration keys are present."""
        missing_keys = [key for key in required_keys if key not in self.config]
        if missing_keys:
            raise ValueError(f"Missing required configuration keys: {missing_keys}")

    async def health_check(self) -> Dict[str, Any]:
        """Perform a health check on the database connection."""
        try:
            cursor = await self._connection.execute("SELECT 1")
            result = await cursor.fetchone()

            # Get database file info
            file_size = os.path.getsize(self.database_path) if os.path.exists(self.database_path) else 0

            return {
                "status": "healthy",
                "database_path": self.database_path,
                "file_size_bytes": file_size,
                "test_query_result": result[0] if result else None
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e),
                "database_path": self.database_path
            }
