# Examples

This directory contains focused examples demonstrating the usage of the Evolvishub Outlook Email Ingestor library.

## Available Examples

### Email Ingestion Examples
- `email_ingestion_example.py` - Comprehensive email ingestion examples with multiple usage patterns

## Prerequisites

Before running the examples, ensure you have:

1. **Azure AD Application**: Register an application in Azure AD
2. **Permissions**: Grant necessary permissions for Microsoft Graph API:
   - `Mail.Read` - Read user mail
   - `Mail.ReadWrite` - Read and write user mail
   - `MailboxSettings.Read` - Read user mailbox settings
3. **Credentials**: Obtain client ID, client secret, and tenant ID

## Configuration

Create a `.env` file in the examples directory with your credentials:

```env
# Azure AD Configuration
AZURE_CLIENT_ID=your_client_id_here
AZURE_CLIENT_SECRET=your_client_secret_here
AZURE_TENANT_ID=your_tenant_id_here
```

## Running Examples

```bash
# Install dependencies
pip install evolvishub-outlook-ingestor

# Run email ingestion examples
python email_ingestion_example.py
```

## Example Patterns

The `email_ingestion_example.py` demonstrates:

### 1. Simple Email Ingestion
```python
# Minimal configuration for quick start
result = await ingest_emails_simple(
    client_id="your-client-id",
    client_secret="your-client-secret",
    tenant_id="your-tenant-id",
    output_format="json"
)
```

### 2. Advanced Email Ingestion
```python
# Full control with custom configuration
ingestor = EmailIngestor(settings=settings, graph_adapter=adapter)
await ingestor.initialize(config)

result = await ingestor.ingest_emails(
    folder_ids=["inbox", "sent"],
    output_format="database"
)
```

### 3. Email Search
```python
# Search emails with specific queries
emails = await ingestor.search_emails("urgent", limit=100)
```

### 4. Conversation Analysis
```python
# Analyze email conversation threads
thread = await ingestor.get_conversation_thread(conversation_id)
```

### 5. Health Monitoring
```python
# Check system health and connectivity
health = await ingestor.health_check()
```

## Security Notes

- Never commit credentials to version control
- Use environment variables or Azure Key Vault for credential management
- Implement proper error handling for production use
- Follow principle of least privilege for permissions
- Use secure connection strings for database access

## Integration Patterns

The library is designed for easy integration into:

- **Microservices**: Clean API for service-to-service communication
- **Data Pipelines**: Batch processing with progress tracking
- **ETL Workflows**: Extract, transform, load email data
- **Analytics Platforms**: Feed email data to analytics systems
- **Backup Systems**: Archive email data for compliance
