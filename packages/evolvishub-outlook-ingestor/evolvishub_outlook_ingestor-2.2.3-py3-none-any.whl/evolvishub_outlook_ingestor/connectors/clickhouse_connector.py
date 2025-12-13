"""
ClickHouse connector for Evolvishub Outlook Ingestor.

This module implements the ClickHouse connector using asyncio-compatible HTTP client
for high-performance columnar database analytics on email data.

Features:
- ClickHouse's columnar storage for fast analytical queries on email data
- Proper data type mapping for email fields to ClickHouse types
- Materialized views for pre-aggregated email analytics
- Compression and encoding optimizations for email content storage
- Distributed table creation for ClickHouse clusters
- Support for both self-hosted and ClickHouse Cloud deployments
"""

import asyncio
import json
import os
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Union
from uuid import UUID
from urllib.parse import urlencode

try:
    import aiohttp
    import clickhouse_connect
    from clickhouse_connect.driver import Client
    CLICKHOUSE_AVAILABLE = True
except ImportError:
    CLICKHOUSE_AVAILABLE = False
    aiohttp = None
    clickhouse_connect = None
    Client = None

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
        mask_sensitive_data,
        sanitize_input,
    )
    return get_credential_manager, mask_sensitive_data, sanitize_input


class ClickHouseConnector(BaseConnector):
    """ClickHouse connector using asyncio-compatible HTTP client."""
    
    def __init__(self, name: str, config: Dict[str, Any], **kwargs):
        """
        Initialize ClickHouse connector.
        
        Args:
            name: Connector name
            config: Configuration dictionary containing:
                - host: ClickHouse host
                - port: ClickHouse HTTP port (default: 8123)
                - database: Database name
                - username: Database username
                - password: Database password
                - secure: Use HTTPS (default: False)
                - cluster: ClickHouse cluster name for distributed tables
                - compression: Enable compression (default: True)
                - session_timeout: Session timeout in seconds
                - send_receive_timeout: Send/receive timeout in seconds
                - verify_ssl: Verify SSL certificates (default: True)
                - ca_cert: CA certificate file path
                - client_cert: Client certificate file path
                - client_key: Client key file path
                - settings: Additional ClickHouse settings
        """
        if not CLICKHOUSE_AVAILABLE:
            raise ImportError(
                "ClickHouse dependencies are required. "
                "Install with: pip install evolvishub-outlook-ingestor[database-clickhouse]"
            )
        
        # ClickHouse doesn't use traditional connection pooling in the same way
        super().__init__(name, config, enable_connection_pooling=False, **kwargs)

        # Get credential manager (lazy loading)
        get_credential_manager, _, _ = _get_security_utils()
        self._credential_manager = get_credential_manager()

        # ClickHouse configuration
        self.host = config.get("host", "localhost")
        self.port = config.get("port", 8123)
        self.database = config.get("database", "outlook_data")
        self.username = config.get("username", "default")
        self.secure = config.get("secure", False)
        self.cluster = config.get("cluster", None)
        self.compression = config.get("compression", True)
        self.session_timeout = config.get("session_timeout", 60)
        self.send_receive_timeout = config.get("send_receive_timeout", 300)
        self.verify_ssl = config.get("verify_ssl", True)
        self.ca_cert = config.get("ca_cert", None)
        self.client_cert = config.get("client_cert", None)
        self.client_key = config.get("client_key", None)
        self.settings = config.get("settings", {})

        # Secure password handling
        password_raw = config.get("password", "")
        password_env = config.get("password_env", "CLICKHOUSE_PASSWORD")

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
        
        # ClickHouse client and session
        self.client: Optional[Client] = None
        self.session: Optional[aiohttp.ClientSession] = None
        
        # Schema definitions
        self.schema_sql = self._get_schema_sql()
        
        # Base URL for HTTP requests
        protocol = "https" if self.secure else "http"
        self.base_url = f"{protocol}://{self.host}:{self.port}"
    
    async def _initialize_connection(self) -> None:
        """Initialize ClickHouse connection."""
        try:
            self.logger.info(
                "Initializing ClickHouse connection",
                host=self.host,
                database=self.database,
                connector=self.name
            )
            
            # Decrypt password for connection
            password = ""
            if self._encrypted_password:
                password = self._credential_manager.decrypt_credential(self._encrypted_password)
            
            # Create ClickHouse client
            loop = asyncio.get_event_loop()
            self.client = await loop.run_in_executor(
                None,
                lambda: clickhouse_connect.get_client(
                    host=self.host,
                    port=self.port,
                    database=self.database,
                    username=self.username,
                    password=password,
                    secure=self.secure,
                    verify=self.verify_ssl,
                    ca_cert=self.ca_cert,
                    client_cert=self.client_cert,
                    client_key=self.client_key,
                    compress=self.compression,
                    session_timeout=self.session_timeout,
                    send_receive_timeout=self.send_receive_timeout,
                    settings=self.settings
                )
            )
            
            # Create aiohttp session for async operations
            connector = aiohttp.TCPConnector(
                verify_ssl=self.verify_ssl,
                ssl_context=self._create_ssl_context() if self.secure else None
            )
            
            self.session = aiohttp.ClientSession(
                connector=connector,
                timeout=aiohttp.ClientTimeout(total=self.send_receive_timeout)
            )
            
            self.logger.info(
                "ClickHouse connection established",
                host=self.host,
                database=self.database,
                connector=self.name
            )
            
        except Exception as e:
            raise ConnectionError(
                f"Failed to connect to ClickHouse: {e}",
                database_type="clickhouse",
                cause=e
            )
    
    async def _initialize_pool(self) -> None:
        """ClickHouse doesn't use connection pooling - delegate to single connection."""
        await self._initialize_connection()
    
    async def _cleanup_connection(self) -> None:
        """Cleanup ClickHouse connection."""
        if self.session:
            try:
                await self.session.close()
                self.logger.info("ClickHouse session closed", connector=self.name)
            except Exception as e:
                self.logger.warning(
                    "Error closing ClickHouse session",
                    connector=self.name,
                    error=str(e)
                )
            finally:
                self.session = None
        
        if self.client:
            try:
                loop = asyncio.get_event_loop()
                await loop.run_in_executor(None, self.client.close)
                self.logger.info("ClickHouse client closed", connector=self.name)
            except Exception as e:
                self.logger.warning(
                    "Error closing ClickHouse client",
                    connector=self.name,
                    error=str(e)
                )
            finally:
                self.client = None
    
    async def _cleanup_pool(self) -> None:
        """ClickHouse doesn't use connection pooling - delegate to single connection."""
        await self._cleanup_connection()
    
    async def _test_connection(self) -> None:
        """Test ClickHouse connection."""
        if not self.client:
            raise ConnectionError("No ClickHouse client available")
        
        try:
            # Test with a simple query
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(
                None,
                lambda: self.client.query("SELECT 1").result_rows
            )
            
            if not result or result[0][0] != 1:
                raise ConnectionError("ClickHouse connection test failed")
                
            self.logger.debug("ClickHouse connection test passed", connector=self.name)
            
        except Exception as e:
            raise ConnectionError(f"ClickHouse connection test failed: {e}")
    
    def _create_ssl_context(self):
        """Create SSL context for secure connections."""
        import ssl
        
        context = ssl.create_default_context()
        
        if self.ca_cert:
            context.load_verify_locations(self.ca_cert)
        
        if self.client_cert and self.client_key:
            context.load_cert_chain(self.client_cert, self.client_key)
        
        if not self.verify_ssl:
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
        
        return context
    
    async def _initialize_schema(self) -> None:
        """Initialize ClickHouse database schema."""
        try:
            self.logger.info("Initializing ClickHouse schema", connector=self.name)
            
            loop = asyncio.get_event_loop()
            
            # Create database if it doesn't exist
            await loop.run_in_executor(
                None,
                lambda: self.client.command(f"CREATE DATABASE IF NOT EXISTS {self.database}")
            )
            
            # Execute schema creation statements
            for statement in self.schema_sql:
                try:
                    await loop.run_in_executor(None, lambda s=statement: self.client.command(s))
                except Exception as e:
                    self.logger.warning(
                        "Schema statement failed (may already exist)",
                        statement=statement[:100] + "..." if len(statement) > 100 else statement,
                        error=str(e),
                        connector=self.name
                    )
            
            self.logger.info("ClickHouse schema initialized", connector=self.name)
            
        except Exception as e:
            raise DatabaseError(
                f"Failed to initialize ClickHouse schema: {e}",
                database_type="clickhouse",
                operation="initialize_schema",
                cause=e
            )
    
    def _get_schema_sql(self) -> List[str]:
        """Get ClickHouse schema SQL statements."""
        # Determine table engine based on cluster configuration
        table_engine = "ReplicatedMergeTree" if self.cluster else "MergeTree"
        
        statements = [
            # Main emails table
            f"""
            CREATE TABLE IF NOT EXISTS {self.database}.emails (
                id String,
                message_id Nullable(String),
                subject Nullable(String),
                body Nullable(String),
                body_preview Nullable(String),
                sender_email Nullable(String),
                sender_name Nullable(String),
                received_date Nullable(DateTime64(3)),
                sent_date Nullable(DateTime64(3)),
                importance Nullable(String),
                is_read UInt8 DEFAULT 0,
                has_attachments UInt8 DEFAULT 0,
                folder_id Nullable(String),
                folder_name Nullable(String),
                categories Array(String),
                headers Map(String, String),
                metadata Map(String, String),
                sender_domain Nullable(String),
                created_at DateTime64(3) DEFAULT now64(),
                updated_at DateTime64(3) DEFAULT now64(),
                version UInt64 DEFAULT 1
            ) ENGINE = {table_engine}()
            PARTITION BY toYYYYMM(received_date)
            ORDER BY (sender_domain, received_date, id)
            SETTINGS index_granularity = 8192
            """,
            
            # Recipients table
            f"""
            CREATE TABLE IF NOT EXISTS {self.database}.email_recipients (
                email_id String,
                recipient_type Enum8('to' = 1, 'cc' = 2, 'bcc' = 3),
                email_address String,
                display_name Nullable(String)
            ) ENGINE = {table_engine}()
            ORDER BY (email_id, recipient_type, email_address)
            SETTINGS index_granularity = 8192
            """,
            
            # Attachments table
            f"""
            CREATE TABLE IF NOT EXISTS {self.database}.email_attachments (
                id String,
                email_id String,
                name String,
                content_type Nullable(String),
                size Nullable(UInt64),
                content_hash Nullable(String),
                is_inline UInt8 DEFAULT 0,
                attachment_type Nullable(String),
                storage_location Nullable(String),
                storage_backend Nullable(String),
                extended_properties Map(String, String),
                created_at DateTime64(3) DEFAULT now64()
            ) ENGINE = {table_engine}()
            ORDER BY (email_id, id)
            SETTINGS index_granularity = 8192
            """
        ]
        
        # Add distributed tables if cluster is configured
        if self.cluster:
            statements.extend([
                f"""
                CREATE TABLE IF NOT EXISTS {self.database}.emails_distributed AS {self.database}.emails
                ENGINE = Distributed({self.cluster}, {self.database}, emails, rand())
                """,
                
                f"""
                CREATE TABLE IF NOT EXISTS {self.database}.email_recipients_distributed AS {self.database}.email_recipients
                ENGINE = Distributed({self.cluster}, {self.database}, email_recipients, rand())
                """,
                
                f"""
                CREATE TABLE IF NOT EXISTS {self.database}.email_attachments_distributed AS {self.database}.email_attachments
                ENGINE = Distributed({self.cluster}, {self.database}, email_attachments, rand())
                """
            ])
        
        return statements

    async def _store_email_impl(
        self,
        email: EmailMessage,
        transaction: Optional[Any] = None,
        **kwargs
    ) -> str:
        """Store email in ClickHouse."""
        try:
            # Prepare email data for ClickHouse
            email_data = self._prepare_email_data(email)

            # Get table name (distributed if cluster is configured)
            table_name = f"{self.database}.emails_distributed" if self.cluster else f"{self.database}.emails"

            loop = asyncio.get_event_loop()

            # Insert email data
            await loop.run_in_executor(
                None,
                lambda: self.client.insert(table_name, [email_data])
            )

            # Insert recipients
            if email.recipients:
                await self._store_recipients(email.id, email.recipients)

            # Insert attachments
            if email.attachments:
                await self._store_attachments(email.id, email.attachments)

            return email.id

        except Exception as e:
            raise DatabaseError(
                f"Failed to store email in ClickHouse: {e}",
                database_type="clickhouse",
                operation="store_email",
                cause=e
            )

    async def _store_emails_batch_impl(
        self,
        emails: List[EmailMessage],
        transaction: Optional[Any] = None,
        **kwargs
    ) -> List[str]:
        """Store multiple emails in ClickHouse."""
        try:
            # Prepare batch data
            email_data_batch = [self._prepare_email_data(email) for email in emails]
            recipients_batch = []
            attachments_batch = []

            # Collect recipients and attachments
            for email in emails:
                if email.recipients:
                    for recipient_type, recipients in email.recipients.items():
                        for recipient in recipients:
                            recipients_batch.append({
                                "email_id": email.id,
                                "recipient_type": recipient_type,
                                "email_address": recipient.email,
                                "display_name": recipient.name
                            })

                if email.attachments:
                    for attachment in email.attachments:
                        attachments_batch.append(self._prepare_attachment_data(email.id, attachment))

            # Get table names
            emails_table = f"{self.database}.emails_distributed" if self.cluster else f"{self.database}.emails"
            recipients_table = f"{self.database}.email_recipients_distributed" if self.cluster else f"{self.database}.email_recipients"
            attachments_table = f"{self.database}.email_attachments_distributed" if self.cluster else f"{self.database}.email_attachments"

            loop = asyncio.get_event_loop()

            # Batch insert emails
            await loop.run_in_executor(
                None,
                lambda: self.client.insert(emails_table, email_data_batch)
            )

            # Batch insert recipients
            if recipients_batch:
                await loop.run_in_executor(
                    None,
                    lambda: self.client.insert(recipients_table, recipients_batch)
                )

            # Batch insert attachments
            if attachments_batch:
                await loop.run_in_executor(
                    None,
                    lambda: self.client.insert(attachments_table, attachments_batch)
                )

            return [email.id for email in emails]

        except Exception as e:
            raise DatabaseError(
                f"Failed to store emails batch in ClickHouse: {e}",
                database_type="clickhouse",
                operation="store_emails_batch",
                cause=e
            )

    async def _get_email_impl(
        self,
        email_id: str,
        include_attachments: bool = True,
        **kwargs
    ) -> Optional[EmailMessage]:
        """Retrieve email from ClickHouse."""
        try:
            # Get table name
            table_name = f"{self.database}.emails_distributed" if self.cluster else f"{self.database}.emails"

            loop = asyncio.get_event_loop()

            # Query for specific email
            result = await loop.run_in_executor(
                None,
                lambda: self.client.query(
                    f"SELECT * FROM {table_name} WHERE id = %(email_id)s LIMIT 1",
                    parameters={"email_id": email_id}
                )
            )

            if not result.result_rows:
                return None

            # Convert row to EmailMessage
            email = self._row_to_email(result.result_rows[0], result.column_names)

            # Get recipients
            email.recipients = await self._get_recipients(email_id)

            # Get attachments if requested
            if include_attachments:
                email.attachments = await self._get_attachments(email_id)

            return email

        except Exception as e:
            raise DatabaseError(
                f"Failed to retrieve email from ClickHouse: {e}",
                database_type="clickhouse",
                operation="get_email",
                cause=e
            )

    async def _search_emails_impl(
        self,
        filters: Dict[str, Any],
        limit: Optional[int] = None,
        offset: int = 0,
        sort_by: Optional[str] = None,
        sort_order: str = "desc",
        **kwargs
    ) -> List[EmailMessage]:
        """Search emails in ClickHouse."""
        try:
            # Build query
            table_name = f"{self.database}.emails_distributed" if self.cluster else f"{self.database}.emails"
            query_parts = [f"SELECT * FROM {table_name} WHERE 1=1"]
            parameters = {}

            # Add filters
            if "sender_email" in filters:
                query_parts.append("AND sender_email = %(sender_email)s")
                parameters["sender_email"] = filters["sender_email"]

            if "subject_contains" in filters:
                query_parts.append("AND positionCaseInsensitive(subject, %(subject_text)s) > 0")
                parameters["subject_text"] = filters["subject_contains"]

            if "date_from" in filters:
                query_parts.append("AND received_date >= %(date_from)s")
                parameters["date_from"] = filters["date_from"]

            if "date_to" in filters:
                query_parts.append("AND received_date <= %(date_to)s")
                parameters["date_to"] = filters["date_to"]

            if "folder_id" in filters:
                query_parts.append("AND folder_id = %(folder_id)s")
                parameters["folder_id"] = filters["folder_id"]

            if "has_attachments" in filters:
                query_parts.append("AND has_attachments = %(has_attachments)s")
                parameters["has_attachments"] = 1 if filters["has_attachments"] else 0

            if "sender_domain" in filters:
                query_parts.append("AND sender_domain = %(sender_domain)s")
                parameters["sender_domain"] = filters["sender_domain"]

            # Full-text search
            if "search_text" in filters:
                query_parts.append(
                    "AND (positionCaseInsensitive(subject, %(search_text)s) > 0 OR "
                    "positionCaseInsensitive(body, %(search_text)s) > 0)"
                )
                parameters["search_text"] = filters["search_text"]

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

            loop = asyncio.get_event_loop()

            # Execute query
            result = await loop.run_in_executor(
                None,
                lambda: self.client.query(query, parameters=parameters)
            )

            emails = []
            for row in result.result_rows:
                email = self._row_to_email(row, result.column_names)
                # Get recipients and attachments for each email
                email.recipients = await self._get_recipients(email.id)
                email.attachments = await self._get_attachments(email.id)
                emails.append(email)

            return emails

        except Exception as e:
            raise DatabaseError(
                f"Failed to search emails in ClickHouse: {e}",
                database_type="clickhouse",
                operation="search_emails",
                cause=e
            )

    def _prepare_email_data(self, email: EmailMessage) -> Dict[str, Any]:
        """Prepare email data for ClickHouse insertion."""
        # Extract sender domain for partitioning
        sender_domain = ""
        if email.sender and email.sender.email:
            sender_domain = email.sender.email.split("@")[-1] if "@" in email.sender.email else "unknown"

        return {
            "id": email.id,
            "message_id": email.message_id,
            "subject": email.subject,
            "body": email.body,
            "body_preview": email.body_preview,
            "sender_email": email.sender.email if email.sender else None,
            "sender_name": email.sender.name if email.sender else None,
            "received_date": email.received_date,
            "sent_date": email.sent_date,
            "importance": email.importance,
            "is_read": 1 if email.is_read else 0,
            "has_attachments": 1 if email.attachments else 0,
            "folder_id": email.folder.id if email.folder else None,
            "folder_name": email.folder.name if email.folder else None,
            "categories": email.categories or [],
            "headers": email.headers or {},
            "metadata": email.metadata or {},
            "sender_domain": sender_domain,
            "created_at": datetime.now(timezone.utc),
            "updated_at": datetime.now(timezone.utc),
            "version": 1
        }

    def _prepare_attachment_data(self, email_id: str, attachment: EmailAttachment) -> Dict[str, Any]:
        """Prepare attachment data for ClickHouse insertion."""
        return {
            "id": attachment.id,
            "email_id": email_id,
            "name": attachment.name,
            "content_type": attachment.content_type,
            "size": attachment.size,
            "content_hash": attachment.content_hash,
            "is_inline": 1 if attachment.is_inline else 0,
            "attachment_type": attachment.attachment_type,
            "storage_location": attachment.extended_properties.get("storage_location") if attachment.extended_properties else None,
            "storage_backend": attachment.extended_properties.get("storage_backend") if attachment.extended_properties else None,
            "extended_properties": attachment.extended_properties or {},
            "created_at": datetime.now(timezone.utc)
        }

    def _row_to_email(self, row: tuple, column_names: List[str]) -> EmailMessage:
        """Convert ClickHouse row to EmailMessage."""
        from evolvishub_outlook_ingestor.core.data_models import EmailAddress, OutlookFolder

        # Create dictionary from row and column names
        data = dict(zip(column_names, row))

        # Create sender
        sender = None
        if data.get("sender_email"):
            sender = EmailAddress(email=data["sender_email"], name=data.get("sender_name"))

        # Create folder
        folder = None
        if data.get("folder_id"):
            folder = OutlookFolder(id=data["folder_id"], name=data.get("folder_name"))

        return EmailMessage(
            id=data["id"],
            message_id=data.get("message_id"),
            subject=data.get("subject"),
            body=data.get("body"),
            body_preview=data.get("body_preview"),
            sender=sender,
            received_date=data.get("received_date"),
            sent_date=data.get("sent_date"),
            importance=data.get("importance"),
            is_read=bool(data.get("is_read", 0)),
            folder=folder,
            categories=data.get("categories", []),
            headers=data.get("headers", {}),
            metadata=data.get("metadata", {})
        )

    async def _store_recipients(self, email_id: str, recipients: Dict[str, List]) -> None:
        """Store email recipients."""
        recipients_data = []
        for recipient_type, recipient_list in recipients.items():
            for recipient in recipient_list:
                recipients_data.append({
                    "email_id": email_id,
                    "recipient_type": recipient_type,
                    "email_address": recipient.email,
                    "display_name": recipient.name
                })

        if recipients_data:
            table_name = f"{self.database}.email_recipients_distributed" if self.cluster else f"{self.database}.email_recipients"
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(
                None,
                lambda: self.client.insert(table_name, recipients_data)
            )

    async def _store_attachments(self, email_id: str, attachments: List[EmailAttachment]) -> None:
        """Store email attachments."""
        attachments_data = [self._prepare_attachment_data(email_id, attachment) for attachment in attachments]

        if attachments_data:
            table_name = f"{self.database}.email_attachments_distributed" if self.cluster else f"{self.database}.email_attachments"
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(
                None,
                lambda: self.client.insert(table_name, attachments_data)
            )

    async def _get_recipients(self, email_id: str) -> Dict[str, List]:
        """Get email recipients."""
        from evolvishub_outlook_ingestor.core.data_models import EmailAddress

        recipients = {"to": [], "cc": [], "bcc": []}

        table_name = f"{self.database}.email_recipients_distributed" if self.cluster else f"{self.database}.email_recipients"

        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(
            None,
            lambda: self.client.query(
                f"SELECT recipient_type, email_address, display_name FROM {table_name} WHERE email_id = %(email_id)s",
                parameters={"email_id": email_id}
            )
        )

        for row in result.result_rows:
            recipient_type, email_address, display_name = row
            recipient = EmailAddress(email=email_address, name=display_name)
            if recipient_type in recipients:
                recipients[recipient_type].append(recipient)

        return recipients

    async def _get_attachments(self, email_id: str) -> List[EmailAttachment]:
        """Get email attachments."""
        attachments = []

        table_name = f"{self.database}.email_attachments_distributed" if self.cluster else f"{self.database}.email_attachments"

        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(
            None,
            lambda: self.client.query(
                f"SELECT * FROM {table_name} WHERE email_id = %(email_id)s",
                parameters={"email_id": email_id}
            )
        )

        for row in result.result_rows:
            data = dict(zip(result.column_names, row))

            # Reconstruct extended_properties
            extended_properties = data.get("extended_properties", {})
            if data.get("storage_location"):
                extended_properties["storage_location"] = data["storage_location"]
            if data.get("storage_backend"):
                extended_properties["storage_backend"] = data["storage_backend"]

            attachment = EmailAttachment(
                id=data["id"],
                name=data["name"],
                content_type=data["content_type"],
                size=data["size"],
                content_hash=data["content_hash"],
                is_inline=bool(data.get("is_inline", 0)),
                attachment_type=data["attachment_type"],
                extended_properties=extended_properties
            )
            attachments.append(attachment)

        return attachments

    async def _begin_transaction(self, isolation_level: Optional[str] = None) -> Any:
        """Begin ClickHouse transaction (ClickHouse has limited transaction support)."""
        # ClickHouse has limited transaction support, mainly for individual operations
        return {"transaction_id": f"clickhouse_tx_{datetime.now().timestamp()}"}

    async def _commit_transaction(self, transaction: Any) -> None:
        """Commit ClickHouse transaction (automatic with ClickHouse)."""
        # ClickHouse commits automatically on write operations
        pass

    async def _rollback_transaction(self, transaction: Any) -> None:
        """Rollback ClickHouse transaction (limited support)."""
        # ClickHouse has limited rollback support
        raise TransactionError("ClickHouse has limited transaction rollback support")

    # Analytics and Materialized Views

    async def create_analytics_views(self) -> None:
        """Create materialized views for email analytics."""
        try:
            loop = asyncio.get_event_loop()

            # Email volume by day
            await loop.run_in_executor(
                None,
                lambda: self.client.command(f"""
                CREATE MATERIALIZED VIEW IF NOT EXISTS {self.database}.email_volume_daily
                ENGINE = SummingMergeTree()
                ORDER BY (date, sender_domain)
                AS SELECT
                    toDate(received_date) as date,
                    sender_domain,
                    count() as email_count,
                    sum(has_attachments) as emails_with_attachments
                FROM {self.database}.emails
                GROUP BY date, sender_domain
                """)
            )

            # Top senders by volume
            await loop.run_in_executor(
                None,
                lambda: self.client.command(f"""
                CREATE MATERIALIZED VIEW IF NOT EXISTS {self.database}.top_senders
                ENGINE = AggregatingMergeTree()
                ORDER BY sender_email
                AS SELECT
                    sender_email,
                    sender_domain,
                    count() as email_count,
                    uniq(folder_id) as unique_folders,
                    avg(length(body)) as avg_body_length
                FROM {self.database}.emails
                WHERE sender_email IS NOT NULL
                GROUP BY sender_email, sender_domain
                """)
            )

            self.logger.info(
                "ClickHouse analytics views created",
                connector=self.name
            )

        except Exception as e:
            self.logger.warning(
                "Failed to create analytics views",
                error=str(e),
                connector=self.name
            )

    async def get_email_analytics(self, date_from: datetime, date_to: datetime) -> Dict[str, Any]:
        """Get email analytics for date range."""
        try:
            loop = asyncio.get_event_loop()

            # Get email volume by day
            volume_result = await loop.run_in_executor(
                None,
                lambda: self.client.query(f"""
                SELECT
                    date,
                    sum(email_count) as total_emails,
                    sum(emails_with_attachments) as emails_with_attachments
                FROM {self.database}.email_volume_daily
                WHERE date >= %(date_from)s AND date <= %(date_to)s
                GROUP BY date
                ORDER BY date
                """, parameters={"date_from": date_from.date(), "date_to": date_to.date()})
            )

            # Get top senders
            senders_result = await loop.run_in_executor(
                None,
                lambda: self.client.query(f"""
                SELECT
                    sender_email,
                    sender_domain,
                    sum(email_count) as total_emails
                FROM {self.database}.top_senders
                GROUP BY sender_email, sender_domain
                ORDER BY total_emails DESC
                LIMIT 10
                """)
            )

            return {
                "volume_by_day": [
                    {"date": row[0], "total_emails": row[1], "emails_with_attachments": row[2]}
                    for row in volume_result.result_rows
                ],
                "top_senders": [
                    {"sender_email": row[0], "sender_domain": row[1], "total_emails": row[2]}
                    for row in senders_result.result_rows
                ]
            }

        except Exception as e:
            raise DatabaseError(
                f"Failed to get email analytics: {e}",
                database_type="clickhouse",
                operation="get_analytics",
                cause=e
            )


