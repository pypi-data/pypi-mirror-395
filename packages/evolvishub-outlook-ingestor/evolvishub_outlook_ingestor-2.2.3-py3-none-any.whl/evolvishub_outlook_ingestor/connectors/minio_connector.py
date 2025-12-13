"""
MinIO S3-Compatible Object Storage Connector for Evolvishub Outlook Ingestor.

This module provides integration with MinIO, a high-performance, S3-compatible
object storage system that can be self-hosted for on-premises deployments.
"""

import asyncio
import io
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Union
from urllib.parse import urlparse

try:
    from minio import Minio
    from minio.error import S3Error, InvalidResponseError
    from minio.commonconfig import Tags
    MINIO_AVAILABLE = True
except ImportError:
    MINIO_AVAILABLE = False

from evolvishub_outlook_ingestor.connectors.base_storage_connector import (
    BaseStorageConnector,
    StorageObject,
    StorageConfig,
)
from evolvishub_outlook_ingestor.core.exceptions import (
    StorageError,
    ConnectionError,
    ValidationError,
    ConfigurationError,
)


class MinIOConnector(BaseStorageConnector):
    """
    MinIO S3-compatible object storage connector.
    
    This connector provides integration with MinIO object storage, supporting
    both self-hosted MinIO instances and other S3-compatible storage services.
    It offers high-performance attachment storage with features like:
    
    - Automatic bucket creation and management
    - Pre-signed URL generation for secure access
    - Metadata storage and retrieval
    - Content deduplication using SHA256 hashes
    - Configurable retention policies
    
    Attributes:
        client (Minio): MinIO client instance
        
    Example:
        ```python
        config = StorageConfig(
            endpoint_url="localhost:9000",
            access_key="minioadmin",
            secret_key="minioadmin",
            bucket_name="email-attachments",
            use_ssl=False  # For local development
        )
        
        connector = MinIOConnector("minio", config)
        
        async with connector:
            # Upload attachment
            storage_obj = await connector.upload_attachment(attachment)
            
            # Generate secure download URL (1 hour expiry)
            download_url = await connector.generate_presigned_url(
                storage_obj.key,
                expires_in=3600
            )
            
            # Download attachment content
            content = await connector.download_attachment(storage_obj.key)
        ```
        
    Note:
        Requires the 'minio' package to be installed:
        pip install minio
    """
    
    def __init__(self, name: str, config: Union[StorageConfig, Dict[str, Any]]):
        """
        Initialize MinIO connector.
        
        Args:
            name: Unique identifier for this connector
            config: MinIO configuration
            
        Raises:
            ImportError: If minio package is not installed
        """
        if not MINIO_AVAILABLE:
            raise ImportError(
                "MinIO connector requires 'minio' package. "
                "Install with: pip install minio"
            )
        
        super().__init__(name, config)
        self.client: Optional[Minio] = None
    
    async def _validate_config(self) -> None:
        """Validate MinIO configuration."""
        if not self.config.endpoint_url:
            raise ConfigurationError("MinIO endpoint_url is required")
        
        if not self.config.access_key:
            raise ConfigurationError("MinIO access_key is required")
        
        if not self.config.secret_key:
            raise ConfigurationError("MinIO secret_key is required")
        
        if not self.config.bucket_name:
            raise ConfigurationError("MinIO bucket_name is required")
        
        # Validate endpoint format
        try:
            parsed = urlparse(self.config.endpoint_url)
            if not parsed.netloc and not parsed.path:
                # Handle cases like "localhost:9000"
                if ":" in self.config.endpoint_url:
                    host, port = self.config.endpoint_url.split(":", 1)
                    if not host or not port.isdigit():
                        raise ValueError("Invalid endpoint format")
                else:
                    raise ValueError("Invalid endpoint format")
        except Exception as e:
            raise ConfigurationError(f"Invalid MinIO endpoint URL: {e}")
    
    async def _initialize_client(self) -> None:
        """Initialize MinIO client."""
        try:
            # Parse endpoint
            endpoint = self.config.endpoint_url
            if endpoint.startswith(("http://", "https://")):
                parsed = urlparse(endpoint)
                endpoint = parsed.netloc
                if parsed.port:
                    endpoint = f"{parsed.hostname}:{parsed.port}"
                else:
                    endpoint = parsed.hostname
            
            # Create MinIO client
            self.client = Minio(
                endpoint=endpoint,
                access_key=self.config.access_key,
                secret_key=self.config.secret_key,
                secure=self.config.use_ssl,
                region=self.config.region,
            )
            
            self.logger.debug(f"MinIO client initialized for endpoint: {endpoint}")
            
        except Exception as e:
            raise ConnectionError(f"Failed to initialize MinIO client: {e}")
    
    async def _cleanup_client(self) -> None:
        """Cleanup MinIO client."""
        # MinIO client doesn't require explicit cleanup
        self.client = None
    
    async def _test_connection(self) -> None:
        """Test MinIO connection."""
        try:
            # Test connection by listing buckets
            loop = asyncio.get_event_loop()
            buckets = await loop.run_in_executor(None, list, self.client.list_buckets())
            self.logger.debug(f"MinIO connection test successful. Found {len(buckets)} buckets")
            
        except Exception as e:
            raise ConnectionError(f"MinIO connection test failed: {e}")
    
    async def _ensure_bucket_exists(self) -> None:
        """Ensure MinIO bucket exists."""
        try:
            loop = asyncio.get_event_loop()
            
            # Check if bucket exists
            bucket_exists = await loop.run_in_executor(
                None, self.client.bucket_exists, self.config.bucket_name
            )
            
            if not bucket_exists:
                # Create bucket
                await loop.run_in_executor(
                    None, self.client.make_bucket, self.config.bucket_name, self.config.region
                )
                self.logger.info(f"Created MinIO bucket: {self.config.bucket_name}")
            else:
                self.logger.debug(f"MinIO bucket exists: {self.config.bucket_name}")
                
        except Exception as e:
            raise StorageError(f"Failed to ensure bucket exists: {e}")
    
    async def _upload_object(
        self,
        key: str,
        content: bytes,
        content_type: str,
        metadata: Dict[str, str]
    ) -> StorageObject:
        """Upload object to MinIO."""
        try:
            loop = asyncio.get_event_loop()
            
            # Create file-like object from bytes
            content_stream = io.BytesIO(content)
            content_size = len(content)
            
            # Upload object
            result = await loop.run_in_executor(
                None,
                self.client.put_object,
                self.config.bucket_name,
                key,
                content_stream,
                content_size,
                content_type,
                metadata
            )
            
            # Get object info for response
            stat = await loop.run_in_executor(
                None, self.client.stat_object, self.config.bucket_name, key
            )
            
            return StorageObject(
                key=key,
                bucket=self.config.bucket_name,
                size=stat.size,
                content_type=stat.content_type,
                etag=stat.etag,
                last_modified=stat.last_modified,
                metadata=stat.metadata or {}
            )
            
        except S3Error as e:
            raise StorageError(f"MinIO upload failed: {e}")
        except Exception as e:
            raise StorageError(f"Unexpected error during upload: {e}")
    
    async def _download_object(self, key: str) -> bytes:
        """Download object from MinIO."""
        try:
            loop = asyncio.get_event_loop()
            
            # Download object
            response = await loop.run_in_executor(
                None, self.client.get_object, self.config.bucket_name, key
            )
            
            # Read content
            content = response.read()
            response.close()
            response.release_conn()
            
            return content
            
        except S3Error as e:
            if e.code == "NoSuchKey":
                raise StorageError(f"Object not found: {key}")
            raise StorageError(f"MinIO download failed: {e}")
        except Exception as e:
            raise StorageError(f"Unexpected error during download: {e}")
    
    async def _delete_object(self, key: str) -> bool:
        """Delete object from MinIO."""
        try:
            loop = asyncio.get_event_loop()
            
            await loop.run_in_executor(
                None, self.client.remove_object, self.config.bucket_name, key
            )
            
            return True
            
        except S3Error as e:
            if e.code == "NoSuchKey":
                self.logger.warning(f"Object not found for deletion: {key}")
                return False
            raise StorageError(f"MinIO deletion failed: {e}")
        except Exception as e:
            raise StorageError(f"Unexpected error during deletion: {e}")
    
    async def _generate_presigned_url_impl(
        self,
        key: str,
        expires_in: int,
        method: str
    ) -> str:
        """Generate presigned URL for MinIO object."""
        try:
            loop = asyncio.get_event_loop()
            
            # Convert expires_in to timedelta
            expires = timedelta(seconds=expires_in)
            
            # Generate presigned URL
            if method.upper() == "GET":
                url = await loop.run_in_executor(
                    None,
                    self.client.presigned_get_object,
                    self.config.bucket_name,
                    key,
                    expires
                )
            elif method.upper() == "PUT":
                url = await loop.run_in_executor(
                    None,
                    self.client.presigned_put_object,
                    self.config.bucket_name,
                    key,
                    expires
                )
            else:
                raise ValidationError(f"Unsupported HTTP method: {method}")
            
            return url
            
        except S3Error as e:
            raise StorageError(f"MinIO presigned URL generation failed: {e}")
        except Exception as e:
            raise StorageError(f"Unexpected error during URL generation: {e}")
    
    async def _list_objects(self, prefix: str, limit: int) -> List[StorageObject]:
        """List objects in MinIO bucket."""
        try:
            loop = asyncio.get_event_loop()
            
            # List objects with prefix
            objects = await loop.run_in_executor(
                None,
                lambda: list(self.client.list_objects(
                    self.config.bucket_name,
                    prefix=prefix,
                    recursive=True
                ))
            )
            
            # Convert to StorageObject instances
            storage_objects = []
            for obj in objects[:limit]:
                # Get detailed object info
                stat = await loop.run_in_executor(
                    None, self.client.stat_object, self.config.bucket_name, obj.object_name
                )
                
                storage_obj = StorageObject(
                    key=obj.object_name,
                    bucket=self.config.bucket_name,
                    size=obj.size,
                    content_type=stat.content_type,
                    etag=obj.etag,
                    last_modified=obj.last_modified,
                    metadata=stat.metadata or {}
                )
                storage_objects.append(storage_obj)
            
            return storage_objects
            
        except S3Error as e:
            raise StorageError(f"MinIO list operation failed: {e}")
        except Exception as e:
            raise StorageError(f"Unexpected error during list operation: {e}")
    
    async def get_bucket_info(self) -> Dict[str, Any]:
        """
        Get information about the MinIO bucket.
        
        Returns:
            Dictionary containing bucket information
        """
        try:
            loop = asyncio.get_event_loop()
            
            # Get bucket location
            location = await loop.run_in_executor(
                None, self.client.get_bucket_location, self.config.bucket_name
            )
            
            # Count objects (limited to avoid performance issues)
            objects = await loop.run_in_executor(
                None,
                lambda: list(self.client.list_objects(
                    self.config.bucket_name,
                    recursive=True
                ))
            )
            
            total_size = sum(obj.size for obj in objects)
            
            return {
                "bucket_name": self.config.bucket_name,
                "location": location,
                "object_count": len(objects),
                "total_size": total_size,
                "endpoint": self.config.endpoint_url,
            }
            
        except Exception as e:
            self.logger.error(f"Failed to get bucket info: {e}")
            return {
                "bucket_name": self.config.bucket_name,
                "error": str(e)
            }
    
    def get_status(self) -> Dict[str, Any]:
        """Get MinIO connector status."""
        status = super().get_status()
        status.update({
            "storage_type": "MinIO S3-Compatible",
            "ssl_enabled": self.config.use_ssl,
            "verify_ssl": self.config.verify_ssl,
        })
        return status
