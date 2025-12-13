"""
IMAP/POP3 protocol adapter for Evolvishub Outlook Ingestor.

This module implements the IMAP/POP3 protocol adapter for accessing
Outlook emails using standard email protocols with async support.

Features:
- Async IMAP operations using aioimaplib
- SSL/TLS connection support
- Folder synchronization and email parsing
- Efficient message retrieval with UID tracking
- Email parsing with email library
- Comprehensive error handling
"""

import asyncio
import email
import email.policy
from datetime import datetime, timezone
from email.message import EmailMessage as StdEmailMessage
from typing import Any, AsyncGenerator, Dict, List, Optional, Tuple

import aioimaplib
from aioimaplib import IMAP4_SSL, IMAP4

from evolvishub_outlook_ingestor.core.data_models import (
    EmailAddress,
    EmailAttachment,
    EmailMessage,
    OutlookFolder,
    AttachmentType,
    EmailImportance,
)
from evolvishub_outlook_ingestor.core.exceptions import (
    AuthenticationError,
    IMAPError,
    ProtocolError,
)
from evolvishub_outlook_ingestor.protocols.base_protocol import BaseProtocol
from evolvishub_outlook_ingestor.utils.retry import retry_with_config, RetryConfig


class IMAPAdapter(BaseProtocol):
    """IMAP/POP3 protocol adapter."""
    
    def __init__(self, name: str, config: Dict[str, Any], **kwargs):
        """
        Initialize IMAP adapter.
        
        Args:
            name: Adapter name
            config: Configuration dictionary containing:
                - server: IMAP server hostname
                - port: IMAP server port (default: 993 for SSL, 143 for non-SSL)
                - username: Username or email address
                - password: Password
                - use_ssl: Use SSL/TLS connection (default: True)
                - timeout: Connection timeout in seconds
        """
        super().__init__(name, config, **kwargs)
        
        # IMAP configuration
        self.server = config.get("server", "outlook.office365.com")
        self.port = config.get("port")
        self.username = config.get("username", "")
        self.password = config.get("password", "")
        self.use_ssl = config.get("use_ssl", True)
        self.timeout = config.get("timeout", 60)
        
        # Set default port based on SSL setting
        if self.port is None:
            self.port = 993 if self.use_ssl else 143
        
        # IMAP connection
        self.imap_client = None
        self.current_folder = None
        
        # UID tracking for efficient synchronization
        self.folder_uid_validity = {}
        self.folder_last_uid = {}
        
        # Retry configuration for IMAP
        self.retry_config = RetryConfig(
            max_attempts=3,
            base_delay=1.0,
            max_delay=30.0,
            retry_on_exceptions=[
                aioimaplib.AioImapException,
                ConnectionError,
                OSError,
            ],
            stop_on_exceptions=[
                AuthenticationError,
            ]
        )
    
    async def _initialize_connection(self) -> None:
        """Initialize connection to IMAP server."""
        if not all([self.username, self.password]):
            raise AuthenticationError(
                "Missing required IMAP credentials",
                auth_method="login",
                context={
                    "username_provided": bool(self.username),
                    "password_provided": bool(self.password),
                }
            )
        
        try:
            # Create IMAP client
            if self.use_ssl:
                self.imap_client = IMAP4_SSL(
                    host=self.server,
                    port=self.port,
                    timeout=self.timeout,
                )
            else:
                self.imap_client = IMAP4(
                    host=self.server,
                    port=self.port,
                    timeout=self.timeout,
                )
            
            self.logger.info(
                "IMAP connection initialized",
                server=self.server,
                port=self.port,
                ssl=self.use_ssl
            )
            
        except Exception as e:
            raise ProtocolError(
                f"Failed to initialize IMAP connection: {e}",
                protocol=self.name,
                server=self.server,
                cause=e
            )
    
    async def _authenticate(self) -> None:
        """Authenticate with IMAP server."""
        try:
            # Wait for connection to be ready
            await self.imap_client.wait_hello_from_server()
            
            # Login to server
            response = await self.imap_client.login(self.username, self.password)
            
            if response.result != 'OK':
                raise AuthenticationError(
                    f"IMAP authentication failed: {response.lines}",
                    auth_method="login",
                    username=self.username,
                    context={"imap_response": str(response.lines)}
                )
            
            self.logger.info("IMAP authentication successful", username=self.username)
            
        except aioimaplib.AioImapException as e:
            raise AuthenticationError(
                f"IMAP authentication failed: {e}",
                auth_method="login",
                username=self.username,
                cause=e
            )
        except Exception as e:
            raise IMAPError(
                f"IMAP connection error: {e}",
                imap_response=str(e),
                cause=e
            )
    
    async def _cleanup_connection(self) -> None:
        """Cleanup connection resources."""
        if self.imap_client:
            try:
                await self.imap_client.logout()
            except Exception as e:
                self.logger.warning("Error during IMAP logout", error=str(e))
            finally:
                self.imap_client = None
        
        self.current_folder = None
        self.folder_uid_validity.clear()
        self.folder_last_uid.clear()
    
    async def _select_folder(self, folder_name: str) -> None:
        """Select IMAP folder."""
        if self.current_folder == folder_name:
            return
        
        try:
            response = await self.imap_client.select(folder_name)
            
            if response.result != 'OK':
                raise IMAPError(
                    f"Failed to select folder '{folder_name}': {response.lines}",
                    imap_response=str(response.lines)
                )
            
            self.current_folder = folder_name
            
            # Update UID validity tracking
            for line in response.lines:
                if b'UIDVALIDITY' in line:
                    uid_validity = int(line.split(b'UIDVALIDITY ')[1].split(b']')[0])
                    self.folder_uid_validity[folder_name] = uid_validity
                    break
            
        except aioimaplib.AioImapException as e:
            raise IMAPError(
                f"IMAP folder selection failed: {e}",
                imap_response=str(e),
                cause=e
            )
    
    async def _fetch_emails_impl(
        self,
        folder_filters: Optional[List[str]] = None,
        date_range: Optional[Dict[str, datetime]] = None,
        limit: Optional[int] = None,
        include_attachments: bool = True,
        **kwargs
    ) -> List[EmailMessage]:
        """Fetch emails from IMAP server."""
        emails = []
        
        # Get folders to process
        folders = await self.get_folders()
        if folder_filters:
            folders = [f for f in folders if f.name in folder_filters]
        
        # Process each folder
        for folder in folders:
            try:
                folder_emails = await self._fetch_folder_emails(
                    folder.name,
                    date_range=date_range,
                    limit=limit - len(emails) if limit else None,
                    include_attachments=include_attachments,
                    **kwargs
                )
                emails.extend(folder_emails)
                
                if limit and len(emails) >= limit:
                    emails = emails[:limit]
                    break
                    
            except Exception as e:
                self.logger.warning(
                    "Failed to process folder",
                    folder_name=folder.name,
                    error=str(e)
                )
                continue
        
        return emails
    
    async def _fetch_folder_emails(
        self,
        folder_name: str,
        date_range: Optional[Dict[str, datetime]] = None,
        limit: Optional[int] = None,
        include_attachments: bool = True,
        **kwargs
    ) -> List[EmailMessage]:
        """Fetch emails from a specific folder."""
        await self._select_folder(folder_name)
        
        # Build search criteria
        search_criteria = ['ALL']
        
        if date_range:
            if 'start' in date_range:
                date_str = date_range['start'].strftime('%d-%b-%Y')
                search_criteria = ['SINCE', date_str]
            if 'end' in date_range:
                date_str = date_range['end'].strftime('%d-%b-%Y')
                if len(search_criteria) > 1:
                    search_criteria.extend(['BEFORE', date_str])
                else:
                    search_criteria = ['BEFORE', date_str]
        
        try:
            # Search for messages
            response = await self.imap_client.search(*search_criteria)
            
            if response.result != 'OK':
                raise IMAPError(
                    f"IMAP search failed: {response.lines}",
                    imap_response=str(response.lines)
                )
            
            # Get message UIDs
            message_uids = []
            for line in response.lines:
                if line:
                    uids = line.decode().split()
                    message_uids.extend(uids)
            
            # Apply limit
            if limit and len(message_uids) > limit:
                message_uids = message_uids[-limit:]  # Get most recent
            
            # Fetch messages
            emails = []
            for uid in message_uids:
                try:
                    email = await self._fetch_message_by_uid(uid, include_attachments)
                    if email:
                        emails.append(email)
                except Exception as e:
                    self.logger.warning(
                        "Failed to fetch message",
                        uid=uid,
                        folder=folder_name,
                        error=str(e)
                    )
                    continue
            
            return emails
            
        except aioimaplib.AioImapException as e:
            raise IMAPError(
                f"IMAP fetch failed: {e}",
                imap_response=str(e),
                cause=e
            )

    async def _fetch_message_by_uid(self, uid: str, include_attachments: bool = True) -> Optional[EmailMessage]:
        """Fetch a single message by UID."""
        try:
            # Fetch message headers and body
            response = await self.imap_client.fetch(uid, '(RFC822)')

            if response.result != 'OK':
                return None

            # Parse email message
            raw_email = None
            for line in response.lines:
                if isinstance(line, bytes) and line.startswith(b'* '):
                    # Find the RFC822 content
                    parts = line.split(b'RFC822 ')
                    if len(parts) > 1:
                        raw_email = parts[1]
                        break

            if not raw_email:
                return None

            # Parse with email library
            msg = email.message_from_bytes(raw_email, policy=email.policy.default)

            # Convert to EmailMessage
            return self._convert_email_message(msg, uid, include_attachments)

        except Exception as e:
            self.logger.warning(
                "Failed to fetch message by UID",
                uid=uid,
                error=str(e)
            )
            return None

    def _convert_email_message(
        self,
        msg: StdEmailMessage,
        uid: str,
        include_attachments: bool = True
    ) -> EmailMessage:
        """Convert standard email message to EmailMessage."""
        # Extract basic information
        email_id = uid
        subject = msg.get('Subject', '')
        message_id = msg.get('Message-ID', '')

        # Extract body content
        body_content = ''
        body_type = 'text'

        if msg.is_multipart():
            # Handle multipart messages
            for part in msg.walk():
                content_type = part.get_content_type()
                if content_type == 'text/plain' and not body_content:
                    body_content = part.get_content()
                    body_type = 'text'
                elif content_type == 'text/html':
                    body_content = part.get_content()
                    body_type = 'html'
        else:
            # Handle single part messages
            content_type = msg.get_content_type()
            body_content = msg.get_content()
            body_type = 'html' if content_type == 'text/html' else 'text'

        # Parse sender and recipients
        sender = self._parse_email_address(msg.get('From', ''))
        from_address = sender

        to_recipients = self._parse_email_addresses(msg.get('To', ''))
        cc_recipients = self._parse_email_addresses(msg.get('Cc', ''))
        bcc_recipients = self._parse_email_addresses(msg.get('Bcc', ''))
        reply_to = self._parse_email_addresses(msg.get('Reply-To', ''))

        # Parse dates
        sent_date = self._parse_email_date(msg.get('Date'))
        received_date = sent_date  # IMAP doesn't provide separate received date

        # Parse importance (X-Priority header)
        importance = EmailImportance.NORMAL
        priority = msg.get('X-Priority', '').strip()
        if priority in ['1', '2']:
            importance = EmailImportance.HIGH
        elif priority in ['4', '5']:
            importance = EmailImportance.LOW

        # Parse flags (would need IMAP FLAGS response for accurate info)
        is_read = False  # Default, would need FLAGS to determine
        is_draft = False

        # Parse headers
        headers = dict(msg.items())

        # Process attachments
        attachments = []
        has_attachments = False

        if include_attachments and msg.is_multipart():
            attachments = self._extract_attachments(msg)
            has_attachments = len(attachments) > 0

        # Calculate size (approximate)
        size = len(str(msg))

        # Create EmailMessage
        email = EmailMessage(
            id=email_id,
            message_id=message_id,
            subject=subject,
            body=body_content,
            body_type=body_type,
            is_html=(body_type == 'html'),
            sender=sender,
            from_address=from_address,
            to_recipients=to_recipients,
            cc_recipients=cc_recipients,
            bcc_recipients=bcc_recipients,
            reply_to=reply_to,
            sent_date=sent_date,
            received_date=received_date,
            importance=importance,
            is_read=is_read,
            is_draft=is_draft,
            has_attachments=has_attachments,
            folder_id=self.current_folder,
            folder_path=f"/{self.current_folder}",
            attachments=attachments,
            headers=headers,
            internet_headers=headers,
            size=size,
        )

        return email

    def _parse_email_address(self, addr_str: str) -> Optional[EmailAddress]:
        """Parse email address string."""
        if not addr_str:
            return None

        try:
            # Use email.utils to parse address
            import email.utils
            name, email_addr = email.utils.parseaddr(addr_str)

            if not email_addr:
                return None

            return EmailAddress(email=email_addr, name=name or '')

        except Exception:
            return None

    def _parse_email_addresses(self, addr_str: str) -> List[EmailAddress]:
        """Parse multiple email addresses from string."""
        if not addr_str:
            return []

        addresses = []
        try:
            import email.utils
            parsed_addresses = email.utils.getaddresses([addr_str])

            for name, email_addr in parsed_addresses:
                if email_addr:
                    addresses.append(EmailAddress(email=email_addr, name=name or ''))

        except Exception:
            pass

        return addresses

    def _parse_email_date(self, date_str: Optional[str]) -> Optional[datetime]:
        """Parse email date string."""
        if not date_str:
            return None

        try:
            import email.utils
            timestamp = email.utils.parsedate_to_datetime(date_str)

            # Convert to UTC if timezone aware
            if timestamp.tzinfo:
                timestamp = timestamp.astimezone(timezone.utc).replace(tzinfo=None)

            return timestamp

        except Exception:
            return None

    def _extract_attachments(self, msg: StdEmailMessage) -> List[EmailAttachment]:
        """Extract attachments from email message."""
        attachments = []

        for part in msg.walk():
            # Skip multipart containers
            if part.get_content_maintype() == 'multipart':
                continue

            # Skip text parts that are not attachments
            content_disposition = part.get('Content-Disposition', '')
            if 'attachment' not in content_disposition and part.get_content_type().startswith('text/'):
                continue

            # Extract attachment information
            filename = part.get_filename()
            if not filename:
                continue

            content_type = part.get_content_type()
            content_id = part.get('Content-ID')
            is_inline = 'inline' in content_disposition

            # Get attachment content
            content = None
            size = 0
            try:
                content = part.get_content()
                if isinstance(content, str):
                    content = content.encode('utf-8')
                size = len(content) if content else 0
            except Exception as e:
                self.logger.warning(
                    "Failed to extract attachment content",
                    filename=filename,
                    error=str(e)
                )

            # Determine attachment type
            attachment_type = AttachmentType.INLINE_ATTACHMENT if is_inline else AttachmentType.FILE

            attachment = EmailAttachment(
                id=f"{self.current_folder}_{filename}_{hash(content_id or filename)}",
                name=filename,
                content_type=content_type,
                size=size,
                attachment_type=attachment_type,
                is_inline=is_inline,
                content_id=content_id,
                content=content,
            )

            attachments.append(attachment)

        return attachments

    async def _fetch_emails_stream_impl(
        self,
        folder_filters: Optional[List[str]] = None,
        date_range: Optional[Dict[str, datetime]] = None,
        batch_size: int = 100,
        include_attachments: bool = True,
        **kwargs
    ) -> AsyncGenerator[List[EmailMessage], None]:
        """Stream emails in batches."""
        # Get folders to process
        folders = await self.get_folders()
        if folder_filters:
            folders = [f for f in folders if f.name in folder_filters]

        # Process each folder
        for folder in folders:
            async for batch in self._stream_folder_emails(
                folder.name,
                date_range=date_range,
                batch_size=batch_size,
                include_attachments=include_attachments,
                **kwargs
            ):
                yield batch

    async def _get_folders_impl(self) -> List[OutlookFolder]:
        """Fetch folder list from IMAP server."""
        try:
            # List all folders
            response = await self.imap_client.list()

            if response.result != 'OK':
                raise IMAPError(
                    f"IMAP list failed: {response.lines}",
                    imap_response=str(response.lines)
                )

            folders = []
            for line in response.lines:
                if isinstance(line, bytes):
                    folder = self._parse_folder_line(line.decode())
                    if folder:
                        folders.append(folder)

            return folders

        except aioimaplib.AioImapException as e:
            raise IMAPError(
                f"IMAP folder list failed: {e}",
                imap_response=str(e),
                cause=e
            )

    def _parse_folder_line(self, line: str) -> Optional[OutlookFolder]:
        """Parse IMAP LIST response line."""
        try:
            # Parse LIST response: * LIST (flags) "delimiter" "name"
            import re

            # Simple regex to extract folder name
            match = re.search(r'"([^"]*)"$', line)
            if not match:
                # Try without quotes
                parts = line.split()
                if len(parts) >= 3:
                    folder_name = parts[-1]
                else:
                    return None
            else:
                folder_name = match.group(1)

            if not folder_name:
                return None

            # Skip system folders that start with special characters
            if folder_name.startswith('[') or folder_name.startswith('\\'):
                return None

            return OutlookFolder(
                id=folder_name,
                name=folder_name,
                display_name=folder_name,
                folder_path=f"/{folder_name}",
                total_item_count=0,  # IMAP doesn't provide this easily
                unread_item_count=0,  # Would need STATUS command
            )

        except Exception as e:
            self.logger.warning(
                "Failed to parse folder line",
                line=line,
                error=str(e)
            )
            return None
