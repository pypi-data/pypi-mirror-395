"""
Thread Builder for constructing email conversation threads.

This module provides utilities for grouping emails by conversation_id
and constructing conversation threads for thread-based classification.
"""

from typing import List, Dict, Optional, Set
from datetime import datetime
from collections import defaultdict
import logging

from .data_models import EmailMessage, EmailAddress

logger = logging.getLogger(__name__)


class ConversationThread:
    """Represents an email conversation thread."""
    
    def __init__(self, conversation_id: str):
        """
        Initialize a conversation thread.
        
        Args:
            conversation_id: Unique conversation identifier from Microsoft Graph API
        """
        self.conversation_id = conversation_id
        self.messages: List[EmailMessage] = []
        self.participants: Set[str] = set()
        self.subject: Optional[str] = None
        self.subject_normalized: Optional[str] = None
        self.first_message_date: Optional[datetime] = None
        self.last_message_date: Optional[datetime] = None
    
    def add_message(self, message: EmailMessage) -> None:
        """
        Add a message to the thread.
        
        Args:
            message: Email message to add
        """
        self.messages.append(message)
        
        # Update participants
        if message.sender_email:
            self.participants.add(message.sender_email)
        
        # Update subject (use first non-empty subject)
        if not self.subject and message.subject:
            self.subject = message.subject
            self.subject_normalized = self._normalize_subject(message.subject)
        
        # Update date range
        if message.received_date:
            if not self.first_message_date or message.received_date < self.first_message_date:
                self.first_message_date = message.received_date
            if not self.last_message_date or message.received_date > self.last_message_date:
                self.last_message_date = message.received_date
    
    def sort_messages(self) -> None:
        """Sort messages chronologically by received_date."""
        self.messages.sort(key=lambda m: m.received_date or datetime.min)
    
    @staticmethod
    def _normalize_subject(subject: str) -> str:
        """
        Normalize email subject by removing RE:, FW:, etc.
        
        Args:
            subject: Original email subject
            
        Returns:
            Normalized subject
        """
        if not subject:
            return ""
        
        # Remove common prefixes
        prefixes = ['re:', 'fw:', 'fwd:', 'aw:', 'wg:']
        normalized = subject.lower().strip()
        
        for prefix in prefixes:
            while normalized.startswith(prefix):
                normalized = normalized[len(prefix):].strip()
        
        return normalized
    
    @property
    def message_count(self) -> int:
        """Number of messages in thread."""
        return len(self.messages)
    
    @property
    def participant_count(self) -> int:
        """Number of unique participants."""
        return len(self.participants)
    
    def to_dict(self) -> Dict:
        """
        Convert thread to dictionary representation.
        
        Returns:
            Dictionary with thread metadata
        """
        return {
            'conversation_id': self.conversation_id,
            'subject': self.subject,
            'subject_normalized': self.subject_normalized,
            'message_count': self.message_count,
            'participant_count': self.participant_count,
            'first_message_date': self.first_message_date.isoformat() if self.first_message_date else None,
            'last_message_date': self.last_message_date.isoformat() if self.last_message_date else None,
            'participants': list(self.participants)
        }


class ThreadBuilder:
    """
    Builder for constructing email conversation threads.
    
    Groups emails by conversation_id and provides utilities for
    thread construction and text generation for classification.
    """
    
    def __init__(self, max_thread_length: int = 4000):
        """
        Initialize ThreadBuilder.
        
        Args:
            max_thread_length: Maximum token length for thread text (default: 4000)
        """
        self.max_thread_length = max_thread_length
        self.logger = logging.getLogger(__name__)
    
    def group_by_conversation(self, emails: List[EmailMessage]) -> Dict[str, ConversationThread]:
        """
        Group emails by conversation_id.
        
        Args:
            emails: List of email messages
            
        Returns:
            Dictionary mapping conversation_id to ConversationThread
        """
        threads: Dict[str, ConversationThread] = {}
        emails_without_conversation_id = []
        
        for email in emails:
            if email.conversation_id:
                # Add to existing thread or create new one
                if email.conversation_id not in threads:
                    threads[email.conversation_id] = ConversationThread(email.conversation_id)
                threads[email.conversation_id].add_message(email)
            else:
                # Track emails without conversation_id for fallback processing
                emails_without_conversation_id.append(email)
        
        # Sort messages in each thread chronologically
        for thread in threads.values():
            thread.sort_messages()
        
        if emails_without_conversation_id:
            self.logger.warning(
                f"Found {len(emails_without_conversation_id)} emails without conversation_id. "
                "These will be processed individually."
            )
        
        return threads
    
    def construct_thread_text(
        self,
        thread: ConversationThread,
        include_metadata: bool = True,
        truncate: bool = True
    ) -> str:
        """
        Construct classification input text from conversation thread.
        
        Args:
            thread: Conversation thread
            include_metadata: Whether to include email metadata (sender, date)
            truncate: Whether to apply smart truncation for long threads
            
        Returns:
            Formatted thread text for classification
        """
        if not thread.messages:
            return ""
        
        # Check if truncation is needed
        if truncate and thread.message_count > 10:
            # Smart truncation: keep first 3 + last 5 emails
            messages_to_include = thread.messages[:3] + thread.messages[-5:]
            truncated = True
        else:
            messages_to_include = thread.messages
            truncated = False
        
        # Build thread text
        parts = []
        
        if include_metadata:
            parts.append(f"=== EMAIL CONVERSATION THREAD ===")
            parts.append(f"Subject: {thread.subject or '(No Subject)'}")
            parts.append(f"Participants: {thread.participant_count}")
            parts.append(f"Messages: {thread.message_count}")
            parts.append("")
        
        for i, message in enumerate(messages_to_include, 1):
            # Check if this is a truncation point
            if truncated and i == 4:
                parts.append(f"\n... [{thread.message_count - 8} messages omitted] ...\n")
            
            # Email header
            if include_metadata:
                parts.append(f"=== Email {i} ({message.received_date or 'Unknown Date'}) ===")
                parts.append(f"From: {message.sender_email or 'Unknown'}")
                if message.subject:
                    parts.append(f"Subject: {message.subject}")
                parts.append("")
            
            # Email body
            body = message.body_text or message.body_preview or "(No content)"
            parts.append(body.strip())
            parts.append("")
        
        thread_text = "\n".join(parts)
        
        # Final length check and truncation if needed
        if len(thread_text) > self.max_thread_length * 4:  # Rough estimate: 4 chars per token
            self.logger.warning(
                f"Thread {thread.conversation_id} exceeds max length. "
                f"Truncating from {len(thread_text)} to ~{self.max_thread_length * 4} characters."
            )
            thread_text = thread_text[:self.max_thread_length * 4] + "\n\n[Thread truncated due to length]"
        
        return thread_text
    
    def get_thread_metadata(self, thread: ConversationThread) -> Dict:
        """
        Extract metadata from conversation thread.
        
        Args:
            thread: Conversation thread
            
        Returns:
            Dictionary with thread metadata
        """
        return {
            'conversation_id': thread.conversation_id,
            'subject': thread.subject,
            'subject_normalized': thread.subject_normalized,
            'message_count': thread.message_count,
            'participant_count': thread.participant_count,
            'first_message_date': thread.first_message_date,
            'last_message_date': thread.last_message_date,
            'participants': list(thread.participants),
            'first_email_id': thread.messages[0].id if thread.messages else None,
            'last_email_id': thread.messages[-1].id if thread.messages else None,
        }

