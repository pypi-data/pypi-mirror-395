"""
Email Ingestion Example

This example demonstrates how to use the focused evolvishub-outlook-ingestor
library for email ingestion from Microsoft Outlook using Microsoft Graph API.

The library is designed as a pure data ingestion tool that can be easily
integrated into other applications and microservices.
"""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Any

from evolvishub_outlook_ingestor import (
    EmailIngestor,
    ingest_emails_simple,
    IngestionConfig,
    Settings,
)
from evolvishub_outlook_ingestor.protocols.microsoft_graph import GraphAPIAdapter

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def simple_email_ingestion():
    """
    Demonstrate simple email ingestion with minimal configuration.
    
    This is the easiest way to get started with the library.
    """
    logger.info("🚀 Starting simple email ingestion example")
    
    try:
        # Simple ingestion with minimal configuration
        result = await ingest_emails_simple(
            client_id="your-client-id",
            client_secret="your-client-secret", 
            tenant_id="your-tenant-id",
            user_id="me",
            folder_ids=["inbox"],  # Only inbox
            output_format="json"
        )
        
        logger.info(f"✅ Simple ingestion completed:")
        logger.info(f"  Status: {result['status']}")
        logger.info(f"  Processed: {result['processed_emails']} emails")
        logger.info(f"  Failed: {result['failed_emails']} emails")
        logger.info(f"  Data: {len(result['data'])} email records")
        
        return result
        
    except Exception as e:
        logger.error(f"❌ Simple ingestion failed: {e}")
        raise


async def advanced_email_ingestion():
    """
    Demonstrate advanced email ingestion with full configuration.
    
    This shows how to use the library with custom settings and processing.
    """
    logger.info("🚀 Starting advanced email ingestion example")
    
    # Create settings
    settings = Settings()
    settings.graph_api.client_id = "your-client-id"
    settings.graph_api.client_secret = "your-client-secret"
    settings.graph_api.tenant_id = "your-tenant-id"
    
    # Create Graph adapter
    adapter = GraphAPIAdapter("graph_api", {
        "client_id": settings.graph_api.client_id,
        "client_secret": settings.graph_api.client_secret,
        "tenant_id": settings.graph_api.tenant_id
    })
    await adapter.initialize()
    
    # Create ingestion configuration
    def progress_callback(processed: int, total: int):
        percentage = (processed / total) * 100 if total > 0 else 0
        logger.info(f"📊 Progress: {processed}/{total} ({percentage:.1f}%)")
    
    config = IngestionConfig(
        batch_size=50,
        max_concurrent_requests=5,
        include_attachments=True,
        attachment_size_limit=10 * 1024 * 1024,  # 10MB
        retry_attempts=3,
        progress_callback=progress_callback,
        date_range_start=datetime.utcnow() - timedelta(days=30),  # Last 30 days
        date_range_end=datetime.utcnow()
    )
    
    # Create email ingestor
    ingestor = EmailIngestor(
        settings=settings,
        graph_adapter=adapter
    )
    
    try:
        # Initialize
        await ingestor.initialize(config)
        
        # Get available folders
        folders = await ingestor.get_folders()
        logger.info(f"📁 Available folders: {len(folders)}")
        for folder in folders[:5]:  # Show first 5
            logger.info(f"  - {folder['display_name']}: {folder['total_item_count']} emails")
        
        # Ingest emails from specific folders
        folder_ids = ["inbox", "sent"]
        result = await ingestor.ingest_emails(
            folder_ids=folder_ids,
            output_format="json"
        )
        
        logger.info(f"✅ Advanced ingestion completed:")
        logger.info(f"  Status: {result.status.value}")
        logger.info(f"  Total emails: {result.total_emails}")
        logger.info(f"  Processed: {result.processed_emails}")
        logger.info(f"  Failed: {result.failed_emails}")
        logger.info(f"  Success rate: {(result.processed_emails / result.total_emails * 100):.1f}%")
        logger.info(f"  Duration: {result.end_time - result.start_time}")
        
        return result
        
    finally:
        await ingestor.cleanup()


async def email_search_example():
    """
    Demonstrate email search functionality.
    """
    logger.info("🔍 Starting email search example")
    
    # Create settings and adapter
    settings = Settings()
    settings.graph_api.client_id = "your-client-id"
    settings.graph_api.client_secret = "your-client-secret"
    settings.graph_api.tenant_id = "your-tenant-id"
    
    adapter = GraphAPIAdapter("graph_api", {
        "client_id": settings.graph_api.client_id,
        "client_secret": settings.graph_api.client_secret,
        "tenant_id": settings.graph_api.tenant_id
    })
    await adapter.initialize()
    
    ingestor = EmailIngestor(settings=settings, graph_adapter=adapter)
    await ingestor.initialize()
    
    try:
        # Search for emails
        search_queries = [
            "meeting",
            "project alpha",
            "urgent",
            "invoice"
        ]
        
        for query in search_queries:
            logger.info(f"🔍 Searching for: '{query}'")
            
            emails = await ingestor.search_emails(
                query=query,
                limit=10,
                output_format="list"
            )
            
            logger.info(f"  Found {len(emails)} emails")
            
            # Show first few results
            for email in emails[:3]:
                logger.info(f"    - {email.subject} (from: {email.sender.address if email.sender else 'Unknown'})")
        
    finally:
        await ingestor.cleanup()


