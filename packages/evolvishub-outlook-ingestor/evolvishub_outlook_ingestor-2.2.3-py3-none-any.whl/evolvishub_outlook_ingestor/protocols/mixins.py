"""
Protocol capabilities for shared functionality across protocol implementations.

This module provides reusable capability classes that eliminate code duplication and
ensure consistent patterns across all protocol adapters. These capabilities can be
mixed into protocol classes to provide specific functionality like authentication,
rate limiting, error handling, connection management, and health checking.
"""

import asyncio
import time
from abc import ABC
from datetime import datetime, timedelta
from typing import Any, Dict, Optional, Callable, Union
from dataclasses import dataclass

from evolvishub_outlook_ingestor.core.exceptions import (
    AuthenticationError,
    ProtocolError,
    RateLimitError,
)
from evolvishub_outlook_ingestor.core.logging import LoggerMixin


@dataclass
class AuthenticationConfig:
    """Standardized authentication configuration."""
    auth_type: str  # 'oauth2', 'basic', 'token'
    client_id: Optional[str] = None
    client_secret: Optional[str] = None
    tenant_id: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
    token: Optional[str] = None
    token_expiry: Optional[datetime] = None
    refresh_token: Optional[str] = None
    scopes: Optional[list] = None


@dataclass
class RateLimitConfig:
    """Rate limiting configuration."""
    requests_per_minute: int = 100
    burst_limit: int = 10
    backoff_factor: float = 1.5
    max_backoff: float = 60.0


class AuthenticationCapability(LoggerMixin):
    """Capability for standardized authentication handling."""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._auth_config: Optional[AuthenticationConfig] = None
        self._access_token: Optional[str] = None
        self._token_expiry: Optional[datetime] = None
        self._refresh_token: Optional[str] = None
    
    def configure_authentication(self, auth_config: AuthenticationConfig) -> None:
        """Configure authentication settings."""
        self._auth_config = auth_config
        self._access_token = auth_config.token
        self._token_expiry = auth_config.token_expiry
        self._refresh_token = auth_config.refresh_token
    
    async def ensure_authenticated(self) -> bool:
        """Ensure valid authentication token is available."""
        if not self._auth_config:
            raise AuthenticationError("Authentication not configured")
        
        # Check if token is expired or missing
        if self._needs_token_refresh():
            await self._refresh_authentication()
        
        return self._access_token is not None
    
    def _needs_token_refresh(self) -> bool:
        """Check if authentication token needs refresh."""
        if not self._access_token:
            return True
        
        if not self._token_expiry:
            return False
        
        # Refresh if token expires within 5 minutes
        return datetime.now() >= (self._token_expiry - timedelta(minutes=5))
    
    async def _refresh_authentication(self) -> None:
        """Refresh authentication token (to be implemented by subclasses)."""
        raise NotImplementedError("Subclasses must implement _refresh_authentication")
    
    def get_auth_headers(self) -> Dict[str, str]:
        """Get authentication headers for requests."""
        if not self._access_token:
            raise AuthenticationError("No valid access token available")
        
        return {
            "Authorization": f"Bearer {self._access_token}",
            "Content-Type": "application/json"
        }


class RateLimitingCapability(LoggerMixin):
    """Capability for standardized rate limiting."""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._rate_config: Optional[RateLimitConfig] = None
        self._request_times: list = []
        self._burst_count: int = 0
        self._last_request_time: float = 0
    
    def configure_rate_limiting(self, rate_config: RateLimitConfig) -> None:
        """Configure rate limiting settings."""
        self._rate_config = rate_config
    
    async def rate_limit_request(self) -> None:
        """Apply rate limiting before making a request."""
        if not self._rate_config:
            return
        
        current_time = time.time()
        
        # Clean old request times (older than 1 minute)
        minute_ago = current_time - 60
        self._request_times = [t for t in self._request_times if t > minute_ago]
        
        # Check if we're within rate limits
        if len(self._request_times) >= self._rate_config.requests_per_minute:
            sleep_time = 60 - (current_time - self._request_times[0])
            if sleep_time > 0:
                self.logger.warning(f"Rate limit reached, sleeping for {sleep_time:.2f} seconds")
                await asyncio.sleep(sleep_time)
        
        # Check burst limit
        if self._burst_count >= self._rate_config.burst_limit:
            time_since_last = current_time - self._last_request_time
            if time_since_last < 1.0:  # Less than 1 second
                sleep_time = 1.0 - time_since_last
                await asyncio.sleep(sleep_time)
                self._burst_count = 0
        
        # Record this request
        self._request_times.append(current_time)
        self._last_request_time = current_time
        self._burst_count += 1
        
        # Reset burst count if enough time has passed
        if current_time - self._last_request_time > 1.0:
            self._burst_count = 0


