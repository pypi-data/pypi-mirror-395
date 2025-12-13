"""
Email processor for Evolvishub Outlook Ingestor.

This module implements email content processing and normalization including:
- Email content parsing and normalization
- HTML to text conversion capabilities
- Email address extraction and validation
- Character encoding detection and conversion
- Duplicate detection based on Message-ID
"""

import hashlib
import re
from collections import OrderedDict
from datetime import datetime
from typing import Any, Dict, List, Optional, Set
from uuid import UUID

import chardet
from bs4 import BeautifulSoup
from email_validator import EmailNotValidError, validate_email

from evolvishub_outlook_ingestor.core.base_processor import BaseProcessor
from evolvishub_outlook_ingestor.core.data_models import (
    EmailAddress,
    EmailMessage,
    ProcessingResult,
    ProcessingStatus,
)
from evolvishub_outlook_ingestor.core.exceptions import ProcessingError, ValidationError


class LRUSet:
    """LRU (Least Recently Used) Set with maximum size limit."""

    def __init__(self, maxsize: int = 10000):
        """
        Initialize LRU set.

        Args:
            maxsize: Maximum number of items to store
        """
        self.maxsize = maxsize
        self.data = OrderedDict()

    def add(self, item: str) -> None:
        """Add item to set, removing oldest if at capacity."""
        if item in self.data:
            # Move to end (most recently used)
            self.data.move_to_end(item)
        else:
            # Add new item
            self.data[item] = True

            # Remove oldest if over capacity
            if len(self.data) > self.maxsize:
                self.data.popitem(last=False)

    def __contains__(self, item: str) -> bool:
        """Check if item is in set."""
        if item in self.data:
            # Move to end (most recently used)
            self.data.move_to_end(item)
            return True
        return False

    def __len__(self) -> int:
        """Get number of items in set."""
        return len(self.data)

    def clear(self) -> None:
        """Clear all items from set."""
        self.data.clear()


# Import security utilities with lazy loading to avoid circular imports
def _get_security_utils():
    from evolvishub_outlook_ingestor.utils.security import sanitize_input, InputSanitizer
    return sanitize_input, InputSanitizer


