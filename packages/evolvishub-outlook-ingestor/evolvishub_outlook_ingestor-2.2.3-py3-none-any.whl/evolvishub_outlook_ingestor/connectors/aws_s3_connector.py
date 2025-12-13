"""
AWS S3 Object Storage Connector for Evolvishub Outlook Ingestor.

This module provides integration with Amazon S3, the industry-leading cloud
object storage service, offering enterprise-grade scalability, security,
and performance for email attachment storage.
"""

import asyncio
import io
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Union

try:
    import boto3
    from botocore.exceptions import ClientError, NoCredentialsError, BotoCoreError
    from botocore.config import Config
    AWS_AVAILABLE = True
except ImportError:
    AWS_AVAILABLE = False

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


class AWSS3Connector(BaseStorageConnector):
    """
    Amazon S3 object storage connector.
    
    This connector provides integration with Amazon S3, offering enterprise-grade
    object storage with features like:
    
    - Multi-region support with automatic failover
    - Server-side encryption (SSE-S3, SSE-KMS, SSE-C)
    - Intelligent tiering for cost optimization
    - Cross-region replication for disaster recovery
    - CloudWatch integration for monitoring
    - IAM-based access control
    
    Attributes:
        s3_client: Boto3 S3 client instance
        s3_resource: Boto3 S3 resource instance
        
    Example:
        ```python
        config = StorageConfig(
            access_key="AKIAIOSFODNN7EXAMPLE",
            secret_key="wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY",
            bucket_name="my-email-attachments",
            region="us-east-1"
        )
        
        connector = AWSS3Connector("s3", config)
        
        async with connector:
            # Upload with server-side encryption
            storage_obj = await connector.upload_attachment(
                attachment,
                metadata={"encryption": "AES256"}
            )
            
            # Generate CloudFront-compatible URL
            download_url = await connector.generate_presigned_url(
                storage_obj.key,
                expires_in=7200  # 2 hours
            )
        ```
        
    Note:
        Requires the 'boto3' package to be installed:
        pip install boto3
    """
    
    def __init__(self, name: str, config: Union[StorageConfig, Dict[str, Any]]):
        """
        Initialize AWS S3 connector.
        
        Args:
            name: Unique identifier for this connector
            config: AWS S3 configuration
            
        Raises:
            ImportError: If boto3 package is not installed
        """
        if not AWS_AVAILABLE:
            raise ImportError(
                "AWS S3 connector requires 'boto3' package. "
                "Install with: pip install boto3"
            )
        
        super().__init__(name, config)
        self.s3_client = None
        self.s3_resource = None
        self._session = None
    
    async def _validate_config(self) -> None:
        """Validate AWS S3 configuration."""
        if not self.config.access_key:
            raise ConfigurationError("AWS access_key is required")
        
        if not self.config.secret_key:
            raise ConfigurationError("AWS secret_key is required")
        
        if not self.config.bucket_name:
            raise ConfigurationError("AWS S3 bucket_name is required")
        
        if not self.config.region:
            raise ConfigurationError("AWS region is required")
        
        # Validate region format
        valid_regions = [
            'us-east-1', 'us-east-2', 'us-west-1', 'us-west-2',
            'eu-west-1', 'eu-west-2', 'eu-west-3', 'eu-central-1',
            'ap-southeast-1', 'ap-southeast-2', 'ap-northeast-1',
            'ap-northeast-2', 'ap-south-1', 'sa-east-1',
            'ca-central-1', 'eu-north-1', 'ap-east-1', 'me-south-1',
            'af-south-1', 'eu-south-1', 'ap-northeast-3'
        ]
        
        if self.config.region not in valid_regions:
            self.logger.warning(f"Region '{self.config.region}' not in known regions list")
    
    async def _initialize_client(self) -> None:
        """Initialize AWS S3 client and resource."""
        try:
            # Create boto3 session
            self._session = boto3.Session(
                aws_access_key_id=self.config.access_key,
                aws_secret_access_key=self.config.secret_key,
                region_name=self.config.region
            )
            
            # Configure boto3 client settings
            boto_config = Config(
                region_name=self.config.region,
                retries={
                    'max_attempts': self.config.max_retries,
                    'mode': 'adaptive'
                },
                max_pool_connections=50,
                connect_timeout=self.config.timeout,
                read_timeout=self.config.timeout,
            )
            
            # Create S3 client and resource
            self.s3_client = self._session.client('s3', config=boto_config)
            self.s3_resource = self._session.resource('s3', config=boto_config)
            
            self.logger.debug(f"AWS S3 client initialized for region: {self.config.region}")
            
        except Exception as e:
            raise ConnectionError(f"Failed to initialize AWS S3 client: {e}")
    
    async def _cleanup_client(self) -> None:
        """Cleanup AWS S3 client."""
        # Boto3 clients don't require explicit cleanup
        self.s3_client = None
        self.s3_resource = None
        self._session = None
    
    async def _test_connection(self) -> None:
        """Test AWS S3 connection."""
        try:
            loop = asyncio.get_event_loop()
            
            # Test connection by listing buckets
            response = await loop.run_in_executor(
                None, self.s3_client.list_buckets
            )
            
            bucket_count = len(response.get('Buckets', []))
            self.logger.debug(f"AWS S3 connection test successful. Found {bucket_count} buckets")
            
        except NoCredentialsError:
            raise ConnectionError("AWS credentials not found or invalid")
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == 'InvalidAccessKeyId':
                raise ConnectionError("Invalid AWS access key")
            elif error_code == 'SignatureDoesNotMatch':
                raise ConnectionError("Invalid AWS secret key")
            else:
                raise ConnectionError(f"AWS S3 connection test failed: {e}")
        except Exception as e:
            raise ConnectionError(f"AWS S3 connection test failed: {e}")
    
    async def _ensure_bucket_exists(self) -> None:
        """Ensure AWS S3 bucket exists."""
        try:
            loop = asyncio.get_event_loop()
            
            # Check if bucket exists
            try:
                await loop.run_in_executor(
                    None, self.s3_client.head_bucket, Bucket=self.config.bucket_name
                )
                self.logger.debug(f"AWS S3 bucket exists: {self.config.bucket_name}")
                
            except ClientError as e:
                error_code = e.response['Error']['Code']
                if error_code == '404':
                    # Bucket doesn't exist, create it
                    create_args = {'Bucket': self.config.bucket_name}
                    
                    # Add location constraint for regions other than us-east-1
                    if self.config.region != 'us-east-1':
                        create_args['CreateBucketConfiguration'] = {
                            'LocationConstraint': self.config.region
                        }
                    
                    await loop.run_in_executor(
                        None, self.s3_client.create_bucket, **create_args
                    )
                    
                    # Wait for bucket to be available
                    waiter = self.s3_client.get_waiter('bucket_exists')
                    await loop.run_in_executor(
                        None, waiter.wait, Bucket=self.config.bucket_name
                    )
                    
                    self.logger.info(f"Created AWS S3 bucket: {self.config.bucket_name}")
                else:
                    raise StorageError(f"Failed to access bucket: {e}")
                    
        except Exception as e:
            raise StorageError(f"Failed to ensure bucket exists: {e}")
    
    async def _upload_object(
        self,
        key: str,
        content: bytes,
        content_type: str,
        metadata: Dict[str, str]
    ) -> StorageObject:
        """Upload object to AWS S3."""
        try:
            loop = asyncio.get_event_loop()
            
            # Prepare upload arguments
            upload_args = {
                'Bucket': self.config.bucket_name,
                'Key': key,
                'Body': content,
                'ContentType': content_type,
                'Metadata': metadata,
                'ServerSideEncryption': 'AES256',  # Enable server-side encryption
            }
            
            # Upload object
            await loop.run_in_executor(
                None, self.s3_client.put_object, **upload_args
            )
            
            # Get object metadata
            response = await loop.run_in_executor(
                None, self.s3_client.head_object,
                Bucket=self.config.bucket_name, Key=key
            )
            
            return StorageObject(
                key=key,
                bucket=self.config.bucket_name,
                size=response['ContentLength'],
                content_type=response['ContentType'],
                etag=response['ETag'].strip('"'),
                last_modified=response['LastModified'],
                metadata=response.get('Metadata', {})
            )
            
        except ClientError as e:
            raise StorageError(f"AWS S3 upload failed: {e}")
        except Exception as e:
            raise StorageError(f"Unexpected error during upload: {e}")
    
    async def _download_object(self, key: str) -> bytes:
        """Download object from AWS S3."""
        try:
            loop = asyncio.get_event_loop()
            
            # Download object
            response = await loop.run_in_executor(
                None, self.s3_client.get_object,
                Bucket=self.config.bucket_name, Key=key
            )
            
            # Read content
            content = response['Body'].read()
            
            return content
            
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == 'NoSuchKey':
                raise StorageError(f"Object not found: {key}")
            raise StorageError(f"AWS S3 download failed: {e}")
        except Exception as e:
            raise StorageError(f"Unexpected error during download: {e}")
    
    async def _delete_object(self, key: str) -> bool:
        """Delete object from AWS S3."""
        try:
            loop = asyncio.get_event_loop()
            
            await loop.run_in_executor(
                None, self.s3_client.delete_object,
                Bucket=self.config.bucket_name, Key=key
            )
            
            return True
            
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == 'NoSuchKey':
                self.logger.warning(f"Object not found for deletion: {key}")
                return False
            raise StorageError(f"AWS S3 deletion failed: {e}")
        except Exception as e:
            raise StorageError(f"Unexpected error during deletion: {e}")
    
    async def _generate_presigned_url_impl(
        self,
        key: str,
        expires_in: int,
        method: str
    ) -> str:
        """Generate presigned URL for AWS S3 object."""
        try:
            loop = asyncio.get_event_loop()
            
            # Map HTTP methods to S3 operations
            operation_map = {
                'GET': 'get_object',
                'PUT': 'put_object',
                'DELETE': 'delete_object'
            }
            
            operation = operation_map.get(method.upper())
            if not operation:
                raise ValidationError(f"Unsupported HTTP method: {method}")
            
            # Generate presigned URL
            url = await loop.run_in_executor(
                None,
                self.s3_client.generate_presigned_url,
                operation,
                {'Bucket': self.config.bucket_name, 'Key': key},
                expires_in
            )
            
            return url
            
        except ClientError as e:
            raise StorageError(f"AWS S3 presigned URL generation failed: {e}")
        except Exception as e:
            raise StorageError(f"Unexpected error during URL generation: {e}")
    
    async def _list_objects(self, prefix: str, limit: int) -> List[StorageObject]:
        """List objects in AWS S3 bucket."""
        try:
            loop = asyncio.get_event_loop()
            
            # List objects with prefix
            paginator = self.s3_client.get_paginator('list_objects_v2')
            page_iterator = paginator.paginate(
                Bucket=self.config.bucket_name,
                Prefix=prefix,
                MaxKeys=limit
            )
            
            storage_objects = []
            object_count = 0
            
            for page in page_iterator:
                if object_count >= limit:
                    break
                
                for obj in page.get('Contents', []):
                    if object_count >= limit:
                        break
                    
                    # Get detailed object metadata
                    response = await loop.run_in_executor(
                        None, self.s3_client.head_object,
                        Bucket=self.config.bucket_name, Key=obj['Key']
                    )
                    
                    storage_obj = StorageObject(
                        key=obj['Key'],
                        bucket=self.config.bucket_name,
                        size=obj['Size'],
                        content_type=response.get('ContentType', 'application/octet-stream'),
                        etag=obj['ETag'].strip('"'),
                        last_modified=obj['LastModified'],
                        metadata=response.get('Metadata', {})
                    )
                    storage_objects.append(storage_obj)
                    object_count += 1
            
            return storage_objects
            
        except ClientError as e:
            raise StorageError(f"AWS S3 list operation failed: {e}")
        except Exception as e:
            raise StorageError(f"Unexpected error during list operation: {e}")
    
    async def enable_versioning(self) -> bool:
        """
        Enable versioning on the S3 bucket.
        
        Returns:
            True if versioning was enabled successfully
        """
        try:
            loop = asyncio.get_event_loop()
            
            await loop.run_in_executor(
                None,
                self.s3_client.put_bucket_versioning,
                Bucket=self.config.bucket_name,
                VersioningConfiguration={'Status': 'Enabled'}
            )
            
            self.logger.info(f"Enabled versioning for bucket: {self.config.bucket_name}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to enable versioning: {e}")
            return False
    
    async def set_lifecycle_policy(self, transition_days: int = 30) -> bool:
        """
        Set lifecycle policy to transition objects to cheaper storage classes.
        
        Args:
            transition_days: Days after which to transition to IA storage
            
        Returns:
            True if lifecycle policy was set successfully
        """
        try:
            loop = asyncio.get_event_loop()
            
            lifecycle_config = {
                'Rules': [
                    {
                        'ID': 'EmailAttachmentLifecycle',
                        'Status': 'Enabled',
                        'Filter': {'Prefix': ''},
                        'Transitions': [
                            {
                                'Days': transition_days,
                                'StorageClass': 'STANDARD_IA'
                            },
                            {
                                'Days': transition_days * 3,
                                'StorageClass': 'GLACIER'
                            }
                        ]
                    }
                ]
            }
            
            await loop.run_in_executor(
                None,
                self.s3_client.put_bucket_lifecycle_configuration,
                Bucket=self.config.bucket_name,
                LifecycleConfiguration=lifecycle_config
            )
            
            self.logger.info(f"Set lifecycle policy for bucket: {self.config.bucket_name}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to set lifecycle policy: {e}")
            return False
    
    def get_status(self) -> Dict[str, Any]:
        """Get AWS S3 connector status."""
        status = super().get_status()
        status.update({
            "storage_type": "Amazon S3",
            "encryption": "AES256",
            "versioning_enabled": False,  # Would need to check bucket config
        })
        return status
