"""
Retry mechanisms for Evolvishub Outlook Ingestor.

This module provides comprehensive retry functionality with:
- Exponential backoff
- Jitter for avoiding thundering herd
- Configurable retry conditions
- Circuit breaker pattern
- Async/await support
- Detailed logging

The retry mechanisms are designed to handle transient failures
gracefully while avoiding overwhelming external services.
"""

import asyncio
import random
import time
from functools import wraps
from typing import Any, Callable, List, Optional, Type, Union

from tenacity import (
    AsyncRetrying,
    RetryError,
    Retrying,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
    wait_random_exponential,
)

from evolvishub_outlook_ingestor.core.exceptions import (
    AuthenticationError,
    ConnectionError,
    OutlookIngestorError,
    TimeoutError,
)
from evolvishub_outlook_ingestor.core.logging import LoggerMixin, get_logger


class RetryConfig:
    """Configuration for retry behavior."""
    
    def __init__(
        self,
        max_attempts: int = 3,
        base_delay: float = 1.0,
        max_delay: float = 60.0,
        exponential_base: float = 2.0,
        jitter: bool = True,
        retry_on_exceptions: Optional[List[Type[Exception]]] = None,
        stop_on_exceptions: Optional[List[Type[Exception]]] = None,
    ):
        """
        Initialize retry configuration.
        
        Args:
            max_attempts: Maximum number of retry attempts
            base_delay: Base delay in seconds
            max_delay: Maximum delay in seconds
            exponential_base: Base for exponential backoff
            jitter: Add random jitter to delays
            retry_on_exceptions: Exception types to retry on
            stop_on_exceptions: Exception types to never retry
        """
        self.max_attempts = max_attempts
        self.base_delay = base_delay
        self.max_delay = max_delay
        self.exponential_base = exponential_base
        self.jitter = jitter
        
        # Default retryable exceptions
        self.retry_on_exceptions = retry_on_exceptions or [
            ConnectionError,
            TimeoutError,
            OSError,
            asyncio.TimeoutError,
        ]
        
        # Exceptions that should never be retried
        self.stop_on_exceptions = stop_on_exceptions or [
            AuthenticationError,
            ValueError,
            TypeError,
        ]


class CircuitBreaker:
    """Circuit breaker pattern implementation."""
    
    def __init__(
        self,
        failure_threshold: int = 5,
        recovery_timeout: float = 60.0,
        expected_exception: Type[Exception] = Exception,
    ):
        """
        Initialize circuit breaker.
        
        Args:
            failure_threshold: Number of failures before opening circuit
            recovery_timeout: Time to wait before trying again
            expected_exception: Exception type to track
        """
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.expected_exception = expected_exception
        
        self.failure_count = 0
        self.last_failure_time = None
        self.state = "closed"  # closed, open, half-open
        
        self.logger = get_logger(self.__class__.__name__)
    
    def __call__(self, func: Callable) -> Callable:
        """Decorator to apply circuit breaker."""
        @wraps(func)
        async def wrapper(*args, **kwargs):
            if self.state == "open":
                if self._should_attempt_reset():
                    self.state = "half-open"
                    self.logger.info("Circuit breaker half-open, attempting reset")
                else:
                    raise OutlookIngestorError(
                        "Circuit breaker is open",
                        error_code="CIRCUIT_BREAKER_OPEN"
                    )
            
            try:
                result = await func(*args, **kwargs)
                self._on_success()
                return result
                
            except self.expected_exception as e:
                self._on_failure()
                raise
        
        return wrapper
    
    def _should_attempt_reset(self) -> bool:
        """Check if we should attempt to reset the circuit."""
        if self.last_failure_time is None:
            return True
        
        return time.time() - self.last_failure_time >= self.recovery_timeout
    
    def _on_success(self) -> None:
        """Handle successful operation."""
        if self.state == "half-open":
            self.state = "closed"
            self.failure_count = 0
            self.logger.info("Circuit breaker reset to closed state")
    
    def _on_failure(self) -> None:
        """Handle failed operation."""
        self.failure_count += 1
        self.last_failure_time = time.time()
        
        if self.failure_count >= self.failure_threshold:
            self.state = "open"
            self.logger.warning(
                "Circuit breaker opened",
                failure_count=self.failure_count,
                threshold=self.failure_threshold
            )


