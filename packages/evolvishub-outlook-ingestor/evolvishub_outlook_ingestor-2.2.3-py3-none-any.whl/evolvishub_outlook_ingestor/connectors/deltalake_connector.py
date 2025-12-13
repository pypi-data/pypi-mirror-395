"""
Delta Lake connector for Evolvishub Outlook Ingestor.

This module implements the Delta Lake connector using delta-spark
for ACID transactional storage layer with Apache Spark backend.

Features:
- ACID transactions for email data consistency and concurrent writes
- Schema evolution for email structure changes over time
- Time travel capabilities for accessing historical email states
- Z-ordering optimization for query performance on common fields
- Support for local filesystem and cloud storage (S3, Azure Data Lake, GCS)
- Email partitioning by received_date and sender_domain
- Delta Lake merge operations for efficient upsert of email updates
"""

import asyncio
import json
import os
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Union
from uuid import UUID

try:
    from pyspark.sql import SparkSession, DataFrame
    from pyspark.sql.types import (
        StructType, StructField, StringType, TimestampType, 
        BooleanType, IntegerType, LongType, ArrayType, MapType
    )
    from pyspark.sql.functions import col, lit, when, coalesce
    from delta import configure_spark_with_delta_pip
    from delta.tables import DeltaTable
    DELTA_AVAILABLE = True
except ImportError:
    DELTA_AVAILABLE = False
    SparkSession = None
    DataFrame = None
    DeltaTable = None
    StructType = None
    StructField = None
    StringType = None
    TimestampType = None
    BooleanType = None
    IntegerType = None
    LongType = None
    ArrayType = None
    MapType = None

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


