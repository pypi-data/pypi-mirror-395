"""
Email Ingestor Protocol for Microsoft Graph API integration.

This module provides a focused, production-ready email ingestion protocol with:
- Complete email CRUD operations
- Advanced search and filtering
- Batch processing capabilities
- Error handling and retry mechanisms
- Progress tracking and monitoring
- Configurable data transformation
- Multiple output format support

This is a pure data ingestion library designed for easy integration
with other microservices and applications.
"""

import asyncio
import warnings
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional, Union, AsyncGenerator, Callable
from urllib.parse import urlencode
import json
import logging
from dataclasses import dataclass

from evolvishub_outlook_ingestor.core.data_models import (
    EmailMessage,
    EmailAddress,
    EmailAttachment,
    OutlookFolder,
    ProcessingResult,
    ProcessingStatus,
)
from evolvishub_outlook_ingestor.core.exceptions import (
    GraphAPIError,
    ProtocolError,
    ValidationError,
)
from evolvishub_outlook_ingestor.core.logging import LoggerMixin
from evolvishub_outlook_ingestor.utils.retry import retry_with_config


@dataclass
class IngestionConfig:
    """Configuration for email ingestion operations."""
    batch_size: int = 100
    max_concurrent_requests: int = 10
    include_attachments: bool = True
    attachment_size_limit: int = 25 * 1024 * 1024  # 25MB
    retry_attempts: int = 3
    retry_delay: float = 1.0
    progress_callback: Optional[Callable[[int, int], None]] = None
    filter_query: Optional[str] = None
    date_range_start: Optional[datetime] = None
    date_range_end: Optional[datetime] = None


@dataclass
class IngestionProgress:
    """Progress tracking for email ingestion operations."""
    total_emails: int = 0
    processed_emails: int = 0
    failed_emails: int = 0
    current_folder: str = ""
    start_time: Optional[datetime] = None
    estimated_completion: Optional[datetime] = None
    
    @property
    def completion_percentage(self) -> float:
        """Calculate completion percentage."""
        if self.total_emails == 0:
            return 0.0
        return (self.processed_emails / self.total_emails) * 100
    
    @property
    def success_rate(self) -> float:
        """Calculate success rate."""
        total_processed = self.processed_emails + self.failed_emails
        if total_processed == 0:
            return 100.0
        return (self.processed_emails / total_processed) * 100


