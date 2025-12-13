"""
Microsoft Graph API protocol adapter for Evolvishub Outlook Ingestor.

This module implements the Microsoft Graph API protocol adapter for accessing
Outlook emails using modern OAuth2 authentication and REST API calls.

Features:
- OAuth2 authentication using MSAL library
- Async HTTP operations with aiohttp
- Rate limiting (100 requests/minute default)
- Pagination support for large datasets
- Folder filtering and date range queries
- Comprehensive error handling for Graph API specific errors
"""

import asyncio
import json
import time
from dataclasses import asdict
from datetime import datetime, timedelta
from typing import Any, AsyncGenerator, Dict, List, Optional
from urllib.parse import urlencode

import aiohttp
from msal import ConfidentialClientApplication

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
    GraphAPIError,
    ProtocolError,
)
from evolvishub_outlook_ingestor.protocols.base_protocol import BaseProtocol
from evolvishub_outlook_ingestor.utils.retry import retry_with_config, RetryConfig
from evolvishub_outlook_ingestor.protocols.mixins import (
    AuthenticationConfig,
    RateLimitConfig,
    AuthenticationCapability,
    RateLimitingCapability,
    ErrorHandlingCapability,
    ConnectionCapability,
    HealthCheckCapability,
)
# Import security utilities with lazy loading to avoid circular imports
def _get_security_utils():
    from evolvishub_outlook_ingestor.utils.security import (
        get_credential_manager,
        mask_sensitive_data,
    )
    return get_credential_manager, mask_sensitive_data

from evolvishub_outlook_ingestor.core.enhanced_html_converter import convert_email_body_to_text_enhanced


