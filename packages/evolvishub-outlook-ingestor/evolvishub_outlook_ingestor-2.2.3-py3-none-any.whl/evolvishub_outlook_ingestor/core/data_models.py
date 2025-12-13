"""
Data models for Evolvishub Outlook Ingestor.

This module defines the core data structures used throughout the library for
representing emails, attachments, folders, and processing results. All models
use Pydantic for validation, serialization, and type safety.

The models are designed to be:
- Comprehensive: Cover all relevant email and metadata fields
- Extensible: Allow for custom fields and future enhancements
- Serializable: Support JSON serialization for storage and transmission
- Type-safe: Provide full type hints for development tools
"""

import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Union
from uuid import UUID

from pydantic import BaseModel, Field, field_validator, ConfigDict


class ProcessingStatus(str, Enum):
    """Processing status enumeration."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    RETRYING = "retrying"


class EmailImportance(str, Enum):
    """Email importance levels."""
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"


class EmailSensitivity(str, Enum):
    """Email sensitivity levels."""
    NORMAL = "normal"
    PERSONAL = "personal"
    PRIVATE = "private"
    CONFIDENTIAL = "confidential"


class AttachmentType(str, Enum):
    """Attachment type enumeration."""
    FILE = "file"
    EMBEDDED_IMAGE = "embedded_image"
    INLINE_ATTACHMENT = "inline_attachment"
    REFERENCE = "reference"


class EmailAddress(BaseModel):
    """Email address model with validation."""
    
    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True,
        extra="allow"
    )
    
    email: str = Field(..., description="Email address")
    name: Optional[str] = Field(None, description="Display name")
    
    @field_validator("email")
    @classmethod
    def validate_email(cls, v: str) -> str:
        """Validate email address format."""
        if "@" not in v or "." not in v.split("@")[-1]:
            raise ValueError("Invalid email address format")
        return v.lower()
    
    def __str__(self) -> str:
        """String representation."""
        if self.name:
            return f"{self.name} <{self.email}>"
        return self.email


class EmailAttachment(BaseModel):
    """Email attachment model."""
    
    model_config = ConfigDict(
        validate_assignment=True,
        extra="allow"
    )
    
    # Basic information
    id: str = Field(..., description="Attachment ID")
    name: str = Field(..., description="Attachment filename")
    content_type: str = Field(..., description="MIME content type")
    size: int = Field(..., description="Attachment size in bytes")
    
    # Type and classification
    attachment_type: AttachmentType = Field(default=AttachmentType.FILE, description="Attachment type")
    is_inline: bool = Field(default=False, description="Is inline attachment")
    content_id: Optional[str] = Field(None, description="Content ID for inline attachments")
    
    # Content
    content: Optional[bytes] = Field(None, description="Attachment content")
    content_location: Optional[str] = Field(None, description="Content storage location")
    
    # Metadata
    created_date: Optional[datetime] = Field(None, description="Creation date")
    modified_date: Optional[datetime] = Field(None, description="Modification date")
    
    # Security
    is_safe: Optional[bool] = Field(None, description="Security scan result")
    scan_result: Optional[str] = Field(None, description="Security scan details")
    
    @field_validator("size")
    @classmethod
    def validate_size(cls, v: int) -> int:
        """Validate attachment size."""
        if v < 0:
            raise ValueError("Attachment size cannot be negative")
        return v


class OutlookFolder(BaseModel):
    """Outlook folder model."""
    
    model_config = ConfigDict(
        validate_assignment=True,
        extra="allow"
    )
    
    # Basic information
    id: str = Field(..., description="Folder ID")
    name: str = Field(..., description="Folder name")
    display_name: str = Field(..., description="Folder display name")
    
    # Hierarchy
    parent_folder_id: Optional[str] = Field(None, description="Parent folder ID")
    folder_path: str = Field(..., description="Full folder path")
    
    # Counts
    total_item_count: int = Field(default=0, description="Total items in folder")
    unread_item_count: int = Field(default=0, description="Unread items count")
    
    # Metadata
    folder_class: Optional[str] = Field(None, description="Folder class")
    is_hidden: bool = Field(default=False, description="Is hidden folder")
    
    # Timestamps
    created_date: Optional[datetime] = Field(None, description="Creation date")
    modified_date: Optional[datetime] = Field(None, description="Last modification date")


class EmailMessage(BaseModel):
    """Comprehensive email message model."""
    
    model_config = ConfigDict(
        validate_assignment=True,
        extra="allow"
    )
        
    # Unique identifiers
    id: Optional[str] = Field(None, description="Message ID")
    message_id: Optional[str] = Field(None, description="Email ID from MsGraph V1.0 API")
    conversation_id: Optional[str] = Field(None, description="Conversation thread ID")
    conversation_index: Optional[str] = Field(None, description="Conversation index")

    # Basic message information
    subject: Optional[str] = Field(None, description="Email subject")
    body: Optional[str] = Field(None, description="Email body content")
    body_html: Optional[str] = Field(None, description="Email body in HTML format")
    body_preview: Optional[str] = Field(None, description="Body preview/snippet")
    body_text: Optional[str] = Field(None, description="Plain text body content")
    unique_body: Optional[str] = Field(None, description="Latest message content only (from Microsoft Graph API uniqueBody)")
    unique_body_content_type: Optional[str] = Field(None, description="Content type of unique_body (html or text)")
    email_address_source: Optional[str] = Field(None, description="Email address source")

    # Content format
    body_type: str = Field(default="text", description="Body content type (text/html)")
    is_html: bool = Field(default=False, description="Is HTML content")
    
    # Participants
    sender: Optional[EmailAddress] = Field(None, description="Sender address")
    from_address: Optional[EmailAddress] = Field(None, description="From address")
    to_recipients: List[EmailAddress] = Field(default_factory=list, description="To recipients")
    cc_recipients: List[EmailAddress] = Field(default_factory=list, description="CC recipients")
    bcc_recipients: List[EmailAddress] = Field(default_factory=list, description="BCC recipients")
    reply_to: List[EmailAddress] = Field(default_factory=list, description="Reply-to addresses")
    
    # Timestamps
    sent_datetime: Optional[datetime] = Field(None, description="Sent datetime")
    received_datetime: Optional[datetime] = Field(None, description="Received datetime")
    created_datetime: Optional[datetime] = Field(None, description="Creation datetime")
    modified_datetime: Optional[datetime] = Field(None, description="Last modification datetime")

    # Message properties
    importance: EmailImportance = Field(default=EmailImportance.NORMAL, description="Message importance")
    sensitivity: EmailSensitivity = Field(default=EmailSensitivity.NORMAL, description="Message sensitivity")
    priority: Optional[str] = Field(None, description="Message priority")
    
    # Status flags
    is_read: bool = Field(default=False, description="Is message read")
    is_draft: bool = Field(default=False, description="Is draft message")
    has_attachments: bool = Field(default=False, description="Has attachments")
    is_flagged: bool = Field(default=False, description="Is flagged")
    
    # Folder information
    parent_folder_id: Optional[str] = Field(None, description="Containing folder ID")
    folder_path: Optional[str] = Field(None, description="Folder path")
    
    # Attachments
    attachments: List[EmailAttachment] = Field(default_factory=list, description="Email attachments")
    
    # Headers and metadata
    headers: Dict[str, str] = Field(default_factory=dict, description="Email headers")
    internet_headers: Dict[str, str] = Field(default_factory=dict, description="Internet headers")
    
    # Categories and classification
    categories: List[str] = Field(default_factory=list, description="Message categories")
    
    # Threading information
    in_reply_to: Optional[str] = Field(None, description="In-Reply-To header")
    references: List[str] = Field(default_factory=list, description="References header")
    
    # Size information
    size: Optional[int] = Field(None, description="Message size in bytes")

    # Business relevance flag
    is_valid_email : Optional[bool] = Field(False, description="Is valid business email")
    
    # Custom properties
    extended_properties: Dict[str, Any] = Field(default_factory=dict, description="Extended properties")


class ProcessingResult(BaseModel):
    """Processing operation result model."""
    
    model_config = ConfigDict(
        validate_assignment=True,
        extra="allow"
    )
    
    # Operation identification
    operation_id: UUID = Field(default_factory=uuid.uuid4, description="Operation ID")
    correlation_id: Optional[str] = Field(None, description="Correlation ID")
    
    # Status and timing
    status: ProcessingStatus = Field(..., description="Processing status")
    start_time: datetime = Field(default_factory=datetime.utcnow, description="Start time")
    end_time: Optional[datetime] = Field(None, description="End time")
    duration_seconds: Optional[float] = Field(None, description="Duration in seconds")
    
    # Processing statistics
    total_items: int = Field(default=0, description="Total items processed")
    successful_items: int = Field(default=0, description="Successfully processed items")
    failed_items: int = Field(default=0, description="Failed items")
    skipped_items: int = Field(default=0, description="Skipped items")
    
    # Error information
    error_message: Optional[str] = Field(None, description="Error message")
    error_details: Optional[Dict[str, Any]] = Field(None, description="Error details")
    warnings: List[str] = Field(default_factory=list, description="Warning messages")
    
    # Performance metrics
    items_per_second: Optional[float] = Field(None, description="Processing rate")
    memory_usage_mb: Optional[float] = Field(None, description="Peak memory usage")
    
    # Results data
    emails: List[EmailMessage] = Field(default_factory=list, description="Processed email messages")
    processed_items: int = Field(0, description="Number of processed items")
    results: List[Dict[str, Any]] = Field(default_factory=list, description="Processing results")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")
    
    def calculate_duration(self) -> None:
        """Calculate duration if end_time is set."""
        if self.end_time and self.start_time:
            self.duration_seconds = (self.end_time - self.start_time).total_seconds()
    
    def calculate_rate(self) -> None:
        """Calculate processing rate."""
        if self.duration_seconds and self.duration_seconds > 0:
            self.items_per_second = self.successful_items / self.duration_seconds


class BatchProcessingConfig(BaseModel):
    """Batch processing configuration model with multi-user support."""

    model_config = ConfigDict(
        validate_assignment=True,
        extra="allow"
    )

    batch_size: int = Field(default=100, description="Batch size for email processing")
    max_workers: int = Field(default=4, description="Maximum worker threads")
    timeout_seconds: int = Field(default=300, description="Batch timeout")
    retry_attempts: int = Field(default=3, description="Retry attempts")

    # Multi-user processing configuration
    max_concurrent_users: int = Field(default=5, description="Maximum concurrent users to process")
    max_concurrent_batches: int = Field(default=3, description="Maximum concurrent batches per user")
    user_processing_delay: float = Field(default=0.5, description="Delay between user processing starts (seconds)")

    # Rate limiting for Microsoft Graph API
    requests_per_minute: int = Field(default=100, description="Requests per minute per user")
    burst_limit: int = Field(default=20, description="Burst request limit")

    # Memory management
    max_memory_mb: int = Field(default=1024, description="Maximum memory usage")
    memory_check_interval: int = Field(default=100, description="Memory check interval")

    # Progress tracking
    progress_callback: Optional[Any] = Field(default=None, description="Progress callback function")
    enable_progress_tracking: bool = Field(default=True, description="Enable progress tracking")

    # Error handling
    fail_fast: bool = Field(default=False, description="Stop processing on first user failure")
    continue_on_user_error: bool = Field(default=True, description="Continue processing other users if one fails")


@dataclass
class UserProcessingResult:
    """Result of processing emails for a single user."""
    user_id: str
    status: ProcessingStatus
    total_emails: int = 0
    processed_emails: int = 0
    failed_emails: int = 0
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    error_message: Optional[str] = None
    folders_processed: List[str] = field(default_factory=list)

    @property
    def success_rate(self) -> float:
        """Calculate success rate for this user."""
        total_processed = self.processed_emails + self.failed_emails
        if total_processed == 0:
            return 100.0
        return (self.processed_emails / total_processed) * 100

    @property
    def duration_seconds(self) -> float:
        """Calculate processing duration in seconds."""
        if self.start_time and self.end_time:
            return (self.end_time - self.start_time).total_seconds()
        return 0.0


@dataclass
class MultiUserProcessingResult:
    """Result of processing emails for multiple users."""
    operation_id: str
    status: ProcessingStatus
    total_users: int = 0
    successful_users: int = 0
    failed_users: int = 0
    total_emails: int = 0
    processed_emails: int = 0
    failed_emails: int = 0
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    user_results: Dict[str, UserProcessingResult] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)

    @property
    def success_rate(self) -> float:
        """Calculate overall success rate."""
        if self.total_users == 0:
            return 100.0
        return (self.successful_users / self.total_users) * 100

    @property
    def email_success_rate(self) -> float:
        """Calculate email processing success rate."""
        total_processed = self.processed_emails + self.failed_emails
        if total_processed == 0:
            return 100.0
        return (self.processed_emails / total_processed) * 100

    @property
    def duration_seconds(self) -> float:
        """Calculate total processing duration in seconds."""
        if self.start_time and self.end_time:
            return (self.end_time - self.start_time).total_seconds()
        return 0.0

    def add_user_result(self, user_result: UserProcessingResult) -> None:
        """Add a user processing result."""
        self.user_results[user_result.user_id] = user_result

        # Update aggregated statistics
        self.total_emails += user_result.total_emails
        self.processed_emails += user_result.processed_emails
        self.failed_emails += user_result.failed_emails

        if user_result.status == ProcessingStatus.COMPLETED:
            self.successful_users += 1
        else:
            self.failed_users += 1
