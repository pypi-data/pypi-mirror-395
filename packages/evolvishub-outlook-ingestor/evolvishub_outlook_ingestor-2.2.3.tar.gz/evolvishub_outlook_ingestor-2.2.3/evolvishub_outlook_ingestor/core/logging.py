"""
Logging utilities for Evolvishub Outlook Ingestor.

This module provides structured logging capabilities with support for:
- JSON and text formatting
- Correlation ID tracking
- Performance metrics
- Multiple output destinations
- Log level configuration
- Context management

The logging system is designed for production use with comprehensive
monitoring and debugging capabilities.
"""

import json
import logging
import logging.handlers
import sys
import time
import uuid
from contextvars import ContextVar
from typing import Any, Dict, Optional, Union
from pathlib import Path

import structlog
from structlog.typing import FilteringBoundLogger

# Context variable for correlation ID tracking
correlation_id_var: ContextVar[Optional[str]] = ContextVar("correlation_id", default=None)


def set_correlation_id(correlation_id: Optional[str] = None) -> str:
    """
    Set correlation ID for request tracking.
    
    Args:
        correlation_id: Correlation ID to set, generates new one if None
        
    Returns:
        The correlation ID that was set
    """
    if correlation_id is None:
        correlation_id = str(uuid.uuid4())
    
    correlation_id_var.set(correlation_id)
    return correlation_id


def get_correlation_id() -> Optional[str]:
    """Get current correlation ID."""
    return correlation_id_var.get()


def add_correlation_id(logger: FilteringBoundLogger, method_name: str, event_dict: Dict[str, Any]) -> Dict[str, Any]:
    """Add correlation ID to log events."""
    correlation_id = get_correlation_id()
    if correlation_id:
        event_dict["correlation_id"] = correlation_id
    return event_dict


def add_timestamp(logger: FilteringBoundLogger, method_name: str, event_dict: Dict[str, Any]) -> Dict[str, Any]:
    """Add timestamp to log events."""
    event_dict["timestamp"] = time.time()
    return event_dict


def add_log_level(logger: FilteringBoundLogger, method_name: str, event_dict: Dict[str, Any]) -> Dict[str, Any]:
    """Add log level to log events."""
    event_dict["level"] = method_name.upper()
    return event_dict


class JSONFormatter(logging.Formatter):
    """JSON log formatter for structured logging."""
    
    def format(self, record: logging.LogRecord) -> str:
        """Format log record as JSON."""
        log_data = {
            "timestamp": record.created,
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }
        
        # Add correlation ID if available
        correlation_id = get_correlation_id()
        if correlation_id:
            log_data["correlation_id"] = correlation_id
        
        # Add exception information if present
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
        
        # Add extra fields
        for key, value in record.__dict__.items():
            if key not in {
                "name", "msg", "args", "levelname", "levelno", "pathname",
                "filename", "module", "lineno", "funcName", "created",
                "msecs", "relativeCreated", "thread", "threadName",
                "processName", "process", "getMessage", "exc_info",
                "exc_text", "stack_info"
            }:
                log_data[key] = value
        
        return json.dumps(log_data, default=str)


class TextFormatter(logging.Formatter):
    """Enhanced text formatter with correlation ID support."""
    
    def format(self, record: logging.LogRecord) -> str:
        """Format log record as text."""
        # Add correlation ID to record if available
        correlation_id = get_correlation_id()
        if correlation_id:
            record.correlation_id = correlation_id[:8]  # Short version for text logs
        
        return super().format(record)


