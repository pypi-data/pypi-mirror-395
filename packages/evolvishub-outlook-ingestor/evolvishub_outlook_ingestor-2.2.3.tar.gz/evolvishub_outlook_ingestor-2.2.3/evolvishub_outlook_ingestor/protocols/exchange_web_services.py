"""
Exchange Web Services (EWS) protocol adapter for Evolvishub Outlook Ingestor.

This module implements the Exchange Web Services protocol adapter for accessing
Outlook emails using the exchangelib library with async wrapper support.

Features:
- Basic and modern authentication support
- Async wrapper around exchangelib
- Folder traversal and email fetching
- Attachment downloading with size limits
- Connection pooling and retry logic
- Comprehensive error handling
"""

import asyncio
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from typing import Any, AsyncGenerator, Dict, List, Optional

from exchangelib import (
    Account,
    Configuration,
    Credentials,
    DELEGATE,
    EWSDateTime,
    EWSTimeZone,
    Folder,
    Message,
    OAuth2Credentials,
)
from exchangelib.errors import (
    EWSError,
    ErrorAccessDenied,
    ErrorInvalidCredentials,
    ErrorServerBusy,
    ErrorTimeoutExpired,
    TransportError,
)

from evolvishub_outlook_ingestor.core.data_models import (
    EmailAddress,
    EmailAttachment,
    EmailMessage,
    OutlookFolder,
    AttachmentType,
    EmailImportance,
    EmailSensitivity,
)
from evolvishub_outlook_ingestor.core.exceptions import (
    AuthenticationError,
    ExchangeError,
    ProtocolError,
    TimeoutError,
)
from evolvishub_outlook_ingestor.protocols.base_protocol import BaseProtocol
from evolvishub_outlook_ingestor.utils.retry import retry_with_config, RetryConfig


