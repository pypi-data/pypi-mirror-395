# 🗄️ **Storage Architecture - Evolvishub Outlook Ingestor**

## **Overview**

The Evolvishub Outlook Ingestor provides a sophisticated hybrid storage architecture that combines the benefits of database storage for metadata with object storage for large attachments. This approach optimizes performance, cost, and scalability for enterprise email processing workflows.

## **🏗️ Architecture Components**

### **1. Storage Connectors**

#### **Base Storage Connector**
- Abstract base class defining the storage interface
- Provides common functionality for all storage implementations
- Handles authentication, connection management, and error handling

#### **Supported Storage Backends**

| Storage Type | Connector | Use Case | Features |
|--------------|-----------|----------|----------|
| **MinIO** | `MinIOConnector` | Self-hosted S3-compatible | High performance, on-premises control |
| **AWS S3** | `AWSS3Connector` | Cloud storage, enterprise scale | Global CDN, lifecycle policies, encryption |
| **Azure Blob** | `AzureBlobConnector` | Microsoft ecosystem integration | Hot/Cool/Archive tiers, Azure AD integration |
| **Google Cloud Storage** | `GCSConnector` | Google Workspace integration | ML integration, global infrastructure |

### **2. Enhanced Attachment Processor**

The `EnhancedAttachmentProcessor` orchestrates the hybrid storage strategy with advanced features:

- **Multi-backend routing** based on configurable rules
- **Content deduplication** using SHA256 hashes
- **Compression** for text-based attachments
- **Security scanning** integration points
- **Performance monitoring** and metrics

### **3. Storage Strategies**

#### **Database Only**
```python
strategy = StorageStrategy.DATABASE_ONLY
```
- Stores attachment content directly in the database
- Best for: Small files (<1MB), frequently accessed attachments
- Pros: Fast access, transactional consistency
- Cons: Database size growth, memory usage

#### **Storage Only**
```python
strategy = StorageStrategy.STORAGE_ONLY
```
- Stores attachments exclusively in object storage
- Best for: Large files (>5MB), archival content
- Pros: Unlimited scalability, cost-effective
- Cons: Network latency for access

#### **Hybrid**
```python
strategy = StorageStrategy.HYBRID
```
- Stores metadata in database, content in object storage
- Best for: Medium files (1-5MB), balanced access patterns
- Pros: Fast metadata queries, scalable content storage
- Cons: Complexity in retrieval logic

## **📋 Configuration**

### **Basic Configuration**

```python
from evolvishub_outlook_ingestor.processors.enhanced_attachment_processor import (
    EnhancedAttachmentProcessor,
    StorageStrategy,
    CompressionType
)

config = {
    "storage_strategy": "hybrid",
    "size_threshold": 1024 * 1024,  # 1MB
    "enable_compression": True,
    "enable_deduplication": True,
    "enable_virus_scanning": False,
    "max_attachment_size": 50 * 1024 * 1024,  # 50MB
    "default_storage_backend": "primary",
    
    # File type restrictions
    "allowed_extensions": [
        ".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx",
        ".txt", ".csv", ".json", ".xml", ".zip", ".tar", ".gz",
        ".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".svg"
    ],
    
    "blocked_extensions": [
        ".exe", ".bat", ".cmd", ".com", ".scr", ".vbs", ".js", ".jar"
    ],
    
    # Storage routing rules
    "storage_rules": [
        {
            "name": "large_files",
            "condition": "size > 5*1024*1024",
            "strategy": "storage_only",
            "storage_backend": "archive"
        },
        {
            "name": "medium_files",
            "condition": "size > 1024*1024 and size <= 5*1024*1024",
            "strategy": "hybrid",
            "storage_backend": "primary"
        },
        {
            "name": "small_files",
            "condition": "size <= 1024*1024",
            "strategy": "database_only"
        },
        {
            "name": "compressible_text",
            "condition": "content_type.startswith('text/')",
            "strategy": "hybrid",
            "storage_backend": "primary",
            "compress": True,
            "compression_type": "gzip"
        }
    ]
}
```

### **Storage Backend Configuration**