async def conversation_thread_example():
    """
    Demonstrate conversation thread functionality.
    """
    logger.info("💬 Starting conversation thread example")
    
    # Create settings and adapter
    settings = Settings()
    settings.graph_api.client_id = "your-client-id"
    settings.graph_api.client_secret = "your-client-secret"
    settings.graph_api.tenant_id = "your-tenant-id"
    
    adapter = GraphAPIAdapter("graph_api", {
        "client_id": settings.graph_api.client_id,
        "client_secret": settings.graph_api.client_secret,
        "tenant_id": settings.graph_api.tenant_id
    })
    await adapter.initialize()
    
    ingestor = EmailIngestor(settings=settings, graph_adapter=adapter)
    await ingestor.initialize()
    
    try:
        # Get recent emails to find conversation IDs
        recent_emails = await ingestor.search_emails(
            query="",  # Empty query to get recent emails
            limit=20,
            output_format="list"
        )
        
        # Find emails with conversation IDs
        conversation_ids = set()
        for email in recent_emails:
            if email.conversation_id:
                conversation_ids.add(email.conversation_id)
        
        logger.info(f"💬 Found {len(conversation_ids)} conversation threads")
        
        # Analyze first few conversations
        for i, conversation_id in enumerate(list(conversation_ids)[:3]):
            logger.info(f"💬 Analyzing conversation {i+1}: {conversation_id}")
            
            thread_emails = await ingestor.get_conversation_thread(
                conversation_id=conversation_id,
                output_format="list"
            )
            
            logger.info(f"  Thread has {len(thread_emails)} emails")
            
            # Show thread timeline
            for email in thread_emails:
                date_str = email.received_date.strftime("%Y-%m-%d %H:%M") if email.received_date else "Unknown"
                sender = email.sender.address if email.sender else "Unknown"
                logger.info(f"    {date_str} - {sender}: {email.subject}")
        
    finally:
        await ingestor.cleanup()


async def health_check_example():
    """
    Demonstrate health check functionality.
    """
    logger.info("🏥 Starting health check example")
    
    # Create settings and adapter
    settings = Settings()
    settings.graph_api.client_id = "your-client-id"
    settings.graph_api.client_secret = "your-client-secret"
    settings.graph_api.tenant_id = "your-tenant-id"
    
    adapter = GraphAPIAdapter("graph_api", {
        "client_id": settings.graph_api.client_id,
        "client_secret": settings.graph_api.client_secret,
        "tenant_id": settings.graph_api.tenant_id
    })
    await adapter.initialize()
    
    ingestor = EmailIngestor(settings=settings, graph_adapter=adapter)
    await ingestor.initialize()
    
    try:
        # Perform health check
        health = await ingestor.health_check()
        
        logger.info(f"🏥 Health check results:")
        logger.info(f"  Overall status: {health['status']}")
        logger.info(f"  Timestamp: {health['timestamp']}")
        
        for component, status in health.get('components', {}).items():
            status_emoji = "✅" if status.startswith("healthy") else "❌"
            logger.info(f"  {status_emoji} {component}: {status}")
        
        return health
        
    finally:
        await ingestor.cleanup()


async def main():
    """
    Main function to run all examples.
    
    Note: You need to replace the placeholder credentials with real values
    from your Azure App Registration.
    """
    logger.info("🎯 Evolvishub Outlook Email Ingestor - Examples")
    logger.info("=" * 60)
    
    # Note: These examples require valid Azure credentials
    logger.warning("⚠️  Please update the credentials in the examples before running!")
    logger.warning("⚠️  You need to register an app in Azure and get client_id, client_secret, and tenant_id")
    
    try:
        # Run examples (commented out to avoid errors with placeholder credentials)
        
        # Example 1: Simple ingestion
        # await simple_email_ingestion()
        
        # Example 2: Advanced ingestion
        # await advanced_email_ingestion()
        
        # Example 3: Email search
        # await email_search_example()
        
        # Example 4: Conversation threads
        # await conversation_thread_example()
        
        # Example 5: Health check
        # await health_check_example()
        
        logger.info("✅ All examples completed successfully!")
        
    except Exception as e:
        logger.error(f"❌ Examples failed: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(main())