class DeltaLakeConnector(BaseConnector):
    """Delta Lake connector using PySpark and Delta Lake."""
    
    def __init__(self, name: str, config: Dict[str, Any], **kwargs):
        """
        Initialize Delta Lake connector.
        
        Args:
            name: Connector name
            config: Configuration dictionary containing:
                - table_path: Path to Delta Lake table (local or cloud)
                - app_name: Spark application name
                - master: Spark master URL (local[*] for local mode)
                - warehouse_dir: Spark warehouse directory
                - partition_columns: List of columns to partition by
                - z_order_columns: List of columns for Z-ordering optimization
                - cloud_provider: Cloud provider (aws, azure, gcp)
                - cloud_config: Cloud-specific configuration
                - enable_time_travel: Enable time travel features
                - checkpoint_interval: Delta checkpoint interval
                - log_retention_duration: Log retention duration
                - deleted_file_retention_duration: Deleted file retention
        """
        if not DELTA_AVAILABLE:
            raise ImportError(
                "Delta Lake dependencies are required. "
                "Install with: pip install evolvishub-outlook-ingestor[datalake-delta]"
            )
        
        # Delta Lake doesn't use traditional connection pooling
        super().__init__(name, config, enable_connection_pooling=False, **kwargs)

        # Get credential manager (lazy loading)
        get_credential_manager, _, _ = _get_security_utils()
        self._credential_manager = get_credential_manager()

        # Delta Lake configuration
        self.table_path = config.get("table_path", f"./delta-tables/{name}")
        self.app_name = config.get("app_name", f"evolvishub-outlook-ingestor-{name}")
        self.master = config.get("master", "local[*]")
        self.warehouse_dir = config.get("warehouse_dir", "./spark-warehouse")
        self.partition_columns = config.get("partition_columns", ["received_date_partition", "sender_domain"])
        self.z_order_columns = config.get("z_order_columns", ["received_date", "sender_email"])
        self.cloud_provider = config.get("cloud_provider", None)
        self.cloud_config = config.get("cloud_config", {})
        self.enable_time_travel = config.get("enable_time_travel", True)
        self.checkpoint_interval = config.get("checkpoint_interval", 10)
        self.log_retention_duration = config.get("log_retention_duration", "interval 30 days")
        self.deleted_file_retention_duration = config.get("deleted_file_retention_duration", "interval 7 days")
        
        # Spark session
        self.spark: Optional[SparkSession] = None
        self.delta_table: Optional[DeltaTable] = None
        
        # Schema definitions
        self.email_schema = self._get_email_schema()
        self.attachment_schema = self._get_attachment_schema()
        
        # Ensure table directory exists
        os.makedirs(os.path.dirname(self.table_path) if os.path.dirname(self.table_path) else ".", exist_ok=True)
    
    async def _initialize_connection(self) -> None:
        """Initialize Spark session and Delta Lake table."""
        try:
            self.logger.info(
                "Initializing Delta Lake connection",
                table_path=self.table_path,
                app_name=self.app_name,
                connector=self.name
            )
            
            # Create Spark session in thread pool since it's synchronous
            loop = asyncio.get_event_loop()
            self.spark = await loop.run_in_executor(None, self._create_spark_session)
            
            # Initialize Delta Lake table
            await self._initialize_delta_table()
            
            self.logger.info(
                "Delta Lake connection established",
                table_path=self.table_path,
                connector=self.name
            )
            
        except Exception as e:
            raise ConnectionError(
                f"Failed to initialize Delta Lake: {e}",
                database_type="deltalake",
                cause=e
            )
    
    async def _initialize_pool(self) -> None:
        """Delta Lake doesn't use connection pooling - delegate to single connection."""
        await self._initialize_connection()
    
    async def _cleanup_connection(self) -> None:
        """Cleanup Spark session."""
        if self.spark:
            try:
                loop = asyncio.get_event_loop()
                await loop.run_in_executor(None, self.spark.stop)
                self.logger.info("Delta Lake connection closed", connector=self.name)
            except Exception as e:
                self.logger.warning(
                    "Error closing Delta Lake connection",
                    connector=self.name,
                    error=str(e)
                )
            finally:
                self.spark = None
                self.delta_table = None
    
    async def _cleanup_pool(self) -> None:
        """Delta Lake doesn't use connection pooling - delegate to single connection."""
        await self._cleanup_connection()
    
    async def _test_connection(self) -> None:
        """Test Delta Lake connection."""
        if not self.spark:
            raise ConnectionError("No Spark session available")
        
        try:
            # Test with a simple operation
            loop = asyncio.get_event_loop()
            test_df = await loop.run_in_executor(
                None, 
                lambda: self.spark.sql("SELECT 1 as test").collect()
            )
            
            if not test_df or test_df[0]['test'] != 1:
                raise ConnectionError("Delta Lake connection test failed")
                
            self.logger.debug("Delta Lake connection test passed", connector=self.name)
            
        except Exception as e:
            raise ConnectionError(f"Delta Lake connection test failed: {e}")
    
    def _create_spark_session(self) -> SparkSession:
        """Create and configure Spark session for Delta Lake."""
        # Configure Spark with Delta Lake
        builder = SparkSession.builder \
            .appName(self.app_name) \
            .master(self.master) \
            .config("spark.sql.warehouse.dir", self.warehouse_dir) \
            .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
            .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
            .config("spark.databricks.delta.retentionDurationCheck.enabled", "false") \
            .config("spark.databricks.delta.schema.autoMerge.enabled", "true")
        
        # Add cloud-specific configurations
        if self.cloud_provider == "aws":
            builder = self._configure_aws_spark(builder)
        elif self.cloud_provider == "azure":
            builder = self._configure_azure_spark(builder)
        elif self.cloud_provider == "gcp":
            builder = self._configure_gcp_spark(builder)
        
        # Configure Delta Lake
        builder = configure_spark_with_delta_pip(builder)
        
        return builder.getOrCreate()
    
    def _configure_aws_spark(self, builder):
        """Configure Spark for AWS S3."""
        aws_config = self.cloud_config
        
        builder = builder \
            .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
            .config("spark.hadoop.fs.s3a.aws.credentials.provider", 
                   "org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider")
        
        if aws_config.get("access_key"):
            builder = builder.config("spark.hadoop.fs.s3a.access.key", aws_config["access_key"])
        if aws_config.get("secret_key"):
            builder = builder.config("spark.hadoop.fs.s3a.secret.key", aws_config["secret_key"])
        if aws_config.get("region"):
            builder = builder.config("spark.hadoop.fs.s3a.endpoint.region", aws_config["region"])
        
        return builder
    
    def _configure_azure_spark(self, builder):
        """Configure Spark for Azure Data Lake."""
        azure_config = self.cloud_config
        
        if azure_config.get("account_name") and azure_config.get("account_key"):
            builder = builder.config(
                f"spark.hadoop.fs.azure.account.key.{azure_config['account_name']}.dfs.core.windows.net",
                azure_config["account_key"]
            )
        
        return builder
    
    def _configure_gcp_spark(self, builder):
        """Configure Spark for Google Cloud Storage."""
        gcp_config = self.cloud_config
        
        builder = builder \
            .config("spark.hadoop.fs.gs.impl", "com.google.cloud.hadoop.fs.gcs.GoogleHadoopFileSystem") \
            .config("spark.hadoop.fs.AbstractFileSystem.gs.impl", 
                   "com.google.cloud.hadoop.fs.gcs.GoogleHadoopFS")
        
        if gcp_config.get("service_account_key"):
            builder = builder.config(
                "spark.hadoop.google.cloud.auth.service.account.json.keyfile",
                gcp_config["service_account_key"]
            )
        
        return builder
    
    async def _initialize_delta_table(self) -> None:
        """Initialize Delta Lake table if it doesn't exist."""
        try:
            loop = asyncio.get_event_loop()
            
            # Check if table exists
            table_exists = await loop.run_in_executor(
                None,
                lambda: DeltaTable.isDeltaTable(self.spark, self.table_path)
            )
            
            if not table_exists:
                # Create new Delta table
                await self._create_delta_table()
            else:
                # Load existing table
                self.delta_table = await loop.run_in_executor(
                    None,
                    lambda: DeltaTable.forPath(self.spark, self.table_path)
                )
            
            self.logger.info(
                "Delta Lake table initialized",
                table_path=self.table_path,
                exists=table_exists,
                connector=self.name
            )
            
        except Exception as e:
            raise DatabaseError(
                f"Failed to initialize Delta Lake table: {e}",
                database_type="deltalake",
                operation="initialize_table",
                cause=e
            )
    
    async def _create_delta_table(self) -> None:
        """Create new Delta Lake table with proper schema and partitioning."""
        try:
            loop = asyncio.get_event_loop()
            
            # Create empty DataFrame with schema
            empty_df = await loop.run_in_executor(
                None,
                lambda: self.spark.createDataFrame([], self.email_schema)
            )
            
            # Write as Delta table with partitioning
            await loop.run_in_executor(
                None,
                lambda: empty_df.write
                .format("delta")
                .partitionBy(*self.partition_columns)
                .option("delta.checkpoint.writeStatsAsJson", "false")
                .option("delta.checkpoint.writeStatsAsStruct", "true")
                .save(self.table_path)
            )
            
            # Load the created table
            self.delta_table = await loop.run_in_executor(
                None,
                lambda: DeltaTable.forPath(self.spark, self.table_path)
            )
            
            # Set table properties
            await self._set_table_properties()
            
            self.logger.info(
                "Delta Lake table created",
                table_path=self.table_path,
                partitions=self.partition_columns,
                connector=self.name
            )
            
        except Exception as e:
            raise DatabaseError(
                f"Failed to create Delta Lake table: {e}",
                database_type="deltalake",
                operation="create_table",
                cause=e
            )
    
    async def _set_table_properties(self) -> None:
        """Set Delta Lake table properties for optimization."""
        try:
            loop = asyncio.get_event_loop()
            
            # Set table properties
            properties = {
                "delta.checkpoint.writeStatsAsJson": "false",
                "delta.checkpoint.writeStatsAsStruct": "true",
                "delta.autoOptimize.optimizeWrite": "true",
                "delta.autoOptimize.autoCompact": "true",
                "delta.logRetentionDuration": self.log_retention_duration,
                "delta.deletedFileRetentionDuration": self.deleted_file_retention_duration,
            }
            
            for key, value in properties.items():
                await loop.run_in_executor(
                    None,
                    lambda k=key, v=value: self.spark.sql(
                        f"ALTER TABLE delta.`{self.table_path}` SET TBLPROPERTIES ('{k}' = '{v}')"
                    ).collect()
                )
            
        except Exception as e:
            self.logger.warning(
                "Failed to set table properties",
                error=str(e),
                connector=self.name
            )

    def _get_email_schema(self) -> StructType:
        """Get Spark schema for email data."""
        return StructType([
            StructField("id", StringType(), False),
            StructField("message_id", StringType(), True),
            StructField("subject", StringType(), True),
            StructField("body", StringType(), True),
            StructField("body_preview", StringType(), True),
            StructField("sender_email", StringType(), True),
            StructField("sender_name", StringType(), True),
            StructField("received_date", TimestampType(), True),
            StructField("sent_date", TimestampType(), True),
            StructField("importance", StringType(), True),
            StructField("is_read", BooleanType(), True),
            StructField("has_attachments", BooleanType(), True),
            StructField("folder_id", StringType(), True),
            StructField("folder_name", StringType(), True),
            StructField("categories", ArrayType(StringType()), True),
            StructField("headers", MapType(StringType(), StringType()), True),
            StructField("metadata", MapType(StringType(), StringType()), True),
            StructField("recipients_to", ArrayType(StructType([
                StructField("email", StringType(), True),
                StructField("name", StringType(), True)
            ])), True),
            StructField("recipients_cc", ArrayType(StructType([
                StructField("email", StringType(), True),
                StructField("name", StringType(), True)
            ])), True),
            StructField("recipients_bcc", ArrayType(StructType([
                StructField("email", StringType(), True),
                StructField("name", StringType(), True)
            ])), True),
            StructField("attachments", ArrayType(StructType([
                StructField("id", StringType(), True),
                StructField("name", StringType(), True),
                StructField("content_type", StringType(), True),
                StructField("size", LongType(), True),
                StructField("content_hash", StringType(), True),
                StructField("is_inline", BooleanType(), True),
                StructField("attachment_type", StringType(), True),
                StructField("extended_properties", MapType(StringType(), StringType()), True)
            ])), True),
            # Partition columns
            StructField("received_date_partition", StringType(), True),  # YYYY-MM-DD format
            StructField("sender_domain", StringType(), True),
            # Audit columns
            StructField("created_at", TimestampType(), True),
            StructField("updated_at", TimestampType(), True),
            StructField("version", LongType(), True)
        ])

    def _get_attachment_schema(self) -> StructType:
        """Get Spark schema for attachment data (separate table if needed)."""
        return StructType([
            StructField("id", StringType(), False),
            StructField("email_id", StringType(), False),
            StructField("name", StringType(), True),
            StructField("content_type", StringType(), True),
            StructField("size", LongType(), True),
            StructField("content_hash", StringType(), True),
            StructField("is_inline", BooleanType(), True),
            StructField("attachment_type", StringType(), True),
            StructField("storage_location", StringType(), True),
            StructField("storage_backend", StringType(), True),
            StructField("extended_properties", MapType(StringType(), StringType()), True),
            StructField("created_at", TimestampType(), True)
        ])

    async def _store_email_impl(
        self,
        email: EmailMessage,
        transaction: Optional[Any] = None,
        **kwargs
    ) -> str:
        """Store email in Delta Lake."""
        try:
            # Prepare email data for Delta Lake
            email_data = self._prepare_email_data(email)

            loop = asyncio.get_event_loop()

            # Create DataFrame
            df = await loop.run_in_executor(
                None,
                lambda: self.spark.createDataFrame([email_data], self.email_schema)
            )

            # Perform merge operation for upsert
            await self._merge_email_data(df)

            return email.id

        except Exception as e:
            raise DatabaseError(
                f"Failed to store email in Delta Lake: {e}",
                database_type="deltalake",
                operation="store_email",
                cause=e
            )

    async def _store_emails_batch_impl(
        self,
        emails: List[EmailMessage],
        transaction: Optional[Any] = None,
        **kwargs
    ) -> List[str]:
        """Store multiple emails in Delta Lake."""
        try:
            # Prepare batch data
            email_data_batch = [self._prepare_email_data(email) for email in emails]

            loop = asyncio.get_event_loop()

            # Create DataFrame
            df = await loop.run_in_executor(
                None,
                lambda: self.spark.createDataFrame(email_data_batch, self.email_schema)
            )

            # Perform merge operation for batch upsert
            await self._merge_email_data(df)

            return [email.id for email in emails]

        except Exception as e:
            raise DatabaseError(
                f"Failed to store emails batch in Delta Lake: {e}",
                database_type="deltalake",
                operation="store_emails_batch",
                cause=e
            )

    async def _merge_email_data(self, df: DataFrame, **kwargs) -> None:
        """Merge email data using Delta Lake merge operation."""
        try:
            loop = asyncio.get_event_loop()

            # Perform merge operation
            await loop.run_in_executor(
                None,
                lambda: self.delta_table.alias("target")
                .merge(df.alias("source"), "target.id = source.id")
                .whenMatchedUpdateAll()
                .whenNotMatchedInsertAll()
                .execute()
            )

            # Optimize table periodically
            if kwargs.get("optimize", False):
                await self._optimize_table()

        except Exception as e:
            raise DatabaseError(
                f"Failed to merge email data: {e}",
                database_type="deltalake",
                operation="merge_data",
                cause=e
            )

    async def _optimize_table(self) -> None:
        """Optimize Delta Lake table with Z-ordering."""
        try:
            loop = asyncio.get_event_loop()

            # Run OPTIMIZE command
            optimize_sql = f"OPTIMIZE delta.`{self.table_path}`"
            if self.z_order_columns:
                optimize_sql += f" ZORDER BY ({', '.join(self.z_order_columns)})"

            await loop.run_in_executor(
                None,
                lambda: self.spark.sql(optimize_sql).collect()
            )

            self.logger.info(
                "Delta Lake table optimized",
                z_order_columns=self.z_order_columns,
                connector=self.name
            )

        except Exception as e:
            self.logger.warning(
                "Failed to optimize Delta Lake table",
                error=str(e),
                connector=self.name
            )

    async def _get_email_impl(
        self,
        email_id: str,
        include_attachments: bool = True,
        **kwargs
    ) -> Optional[EmailMessage]:
        """Retrieve email from Delta Lake."""
        try:
            loop = asyncio.get_event_loop()

            # Query for specific email
            df = await loop.run_in_executor(
                None,
                lambda: self.spark.read.format("delta").load(self.table_path)
                .filter(col("id") == email_id)
                .limit(1)
            )

            rows = await loop.run_in_executor(None, df.collect)

            if not rows:
                return None

            # Convert row to EmailMessage
            return self._row_to_email(rows[0])

        except Exception as e:
            raise DatabaseError(
                f"Failed to retrieve email from Delta Lake: {e}",
                database_type="deltalake",
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
        """Search emails in Delta Lake."""
        try:
            loop = asyncio.get_event_loop()

            # Start with base DataFrame
            df = await loop.run_in_executor(
                None,
                lambda: self.spark.read.format("delta").load(self.table_path)
            )

            # Apply filters
            df = await self._apply_filters(df, filters)

            # Apply sorting
            if sort_by:
                df = await loop.run_in_executor(
                    None,
                    lambda: df.orderBy(col(sort_by).desc() if sort_order.lower() == "desc" else col(sort_by).asc())
                )
            else:
                df = await loop.run_in_executor(
                    None,
                    lambda: df.orderBy(col("received_date").desc())
                )

            # Apply pagination
            if offset > 0:
                df = await loop.run_in_executor(None, lambda: df.offset(offset))

            if limit:
                df = await loop.run_in_executor(None, lambda: df.limit(limit))

            # Collect results
            rows = await loop.run_in_executor(None, df.collect)

            # Convert to EmailMessage objects
            return [self._row_to_email(row) for row in rows]

        except Exception as e:
            raise DatabaseError(
                f"Failed to search emails in Delta Lake: {e}",
                database_type="deltalake",
                operation="search_emails",
                cause=e
            )

    async def _apply_filters(self, df: DataFrame, filters: Dict[str, Any]) -> DataFrame:
        """Apply search filters to DataFrame."""
        loop = asyncio.get_event_loop()

        for key, value in filters.items():
            if key == "sender_email":
                df = await loop.run_in_executor(None, lambda: df.filter(col("sender_email") == value))
            elif key == "subject_contains":
                df = await loop.run_in_executor(None, lambda: df.filter(col("subject").contains(value)))
            elif key == "date_from":
                df = await loop.run_in_executor(None, lambda: df.filter(col("received_date") >= value))
            elif key == "date_to":
                df = await loop.run_in_executor(None, lambda: df.filter(col("received_date") <= value))
            elif key == "folder_id":
                df = await loop.run_in_executor(None, lambda: df.filter(col("folder_id") == value))
            elif key == "has_attachments":
                df = await loop.run_in_executor(None, lambda: df.filter(col("has_attachments") == value))
            elif key == "sender_domain":
                df = await loop.run_in_executor(None, lambda: df.filter(col("sender_domain") == value))

        return df

    def _prepare_email_data(self, email: EmailMessage) -> Dict[str, Any]:
        """Prepare email data for Delta Lake storage."""
        # Extract sender domain for partitioning
        sender_domain = ""
        if email.sender and email.sender.email:
            sender_domain = email.sender.email.split("@")[-1] if "@" in email.sender.email else "unknown"

        # Format received date for partitioning (YYYY-MM-DD)
        received_date_partition = ""
        if email.received_date:
            received_date_partition = email.received_date.strftime("%Y-%m-%d")

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
            "received_date_partition": received_date_partition,
            "sender_domain": sender_domain,
            "created_at": datetime.now(timezone.utc),
            "updated_at": datetime.now(timezone.utc),
            "version": 1
        }

    def _row_to_email(self, row) -> EmailMessage:
        """Convert Spark Row to EmailMessage."""
        from evolvishub_outlook_ingestor.core.data_models import EmailAddress, OutlookFolder

        # Create sender
        sender = None
        if row.sender_email:
            sender = EmailAddress(email=row.sender_email, name=row.sender_name)

        # Create folder
        folder = None
        if row.folder_id:
            folder = OutlookFolder(id=row.folder_id, name=row.folder_name)

        # Create recipients
        recipients = {"to": [], "cc": [], "bcc": []}

        if row.recipients_to:
            recipients["to"] = [EmailAddress(email=r["email"], name=r["name"]) for r in row.recipients_to]
        if row.recipients_cc:
            recipients["cc"] = [EmailAddress(email=r["email"], name=r["name"]) for r in row.recipients_cc]
        if row.recipients_bcc:
            recipients["bcc"] = [EmailAddress(email=r["email"], name=r["name"]) for r in row.recipients_bcc]

        # Create attachments
        attachments = []
        if row.attachments:
            for att_data in row.attachments:
                attachment = EmailAttachment(
                    id=att_data["id"],
                    name=att_data["name"],
                    content_type=att_data["content_type"],
                    size=att_data["size"],
                    content_hash=att_data["content_hash"],
                    is_inline=att_data["is_inline"],
                    attachment_type=att_data["attachment_type"],
                    extended_properties=att_data["extended_properties"]
                )
                attachments.append(attachment)

        return EmailMessage(
            id=row.id,
            message_id=row.message_id,
            subject=row.subject,
            body=row.body,
            body_preview=row.body_preview,
            sender=sender,
            received_date=row.received_date,
            sent_date=row.sent_date,
            importance=row.importance,
            is_read=row.is_read,
            folder=folder,
            categories=row.categories or [],
            headers=row.headers or {},
            metadata=row.metadata or {},
            recipients=recipients,
            attachments=attachments
        )

    async def _begin_transaction(self, isolation_level: Optional[str] = None) -> Any:
        """Begin Delta Lake transaction (Delta Lake handles ACID automatically)."""
        # Delta Lake provides ACID transactions automatically
        # Return a transaction context for compatibility
        return {"transaction_id": f"delta_tx_{datetime.now().timestamp()}"}

    async def _commit_transaction(self, transaction: Any) -> None:
        """Commit Delta Lake transaction (automatic with Delta Lake)."""
        # Delta Lake commits automatically on write operations
        pass

    async def _rollback_transaction(self, transaction: Any) -> None:
        """Rollback Delta Lake transaction (not supported, use time travel)."""
        # Delta Lake doesn't support explicit rollback
        # Use time travel features to access previous versions
        raise TransactionError("Delta Lake doesn't support explicit rollback. Use time travel features instead.")

    # Time Travel and Advanced Features

    async def get_email_at_version(self, email_id: str, version: int) -> Optional[EmailMessage]:
        """Get email at specific version using Delta Lake time travel."""
        try:
            loop = asyncio.get_event_loop()

            df = await loop.run_in_executor(
                None,
                lambda: self.spark.read.format("delta").option("versionAsOf", version)
                .load(self.table_path)
                .filter(col("id") == email_id)
                .limit(1)
            )

            rows = await loop.run_in_executor(None, df.collect)

            if not rows:
                return None

            return self._row_to_email(rows[0])

        except Exception as e:
            raise DatabaseError(
                f"Failed to get email at version {version}: {e}",
                database_type="deltalake",
                operation="time_travel",
                cause=e
            )

    async def get_email_at_timestamp(self, email_id: str, timestamp: datetime) -> Optional[EmailMessage]:
        """Get email at specific timestamp using Delta Lake time travel."""
        try:
            loop = asyncio.get_event_loop()

            timestamp_str = timestamp.strftime("%Y-%m-%d %H:%M:%S")

            df = await loop.run_in_executor(
                None,
                lambda: self.spark.read.format("delta").option("timestampAsOf", timestamp_str)
                .load(self.table_path)
                .filter(col("id") == email_id)
                .limit(1)
            )

            rows = await loop.run_in_executor(None, df.collect)

            if not rows:
                return None

            return self._row_to_email(rows[0])

        except Exception as e:
            raise DatabaseError(
                f"Failed to get email at timestamp {timestamp}: {e}",
                database_type="deltalake",
                operation="time_travel",
                cause=e
            )

    async def get_table_history(self, limit: int = 20) -> List[Dict[str, Any]]:
        """Get Delta Lake table history."""
        try:
            loop = asyncio.get_event_loop()

            history_df = await loop.run_in_executor(
                None,
                lambda: self.delta_table.history(limit)
            )

            rows = await loop.run_in_executor(None, history_df.collect)

            return [row.asDict() for row in rows]

        except Exception as e:
            raise DatabaseError(
                f"Failed to get table history: {e}",
                database_type="deltalake",
                operation="get_history",
                cause=e
            )

    async def vacuum_table(self, retention_hours: int = 168) -> None:
        """Vacuum Delta Lake table to remove old files."""
        try:
            loop = asyncio.get_event_loop()

            await loop.run_in_executor(
                None,
                lambda: self.delta_table.vacuum(retention_hours)
            )

            self.logger.info(
                "Delta Lake table vacuumed",
                retention_hours=retention_hours,
                connector=self.name
            )

        except Exception as e:
            raise DatabaseError(
                f"Failed to vacuum table: {e}",
                database_type="deltalake",
                operation="vacuum",
                cause=e
            )