def setup_logging(
    log_level: str = "INFO",
    log_format: str = "json",
    log_file: Optional[str] = None,
    enable_console: bool = True,
    enable_correlation_id: bool = True,
    enable_performance_metrics: bool = True,
    max_file_size: int = 10 * 1024 * 1024,  # 10MB
    backup_count: int = 5,
) -> None:
    """
    Setup logging configuration.
    
    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_format: Log format (json, text)
        log_file: Log file path (optional)
        enable_console: Enable console logging
        enable_correlation_id: Enable correlation ID tracking
        enable_performance_metrics: Enable performance metrics
        max_file_size: Maximum log file size in bytes
        backup_count: Number of backup files to keep
    """
    # Configure structlog
    processors = [
        structlog.stdlib.filter_by_level,
        add_log_level,
        add_timestamp,
    ]
    
    if enable_correlation_id:
        processors.append(add_correlation_id)
    
    if enable_performance_metrics:
        processors.append(structlog.processors.TimeStamper(fmt="iso"))
    
    if log_format == "json":
        processors.extend([
            structlog.processors.JSONRenderer()
        ])
    else:
        processors.extend([
            structlog.processors.add_logger_name,
            structlog.dev.ConsoleRenderer()
        ])
    
    structlog.configure(
        processors=processors,
        wrapper_class=structlog.stdlib.BoundLogger,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )
    
    # Configure standard logging
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, log_level.upper()))
    
    # Remove existing handlers
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    # Setup formatters
    if log_format == "json":
        formatter = JSONFormatter()
        text_formatter = TextFormatter(
            fmt="%(asctime)s [%(levelname)s] %(name)s: %(message)s [%(correlation_id)s]",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
    else:
        formatter = TextFormatter(
            fmt="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        text_formatter = formatter
    
    # Console handler
    if enable_console:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(text_formatter if log_format == "json" else formatter)
        root_logger.addHandler(console_handler)
    
    # File handler
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        file_handler = logging.handlers.RotatingFileHandler(
            log_file,
            maxBytes=max_file_size,
            backupCount=backup_count,
            encoding="utf-8"
        )
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)


def get_logger(name: str) -> FilteringBoundLogger:
    """
    Get a structured logger instance.
    
    Args:
        name: Logger name
        
    Returns:
        Structured logger instance
    """
    return structlog.get_logger(name)


class LoggerMixin:
    """Mixin class to add logging capabilities to other classes."""
    
    @property
    def logger(self) -> FilteringBoundLogger:
        """Get logger for this class."""
        return get_logger(self.__class__.__name__)


class PerformanceLogger:
    """Context manager for performance logging."""
    
    def __init__(
        self,
        logger: FilteringBoundLogger,
        operation: str,
        **context
    ):
        self.logger = logger
        self.operation = operation
        self.context = context
        self.start_time: Optional[float] = None
    
    def __enter__(self) -> "PerformanceLogger":
        """Start performance measurement."""
        self.start_time = time.time()
        self.logger.info(
            "Operation started",
            operation=self.operation,
            **self.context
        )
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """End performance measurement and log results."""
        if self.start_time is not None:
            duration = time.time() - self.start_time
            
            if exc_type is None:
                self.logger.info(
                    "Operation completed",
                    operation=self.operation,
                    duration_seconds=duration,
                    **self.context
                )
            else:
                self.logger.error(
                    "Operation failed",
                    operation=self.operation,
                    duration_seconds=duration,
                    error_type=exc_type.__name__ if exc_type else None,
                    error_message=str(exc_val) if exc_val else None,
                    **self.context
                )


def log_performance(operation: str, **context):
    """
    Decorator for automatic performance logging.
    
    Args:
        operation: Operation name
        **context: Additional context to log
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            logger = get_logger(func.__module__)
            with PerformanceLogger(logger, operation, **context):
                return func(*args, **kwargs)
        return wrapper
    return decorator


def log_async_performance(operation: str, **context):
    """
    Decorator for automatic performance logging of async functions.
    
    Args:
        operation: Operation name
        **context: Additional context to log
    """
    def decorator(func):
        async def wrapper(*args, **kwargs):
            logger = get_logger(func.__module__)
            with PerformanceLogger(logger, operation, **context):
                return await func(*args, **kwargs)
        return wrapper
    return decorator