class ErrorHandlingCapability(LoggerMixin):
    """Capability for standardized error handling patterns."""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._error_count: int = 0
        self._last_error: Optional[Exception] = None
        self._last_error_time: Optional[datetime] = None
    
    async def handle_protocol_error(
        self,
        operation: str,
        error: Exception,
        context: Optional[Dict[str, Any]] = None,
        retry_count: int = 0,
        max_retries: int = 3
    ) -> bool:
        """
        Handle protocol errors with standardized logging and retry logic.
        
        Args:
            operation: Name of the operation that failed
            error: The exception that occurred
            context: Additional context for logging
            retry_count: Current retry attempt
            max_retries: Maximum number of retries
            
        Returns:
            True if operation should be retried, False otherwise
        """
        self._error_count += 1
        self._last_error = error
        self._last_error_time = datetime.now()
        
        # Log the error with context
        log_context = {
            "operation": operation,
            "error_type": type(error).__name__,
            "error_message": str(error),
            "retry_count": retry_count,
            "max_retries": max_retries,
            **(context or {})
        }
        
        if retry_count < max_retries:
            self.logger.warning(f"Operation '{operation}' failed, will retry", **log_context)
            
            # Calculate backoff delay
            delay = min(2 ** retry_count, 30)  # Exponential backoff, max 30 seconds
            await asyncio.sleep(delay)
            
            return True  # Retry
        else:
            self.logger.error(f"Operation '{operation}' failed after {max_retries} retries", **log_context)
            return False  # Don't retry
    
    def get_error_stats(self) -> Dict[str, Any]:
        """Get error statistics for monitoring."""
        # Calculate error rate (errors per hour)
        error_rate = 0.0
        if hasattr(self, '_start_time') and self._start_time:
            hours_elapsed = (datetime.utcnow() - self._start_time).total_seconds() / 3600
            if hours_elapsed > 0:
                error_rate = self._error_count / hours_elapsed

        return {
            "total_errors": self._error_count,
            "error_rate": error_rate,
            "last_error": str(self._last_error) if self._last_error else None,
            "last_error_time": self._last_error_time.isoformat() if self._last_error_time else None,
            "last_error_type": type(self._last_error).__name__ if self._last_error else None
        }


