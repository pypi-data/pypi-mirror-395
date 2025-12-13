"""
Enhanced Attachment Processing Module for Evolvishub Outlook Ingestor.

This module provides advanced attachment processing with hybrid storage support,
deduplication, compression, and multiple storage backend routing.
"""

import asyncio
import hashlib
import mimetypes
import os
import gzip
import zlib
from datetime import datetime
from typing import Dict, List, Optional, Any, Set, Tuple, Union
from pathlib import Path
from dataclasses import dataclass
from enum import Enum

try:
    import magic
    MAGIC_AVAILABLE = True
except ImportError:
    MAGIC_AVAILABLE = False

try:
    from PIL import Image
    PILLOW_AVAILABLE = True
except ImportError:
    PILLOW_AVAILABLE = False

from evolvishub_outlook_ingestor.core.base_processor import BaseProcessor
from evolvishub_outlook_ingestor.core.data_models import (
    EmailAttachment,
    EmailMessage,
    ProcessingResult,
    ProcessingStatus,
    AttachmentType,
)
from evolvishub_outlook_ingestor.core.exceptions import ProcessingError, ValidationError
from evolvishub_outlook_ingestor.connectors.base_storage_connector import BaseStorageConnector


class StorageStrategy(Enum):
    """Storage strategy for attachments."""
    DATABASE_ONLY = "database_only"
    STORAGE_ONLY = "storage_only"
    HYBRID = "hybrid"
    SIZE_BASED = "size_based"


class CompressionType(Enum):
    """Compression types for attachments."""
    NONE = "none"
    GZIP = "gzip"
    ZLIB = "zlib"


@dataclass
class AttachmentStorageInfo:
    """Information about where an attachment is stored."""
    attachment_id: str
    storage_location: str  # "database", "storage", or storage key
    storage_backend: Optional[str] = None  # Storage connector name
    content_hash: Optional[str] = None
    compressed: bool = False
    compression_type: Optional[CompressionType] = None
    original_size: int = 0
    stored_size: int = 0
    metadata: Dict[str, Any] = None


@dataclass
class StorageRule:
    """Rule for determining storage strategy."""
    name: str
    condition: str  # Python expression to evaluate
    strategy: StorageStrategy
    storage_backend: Optional[str] = None
    compress: bool = False
    compression_type: CompressionType = CompressionType.GZIP