# DatabaseConnector interface implementation for ClickHouse
from evolvishub_outlook_ingestor.connectors.database_connector import (
    DatabaseConnector,
    DatabaseConfig,
)


class ClickHouseDatabaseConnector(DatabaseConnector):
    """
    Production-ready ClickHouse database connector for email ingestion.

    This connector provides enterprise-grade ClickHouse integration with:
    - Columnar storage optimizations for analytics
    - Proper schema management
    - Batch processing for efficiency
    - Comprehensive error handling
    - ClickHouse-specific optimizations for email data
    """

    def __init__(self, config: Union[DatabaseConfig, Dict[str, Any]]):
        """
        Initialize ClickHouse connector.

        Args:
            config: Database configuration (DatabaseConfig or legacy dict format)
        """
        # Handle backward compatibility with old dict-based config
        if isinstance(config, dict):
            db_config = DatabaseConfig(
                database_type="clickhouse",
                host=config.get('host'),
                port=config.get('port', 8123),
                database=config.get('database'),
                username=config.get('username'),
                password=config.get('password'),
                table_name=config.get('table_name', 'emails'),
                batch_size=config.get('batch_size', 1000),  # Larger batches for ClickHouse
                max_connections=config.get('max_pool_size', 10),
                secure=config.get('secure', False),
                cluster=config.get('cluster'),
                compression=config.get('compression', True),
                session_timeout=config.get('session_timeout', 60),
                send_receive_timeout=config.get('send_receive_timeout', 300),
                verify_ssl=config.get('verify_ssl', True),
                ca_cert=config.get('ca_cert'),
                client_cert=config.get('client_cert'),
                client_key=config.get('client_key'),
                settings=config.get('settings')
            )
        else:
            db_config = config

        super().__init__(db_config)
        self.client = None
        self._validate_clickhouse_config()

    def _validate_clickhouse_config(self):
        """Validate ClickHouse-specific configuration."""
        if not self.config.host:
            raise ValueError("ClickHouse host is required")
        if not self.config.database:
            raise ValueError("ClickHouse database name is required")
        if not self.config.username:
            raise ValueError("ClickHouse username is required")

    async def _connect(self):
        """Establish ClickHouse connection."""
        try:
            if not CLICKHOUSE_AVAILABLE:
                raise ImportError("ClickHouse dependencies not available")

            import clickhouse_connect

            # Create ClickHouse client in thread pool since it's synchronous
            loop = asyncio.get_event_loop()
            self.client = await loop.run_in_executor(
                None,
                lambda: clickhouse_connect.get_client(
                    host=self.config.host,
                    port=self.config.port or 8123,
                    database=self.config.database,
                    username=self.config.username,
                    password=self.config.password or '',
                    secure=self.config.secure,
                    verify=self.config.verify_ssl,
                    ca_cert=self.config.ca_cert,
                    client_cert=self.config.client_cert,
                    client_key=self.config.client_key,
                    compress=self.config.compression,
                    session_timeout=self.config.session_timeout,
                    send_receive_timeout=self.config.send_receive_timeout,
                    settings=self.config.settings or {}
                )
            )

            self._connection = self.client
            self.logger.info("ClickHouse connection established")

        except Exception as e:
            self.logger.error(f"Failed to connect to ClickHouse: {e}")
            raise DatabaseError(f"Failed to connect to ClickHouse: {e}") from e

    async def _disconnect(self):
        """Close ClickHouse connection."""
        try:
            if self.client:
                # ClickHouse client doesn't need explicit closing
                self.client = None
                self._connection = None
            self.logger.info("ClickHouse connection closed")

        except Exception as e:
            self.logger.error(f"Failed to disconnect from ClickHouse: {e}")
            raise DatabaseError(f"Failed to disconnect from ClickHouse: {e}") from e

    async def _create_schema(self):
        """Create ClickHouse schema/tables if they don't exist."""
        try:
            loop = asyncio.get_event_loop()

            # Create emails table with ClickHouse optimizations
            create_table_sql = f"""
                CREATE TABLE IF NOT EXISTS {self.config.table_name} (
                    id UInt64,
                    message_id String,
                    subject String,
                    sender_email String,
                    sender_name String,
                    received_datetime DateTime64(6),
                    sent_datetime DateTime64(6),
                    body_text String,
                    body_html String,
                    importance LowCardinality(String),
                    sensitivity LowCardinality(String),
                    has_attachments UInt8,
                    attachment_count UInt32,
                    folder_path String,
                    categories Array(String),
                    headers String,
                    metadata String,
                    created_at DateTime64(6) DEFAULT now64(),
                    updated_at DateTime64(6) DEFAULT now64()
                ) ENGINE = MergeTree()
                ORDER BY (received_datetime, message_id)
                PARTITION BY toYYYYMM(received_datetime)
                SETTINGS index_granularity = 8192
            """

            await loop.run_in_executor(None, self.client.command, create_table_sql)

            # Create indexes for performance
            await loop.run_in_executor(
                None,
                self.client.command,
                f"ALTER TABLE {self.config.table_name} ADD INDEX IF NOT EXISTS idx_message_id message_id TYPE bloom_filter GRANULARITY 1"
            )

            await loop.run_in_executor(
                None,
                self.client.command,
                f"ALTER TABLE {self.config.table_name} ADD INDEX IF NOT EXISTS idx_sender_email sender_email TYPE bloom_filter GRANULARITY 1"
            )

            self.logger.info("ClickHouse schema created successfully")

        except Exception as e:
            self.logger.error(f"Failed to create ClickHouse schema: {e}")
            raise DatabaseError(f"Failed to create ClickHouse schema: {e}") from e

    async def _store_email_batch(self, emails: List[EmailMessage]) -> int:
        """Store a batch of emails in ClickHouse."""
        if not emails:
            return 0

        try:
            loop = asyncio.get_event_loop()

            # Prepare data for batch insert
            data = []
            for i, email in enumerate(emails):
                data.append([
                    i + 1,  # Simple ID for now
                    email.message_id,
                    email.subject or '',
                    email.sender.email if email.sender else '',
                    email.sender.name if email.sender else '',
                    email.received_datetime,
                    email.sent_datetime,
                    email.body_text or '',
                    email.body_html or '',
                    email.importance or 'normal',
                    email.sensitivity or 'normal',
                    1 if email.attachments else 0,
                    len(email.attachments) if email.attachments else 0,
                    email.folder_path or '',
                    email.categories or [],
                    json.dumps(email.headers) if email.headers else '{}',
                    json.dumps(email.metadata) if email.metadata else '{}'
                ])

            # Insert data in thread pool
            await loop.run_in_executor(
                None,
                lambda: self.client.insert(
                    self.config.table_name,
                    data,
                    column_names=[
                        'id', 'message_id', 'subject', 'sender_email', 'sender_name',
                        'received_datetime', 'sent_datetime', 'body_text', 'body_html',
                        'importance', 'sensitivity', 'has_attachments', 'attachment_count',
                        'folder_path', 'categories', 'headers', 'metadata'
                    ]
                )
            )

            stored_count = len(emails)
            self.logger.info(f"Stored {stored_count} emails in ClickHouse batch")
            return stored_count

        except Exception as e:
            self.logger.error(f"Failed to store email batch in ClickHouse: {e}")
            raise DatabaseError(f"Failed to store email batch in ClickHouse: {e}") from e

    async def _store_single_email(self, email: EmailMessage) -> bool:
        """Store a single email in ClickHouse."""
        try:
            result = await self._store_email_batch([email])
            return result > 0

        except Exception as e:
            self.logger.error(f"Failed to store single email in ClickHouse: {e}")
            raise DatabaseError(f"Failed to store single email in ClickHouse: {e}") from e

    async def _check_email_exists(self, email_id: str) -> bool:
        """Check if email exists in ClickHouse."""
        try:
            loop = asyncio.get_event_loop()

            result = await loop.run_in_executor(
                None,
                lambda: self.client.query(
                    f"SELECT 1 FROM {self.config.table_name} WHERE message_id = %(message_id)s LIMIT 1",
                    parameters={'message_id': email_id}
                )
            )

            return len(result.result_rows) > 0

        except Exception as e:
            self.logger.error(f"Failed to check email existence in ClickHouse: {e}")
            raise DatabaseError(f"Failed to check email existence in ClickHouse: {e}") from e

    async def _get_total_email_count(self) -> int:
        """Get total email count from ClickHouse."""
        try:
            loop = asyncio.get_event_loop()

            result = await loop.run_in_executor(
                None,
                lambda: self.client.query(f"SELECT COUNT(*) FROM {self.config.table_name}")
            )

            return result.result_rows[0][0] if result.result_rows else 0

        except Exception as e:
            self.logger.error(f"Failed to get email count from ClickHouse: {e}")
            raise DatabaseError(f"Failed to get email count from ClickHouse: {e}") from e
