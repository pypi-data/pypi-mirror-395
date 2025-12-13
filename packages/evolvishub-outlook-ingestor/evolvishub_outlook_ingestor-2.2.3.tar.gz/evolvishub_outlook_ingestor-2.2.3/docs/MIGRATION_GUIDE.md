# 🔄 **Migration Guide - Evolvishub Outlook Ingestor**

## **Overview**

This guide helps you migrate from the basic attachment processing to the new hybrid storage architecture with enhanced attachment processing capabilities.

## **📋 Migration Checklist**

### **Pre-Migration**
- [ ] Backup existing database and attachment data
- [ ] Review current attachment storage patterns
- [ ] Plan storage backend configuration
- [ ] Test migration process in development environment
- [ ] Prepare rollback plan

### **Migration Steps**
- [ ] Install new dependencies
- [ ] Configure storage backends
- [ ] Update processor configuration
- [ ] Migrate existing attachments
- [ ] Validate data integrity
- [ ] Monitor performance

### **Post-Migration**
- [ ] Verify all attachments are accessible
- [ ] Monitor storage utilization
- [ ] Optimize storage rules based on usage patterns
- [ ] Set up lifecycle management policies

## **🚀 Step-by-Step Migration**

### **Step 1: Install New Dependencies**

```bash
# Install storage connectors
pip install evolvishub-outlook-ingestor[storage,cloud-aws,cloud-azure,cloud-gcp]

# Or install specific backends
pip install evolvishub-outlook-ingestor[storage]  # MinIO only
pip install evolvishub-outlook-ingestor[cloud-aws]  # AWS S3 only
```

### **Step 2: Configure Storage Backends**

#### **Option A: MinIO (Self-Hosted)**
```python
from evolvishub_outlook_ingestor.connectors.minio_connector import MinIOConnector

minio_config = {
    "endpoint_url": "localhost:9000",
    "access_key": "minioadmin",
    "secret_key": "minioadmin", 
    "bucket_name": "email-attachments",
    "use_ssl": False  # Set to True for production
}

minio_connector = MinIOConnector("primary_storage", minio_config)
```

#### **Option B: AWS S3**
```python
from evolvishub_outlook_ingestor.connectors.aws_s3_connector import AWSS3Connector

s3_config = {
    "access_key": "your_aws_access_key",
    "secret_key": "your_aws_secret_key",
    "bucket_name": "email-attachments-prod",
    "region": "us-east-1"
}

s3_connector = AWSS3Connector("primary_storage", s3_config)
```

#### **Option C: Azure Blob Storage**
```python
from evolvishub_outlook_ingestor.connectors.azure_blob_connector import AzureBlobConnector

azure_config = {
    "access_key": "DefaultEndpointsProtocol=https;AccountName=myaccount;AccountKey=mykey==",
    "secret_key": "",
    "bucket_name": "email-attachments"
}

azure_connector = AzureBlobConnector("primary_storage", azure_config)
```

### **Step 3: Update Processor Configuration**

#### **Before (Basic Processor)**
```python
from evolvishub_outlook_ingestor.processors.attachment_processor import AttachmentProcessor

# Old basic processor
processor = AttachmentProcessor("attachments", {
    "max_attachment_size": 50 * 1024 * 1024,
    "extract_metadata": True,
    "calculate_hashes": True
})
```

#### **After (Enhanced Processor)**
```python
from evolvishub_outlook_ingestor.processors.enhanced_attachment_processor import (
    EnhancedAttachmentProcessor,
    StorageStrategy
)

# New enhanced processor with hybrid storage
processor_config = {
    "storage_strategy": "hybrid",
    "size_threshold": 1024 * 1024,  # 1MB
    "enable_compression": True,
    "enable_deduplication": True,
    "max_attachment_size": 50 * 1024 * 1024,
    "default_storage_backend": "primary_storage",
    
    "storage_rules": [
        {
            "name": "large_files",
            "condition": "size > 5*1024*1024",  # > 5MB
            "strategy": "storage_only",
            "storage_backend": "primary_storage"
        },
        {
            "name": "medium_files", 
            "condition": "size > 1024*1024 and size <= 5*1024*1024",  # 1-5MB
            "strategy": "hybrid",
            "storage_backend": "primary_storage"
        },
        {
            "name": "small_files",
            "condition": "size <= 1024*1024",  # <= 1MB
            "strategy": "database_only"
        }
    ]
}

processor = EnhancedAttachmentProcessor("enhanced_attachments", processor_config)

# Add storage backend
await processor.add_storage_backend("primary_storage", storage_connector)
```