def retry_with_config(config: RetryConfig):
    """
    Decorator for retrying functions with custom configuration.
    
    Args:
        config: RetryConfig instance
        
    Returns:
        Decorator function
    """
    def decorator(func: Callable) -> Callable:
        logger = get_logger(func.__module__)
        
        # Build retry condition
        retry_condition = retry_if_exception_type(tuple(config.retry_on_exceptions))
        
        # Build wait strategy
        if config.jitter:
            wait_strategy = wait_random_exponential(
                multiplier=config.base_delay,
                max=config.max_delay
            )
        else:
            wait_strategy = wait_exponential(
                multiplier=config.base_delay,
                max=config.max_delay
            )
        
        # Build stop condition
        stop_condition = stop_after_attempt(config.max_attempts)
        
        if asyncio.iscoroutinefunction(func):
            @wraps(func)
            async def async_wrapper(*args, **kwargs):
                async for attempt in AsyncRetrying(
                    retry=retry_condition,
                    wait=wait_strategy,
                    stop=stop_condition,
                    reraise=True,
                ):
                    with attempt:
                        logger.debug(
                            "Attempting operation",
                            function=func.__name__,
                            attempt=attempt.retry_state.attempt_number
                        )
                        
                        try:
                            result = await func(*args, **kwargs)
                            
                            if attempt.retry_state.attempt_number > 1:
                                logger.info(
                                    "Operation succeeded after retries",
                                    function=func.__name__,
                                    attempts=attempt.retry_state.attempt_number
                                )
                            
                            return result
                            
                        except Exception as e:
                            # Check if we should stop retrying
                            if any(isinstance(e, exc_type) for exc_type in config.stop_on_exceptions):
                                logger.error(
                                    "Operation failed with non-retryable exception",
                                    function=func.__name__,
                                    error=str(e),
                                    error_type=type(e).__name__
                                )
                                raise
                            
                            logger.warning(
                                "Operation failed, will retry",
                                function=func.__name__,
                                attempt=attempt.retry_state.attempt_number,
                                error=str(e),
                                error_type=type(e).__name__
                            )
                            raise
            
            return async_wrapper
        
        else:
            @wraps(func)
            def sync_wrapper(*args, **kwargs):
                for attempt in Retrying(
                    retry=retry_condition,
                    wait=wait_strategy,
                    stop=stop_condition,
                    reraise=True,
                ):
                    with attempt:
                        logger.debug(
                            "Attempting operation",
                            function=func.__name__,
                            attempt=attempt.retry_state.attempt_number
                        )
                        
                        try:
                            result = func(*args, **kwargs)
                            
                            if attempt.retry_state.attempt_number > 1:
                                logger.info(
                                    "Operation succeeded after retries",
                                    function=func.__name__,
                                    attempts=attempt.retry_state.attempt_number
                                )
                            
                            return result
                            
                        except Exception as e:
                            # Check if we should stop retrying
                            if any(isinstance(e, exc_type) for exc_type in config.stop_on_exceptions):
                                logger.error(
                                    "Operation failed with non-retryable exception",
                                    function=func.__name__,
                                    error=str(e),
                                    error_type=type(e).__name__
                                )
                                raise
                            
                            logger.warning(
                                "Operation failed, will retry",
                                function=func.__name__,
                                attempt=attempt.retry_state.attempt_number,
                                error=str(e),
                                error_type=type(e).__name__
                            )
                            raise
            
            return sync_wrapper
    
    return decorator


# Predefined retry configurations
DEFAULT_RETRY_CONFIG = RetryConfig()

AGGRESSIVE_RETRY_CONFIG = RetryConfig(
    max_attempts=5,
    base_delay=0.5,
    max_delay=30.0,
    exponential_base=1.5,
)

CONSERVATIVE_RETRY_CONFIG = RetryConfig(
    max_attempts=2,
    base_delay=2.0,
    max_delay=120.0,
    exponential_base=3.0,
)

# Convenience decorators
def retry_default(func: Callable) -> Callable:
    """Apply default retry configuration."""
    return retry_with_config(DEFAULT_RETRY_CONFIG)(func)


def retry_aggressive(func: Callable) -> Callable:
    """Apply aggressive retry configuration."""
    return retry_with_config(AGGRESSIVE_RETRY_CONFIG)(func)


def retry_conservative(func: Callable) -> Callable:
    """Apply conservative retry configuration."""
    return retry_with_config(CONSERVATIVE_RETRY_CONFIG)(func)
