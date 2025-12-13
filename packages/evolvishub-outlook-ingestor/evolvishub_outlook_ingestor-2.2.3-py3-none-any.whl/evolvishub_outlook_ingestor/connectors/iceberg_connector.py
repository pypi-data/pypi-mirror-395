"""
Apache Iceberg connector for Evolvishub Outlook Ingestor.

This module implements the Apache Iceberg connector using pyiceberg
for open table format with large-scale analytics capabilities.

Features:
- Automatic hidden partitioning for email data optimization
- Schema evolution without breaking existing queries or consumers
- Snapshot isolation and time travel for email versioning
- Multiple compute engine support (Spark, Trino, Flink)
- Efficient metadata operations for large email datasets
- Compaction strategies for optimal storage and query performance
"""

import asyncio
import json
import os
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Union
from uuid import UUID

try:
    from pyiceberg.catalog import load_catalog
    from pyiceberg.table import Table
    from pyiceberg.schema import Schema
    from pyiceberg.types import (
        NestedField, StringType, TimestampType, BooleanType, 
        LongType, ListType, MapType, StructType
    )
    from pyiceberg.partitioning import PartitionSpec, PartitionField
    from pyiceberg.transforms import DayTransform, BucketTransform
    import pyarrow as pa
    import pyarrow.compute as pc
    ICEBERG_AVAILABLE = True
except ImportError:
    ICEBERG_AVAILABLE = False
    load_catalog = None
    Table = None
    Schema = None
    NestedField = None
    StringType = None
    TimestampType = None
    BooleanType = None
    LongType = None
    ListType = None
    MapType = None
    StructType = None
    PartitionSpec = None
    PartitionField = None
    DayTransform = None
    BucketTransform = None

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