class GraphAPIAdapter(
    BaseProtocol,
    AuthenticationCapability,
    RateLimitingCapability,
    ErrorHandlingCapability,
    ConnectionCapability,
    HealthCheckCapability
):
    """Microsoft Graph API protocol adapter."""
    
    def __init__(self, name: str, config: Dict[str, Any], **kwargs):
        """
        Initialize Graph API adapter.
        
        Args:
            name: Adapter name
            config: Configuration dictionary containing:
                - client_id: Azure AD application client ID
                - client_secret: Azure AD application client secret
                - tenant_id: Azure AD tenant ID
                - server: Graph API server (default: graph.microsoft.com)
                - rate_limit: Requests per minute (default: 100)
                - timeout: Request timeout in seconds (default: 60)
        """
        # Initialize all mixins
        super().__init__(name, config, **kwargs)

        # Get credential manager (lazy loading)
        get_credential_manager, _ = _get_security_utils()
        self._credential_manager = get_credential_manager()

        # Graph API configuration
        self.client_id = config.get("client_id", "")
        self.tenant_id = config.get("tenant_id", "")

        # Use custom base_url if provided, otherwise construct from server
        if "base_url" in config:
            self.base_url = config["base_url"]
            # Extract server from base_url for backward compatibility
            if "graph.microsoft.com" in self.base_url:
                self.server = "graph.microsoft.com"
            else:
                # Extract server from custom URL
                import re
                match = re.search(r'https://([^/]+)', self.base_url)
                self.server = match.group(1) if match else "graph.microsoft.com"
        else:
            self.server = config.get("server", "graph.microsoft.com")
            self.base_url = f"https://{self.server}/v1.0"

        # Secure client secret handling
        client_secret_raw = config.get("client_secret", "")
        client_secret_env = config.get("client_secret_env", "GRAPH_CLIENT_SECRET")

        # Try to get client secret from environment first, then from config
        client_secret = (
            self._credential_manager.get_credential_from_env(client_secret_env) or
            client_secret_raw
        )

        # Encrypt client secret for storage
        if client_secret:
            self._encrypted_client_secret = self._credential_manager.encrypt_credential(client_secret)
        else:
            self._encrypted_client_secret = ""
        
        # Authentication
        self.msal_app = None
        self.access_token = None
        self.token_expires_at = None
        
        # HTTP session
        self.session = None
        
        # Rate limiting
        self.rate_limit = config.get("rate_limit", 100)  # requests per minute
        self.request_interval = 60.0 / self.rate_limit  # seconds between requests
        self.last_request_time = 0.0
        
        # Retry configuration for Graph API
        self.retry_config = RetryConfig(
            max_attempts=3,
            base_delay=1.0,
            max_delay=30.0,
            retry_on_exceptions=[
                aiohttp.ClientError,
                asyncio.TimeoutError,
                GraphAPIError,
            ],
            stop_on_exceptions=[
                AuthenticationError,
            ]
        )
    
    async def _initialize_connection(self) -> None:
        """Initialize connection to Graph API."""
        # Get decrypted client secret
        client_secret = self._credential_manager.decrypt_credential(self._encrypted_client_secret)

        if not all([self.client_id, client_secret, self.tenant_id]):
            raise AuthenticationError(
                "Missing required Graph API credentials",
                auth_method="oauth2",
                context={
                    "client_id_provided": bool(self.client_id),
                    "client_secret_provided": bool(client_secret),
                    "tenant_id_provided": bool(self.tenant_id),
                }
            )
        
        # Initialize MSAL application
        authority = f"https://login.microsoftonline.com/{self.tenant_id}"
        self.msal_app = ConfidentialClientApplication(
            client_id=self.client_id,
            client_credential=client_secret,
            authority=authority,
        )
        
        # Initialize HTTP session
        timeout = aiohttp.ClientTimeout(total=self.config.get("timeout", 60))
        self.session = aiohttp.ClientSession(timeout=timeout)
        
        self.logger.info("Graph API connection initialized", server=self.server)
    
    async def _authenticate(self) -> None:
        """Authenticate with Microsoft Graph API using OAuth2."""
        if not self.msal_app:
            raise AuthenticationError("MSAL application not initialized")
        
        try:
            # Request access token for Graph API
            scopes = ["https://graph.microsoft.com/.default"]
            result = self.msal_app.acquire_token_for_client(scopes=scopes)
            
            if "access_token" not in result:
                error_description = result.get("error_description", "Unknown error")
                raise AuthenticationError(
                    f"Failed to acquire access token: {error_description}",
                    auth_method="oauth2",
                    context={"error": result.get("error"), "correlation_id": result.get("correlation_id")}
                )
            
            self.access_token = result["access_token"]
            expires_in = result.get("expires_in", 3600)
            self.token_expires_at = datetime.utcnow() + timedelta(seconds=expires_in - 300)  # 5 min buffer
            
            self.logger.info(
                "Graph API authentication successful",
                expires_at=self.token_expires_at.isoformat()
            )
            
        except Exception as e:
            raise AuthenticationError(
                f"Graph API authentication failed: {e}",
                auth_method="oauth2",
                cause=e
            )
    
    async def _cleanup_connection(self) -> None:
        """Cleanup connection resources."""
        if self.session:
            await self.session.close()
            self.session = None
        
        self.access_token = None
        self.token_expires_at = None
        self.msal_app = None
    
    async def _ensure_authenticated(self) -> None:
        """Ensure we have a valid access token."""
        if not self.access_token or (
            self.token_expires_at and datetime.utcnow() >= self.token_expires_at
        ):
            await self._authenticate()
    
    async def _rate_limit(self) -> None:
        """Apply rate limiting between requests."""
        if self.enable_rate_limiting:
            current_time = asyncio.get_event_loop().time()
            time_since_last = current_time - self.last_request_time
            
            if time_since_last < self.request_interval:
                sleep_time = self.request_interval - time_since_last
                await asyncio.sleep(sleep_time)
            
            self.last_request_time = asyncio.get_event_loop().time()
    
    async def _make_request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Make request with retry logic."""
        return await self._make_request_impl(method, endpoint, params, data)
    async def _make_request_impl(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Make authenticated request to Graph API."""
        await self._ensure_authenticated()
        await self._rate_limit()
        
        url = f"{self.base_url}{endpoint}"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        
        try:
            async with self.session.request(
                method=method,
                url=url,
                headers=headers,
                params=params,
                json=data,
            ) as response:
                
                # Handle rate limiting
                if response.status == 429:
                    retry_after = int(response.headers.get("Retry-After", 60))
                    self.logger.warning(
                        "Graph API rate limit exceeded",
                        retry_after=retry_after,
                        endpoint=endpoint
                    )
                    await asyncio.sleep(retry_after)
                    raise GraphAPIError(
                        "Rate limit exceeded",
                        status_code=429,
                        error_code="TooManyRequests"
                    )
                
                # Handle authentication errors
                if response.status == 401:
                    self.access_token = None  # Force re-authentication
                    raise AuthenticationError(
                        "Graph API authentication failed",
                        auth_method="oauth2"
                    )
                
                # Parse response
                response_data = await response.json()
                
                # Handle API errors
                if response.status >= 400:
                    error_info = response_data.get("error", {})
                    error_code = error_info.get("code", "UnknownError")
                    error_message = error_info.get("message", "Unknown error")
                    
                    raise GraphAPIError(
                        f"Graph API error: {error_message}",
                        status_code=response.status,
                        error_code=error_code,
                        context={"endpoint": endpoint, "method": method}
                    )
                
                return response_data
                
        except aiohttp.ClientError as e:
            raise GraphAPIError(
                f"HTTP client error: {e}",
                context={"endpoint": endpoint, "method": method},
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
        """Fetch emails from Graph API."""
        emails = []
        
        # Get folders to process
        folders = await self.get_folders()
        if folder_filters:
            folders = [f for f in folders if f.name in folder_filters]
        
        # Process each folder
        for folder in folders:
            folder_emails = await self._fetch_folder_emails(
                folder.id,
                date_range=date_range,
                limit=limit,
                include_attachments=include_attachments,
                **kwargs
            )
            emails.extend(folder_emails)
            
            if limit and len(emails) >= limit:
                emails = emails[:limit]
                break
        
        return emails
    
    async def _fetch_folder_emails(
        self,
        folder_id: str,
        date_range: Optional[Dict[str, datetime]] = None,
        limit: Optional[int] = None,
        include_attachments: bool = True,
        **kwargs
    ) -> List[EmailMessage]:
        """Fetch emails from a specific folder."""
        emails = []
        
        # Build query parameters
        params = {
            "$top": min(limit or 10000, 10000),  # Graph API max is 10000
            "$orderby": "receivedDateTime desc",
        }
        
        # Add date filter
        if date_range:
            filters = []
            if "start" in date_range:
                filters.append(f"receivedDateTime ge {date_range['start'].isoformat()}Z")
            if "end" in date_range:
                filters.append(f"receivedDateTime le {date_range['end'].isoformat()}Z")
            
            if filters:
                params["$filter"] = " and ".join(filters)
        
        # Fetch emails with pagination
        endpoint = f"/me/mailFolders/{folder_id}/messages"
        
        while endpoint and (not limit or len(emails) < limit):
            response = await self._make_request("GET", endpoint, params=params)
            
            # Process emails
            for email_data in response.get("value", []):
                email = await self._convert_graph_email(email_data, include_attachments)
                emails.append(email)
                
                if limit and len(emails) >= limit:
                    break
            
            # Get next page
            endpoint = response.get("@odata.nextLink")
            if endpoint:
                # Extract endpoint from full URL
                endpoint = endpoint.replace(self.base_url, "")
                params = {}  # Parameters are included in the nextLink URL
        
        return emails

    async def _convert_graph_email(
        self,
        email_data: Dict[str, Any],
        include_attachments: bool = True
    ) -> EmailMessage:
        """Convert Graph API email data to EmailMessage."""
        # Extract basic email information
        email_id = email_data.get("id", "")
        email_address_source = email_data.get("email_address_source", "")

        subject = email_data.get("subject", "")
        body_content = email_data.get("body", {}).get("content", "")
        body_type = email_data.get("body", {}).get("contentType", "text").lower()
        body_html = email_data.get("body_html","")
        body_preview = email_data.get("body_preview","")
        body_text = email_data.get("body_text","")

        # Extract uniqueBody field (Microsoft Graph API v1.0)
        unique_body_content = email_data.get("uniqueBody", {}).get("content", "")
        unique_body_content_type = email_data.get("uniqueBody", {}).get("contentType", "").lower() if unique_body_content else None

        # Parse sender and recipients
        sender = self._parse_email_address(email_data.get("sender", {}).get("emailAddress", {}))
        from_address = self._parse_email_address(email_data.get("from", {}).get("emailAddress", {}))

        
        to_recipients = [
            self._parse_email_address(addr.get("emailAddress", {}))
            for addr in email_data.get("toRecipients", [])
        ]
        cc_recipients = [
            self._parse_email_address(addr.get("emailAddress", {}))
            for addr in email_data.get("ccRecipients", [])
        ]
        bcc_recipients = [
            self._parse_email_address(addr.get("emailAddress", {}))
            for addr in email_data.get("bccRecipients", [])
        ]
        reply_to = [
            self._parse_email_address(addr.get("emailAddress", {}))
            for addr in email_data.get("replyTo", [])
        ]

        # Parse dates
        sent_datetime = self._parse_datetime(email_data.get("sentDateTime"))
        received_datetime = self._parse_datetime(email_data.get("receivedDateTime"))
        created_datetime = self._parse_datetime(email_data.get("createdDateTime"))
        modified_datetime = self._parse_datetime(email_data.get("lastModifiedDateTime"))

        # Parse importance and sensitivity
        importance_map = {
            "low": EmailImportance.LOW,
            "normal": EmailImportance.NORMAL,
            "high": EmailImportance.HIGH,
        }
        importance = importance_map.get(
            email_data.get("importance", "normal").lower(),
            EmailImportance.NORMAL
        )

        # Parse flags and properties
        is_read = email_data.get("isRead", False)
        is_draft = email_data.get("isDraft", False)
        has_attachments = email_data.get("hasAttachments", False)

        # Parse folder information
        folder_id = email_data.get("parentFolderId", "")

        # Parse headers (Graph API provides limited headers)
        headers = {}
        internet_headers = email_data.get("internetMessageHeaders", [])
        for header in internet_headers:
            headers[header.get("name", "")] = header.get("value", "")

        # Get message size
        size = email_data.get("bodyPreview", "")  # Graph API doesn't provide exact size

        # Fetch attachments if requested
        attachments = []
        if include_attachments and has_attachments:
            attachments = await self._fetch_email_attachments(email_id)

        # Create EmailMessage
        email = EmailMessage(
            id=email_id,
            email_address_source=email_address_source,
            message_id=email_data.get('internetMessageId',''),
            conversation_id=email_data.get("conversationId"),
            conversation_index=email_data.get("conversationIndex"),
            subject=subject,
            body=body_content,
            body_type=body_type,
            body_html=body_html,
            body_preview=body_preview,
            body_text=body_text,
            unique_body=unique_body_content,
            unique_body_content_type=unique_body_content_type,
            is_html=(body_type == "html"),
            sender=sender,
            from_address=from_address,
            to_recipients=to_recipients,
            cc_recipients=cc_recipients,
            bcc_recipients=bcc_recipients,
            reply_to=reply_to,
            sent_datetime=sent_datetime,
            received_datetime=received_datetime,
            created_datetime=created_datetime,
            modified_datetime=modified_datetime,
            importance=importance,
            is_read=is_read,
            is_draft=is_draft,
            has_attachments=has_attachments,
            folder_id=folder_id,
            attachments=attachments,
            headers=headers,
            internet_headers=headers,
            size=len(body_content) if body_content else 0,
        )

        return email

    def _parse_email_address(self, addr_data: Dict[str, Any]) -> Optional[EmailAddress]:
        """Parse email address from Graph API data."""
        if not addr_data:
            return None

        email = addr_data.get("address", "")
        name = addr_data.get("name", "")

        if not email:
            return None

        return EmailAddress(email=email, name=name)

    def _parse_datetime(self, date_str: Optional[str]) -> Optional[datetime]:
        """Parse datetime string from Graph API."""
        if not date_str:
            return None

        try:
            # Graph API returns ISO format with Z suffix
            if date_str.endswith("Z"):
                date_str = date_str[:-1] + "+00:00"
            return datetime.fromisoformat(date_str.replace("Z", "+00:00"))
        except (ValueError, AttributeError):
            return None

    async def _fetch_email_attachments(self, email_id: str) -> List[EmailAttachment]:
        """Fetch attachments for an email."""
        attachments = []

        try:
            endpoint = f"/me/messages/{email_id}/attachments"
            response = await self._make_request("GET", endpoint)

            for attachment_data in response.get("value", []):
                attachment = self._convert_graph_attachment(attachment_data)
                if attachment:
                    attachments.append(attachment)

        except Exception as e:
            self.logger.warning(
                "Failed to fetch attachments",
                email_id=email_id,
                error=str(e)
            )

        return attachments

    def _convert_graph_attachment(self, attachment_data: Dict[str, Any]) -> Optional[EmailAttachment]:
        """Convert Graph API attachment data to EmailAttachment."""
        attachment_id = attachment_data.get("id", "")
        name = attachment_data.get("name", "")
        content_type = attachment_data.get("contentType", "")
        size = attachment_data.get("size", 0)

        # Determine attachment type
        attachment_type = AttachmentType.FILE
        is_inline = attachment_data.get("isInline", False)
        if is_inline:
            attachment_type = AttachmentType.INLINE_ATTACHMENT

        content_id = attachment_data.get("contentId")

        # Get content if it's a file attachment (not reference)
        content = None
        if attachment_data.get("@odata.type") == "#microsoft.graph.fileAttachment":
            content_bytes = attachment_data.get("contentBytes")
            if content_bytes:
                import base64
                try:
                    content = base64.b64decode(content_bytes)
                except Exception:
                    pass

        return EmailAttachment(
            id=attachment_id,
            name=name,
            content_type=content_type,
            size=size,
            attachment_type=attachment_type,
            is_inline=is_inline,
            content_id=content_id,
            content=content,
        )

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
                folder.id,
                date_range=date_range,
                batch_size=batch_size,
                include_attachments=include_attachments,
                **kwargs
            ):
                yield batch

    async def _stream_folder_emails(
        self,
        folder_id: str,
        date_range: Optional[Dict[str, datetime]] = None,
        batch_size: int = 100,
        include_attachments: bool = True,
        **kwargs
    ) -> AsyncGenerator[List[EmailMessage], None]:
        """Stream emails from a specific folder."""
        # Build query parameters
        params = {
            "$top": min(batch_size, 1000),  # Graph API max is 1000
            "$orderby": "receivedDateTime desc",
        }

        # Add date filter
        if date_range:
            filters = []
            if "start" in date_range:
                filters.append(f"receivedDateTime ge {date_range['start'].isoformat()}Z")
            if "end" in date_range:
                filters.append(f"receivedDateTime le {date_range['end'].isoformat()}Z")

            if filters:
                params["$filter"] = " and ".join(filters)

        # Fetch emails with pagination
        endpoint = f"/me/mailFolders/{folder_id}/messages"

        while endpoint:
            response = await self._make_request("GET", endpoint, params=params)

            # Process emails in current page
            emails = []
            for email_data in response.get("value", []):
                email = await self._convert_graph_email(email_data, include_attachments)
                emails.append(email)

            if emails:
                yield emails

            # Get next page
            endpoint = response.get("@odata.nextLink")
            if endpoint:
                # Extract endpoint from full URL
                endpoint = endpoint.replace(self.base_url, "")
                params = {}  # Parameters are included in the nextLink URL

    async def _get_folders_impl(self) -> List[OutlookFolder]:
        """Fetch folder list from Graph API."""
        folders = []

        try:
            endpoint = "/me/mailFolders"
            params = {"$top": 1000}  # Get all folders

            response = await self._make_request("GET", endpoint, params=params)

            for folder_data in response.get("value", []):
                folder = self._convert_graph_folder(folder_data)
                if folder:
                    folders.append(folder)

        except Exception as e:
            self.logger.error("Failed to fetch folders", error=str(e))
            raise ProtocolError(
                f"Failed to fetch folders: {e}",
                protocol=self.name,
                cause=e
            )

        return folders

    def _convert_graph_folder(self, folder_data: Dict[str, Any]) -> Optional[OutlookFolder]:
        """Convert Graph API folder data to OutlookFolder."""
        folder_id = folder_data.get("id", "")
        name = folder_data.get("displayName", "")
        parent_folder_id = folder_data.get("parentFolderId")

        total_item_count = folder_data.get("totalItemCount", 0)
        unread_item_count = folder_data.get("unreadItemCount", 0)

        return OutlookFolder(
            id=folder_id,
            name=name,
            display_name=name,
            parent_folder_id=parent_folder_id,
            folder_path=f"/{name}",  # Simplified path
            total_item_count=total_item_count,
            unread_item_count=unread_item_count,
        )

    # High-level convenience methods (replacing EmailIngestorProtocol functionality)

    async def get_emails(
        self,
        folder_ids: Optional[List[str]] = None,
        user_id: str = "me",
        limit: Optional[int] = None,
        config: Optional[Dict[str, Any]] = None
    ) -> List[EmailMessage]:
        """
        Get emails from specified folders with high-level interface.

        This method provides the same interface as the deprecated EmailIngestorProtocol
        but with better performance and consistency.

        Args:
            folder_ids: List of folder IDs to fetch from (default: ["inbox"])
            user_id: User ID or 'me' for current user
            limit: Maximum number of emails to fetch
            config: Additional configuration options

        Returns:
            List of EmailMessage objects
        """
        if folder_ids is None:
            folder_ids = ["inbox"]

        all_emails = []

        for folder_id in folder_ids:
            try:
                # Use the fixed _fetch_emails_from_folder method that resolves KeyError: 'context'
                emails = []
                # Convert IngestionConfig dataclass to dict if needed
                config_dict = asdict(config) if config and hasattr(config, '__dataclass_fields__') else (config or {})

                async for email in self._fetch_emails_from_folder(
                    folder_id=folder_id,
                    user_id=user_id,
                    limit=limit,
                    **config_dict
                ):
                    emails.append(email)
                    if limit and len(all_emails) + len(emails) >= limit:
                        break

                all_emails.extend(emails)

                if limit and len(all_emails) >= limit:
                    break

            except Exception as e:
                await self.handle_protocol_error(
                    operation=f"get_emails_from_folder_{folder_id}",
                    error=e,
                    context={"folder_id": folder_id, "user_id": user_id}
                )
                # Continue with other folders
                continue

        return all_emails[:limit] if limit else all_emails

    async def fetch_emails(
        self,
        folder_filters: Optional[List[str]] = None,
        date_range: Optional[Dict[str, Any]] = None,
        user_id: str = "me",
        limit: Optional[int] = None,
        **kwargs
    ) -> List[EmailMessage]:
        """
        Fetch emails method for compatibility with OutlookIngestor.

        This method provides the interface expected by the OutlookIngestor
        and uses the fixed _fetch_emails_from_folder implementation.

        Args:
            folder_filters: List of folder names to fetch from (default: ["inbox"])
            date_range: Date range filter
            user_id: User ID or 'me' for current user
            limit: Maximum number of emails to fetch
            **kwargs: Additional parameters

        Returns:
            List of EmailMessage objects
        """
        if folder_filters is None:
            folder_filters = ["inbox"]

        # Convert folder names to folder IDs if needed
        folder_ids = []
        if folder_filters:
            # Get all folders to map names to IDs
            all_folders = await self.get_folders(user_id=user_id)
            folder_map = {folder.name.lower(): folder.id for folder in all_folders}

            for folder_name in folder_filters:
                folder_id = folder_map.get(folder_name.lower(), folder_name)
                folder_ids.append(folder_id)
        else:
            folder_ids = ["inbox"]

        # Use the get_emails method which now uses the fixed implementation
        return await self.get_emails(
            folder_ids=folder_ids,
            user_id=user_id,
            limit=limit,
            config={"date_range": date_range, **kwargs}
        )

    async def search_emails(
        self,
        query: str,
        folder_ids: Optional[List[str]] = None,
        user_id: str = "me",
        limit: Optional[int] = None
    ) -> List[EmailMessage]:
        """
        Search emails with specified query.

        Args:
            query: Search query string
            folder_ids: List of folder IDs to search in (default: all folders)
            user_id: User ID or 'me' for current user
            limit: Maximum number of results

        Returns:
            List of matching EmailMessage objects
        """
        try:
            # Ensure authenticated
            await self.ensure_authenticated()

            # Build search URL
            search_url = f"{self.base_url}/users/{user_id}/messages"

            params = {
                "$search": f'"{query}"',
                "$select": "id,subject,from,toRecipients,ccRecipients,bccRecipients,receivedDateTime,sentDateTime,bodyPreview,body,uniqueBody,hasAttachments,importance,isRead,isDraft,flag,categories,internetMessageId,conversationId,parentFolderId",
                "$orderby": "receivedDateTime desc"
            }

            if limit:
                params["$top"] = str(limit)

            # Apply rate limiting
            await self.rate_limit_request()

            response = await self._make_request("GET", search_url, params=params)

            emails = []
            for item in response.get("value", []):
                try:
                    email = self._parse_email_message(item,user_id)
                    emails.append(email)
                except Exception as e:
                    self.logger.warning(f"Failed to parse email: {e}")
                    continue

            return emails

        except Exception as e:
            await self.handle_protocol_error(
                operation="search_emails",
                error=e,
                context={"query": query, "user_id": user_id}
            )
            raise

    async def get_folders(
        self,
        user_id: str = "me",
        include_hidden: bool = False
    ) -> List[OutlookFolder]:
        """
        Get list of available folders.

        Args:
            user_id: User ID or 'me' for current user
            include_hidden: Whether to include hidden folders

        Returns:
            List of OutlookFolder objects
        """
        try:
            # Use existing _get_folders_impl method
            folders = []
            async for folder in self._get_folders_impl(user_id=user_id):
                # Filter hidden folders if requested
                if not include_hidden and folder.name.startswith("."):
                    continue
                folders.append(folder)

            return folders

        except Exception as e:
            await self.handle_protocol_error(
                operation="get_folders",
                error=e,
                context={"user_id": user_id}
            )
            raise

    # ============================================================================
    # MIXIN METHOD IMPLEMENTATIONS
    # ============================================================================

    # AuthenticationMixin methods
    def configure_authentication(self, config: AuthenticationConfig) -> None:
        """Configure authentication settings."""
        self._auth_config = config

        # Update internal authentication settings
        if config.client_id:
            self.client_id = config.client_id
        if config.client_secret:
            self._encrypted_client_secret = self._credential_manager.encrypt_credential(config.client_secret)
        if config.tenant_id:
            self.tenant_id = config.tenant_id

        # Recreate MSAL app with new config
        self.msal_app = None
        self.access_token = None
        self.token_expires_at = None

    async def _authenticate_impl(self) -> None:
        """Implement authentication logic."""
        if not self._auth_config:
            raise AuthenticationError("Authentication not configured")

        try:
            # Initialize MSAL app if needed
            if not self.msal_app:
                authority = f"https://login.microsoftonline.com/{self.tenant_id}"
                self.msal_app = ConfidentialClientApplication(
                    client_id=self.client_id,
                    client_credential=self._credential_manager.decrypt_credential(self._encrypted_client_secret),
                    authority=authority
                )

            # Get token using client credentials flow
            scopes = self._auth_config.scopes or ["https://graph.microsoft.com/.default"]
            result = self.msal_app.acquire_token_for_client(scopes=scopes)

            if "access_token" in result:
                self.access_token = result["access_token"]
                self.token_expires_at = datetime.utcnow() + timedelta(seconds=result.get("expires_in", 3600))
                self._authenticated = True
                self.logger.info("Authentication successful")
            else:
                error_msg = result.get("error_description", "Unknown authentication error")
                raise AuthenticationError(f"Authentication failed: {error_msg}")

        except Exception as e:
            self.logger.error(f"Authentication failed: {e}")
            raise AuthenticationError(f"Authentication failed: {e}") from e

    async def _refresh_authentication(self) -> None:
        """Refresh authentication token."""
        # For client credentials flow, we just re-authenticate
        await self._authenticate_impl()

    # RateLimitingMixin methods
    def configure_rate_limiting(self, config: RateLimitConfig) -> None:
        """Configure rate limiting settings."""
        self._rate_config = config
        self.rate_limit = config.requests_per_minute
        self.logger.info(f"Rate limiting configured: {config.requests_per_minute} requests/minute")

    async def rate_limit_request(self) -> None:
        """Apply rate limiting before making requests."""
        if not self._rate_config:
            return

        current_time = time.time()

        # Initialize tracking if needed
        if not hasattr(self, '_request_times'):
            self._request_times = []
        if not hasattr(self, '_last_request_time'):
            self._last_request_time = 0
        if not hasattr(self, '_burst_count'):
            self._burst_count = 0

        # Remove old request times (older than 1 minute)
        minute_ago = current_time - 60
        self._request_times = [t for t in self._request_times if t > minute_ago]

        # Check if we're within rate limits
        if len(self._request_times) >= self._rate_config.requests_per_minute:
            sleep_time = 60 - (current_time - self._request_times[0])
            if sleep_time > 0:
                self.logger.warning(f"Rate limit reached, sleeping for {sleep_time:.2f} seconds")
                await asyncio.sleep(sleep_time)

        # Check burst limit
        if current_time - self._last_request_time < 1.0:
            self._burst_count += 1
            if self._burst_count > self._rate_config.burst_limit:
                sleep_time = 1.0 - (current_time - self._last_request_time)
                if sleep_time > 0:
                    await asyncio.sleep(sleep_time)
        else:
            self._burst_count = 0

        # Record this request
        self._request_times.append(current_time)
        self._last_request_time = current_time

    # ConnectionMixin methods
    async def _connect_impl(self) -> None:
        """Implement connection logic."""
        try:
            # Initialize HTTP session
            if not self.session:
                timeout = aiohttp.ClientTimeout(total=self.timeout)
                self.session = aiohttp.ClientSession(timeout=timeout)

            # Test connection with a simple request
            headers = {"Authorization": f"Bearer {self.access_token}"} if self.access_token else {}
            async with self.session.get(f"{self.base_url}/me", headers=headers) as response:
                if response.status == 401:
                    # Need to authenticate first
                    await self.ensure_authenticated()
                    headers = {"Authorization": f"Bearer {self.access_token}"}
                    async with self.session.get(f"{self.base_url}/me", headers=headers) as retry_response:
                        if retry_response.status < 400:
                            self._is_connected = True
                            self._connection_time = datetime.utcnow()
                        else:
                            raise ProtocolError(f"Connection test failed: {retry_response.status}")
                elif response.status < 400:
                    self._is_connected = True
                    self._connection_time = datetime.utcnow()
                else:
                    raise ProtocolError(f"Connection test failed: {response.status}")

        except Exception as e:
            self.logger.error(f"Connection failed: {e}")
            raise ProtocolError(f"Connection failed: {e}") from e

    async def _establish_connection(self) -> None:
        """Establish connection with retry logic."""
        await self._connect_impl()

    def is_connected(self) -> bool:
        """Check if currently connected."""
        return getattr(self, '_is_connected', False) and self.session and not self.session.closed

    # HealthCheckMixin methods
    async def health_check_detailed(self) -> Dict[str, Any]:
        """Perform detailed health check."""
        health_status = {
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "components": {},
            "active_operations": getattr(self, '_active_operations', 0),
            "uptime": (datetime.utcnow() - getattr(self, '_start_time', datetime.utcnow())).total_seconds()
        }

        # Check authentication status
        auth_status = "healthy" if getattr(self, '_authenticated', False) else "unhealthy"
        health_status["components"]["authentication"] = auth_status

        # Check connection status
        conn_status = "connected" if self.is_connected() else "disconnected"
        health_status["components"]["connection"] = conn_status

        # Check rate limiter status
        rate_status = "active" if getattr(self, '_rate_config', None) else "inactive"
        health_status["components"]["rate_limiter"] = rate_status

        # Overall status
        if auth_status == "unhealthy" or conn_status == "disconnected":
            health_status["status"] = "unhealthy"
        elif rate_status == "inactive":
            health_status["status"] = "degraded"

        return health_status

    def set_component_status(self, component: str, status: str) -> None:
        """Set status for a specific component."""
        if not hasattr(self, '_component_status'):
            self._component_status = {}
        self._component_status[component] = status

    def get_component_status(self) -> Dict[str, str]:
        """Get status of all components."""
        return getattr(self, '_component_status', {})

    # ============================================================================
    # INTERNAL HELPER METHODS
    # ============================================================================

    def _parse_body_content(self, email_data: Dict[str, Any]) -> Dict[str, Any]:
        """Parse body content from Graph API email data dictionary."""
        try:
            # Process the email body content for dual-format storage
            original_body_content = email_data.get("body", {}).get("content", "")
            original_body_type = email_data.get("body", {}).get("contentType", "text").lower()

            email_id = email_data.get("id", "unknown")
            conversion_result = convert_email_body_to_text_enhanced(original_body_content, original_body_type, email_id)

            # Store both formats in email_data
            if original_body_type == "html":
                # Store original HTML in body_html and converted text in body_preview
                email_data["body_html"] = original_body_content
                email_data["body_preview"] = conversion_result["text"] if conversion_result["conversion_successful"] else original_body_content
                email_data["body_text"] = conversion_result["text"] if conversion_result["conversion_successful"] else ""
            else:
                # For plain text emails, store in both body_text and body_preview
                email_data["body_text"] = original_body_content
                email_data["body_preview"] = original_body_content
                email_data["body_html"] = ""

            # Update the body content for backward compatibility (use plain text)
            email_data["body"]["content"] = email_data["body_preview"]
            email_data["body"]["contentType"] = "plain_text"

            # Log enhanced conversion details
            if conversion_result["conversion_successful"]:
                method_used = conversion_result.get("method_used", "unknown")
                duration = conversion_result.get("conversion_duration", 0)
                # self.logger.info(
                #     f"Email content processed for dual storage {email_id}: "
                #     f"HTML({len(original_body_content)}) -> Text({len(conversion_result['text'])}) chars "
                #     f"using {method_used} ({duration:.2f}s)"
                # )
            else:
                method_used = conversion_result.get("method_used", "unknown")
                error = conversion_result.get("error", "Unknown error")
                # self.logger.warning(
                #     f"HTML-to-text conversion failed for email {email_id} using {method_used}: {error}, "
                #     f"storing original as fallback"
                # )

        except Exception as conversion_error:
            # If all else fails, create a minimal email object to prevent total failure
            email_id = email_data.get("id", "unknown")
            self.logger.error(
                f"Complete email conversion failed for {email_id}, returning original email data dictionary. Error: {conversion_error}"
            )
        
        return email_data


    def _parse_email_message(self, email_data: Dict[str, Any], user_id: Optional[str] = None) -> EmailMessage:
        """Parse email data from Graph API response into EmailMessage object."""
        try:
            # Parse body content
            email_data = self._parse_body_content(email_data)
            body_content = email_data.get("body", {}).get("content", "")
            body_type = email_data.get("body", {}).get("contentType", "text").lower()
            body_html = email_data.get("body_html")
            body_preview = email_data.get("body_preview")
            body_text = email_data.get("body_text")

            # Parse sender
            sender_data = email_data.get("from", {}).get("emailAddress", {})
            sender = EmailAddress(
                email=sender_data.get("address", ""),
                name=sender_data.get("name", "")
            )

            # Parse recipients
            to_recipients = []
            for recipient in email_data.get("toRecipients", []):
                addr_data = recipient.get("emailAddress", {})
                to_recipients.append(EmailAddress(
                    email=addr_data.get("address", ""),
                    name=addr_data.get("name", "")
                ))

            cc_recipients = []
            for recipient in email_data.get("ccRecipients", []):
                addr_data = recipient.get("emailAddress", {})
                cc_recipients.append(EmailAddress(
                    email=addr_data.get("address", ""),
                    name=addr_data.get("name", "")
                ))

            # Parse dates
            sent_date = None
            if email_data.get("sentDateTime"):
                sent_date = datetime.fromisoformat(email_data["sentDateTime"].replace("Z", "+00:00"))

            received_date = None
            if email_data.get("receivedDateTime"):
                received_date = datetime.fromisoformat(email_data["receivedDateTime"].replace("Z", "+00:00"))

            # Parse importance
            importance_map = {
                "low": EmailImportance.LOW,
                "normal": EmailImportance.NORMAL,
                "high": EmailImportance.HIGH
            }
            importance = importance_map.get(email_data.get("importance", "normal").lower(), EmailImportance.NORMAL)

            # Create EmailMessage
            email = EmailMessage(
                message_id=email_data.get("id",""),
                conversation_id=email_data.get("conversationId"),
                conversation_index=email_data.get("conversationIndex"),
                email_address_source=user_id if user_id else None,
                subject=email_data.get("subject", ""),
                body=body_content,
                body_type=body_type,
                body_html=body_html,
                body_preview=body_preview,
                body_text=body_text,
                sender=sender,
                from_address=sender,
                to_recipients=to_recipients,
                cc_recipients=cc_recipients,
                sent_datetime=sent_date,
                received_datetime=received_date,
                importance=importance,
                is_read=email_data.get("isRead", False),
                has_attachments=email_data.get("hasAttachments", False),
                size=email_data.get("size", 0),
                parent_folder_id=email_data.get("parentFolderId", "")
            )

            return email

        except Exception as e:
            self.logger.error(f"Failed to parse email message: {e}")
            raise ProtocolError(f"Failed to parse email message: {e}") from e

    async def _fetch_emails_from_folder(self, folder_id: str = "inbox", user_id: str = "me",
                                limit: Optional[int] = None, **kwargs) -> AsyncGenerator[EmailMessage, None]:
        """
        Direct Microsoft Graph API implementation for fetching emails from a specific folder.

        This method bypasses the problematic library implementation that was causing
        KeyError: 'context' and implements direct API calls using the confirmed
        working authentication and _make_request method.

        Args:
            folder_id: The folder ID to fetch emails from (default: "inbox")
            user_id: The user ID or 'me' for current user (default: "me")
            limit: Maximum number of emails to fetch (optional)
            **kwargs: Additional parameters (ignored for compatibility)

        Yields:
            EmailMessage: Individual email messages from the folder

        Raises:
            ProtocolError: If the API request fails or email parsing fails
        """
        try:
            self.logger.info(f"Fetching emails from folder '{folder_id}' for user '{user_id}'")

            endpoint = f"/users/{user_id}/mailFolders/{folder_id}/messages"
            params = {
                "$orderby": "receivedDateTime desc",
                "$top": "50"  # Batch size for pagination
            }

            # Add date filtering if provided in kwargs
            if 'date_range_start' in kwargs and kwargs['date_range_start']:
                start_date = kwargs['date_range_start']
                if hasattr(start_date, 'isoformat'):
                        start_date = start_date.isoformat()
                params["$filter"] = f"receivedDateTime ge {start_date}"
            if 'date_range_end' in kwargs and kwargs['date_range_end']:
                end_date = kwargs['date_range_end']
                if hasattr(end_date, 'isoformat'):
                    end_date = end_date.isoformat()
                if "$filter" in params:
                    params["$filter"] += f" and receivedDateTime le {end_date}"
                else:
                    params["$filter"] = f"receivedDateTime le {end_date}"

            count = 0
            next_link = None
            page_count = 0

            while True:
                page_count += 1
                self.logger.info(f"Fetching page {page_count} for folder '{folder_id}'")

                try:
                    if next_link:
                        # Use next link for pagination - remove base URL to get relative path
                        relative_url = next_link.replace(self.base_url, "")
                        response = await self._make_request("GET", relative_url)
                    else:
                        response = await self._make_request("GET", endpoint, params=params)

                    # Validate response structure
                    if not isinstance(response, dict):
                        self.logger.error(f"Invalid response type: {type(response)}")
                        break

                    emails_data = response.get("value", [])
                    self.logger.info(f"Retrieved {len(emails_data)} emails from page {page_count}")

                    if not emails_data:
                        self.logger.info(f"No more emails found in folder '{folder_id}'")
                        break

                    for email_data in emails_data:
                        if limit and count >= limit:
                            self.logger.info(f"Reached limit of {limit} emails")
                            return

                        try:
                            # Parse email using existing method
                            email = self._parse_email_message(email_data,user_id)
                            yield email
                            count += 1

                            if count % 10 == 0:
                                self.logger.info(f"Processed {count} emails from folder '{folder_id}'")

                        except Exception as parse_error:
                            email_id = email_data.get('id', 'unknown')
                            self.logger.warning(f"Failed to parse email {email_id}: {parse_error}")
                            continue

                    # Check for next page
                    next_link = response.get("@odata.nextLink")
                    if not next_link:
                        self.logger.info(f"No more pages available for folder '{folder_id}'")
                        break

                    if limit and count >= limit:
                        self.logger.info(f"Reached email limit of {limit}")
                        break

                except Exception as request_error:
                    self.logger.error(f"Failed to fetch page {page_count} from folder '{folder_id}': {request_error}")
                    # Don't break on single page failure, try to continue
                    break

            self.logger.info(f"Successfully fetched {count} emails from folder '{folder_id}'")

        except Exception as e:
            error_msg = f"Failed to fetch emails from folder '{folder_id}': {e}"
            self.logger.error(error_msg)
            self.logger.error(f"Exception type: {type(e).__name__}")
            self.logger.error(f"Exception args: {e.args}")
            raise ProtocolError(error_msg) from e

    async def _get_folders_impl(self, user_id: str = "me") -> AsyncGenerator[OutlookFolder, None]:
        """Async generator implementation for fetching folders."""
        try:
            endpoint = f"/users/{user_id}/mailFolders"
            params = {"$top": "50"}

            next_link = None

            while True:
                if next_link:
                    response = await self._make_request("GET", next_link.replace(self.base_url, ""))
                else:
                    response = await self._make_request("GET", endpoint, params=params)

                folders_data = response.get("value", [])

                for folder_data in folders_data:
                    try:
                        folder = OutlookFolder(
                            id=folder_data.get("id", ""),
                            name=folder_data.get("displayName", ""),
                            display_name=folder_data.get("displayName", ""),
                            parent_folder_id=folder_data.get("parentFolderId"),
                            folder_path=f"/{folder_data.get('displayName', '')}",
                            total_item_count=folder_data.get("totalItemCount", 0),
                            unread_item_count=folder_data.get("unreadItemCount", 0)
                        )
                        yield folder
                    except Exception as e:
                        self.logger.warning(f"Failed to parse folder {folder_data.get('id', 'unknown')}: {e}")
                        continue

                # Check for next page
                next_link = response.get("@odata.nextLink")
                if not next_link:
                    break

        except Exception as e:
            self.logger.error(f"Failed to fetch folders: {e}")
            raise ProtocolError(f"Failed to fetch folders: {e}") from e
