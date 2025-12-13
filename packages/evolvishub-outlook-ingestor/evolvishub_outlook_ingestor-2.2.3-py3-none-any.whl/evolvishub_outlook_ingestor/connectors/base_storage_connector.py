"""
Base Object Storage Connector for Evolvishub Outlook Ingestor.

This module provides the abstract base class for all object storage connectors,
ensuring consistent behavior across different cloud storage providers and
self-hosted solutions like MinIO.
"""

import asyncio
import hashlib
import mimetypes
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, BinaryIO, Union
from dataclasses import dataclass
from urllib.parse import urlparse
import logging

from evolvishub_outlook_ingestor.core.logging import LoggerMixin
from evolvishub_outlook_ingestor.core.exceptions import (
    StorageError,
    ConnectionError,
    ValidationError,
    ConfigurationError,
)
from evolvishub_outlook_ingestor.core.data_models import EmailAttachment


@dataclass
class StorageObject:
    """
    Represents an object stored in object storage.
    
    Attributes:
        key (str): Unique identifier/path for the object
        bucket (str): Storage bucket/container name
        size (int): Size of the object in bytes
        content_type (str): MIME type of the object
        etag (str): Entity tag (usually MD5 hash)
        last_modified (datetime): Last modification timestamp
        metadata (Dict[str, str]): Custom metadata key-value pairs
        url (Optional[str]): Pre-signed URL for access (if generated)
        expires_at (Optional[datetime]): URL expiration time
    """
    key: str
    bucket: str
    size: int
    content_type: str
    etag: str
    last_modified: datetime
    metadata: Dict[str, str]
    url: Optional[str] = None
    expires_at: Optional[datetime] = None


@dataclass
class StorageConfig:
    """
    Configuration for object storage connections.
    
    Attributes:
        endpoint_url (Optional[str]): Custom endpoint URL (for S3-compatible services)
        region (Optional[str]): Storage region
        access_key (str): Access key ID
        secret_key (str): Secret access key
        bucket_name (str): Default bucket name
        use_ssl (bool): Whether to use SSL/TLS
        verify_ssl (bool): Whether to verify SSL certificates
        timeout (int): Request timeout in seconds
        max_retries (int): Maximum number of retry attempts
        retry_delay (float): Delay between retries in seconds
    """
    access_key: str
    secret_key: str
    bucket_name: str
    endpoint_url: Optional[str] = None
    region: Optional[str] = None
    use_ssl: bool = True
    verify_ssl: bool = True
    timeout: int = 30
    max_retries: int = 3
    retry_delay: float = 1.0