### **Step 4: Migration Script**

```python
import asyncio
from datetime import datetime
from typing import List

from evolvishub_outlook_ingestor.connectors.postgresql_connector import PostgreSQLConnector
from evolvishub_outlook_ingestor.processors.enhanced_attachment_processor import EnhancedAttachmentProcessor
from evolvishub_outlook_ingestor.core.data_models import EmailMessage

async def migrate_existing_attachments():
    """
    Migrate existing attachments to hybrid storage.
    """
    print("🔄 Starting attachment migration...")
    
    # Initialize database connector
    db_config = {
        "host": "localhost",
        "database": "outlook_ingestor",
        "username": "postgres", 
        "password": "your_password"
    }
    
    db_connector = PostgreSQLConnector("postgres", db_config)
    await db_connector.initialize()
    
    # Initialize enhanced processor with storage
    processor = EnhancedAttachmentProcessor("migration", processor_config)
    await processor.add_storage_backend("primary_storage", storage_connector)
    
    try:
        # Fetch emails with attachments that need migration
        emails_to_migrate = await fetch_emails_for_migration(db_connector)
        
        print(f"📧 Found {len(emails_to_migrate)} emails to migrate")
        
        migration_stats = {
            "processed": 0,
            "errors": 0,
            "attachments_migrated": 0,
            "storage_saved": 0
        }
        
        # Process emails in batches
        batch_size = 50
        for i in range(0, len(emails_to_migrate), batch_size):
            batch = emails_to_migrate[i:i + batch_size]
            
            print(f"📦 Processing batch {i//batch_size + 1}/{(len(emails_to_migrate) + batch_size - 1)//batch_size}")
            
            for email in batch:
                try:
                    # Process with enhanced processor
                    result = await processor.process(email)
                    
                    if result.status.value == "success":
                        # Update email in database with new storage info
                        await db_connector.update_email(email)
                        
                        migration_stats["processed"] += 1
                        migration_stats["attachments_migrated"] += result.metadata["processed_count"]
                        
                        # Calculate storage savings
                        for storage_info in result.metadata.get("storage_infos", []):
                            original_size = storage_info.get("original_size", 0)
                            stored_size = storage_info.get("stored_size", 0)
                            migration_stats["storage_saved"] += (original_size - stored_size)
                    
                    else:
                        print(f"❌ Failed to migrate email {email.id}: {result.error_message}")
                        migration_stats["errors"] += 1
                        
                except Exception as e:
                    print(f"❌ Error migrating email {email.id}: {e}")
                    migration_stats["errors"] += 1
            
            # Small delay between batches
            await asyncio.sleep(0.1)
        
        # Print migration summary
        print("\n📊 Migration Summary:")
        print(f"   ✅ Emails processed: {migration_stats['processed']}")
        print(f"   📎 Attachments migrated: {migration_stats['attachments_migrated']}")
        print(f"   💾 Storage saved: {migration_stats['storage_saved'] / (1024*1024):.1f} MB")
        print(f"   ❌ Errors: {migration_stats['errors']}")
        
        if migration_stats["errors"] == 0:
            print("🎉 Migration completed successfully!")
        else:
            print(f"⚠️  Migration completed with {migration_stats['errors']} errors")
            
    except Exception as e:
        print(f"💥 Migration failed: {e}")
        raise
        
    finally:
        await db_connector.cleanup()
        await storage_connector.cleanup()


async def fetch_emails_for_migration(db_connector: PostgreSQLConnector) -> List[EmailMessage]:
    """
    Fetch emails that need migration to hybrid storage.
    """
    # This would typically query for emails with attachments
    # that haven't been migrated yet
    
    query = """
    SELECT * FROM emails 
    WHERE has_attachments = true 
    AND migration_status IS NULL
    ORDER BY received_date DESC
    LIMIT 1000
    """
    
    emails = await db_connector.fetch_emails_by_query(query)
    return emails


async def validate_migration():
    """
    Validate that migration was successful.
    """
    print("🔍 Validating migration...")
    
    # Check that all attachments are accessible
    validation_stats = {
        "total_checked": 0,
        "accessible": 0,
        "errors": 0
    }
    
    # Sample validation logic
    emails_to_check = await fetch_migrated_emails()
    
    for email in emails_to_check:
        for attachment in email.attachments or []:
            validation_stats["total_checked"] += 1
            
            try:
                # Try to access attachment based on storage info
                if hasattr(attachment, 'extended_properties') and attachment.extended_properties:
                    storage_key = attachment.extended_properties.get('storage_key')
                    storage_backend = attachment.extended_properties.get('storage_backend')
                    
                    if storage_key and storage_backend:
                        # Validate object storage access
                        backend = processor.storage_backends[storage_backend]
                        content = await backend.download_attachment(storage_key)
                        
                        if content:
                            validation_stats["accessible"] += 1
                    else:
                        # Database storage - check content exists
                        if attachment.content:
                            validation_stats["accessible"] += 1
                        
            except Exception as e:
                print(f"❌ Validation error for attachment {attachment.id}: {e}")
                validation_stats["errors"] += 1
    
    print(f"📊 Validation Results:")
    print(f"   📎 Total attachments checked: {validation_stats['total_checked']}")
    print(f"   ✅ Accessible: {validation_stats['accessible']}")
    print(f"   ❌ Errors: {validation_stats['errors']}")
    
    success_rate = validation_stats["accessible"] / validation_stats["total_checked"] * 100
    print(f"   📈 Success rate: {success_rate:.1f}%")
    
    return success_rate > 95  # Consider successful if >95% accessible


if __name__ == "__main__":
    # Run migration
    asyncio.run(migrate_existing_attachments())
    
    # Validate migration
    asyncio.run(validate_migration())
```

