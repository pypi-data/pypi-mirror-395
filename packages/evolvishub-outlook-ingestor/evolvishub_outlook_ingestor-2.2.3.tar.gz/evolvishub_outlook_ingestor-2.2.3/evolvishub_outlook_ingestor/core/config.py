"""
Configuration management for Evolvishub Outlook Ingestor.

This module provides centralized configuration management using Pydantic Settings
with support for:
- Environment variable overrides
- YAML configuration files
- Type validation and conversion
- Nested configuration structures
- Default values and validation

The configuration system follows the 12-factor app methodology and supports
different environments (development, staging, production).
"""

import os
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import yaml
from pydantic import BaseModel, Field, field_validator, ValidationError
from pydantic_settings import BaseSettings


class DatabaseConfig(BaseModel):
    """Database configuration settings."""
    
    # Connection settings
    host: str = Field(default="localhost", description="Database host")
    port: int = Field(default=5432, description="Database port")
    database: str = Field(default="outlook_data", description="Database name")
    username: str = Field(default="postgres", description="Database username")
    password: str = Field(default="", description="Database password")
    
    # Connection pool settings
    pool_size: int = Field(default=10, description="Connection pool size")
    max_overflow: int = Field(default=20, description="Maximum pool overflow")
    pool_timeout: int = Field(default=30, description="Pool timeout in seconds")
    pool_recycle: int = Field(default=3600, description="Pool recycle time in seconds")
    
    # SSL settings (secure defaults)
    ssl_mode: str = Field(default="require", description="SSL mode")
    ssl_cert: Optional[str] = Field(default=None, description="SSL certificate path")
    ssl_key: Optional[str] = Field(default=None, description="SSL key path")
    ssl_ca: Optional[str] = Field(default=None, description="SSL CA path")

    @field_validator('ssl_mode')
    @classmethod
    def validate_ssl_mode(cls, v: str) -> str:
        """Validate SSL mode is secure."""
        allowed_modes = ['require', 'verify-ca', 'verify-full']
        if v not in allowed_modes:
            raise ValueError(f"SSL mode must be one of {allowed_modes} for security")
        return v

    @field_validator('password')
    @classmethod
    def validate_password_strength(cls, v: str) -> str:
        """Validate password strength."""
        if v and len(v) < 8:
            raise ValueError("Database password must be at least 8 characters long")
        return v

    @field_validator('host')
    @classmethod
    def validate_host(cls, v: str) -> str:
        """Validate host is not localhost in production."""
        # This would be enhanced based on environment
        if v == "localhost":
            import os
            env = os.environ.get("ENVIRONMENT", "development")
            if env == "production":
                raise ValueError("Database host cannot be localhost in production")
        return v


class ProtocolConfig(BaseModel):
    """Protocol configuration settings."""
    
    # Connection settings
    server: str = Field(default="outlook.office365.com", description="Server hostname")
    port: Optional[int] = Field(default=None, description="Server port")
    use_ssl: bool = Field(default=True, description="Use SSL/TLS")
    
    # Authentication
    username: str = Field(default="", description="Username/email")
    password: str = Field(default="", description="Password")
    
    # OAuth2 settings (for Graph API)
    client_id: Optional[str] = Field(default=None, description="OAuth2 client ID")
    client_secret: Optional[str] = Field(default=None, description="OAuth2 client secret")
    tenant_id: Optional[str] = Field(default=None, description="Azure tenant ID")
    
    # Connection settings
    timeout: int = Field(default=60, description="Connection timeout in seconds")
    max_retries: int = Field(default=3, description="Maximum retry attempts")
    retry_delay: float = Field(default=1.0, description="Retry delay in seconds")
    
    # Rate limiting
    rate_limit: int = Field(default=100, description="Requests per minute")
    burst_limit: int = Field(default=10, description="Burst request limit")


class ProcessingConfig(BaseModel):
    """Processing configuration settings."""
    
    # Batch processing
    batch_size: int = Field(default=1000, description="Batch size for processing")
    max_workers: int = Field(default=4, description="Maximum worker threads")
    chunk_size: int = Field(default=100, description="Chunk size for parallel processing")
    
    # Timeouts
    timeout_seconds: int = Field(default=300, description="Processing timeout")
    item_timeout: int = Field(default=30, description="Individual item timeout")
    
    # Retry settings
    retry_attempts: int = Field(default=3, description="Retry attempts")
    retry_delay: float = Field(default=1.0, description="Retry delay in seconds")
    retry_backoff: float = Field(default=2.0, description="Retry backoff multiplier")
    
    # Memory management
    max_memory_mb: int = Field(default=1024, description="Maximum memory usage in MB")
    memory_check_interval: int = Field(default=100, description="Memory check interval")
    
    # Temporary storage
    temp_directory: str = Field(default="/tmp/outlook_ingestor", description="Temporary directory")
    cleanup_temp_files: bool = Field(default=True, description="Cleanup temporary files")