class BaseStorageConnector(ABC, LoggerMixin):
    """
    Abstract base class for object storage connectors.
    
    This class provides a unified interface for all object storage implementations,
    including AWS S3, Azure Blob Storage, Google Cloud Storage, and MinIO.
    It handles common operations like upload, download, delete, and URL generation.
    
    Attributes:
        name (str): Unique identifier for this connector instance
        config (StorageConfig): Storage configuration
        client: Storage client instance (implementation-specific)
        is_connected (bool): Connection status
        
    Example:
        ```python
        # Using MinIO connector
        config = StorageConfig(
            endpoint_url="http://localhost:9000",
            access_key="minioadmin",
            secret_key="minioadmin",
            bucket_name="email-attachments"
        )
        
        connector = MinIOConnector("minio", config)
        
        async with connector:
            # Upload attachment
            storage_obj = await connector.upload_attachment(attachment)
            
            # Generate secure URL
            url = await connector.generate_presigned_url(
                storage_obj.key, 
                expires_in=3600
            )
        ```
    """
    
    def __init__(self, name: str, config: Union[StorageConfig, Dict[str, Any]]):
        """
        Initialize the storage connector.
        
        Args:
            name: Unique identifier for this connector
            config: Storage configuration (StorageConfig or dict)
        """
        self.name = name
        self.config = config if isinstance(config, StorageConfig) else StorageConfig(**config)
        self.client = None
        self.is_connected = False
        self._setup_logger()
    
    async def __aenter__(self):
        """Async context manager entry."""
        await self.initialize()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.cleanup()
    
    async def initialize(self) -> None:
        """
        Initialize the storage connector and establish connection.
        
        Raises:
            ConnectionError: If unable to establish connection
            ConfigurationError: If configuration is invalid
        """
        try:
            self.logger.info(f"Initializing {self.__class__.__name__} connector: {self.name}")
            
            # Validate configuration
            await self._validate_config()
            
            # Initialize client
            await self._initialize_client()
            
            # Test connection
            await self._test_connection()
            
            # Ensure bucket exists
            await self._ensure_bucket_exists()
            
            self.is_connected = True
            self.logger.info(f"Storage connector {self.name} initialized successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize storage connector {self.name}: {e}")
            raise ConnectionError(f"Storage initialization failed: {e}")
    
    async def cleanup(self) -> None:
        """Cleanup storage connector and close connections."""
        try:
            if self.client:
                await self._cleanup_client()
            self.is_connected = False
            self.logger.info(f"Storage connector {self.name} cleaned up")
        except Exception as e:
            self.logger.error(f"Error during storage cleanup: {e}")
    
    async def upload_attachment(
        self,
        attachment: EmailAttachment,
        key_prefix: str = "",
        metadata: Optional[Dict[str, str]] = None
    ) -> StorageObject:
        """
        Upload an email attachment to object storage.
        
        Args:
            attachment: EmailAttachment object to upload
            key_prefix: Optional prefix for the storage key
            metadata: Additional metadata to store with the object
            
        Returns:
            StorageObject with upload details
            
        Raises:
            StorageError: If upload fails
            ValidationError: If attachment is invalid
        """
        if not self.is_connected:
            raise ConnectionError("Storage connector not initialized")
        
        # Generate storage key
        storage_key = self._generate_storage_key(attachment, key_prefix)
        
        # Prepare metadata
        object_metadata = {
            "attachment_id": attachment.id,
            "original_name": attachment.name,
            "content_type": attachment.content_type,
            "size": str(attachment.size),
            "uploaded_at": datetime.utcnow().isoformat(),
        }
        if metadata:
            object_metadata.update(metadata)
        
        try:
            # Upload to storage
            storage_obj = await self._upload_object(
                key=storage_key,
                content=attachment.content,
                content_type=attachment.content_type,
                metadata=object_metadata
            )
            
            self.logger.info(f"Uploaded attachment {attachment.id} to {storage_key}")
            return storage_obj
            
        except Exception as e:
            self.logger.error(f"Failed to upload attachment {attachment.id}: {e}")
            raise StorageError(f"Upload failed: {e}")
    
    async def download_attachment(self, storage_key: str) -> bytes:
        """
        Download an attachment from object storage.
        
        Args:
            storage_key: Storage key/path of the object
            
        Returns:
            Binary content of the attachment
            
        Raises:
            StorageError: If download fails
        """
        if not self.is_connected:
            raise ConnectionError("Storage connector not initialized")
        
        try:
            content = await self._download_object(storage_key)
            self.logger.debug(f"Downloaded attachment from {storage_key}")
            return content
            
        except Exception as e:
            self.logger.error(f"Failed to download attachment from {storage_key}: {e}")
            raise StorageError(f"Download failed: {e}")
    
    async def delete_attachment(self, storage_key: str) -> bool:
        """
        Delete an attachment from object storage.
        
        Args:
            storage_key: Storage key/path of the object
            
        Returns:
            True if deletion was successful
            
        Raises:
            StorageError: If deletion fails
        """
        if not self.is_connected:
            raise ConnectionError("Storage connector not initialized")
        
        try:
            success = await self._delete_object(storage_key)
            if success:
                self.logger.info(f"Deleted attachment from {storage_key}")
            return success
            
        except Exception as e:
            self.logger.error(f"Failed to delete attachment from {storage_key}: {e}")
            raise StorageError(f"Deletion failed: {e}")
    
    async def generate_presigned_url(
        self,
        storage_key: str,
        expires_in: int = 3600,
        method: str = "GET"
    ) -> str:
        """
        Generate a pre-signed URL for secure access to an attachment.
        
        Args:
            storage_key: Storage key/path of the object
            expires_in: URL expiration time in seconds (default: 1 hour)
            method: HTTP method for the URL (GET, PUT, etc.)
            
        Returns:
            Pre-signed URL string
            
        Raises:
            StorageError: If URL generation fails
        """
        if not self.is_connected:
            raise ConnectionError("Storage connector not initialized")
        
        try:
            url = await self._generate_presigned_url_impl(storage_key, expires_in, method)
            self.logger.debug(f"Generated presigned URL for {storage_key}")
            return url
            
        except Exception as e:
            self.logger.error(f"Failed to generate presigned URL for {storage_key}: {e}")
            raise StorageError(f"URL generation failed: {e}")
    
    async def list_attachments(
        self,
        prefix: str = "",
        limit: int = 1000
    ) -> List[StorageObject]:
        """
        List attachments in storage with optional prefix filter.
        
        Args:
            prefix: Key prefix to filter objects
            limit: Maximum number of objects to return
            
        Returns:
            List of StorageObject instances
        """
        if not self.is_connected:
            raise ConnectionError("Storage connector not initialized")
        
        try:
            objects = await self._list_objects(prefix, limit)
            self.logger.debug(f"Listed {len(objects)} objects with prefix '{prefix}'")
            return objects
            
        except Exception as e:
            self.logger.error(f"Failed to list objects: {e}")
            raise StorageError(f"List operation failed: {e}")
    
    def _generate_storage_key(self, attachment: EmailAttachment, prefix: str = "") -> str:
        """
        Generate a unique storage key for an attachment.
        
        Args:
            attachment: EmailAttachment object
            prefix: Optional prefix for the key
            
        Returns:
            Unique storage key
        """
        # Create hash of content for deduplication
        content_hash = hashlib.sha256(attachment.content).hexdigest()
        
        # Extract file extension
        file_ext = ""
        if "." in attachment.name:
            file_ext = attachment.name.split(".")[-1].lower()
        
        # Generate key: prefix/year/month/day/hash.ext
        date_path = datetime.utcnow().strftime("%Y/%m/%d")
        key = f"{prefix}/{date_path}/{content_hash}"
        
        if file_ext:
            key += f".{file_ext}"
        
        return key.strip("/")
    
    # Abstract methods that must be implemented by subclasses
    
    @abstractmethod
    async def _validate_config(self) -> None:
        """Validate storage configuration."""
        pass
    
    @abstractmethod
    async def _initialize_client(self) -> None:
        """Initialize storage client."""
        pass
    
    @abstractmethod
    async def _cleanup_client(self) -> None:
        """Cleanup storage client."""
        pass
    
    @abstractmethod
    async def _test_connection(self) -> None:
        """Test storage connection."""
        pass
    
    @abstractmethod
    async def _ensure_bucket_exists(self) -> None:
        """Ensure storage bucket exists."""
        pass
    
    @abstractmethod
    async def _upload_object(
        self,
        key: str,
        content: bytes,
        content_type: str,
        metadata: Dict[str, str]
    ) -> StorageObject:
        """Upload object to storage."""
        pass
    
    @abstractmethod
    async def _download_object(self, key: str) -> bytes:
        """Download object from storage."""
        pass
    
    @abstractmethod
    async def _delete_object(self, key: str) -> bool:
        """Delete object from storage."""
        pass
    
    @abstractmethod
    async def _generate_presigned_url_impl(
        self,
        key: str,
        expires_in: int,
        method: str
    ) -> str:
        """Generate presigned URL."""
        pass
    
    @abstractmethod
    async def _list_objects(self, prefix: str, limit: int) -> List[StorageObject]:
        """List objects in storage."""
        pass
    
    def get_status(self) -> Dict[str, Any]:
        """
        Get connector status information.
        
        Returns:
            Dictionary containing status information
        """
        return {
            "connector": self.name,
            "type": self.__class__.__name__,
            "is_connected": self.is_connected,
            "bucket": self.config.bucket_name,
            "endpoint": getattr(self.config, 'endpoint_url', None),
            "region": getattr(self.config, 'region', None),
        }