class EmailIngestorProtocol(LoggerMixin):
    """
    Focused email ingestion protocol for Microsoft Graph API.

    .. deprecated:: 1.3.0
        EmailIngestorProtocol is deprecated and will be removed in version 2.0.0.
        Use GraphAPIAdapter directly for better performance and consistency.

    This protocol provides a clean, simple interface for email ingestion
    operations that can be easily integrated into other applications.

    For new code, use GraphAPIAdapter which provides:
    - Better performance (no wrapper overhead)
    - Consistent interface with other protocols
    - Enhanced error handling and rate limiting
    - Standardized authentication patterns
    """
    
    def __init__(self, graph_adapter):
        """
        Initialize email ingestor protocol.

        .. deprecated:: 1.3.0
            Use GraphAPIAdapter directly instead of wrapping it.

        Args:
            graph_adapter: Microsoft Graph API adapter instance
        """
        # Issue deprecation warning
        warnings.warn(
            "EmailIngestorProtocol is deprecated and will be removed in version 2.0.0. "
            "Use GraphAPIAdapter directly for better performance and consistency. "
            "See migration guide: https://docs.evolvishub.com/migration/email-ingestor-protocol",
            DeprecationWarning,
            stacklevel=2
        )

        self.graph_adapter = graph_adapter
        self.base_url = graph_adapter.base_url if hasattr(graph_adapter, 'base_url') else "https://graph.microsoft.com/v1.0"
        self._progress = IngestionProgress()
        self._semaphore = None
        
    async def initialize(self, config: Optional[IngestionConfig] = None) -> bool:
        """
        Initialize the email ingestor protocol.
        
        Args:
            config: Optional ingestion configuration
            
        Returns:
            True if initialization successful
        """
        try:
            self.config = config or IngestionConfig()
            self._semaphore = asyncio.Semaphore(self.config.max_concurrent_requests)
            
            # Test connection
            await self._test_connection()
            
            self.logger.info("Email ingestor protocol initialized successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to initialize email ingestor protocol: {e}")
            raise ProtocolError(f"Failed to initialize email ingestor protocol: {e}") from e
    
    async def _test_connection(self) -> bool:
        """Test the connection to Microsoft Graph API."""
        try:
            endpoint = "/me/mailFolders/inbox"
            await self.graph_adapter._make_request("GET", endpoint, params={"$top": "1"})
            return True
        except Exception as e:
            self.logger.error(f"Connection test failed: {e}")
            raise
    
    async def get_folders(self, user_id: str = "me") -> List[OutlookFolder]:
        """
        Get all mail folders for a user.
        
        Args:
            user_id: User ID or 'me' for current user
            
        Returns:
            List of OutlookFolder objects
        """
        try:
            endpoint = f"/users/{user_id}/mailFolders"
            response = await self.graph_adapter._make_request("GET", endpoint)
            
            folders = []
            for folder_data in response.get("value", []):
                folder = self._convert_graph_folder(folder_data)
                folders.append(folder)
            
            self.logger.info(f"Retrieved {len(folders)} folders", user_id=user_id)
            return folders
            
        except Exception as e:
            self.logger.error(f"Failed to get folders: {e}", user_id=user_id)
            raise ProtocolError(f"Failed to get folders: {e}") from e
    
    async def get_emails(
        self,
        folder_id: str = "inbox",
        user_id: str = "me",
        limit: Optional[int] = None,
        config: Optional[IngestionConfig] = None
    ) -> List[EmailMessage]:
        """
        Get emails from a specific folder.
        
        Args:
            folder_id: Folder ID to retrieve emails from
            user_id: User ID or 'me' for current user
            limit: Maximum number of emails to return
            config: Optional ingestion configuration
            
        Returns:
            List of EmailMessage objects
        """
        ingestion_config = config or self.config
        
        try:
            endpoint = f"/users/{user_id}/mailFolders/{folder_id}/messages"
            
            # Build query parameters
            params = {}
            
            if ingestion_config.filter_query:
                params["$filter"] = ingestion_config.filter_query
            
            # Add date range filter
            if ingestion_config.date_range_start or ingestion_config.date_range_end:
                date_filters = []
                if ingestion_config.date_range_start:
                    date_filters.append(f"receivedDateTime ge {ingestion_config.date_range_start.isoformat()}Z")
                if ingestion_config.date_range_end:
                    date_filters.append(f"receivedDateTime le {ingestion_config.date_range_end.isoformat()}Z")
                
                if date_filters:
                    if params.get("$filter"):
                        params["$filter"] += " and " + " and ".join(date_filters)
                    else:
                        params["$filter"] = " and ".join(date_filters)
            
            params["$orderby"] = "receivedDateTime desc"
            params["$top"] = str(ingestion_config.batch_size)
            
            # Fetch emails with pagination
            emails = []
            next_link = None
            
            while True:
                if next_link:
                    endpoint = next_link.replace(self.base_url, "")
                    params = {}
                
                response = await self.graph_adapter._make_request("GET", endpoint, params=params)
                
                # Convert emails
                batch_emails = []
                for email_data in response.get("value", []):
                    try:
                        email = self._convert_graph_email(email_data)
                        
                        # Get attachments if configured
                        if ingestion_config.include_attachments and email.has_attachments:
                            email.attachments = await self._get_email_attachments(
                                email.id, user_id, ingestion_config
                            )
                        
                        batch_emails.append(email)
                        
                    except Exception as e:
                        self.logger.warning(f"Failed to process email {email_data.get('id', 'unknown')}: {e}")
                        continue
                
                emails.extend(batch_emails)
                
                # Update progress
                if ingestion_config.progress_callback:
                    ingestion_config.progress_callback(len(emails), limit or len(emails))
                
                # Check for more pages
                next_link = response.get("@odata.nextLink")
                if not next_link or (limit and len(emails) >= limit):
                    break
            
            # Apply limit if specified
            if limit and len(emails) > limit:
                emails = emails[:limit]
            
            self.logger.info(f"Retrieved {len(emails)} emails", folder_id=folder_id, user_id=user_id)
            return emails
            
        except Exception as e:
            self.logger.error(f"Failed to get emails: {e}", folder_id=folder_id, user_id=user_id)
            raise ProtocolError(f"Failed to get emails: {e}") from e
    
    async def search_emails(
        self,
        query: str,
        user_id: str = "me",
        folder_id: Optional[str] = None,
        limit: Optional[int] = None,
        config: Optional[IngestionConfig] = None
    ) -> List[EmailMessage]:
        """
        Search emails with advanced query.
        
        Args:
            query: Search query (supports KQL - Keyword Query Language)
            user_id: User ID or 'me' for current user
            folder_id: Optional folder ID to search within
            limit: Maximum number of results
            config: Optional ingestion configuration
            
        Returns:
            List of EmailMessage objects
        """
        ingestion_config = config or self.config
        
        try:
            if folder_id:
                endpoint = f"/users/{user_id}/mailFolders/{folder_id}/messages"
            else:
                endpoint = f"/users/{user_id}/messages"
            
            params = {
                "$search": f'"{query}"',
                "$orderby": "receivedDateTime desc"
            }
            
            if limit:
                params["$top"] = str(limit)
            
            # Fetch emails with pagination
            emails = []
            next_link = None
            
            while True:
                if next_link:
                    endpoint = next_link.replace(self.base_url, "")
                    params = {}
                
                response = await self.graph_adapter._make_request("GET", endpoint, params=params)
                
                # Convert emails
                for email_data in response.get("value", []):
                    try:
                        email = self._convert_graph_email(email_data)
                        emails.append(email)
                    except Exception as e:
                        self.logger.warning(f"Failed to process search result: {e}")
                        continue
                
                # Check for more pages
                next_link = response.get("@odata.nextLink")
                if not next_link or (limit and len(emails) >= limit):
                    break
            
            # Apply limit if specified
            if limit and len(emails) > limit:
                emails = emails[:limit]
            
            self.logger.info(f"Search found {len(emails)} emails", query=query, user_id=user_id)
            return emails

        except Exception as e:
            self.logger.error(f"Failed to search emails: {e}", query=query, user_id=user_id)
            raise ProtocolError(f"Failed to search emails: {e}") from e

    async def ingest_all_emails(
        self,
        user_id: str = "me",
        folder_ids: Optional[List[str]] = None,
        config: Optional[IngestionConfig] = None
    ) -> IngestionProgress:
        """
        Ingest all emails from specified folders or all folders.

        Args:
            user_id: User ID or 'me' for current user
            folder_ids: List of folder IDs to ingest from (None for all folders)
            config: Optional ingestion configuration

        Returns:
            IngestionProgress object with results
        """
        ingestion_config = config or self.config
        self._progress = IngestionProgress()
        self._progress.start_time = datetime.now(timezone.utc)

        try:
            # Get folders to process
            if folder_ids is None:
                folders = await self.get_folders(user_id)
                folder_ids = [folder.id for folder in folders]

            # Estimate total emails
            total_emails = 0
            for folder_id in folder_ids:
                try:
                    folder_info = await self._get_folder_info(folder_id, user_id)
                    total_emails += folder_info.get("totalItemCount", 0)
                except Exception as e:
                    self.logger.warning(f"Failed to get folder info for {folder_id}: {e}")

            self._progress.total_emails = total_emails

            # Process each folder
            all_emails = []
            for folder_id in folder_ids:
                try:
                    self._progress.current_folder = folder_id
                    self.logger.info(f"Processing folder: {folder_id}")

                    folder_emails = await self.get_emails(
                        folder_id=folder_id,
                        user_id=user_id,
                        config=ingestion_config
                    )

                    all_emails.extend(folder_emails)
                    self._progress.processed_emails += len(folder_emails)

                    # Update progress callback
                    if ingestion_config.progress_callback:
                        ingestion_config.progress_callback(
                            self._progress.processed_emails,
                            self._progress.total_emails
                        )

                except Exception as e:
                    self.logger.error(f"Failed to process folder {folder_id}: {e}")
                    self._progress.failed_emails += 1
                    continue

            # Calculate estimated completion
            if self._progress.start_time:
                elapsed = datetime.now(timezone.utc) - self._progress.start_time
                if self._progress.processed_emails > 0:
                    avg_time_per_email = elapsed.total_seconds() / self._progress.processed_emails
                    remaining_emails = self._progress.total_emails - self._progress.processed_emails
                    remaining_time = timedelta(seconds=avg_time_per_email * remaining_emails)
                    self._progress.estimated_completion = datetime.now(timezone.utc) + remaining_time

            self.logger.info(
                f"Ingestion completed: {self._progress.processed_emails} emails processed, "
                f"{self._progress.failed_emails} failed, "
                f"{self._progress.success_rate:.1f}% success rate"
            )

            return self._progress

        except Exception as e:
            self.logger.error(f"Failed to ingest emails: {e}")
            raise ProtocolError(f"Failed to ingest emails: {e}") from e

    async def get_conversation_thread(
        self,
        conversation_id: str,
        user_id: str = "me"
    ) -> List[EmailMessage]:
        """
        Get all emails in a conversation thread.

        Args:
            conversation_id: Conversation ID
            user_id: User ID or 'me' for current user

        Returns:
            List of EmailMessage objects in the conversation
        """
        try:
            endpoint = f"/users/{user_id}/messages"
            params = {
                "$filter": f"conversationId eq '{conversation_id}'",
                "$orderby": "receivedDateTime asc"
            }

            response = await self.graph_adapter._make_request("GET", endpoint, params=params)

            emails = []
            for email_data in response.get("value", []):
                email = self._convert_graph_email(email_data)
                emails.append(email)

            self.logger.info(f"Retrieved conversation with {len(emails)} emails", conversation_id=conversation_id)
            return emails

        except Exception as e:
            self.logger.error(f"Failed to get conversation: {e}", conversation_id=conversation_id)
            raise ProtocolError(f"Failed to get conversation: {e}") from e

    async def get_delta_emails(
        self,
        folder_id: str = "inbox",
        delta_token: Optional[str] = None,
        user_id: str = "me"
    ) -> Dict[str, Any]:
        """
        Get email changes using delta query for incremental sync.

        Args:
            folder_id: Folder ID to sync
            delta_token: Delta token from previous sync
            user_id: User ID or 'me' for current user

        Returns:
            Dictionary with emails and delta token
        """
        try:
            if delta_token:
                endpoint = f"/users/{user_id}/mailFolders/{folder_id}/messages/delta"
                params = {"$deltatoken": delta_token}
            else:
                endpoint = f"/users/{user_id}/mailFolders/{folder_id}/messages/delta"
                params = {}

            response = await self.graph_adapter._make_request("GET", endpoint, params=params)

            # Process emails
            emails = []
            deleted_email_ids = []

            for item in response.get("value", []):
                if item.get("@removed"):
                    # Deleted email
                    deleted_email_ids.append(item.get("id", ""))
                else:
                    # Added or updated email
                    email = self._convert_graph_email(item)
                    emails.append(email)

            # Extract new delta token
            new_delta_token = None
            delta_link = response.get("@odata.deltaLink")
            if delta_link and "$deltatoken=" in delta_link:
                new_delta_token = delta_link.split("$deltatoken=")[1].split("&")[0]

            result = {
                "emails": emails,
                "deleted_email_ids": deleted_email_ids,
                "delta_token": new_delta_token,
                "has_more": "@odata.nextLink" in response
            }

            self.logger.info(f"Delta sync found {len(emails)} emails, {len(deleted_email_ids)} deleted")
            return result

        except Exception as e:
            self.logger.error(f"Failed to get delta emails: {e}")
            raise ProtocolError(f"Failed to get delta emails: {e}") from e

    async def _get_folder_info(self, folder_id: str, user_id: str = "me") -> Dict[str, Any]:
        """Get folder information including item counts."""
        try:
            endpoint = f"/users/{user_id}/mailFolders/{folder_id}"
            response = await self.graph_adapter._make_request("GET", endpoint)
            return response
        except Exception as e:
            self.logger.warning(f"Failed to get folder info: {e}")
            return {}

    async def _get_email_attachments(
        self,
        email_id: str,
        user_id: str,
        config: IngestionConfig
    ) -> List[EmailAttachment]:
        """Get attachments for an email."""
        try:
            endpoint = f"/users/{user_id}/messages/{email_id}/attachments"
            response = await self.graph_adapter._make_request("GET", endpoint)

            attachments = []
            for attachment_data in response.get("value", []):
                # Check size limit
                size = attachment_data.get("size", 0)
                if size > config.attachment_size_limit:
                    self.logger.warning(f"Skipping large attachment: {size} bytes")
                    continue

                attachment = EmailAttachment(
                    id=attachment_data.get("id", ""),
                    filename=attachment_data.get("name", ""),
                    content_type=attachment_data.get("contentType", ""),
                    size=size,
                    is_inline=attachment_data.get("isInline", False),
                    content_id=attachment_data.get("contentId"),
                    content=attachment_data.get("contentBytes")
                )
                attachments.append(attachment)

            return attachments

        except Exception as e:
            self.logger.warning(f"Failed to get attachments for email {email_id}: {e}")
            return []

    def _convert_graph_email(self, email_data: Dict[str, Any]) -> EmailMessage:
        """Convert Graph API email data to EmailMessage object."""
        # Parse recipients
        recipients = []
        for recipient_data in email_data.get("toRecipients", []):
            email_addr = recipient_data.get("emailAddress", {})
            recipient = EmailAddress(
                address=email_addr.get("address", ""),
                name=email_addr.get("name")
            )
            recipients.append(recipient)

        cc_recipients = []
        for recipient_data in email_data.get("ccRecipients", []):
            email_addr = recipient_data.get("emailAddress", {})
            recipient = EmailAddress(
                address=email_addr.get("address", ""),
                name=email_addr.get("name")
            )
            cc_recipients.append(recipient)

        bcc_recipients = []
        for recipient_data in email_data.get("bccRecipients", []):
            email_addr = recipient_data.get("emailAddress", {})
            recipient = EmailAddress(
                address=email_addr.get("address", ""),
                name=email_addr.get("name")
            )
            bcc_recipients.append(recipient)

        # Parse sender
        sender = None
        sender_data = email_data.get("from", {}).get("emailAddress", {})
        if sender_data.get("address"):
            sender = EmailAddress(
                address=sender_data.get("address", ""),
                name=sender_data.get("name")
            )

        # Parse body
        body_data = email_data.get("body", {})
        body = body_data.get("content", "")
        is_html = body_data.get("contentType", "").lower() == "html"

        return EmailMessage(
            id=email_data.get("id", ""),
            message_id=email_data.get("internetMessageId", ""),
            conversation_id=email_data.get("conversationId"),
            subject=email_data.get("subject", ""),
            body=body,
            is_html=is_html,
            sender=sender,
            recipients=recipients,
            cc_recipients=cc_recipients,
            bcc_recipients=bcc_recipients,
            sent_date=self._parse_datetime(email_data.get("sentDateTime")),
            received_date=self._parse_datetime(email_data.get("receivedDateTime")),
            is_read=email_data.get("isRead", False),
            is_draft=email_data.get("isDraft", False),
            has_attachments=email_data.get("hasAttachments", False),
            attachments=[],  # Will be populated separately if needed
            importance=email_data.get("importance", "normal"),
            categories=email_data.get("categories", []),
            folder_id=email_data.get("parentFolderId"),
            created_date=self._parse_datetime(email_data.get("createdDateTime")),
            last_modified_date=self._parse_datetime(email_data.get("lastModifiedDateTime"))
        )

    def _convert_graph_folder(self, folder_data: Dict[str, Any]) -> OutlookFolder:
        """Convert Graph API folder data to OutlookFolder object."""
        return OutlookFolder(
            id=folder_data.get("id", ""),
            display_name=folder_data.get("displayName", ""),
            parent_folder_id=folder_data.get("parentFolderId"),
            child_folder_count=folder_data.get("childFolderCount", 0),
            unread_item_count=folder_data.get("unreadItemCount", 0),
            total_item_count=folder_data.get("totalItemCount", 0),
            size_in_bytes=folder_data.get("sizeInBytes", 0),
            is_hidden=folder_data.get("isHidden", False)
        )

    def _parse_datetime(self, date_str: Optional[str]) -> Optional[datetime]:
        """Parse datetime string from Graph API."""
        if not date_str:
            return None

        try:
            if date_str.endswith("Z"):
                date_str = date_str[:-1] + "+00:00"
            return datetime.fromisoformat(date_str.replace("Z", "+00:00"))
        except (ValueError, AttributeError):
            return None

    def get_progress(self) -> IngestionProgress:
        """Get current ingestion progress."""
        return self._progress

    async def cleanup(self):
        """Cleanup resources."""
        try:
            # Close any open connections
            if hasattr(self.graph_adapter, 'cleanup'):
                await self.graph_adapter.cleanup()

            self.logger.info("Email ingestor protocol cleanup completed")

        except Exception as e:
            self.logger.error(f"Failed to cleanup email ingestor protocol: {e}")

    async def health_check(self) -> Dict[str, Any]:
        """
        Perform health check.

        Returns:
            Health check results
        """
        health_status = {
            "status": "healthy",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "components": {}
        }

        try:
            # Test connection
            connection_ok = await self._test_connection()
            health_status["components"]["connection"] = "healthy" if connection_ok else "unhealthy"

            # Test folder access
            try:
                folders = await self.get_folders()
                health_status["components"]["folder_access"] = f"healthy ({len(folders)} folders)"
            except Exception as e:
                health_status["components"]["folder_access"] = f"unhealthy: {e}"

            # Determine overall status
            unhealthy_components = [
                comp for comp, status in health_status["components"].items()
                if not status.startswith("healthy")
            ]

            if unhealthy_components:
                health_status["status"] = "unhealthy"

            return health_status

        except Exception as e:
            health_status["status"] = "error"
            health_status["error"] = str(e)
            return health_status

    # CRUD Operations for Complete Email Management

    async def create_email(
        self,
        email: EmailMessage,
        user_id: str = "me",
        folder_id: str = "drafts",
        save_to_sent_items: bool = True
    ) -> EmailMessage:
        """
        Create a new email message.

        Args:
            email: EmailMessage object to create
            user_id: User ID or 'me' for current user
            folder_id: Folder ID to save the email
            save_to_sent_items: Whether to save to sent items when sent

        Returns:
            Created EmailMessage object

        Raises:
            ProtocolError: If email creation fails
        """
        try:
            endpoint = f"/users/{user_id}/mailFolders/{folder_id}/messages"
            data = self._convert_email_to_graph(email, save_to_sent_items)

            response = await self.graph_adapter._make_request("POST", endpoint, data=data)

            created_email = self._convert_graph_email(response)
            self.logger.info("Created email", subject=email.subject, user_id=user_id)
            return created_email

        except Exception as e:
            self.logger.error(f"Failed to create email: {e}", subject=email.subject, user_id=user_id)
            raise ProtocolError(f"Failed to create email: {e}") from e

    async def update_email(
        self,
        email: EmailMessage,
        user_id: str = "me"
    ) -> EmailMessage:
        """
        Update an existing email message.

        Args:
            email: EmailMessage object with updates
            user_id: User ID or 'me' for current user

        Returns:
            Updated EmailMessage object

        Raises:
            ProtocolError: If email update fails
        """
        try:
            endpoint = f"/users/{user_id}/messages/{email.id}"
            data = self._convert_email_to_graph(email)

            response = await self.graph_adapter._make_request("PATCH", endpoint, data=data)

            updated_email = self._convert_graph_email(response)
            self.logger.info("Updated email", email_id=email.id, user_id=user_id)
            return updated_email

        except Exception as e:
            self.logger.error(f"Failed to update email: {e}", email_id=email.id, user_id=user_id)
            raise ProtocolError(f"Failed to update email: {e}") from e

    async def delete_email(
        self,
        email_id: str,
        user_id: str = "me",
        permanent: bool = False
    ) -> bool:
        """
        Delete an email message.

        Args:
            email_id: Email ID to delete
            user_id: User ID or 'me' for current user
            permanent: Whether to permanently delete (true) or move to deleted items (false)

        Returns:
            True if deletion successful

        Raises:
            ProtocolError: If email deletion fails
        """
        try:
            if permanent:
                # Permanently delete
                endpoint = f"/users/{user_id}/messages/{email_id}"
                await self.graph_adapter._make_request("DELETE", endpoint)
            else:
                # Move to deleted items
                endpoint = f"/users/{user_id}/messages/{email_id}/move"
                data = {"destinationId": "deleteditems"}
                await self.graph_adapter._make_request("POST", endpoint, data=data)

            self.logger.info("Deleted email", email_id=email_id, permanent=permanent, user_id=user_id)
            return True

        except Exception as e:
            self.logger.error(f"Failed to delete email: {e}", email_id=email_id, user_id=user_id)
            raise ProtocolError(f"Failed to delete email: {e}") from e

    async def send_email(
        self,
        email: EmailMessage,
        user_id: str = "me",
        save_to_sent_items: bool = True
    ) -> bool:
        """
        Send an email message.

        Args:
            email: EmailMessage object to send
            user_id: User ID or 'me' for current user
            save_to_sent_items: Whether to save to sent items

        Returns:
            True if sending successful

        Raises:
            ProtocolError: If email sending fails
        """
        try:
            endpoint = f"/users/{user_id}/sendMail"
            data = {
                "message": self._convert_email_to_graph(email),
                "saveToSentItems": save_to_sent_items
            }

            await self.graph_adapter._make_request("POST", endpoint, data=data)

            self.logger.info("Sent email", subject=email.subject, user_id=user_id)
            return True

        except Exception as e:
            self.logger.error(f"Failed to send email: {e}", subject=email.subject, user_id=user_id)
            raise ProtocolError(f"Failed to send email: {e}") from e

    def _convert_email_to_graph(self, email: EmailMessage, save_to_sent_items: bool = True) -> Dict[str, Any]:
        """
        Convert EmailMessage object to Microsoft Graph API format.

        Args:
            email: EmailMessage object to convert
            save_to_sent_items: Whether to save to sent items

        Returns:
            Dictionary in Microsoft Graph API format
        """
        data = {
            "subject": email.subject,
            "body": {
                "contentType": "html" if email.is_html else "text",
                "content": email.body
            },
            "importance": email.importance or "normal"
        }

        # Add sender (from)
        if email.sender:
            data["from"] = {
                "emailAddress": {
                    "address": email.sender.address,
                    "name": email.sender.name
                }
            }

        # Add recipients
        if email.recipients:
            data["toRecipients"] = [
                {
                    "emailAddress": {
                        "address": recipient.address,
                        "name": recipient.name
                    }
                }
                for recipient in email.recipients
            ]

        # Add CC recipients
        if email.cc_recipients:
            data["ccRecipients"] = [
                {
                    "emailAddress": {
                        "address": recipient.address,
                        "name": recipient.name
                    }
                }
                for recipient in email.cc_recipients
            ]

        # Add BCC recipients
        if email.bcc_recipients:
            data["bccRecipients"] = [
                {
                    "emailAddress": {
                        "address": recipient.address,
                        "name": recipient.name
                    }
                }
                for recipient in email.bcc_recipients
            ]

        # Add categories
        if email.categories:
            data["categories"] = email.categories

        return data
