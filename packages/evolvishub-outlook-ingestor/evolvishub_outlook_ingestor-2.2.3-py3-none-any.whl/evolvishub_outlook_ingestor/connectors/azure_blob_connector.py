"""
Azure Blob Storage Connector for Evolvishub Outlook Ingestor.

This module provides integration with Microsoft Azure Blob Storage, offering
enterprise-grade cloud storage with seamless integration into Microsoft 365
and Azure ecosystems.
"""

import asyncio
import io
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Union
from urllib.parse import urlparse

try:
    from azure.storage.blob.aio import BlobServiceClient, ContainerClient, BlobClient
    from azure.storage.blob import BlobSasPermissions, generate_blob_sas
    from azure.core.exceptions import (
        ResourceNotFoundError,
        ResourceExistsError,
        ClientAuthenticationError,
        HttpResponseError
    )
    AZURE_AVAILABLE = True
except ImportError:
    AZURE_AVAILABLE = False

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


class AzureBlobConnector(BaseStorageConnector):
    """
    Microsoft Azure Blob Storage connector.
    
    This connector provides integration with Azure Blob Storage, offering
    enterprise-grade cloud storage with features like:
    
    - Hot, Cool, and Archive storage tiers for cost optimization
    - Azure Active Directory integration
    - Geo-redundant storage options
    - Azure CDN integration for global content delivery
    - Advanced threat protection and encryption
    - Seamless integration with Microsoft 365 and Azure services
    
    Attributes:
        blob_service_client: Azure BlobServiceClient instance
        container_client: Azure ContainerClient instance
        
    Example:
        ```python
        config = StorageConfig(
            # Using connection string
            access_key="DefaultEndpointsProtocol=https;AccountName=...",
            secret_key="",  # Not used with connection string
            bucket_name="email-attachments",
            
            # Or using account key
            # access_key="storage_account_name",
            # secret_key="storage_account_key",
        )
        
        connector = AzureBlobConnector("azure", config)
        
        async with connector:
            # Upload with cool tier for cost savings
            storage_obj = await connector.upload_attachment(
                attachment,
                metadata={"tier": "Cool"}
            )
            
            # Generate SAS URL for secure access
            download_url = await connector.generate_presigned_url(
                storage_obj.key,
                expires_in=3600
            )
        ```
        
    Note:
        Requires the 'azure-storage-blob' package to be installed:
        pip install azure-storage-blob
    """
    
    def __init__(self, name: str, config: Union[StorageConfig, Dict[str, Any]]):
        """
        Initialize Azure Blob Storage connector.
        
        Args:
            name: Unique identifier for this connector
            config: Azure Blob Storage configuration
            
        Raises:
            ImportError: If azure-storage-blob package is not installed
        """
        if not AZURE_AVAILABLE:
            raise ImportError(
                "Azure Blob Storage connector requires 'azure-storage-blob' package. "
                "Install with: pip install azure-storage-blob"
            )
        
        super().__init__(name, config)
        self.blob_service_client: Optional[BlobServiceClient] = None
        self.container_client: Optional[ContainerClient] = None
        self.account_name: Optional[str] = None
        self.account_key: Optional[str] = None
    
    async def _validate_config(self) -> None:
        """Validate Azure Blob Storage configuration."""
        if not self.config.bucket_name:
            raise ConfigurationError("Azure container name (bucket_name) is required")
        
        # Check if using connection string or account key authentication
        if self.config.access_key.startswith("DefaultEndpointsProtocol"):
            # Connection string format
            self.logger.debug("Using Azure connection string authentication")
        else:
            # Account name + key format
            if not self.config.access_key:
                raise ConfigurationError("Azure storage account name (access_key) is required")
            
            if not self.config.secret_key:
                raise ConfigurationError("Azure storage account key (secret_key) is required")
            
            self.account_name = self.config.access_key
            self.account_key = self.config.secret_key
    
    async def _initialize_client(self) -> None:
        """Initialize Azure Blob Storage client."""
        try:
            if self.config.access_key.startswith("DefaultEndpointsProtocol"):
                # Initialize with connection string
                self.blob_service_client = BlobServiceClient.from_connection_string(
                    self.config.access_key
                )
            else:
                # Initialize with account name and key
                account_url = f"https://{self.account_name}.blob.core.windows.net"
                self.blob_service_client = BlobServiceClient(
                    account_url=account_url,
                    credential=self.account_key
                )
            
            # Get container client
            self.container_client = self.blob_service_client.get_container_client(
                self.config.bucket_name
            )
            
            self.logger.debug("Azure Blob Storage client initialized")
            
        except Exception as e:
            raise ConnectionError(f"Failed to initialize Azure Blob Storage client: {e}")
    
    async def _cleanup_client(self) -> None:
        """Cleanup Azure Blob Storage client."""
        try:
            if self.container_client:
                await self.container_client.close()
            if self.blob_service_client:
                await self.blob_service_client.close()
        except Exception as e:
            self.logger.error(f"Error during Azure client cleanup: {e}")
        finally:
            self.container_client = None
            self.blob_service_client = None
    
    async def _test_connection(self) -> None:
        """Test Azure Blob Storage connection."""
        try:
            # Test connection by getting account information
            account_info = await self.blob_service_client.get_account_information()
            self.logger.debug(f"Azure connection test successful. Account type: {account_info.get('account_kind')}")
            
        except ClientAuthenticationError:
            raise ConnectionError("Azure authentication failed - check credentials")
        except Exception as e:
            raise ConnectionError(f"Azure Blob Storage connection test failed: {e}")
    
    async def _ensure_bucket_exists(self) -> None:
        """Ensure Azure container exists."""
        try:
            # Check if container exists
            try:
                await self.container_client.get_container_properties()
                self.logger.debug(f"Azure container exists: {self.config.bucket_name}")
                
            except ResourceNotFoundError:
                # Container doesn't exist, create it
                await self.container_client.create_container()
                self.logger.info(f"Created Azure container: {self.config.bucket_name}")
                
        except ResourceExistsError:
            # Container already exists (race condition)
            self.logger.debug(f"Azure container already exists: {self.config.bucket_name}")
        except Exception as e:
            raise StorageError(f"Failed to ensure container exists: {e}")
    
    async def _upload_object(
        self,
        key: str,
        content: bytes,
        content_type: str,
        metadata: Dict[str, str]
    ) -> StorageObject:
        """Upload object to Azure Blob Storage."""
        try:
            # Get blob client
            blob_client = self.container_client.get_blob_client(key)
            
            # Prepare upload arguments
            upload_args = {
                'data': content,
                'content_type': content_type,
                'metadata': metadata,
                'overwrite': True
            }
            
            # Set storage tier if specified in metadata
            if 'tier' in metadata:
                upload_args['standard_blob_tier'] = metadata['tier']
            
            # Upload blob
            await blob_client.upload_blob(**upload_args)
            
            # Get blob properties
            properties = await blob_client.get_blob_properties()
            
            return StorageObject(
                key=key,
                bucket=self.config.bucket_name,
                size=properties.size,
                content_type=properties.content_settings.content_type,
                etag=properties.etag.strip('"'),
                last_modified=properties.last_modified,
                metadata=properties.metadata or {}
            )
            
        except Exception as e:
            raise StorageError(f"Azure Blob upload failed: {e}")
    
    async def _download_object(self, key: str) -> bytes:
        """Download object from Azure Blob Storage."""
        try:
            # Get blob client
            blob_client = self.container_client.get_blob_client(key)
            
            # Download blob
            download_stream = await blob_client.download_blob()
            content = await download_stream.readall()
            
            return content
            
        except ResourceNotFoundError:
            raise StorageError(f"Object not found: {key}")
        except Exception as e:
            raise StorageError(f"Azure Blob download failed: {e}")
    
    async def _delete_object(self, key: str) -> bool:
        """Delete object from Azure Blob Storage."""
        try:
            # Get blob client
            blob_client = self.container_client.get_blob_client(key)
            
            # Delete blob
            await blob_client.delete_blob()
            
            return True
            
        except ResourceNotFoundError:
            self.logger.warning(f"Object not found for deletion: {key}")
            return False
        except Exception as e:
            raise StorageError(f"Azure Blob deletion failed: {e}")
    
    async def _generate_presigned_url_impl(
        self,
        key: str,
        expires_in: int,
        method: str
    ) -> str:
        """Generate SAS URL for Azure Blob object."""
        try:
            # Calculate expiry time
            expiry = datetime.utcnow() + timedelta(seconds=expires_in)
            
            # Set permissions based on method
            if method.upper() == "GET":
                permissions = BlobSasPermissions(read=True)
            elif method.upper() == "PUT":
                permissions = BlobSasPermissions(write=True, create=True)
            elif method.upper() == "DELETE":
                permissions = BlobSasPermissions(delete=True)
            else:
                raise ValidationError(f"Unsupported HTTP method: {method}")
            
            # Generate SAS token
            if self.account_name and self.account_key:
                # Using account key
                sas_token = generate_blob_sas(
                    account_name=self.account_name,
                    container_name=self.config.bucket_name,
                    blob_name=key,
                    account_key=self.account_key,
                    permission=permissions,
                    expiry=expiry
                )
                
                # Construct URL
                url = f"https://{self.account_name}.blob.core.windows.net/{self.config.bucket_name}/{key}?{sas_token}"
            else:
                # Using connection string - need to extract account info
                blob_client = self.container_client.get_blob_client(key)
                url = blob_client.url + "?" + generate_blob_sas(
                    account_name=blob_client.account_name,
                    container_name=self.config.bucket_name,
                    blob_name=key,
                    account_key=self.account_key or "",  # This might not work with connection string
                    permission=permissions,
                    expiry=expiry
                )
            
            return url
            
        except Exception as e:
            raise StorageError(f"Azure SAS URL generation failed: {e}")
    
    async def _list_objects(self, prefix: str, limit: int) -> List[StorageObject]:
        """List objects in Azure container."""
        try:
            storage_objects = []
            count = 0
            
            # List blobs with prefix
            async for blob in self.container_client.list_blobs(name_starts_with=prefix):
                if count >= limit:
                    break
                
                # Get detailed blob properties
                blob_client = self.container_client.get_blob_client(blob.name)
                properties = await blob_client.get_blob_properties()
                
                storage_obj = StorageObject(
                    key=blob.name,
                    bucket=self.config.bucket_name,
                    size=blob.size,
                    content_type=properties.content_settings.content_type or 'application/octet-stream',
                    etag=blob.etag.strip('"'),
                    last_modified=blob.last_modified,
                    metadata=properties.metadata or {}
                )
                storage_objects.append(storage_obj)
                count += 1
            
            return storage_objects
            
        except Exception as e:
            raise StorageError(f"Azure Blob list operation failed: {e}")
    
    async def set_blob_tier(self, key: str, tier: str) -> bool:
        """
        Set the storage tier for a blob.
        
        Args:
            key: Blob key/name
            tier: Storage tier ('Hot', 'Cool', 'Archive')
            
        Returns:
            True if tier was set successfully
        """
        try:
            blob_client = self.container_client.get_blob_client(key)
            await blob_client.set_standard_blob_tier(tier)
            
            self.logger.info(f"Set blob {key} to {tier} tier")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to set blob tier: {e}")
            return False
    
    async def get_container_info(self) -> Dict[str, Any]:
        """
        Get information about the Azure container.
        
        Returns:
            Dictionary containing container information
        """
        try:
            # Get container properties
            properties = await self.container_client.get_container_properties()
            
            # Count blobs (limited to avoid performance issues)
            blob_count = 0
            total_size = 0
            
            async for blob in self.container_client.list_blobs():
                blob_count += 1
                total_size += blob.size
                if blob_count >= 1000:  # Limit for performance
                    break
            
            return {
                "container_name": self.config.bucket_name,
                "last_modified": properties.last_modified,
                "etag": properties.etag,
                "blob_count": blob_count,
                "total_size": total_size,
                "public_access": properties.public_access,
            }
            
        except Exception as e:
            self.logger.error(f"Failed to get container info: {e}")
            return {
                "container_name": self.config.bucket_name,
                "error": str(e)
            }
    
    def get_status(self) -> Dict[str, Any]:
        """Get Azure Blob Storage connector status."""
        status = super().get_status()
        status.update({
            "storage_type": "Azure Blob Storage",
            "account_name": self.account_name,
            "supports_tiers": True,
        })
        return status