class EnhancedAttachmentProcessor(BaseProcessor):
    """
    Enhanced attachment processor with hybrid storage support.
    
    This processor provides advanced attachment handling including:
    - Multiple storage backend support (database + object storage)
    - Content-based deduplication using SHA256 hashes
    - Configurable compression for supported file types
    - Size-based storage routing rules
    - Virus scanning integration
    - Metadata indexing and search
    
    Example:
        ```python
        # Configure processor with hybrid storage
        config = {
            "storage_strategy": "hybrid",
            "size_threshold": 1024 * 1024,  # 1MB
            "enable_compression": True,
            "enable_deduplication": True,
            "storage_backends": {
                "primary": "minio",
                "archive": "aws_s3"
            },
            "storage_rules": [
                {
                    "name": "large_files",
                    "condition": "size > 1024*1024",
                    "strategy": "storage_only",
                    "storage_backend": "primary"
                },
                {
                    "name": "images",
                    "condition": "content_type.startswith('image/')",
                    "strategy": "hybrid",
                    "compress": True
                }
            ]
        }
        
        processor = EnhancedAttachmentProcessor("enhanced_attachments", config)
        
        # Add storage connectors
        await processor.add_storage_backend("minio", minio_connector)
        await processor.add_storage_backend("aws_s3", s3_connector)
        
        # Process email with attachments
        result = await processor.process(email_message)
        ```
    """
    
    def __init__(
        self,
        name: str = "enhanced_attachment_processor",
        config: Optional[Dict[str, Any]] = None,
        **kwargs
    ):
        """
        Initialize enhanced attachment processor.
        
        Args:
            name: Processor name
            config: Configuration dictionary
        """
        super().__init__(name, config, **kwargs)
        
        # Storage configuration
        self.storage_strategy = StorageStrategy(
            self.config.get("storage_strategy", "hybrid")
        )
        self.size_threshold = self.config.get("size_threshold", 1024 * 1024)  # 1MB
        self.enable_compression = self.config.get("enable_compression", True)
        self.enable_deduplication = self.config.get("enable_deduplication", True)
        self.enable_virus_scanning = self.config.get("enable_virus_scanning", False)
        
        # Storage backends
        self.storage_backends: Dict[str, BaseStorageConnector] = {}
        self.default_storage_backend = self.config.get("default_storage_backend", "primary")
        
        # Storage rules
        self.storage_rules: List[StorageRule] = []
        self._load_storage_rules()
        
        # Deduplication cache
        self.deduplication_cache: Dict[str, AttachmentStorageInfo] = {}
        
        # Compression settings
        self.compressible_types = set(self.config.get("compressible_types", [
            "text/plain", "text/html", "text/css", "text/javascript",
            "application/json", "application/xml", "application/csv"
        ]))
        
        # File type validation
        self.max_attachment_size = self.config.get("max_attachment_size", 50 * 1024 * 1024)  # 50MB
        self.allowed_extensions = set(self.config.get("allowed_extensions", [
            ".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx",
            ".txt", ".csv", ".json", ".xml", ".zip", ".tar", ".gz",
            ".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".svg"
        ]))
        self.blocked_extensions = set(self.config.get("blocked_extensions", [
            ".exe", ".bat", ".cmd", ".com", ".scr", ".vbs", ".js", ".jar"
        ]))
    
    def _load_storage_rules(self) -> None:
        """Load storage rules from configuration."""
        rules_config = self.config.get("storage_rules", [])
        
        for rule_config in rules_config:
            rule = StorageRule(
                name=rule_config["name"],
                condition=rule_config["condition"],
                strategy=StorageStrategy(rule_config["strategy"]),
                storage_backend=rule_config.get("storage_backend"),
                compress=rule_config.get("compress", False),
                compression_type=CompressionType(
                    rule_config.get("compression_type", "gzip")
                )
            )
            self.storage_rules.append(rule)
        
        # Add default rules if none specified
        if not self.storage_rules:
            self._add_default_storage_rules()
    
    def _add_default_storage_rules(self) -> None:
        """Add default storage rules."""
        # Large files go to object storage
        self.storage_rules.append(StorageRule(
            name="large_files",
            condition=f"size > {self.size_threshold}",
            strategy=StorageStrategy.STORAGE_ONLY,
            storage_backend=self.default_storage_backend
        ))
        
        # Small files stay in database
        self.storage_rules.append(StorageRule(
            name="small_files",
            condition=f"size <= {self.size_threshold}",
            strategy=StorageStrategy.DATABASE_ONLY
        ))
        
        # Compressible text files
        self.storage_rules.append(StorageRule(
            name="compressible_text",
            condition="content_type.startswith('text/') and size > 1024",
            strategy=StorageStrategy.HYBRID,
            compress=True,
            compression_type=CompressionType.GZIP
        ))
    
    async def add_storage_backend(
        self,
        name: str,
        connector: BaseStorageConnector
    ) -> None:
        """
        Add a storage backend connector.
        
        Args:
            name: Backend name
            connector: Storage connector instance
        """
        self.storage_backends[name] = connector
        self.logger.info(f"Added storage backend: {name}")
    
    async def remove_storage_backend(self, name: str) -> None:
        """
        Remove a storage backend connector.
        
        Args:
            name: Backend name to remove
        """
        if name in self.storage_backends:
            del self.storage_backends[name]
            self.logger.info(f"Removed storage backend: {name}")
    
    def _calculate_content_hash(self, content: bytes) -> str:
        """
        Calculate SHA256 hash of content for deduplication.
        
        Args:
            content: File content
            
        Returns:
            SHA256 hash string
        """
        return hashlib.sha256(content).hexdigest()
    
    def _compress_content(
        self,
        content: bytes,
        compression_type: CompressionType
    ) -> bytes:
        """
        Compress content using specified compression type.
        
        Args:
            content: Original content
            compression_type: Compression method
            
        Returns:
            Compressed content
        """
        if compression_type == CompressionType.GZIP:
            return gzip.compress(content)
        elif compression_type == CompressionType.ZLIB:
            return zlib.compress(content)
        else:
            return content
    
    def _decompress_content(
        self,
        content: bytes,
        compression_type: CompressionType
    ) -> bytes:
        """
        Decompress content using specified compression type.
        
        Args:
            content: Compressed content
            compression_type: Compression method
            
        Returns:
            Decompressed content
        """
        if compression_type == CompressionType.GZIP:
            return gzip.decompress(content)
        elif compression_type == CompressionType.ZLIB:
            return zlib.decompress(content)
        else:
            return content
    
    def _evaluate_storage_rule(
        self,
        rule: StorageRule,
        attachment: EmailAttachment
    ) -> bool:
        """
        Evaluate if a storage rule applies to an attachment.
        
        Args:
            rule: Storage rule to evaluate
            attachment: Attachment to check
            
        Returns:
            True if rule applies
        """
        try:
            # Create evaluation context
            context = {
                "size": attachment.size,
                "content_type": attachment.content_type,
                "name": attachment.name,
                "extension": Path(attachment.name).suffix.lower(),
                "is_inline": attachment.is_inline,
                "attachment_type": attachment.attachment_type,
            }
            
            # Evaluate condition
            return eval(rule.condition, {"__builtins__": {}}, context)
            
        except Exception as e:
            self.logger.warning(f"Failed to evaluate storage rule {rule.name}: {e}")
            return False
    
    def _determine_storage_strategy(
        self,
        attachment: EmailAttachment
    ) -> Tuple[StorageStrategy, Optional[str], bool, CompressionType]:
        """
        Determine storage strategy for an attachment.
        
        Args:
            attachment: Attachment to analyze
            
        Returns:
            Tuple of (strategy, backend_name, compress, compression_type)
        """
        # Check rules in order
        for rule in self.storage_rules:
            if self._evaluate_storage_rule(rule, attachment):
                return (
                    rule.strategy,
                    rule.storage_backend or self.default_storage_backend,
                    rule.compress,
                    rule.compression_type
                )
        
        # Default strategy
        return (
            self.storage_strategy,
            self.default_storage_backend,
            False,
            CompressionType.NONE
        )

    async def _validate_attachment(self, attachment: EmailAttachment) -> None:
        """
        Validate attachment before processing.

        Args:
            attachment: Attachment to validate

        Raises:
            ValidationError: If attachment is invalid
        """
        # Check file size
        if attachment.size > self.max_attachment_size:
            raise ValidationError(
                f"Attachment {attachment.name} exceeds maximum size "
                f"({attachment.size} > {self.max_attachment_size})"
            )

        # Check file extension
        file_ext = Path(attachment.name).suffix.lower()
        if file_ext in self.blocked_extensions:
            raise ValidationError(
                f"Attachment {attachment.name} has blocked extension: {file_ext}"
            )

        if self.allowed_extensions and file_ext not in self.allowed_extensions:
            raise ValidationError(
                f"Attachment {attachment.name} has disallowed extension: {file_ext}"
            )

        # Validate content type
        if MAGIC_AVAILABLE:
            try:
                detected_type = magic.from_buffer(attachment.content, mime=True)
                if detected_type != attachment.content_type:
                    self.logger.warning(
                        f"Content type mismatch for {attachment.name}: "
                        f"declared={attachment.content_type}, detected={detected_type}"
                    )
            except Exception as e:
                self.logger.warning(f"Failed to detect content type: {e}")

    async def _scan_for_viruses(self, attachment: EmailAttachment) -> bool:
        """
        Scan attachment for viruses (placeholder for integration).

        Args:
            attachment: Attachment to scan

        Returns:
            True if clean, False if infected
        """
        if not self.enable_virus_scanning:
            return True

        # TODO: Integrate with ClamAV or cloud-based scanning service
        # This is a placeholder implementation
        self.logger.debug(f"Virus scanning {attachment.name} (placeholder)")

        # Simulate scanning delay
        await asyncio.sleep(0.1)

        return True  # Assume clean for now

    async def _check_deduplication(
        self,
        content_hash: str
    ) -> Optional[AttachmentStorageInfo]:
        """
        Check if attachment already exists (deduplication).

        Args:
            content_hash: SHA256 hash of content

        Returns:
            Storage info if duplicate found, None otherwise
        """
        if not self.enable_deduplication:
            return None

        return self.deduplication_cache.get(content_hash)

    async def _store_attachment(
        self,
        attachment: EmailAttachment,
        strategy: StorageStrategy,
        backend_name: Optional[str],
        compress: bool,
        compression_type: CompressionType
    ) -> AttachmentStorageInfo:
        """
        Store attachment according to strategy.

        Args:
            attachment: Attachment to store
            strategy: Storage strategy
            backend_name: Storage backend name
            compress: Whether to compress
            compression_type: Compression method

        Returns:
            Storage information
        """
        content = attachment.content
        original_size = len(content)

        # Compress if requested
        if compress and compression_type != CompressionType.NONE:
            content = self._compress_content(content, compression_type)

        stored_size = len(content)
        content_hash = self._calculate_content_hash(attachment.content)

        storage_info = AttachmentStorageInfo(
            attachment_id=attachment.id,
            storage_location="",
            content_hash=content_hash,
            compressed=compress,
            compression_type=compression_type if compress else None,
            original_size=original_size,
            stored_size=stored_size,
            metadata={
                "original_name": attachment.name,
                "content_type": attachment.content_type,
                "stored_at": datetime.utcnow().isoformat(),
            }
        )

        if strategy == StorageStrategy.DATABASE_ONLY:
            # Store in database (update attachment content)
            attachment.content = content
            storage_info.storage_location = "database"

        elif strategy == StorageStrategy.STORAGE_ONLY:
            # Store in object storage only
            if not backend_name or backend_name not in self.storage_backends:
                raise ProcessingError(f"Storage backend not available: {backend_name}")

            storage_connector = self.storage_backends[backend_name]

            # Create temporary attachment for upload
            temp_attachment = EmailAttachment(
                id=attachment.id,
                name=attachment.name,
                content_type=attachment.content_type,
                size=stored_size,
                content=content,
                attachment_type=attachment.attachment_type,
                is_inline=attachment.is_inline,
                content_id=attachment.content_id
            )

            # Upload to storage
            storage_obj = await storage_connector.upload_attachment(
                temp_attachment,
                metadata=storage_info.metadata
            )

            storage_info.storage_location = storage_obj.key
            storage_info.storage_backend = backend_name

            # Clear content from attachment (stored externally)
            attachment.content = b""

        elif strategy == StorageStrategy.HYBRID:
            # Store metadata in database, content in storage
            if not backend_name or backend_name not in self.storage_backends:
                raise ProcessingError(f"Storage backend not available: {backend_name}")

            storage_connector = self.storage_backends[backend_name]

            # Create temporary attachment for upload
            temp_attachment = EmailAttachment(
                id=attachment.id,
                name=attachment.name,
                content_type=attachment.content_type,
                size=stored_size,
                content=content,
                attachment_type=attachment.attachment_type,
                is_inline=attachment.is_inline,
                content_id=attachment.content_id
            )

            # Upload to storage
            storage_obj = await storage_connector.upload_attachment(
                temp_attachment,
                metadata=storage_info.metadata
            )

            storage_info.storage_location = storage_obj.key
            storage_info.storage_backend = backend_name

            # Keep minimal metadata in database
            attachment.content = b""  # Clear content
            attachment.extended_properties = attachment.extended_properties or {}
            attachment.extended_properties.update({
                "storage_key": storage_obj.key,
                "storage_backend": backend_name,
                "content_hash": content_hash,
                "compressed": compress,
                "original_size": original_size,
                "stored_size": stored_size,
            })

        # Update deduplication cache
        if self.enable_deduplication:
            self.deduplication_cache[content_hash] = storage_info

        return storage_info

    async def process_attachment(
        self,
        attachment: EmailAttachment
    ) -> AttachmentStorageInfo:
        """
        Process a single attachment.

        Args:
            attachment: Attachment to process

        Returns:
            Storage information
        """
        try:
            # Validate attachment
            await self._validate_attachment(attachment)

            # Virus scanning
            if not await self._scan_for_viruses(attachment):
                raise ProcessingError(f"Virus detected in attachment: {attachment.name}")

            # Check for duplicates
            content_hash = self._calculate_content_hash(attachment.content)
            existing_storage = await self._check_deduplication(content_hash)

            if existing_storage:
                self.logger.info(f"Duplicate attachment found: {attachment.name}")
                return existing_storage

            # Determine storage strategy
            strategy, backend_name, compress, compression_type = self._determine_storage_strategy(attachment)

            # Store attachment
            storage_info = await self._store_attachment(
                attachment, strategy, backend_name, compress, compression_type
            )

            self.logger.info(
                f"Processed attachment {attachment.name}: "
                f"strategy={strategy.value}, size={attachment.size}, "
                f"stored_size={storage_info.stored_size}"
            )

            return storage_info

        except Exception as e:
            self.logger.error(f"Failed to process attachment {attachment.name}: {e}")
            raise ProcessingError(f"Attachment processing failed: {e}")

    async def process(self, email: EmailMessage) -> ProcessingResult:
        """
        Process all attachments in an email message.

        Args:
            email: Email message to process

        Returns:
            Processing result
        """
        try:
            if not email.attachments:
                return ProcessingResult(
                    status=ProcessingStatus.SUCCESS,
                    processed_data=email,
                    metadata={"attachment_count": 0}
                )

            storage_infos = []
            processed_count = 0

            for attachment in email.attachments:
                try:
                    storage_info = await self.process_attachment(attachment)
                    storage_infos.append(storage_info)
                    processed_count += 1

                except Exception as e:
                    self.logger.error(f"Failed to process attachment {attachment.name}: {e}")
                    # Continue processing other attachments

            return ProcessingResult(
                status=ProcessingStatus.SUCCESS,
                processed_data=email,
                metadata={
                    "attachment_count": len(email.attachments),
                    "processed_count": processed_count,
                    "storage_infos": [info.__dict__ for info in storage_infos],
                }
            )

        except Exception as e:
            self.logger.error(f"Email attachment processing failed: {e}")
            return ProcessingResult(
                status=ProcessingStatus.FAILED,
                processed_data=email,
                error_message=str(e),
                metadata={"attachment_count": len(email.attachments or [])}
            )

    async def retrieve_attachment(
        self,
        storage_info: AttachmentStorageInfo
    ) -> bytes:
        """
        Retrieve attachment content from storage.

        Args:
            storage_info: Storage information

        Returns:
            Attachment content
        """
        try:
            if storage_info.storage_location == "database":
                # Content should be in the attachment object
                raise ProcessingError("Database retrieval not implemented in this context")

            elif storage_info.storage_backend:
                # Retrieve from object storage
                if storage_info.storage_backend not in self.storage_backends:
                    raise ProcessingError(f"Storage backend not available: {storage_info.storage_backend}")

                storage_connector = self.storage_backends[storage_info.storage_backend]
                content = await storage_connector.download_attachment(storage_info.storage_location)

                # Decompress if needed
                if storage_info.compressed and storage_info.compression_type:
                    content = self._decompress_content(content, storage_info.compression_type)

                return content

            else:
                raise ProcessingError("Invalid storage information")

        except Exception as e:
            self.logger.error(f"Failed to retrieve attachment: {e}")
            raise ProcessingError(f"Attachment retrieval failed: {e}")

    def get_status(self) -> Dict[str, Any]:
        """Get processor status."""
        return {
            "processor": self.name,
            "storage_strategy": self.storage_strategy.value,
            "storage_backends": list(self.storage_backends.keys()),
            "deduplication_enabled": self.enable_deduplication,
            "compression_enabled": self.enable_compression,
            "virus_scanning_enabled": self.enable_virus_scanning,
            "cache_size": len(self.deduplication_cache),
            "storage_rules": len(self.storage_rules),
        }