class EmailConfig(BaseModel):
    """Email processing configuration."""
    
    # Content extraction
    extract_headers: bool = Field(default=True, description="Extract email headers")
    extract_body: bool = Field(default=True, description="Extract email body")
    extract_attachments: bool = Field(default=True, description="Extract attachments")
    extract_metadata: bool = Field(default=True, description="Extract metadata")
    
    # Attachment settings
    max_attachment_size: int = Field(default=52428800, description="Max attachment size (50MB)")
    supported_attachment_types: List[str] = Field(
        default_factory=lambda: [
            "pdf", "doc", "docx", "xls", "xlsx", "ppt", "pptx",
            "txt", "csv", "json", "xml", "html",
            "jpg", "jpeg", "png", "gif", "bmp", "tiff",
            "zip", "rar", "7z", "tar", "gz"
        ],
        description="Supported attachment file types"
    )
    
    # Content processing
    decode_html: bool = Field(default=True, description="Decode HTML content")
    extract_links: bool = Field(default=True, description="Extract links from content")
    detect_language: bool = Field(default=False, description="Detect content language")
    
    # Folder settings
    include_folders: List[str] = Field(
        default_factory=lambda: ["Inbox", "Sent Items", "Drafts"],
        description="Folders to include in processing"
    )
    exclude_folders: List[str] = Field(
        default_factory=lambda: ["Deleted Items", "Junk Email"],
        description="Folders to exclude from processing"
    )


class LoggingConfig(BaseModel):
    """Logging configuration settings."""
    
    level: str = Field(default="INFO", description="Log level")
    format: str = Field(default="json", description="Log format (json, text)")
    
    # File logging
    log_file: Optional[str] = Field(default=None, description="Log file path")
    max_file_size: int = Field(default=10485760, description="Max log file size (10MB)")
    backup_count: int = Field(default=5, description="Number of backup files")
    
    # Structured logging
    enable_correlation_id: bool = Field(default=True, description="Enable correlation IDs")
    enable_performance_metrics: bool = Field(default=True, description="Enable performance metrics")
    
    # External logging
    syslog_host: Optional[str] = Field(default=None, description="Syslog host")
    syslog_port: int = Field(default=514, description="Syslog port")


class MonitoringConfig(BaseModel):
    """Monitoring and metrics configuration."""
    
    # Metrics
    enable_metrics: bool = Field(default=True, description="Enable metrics collection")
    metrics_port: int = Field(default=8000, description="Metrics server port")
    metrics_path: str = Field(default="/metrics", description="Metrics endpoint path")
    
    # Health checks
    enable_health_checks: bool = Field(default=True, description="Enable health checks")
    health_check_interval: int = Field(default=30, description="Health check interval")
    
    # Performance monitoring
    enable_profiling: bool = Field(default=False, description="Enable performance profiling")
    profile_output_dir: str = Field(default="/tmp/profiles", description="Profile output directory")


class Settings(BaseSettings):
    """Main application settings."""
    
    # Application metadata
    app_name: str = Field(default="Evolvishub Outlook Ingestor", description="Application name")
    app_version: str = Field(default="1.0.2", description="Application version")
    environment: str = Field(default="development", description="Environment")
    debug: bool = Field(default=False, description="Enable debug mode")
    
    # Configuration file
    config_file: Optional[str] = Field(default=None, description="Configuration file path")
    
    # Nested configurations
    database: DatabaseConfig = Field(default_factory=DatabaseConfig)
    protocols: Dict[str, ProtocolConfig] = Field(default_factory=dict)
    processing: ProcessingConfig = Field(default_factory=ProcessingConfig)
    email: EmailConfig = Field(default_factory=EmailConfig)
    logging: LoggingConfig = Field(default_factory=LoggingConfig)
    monitoring: MonitoringConfig = Field(default_factory=MonitoringConfig)
    
    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": False,
        "env_nested_delimiter": "__",
    }
    
    @field_validator("environment")
    @classmethod
    def validate_environment(cls, v: str) -> str:
        """Validate environment setting."""
        valid_environments = ["development", "staging", "production", "test"]
        if v.lower() not in valid_environments:
            raise ValueError(f"Environment must be one of: {valid_environments}")
        return v.lower()
    
    def load_from_yaml(self, config_path: Union[str, Path]) -> None:
        """Load configuration from YAML file."""
        config_path = Path(config_path)
        if not config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {config_path}")
        
        with open(config_path, "r", encoding="utf-8") as f:
            config_data = yaml.safe_load(f)
        
        # Update configuration with YAML data
        for key, value in config_data.items():
            if hasattr(self, key):
                if isinstance(getattr(self, key), BaseModel):
                    # Handle nested configuration
                    nested_config = getattr(self, key)
                    for nested_key, nested_value in value.items():
                        if hasattr(nested_config, nested_key):
                            setattr(nested_config, nested_key, nested_value)
                else:
                    setattr(self, key, value)


@lru_cache
def get_settings() -> Settings:
    """
    Get application settings with caching.
    
    This function creates and caches a Settings instance, loading configuration
    from environment variables and optionally from a YAML file.
    
    Returns:
        Cached Settings instance
    """
    settings = Settings()
    
    # Load from YAML file if specified
    config_file = os.getenv("CONFIG_FILE") or settings.config_file
    if config_file:
        config_path = Path(config_file)
        if config_path.exists():
            settings.load_from_yaml(config_path)
    
    return settings
