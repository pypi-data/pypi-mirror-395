# Configuration Reference

This document provides a comprehensive reference for configuring the Evolvishub Outlook Ingestor library.

## Configuration Methods

The library supports multiple configuration methods in order of precedence:

1. **Environment Variables** (highest precedence)
2. **YAML Configuration Files**
3. **Default Values** (lowest precedence)

## Environment Variables

Environment variables use double underscores (`__`) to represent nested configuration:

```bash
# Application settings
export APP_NAME="My Outlook Ingestor"
export ENVIRONMENT="production"
export DEBUG="false"

# Database settings
export DATABASE__HOST="localhost"
export DATABASE__PORT="5432"
export DATABASE__USERNAME="postgres"
export DATABASE__PASSWORD="your_password"

# Protocol settings
export PROTOCOLS__GRAPH_API__CLIENT_ID="your_client_id"
export PROTOCOLS__GRAPH_API__CLIENT_SECRET="your_client_secret"
export PROTOCOLS__GRAPH_API__TENANT_ID="your_tenant_id"

# Processing settings
export PROCESSING__BATCH_SIZE="1000"
export PROCESSING__MAX_WORKERS="4"
```

## YAML Configuration

Create a `config.yaml` file with your settings:

```yaml
# Application settings
app_name: "Evolvishub Outlook Ingestor"
app_version: "0.1.0"
environment: "production"
debug: false

# Database configuration
database:
  host: "localhost"
  port: 5432
  database: "outlook_data"
  username: "postgres"
  password: "your_password"
  
  # Connection pool settings
  pool_size: 10
  max_overflow: 20
  pool_timeout: 30
  pool_recycle: 3600
  
  # SSL settings
  ssl_mode: "require"
  ssl_cert: "/path/to/client-cert.pem"
  ssl_key: "/path/to/client-key.pem"
  ssl_ca: "/path/to/ca-cert.pem"

# Protocol configurations
protocols:
  # Microsoft Graph API
  graph_api:
    server: "graph.microsoft.com"
    port: 443
    use_ssl: true
    client_id: "your_client_id"
    client_secret: "your_client_secret"
    tenant_id: "your_tenant_id"
    timeout: 60
    max_retries: 3
    retry_delay: 1.0
    rate_limit: 100
    burst_limit: 10
  
  # Exchange Web Services
  exchange:
    server: "outlook.office365.com"
    port: null
    use_ssl: true
    username: "your_email@company.com"
    password: "your_password"
    timeout: 60
    max_retries: 3
    retry_delay: 1.0
    rate_limit: 100
    burst_limit: 10
  
  # IMAP/POP3
  imap:
    server: "outlook.office365.com"
    port: 993
    use_ssl: true
    username: "your_email@company.com"
    password: "your_password"
    timeout: 60
    max_retries: 3
    retry_delay: 1.0
    rate_limit: 50
    burst_limit: 5

# Processing configuration
processing:
  # Batch processing
  batch_size: 1000
  max_workers: 4
  chunk_size: 100
  
  # Timeouts
  timeout_seconds: 300
  item_timeout: 30
  
  # Retry settings
  retry_attempts: 3
  retry_delay: 1.0
  retry_backoff: 2.0
  
  # Memory management
  max_memory_mb: 1024
  memory_check_interval: 100
  
  # Temporary storage
  temp_directory: "/tmp/outlook_ingestor"
  cleanup_temp_files: true

# Email processing configuration
email:
  # Content extraction
  extract_headers: true
  extract_body: true
  extract_attachments: true
  extract_metadata: true
  
  # Attachment settings
  max_attachment_size: 52428800  # 50MB
  supported_attachment_types:
    - "pdf"
    - "doc"
    - "docx"
    - "xls"
    - "xlsx"
    - "ppt"
    - "pptx"
    - "txt"
    - "csv"
    - "json"
    - "xml"
    - "html"
    - "jpg"
    - "jpeg"
    - "png"
    - "gif"
    - "bmp"
    - "tiff"
    - "zip"
    - "rar"
    - "7z"
    - "tar"
    - "gz"
  
  # Content processing
  decode_html: true
  extract_links: true
  detect_language: false
  
  # Folder settings
  include_folders:
    - "Inbox"
    - "Sent Items"
    - "Drafts"
  exclude_folders:
    - "Deleted Items"
    - "Junk Email"

# Logging configuration
logging:
  level: "INFO"
  format: "json"
  
  # File logging
  log_file: "/var/log/outlook_ingestor.log"
  max_file_size: 10485760  # 10MB
  backup_count: 5
  
  # Structured logging
  enable_correlation_id: true
  enable_performance_metrics: true
  
  # External logging
  syslog_host: "localhost"
  syslog_port: 514

# Monitoring configuration
monitoring:
  # Metrics
  enable_metrics: true
  metrics_port: 8000
  metrics_path: "/metrics"
  
  # Health checks
  enable_health_checks: true
  health_check_interval: 30
  
  # Performance monitoring
  enable_profiling: false
  profile_output_dir: "/tmp/profiles"
```

## Configuration Sections