## **⚠️ Important Considerations**

### **Backward Compatibility**

The enhanced attachment processor maintains backward compatibility:

- **Existing database schema**: No changes required
- **Existing attachments**: Continue to work without migration
- **API compatibility**: Same interface as basic processor

### **Performance Impact**

- **Initial migration**: May take time for large datasets
- **Storage access**: Network latency for object storage
- **Memory usage**: Reduced for large attachments
- **Database size**: Significantly reduced for large attachments

### **Rollback Plan**

If migration issues occur:

1. **Stop processing** new emails
2. **Restore database** from backup
3. **Revert to basic processor** configuration
4. **Investigate and fix** issues
5. **Retry migration** with fixes

### **Monitoring**

Monitor these metrics during and after migration:

- **Attachment access latency**
- **Storage backend health**
- **Database size reduction**
- **Error rates**
- **Storage costs**

## **🔧 Troubleshooting**

### **Common Issues**

#### **Storage Connection Errors**
```python
# Test storage connectivity
try:
    await storage_connector.initialize()
    print("✅ Storage connection successful")
except Exception as e:
    print(f"❌ Storage connection failed: {e}")
```

#### **Permission Issues**
```python
# Test storage permissions
try:
    # Upload test file
    test_attachment = EmailAttachment(
        id="test",
        name="test.txt",
        content_type="text/plain",
        size=10,
        content=b"test data"
    )
    
    storage_obj = await storage_connector.upload_attachment(test_attachment)
    print("✅ Upload permission working")
    
    # Download test file
    content = await storage_connector.download_attachment(storage_obj.key)
    print("✅ Download permission working")
    
    # Delete test file
    await storage_connector.delete_attachment(storage_obj.key)
    print("✅ Delete permission working")
    
except Exception as e:
    print(f"❌ Permission error: {e}")
```

#### **Configuration Validation**
```python
# Validate processor configuration
try:
    processor = EnhancedAttachmentProcessor("test", config)
    status = processor.get_status()
    print(f"✅ Processor configuration valid: {status}")
except Exception as e:
    print(f"❌ Configuration error: {e}")
```

## **📞 Support**

If you encounter issues during migration:

1. **Check logs** for detailed error messages
2. **Review configuration** against examples
3. **Test in development** environment first
4. **Contact support** with specific error details
5. **Use rollback plan** if necessary

For additional help:
- [Storage Architecture Documentation](STORAGE_ARCHITECTURE.md)
- [GitHub Issues](https://github.com/evolvisai/metcal/issues)
- [Examples Directory](../examples/)