class ExchangeWebServicesAdapter(BaseProtocol):
    """Exchange Web Services protocol adapter."""
    
    def __init__(self, name: str, config: Dict[str, Any], **kwargs):
        """
        Initialize EWS adapter.
        
        Args:
            name: Adapter name
            config: Configuration dictionary containing:
                - server: Exchange server URL
                - username: Username or email address
                - password: Password
                - auth_type: Authentication type (basic, oauth2)
                - timeout: Request timeout in seconds
                - max_workers: Maximum thread pool workers
        """
        super().__init__(name, config, **kwargs)
        
        # EWS configuration
        self.server = config.get("server", "outlook.office365.com")
        self.username = config.get("username", "")
        self.password = config.get("password", "")
        self.auth_type = config.get("auth_type", "basic")
        self.timeout = config.get("timeout", 60)
        
        # Thread pool for async operations
        self.max_workers = config.get("max_workers", 4)
        self.executor = None
        
        # EWS objects
        self.account = None
        self.credentials = None
        self.configuration = None
        
        # Retry configuration for EWS
        self.retry_config = RetryConfig(
            max_attempts=3,
            base_delay=2.0,
            max_delay=60.0,
            retry_on_exceptions=[
                ErrorServerBusy,
                ErrorTimeoutExpired,
                TransportError,
                ConnectionError,
            ],
            stop_on_exceptions=[
                ErrorAccessDenied,
                ErrorInvalidCredentials,
                AuthenticationError,
            ]
        )
    
    async def _initialize_connection(self) -> None:
        """Initialize connection to Exchange server."""
        if not all([self.username, self.password]):
            raise AuthenticationError(
                "Missing required EWS credentials",
                auth_method=self.auth_type,
                context={
                    "username_provided": bool(self.username),
                    "password_provided": bool(self.password),
                }
            )
        
        # Initialize thread pool executor
        self.executor = ThreadPoolExecutor(max_workers=self.max_workers)
        
        # Setup credentials based on auth type
        if self.auth_type == "oauth2":
            # OAuth2 credentials (requires additional setup)
            self.credentials = OAuth2Credentials(
                client_id=self.config.get("client_id", ""),
                client_secret=self.config.get("client_secret", ""),
                tenant_id=self.config.get("tenant_id", ""),
                identity=self.username,
            )
        else:
            # Basic credentials
            self.credentials = Credentials(
                username=self.username,
                password=self.password,
            )
        
        self.logger.info("EWS connection initialized", server=self.server, auth_type=self.auth_type)
    
    async def _authenticate(self) -> None:
        """Authenticate with Exchange server."""
        try:
            # Run authentication in thread pool
            await self._run_in_executor(self._authenticate_sync)
            
            self.logger.info("EWS authentication successful", username=self.username)
            
        except Exception as e:
            if isinstance(e, (ErrorAccessDenied, ErrorInvalidCredentials)):
                raise AuthenticationError(
                    f"EWS authentication failed: {e}",
                    auth_method=self.auth_type,
                    username=self.username,
                    cause=e
                )
            else:
                raise ExchangeError(
                    f"EWS connection failed: {e}",
                    response_code=getattr(e, 'response_code', None),
                    cause=e
                )
    
    def _authenticate_sync(self) -> None:
        """Synchronous authentication method."""
        # Create configuration
        self.configuration = Configuration(
            server=self.server,
            credentials=self.credentials,
            auth_type=self.auth_type.upper() if self.auth_type != "oauth2" else "OAUTH2",
        )
        
        # Create account and test connection
        self.account = Account(
            primary_smtp_address=self.username,
            config=self.configuration,
            autodiscover=False,
            access_type=DELEGATE,
        )
        
        # Test connection by accessing root folder
        _ = self.account.root
    
    async def _cleanup_connection(self) -> None:
        """Cleanup connection resources."""
        if self.executor:
            self.executor.shutdown(wait=True)
            self.executor = None
        
        self.account = None
        self.credentials = None
        self.configuration = None
    
    async def _run_in_executor(self, func, *args, **kwargs):
        """Run synchronous function in thread pool executor."""
        if not self.executor:
            raise ProtocolError("Thread pool executor not initialized")
        
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(self.executor, func, *args, **kwargs)
    
    async def _fetch_emails_impl(
        self,
        folder_filters: Optional[List[str]] = None,
        date_range: Optional[Dict[str, datetime]] = None,
        limit: Optional[int] = None,
        include_attachments: bool = True,
        **kwargs
    ) -> List[EmailMessage]:
        """Fetch emails from Exchange server."""
        return await self._run_in_executor(
            self._fetch_emails_sync,
            folder_filters,
            date_range,
            limit,
            include_attachments,
            **kwargs
        )
    
    def _fetch_emails_sync(
        self,
        folder_filters: Optional[List[str]] = None,
        date_range: Optional[Dict[str, datetime]] = None,
        limit: Optional[int] = None,
        include_attachments: bool = True,
        **kwargs
    ) -> List[EmailMessage]:
        """Synchronous email fetching."""
        if not self.account:
            raise ExchangeError("Account not initialized")
        
        emails = []
        
        # Get folders to process
        folders = self._get_folders_sync()
        if folder_filters:
            folders = [f for f in folders if f.name in folder_filters]
        
        # Process each folder
        for folder in folders:
            try:
                # Get EWS folder object
                ews_folder = self._get_ews_folder(folder.id)
                if not ews_folder:
                    continue
                
                # Build query
                query_filter = None
                if date_range:
                    tz = EWSTimeZone.localzone()
                    if "start" in date_range:
                        start_date = EWSDateTime.from_datetime(date_range["start"].replace(tzinfo=timezone.utc))
                        query_filter = ews_folder.filter(datetime_received__gte=start_date)
                    if "end" in date_range:
                        end_date = EWSDateTime.from_datetime(date_range["end"].replace(tzinfo=timezone.utc))
                        if query_filter:
                            query_filter = query_filter.filter(datetime_received__lte=end_date)
                        else:
                            query_filter = ews_folder.filter(datetime_received__lte=end_date)
                
                # Get messages
                if query_filter:
                    messages = query_filter.order_by('-datetime_received')
                else:
                    messages = ews_folder.all().order_by('-datetime_received')
                
                # Apply limit
                if limit:
                    remaining_limit = limit - len(emails)
                    if remaining_limit <= 0:
                        break
                    messages = messages[:remaining_limit]
                
                # Convert messages
                for message in messages:
                    try:
                        email = self._convert_ews_message(message, include_attachments)
                        emails.append(email)
                        
                        if limit and len(emails) >= limit:
                            break
                    except Exception as e:
                        self.logger.warning(
                            "Failed to convert message",
                            message_id=getattr(message, 'message_id', 'unknown'),
                            error=str(e)
                        )
                        continue
                
                if limit and len(emails) >= limit:
                    break
                    
            except Exception as e:
                self.logger.warning(
                    "Failed to process folder",
                    folder_name=folder.name,
                    error=str(e)
                )
                continue
        
        return emails

    def _get_ews_folder(self, folder_id: str) -> Optional[Folder]:
        """Get EWS folder object by ID."""
        try:
            # Try to find folder by ID or name
            for folder in self.account.root.walk():
                if folder.id == folder_id or folder.name == folder_id:
                    return folder
            return None
        except Exception:
            return None

    def _convert_ews_message(self, message: Message, include_attachments: bool = True) -> EmailMessage:
        """Convert EWS message to EmailMessage."""
        # Extract basic information
        email_id = message.id if hasattr(message, 'id') else str(message.item_id)
        subject = getattr(message, 'subject', '') or ''
        body_content = ''
        body_type = 'text'

        # Get body content
        if hasattr(message, 'body'):
            body_content = str(message.body) if message.body else ''
            body_type = 'text'
        elif hasattr(message, 'text_body'):
            body_content = str(message.text_body) if message.text_body else ''
            body_type = 'text'

        if hasattr(message, 'html_body') and message.html_body:
            body_content = str(message.html_body)
            body_type = 'html'

        # Parse sender and recipients
        sender = self._parse_ews_email_address(getattr(message, 'sender', None))
        from_address = self._parse_ews_email_address(getattr(message, 'author', None)) or sender

        to_recipients = [
            self._parse_ews_email_address(addr)
            for addr in getattr(message, 'to_recipients', [])
        ]
        cc_recipients = [
            self._parse_ews_email_address(addr)
            for addr in getattr(message, 'cc_recipients', [])
        ]
        bcc_recipients = [
            self._parse_ews_email_address(addr)
            for addr in getattr(message, 'bcc_recipients', [])
        ]

        # Parse dates
        sent_date = self._parse_ews_datetime(getattr(message, 'datetime_sent', None))
        received_date = self._parse_ews_datetime(getattr(message, 'datetime_received', None))
        created_date = self._parse_ews_datetime(getattr(message, 'datetime_created', None))
        modified_date = self._parse_ews_datetime(getattr(message, 'last_modified_time', None))

        # Parse importance
        importance_map = {
            'Low': EmailImportance.LOW,
            'Normal': EmailImportance.NORMAL,
            'High': EmailImportance.HIGH,
        }
        importance = importance_map.get(
            getattr(message, 'importance', 'Normal'),
            EmailImportance.NORMAL
        )

        # Parse flags and properties
        is_read = getattr(message, 'is_read', False)
        is_draft = getattr(message, 'is_draft', False)
        has_attachments = getattr(message, 'has_attachments', False)

        # Parse folder information
        folder_id = getattr(message.folder, 'id', '') if hasattr(message, 'folder') else ''

        # Parse headers
        headers = {}
        if hasattr(message, 'headers'):
            for header in message.headers:
                headers[header.name] = header.value

        # Get message size
        size = getattr(message, 'size', 0) or 0

        # Process attachments
        attachments = []
        if include_attachments and has_attachments:
            attachments = self._convert_ews_attachments(message)

        # Create EmailMessage
        email = EmailMessage(
            id=email_id,
            message_id=headers.get('Message-ID'),
            conversation_id=getattr(message, 'conversation_id', None),
            subject=subject,
            body=body_content,
            body_type=body_type,
            is_html=(body_type == 'html'),
            sender=sender,
            from_address=from_address,
            to_recipients=[addr for addr in to_recipients if addr],
            cc_recipients=[addr for addr in cc_recipients if addr],
            bcc_recipients=[addr for addr in bcc_recipients if addr],
            sent_date=sent_date,
            received_date=received_date,
            created_date=created_date,
            modified_date=modified_date,
            importance=importance,
            is_read=is_read,
            is_draft=is_draft,
            has_attachments=has_attachments,
            folder_id=folder_id,
            attachments=attachments,
            headers=headers,
            internet_headers=headers,
            size=size,
        )

        return email

    def _parse_ews_email_address(self, addr) -> Optional[EmailAddress]:
        """Parse EWS email address object."""
        if not addr:
            return None

        email = getattr(addr, 'email_address', '') or ''
        name = getattr(addr, 'name', '') or ''

        if not email:
            return None

        return EmailAddress(email=email, name=name)

    def _parse_ews_datetime(self, dt) -> Optional[datetime]:
        """Parse EWS datetime object."""
        if not dt:
            return None

        try:
            if hasattr(dt, 'astimezone'):
                return dt.astimezone(timezone.utc).replace(tzinfo=None)
            return dt
        except (AttributeError, ValueError):
            return None

    def _convert_ews_attachments(self, message: Message) -> List[EmailAttachment]:
        """Convert EWS attachments to EmailAttachment objects."""
        attachments = []

        try:
            for attachment in getattr(message, 'attachments', []):
                # Get attachment properties
                attachment_id = getattr(attachment, 'attachment_id', '')
                name = getattr(attachment, 'name', '') or 'unnamed_attachment'
                content_type = getattr(attachment, 'content_type', 'application/octet-stream')
                size = getattr(attachment, 'size', 0) or 0

                # Determine attachment type
                attachment_type = AttachmentType.FILE
                is_inline = getattr(attachment, 'is_inline', False)
                if is_inline:
                    attachment_type = AttachmentType.INLINE_ATTACHMENT

                content_id = getattr(attachment, 'content_id', None)

                # Get content (be careful with large attachments)
                content = None
                max_size = self.config.get('max_attachment_size', 52428800)  # 50MB
                if size <= max_size:
                    try:
                        content = getattr(attachment, 'content', None)
                    except Exception as e:
                        self.logger.warning(
                            "Failed to get attachment content",
                            attachment_name=name,
                            error=str(e)
                        )

                email_attachment = EmailAttachment(
                    id=str(attachment_id),
                    name=name,
                    content_type=content_type,
                    size=size,
                    attachment_type=attachment_type,
                    is_inline=is_inline,
                    content_id=content_id,
                    content=content,
                )

                attachments.append(email_attachment)

        except Exception as e:
            self.logger.warning(
                "Failed to process attachments",
                message_id=getattr(message, 'message_id', 'unknown'),
                error=str(e)
            )

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
        # For EWS, we'll implement a simple batching approach
        # In a production implementation, you might want to use EWS streaming notifications

        all_emails = await self._fetch_emails_impl(
            folder_filters=folder_filters,
            date_range=date_range,
            include_attachments=include_attachments,
            **kwargs
        )

        # Yield emails in batches
        for i in range(0, len(all_emails), batch_size):
            batch = all_emails[i:i + batch_size]
            yield batch

    async def _get_folders_impl(self) -> List[OutlookFolder]:
        """Fetch folder list from Exchange server."""
        return await self._run_in_executor(self._get_folders_sync)

    def _get_folders_sync(self) -> List[OutlookFolder]:
        """Synchronous folder fetching."""
        if not self.account:
            raise ExchangeError("Account not initialized")

        folders = []

        try:
            # Walk through all folders
            for ews_folder in self.account.root.walk():
                folder = self._convert_ews_folder(ews_folder)
                if folder:
                    folders.append(folder)

        except Exception as e:
            self.logger.error("Failed to fetch folders", error=str(e))
            raise ExchangeError(
                f"Failed to fetch folders: {e}",
                cause=e
            )

        return folders

    def _convert_ews_folder(self, ews_folder) -> Optional[OutlookFolder]:
        """Convert EWS folder to OutlookFolder."""
        try:
            folder_id = getattr(ews_folder, 'id', '')
            name = getattr(ews_folder, 'name', '')

            # Get parent folder ID
            parent_folder_id = None
            if hasattr(ews_folder, 'parent') and ews_folder.parent:
                parent_folder_id = getattr(ews_folder.parent, 'id', None)

            # Get folder counts
            total_count = getattr(ews_folder, 'total_count', 0) or 0
            unread_count = getattr(ews_folder, 'unread_count', 0) or 0

            # Build folder path
            folder_path = f"/{name}"

            return OutlookFolder(
                id=folder_id,
                name=name,
                display_name=name,
                parent_folder_id=parent_folder_id,
                folder_path=folder_path,
                total_item_count=total_count,
                unread_item_count=unread_count,
            )

        except Exception as e:
            self.logger.warning(
                "Failed to convert folder",
                folder_name=getattr(ews_folder, 'name', 'unknown'),
                error=str(e)
            )
            return None
