"""
Google Cloud Storage Connector for Evolvishub Outlook Ingestor.

This module provides integration with Google Cloud Storage (GCS), offering
enterprise-grade cloud storage with global infrastructure, advanced ML
integration, and seamless Google Workspace connectivity.
"""

import asyncio
import io
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Union

try:
    from google.cloud import storage
    from google.cloud.storage import Blob, Bucket
    from google.cloud.exceptions import NotFound, Forbidden, GoogleCloudError
    from google.auth.exceptions import DefaultCredentialsError
    from google.oauth2 import service_account
    GCS_AVAILABLE = True
except ImportError:
    GCS_AVAILABLE = False

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


class GCSConnector(BaseStorageConnector):
    """
    Google Cloud Storage connector.
    
    This connector provides integration with Google Cloud Storage, offering
    enterprise-grade cloud storage with features like:
    
    - Multi-regional and dual-regional storage options
    - Nearline, Coldline, and Archive storage classes
    - Cloud CDN integration for global content delivery
    - IAM-based access control with fine-grained permissions
    - Object lifecycle management
    - Integration with Google AI/ML services
    - Seamless Google Workspace integration
    
    Attributes:
        storage_client: Google Cloud Storage client instance
        bucket: GCS Bucket instance
        
    Example:
        ```python
        # Using service account key file
        config = StorageConfig(
            access_key="/path/to/service-account.json",
            secret_key="",  # Not used with service account
            bucket_name="my-email-attachments",
            region="us-central1"
        )
        
        # Or using service account JSON string
        config = StorageConfig(
            access_key='{"type": "service_account", ...}',
            secret_key="",
            bucket_name="my-email-attachments"
        )
        
        connector = GCSConnector("gcs", config)
        
        async with connector:
            # Upload with Nearline storage class
            storage_obj = await connector.upload_attachment(
                attachment,
                metadata={"storage_class": "NEARLINE"}
            )
            
            # Generate signed URL for secure access
            download_url = await connector.generate_presigned_url(
                storage_obj.key,
                expires_in=3600
            )
        ```
        
    Note:
        Requires the 'google-cloud-storage' package to be installed:
        pip install google-cloud-storage
    """
    
    def __init__(self, name: str, config: Union[StorageConfig, Dict[str, Any]]):
        """
        Initialize Google Cloud Storage connector.
        
        Args:
            name: Unique identifier for this connector
            config: GCS configuration
            
        Raises:
            ImportError: If google-cloud-storage package is not installed
        """
        if not GCS_AVAILABLE:
            raise ImportError(
                "Google Cloud Storage connector requires 'google-cloud-storage' package. "
                "Install with: pip install google-cloud-storage"
            )
        
        super().__init__(name, config)
        self.storage_client: Optional[storage.Client] = None
        self.bucket: Optional[Bucket] = None
        self.credentials = None
    
    async def _validate_config(self) -> None:
        """Validate Google Cloud Storage configuration."""
        if not self.config.bucket_name:
            raise ConfigurationError("GCS bucket name is required")
        
        if not self.config.access_key:
            raise ConfigurationError(
                "GCS service account key file path or JSON string is required in access_key"
            )
        
        # Validate service account credentials
        try:
            if self.config.access_key.startswith("{"):
                # JSON string format
                credentials_info = json.loads(self.config.access_key)
                self.credentials = service_account.Credentials.from_service_account_info(
                    credentials_info
                )
            else:
                # File path format
                self.credentials = service_account.Credentials.from_service_account_file(
                    self.config.access_key
                )
        except (json.JSONDecodeError, FileNotFoundError, KeyError) as e:
            raise ConfigurationError(f"Invalid GCS service account credentials: {e}")
    
    async def _initialize_client(self) -> None:
        """Initialize Google Cloud Storage client."""
        try:
            # Create storage client with credentials
            if self.credentials:
                self.storage_client = storage.Client(credentials=self.credentials)
            else:
                # Use default credentials (from environment)
                self.storage_client = storage.Client()
            
            # Get bucket reference
            self.bucket = self.storage_client.bucket(self.config.bucket_name)
            
            self.logger.debug("Google Cloud Storage client initialized")
            
        except DefaultCredentialsError:
            raise ConnectionError("GCS credentials not found - check service account setup")
        except Exception as e:
            raise ConnectionError(f"Failed to initialize GCS client: {e}")
    
    async def _cleanup_client(self) -> None:
        """Cleanup Google Cloud Storage client."""
        try:
            if self.storage_client:
                self.storage_client.close()
        except Exception as e:
            self.logger.error(f"Error during GCS client cleanup: {e}")
        finally:
            self.storage_client = None
            self.bucket = None
    
    async def _test_connection(self) -> None:
        """Test Google Cloud Storage connection."""
        try:
            loop = asyncio.get_event_loop()
            
            # Test connection by listing buckets
            buckets = await loop.run_in_executor(
                None, list, self.storage_client.list_buckets()
            )
            
            self.logger.debug(f"GCS connection test successful. Found {len(buckets)} buckets")
            
        except Forbidden:
            raise ConnectionError("GCS access denied - check service account permissions")
        except Exception as e:
            raise ConnectionError(f"GCS connection test failed: {e}")
    
    async def _ensure_bucket_exists(self) -> None:
        """Ensure Google Cloud Storage bucket exists."""
        try:
            loop = asyncio.get_event_loop()
            
            # Check if bucket exists
            try:
                await loop.run_in_executor(None, self.bucket.reload)
                self.logger.debug(f"GCS bucket exists: {self.config.bucket_name}")
                
            except NotFound:
                # Bucket doesn't exist, create it
                location = self.config.region or "US"
                
                await loop.run_in_executor(
                    None,
                    self.storage_client.create_bucket,
                    self.bucket,
                    location=location
                )
                
                self.logger.info(f"Created GCS bucket: {self.config.bucket_name}")
                
        except Exception as e:
            raise StorageError(f"Failed to ensure bucket exists: {e}")
    
    async def _upload_object(
        self,
        key: str,
        content: bytes,
        content_type: str,
        metadata: Dict[str, str]
    ) -> StorageObject:
        """Upload object to Google Cloud Storage."""
        try:
            loop = asyncio.get_event_loop()
            
            # Create blob
            blob = self.bucket.blob(key)
            
            # Set content type
            blob.content_type = content_type
            
            # Set metadata
            blob.metadata = metadata
            
            # Set storage class if specified
            if 'storage_class' in metadata:
                blob.storage_class = metadata['storage_class']
            
            # Upload content
            await loop.run_in_executor(
                None, blob.upload_from_string, content, content_type
            )
            
            # Reload to get updated properties
            await loop.run_in_executor(None, blob.reload)
            
            return StorageObject(
                key=key,
                bucket=self.config.bucket_name,
                size=blob.size,
                content_type=blob.content_type,
                etag=blob.etag,
                last_modified=blob.updated,
                metadata=blob.metadata or {}
            )
            
        except Exception as e:
            raise StorageError(f"GCS upload failed: {e}")
    
    async def _download_object(self, key: str) -> bytes:
        """Download object from Google Cloud Storage."""
        try:
            loop = asyncio.get_event_loop()
            
            # Get blob
            blob = self.bucket.blob(key)
            
            # Download content
            content = await loop.run_in_executor(None, blob.download_as_bytes)
            
            return content
            
        except NotFound:
            raise StorageError(f"Object not found: {key}")
        except Exception as e:
            raise StorageError(f"GCS download failed: {e}")
    
    async def _delete_object(self, key: str) -> bool:
        """Delete object from Google Cloud Storage."""
        try:
            loop = asyncio.get_event_loop()
            
            # Get blob
            blob = self.bucket.blob(key)
            
            # Delete blob
            await loop.run_in_executor(None, blob.delete)
            
            return True
            
        except NotFound:
            self.logger.warning(f"Object not found for deletion: {key}")
            return False
        except Exception as e:
            raise StorageError(f"GCS deletion failed: {e}")
    
    async def _generate_presigned_url_impl(
        self,
        key: str,
        expires_in: int,
        method: str
    ) -> str:
        """Generate signed URL for Google Cloud Storage object."""
        try:
            loop = asyncio.get_event_loop()
            
            # Get blob
            blob = self.bucket.blob(key)
            
            # Calculate expiration
            expiration = datetime.utcnow() + timedelta(seconds=expires_in)
            
            # Generate signed URL
            url = await loop.run_in_executor(
                None,
                blob.generate_signed_url,
                expiration,
                method=method.upper(),
                version="v4"
            )
            
            return url
            
        except Exception as e:
            raise StorageError(f"GCS signed URL generation failed: {e}")
    
    async def _list_objects(self, prefix: str, limit: int) -> List[StorageObject]:
        """List objects in Google Cloud Storage bucket."""
        try:
            loop = asyncio.get_event_loop()
            
            # List blobs with prefix
            blobs = await loop.run_in_executor(
                None,
                lambda: list(self.storage_client.list_blobs(
                    self.bucket,
                    prefix=prefix,
                    max_results=limit
                ))
            )
            
            storage_objects = []
            for blob in blobs:
                storage_obj = StorageObject(
                    key=blob.name,
                    bucket=self.config.bucket_name,
                    size=blob.size,
                    content_type=blob.content_type or 'application/octet-stream',
                    etag=blob.etag,
                    last_modified=blob.updated,
                    metadata=blob.metadata or {}
                )
                storage_objects.append(storage_obj)
            
            return storage_objects
            
        except Exception as e:
            raise StorageError(f"GCS list operation failed: {e}")
    
    async def set_object_lifecycle(self, max_age_days: int = 365) -> bool:
        """
        Set object lifecycle policy for automatic deletion.
        
        Args:
            max_age_days: Maximum age in days before objects are deleted
            
        Returns:
            True if lifecycle policy was set successfully
        """
        try:
            loop = asyncio.get_event_loop()
            
            # Define lifecycle rule
            rule = {
                "action": {"type": "Delete"},
                "condition": {"age": max_age_days}
            }
            
            # Set lifecycle policy
            await loop.run_in_executor(
                None,
                setattr,
                self.bucket,
                'lifecycle_rules',
                [rule]
            )
            
            await loop.run_in_executor(None, self.bucket.patch)
            
            self.logger.info(f"Set lifecycle policy for bucket: {self.config.bucket_name}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to set lifecycle policy: {e}")
            return False
    
    async def enable_uniform_bucket_access(self) -> bool:
        """
        Enable uniform bucket-level access (recommended for security).
        
        Returns:
            True if uniform access was enabled successfully
        """
        try:
            loop = asyncio.get_event_loop()
            
            # Enable uniform bucket-level access
            await loop.run_in_executor(
                None,
                setattr,
                self.bucket,
                'iam_configuration',
                {"uniform_bucket_level_access_enabled": True}
            )
            
            await loop.run_in_executor(None, self.bucket.patch)
            
            self.logger.info(f"Enabled uniform access for bucket: {self.config.bucket_name}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to enable uniform access: {e}")
            return False
    
    async def get_bucket_info(self) -> Dict[str, Any]:
        """
        Get information about the Google Cloud Storage bucket.
        
        Returns:
            Dictionary containing bucket information
        """
        try:
            loop = asyncio.get_event_loop()
            
            # Reload bucket to get latest info
            await loop.run_in_executor(None, self.bucket.reload)
            
            # Count objects (limited to avoid performance issues)
            blobs = await loop.run_in_executor(
                None,
                lambda: list(self.storage_client.list_blobs(
                    self.bucket,
                    max_results=1000
                ))
            )
            
            total_size = sum(blob.size for blob in blobs if blob.size)
            
            return {
                "bucket_name": self.config.bucket_name,
                "location": self.bucket.location,
                "storage_class": self.bucket.storage_class,
                "created": self.bucket.time_created,
                "updated": self.bucket.updated,
                "object_count": len(blobs),
                "total_size": total_size,
                "versioning_enabled": self.bucket.versioning_enabled,
                "uniform_access": getattr(
                    self.bucket.iam_configuration, 
                    'uniform_bucket_level_access_enabled', 
                    False
                ),
            }
            
        except Exception as e:
            self.logger.error(f"Failed to get bucket info: {e}")
            return {
                "bucket_name": self.config.bucket_name,
                "error": str(e)
            }
    
    def get_status(self) -> Dict[str, Any]:
        """Get Google Cloud Storage connector status."""
        status = super().get_status()
        status.update({
            "storage_type": "Google Cloud Storage",
            "project_id": getattr(self.credentials, 'project_id', None) if self.credentials else None,
            "supports_lifecycle": True,
            "supports_versioning": True,
        })
        return status