#### **MinIO Configuration**
```python
from evolvishub_outlook_ingestor.connectors.minio_connector import MinIOConnector

minio_config = {
    "endpoint_url": "localhost:9000",
    "access_key": "minioadmin",
    "secret_key": "minioadmin",
    "bucket_name": "email-attachments",
    "use_ssl": False,  # Set to True for production
    "region": "us-east-1"
}

minio_connector = MinIOConnector("minio_primary", minio_config)
```

#### **AWS S3 Configuration**
```python
from evolvishub_outlook_ingestor.connectors.aws_s3_connector import AWSS3Connector

s3_config = {
    "access_key": "AKIAIOSFODNN7EXAMPLE",
    "secret_key": "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY",
    "bucket_name": "email-attachments-prod",
    "region": "us-east-1"
}

s3_connector = AWSS3Connector("aws_s3", s3_config)
```

#### **Azure Blob Configuration**
```python
from evolvishub_outlook_ingestor.connectors.azure_blob_connector import AzureBlobConnector

azure_config = {
    "access_key": "DefaultEndpointsProtocol=https;AccountName=myaccount;AccountKey=mykey==;EndpointSuffix=core.windows.net",
    "secret_key": "",  # Not used with connection string
    "bucket_name": "email-attachments"
}

azure_connector = AzureBlobConnector("azure_blob", azure_config)
```

#### **Google Cloud Storage Configuration**
```python
from evolvishub_outlook_ingestor.connectors.gcs_connector import GCSConnector

gcs_config = {
    "access_key": "/path/to/service-account.json",  # Or JSON string
    "secret_key": "",  # Not used
    "bucket_name": "email-attachments-gcs",
    "region": "us-central1"
}

gcs_connector = GCSConnector("gcs", gcs_config)
```

## **🔄 Storage Rules Engine**

### **Rule Evaluation Context**

Storage rules are evaluated using a Python expression with the following context variables:

| Variable | Type | Description |
|----------|------|-------------|
| `size` | int | Attachment size in bytes |
| `content_type` | str | MIME content type |
| `name` | str | Original filename |
| `extension` | str | File extension (lowercase) |
| `is_inline` | bool | Whether attachment is inline |
| `attachment_type` | enum | Attachment type classification |

### **Example Rules**

```python
# Size-based routing
{
    "name": "large_files",
    "condition": "size > 10*1024*1024",  # Files > 10MB
    "strategy": "storage_only",
    "storage_backend": "cold_storage"
}

# Content-type based routing
{
    "name": "images",
    "condition": "content_type.startswith('image/')",
    "strategy": "hybrid",
    "storage_backend": "media_storage"
}

# Extension-based routing
{
    "name": "documents",
    "condition": "extension in ['.pdf', '.doc', '.docx']",
    "strategy": "hybrid",
    "storage_backend": "document_storage",
    "compress": True
}

# Complex conditions
{
    "name": "large_compressible",
    "condition": "size > 1024*1024 and content_type.startswith('text/')",
    "strategy": "storage_only",
    "storage_backend": "archive",
    "compress": True,
    "compression_type": "gzip"
}
```

## **🗜️ Compression**

### **Supported Compression Types**

- **GZIP**: Best for text files, good compression ratio
- **ZLIB**: Alternative compression, slightly faster
- **NONE**: No compression

### **Compression Strategy**

```python
# Automatic compression for text files
compressible_types = [
    "text/plain", "text/html", "text/css", "text/javascript",
    "application/json", "application/xml", "application/csv"
]

# Compression configuration
{
    "name": "compress_text",
    "condition": "content_type in compressible_types and size > 1024",
    "strategy": "hybrid",
    "compress": True,
    "compression_type": "gzip"
}
```

## **🔄 Deduplication**

### **Content-Based Deduplication**

The system uses SHA256 hashes to identify duplicate attachments:

```python
# Automatic deduplication
processor_config = {
    "enable_deduplication": True,
    # ... other config
}

# Manual deduplication check
content_hash = processor._calculate_content_hash(attachment.content)
existing_storage = await processor._check_deduplication(content_hash)

if existing_storage:
    # Use existing storage location
    return existing_storage
```

### **Deduplication Benefits**

