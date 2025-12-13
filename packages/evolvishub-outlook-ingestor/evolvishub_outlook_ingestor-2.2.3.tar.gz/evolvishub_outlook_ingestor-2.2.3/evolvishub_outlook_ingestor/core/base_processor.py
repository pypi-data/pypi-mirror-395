"""
Base processor classes for Evolvishub Outlook Ingestor.

This module defines the abstract base classes and interfaces that all data
processors must implement. It provides a consistent framework for:
- Data processing operations with async/sync patterns
- Comprehensive error handling and recovery mechanisms
- Progress tracking and performance monitoring
- Result reporting and metrics collection
- Resource management and cleanup
- Validation and type safety

All processors in the system inherit from these base classes to ensure
consistency, maintainability, and professional-grade quality.
"""

import asyncio
import time
from abc import ABC, abstractmethod
from typing import Any, AsyncGenerator, Dict, Generic, List, Optional, TypeVar, Union
from uuid import UUID, uuid4

from evolvishub_outlook_ingestor.core.data_models import ProcessingResult, ProcessingStatus
from evolvishub_outlook_ingestor.core.exceptions import ProcessingError, TimeoutError, ValidationError
from evolvishub_outlook_ingestor.core.logging import LoggerMixin, PerformanceLogger, get_logger, set_correlation_id

# Type variables for generic processor
T = TypeVar("T")  # Input type
R = TypeVar("R")  # Result type


class ProcessorMetrics:
    """Metrics collection for processor operations."""
    
    def __init__(self):
        self.reset()
    
    def reset(self) -> None:
        """Reset all metrics."""
        self.total_operations = 0
        self.successful_operations = 0
        self.failed_operations = 0
        self.total_processing_time = 0.0
        self.total_items_processed = 0
        self.peak_memory_usage = 0.0
    
    def record_operation(
        self,
        success: bool,
        processing_time: float,
        items_processed: int = 1,
        memory_usage: float = 0.0
    ) -> None:
        """Record operation metrics."""
        self.total_operations += 1
        if success:
            self.successful_operations += 1
        else:
            self.failed_operations += 1
        
        self.total_processing_time += processing_time
        self.total_items_processed += items_processed
        self.peak_memory_usage = max(self.peak_memory_usage, memory_usage)
    
    @property
    def success_rate(self) -> float:
        """Calculate success rate."""
        if self.total_operations == 0:
            return 0.0
        return self.successful_operations / self.total_operations
    
    @property
    def average_processing_time(self) -> float:
        """Calculate average processing time."""
        if self.total_operations == 0:
            return 0.0
        return self.total_processing_time / self.total_operations
    
    @property
    def items_per_second(self) -> float:
        """Calculate processing rate."""
        if self.total_processing_time == 0:
            return 0.0
        return self.total_items_processed / self.total_processing_time


