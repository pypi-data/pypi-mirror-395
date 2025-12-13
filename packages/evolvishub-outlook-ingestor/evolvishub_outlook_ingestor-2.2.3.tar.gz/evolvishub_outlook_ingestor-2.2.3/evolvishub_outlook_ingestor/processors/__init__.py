"""
Data processors for Evolvishub Outlook Ingestor.

This module contains processors for different types of data processing:
- Email processing and normalization
- Attachment processing and storage
- Enhanced attachment processing with hybrid storage support
- Batch processing for high-volume operations

All processors implement the BaseProcessor interface to ensure
consistent behavior and easy integration.
"""

from evolvishub_outlook_ingestor.processors.email_processor import EmailProcessor
from evolvishub_outlook_ingestor.processors.attachment_processor import AttachmentProcessor

try:
    from evolvishub_outlook_ingestor.processors.enhanced_attachment_processor import (
        EnhancedAttachmentProcessor,
        StorageStrategy,
        CompressionType,
        AttachmentStorageInfo,
        StorageRule
    )
    ENHANCED_ATTACHMENT_PROCESSOR_AVAILABLE = True
except ImportError:
    ENHANCED_ATTACHMENT_PROCESSOR_AVAILABLE = False

__all__ = [
    "EmailProcessor",
    "AttachmentProcessor",
    "EnhancedAttachmentProcessor",
    "StorageStrategy",
    "CompressionType",
    "AttachmentStorageInfo",
    "StorageRule",
    "ENHANCED_ATTACHMENT_PROCESSOR_AVAILABLE",
]
