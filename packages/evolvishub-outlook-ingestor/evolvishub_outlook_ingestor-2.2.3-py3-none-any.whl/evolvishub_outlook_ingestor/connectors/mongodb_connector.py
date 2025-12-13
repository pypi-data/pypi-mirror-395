"""
MongoDB database connector for Evolvishub Outlook Email Ingestor.

This module provides a production-ready MongoDB database connector
specifically designed for email ingestion operations using the new
DatabaseConnector interface.
"""

import asyncio
from typing import Any, Dict, List, Optional, Union
from datetime import datetime
from bson import ObjectId

from evolvishub_outlook_ingestor.connectors.database_connector import (
    DatabaseConnector,
    DatabaseConfig,
)
from evolvishub_outlook_ingestor.core.data_models import (
    EmailMessage, EmailAttachment, OutlookFolder, ProcessingResult
)
from evolvishub_outlook_ingestor.core.exceptions import DatabaseError


class MongoDBConnector(DatabaseConnector):
    """
    Production-ready MongoDB database connector for email ingestion.

    This connector provides enterprise-grade MongoDB integration with:
    - Async motor driver for high performance
    - Proper collection management
    - Batch processing with bulk operations
    - Comprehensive error handling
    - Index optimization
    """

    def __init__(self, config: Union[DatabaseConfig, Dict[str, Any]]):
        """
        Initialize MongoDB connector.

        Args:
            config: Database configuration (DatabaseConfig or legacy dict format)
        """
        # Handle backward compatibility with old dict-based config
        if isinstance(config, dict):
            db_config = DatabaseConfig(
                database_type="mongodb",
                host=config.get('host'),
                port=config.get('port', 27017),
                database=config.get('database'),
                username=config.get('username'),
                password=config.get('password'),
                table_name=config.get('collection_name', 'emails'),
                batch_size=config.get('batch_size', 100),
                max_connections=config.get('max_connections', 10)
            )
        else:
            db_config = config

        super().__init__(db_config)
        self._client = None
        self._database = None
        self._collection = None
        self._validate_mongodb_config()

    def _validate_mongodb_config(self):
        """Validate MongoDB-specific configuration."""
        if not self.config.host:
            raise ValueError("MongoDB host is required")
        if not self.config.database:
            raise ValueError("MongoDB database name is required")
    
    async def _connect(self):
        """Establish MongoDB connection."""
        try:
            from motor.motor_asyncio import AsyncIOMotorClient

            # Build connection string
            if self.config.connection_string:
                connection_string = self.config.connection_string
            else:
                if self.config.username and self.config.password:
                    connection_string = (
                        f"mongodb://{self.config.username}:{self.config.password}"
                        f"@{self.config.host}:{self.config.port or 27017}/{self.config.database}"
                    )
                else:
                    connection_string = f"mongodb://{self.config.host}:{self.config.port or 27017}"

            # Create client
            self._client = AsyncIOMotorClient(
                connection_string,
                maxPoolSize=self.config.max_connections,
                serverSelectionTimeoutMS=30000,
                connectTimeoutMS=20000,
                socketTimeoutMS=20000,
                appname="evolvishub-outlook-ingestor"
            )

            # Get database and collection
            self._database = self._client[self.config.database]
            self._collection = self._database[self.config.table_name]

            # Test connection
            await self._client.admin.command('ping')

            self._connection = self._client
            self.logger.info("MongoDB connection established")

        except ImportError:
            raise DatabaseError(
                "motor library not installed. "
                "Install with: pip install motor"
            )
        except Exception as e:
            raise DatabaseError(f"Failed to connect to MongoDB: {e}")

    async def _disconnect(self):
        """Close MongoDB connection."""
        if self._client:
            self._client.close()
            self._client = None
            self._database = None
            self._collection = None
            self._connection = None
            self.logger.info("MongoDB connection closed")
    
    async def _create_schema(self):
        """Create MongoDB indexes for email storage."""
        try:
            # Create indexes for performance
            await self._collection.create_index("id", unique=True)
            await self._collection.create_index("message_id", unique=True, sparse=True)
            await self._collection.create_index("conversation_id")
            await self._collection.create_index("sender.address")
            await self._collection.create_index([("received_date", -1)])  # Descending for recent emails
            await self._collection.create_index("folder_id")
            await self._collection.create_index("is_read")
            await self._collection.create_index("has_attachments")
            await self._collection.create_index("ingestion_date")

            # Compound indexes for common queries
            await self._collection.create_index([
                ("folder_id", 1),
                ("received_date", -1)
            ])

            await self._collection.create_index([
                ("sender.address", 1),
                ("received_date", -1)
            ])

            self.logger.info("MongoDB indexes created successfully")

        except Exception as e:
            self.logger.warning(f"Failed to create some MongoDB indexes: {e}")

    # Required abstract methods for DatabaseConnector interface

    async def _store_email_batch(self, emails: List[EmailMessage]) -> int:
        """Store a batch of emails in MongoDB."""
        if not emails:
            return 0

        try:
            # Convert emails to MongoDB documents
            documents = []
            for email in emails:
                doc = self._email_to_mongo_format(email)
                documents.append(doc)

            # Use bulk operations for efficiency
            from pymongo import UpdateOne

            operations = []
            for doc in documents:
                operation = UpdateOne(
                    {"id": doc["id"]},
                    {"$set": doc},
                    upsert=True
                )
                operations.append(operation)

            # Execute bulk operation
            result = await self._collection.bulk_write(operations, ordered=False)

            stored_count = result.upserted_count + result.modified_count
            self.logger.debug(f"MongoDB bulk operation: {stored_count} emails processed")

            return stored_count

        except Exception as e:
            self.logger.error(f"Failed to store email batch in MongoDB: {e}")
            return 0

    async def _store_single_email(self, email: EmailMessage) -> bool:
        """Store a single email in MongoDB."""
        try:
            doc = self._email_to_mongo_format(email)

            # Use upsert to handle duplicates
            result = await self._collection.update_one(
                {"id": email.id},
                {"$set": doc},
                upsert=True
            )

            return result.upserted_id is not None or result.modified_count > 0

        except Exception as e:
            self.logger.error(f"Failed to store single email in MongoDB: {e}")
            return False

    async def _check_email_exists(self, email_id: str) -> bool:
        """Check if email exists in MongoDB."""
        try:
            result = await self._collection.find_one({"id": email_id}, {"_id": 1})
            return result is not None
        except Exception as e:
            self.logger.error(f"Failed to check email existence in MongoDB: {e}")
            return False

    async def _get_total_email_count(self) -> int:
        """Get total email count from MongoDB."""
        try:
            count = await self._collection.count_documents({})
            return count
        except Exception as e:
            self.logger.error(f"Failed to get email count from MongoDB: {e}")
            return 0

    def _email_to_mongo_format(self, email: EmailMessage) -> Dict[str, Any]:
        """Convert EmailMessage to MongoDB document format."""
        doc = {
            "id": email.id,
            "message_id": email.message_id,
            "conversation_id": email.conversation_id,
            "subject": email.subject,
            "body": email.body,
            "is_html": email.is_html,
            "sender": {
                "address": email.sender.address,
                "name": email.sender.name
            } if email.sender else None,
            "recipients": [
                {"address": r.address, "name": r.name}
                for r in email.recipients
            ] if email.recipients else [],
            "cc_recipients": [
                {"address": r.address, "name": r.name}
                for r in email.cc_recipients
            ] if email.cc_recipients else [],
            "bcc_recipients": [
                {"address": r.address, "name": r.name}
                for r in email.bcc_recipients
            ] if email.bcc_recipients else [],
            "sent_date": email.sent_date,
            "received_date": email.received_date,
            "created_date": getattr(email, 'created_date', None),
            "last_modified_date": getattr(email, 'last_modified_date', None),
            "is_read": email.is_read,
            "is_draft": email.is_draft,
            "has_attachments": email.has_attachments,
            "importance": getattr(email, 'importance', 'normal'),
            "categories": getattr(email, 'categories', []),
            "folder_id": getattr(email, 'folder_id', None),
            "ingestion_date": datetime.utcnow()
        }

        # Add attachments if present
        if email.attachments:
            doc["attachments"] = [
                {
                    "id": att.id,
                    "filename": att.filename,
                    "content_type": att.content_type,
                    "size": att.size,
                    "is_inline": att.is_inline,
                    "content_id": att.content_id
                }
                for att in email.attachments
            ]

        return doc

    # Legacy methods for backward compatibility
    async def initialize(self) -> None:
        """Initialize the MongoDB connector (legacy method)."""
        return await super().initialize()

    async def disconnect(self) -> None:
        """Disconnect from MongoDB (legacy method)."""
        return await self.cleanup()
    
    async def store_email(self, email: EmailMessage) -> bool:
        """Store an email message in the database (legacy method)."""
        return await self._store_single_email(email)

    # Keep existing methods for backward compatibility but update to use new references
    async def store_email_legacy(self, email: EmailMessage) -> bool:
        """Store an email message in the database (original implementation)."""
        try:
            # Convert email to document
            email_doc = self._email_to_document(email)
            
            # Upsert email
            result = await self._database.emails.replace_one(
                {"_id": email.id},
                email_doc,
                upsert=True
            )
            
            # Store attachments separately
            for attachment in email.attachments:
                await self.store_attachment(attachment, email.id)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to store email {email.id}: {str(e)}")
            raise DatabaseError(f"Failed to store email: {str(e)}")
    
    async def store_attachment(self, attachment: EmailAttachment, email_id: str) -> bool:
        """Store an email attachment."""
        try:
            # Convert attachment to document
            attachment_doc = self._attachment_to_document(attachment, email_id)
            
            # Upsert attachment
            result = await self._database.email_attachments.replace_one(
                {"_id": attachment.id},
                attachment_doc,
                upsert=True
            )
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to store attachment {attachment.id}: {str(e)}")
            raise DatabaseError(f"Failed to store attachment: {str(e)}")
    
    async def get_email(self, email_id: str) -> Optional[EmailMessage]:
        """Retrieve an email by ID."""
        try:
            # Get email document
            email_doc = await self._database.emails.find_one({"_id": email_id})
            if not email_doc:
                return None
            
            # Get attachments
            attachment_docs = await self._database.email_attachments.find(
                {"email_id": email_id}
            ).to_list(length=None)
            
            return self._document_to_email(email_doc, attachment_docs)
            
        except Exception as e:
            self.logger.error(f"Failed to get email {email_id}: {str(e)}")
            raise DatabaseError(f"Failed to get email: {str(e)}")
    
    async def get_emails_by_folder(self, folder_id: str, limit: int = 100, offset: int = 0) -> List[EmailMessage]:
        """Get emails from a specific folder."""
        try:
            # Get email documents
            cursor = self._database.emails.find({"folder_id": folder_id}).sort("received_date", -1).skip(offset).limit(limit)
            email_docs = await cursor.to_list(length=limit)
            
            emails = []
            for email_doc in email_docs:
                # Get attachments for this email
                attachment_docs = await self._database.email_attachments.find(
                    {"email_id": email_doc["_id"]}
                ).to_list(length=None)
                
                emails.append(self._document_to_email(email_doc, attachment_docs))
            
            return emails
            
        except Exception as e:
            self.logger.error(f"Failed to get emails from folder {folder_id}: {str(e)}")
            raise DatabaseError(f"Failed to get emails from folder: {str(e)}")
    
    async def store_folder(self, folder: OutlookFolder) -> bool:
        """Store an Outlook folder."""
        try:
            # Convert folder to document
            folder_doc = self._folder_to_document(folder)
            
            # Upsert folder
            result = await self._database.outlook_folders.replace_one(
                {"_id": folder.id},
                folder_doc,
                upsert=True
            )
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to store folder {folder.id}: {str(e)}")
            raise DatabaseError(f"Failed to store folder: {str(e)}")
    
    async def get_folder(self, folder_id: str) -> Optional[OutlookFolder]:
        """Get a folder by ID."""
        try:
            folder_doc = await self._database.outlook_folders.find_one({"_id": folder_id})
            if not folder_doc:
                return None
            
            return self._document_to_folder(folder_doc)
            
        except Exception as e:
            self.logger.error(f"Failed to get folder {folder_id}: {str(e)}")
            raise DatabaseError(f"Failed to get folder: {str(e)}")
    
    async def delete_email(self, email_id: str) -> bool:
        """Delete an email and its attachments."""
        try:
            # Delete attachments first
            await self._database.email_attachments.delete_many({"email_id": email_id})
            
            # Delete email
            result = await self._database.emails.delete_one({"_id": email_id})
            
            return result.deleted_count > 0
            
        except Exception as e:
            self.logger.error(f"Failed to delete email {email_id}: {str(e)}")
            raise DatabaseError(f"Failed to delete email: {str(e)}")
    
    async def search_emails(self, query: str, limit: int = 100) -> List[EmailMessage]:
        """Search emails by subject or body content."""
        try:
            # Use text search
            cursor = self._database.emails.find(
                {"$text": {"$search": query}}
            ).sort("received_date", -1).limit(limit)
            
            email_docs = await cursor.to_list(length=limit)
            
            emails = []
            for email_doc in email_docs:
                # Get attachments for this email
                attachment_docs = await self._database.email_attachments.find(
                    {"email_id": email_doc["_id"]}
                ).to_list(length=None)
                
                emails.append(self._document_to_email(email_doc, attachment_docs))
            
            return emails
            
        except Exception as e:
            self.logger.error(f"Failed to search emails: {str(e)}")
            raise DatabaseError(f"Failed to search emails: {str(e)}")

    def _email_to_document(self, email: EmailMessage) -> Dict[str, Any]:
        """Convert EmailMessage to MongoDB document."""
        doc = {
            "_id": email.id,
            "message_id": email.message_id,
            "conversation_id": email.conversation_id,
            "subject": email.subject,
            "body": email.body,
            "body_preview": email.body_preview,
            "body_type": email.body_type,
            "is_html": email.is_html,
            "sender": {"email": email.sender.email, "name": email.sender.name} if email.sender else None,
            "from_address": {"email": email.from_address.email, "name": email.from_address.name} if email.from_address else None,
            "to_recipients": [{"email": addr.email, "name": addr.name} for addr in email.to_recipients],
            "cc_recipients": [{"email": addr.email, "name": addr.name} for addr in email.cc_recipients],
            "bcc_recipients": [{"email": addr.email, "name": addr.name} for addr in email.bcc_recipients],
            "reply_to": [{"email": addr.email, "name": addr.name} for addr in email.reply_to],
            "sent_date": email.sent_date,
            "received_date": email.received_date,
            "created_date": email.created_date or datetime.utcnow(),
            "modified_date": datetime.utcnow(),
            "importance": email.importance.value,
            "sensitivity": email.sensitivity.value,
            "priority": email.priority,
            "is_read": email.is_read,
            "is_draft": email.is_draft,
            "has_attachments": email.has_attachments,
            "is_flagged": email.is_flagged,
            "folder_id": email.folder_id,
            "folder_path": email.folder_path,
            "headers": email.headers,
            "internet_headers": email.internet_headers,
            "categories": email.categories,
            "in_reply_to": email.in_reply_to,
            "references": email.references,
            "size": email.size,
            "extended_properties": email.extended_properties
        }
        return doc

    def _attachment_to_document(self, attachment: EmailAttachment, email_id: str) -> Dict[str, Any]:
        """Convert EmailAttachment to MongoDB document."""
        doc = {
            "_id": attachment.id,
            "email_id": email_id,
            "name": attachment.name,
            "content_type": attachment.content_type,
            "size": attachment.size,
            "attachment_type": attachment.attachment_type.value,
            "is_inline": attachment.is_inline,
            "content_id": attachment.content_id,
            "content_location": attachment.content_location,
            "content_bytes": attachment.content_bytes,
            "download_url": attachment.download_url,
            "created_date": attachment.created_date or datetime.utcnow(),
            "modified_date": datetime.utcnow()
        }
        return doc

    def _folder_to_document(self, folder: OutlookFolder) -> Dict[str, Any]:
        """Convert OutlookFolder to MongoDB document."""
        doc = {
            "_id": folder.id,
            "name": folder.name,
            "display_name": folder.display_name,
            "parent_folder_id": folder.parent_folder_id,
            "folder_path": folder.folder_path,
            "folder_type": folder.folder_type,
            "total_item_count": folder.total_item_count,
            "unread_item_count": folder.unread_item_count,
            "child_folder_count": folder.child_folder_count,
            "is_hidden": folder.is_hidden,
            "created_date": folder.created_date or datetime.utcnow(),
            "modified_date": datetime.utcnow()
        }
        return doc

    def _document_to_email(self, doc: Dict[str, Any], attachment_docs: List[Dict[str, Any]]) -> EmailMessage:
        """Convert MongoDB document to EmailMessage object."""
        from evolvishub_outlook_ingestor.core.data_models import EmailAddress, EmailImportance, EmailSensitivity

        # Convert attachments
        attachments = []
        for att_doc in attachment_docs:
            attachments.append(self._document_to_attachment(att_doc))

        return EmailMessage(
            id=doc["_id"],
            message_id=doc.get("message_id"),
            conversation_id=doc.get("conversation_id"),
            subject=doc.get("subject"),
            body=doc.get("body"),
            body_preview=doc.get("body_preview"),
            body_type=doc.get("body_type", "text"),
            is_html=doc.get("is_html", False),
            sender=EmailAddress(**doc["sender"]) if doc.get("sender") else None,
            from_address=EmailAddress(**doc["from_address"]) if doc.get("from_address") else None,
            to_recipients=[EmailAddress(**addr) for addr in doc.get("to_recipients", [])],
            cc_recipients=[EmailAddress(**addr) for addr in doc.get("cc_recipients", [])],
            bcc_recipients=[EmailAddress(**addr) for addr in doc.get("bcc_recipients", [])],
            reply_to=[EmailAddress(**addr) for addr in doc.get("reply_to", [])],
            sent_date=doc.get("sent_date"),
            received_date=doc.get("received_date"),
            created_date=doc.get("created_date"),
            modified_date=doc.get("modified_date"),
            importance=EmailImportance(doc.get("importance", "normal")),
            sensitivity=EmailSensitivity(doc.get("sensitivity", "normal")),
            priority=doc.get("priority"),
            is_read=doc.get("is_read", False),
            is_draft=doc.get("is_draft", False),
            has_attachments=doc.get("has_attachments", False),
            is_flagged=doc.get("is_flagged", False),
            folder_id=doc.get("folder_id"),
            folder_path=doc.get("folder_path"),
            attachments=attachments,
            headers=doc.get("headers", {}),
            internet_headers=doc.get("internet_headers", {}),
            categories=doc.get("categories", []),
            in_reply_to=doc.get("in_reply_to"),
            references=doc.get("references", []),
            size=doc.get("size"),
            extended_properties=doc.get("extended_properties", {})
        )

    def _document_to_attachment(self, doc: Dict[str, Any]) -> EmailAttachment:
        """Convert MongoDB document to EmailAttachment object."""
        from evolvishub_outlook_ingestor.core.data_models import AttachmentType

        return EmailAttachment(
            id=doc["_id"],
            name=doc["name"],
            content_type=doc.get("content_type"),
            size=doc.get("size"),
            attachment_type=AttachmentType(doc.get("attachment_type", "file")),
            is_inline=doc.get("is_inline", False),
            content_id=doc.get("content_id"),
            content_location=doc.get("content_location"),
            content_bytes=doc.get("content_bytes"),
            download_url=doc.get("download_url"),
            created_date=doc.get("created_date"),
            modified_date=doc.get("modified_date")
        )

    def _document_to_folder(self, doc: Dict[str, Any]) -> OutlookFolder:
        """Convert MongoDB document to OutlookFolder object."""
        return OutlookFolder(
            id=doc["_id"],
            name=doc["name"],
            display_name=doc.get("display_name"),
            parent_folder_id=doc.get("parent_folder_id"),
            folder_path=doc.get("folder_path"),
            folder_type=doc.get("folder_type"),
            total_item_count=doc.get("total_item_count", 0),
            unread_item_count=doc.get("unread_item_count", 0),
            child_folder_count=doc.get("child_folder_count", 0),
            is_hidden=doc.get("is_hidden", False),
            created_date=doc.get("created_date"),
            modified_date=doc.get("modified_date")
        )

    def _validate_config(self, required_keys: List[str]) -> None:
        """Validate that required configuration keys are present."""
        missing_keys = [key for key in required_keys if key not in self.config]
        if missing_keys:
            raise ValueError(f"Missing required configuration keys: {missing_keys}")

    async def health_check(self) -> Dict[str, Any]:
        """Perform a health check on the database connection."""
        try:
            # Test connection with a simple operation
            result = await self._database.command("ping")

            # Get server info
            server_info = await self._client.server_info()

            return {
                "status": "healthy",
                "database": self.config.database,
                "host": self.config.host,
                "port": self.config.port,
                "server_version": server_info.get("version"),
                "ping_result": result
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e),
                "database": self.config.database,
                "host": self.config.host,
                "port": self.config.port
            }
