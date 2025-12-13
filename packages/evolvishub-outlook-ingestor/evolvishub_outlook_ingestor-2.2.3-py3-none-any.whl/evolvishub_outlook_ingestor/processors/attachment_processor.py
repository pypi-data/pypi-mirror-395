"""
Attachment processor for Evolvishub Outlook Ingestor.

This module implements email attachment processing including:
- File type detection using python-magic
- Size validation and content scanning
- Inline image extraction from HTML emails
- Virus scanning integration hooks
- Attachment storage optimization
"""

import hashlib
import mimetypes
import os
from datetime import datetime
from typing import Any, Dict, List, Optional, Set
from uuid import UUID

try:
    import magic
    MAGIC_AVAILABLE = True
except ImportError:
    MAGIC_AVAILABLE = False
    magic = None

from evolvishub_outlook_ingestor.core.base_processor import BaseProcessor
from evolvishub_outlook_ingestor.core.data_models import (
    EmailAttachment,
    EmailMessage,
    ProcessingResult,
    ProcessingStatus,
    AttachmentType,
)
from evolvishub_outlook_ingestor.core.exceptions import ProcessingError, ValidationError


class AttachmentProcessor(BaseProcessor[EmailMessage, EmailMessage]):
    """Email attachment processor and validator."""
    
    def __init__(
        self,
        name: str = "attachment_processor",
        config: Optional[Dict[str, Any]] = None,
        **kwargs
    ):
        """
        Initialize attachment processor.
        
        Args:
            name: Processor name
            config: Configuration dictionary containing:
                - max_attachment_size: Maximum attachment size in bytes
                - allowed_types: List of allowed MIME types
                - blocked_types: List of blocked MIME types
                - scan_for_viruses: Enable virus scanning
                - extract_metadata: Extract file metadata
                - calculate_hashes: Calculate file hashes
                - compress_images: Compress image attachments
        """
        super().__init__(name, config, **kwargs)
        
        # Processing configuration
        self.max_attachment_size = config.get("max_attachment_size", 52428800)  # 50MB
        self.allowed_types = set(config.get("allowed_types", []))
        self.blocked_types = set(config.get("blocked_types", [
            "application/x-executable",
            "application/x-msdownload",
            "application/x-msdos-program",
            "application/x-winexe",
        ]))
        self.scan_for_viruses = config.get("scan_for_viruses", False)
        self.extract_metadata = config.get("extract_metadata", True)
        self.calculate_hashes = config.get("calculate_hashes", True)
        self.compress_images = config.get("compress_images", False)
        
        # File type detection
        if MAGIC_AVAILABLE:
            self.magic_mime = magic.Magic(mime=True)
            self.magic_type = magic.Magic()
        else:
            self.magic_mime = None
            self.magic_type = None
        
        # Processed attachment tracking
        self._processed_hashes: Set[str] = set()
        
        # Safe file extensions
        self.safe_extensions = {
            '.txt', '.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx',
            '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.svg',
            '.mp3', '.mp4', '.avi', '.mov', '.wav',
            '.zip', '.rar', '.7z', '.tar', '.gz',
            '.csv', '.json', '.xml', '.html', '.css', '.js',
        }
    
    async def _process_data(
        self,
        input_data: EmailMessage,
        result: ProcessingResult,
        **kwargs
    ) -> ProcessingResult:
        """Process email attachments."""
        try:
            processed_email = input_data.model_copy()
            
            if not processed_email.attachments:
                # No attachments to process
                if not hasattr(result, 'results'):
                    result.results = []
                result.results.append(processed_email)
                result.successful_items += 1
                return result
            
            # Process each attachment
            processed_attachments = []
            
            for attachment in processed_email.attachments:
                try:
                    processed_attachment = await self._process_attachment(attachment)
                    
                    if processed_attachment:
                        processed_attachments.append(processed_attachment)
                    else:
                        result.warnings.append(
                            f"Attachment {attachment.name} was filtered out"
                        )
                        
                except Exception as e:
                    result.warnings.append(
                        f"Failed to process attachment {attachment.name}: {e}"
                    )
                    self.logger.warning(
                        "Attachment processing failed",
                        attachment_name=attachment.name,
                        error=str(e)
                    )
            
            # Update email with processed attachments
            processed_email.attachments = processed_attachments
            processed_email.has_attachments = len(processed_attachments) > 0
            
            # Store processed email in result
            if not hasattr(result, 'results'):
                result.results = []
            result.results.append(processed_email)
            
            result.successful_items += 1
            
            return result
            
        except Exception as e:
            result.failed_items += 1
            result.warnings.append(f"Failed to process email attachments: {e}")
            
            self.logger.error(
                "Email attachment processing failed",
                email_id=input_data.id,
                error=str(e)
            )
            
            raise ProcessingError(
                f"Attachment processing failed: {e}",
                processor=self.name,
                cause=e
            )
    
    async def _process_attachment(self, attachment: EmailAttachment) -> Optional[EmailAttachment]:
        """Process a single attachment."""
        # Validate attachment size
        if not self._validate_size(attachment):
            self.logger.warning(
                "Attachment exceeds size limit",
                attachment_name=attachment.name,
                size=attachment.size,
                max_size=self.max_attachment_size
            )
            return None
        
        # Detect file type
        attachment = self._detect_file_type(attachment)
        
        # Validate file type
        if not self._validate_file_type(attachment):
            self.logger.warning(
                "Attachment type not allowed",
                attachment_name=attachment.name,
                content_type=attachment.content_type
            )
            return None
        
        # Check for duplicates
        if self.calculate_hashes and self._is_duplicate_attachment(attachment):
            self.logger.debug(
                "Skipping duplicate attachment",
                attachment_name=attachment.name
            )
            return None
        
        # Extract metadata
        if self.extract_metadata:
            attachment = self._extract_attachment_metadata(attachment)
        
        # Calculate hashes
        if self.calculate_hashes:
            attachment = self._calculate_attachment_hashes(attachment)
        
        # Scan for viruses
        if self.scan_for_viruses:
            attachment = await self._scan_attachment(attachment)
            
            if not attachment.is_safe:
                self.logger.warning(
                    "Attachment failed virus scan",
                    attachment_name=attachment.name,
                    scan_result=attachment.scan_result
                )
                # Still return the attachment but mark as unsafe
        
        # Compress images if enabled
        if self.compress_images and self._is_image(attachment):
            attachment = self._compress_image(attachment)
        
        # Update processing metadata
        if not attachment.extended_properties:
            attachment.extended_properties = {}
        attachment.extended_properties["processed_at"] = datetime.utcnow().isoformat()
        attachment.extended_properties["processor"] = self.name
        
        return attachment
    
    def _validate_size(self, attachment: EmailAttachment) -> bool:
        """Validate attachment size."""
        if attachment.size > self.max_attachment_size:
            return False
        return True
    
    def _detect_file_type(self, attachment: EmailAttachment) -> EmailAttachment:
        """Detect file type using python-magic if available."""
        if not attachment.content:
            return attachment

        try:
            if MAGIC_AVAILABLE and self.magic_mime and self.magic_type:
                # Detect MIME type
                detected_mime = self.magic_mime.from_buffer(attachment.content)

                # Detect file type description
                detected_type = self.magic_type.from_buffer(attachment.content)

                # Update content type if not set or if detection differs significantly
                if not attachment.content_type or attachment.content_type == "application/octet-stream":
                    attachment.content_type = detected_mime

                # Store detection results in extended properties
                if not attachment.extended_properties:
                    attachment.extended_properties = {}

                attachment.extended_properties["detected_mime"] = detected_mime
                attachment.extended_properties["detected_type"] = detected_type
            
            # Also try to guess from filename
            if attachment.name:
                guessed_type, _ = mimetypes.guess_type(attachment.name)
                if guessed_type:
                    attachment.extended_properties["filename_mime"] = guessed_type
            
        except Exception as e:
            self.logger.warning(
                "Failed to detect file type",
                attachment_name=attachment.name,
                error=str(e)
            )
        
        return attachment
    
    def _validate_file_type(self, attachment: EmailAttachment) -> bool:
        """Validate file type against allowed/blocked lists."""
        content_type = attachment.content_type or ""
        
        # Check blocked types
        if content_type in self.blocked_types:
            return False
        
        # Check by file extension if MIME type check fails
        if attachment.name:
            ext = os.path.splitext(attachment.name)[1].lower()
            
            # Block dangerous extensions
            dangerous_extensions = {
                '.exe', '.bat', '.cmd', '.com', '.pif', '.scr', '.vbs', '.js',
                '.jar', '.app', '.deb', '.pkg', '.dmg', '.msi'
            }
            
            if ext in dangerous_extensions:
                return False
        
        # If allowed types are specified, check against them
        if self.allowed_types:
            return content_type in self.allowed_types
        
        # Default to allow if no specific restrictions
        return True
    
    def _is_duplicate_attachment(self, attachment: EmailAttachment) -> bool:
        """Check if attachment is a duplicate based on content hash."""
        if not attachment.content:
            return False
        
        content_hash = hashlib.sha256(attachment.content).hexdigest()
        
        if content_hash in self._processed_hashes:
            return True
        
        self._processed_hashes.add(content_hash)
        return False
    
    def _extract_attachment_metadata(self, attachment: EmailAttachment) -> EmailAttachment:
        """Extract metadata from attachment."""
        if not attachment.extended_properties:
            attachment.extended_properties = {}
        
        # Basic file information
        if attachment.name:
            name_parts = os.path.splitext(attachment.name)
            attachment.extended_properties["filename_base"] = name_parts[0]
            attachment.extended_properties["filename_ext"] = name_parts[1].lower()
        
        # Content analysis
        if attachment.content:
            attachment.extended_properties["content_length"] = len(attachment.content)
            
            # Check if content is text-based
            try:
                text_content = attachment.content.decode('utf-8')
                attachment.extended_properties["is_text"] = True
                attachment.extended_properties["text_preview"] = text_content[:500]
            except UnicodeDecodeError:
                attachment.extended_properties["is_text"] = False
        
        # Image metadata
        if self._is_image(attachment):
            attachment = self._extract_image_metadata(attachment)
        
        return attachment
    
    def _extract_image_metadata(self, attachment: EmailAttachment) -> EmailAttachment:
        """Extract metadata from image attachments."""
        try:
            from PIL import Image
            import io
            
            if not attachment.content:
                return attachment
            
            # Open image
            image = Image.open(io.BytesIO(attachment.content))
            
            # Extract basic information
            if not attachment.extended_properties:
                attachment.extended_properties = {}
            
            attachment.extended_properties["image_width"] = image.width
            attachment.extended_properties["image_height"] = image.height
            attachment.extended_properties["image_mode"] = image.mode
            attachment.extended_properties["image_format"] = image.format
            
            # Extract EXIF data if available
            if hasattr(image, '_getexif') and image._getexif():
                exif_data = image._getexif()
                if exif_data:
                    # Store selected EXIF data
                    attachment.extended_properties["exif_data"] = {
                        str(k): str(v) for k, v in exif_data.items() 
                        if isinstance(v, (str, int, float))
                    }
            
        except Exception as e:
            self.logger.warning(
                "Failed to extract image metadata",
                attachment_name=attachment.name,
                error=str(e)
            )
        
        return attachment
    
    def _calculate_attachment_hashes(self, attachment: EmailAttachment) -> EmailAttachment:
        """Calculate various hashes for the attachment."""
        if not attachment.content:
            return attachment
        
        try:
            if not attachment.extended_properties:
                attachment.extended_properties = {}
            
            # Calculate multiple hash types
            attachment.extended_properties["md5_hash"] = hashlib.md5(attachment.content).hexdigest()
            attachment.extended_properties["sha1_hash"] = hashlib.sha1(attachment.content).hexdigest()
            attachment.extended_properties["sha256_hash"] = hashlib.sha256(attachment.content).hexdigest()
            
        except Exception as e:
            self.logger.warning(
                "Failed to calculate hashes",
                attachment_name=attachment.name,
                error=str(e)
            )
        
        return attachment
    
    async def _scan_attachment(self, attachment: EmailAttachment) -> EmailAttachment:
        """Scan attachment for viruses (placeholder for integration)."""
        # This is a placeholder for virus scanning integration
        # In a real implementation, you would integrate with:
        # - ClamAV
        # - VirusTotal API
        # - Windows Defender
        # - Other antivirus solutions
        
        try:
            # Placeholder logic - mark as safe by default
            attachment.is_safe = True
            attachment.scan_result = "clean"
            
            # Example integration points:
            # 1. Save attachment to temp file
            # 2. Call antivirus scanner
            # 3. Parse results
            # 4. Update attachment properties
            
            # For demonstration, mark executable files as potentially unsafe
            if attachment.content_type and "executable" in attachment.content_type:
                attachment.is_safe = False
                attachment.scan_result = "potentially_unsafe_executable"
            
            if not attachment.extended_properties:
                attachment.extended_properties = {}
            attachment.extended_properties["scanned_at"] = datetime.utcnow().isoformat()
            
        except Exception as e:
            self.logger.warning(
                "Virus scan failed",
                attachment_name=attachment.name,
                error=str(e)
            )
            attachment.is_safe = None  # Unknown status
            attachment.scan_result = f"scan_error: {e}"
        
        return attachment
    
    def _is_image(self, attachment: EmailAttachment) -> bool:
        """Check if attachment is an image."""
        if not attachment.content_type:
            return False
        
        return attachment.content_type.startswith("image/")
    
    def _compress_image(self, attachment: EmailAttachment) -> EmailAttachment:
        """Compress image attachment (placeholder)."""
        try:
            from PIL import Image
            import io
            
            if not attachment.content or not self._is_image(attachment):
                return attachment
            
            # Open image
            image = Image.open(io.BytesIO(attachment.content))
            
            # Only compress if image is large
            if len(attachment.content) > 1024 * 1024:  # 1MB
                # Resize if too large
                max_size = (1920, 1080)
                if image.size[0] > max_size[0] or image.size[1] > max_size[1]:
                    image.thumbnail(max_size, Image.Resampling.LANCZOS)
                
                # Save with compression
                output = io.BytesIO()
                
                # Convert to RGB if necessary
                if image.mode in ('RGBA', 'LA', 'P'):
                    image = image.convert('RGB')
                
                # Save as JPEG with quality compression
                image.save(output, format='JPEG', quality=85, optimize=True)
                
                compressed_content = output.getvalue()
                
                # Only use compressed version if it's significantly smaller
                if len(compressed_content) < len(attachment.content) * 0.8:
                    attachment.content = compressed_content
                    attachment.content_type = "image/jpeg"
                    attachment.size = len(compressed_content)
                    
                    if not attachment.extended_properties:
                        attachment.extended_properties = {}
                    attachment.extended_properties["compressed"] = True
                    attachment.extended_properties["original_size"] = len(attachment.content)
            
        except Exception as e:
            self.logger.warning(
                "Failed to compress image",
                attachment_name=attachment.name,
                error=str(e)
            )
        
        return attachment