class BaseProcessor(ABC, LoggerMixin, Generic[T, R]):
    """
    Abstract base class for all data processors.
    
    This class provides comprehensive functionality for data processing including:
    - Operation lifecycle management with resource tracking
    - Progress tracking and performance monitoring
    - Error handling with recovery mechanisms
    - Result collection and metrics analysis
    - Resource management and cleanup
    - Validation and type safety
    - Configuration management
    """
    
    def __init__(
        self,
        name: str,
        config: Optional[Dict[str, Any]] = None,
        enable_metrics: bool = True,
        enable_progress_tracking: bool = True,
    ):
        """
        Initialize the processor.
        
        Args:
            name: Processor name
            config: Configuration dictionary
            enable_metrics: Enable metrics collection
            enable_progress_tracking: Enable progress tracking
        """
        self.name = name
        self.config = config or {}
        self.enable_metrics = enable_metrics
        self.enable_progress_tracking = enable_progress_tracking
        
        # Metrics and tracking
        self.metrics = ProcessorMetrics() if enable_metrics else None
        self._operation_history: List[ProcessingResult] = []
        self._current_operation: Optional[ProcessingResult] = None
        
        # State management
        self._is_initialized = False
        self._is_running = False
        self._should_stop = False
        
        # Resource management
        self._resources: List[Any] = []
    
    async def initialize(self) -> None:
        """Initialize the processor."""
        if self._is_initialized:
            return
        
        self.logger.info("Initializing processor", processor=self.name)
        
        try:
            await self._initialize_resources()
            self._is_initialized = True
            self.logger.info("Processor initialized successfully", processor=self.name)
        except Exception as e:
            self.logger.error(
                "Failed to initialize processor",
                processor=self.name,
                error=str(e)
            )
            raise ProcessingError(
                f"Failed to initialize processor {self.name}: {e}",
                processor=self.name,
                cause=e
            )
    
    async def cleanup(self) -> None:
        """Cleanup processor resources."""
        self.logger.info("Cleaning up processor", processor=self.name)
        
        try:
            await self._cleanup_resources()
            self._is_initialized = False
            self.logger.info("Processor cleanup completed", processor=self.name)
        except Exception as e:
            self.logger.error(
                "Error during processor cleanup",
                processor=self.name,
                error=str(e)
            )
    
    async def process(
        self,
        input_data: T,
        operation_id: Optional[UUID] = None,
        correlation_id: Optional[str] = None,
        timeout: Optional[float] = None,
        **kwargs
    ) -> ProcessingResult:
        """
        Process input data and return results.
        
        Args:
            input_data: Data to process
            operation_id: Operation ID for tracking
            correlation_id: Correlation ID for request tracking
            timeout: Processing timeout in seconds
            **kwargs: Additional processing parameters
            
        Returns:
            ProcessingResult with operation details
        """
        if not self._is_initialized:
            await self.initialize()
        
        # Setup operation tracking
        operation_id = operation_id or uuid4()
        correlation_id = correlation_id or set_correlation_id()
        
        result = ProcessingResult(
            operation_id=operation_id,
            correlation_id=correlation_id,
            status=ProcessingStatus.PENDING
        )
        
        self._current_operation = result
        
        self.logger.info(
            "Starting processing operation",
            operation_id=str(operation_id),
            processor=self.name
        )
        
        start_time = time.time()
        
        try:
            # Set timeout if specified
            if timeout:
                result = await asyncio.wait_for(
                    self._process_with_tracking(input_data, result, **kwargs),
                    timeout=timeout
                )
            else:
                result = await self._process_with_tracking(input_data, result, **kwargs)
            
            # Calculate final metrics
            result.end_time = result.end_time or time.time()
            result.calculate_duration()
            result.calculate_rate()
            
            # Record metrics
            if self.metrics:
                processing_time = time.time() - start_time
                self.metrics.record_operation(
                    success=result.status == ProcessingStatus.COMPLETED,
                    processing_time=processing_time,
                    items_processed=result.successful_items
                )
            
            # Store in history
            if self.enable_progress_tracking:
                self._operation_history.append(result)
                # Keep only last 100 operations
                if len(self._operation_history) > 100:
                    self._operation_history = self._operation_history[-100:]
            
            self.logger.info(
                "Processing operation completed",
                operation_id=str(operation_id),
                status=result.status.value,
                duration=result.duration_seconds,
                items_processed=result.successful_items
            )
            
            return result
            
        except asyncio.TimeoutError:
            result.status = ProcessingStatus.FAILED
            result.error_message = f"Processing timeout after {timeout} seconds"
            result.end_time = time.time()
            result.calculate_duration()
            
            self.logger.error(
                "Processing operation timed out",
                operation_id=str(operation_id),
                timeout=timeout
            )
            
            raise TimeoutError(
                f"Processing timeout after {timeout} seconds",
                timeout_seconds=timeout,
                processor=self.name
            )
            
        except Exception as e:
            result.status = ProcessingStatus.FAILED
            result.error_message = str(e)
            result.end_time = time.time()
            result.calculate_duration()
            
            self.logger.error(
                "Processing operation failed",
                operation_id=str(operation_id),
                error=str(e)
            )
            
            raise ProcessingError(
                f"Processing failed: {e}",
                processor=self.name,
                cause=e
            )
        
        finally:
            self._current_operation = None
    
    async def _process_with_tracking(
        self,
        input_data: T,
        result: ProcessingResult,
        **kwargs
    ) -> ProcessingResult:
        """Process with progress tracking."""
        result.status = ProcessingStatus.RUNNING
        result.start_time = time.time()
        
        try:
            # Validate input
            await self._validate_input(input_data)
            
            # Perform actual processing
            processed_result = await self._process_data(input_data, result, **kwargs)
            
            result.status = ProcessingStatus.COMPLETED
            return processed_result
            
        except Exception as e:
            result.status = ProcessingStatus.FAILED
            result.error_message = str(e)
            raise
    
    @abstractmethod
    async def _process_data(
        self,
        input_data: T,
        result: ProcessingResult,
        **kwargs
    ) -> ProcessingResult:
        """
        Abstract method for actual data processing.
        
        Args:
            input_data: Data to process
            result: Processing result to update
            **kwargs: Additional parameters
            
        Returns:
            Updated processing result
        """
        pass
    
    async def _validate_input(self, input_data: T) -> None:
        """
        Validate input data.
        
        Args:
            input_data: Data to validate
            
        Raises:
            ValidationError: If validation fails
        """
        if input_data is None:
            raise ValidationError("Input data cannot be None")
    
    async def _initialize_resources(self) -> None:
        """Initialize processor-specific resources."""
        pass
    
    async def _cleanup_resources(self) -> None:
        """Cleanup processor-specific resources."""
        for resource in self._resources:
            try:
                if hasattr(resource, 'close'):
                    if asyncio.iscoroutinefunction(resource.close):
                        await resource.close()
                    else:
                        resource.close()
            except Exception as e:
                self.logger.warning(
                    "Error closing resource",
                    resource=str(resource),
                    error=str(e)
                )
        
        self._resources.clear()
    
    def get_metrics(self) -> Optional[Dict[str, Any]]:
        """Get processor metrics."""
        if not self.metrics:
            return None
        
        return {
            "total_operations": self.metrics.total_operations,
            "successful_operations": self.metrics.successful_operations,
            "failed_operations": self.metrics.failed_operations,
            "success_rate": self.metrics.success_rate,
            "average_processing_time": self.metrics.average_processing_time,
            "items_per_second": self.metrics.items_per_second,
            "peak_memory_usage": self.metrics.peak_memory_usage,
        }
    
    def get_operation_history(self, limit: Optional[int] = None) -> List[ProcessingResult]:
        """Get operation history."""
        if limit:
            return self._operation_history[-limit:]
        return self._operation_history.copy()
    
    @property
    def is_running(self) -> bool:
        """Check if processor is currently running."""
        return self._is_running
    
    @property
    def current_operation(self) -> Optional[ProcessingResult]:
        """Get current operation if any."""
        return self._current_operation