### Application Settings

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| `app_name` | string | "Evolvishub Outlook Ingestor" | Application name |
| `app_version` | string | "0.1.0" | Application version |
| `environment` | string | "development" | Environment (development, staging, production, test) |
| `debug` | boolean | false | Enable debug mode |

### Database Configuration

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| `host` | string | "localhost" | Database host |
| `port` | integer | 5432 | Database port |
| `database` | string | "outlook_data" | Database name |
| `username` | string | "postgres" | Database username |
| `password` | string | "" | Database password |
| `pool_size` | integer | 10 | Connection pool size |
| `max_overflow` | integer | 20 | Maximum pool overflow |
| `pool_timeout` | integer | 30 | Pool timeout in seconds |
| `pool_recycle` | integer | 3600 | Pool recycle time in seconds |
| `ssl_mode` | string | "prefer" | SSL mode (disable, allow, prefer, require) |

### Protocol Configuration

Each protocol (graph_api, exchange, imap) supports:

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| `server` | string | varies | Server hostname |
| `port` | integer | varies | Server port |
| `use_ssl` | boolean | true | Use SSL/TLS |
| `username` | string | "" | Username/email |
| `password` | string | "" | Password |
| `timeout` | integer | 60 | Connection timeout in seconds |
| `max_retries` | integer | 3 | Maximum retry attempts |
| `retry_delay` | float | 1.0 | Retry delay in seconds |
| `rate_limit` | integer | 100 | Requests per minute |
| `burst_limit` | integer | 10 | Burst request limit |

#### Graph API Specific

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| `client_id` | string | "" | OAuth2 client ID |
| `client_secret` | string | "" | OAuth2 client secret |
| `tenant_id` | string | "" | Azure tenant ID |

### Processing Configuration

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| `batch_size` | integer | 1000 | Batch size for processing |
| `max_workers` | integer | 4 | Maximum worker threads |
| `chunk_size` | integer | 100 | Chunk size for parallel processing |
| `timeout_seconds` | integer | 300 | Processing timeout |
| `item_timeout` | integer | 30 | Individual item timeout |
| `retry_attempts` | integer | 3 | Retry attempts |
| `retry_delay` | float | 1.0 | Retry delay in seconds |
| `retry_backoff` | float | 2.0 | Retry backoff multiplier |
| `max_memory_mb` | integer | 1024 | Maximum memory usage in MB |
| `memory_check_interval` | integer | 100 | Memory check interval |
| `temp_directory` | string | "/tmp/outlook_ingestor" | Temporary directory |
| `cleanup_temp_files` | boolean | true | Cleanup temporary files |

### Email Configuration

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| `extract_headers` | boolean | true | Extract email headers |
| `extract_body` | boolean | true | Extract email body |
| `extract_attachments` | boolean | true | Extract attachments |
| `extract_metadata` | boolean | true | Extract metadata |
| `max_attachment_size` | integer | 52428800 | Max attachment size (50MB) |
| `supported_attachment_types` | list | see above | Supported attachment file types |
| `decode_html` | boolean | true | Decode HTML content |
| `extract_links` | boolean | true | Extract links from content |
| `detect_language` | boolean | false | Detect content language |
| `include_folders` | list | ["Inbox", "Sent Items", "Drafts"] | Folders to include |
| `exclude_folders` | list | ["Deleted Items", "Junk Email"] | Folders to exclude |

### Logging Configuration

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| `level` | string | "INFO" | Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL) |
| `format` | string | "json" | Log format (json, text) |
| `log_file` | string | null | Log file path |
| `max_file_size` | integer | 10485760 | Max log file size (10MB) |
| `backup_count` | integer | 5 | Number of backup files |
| `enable_correlation_id` | boolean | true | Enable correlation IDs |
| `enable_performance_metrics` | boolean | true | Enable performance metrics |
| `syslog_host` | string | null | Syslog host |
| `syslog_port` | integer | 514 | Syslog port |

### Monitoring Configuration

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| `enable_metrics` | boolean | true | Enable metrics collection |
| `metrics_port` | integer | 8000 | Metrics server port |
| `metrics_path` | string | "/metrics" | Metrics endpoint path |
| `enable_health_checks` | boolean | true | Enable health checks |
| `health_check_interval` | integer | 30 | Health check interval |
| `enable_profiling` | boolean | false | Enable performance profiling |
| `profile_output_dir` | string | "/tmp/profiles" | Profile output directory |

## Loading Configuration

### From File

```python
from evolvishub_outlook_ingestor.core.config import Settings

settings = Settings()
settings.load_from_yaml("/path/to/config.yaml")
```

### From Environment

```python
import os
from evolvishub_outlook_ingestor.core.config import get_settings

# Set environment variable
os.environ["CONFIG_FILE"] = "/path/to/config.yaml"

# Get settings (automatically loads from file if CONFIG_FILE is set)
settings = get_settings()
```

### Programmatic Configuration

```python
from evolvishub_outlook_ingestor.core.config import Settings, DatabaseConfig

settings = Settings(
    environment="production",
    debug=False,
    database=DatabaseConfig(
        host="prod-db.example.com",
        port=5432,
        database="outlook_prod",
        username="outlook_user",
        password="secure_password",
        pool_size=20,
    )
)
```