class ConnectionCapability(LoggerMixin):
    """Capability for standardized connection management."""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._is_connected: bool = False
        self._connection_time: Optional[datetime] = None
        self._last_activity: Optional[datetime] = None
        self._connection_attempts: int = 0
    
    async def ensure_connected(self) -> bool:
        """Ensure connection is established."""
        if not self._is_connected:
            await self._establish_connection()
        
        self._last_activity = datetime.now()
        return self._is_connected
    
    async def _establish_connection(self) -> None:
        """Establish connection with retry logic."""
        max_retries = 3
        retry_delay = 1.0

        for attempt in range(max_retries):
            try:
                self._connection_attempts += 1
                await self._connect_impl()
                self._is_connected = True
                self._connection_time = datetime.now()
                return
            except Exception as e:
                if attempt == max_retries - 1:
                    # Last attempt failed, re-raise the exception
                    raise
                # Wait before retrying
                await asyncio.sleep(retry_delay * (attempt + 1))

    async def _connect_impl(self) -> None:
        """Actual connection implementation (to be implemented by subclasses)."""
        raise NotImplementedError("Subclasses must implement _connect_impl")
    
    async def disconnect(self) -> None:
        """Disconnect and cleanup resources."""
        if self._is_connected:
            await self._cleanup_connection()
            self._is_connected = False
            self._connection_time = None
            self.logger.info("Connection closed")
    
    async def _cleanup_connection(self) -> None:
        """Cleanup connection resources (to be implemented by subclasses)."""
        pass
    
    def get_connection_stats(self) -> Dict[str, Any]:
        """Get connection statistics."""
        return {
            "is_connected": self._is_connected,
            "connection_time": self._connection_time.isoformat() if self._connection_time else None,
            "last_activity": self._last_activity.isoformat() if self._last_activity else None,
            "connection_attempts": self._connection_attempts,
            "uptime_seconds": (
                (datetime.now() - self._connection_time).total_seconds()
                if self._connection_time else 0
            )
        }


class HealthCheckCapability(LoggerMixin):
    """Capability for standardized health checking."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._component_status = {}
        self._active_operations = 0
        self._start_time = datetime.utcnow()

    async def health_check(self) -> Dict[str, Any]:
        """Perform comprehensive health check."""
        health_status = {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "checks": {}
        }
        
        try:
            # Connection health
            if hasattr(self, 'get_connection_stats'):
                connection_stats = self.get_connection_stats()
                health_status["checks"]["connection"] = {
                    "status": "healthy" if connection_stats["is_connected"] else "unhealthy",
                    **connection_stats
                }
            
            # Authentication health
            if hasattr(self, 'ensure_authenticated'):
                try:
                    auth_valid = await self.ensure_authenticated()
                    health_status["checks"]["authentication"] = {
                        "status": "healthy" if auth_valid else "unhealthy",
                        "token_valid": auth_valid
                    }
                except Exception as e:
                    health_status["checks"]["authentication"] = {
                        "status": "unhealthy",
                        "error": str(e)
                    }
            
            # Error statistics
            if hasattr(self, 'get_error_stats'):
                error_stats = self.get_error_stats()
                health_status["checks"]["errors"] = {
                    "status": "healthy" if error_stats["total_errors"] < 10 else "degraded",
                    **error_stats
                }
            
            # Overall status
            check_statuses = [check["status"] for check in health_status["checks"].values()]
            if "unhealthy" in check_statuses:
                health_status["status"] = "unhealthy"
            elif "degraded" in check_statuses:
                health_status["status"] = "degraded"
            
        except Exception as e:
            health_status["status"] = "error"
            health_status["error"] = str(e)
        
        return health_status

    async def health_check_detailed(self) -> Dict[str, Any]:
        """Perform detailed health check with component status."""
        health_status = {
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "components": self._component_status.copy(),
            "active_operations": self._active_operations,
            "uptime": (datetime.utcnow() - self._start_time).total_seconds()
        }

        # Check component statuses
        if self._component_status:
            failed_components = [name for name, status in self._component_status.items()
                               if status in ['failed', 'unhealthy', 'error']]
            degraded_components = [name for name, status in self._component_status.items()
                                 if status in ['degraded', 'warning']]

            if failed_components:
                health_status["status"] = "unhealthy"
            elif degraded_components:
                health_status["status"] = "degraded"

        return health_status

    def set_component_status(self, component: str, status: str) -> None:
        """Set status for a specific component."""
        self._component_status[component] = status

    def get_component_status(self) -> Dict[str, str]:
        """Get status of all components."""
        return self._component_status.copy()


# Backward compatibility aliases
# These aliases ensure existing code continues to work while transitioning to the new naming convention
AuthenticationMixin = AuthenticationCapability
RateLimitingMixin = RateLimitingCapability
ErrorHandlingMixin = ErrorHandlingCapability
ConnectionMixin = ConnectionCapability
HealthCheckMixin = HealthCheckCapability