class IcebergConnector(BaseConnector):
    """Apache Iceberg connector using pyiceberg."""
    
    def __init__(self, name: str, config: Dict[str, Any], **kwargs):
        """
        Initialize Iceberg connector.
        
        Args:
            name: Connector name
            config: Configuration dictionary containing:
                - catalog_type: Catalog type (hive, hadoop, rest, glue, etc.)
                - catalog_config: Catalog-specific configuration
                - namespace: Iceberg namespace (database)
                - table_name: Iceberg table name
                - warehouse_path: Warehouse path for file-based catalogs
                - partition_spec: Partition specification
                - table_properties: Additional table properties
                - enable_compaction: Enable automatic compaction
                - compaction_strategy: Compaction strategy configuration
                - snapshot_retention: Snapshot retention configuration
        """
        if not ICEBERG_AVAILABLE:
            raise ImportError(
                "Apache Iceberg dependencies are required. "
                "Install with: pip install evolvishub-outlook-ingestor[datalake-iceberg]"
            )
        
        # Iceberg doesn't use traditional connection pooling
        super().__init__(name, config, enable_connection_pooling=False, **kwargs)

        # Get credential manager (lazy loading)
        get_credential_manager, _, _ = _get_security_utils()
        self._credential_manager = get_credential_manager()

        # Iceberg configuration
        self.catalog_type = config.get("catalog_type", "hadoop")
        self.catalog_config = config.get("catalog_config", {})
        self.namespace = config.get("namespace", "outlook_data")
        self.table_name = config.get("table_name", f"emails_{name}")
        self.warehouse_path = config.get("warehouse_path", "./iceberg-warehouse")
        self.partition_spec = config.get("partition_spec", None)
        self.table_properties = config.get("table_properties", {})
        self.enable_compaction = config.get("enable_compaction", True)
        self.compaction_strategy = config.get("compaction_strategy", {})
        self.snapshot_retention = config.get("snapshot_retention", {})
        
        # Iceberg objects
        self.catalog = None
        self.table: Optional[Table] = None
        
        # Schema definitions
        self.email_schema = self._get_email_schema()
        self.partition_spec_obj = self._get_partition_spec()
        
        # Ensure warehouse directory exists
        os.makedirs(self.warehouse_path, exist_ok=True)
    
    async def _initialize_connection(self) -> None:
        """Initialize Iceberg catalog and table."""
        try:
            self.logger.info(
                "Initializing Iceberg connection",
                catalog_type=self.catalog_type,
                namespace=self.namespace,
                table_name=self.table_name,
                connector=self.name
            )
            
            # Initialize catalog in thread pool since it may be synchronous
            loop = asyncio.get_event_loop()
            self.catalog = await loop.run_in_executor(None, self._create_catalog)
            
            # Initialize table
            await self._initialize_table()
            
            self.logger.info(
                "Iceberg connection established",
                namespace=self.namespace,
                table_name=self.table_name,
                connector=self.name
            )
            
        except Exception as e:
            raise ConnectionError(
                f"Failed to initialize Iceberg: {e}",
                database_type="iceberg",
                cause=e
            )
    
    async def _initialize_pool(self) -> None:
        """Iceberg doesn't use connection pooling - delegate to single connection."""
        await self._initialize_connection()
    
    async def _cleanup_connection(self) -> None:
        """Cleanup Iceberg connection."""
        # Iceberg catalog doesn't need explicit cleanup
        self.catalog = None
        self.table = None
        self.logger.info("Iceberg connection closed", connector=self.name)
    
    async def _cleanup_pool(self) -> None:
        """Iceberg doesn't use connection pooling - delegate to single connection."""
        await self._cleanup_connection()
    
    async def _test_connection(self) -> None:
        """Test Iceberg connection."""
        if not self.catalog:
            raise ConnectionError("No Iceberg catalog available")
        
        try:
            # Test catalog connectivity
            loop = asyncio.get_event_loop()
            namespaces = await loop.run_in_executor(None, self.catalog.list_namespaces)
            
            self.logger.debug(
                "Iceberg connection test passed",
                namespaces=len(namespaces),
                connector=self.name
            )
            
        except Exception as e:
            raise ConnectionError(f"Iceberg connection test failed: {e}")
    
    def _create_catalog(self):
        """Create Iceberg catalog based on configuration."""
        # Build catalog configuration
        catalog_config = {
            "type": self.catalog_type,
            **self.catalog_config
        }
        
        # Add warehouse path for file-based catalogs
        if self.catalog_type in ["hadoop", "hive"]:
            catalog_config["warehouse"] = self.warehouse_path
        
        return load_catalog(name=f"{self.name}_catalog", **catalog_config)
    
    async def _initialize_table(self) -> None:
        """Initialize Iceberg table if it doesn't exist."""
        try:
            loop = asyncio.get_event_loop()
            
            # Check if namespace exists
            try:
                await loop.run_in_executor(
                    None,
                    lambda: self.catalog.load_namespace_properties(self.namespace)
                )
            except Exception:
                # Create namespace if it doesn't exist
                await loop.run_in_executor(
                    None,
                    lambda: self.catalog.create_namespace(self.namespace)
                )
            
            # Check if table exists
            table_identifier = f"{self.namespace}.{self.table_name}"
            
            try:
                self.table = await loop.run_in_executor(
                    None,
                    lambda: self.catalog.load_table(table_identifier)
                )
                self.logger.info(
                    "Iceberg table loaded",
                    table_identifier=table_identifier,
                    connector=self.name
                )
            except Exception:
                # Create new table
                await self._create_table(table_identifier)
            
        except Exception as e:
            raise DatabaseError(
                f"Failed to initialize Iceberg table: {e}",
                database_type="iceberg",
                operation="initialize_table",
                cause=e
            )
    
    async def _create_table(self, table_identifier: str) -> None:
        """Create new Iceberg table with proper schema and partitioning."""
        try:
            loop = asyncio.get_event_loop()
            
            # Create table
            self.table = await loop.run_in_executor(
                None,
                lambda: self.catalog.create_table(
                    identifier=table_identifier,
                    schema=self.email_schema,
                    partition_spec=self.partition_spec_obj,
                    properties=self.table_properties
                )
            )
            
            self.logger.info(
                "Iceberg table created",
                table_identifier=table_identifier,
                schema_fields=len(self.email_schema.fields),
                connector=self.name
            )
            
        except Exception as e:
            raise DatabaseError(
                f"Failed to create Iceberg table: {e}",
                database_type="iceberg",
                operation="create_table",
                cause=e
            )
    
    def _get_email_schema(self) -> Schema:
        """Get Iceberg schema for email data."""
        return Schema(
            NestedField(1, "id", StringType(), required=True),
            NestedField(2, "message_id", StringType(), required=False),
            NestedField(3, "subject", StringType(), required=False),
            NestedField(4, "body", StringType(), required=False),
            NestedField(5, "body_preview", StringType(), required=False),
            NestedField(6, "sender_email", StringType(), required=False),
            NestedField(7, "sender_name", StringType(), required=False),
            NestedField(8, "received_date", TimestampType(), required=False),
            NestedField(9, "sent_date", TimestampType(), required=False),
            NestedField(10, "importance", StringType(), required=False),
            NestedField(11, "is_read", BooleanType(), required=False),
            NestedField(12, "has_attachments", BooleanType(), required=False),
            NestedField(13, "folder_id", StringType(), required=False),
            NestedField(14, "folder_name", StringType(), required=False),
            NestedField(15, "categories", ListType(StringType()), required=False),
            NestedField(16, "headers", MapType(StringType(), StringType()), required=False),
            NestedField(17, "metadata", MapType(StringType(), StringType()), required=False),
            NestedField(18, "recipients_to", ListType(StructType(
                NestedField(181, "email", StringType(), required=False),
                NestedField(182, "name", StringType(), required=False)
            )), required=False),
            NestedField(19, "recipients_cc", ListType(StructType(
                NestedField(191, "email", StringType(), required=False),
                NestedField(192, "name", StringType(), required=False)
            )), required=False),
            NestedField(20, "recipients_bcc", ListType(StructType(
                NestedField(201, "email", StringType(), required=False),
                NestedField(202, "name", StringType(), required=False)
            )), required=False),
            NestedField(21, "attachments", ListType(StructType(
                NestedField(211, "id", StringType(), required=False),
                NestedField(212, "name", StringType(), required=False),
                NestedField(213, "content_type", StringType(), required=False),
                NestedField(214, "size", LongType(), required=False),
                NestedField(215, "content_hash", StringType(), required=False),
                NestedField(216, "is_inline", BooleanType(), required=False),
                NestedField(217, "attachment_type", StringType(), required=False),
                NestedField(218, "extended_properties", MapType(StringType(), StringType()), required=False)
            )), required=False),
            NestedField(22, "sender_domain", StringType(), required=False),
            NestedField(23, "created_at", TimestampType(), required=False),
            NestedField(24, "updated_at", TimestampType(), required=False),
            NestedField(25, "version", LongType(), required=False)
        )
    
    def _get_partition_spec(self) -> PartitionSpec:
        """Get Iceberg partition specification."""
        if self.partition_spec:
            # Use custom partition spec if provided
            return PartitionSpec.parse(self.partition_spec)
        
        # Default partition spec: daily partitioning by received_date and bucketing by sender_domain
        return PartitionSpec(
            PartitionField(
                source_id=8,  # received_date field
                field_id=1000,
                transform=DayTransform(),
                name="received_date_day"
            ),
            PartitionField(
                source_id=22,  # sender_domain field
                field_id=1001,
                transform=BucketTransform(16),  # 16 buckets
                name="sender_domain_bucket"
            )
        )

    async def _store_email_impl(
        self,
        email: EmailMessage,
        transaction: Optional[Any] = None,
        **kwargs
    ) -> str:
        """Store email in Iceberg table."""
        try:
            # Prepare email data for Iceberg
            email_data = self._prepare_email_data(email)

            # Convert to PyArrow table
            loop = asyncio.get_event_loop()
            arrow_table = await loop.run_in_executor(
                None,
                lambda: pa.Table.from_pylist([email_data])
            )

            # Append to Iceberg table
            await loop.run_in_executor(
                None,
                lambda: self.table.append(arrow_table)
            )

            return email.id

        except Exception as e:
            raise DatabaseError(
                f"Failed to store email in Iceberg: {e}",
                database_type="iceberg",
                operation="store_email",
                cause=e
            )

    def _prepare_email_data(self, email: EmailMessage) -> Dict[str, Any]:
        """Prepare email data for Iceberg storage."""
        # Extract sender domain for partitioning
        sender_domain = ""
        if email.sender and email.sender.email:
            sender_domain = email.sender.email.split("@")[-1] if "@" in email.sender.email else "unknown"

        # Prepare recipients
        recipients_to = []
        recipients_cc = []
        recipients_bcc = []

        if email.recipients:
            recipients_to = [{"email": r.email, "name": r.name} for r in email.recipients.get("to", [])]
            recipients_cc = [{"email": r.email, "name": r.name} for r in email.recipients.get("cc", [])]
            recipients_bcc = [{"email": r.email, "name": r.name} for r in email.recipients.get("bcc", [])]

        # Prepare attachments
        attachments = []
        if email.attachments:
            for attachment in email.attachments:
                att_data = {
                    "id": attachment.id,
                    "name": attachment.name,
                    "content_type": attachment.content_type,
                    "size": attachment.size,
                    "content_hash": attachment.content_hash,
                    "is_inline": attachment.is_inline,
                    "attachment_type": attachment.attachment_type,
                    "extended_properties": attachment.extended_properties or {}
                }
                attachments.append(att_data)

        # Convert timestamps to microseconds (Iceberg format)
        received_date_us = None
        if email.received_date:
            received_date_us = int(email.received_date.timestamp() * 1_000_000)

        sent_date_us = None
        if email.sent_date:
            sent_date_us = int(email.sent_date.timestamp() * 1_000_000)

        created_at_us = int(datetime.now(timezone.utc).timestamp() * 1_000_000)

        return {
            "id": email.id,
            "message_id": email.message_id,
            "subject": email.subject,
            "body": email.body,
            "body_preview": email.body_preview,
            "sender_email": email.sender.email if email.sender else None,
            "sender_name": email.sender.name if email.sender else None,
            "received_date": received_date_us,
            "sent_date": sent_date_us,
            "importance": email.importance,
            "is_read": email.is_read,
            "has_attachments": bool(email.attachments),
            "folder_id": email.folder.id if email.folder else None,
            "folder_name": email.folder.name if email.folder else None,
            "categories": email.categories or [],
            "headers": email.headers or {},
            "metadata": email.metadata or {},
            "recipients_to": recipients_to,
            "recipients_cc": recipients_cc,
            "recipients_bcc": recipients_bcc,
            "attachments": attachments,
            "sender_domain": sender_domain,
            "created_at": created_at_us,
            "updated_at": created_at_us,
            "version": 1
        }