- **Storage savings**: Eliminates duplicate file storage
- **Network efficiency**: Avoids redundant uploads
- **Processing speed**: Faster handling of duplicate content
- **Cost reduction**: Lower storage and bandwidth costs

## **🔐 Security Features**

### **Access Control**

```python
# Generate secure URLs with expiration
secure_url = await storage_connector.generate_presigned_url(
    storage_key="path/to/attachment.pdf",
    expires_in=3600,  # 1 hour
    method="GET"
)
```

### **Encryption**

- **AWS S3**: Server-side encryption (SSE-S3, SSE-KMS)
- **Azure Blob**: Encryption at rest and in transit
- **Google Cloud**: Customer-managed encryption keys (CMEK)
- **MinIO**: Server-side encryption with KMS integration

### **Virus Scanning Integration**

```python
# Placeholder for virus scanning integration
async def _scan_for_viruses(self, attachment: EmailAttachment) -> bool:
    # Integrate with ClamAV, VirusTotal, or cloud scanning service
    # Return True if clean, False if infected
    pass
```

## **📊 Monitoring and Metrics**

### **Performance Metrics**

- **Upload/download throughput**
- **Storage utilization by backend**
- **Compression ratios achieved**
- **Deduplication hit rates**
- **Processing latency**

### **Health Checks**

```python
# Storage backend health monitoring
health_status = await storage_connector.get_status()
print(f"Connected: {health_status['is_connected']}")
print(f"Storage Type: {health_status['storage_type']}")
```

## **🚀 Performance Optimization**

### **Best Practices**

1. **Size-based routing**: Route large files to object storage
2. **Compression**: Enable for text-based content
3. **Deduplication**: Reduce storage overhead
4. **Connection pooling**: Reuse connections for better performance
5. **Async operations**: Use async/await for non-blocking I/O

### **Scaling Considerations**

- **Horizontal scaling**: Multiple processor instances
- **Storage tiering**: Hot/warm/cold storage strategies
- **CDN integration**: Global content delivery
- **Caching**: Redis for metadata caching

## **🔧 Troubleshooting**

### **Common Issues**

#### **Connection Errors**
```python
# Check storage backend connectivity
try:
    await storage_connector.initialize()
except ConnectionError as e:
    print(f"Storage connection failed: {e}")
```

#### **Configuration Validation**
```python
# Validate configuration before use
try:
    await storage_connector._validate_config()
except ConfigurationError as e:
    print(f"Invalid configuration: {e}")
```

#### **Storage Quota Issues**
```python
# Monitor storage usage
bucket_info = await storage_connector.get_bucket_info()
print(f"Objects: {bucket_info['object_count']}")
print(f"Total size: {bucket_info['total_size']} bytes")
```

### **Debugging Tools**

```python
# Enable debug logging
import logging
logging.getLogger('evolvishub_outlook_ingestor').setLevel(logging.DEBUG)

# Get processor status
status = processor.get_status()
print(f"Storage backends: {status['storage_backends']}")
print(f"Cache size: {status['cache_size']}")
```

## **📈 Migration Guide**

### **Migrating from Basic to Hybrid Storage**

1. **Backup existing data**
2. **Configure storage backends**
3. **Update processor configuration**
4. **Test with small dataset**
5. **Migrate existing attachments**
6. **Monitor performance**

### **Example Migration Script**

```python
async def migrate_to_hybrid_storage():
    # Initialize new hybrid processor
    processor = EnhancedAttachmentProcessor("hybrid", hybrid_config)
    
    # Add storage backends
    await processor.add_storage_backend("primary", minio_connector)
    await processor.add_storage_backend("archive", s3_connector)
    
    # Process existing emails
    emails = await db_connector.fetch_emails_with_attachments()
    
    for email in emails:
        try:
            result = await processor.process(email)
            if result.status == ProcessingStatus.SUCCESS:
                await db_connector.update_email(email)
        except Exception as e:
            print(f"Migration failed for email {email.id}: {e}")
```

---

## **📚 Additional Resources**

- [API Reference](API_REFERENCE.md)
- [Configuration Examples](../examples/)
- [Performance Tuning Guide](PERFORMANCE_TUNING.md)
- [Security Best Practices](SECURITY.md)