class EmailProcessor(BaseProcessor[EmailMessage, EmailMessage]):
    """Email content processor and normalizer."""
    
    def __init__(
        self,
        name: str = "email_processor",
        config: Optional[Dict[str, Any]] = None,
        **kwargs
    ):
        """
        Initialize email processor.
        
        Args:
            name: Processor name
            config: Configuration dictionary containing:
                - normalize_content: Enable content normalization
                - extract_links: Extract links from email content
                - detect_encoding: Enable character encoding detection
                - validate_addresses: Validate email addresses
                - remove_duplicates: Enable duplicate detection
                - html_to_text: Convert HTML to text
        """
        super().__init__(name, config, **kwargs)
        
        # Processing configuration
        self.normalize_content = config.get("normalize_content", True)
        self.extract_links = config.get("extract_links", True)
        self.detect_encoding = config.get("detect_encoding", True)
        self.validate_addresses = config.get("validate_addresses", True)
        self.remove_duplicates = config.get("remove_duplicates", True)
        self.html_to_text = config.get("html_to_text", True)
        
        # Duplicate tracking with LRU cache to prevent memory leaks
        self._processed_message_ids = LRUSet(maxsize=config.get("duplicate_cache_size", 10000))
        self._processed_hashes = LRUSet(maxsize=config.get("duplicate_cache_size", 10000))
        
        # Content processing patterns
        self._email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
        self._url_pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
        self._phone_pattern = re.compile(r'(\+?1[-.\s]?)?\(?([0-9]{3})\)?[-.\s]?([0-9]{3})[-.\s]?([0-9]{4})')
    
    async def _process_data(
        self,
        input_data: EmailMessage,
        result: ProcessingResult,
        **kwargs
    ) -> ProcessingResult:
        """Process email data."""
        try:
            # Check for duplicates
            if self.remove_duplicates and self._is_duplicate(input_data):
                result.skipped_items += 1
                result.warnings.append(f"Skipped duplicate email: {input_data.id}")
                self.logger.debug("Skipped duplicate email", email_id=input_data.id)
                return result
            
            # Process email content
            processed_email = await self._process_email_content(input_data)
            
            # Validate email addresses
            if self.validate_addresses:
                processed_email = self._validate_email_addresses(processed_email)
            
            # Extract additional metadata
            processed_email = self._extract_metadata(processed_email)
            
            # Store processed email in result
            if not hasattr(result, 'results'):
                result.results = []
            result.results.append(processed_email)
            
            result.successful_items += 1
            
            # Track processed email
            if processed_email.message_id:
                self._processed_message_ids.add(processed_email.message_id)

            content_hash = self._calculate_content_hash(processed_email)
            self._processed_hashes.add(content_hash)
            
            return result
            
        except Exception as e:
            result.failed_items += 1
            result.warnings.append(f"Failed to process email {input_data.id}: {e}")
            
            self.logger.error(
                "Email processing failed",
                email_id=input_data.id,
                error=str(e)
            )
            
            raise ProcessingError(
                f"Email processing failed: {e}",
                processor=self.name,
                cause=e
            )
    
    def _is_duplicate(self, email: EmailMessage) -> bool:
        """Check if email is a duplicate."""
        # Check by Message-ID
        if email.message_id and email.message_id in self._processed_message_ids:
            return True
        
        # Check by content hash
        content_hash = self._calculate_content_hash(email)
        if content_hash in self._processed_hashes:
            return True
        
        return False
    
    def _calculate_content_hash(self, email: EmailMessage) -> str:
        """Calculate content hash for duplicate detection."""
        # Create hash from key email properties
        hash_content = f"{email.subject}|{email.body}|{email.sent_date}"
        if email.sender:
            hash_content += f"|{email.sender.email}"
        
        return hashlib.md5(hash_content.encode('utf-8')).hexdigest()
    
    async def _process_email_content(self, email: EmailMessage) -> EmailMessage:
        """Process and normalize email content."""
        processed_email = email.model_copy()
        
        # Detect and fix encoding
        if self.detect_encoding:
            processed_email = self._fix_encoding(processed_email)
        
        # Normalize content
        if self.normalize_content:
            processed_email = self._normalize_content(processed_email)
        
        # Convert HTML to text if needed
        if self.html_to_text and processed_email.is_html:
            processed_email = self._convert_html_to_text(processed_email)
        
        # Extract links
        if self.extract_links:
            processed_email = self._extract_links_from_content(processed_email)
        
        return processed_email
    
    def _fix_encoding(self, email: EmailMessage) -> EmailMessage:
        """Detect and fix character encoding issues."""
        def fix_text_encoding(text: Optional[str]) -> Optional[str]:
            if not text:
                return text
            
            try:
                # Try to detect encoding if text appears to be bytes
                if isinstance(text, bytes):
                    detected = chardet.detect(text)
                    if detected['encoding']:
                        return text.decode(detected['encoding'])
                
                # Check if text has encoding issues
                try:
                    text.encode('utf-8')
                    return text
                except UnicodeEncodeError:
                    # Try to fix common encoding issues
                    return text.encode('utf-8', errors='replace').decode('utf-8')
                    
            except Exception as e:
                self.logger.warning(
                    "Failed to fix encoding",
                    error=str(e)
                )
                return text
            
            return text
        
        # Fix encoding for text fields
        email.subject = fix_text_encoding(email.subject)
        email.body = fix_text_encoding(email.body)
        
        return email
    
    def _normalize_content(self, email: EmailMessage) -> EmailMessage:
        """Normalize email content with security sanitization."""
        # Normalize and sanitize subject
        if email.subject:
            # Remove excessive whitespace
            email.subject = re.sub(r'\s+', ' ', email.subject.strip())

            # Remove common prefixes
            email.subject = re.sub(r'^(RE:|FW:|FWD:)\s*', '', email.subject, flags=re.IGNORECASE)

            # Sanitize for security
            sanitize_input, _ = _get_security_utils()
            email.subject = sanitize_input(email.subject, "html")

        # Normalize and sanitize body
        if email.body:
            # Remove excessive whitespace
            email.body = re.sub(r'\n\s*\n\s*\n', '\n\n', email.body)
            email.body = re.sub(r'[ \t]+', ' ', email.body)

            # Remove common email signatures and disclaimers
            email.body = self._remove_signatures(email.body)

            # Sanitize for security (but preserve some HTML if it's HTML email)
            if not email.is_html:
                sanitize_input, _ = _get_security_utils()
                email.body = sanitize_input(email.body, "html")

        return email
    
    def _remove_signatures(self, body: str) -> str:
        """Remove common email signatures and disclaimers."""
        # Common signature patterns
        signature_patterns = [
            r'\n--\s*\n.*$',  # Standard signature delimiter
            r'\n_{10,}.*$',   # Underscore delimiter
            r'\nSent from my \w+.*$',  # Mobile signatures
            r'\nThis email.*confidential.*$',  # Confidentiality disclaimers
        ]
        
        for pattern in signature_patterns:
            body = re.sub(pattern, '', body, flags=re.DOTALL | re.IGNORECASE)
        
        return body.strip()
    
    def _convert_html_to_text(self, email: EmailMessage) -> EmailMessage:
        """Convert HTML content to plain text."""
        if not email.body or not email.is_html:
            return email
        
        try:
            # Parse HTML
            soup = BeautifulSoup(email.body, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            # Get text content
            text = soup.get_text()
            
            # Clean up whitespace
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = ' '.join(chunk for chunk in chunks if chunk)
            
            # Update email
            email.body = text
            email.body_type = "text"
            email.is_html = False
            
            # Store original HTML in extended properties
            if not email.extended_properties:
                email.extended_properties = {}
            email.extended_properties["original_html"] = email.body
            
        except Exception as e:
            self.logger.warning(
                "Failed to convert HTML to text",
                email_id=email.id,
                error=str(e)
            )
        
        return email
    
    def _extract_links_from_content(self, email: EmailMessage) -> EmailMessage:
        """Extract links from email content."""
        if not email.body:
            return email
        
        try:
            # Extract URLs
            urls = self._url_pattern.findall(email.body)
            
            # Extract email addresses
            email_addresses = self._email_pattern.findall(email.body)
            
            # Extract phone numbers
            phone_numbers = self._phone_pattern.findall(email.body)
            phone_numbers = [''.join(match) for match in phone_numbers]
            
            # Store in extended properties
            if not email.extended_properties:
                email.extended_properties = {}
            
            if urls:
                email.extended_properties["extracted_urls"] = list(set(urls))
            
            if email_addresses:
                email.extended_properties["extracted_emails"] = list(set(email_addresses))
            
            if phone_numbers:
                email.extended_properties["extracted_phones"] = list(set(phone_numbers))
            
        except Exception as e:
            self.logger.warning(
                "Failed to extract links",
                email_id=email.id,
                error=str(e)
            )
        
        return email
    
    def _validate_email_addresses(self, email: EmailMessage) -> EmailMessage:
        """Validate and normalize email addresses with security checks."""
        def validate_address(addr: Optional[EmailAddress]) -> Optional[EmailAddress]:
            if not addr or not addr.email:
                return addr

            # Security validation first
            sanitize_input, InputSanitizer = _get_security_utils()
            if not InputSanitizer.validate_email_address(addr.email):
                self.logger.warning(
                    "Email address failed security validation",
                    email=addr.email
                )
                return None

            try:
                # Sanitize email address
                sanitized_email = sanitize_input(addr.email, "general")

                # Validate email address
                validated = validate_email(sanitized_email)

                # Update with normalized email
                addr.email = validated.email

                # Sanitize display name if present
                if addr.name:
                    addr.name = sanitize_input(addr.name, "html")

                return addr

            except EmailNotValidError as e:
                self.logger.warning(
                    "Invalid email address",
                    email=addr.email,
                    error=str(e)
                )
                return None
        
        def validate_addresses(addrs: List[EmailAddress]) -> List[EmailAddress]:
            validated = []
            for addr in addrs:
                validated_addr = validate_address(addr)
                if validated_addr:
                    validated.append(validated_addr)
            return validated
        
        # Validate sender and from addresses
        email.sender = validate_address(email.sender)
        email.from_address = validate_address(email.from_address)
        
        # Validate recipient addresses
        email.to_recipients = validate_addresses(email.to_recipients)
        email.cc_recipients = validate_addresses(email.cc_recipients)
        email.bcc_recipients = validate_addresses(email.bcc_recipients)
        email.reply_to = validate_addresses(email.reply_to)
        
        return email
    
    def _extract_metadata(self, email: EmailMessage) -> EmailMessage:
        """Extract additional metadata from email."""
        if not email.extended_properties:
            email.extended_properties = {}
        
        # Calculate content statistics
        if email.body:
            email.extended_properties["word_count"] = len(email.body.split())
            email.extended_properties["char_count"] = len(email.body)
            email.extended_properties["line_count"] = len(email.body.splitlines())
        
        # Extract language hints (simple heuristic)
        if email.body:
            # Common words in different languages
            english_words = ["the", "and", "or", "but", "in", "on", "at", "to", "for", "of", "with", "by"]
            spanish_words = ["el", "la", "y", "o", "pero", "en", "de", "con", "por", "para"]
            french_words = ["le", "la", "et", "ou", "mais", "dans", "de", "avec", "par", "pour"]
            
            body_lower = email.body.lower()
            english_count = sum(1 for word in english_words if word in body_lower)
            spanish_count = sum(1 for word in spanish_words if word in body_lower)
            french_count = sum(1 for word in french_words if word in body_lower)
            
            if english_count > spanish_count and english_count > french_count:
                email.extended_properties["detected_language"] = "en"
            elif spanish_count > french_count:
                email.extended_properties["detected_language"] = "es"
            elif french_count > 0:
                email.extended_properties["detected_language"] = "fr"
        
        # Extract thread information
        if email.subject:
            # Check if it's a reply or forward
            if re.match(r'^(RE:|FW:|FWD:)', email.subject, re.IGNORECASE):
                email.extended_properties["is_reply_or_forward"] = True
        
        # Processing timestamp
        email.extended_properties["processed_at"] = datetime.utcnow().isoformat()
        
        return email
