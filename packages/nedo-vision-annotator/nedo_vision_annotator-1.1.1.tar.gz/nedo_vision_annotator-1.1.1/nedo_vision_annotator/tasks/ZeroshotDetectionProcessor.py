"""
Zeroshot Detection Processor - Handles auto-annotation using zero-shot detection models
"""
import asyncio
import logging
import threading
import time
from abc import ABC, abstractmethod
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Protocol, Tuple, Union, Callable, Any
from uuid import UUID
import torch
import psutil

from ..zeroshot_detection.ZeroShotDetection import ZeroShotDetection
from ..zeroshot_detection.GroundingDinoDetection import GroundingDINODetection, GroundingDINOConfig
from ..types.ZeroShotDetectionType import DetectionResult, ImageSource
from ..types.AutoAnnotationTypes import (
    AnnotationConfig, 
    AnnotationImage, 
    AutoAnnotationResult, 
    BoundingBox
)


class DetectionModelType(Enum):
    """Supported detection model types"""
    GROUNDING_DINO = "grounding_dino"
    # Future models can be added here
    # SAM = "sam"
    # CLIP = "clip"


@dataclass
class BatchConfig:
    """Configuration for batch processing"""
    batch_size: int
    max_workers: int
    timeout_seconds: float = 300.0  # 5 minutes per batch


@dataclass
class ProcessorConfig:
    """Configuration for the ZeroshotDetectionProcessor"""
    model_type: DetectionModelType = DetectionModelType.GROUNDING_DINO
    model_config: Optional[Dict[str, Any]] = None
    batch_config: Optional[BatchConfig] = None
    enable_async: bool = True
    
    def __post_init__(self) -> None:
        """Initialize default values after creation"""
        if self.batch_config is None:
            self.batch_config = self._get_optimal_batch_config()
    
    def _get_optimal_batch_config(self) -> BatchConfig:
        """Calculate optimal batch configuration based on system resources"""
        # Get system memory
        memory_gb = psutil.virtual_memory().total / (1024**3)
        
        # Get CPU count
        cpu_count = psutil.cpu_count()
        
        # Check if CUDA is available
        has_cuda = torch.cuda.is_available()
        
        if has_cuda:
            # GPU-based batching - smaller batches due to VRAM constraints
            if memory_gb >= 32:
                batch_size = 8
                max_workers = min(4, cpu_count // 2)
            elif memory_gb >= 16:
                batch_size = 4
                max_workers = min(3, cpu_count // 2)
            else:
                batch_size = 2
                max_workers = min(2, cpu_count // 2)
        else:
            # CPU-based batching - can handle more images but slower
            if memory_gb >= 16:
                batch_size = 4
                max_workers = min(cpu_count, 6)
            elif memory_gb >= 8:
                batch_size = 2
                max_workers = min(cpu_count // 2, 4)
            else:
                batch_size = 1
                max_workers = min(cpu_count // 2, 2)
        
        return BatchConfig(
            batch_size=max(1, batch_size),
            max_workers=max(1, max_workers)
        )


class DetectionModelFactory:
    """Factory for creating detection model instances"""
    
    @staticmethod
    def create_model(
        model_type: DetectionModelType,
        model_config: Optional[Dict[str, Any]] = None
    ) -> ZeroShotDetection:
        """
        Create a detection model instance.
        
        Args:
            model_type: Type of model to create
            model_config: Optional model-specific configuration
            
        Returns:
            ZeroShotDetection instance
            
        Raises:
            ValueError: If model type is not supported
            RuntimeError: If model creation fails
        """
        if model_type == DetectionModelType.GROUNDING_DINO:
            config = GroundingDINOConfig()
            if model_config:
                # Update config with provided values
                for key, value in model_config.items():
                    if hasattr(config, key):
                        setattr(config, key, value)
            
            return GroundingDINODetection(config)
        
        # Future model implementations can be added here
        # elif model_type == DetectionModelType.SAM:
        #     return SAMDetection(model_config)
        
        else:
            raise ValueError(f"Unsupported model type: {model_type}")


@dataclass
class DetectionRequest:
    """Request for detection processing"""
    request_id: str
    image: AnnotationImage
    config: AnnotationConfig
    dataset_id: UUID


@dataclass
class DetectionResponse:
    """Response from detection processing"""
    request_id: str
    image_id: UUID
    results: List[AutoAnnotationResult]
    processing_time: float
    success: bool
    error_message: Optional[str] = None


class DetectionProcessor(Protocol):
    """Protocol for detection processors - enables dependency injection"""
    
    def process_detections(
        self,
        requests: List[DetectionRequest],
        callback: Optional[Callable[[List[DetectionResponse]], None]] = None
    ) -> List[DetectionResponse]:
        """Process detection requests and return results"""
        ...
    
    async def process_detections_async(
        self,
        requests: List[DetectionRequest],
        callback: Optional[Callable[[List[DetectionResponse]], None]] = None
    ) -> List[DetectionResponse]:
        """Process detection requests asynchronously"""
        ...
    
    def is_ready(self) -> bool:
        """Check if processor is ready to process requests"""
        ...

    def cleanup(self) -> None:
        ...


class ZeroshotDetectionProcessor:
    """
    Processor for zero-shot detection auto-annotation.
    
    This class handles:
    - Multiple detection models (currently Grounding DINO, extensible for future models)
    - Batch processing with optimal configuration based on system resources
    - Concurrent/async processing for multiple requests
    - Thread-safe operation for simultaneous dataset processing
    - Dependency injection for loose coupling with handlers
    """
    
    def __init__(
        self,
        config: Optional[ProcessorConfig] = None,
        logger: Optional[logging.Logger] = None
    ):
        """
        Initialize ZeroshotDetectionProcessor.
        
        Args:
            config: Processor configuration. Uses optimal defaults if None.
            logger: Optional logger instance. Creates one if None.
        """
        self.config = config or ProcessorConfig()
        self.logger = logger or logging.getLogger(__name__)
        
        # Thread-safe model cache for different model types
        self._model_cache: Dict[DetectionModelType, ZeroShotDetection] = {}
        self._model_cache_lock = threading.RLock()
        
        # Thread pool for concurrent processing
        self._executor: Optional[ThreadPoolExecutor] = None
        self._executor_lock = threading.Lock()
        
        # Processing statistics
        self._stats = {
            'total_requests': 0,
            'successful_requests': 0,
            'failed_requests': 0,
            'total_processing_time': 0.0
        }
        self._stats_lock = threading.Lock()
        
        self.logger.info(f"ZeroshotDetectionProcessor initialized with {self.config.model_type.value}")
        self.logger.info(f"Batch config: size={self.config.batch_config.batch_size}, workers={self.config.batch_config.max_workers}")
    
    def _get_or_create_model(self, model_type: DetectionModelType) -> ZeroShotDetection:
        """
        Get cached model or create new one (thread-safe).
        
        Args:
            model_type: Type of model to get/create
            
        Returns:
            ZeroShotDetection instance
        """
        with self._model_cache_lock:
            if model_type not in self._model_cache:
                self.logger.info(f"Creating new {model_type.value} model instance")
                self._model_cache[model_type] = DetectionModelFactory.create_model(
                    model_type, 
                    self.config.model_config
                )
                self.logger.info(f"Model {model_type.value} ready")
            
            return self._model_cache[model_type]
    
    def _get_executor(self) -> ThreadPoolExecutor:
        """Get or create thread pool executor (thread-safe)"""
        with self._executor_lock:
            if self._executor is None:
                max_workers = self.config.batch_config.max_workers
                self._executor = ThreadPoolExecutor(
                    max_workers=max_workers,
                    thread_name_prefix="ZeroShotDetection"
                )
                self.logger.debug(f"Created ThreadPoolExecutor with {max_workers} workers")
            
            return self._executor
    
    def _update_stats(self, success: bool, processing_time: float) -> None:
        """Update processing statistics (thread-safe)"""
        with self._stats_lock:
            self._stats['total_requests'] += 1
            self._stats['total_processing_time'] += processing_time
            
            if success:
                self._stats['successful_requests'] += 1
            else:
                self._stats['failed_requests'] += 1
    
    def _process_single_request(self, request: DetectionRequest) -> DetectionResponse:
        """
        Process a single detection request.
        
        Args:
            request: Detection request to process
            
        Returns:
            DetectionResponse with results or error
        """
        start_time = time.time()
        
        try:
            # Get model instance
            model = self._get_or_create_model(self.config.model_type)
            
            # Prepare image source
            image_source: ImageSource = request.image.image_path
            
            # Prepare text prompt
            text_prompt = request.config.prompt_name
            
            # Run detection
            detection_result = model.predict(
                image=image_source,
                text_prompt=text_prompt,
                box_threshold=request.config.threshold
            )
            
            # Convert to AutoAnnotationResult format
            results = []
            for i in range(len(detection_result.boxes)):
                # Grounding DINO returns boxes in normalized (cx, cy, w, h) format
                box_tensor = detection_result.boxes[i]
                cx, cy, w, h = box_tensor.tolist()
                
                # Convert from center-width-height to top-left-width-height format
                # Ensure coordinates are in 0-1 range (normalized)
                x = max(0.0, min(1.0, cx - w/2))  # top-left x
                y = max(0.0, min(1.0, cy - h/2))  # top-left y
                width = max(0.0, min(1.0, w))      # width
                height = max(0.0, min(1.0, h))     # height
                
                result = AutoAnnotationResult(
                    class_name=request.config.class_name,
                    confidence=float(detection_result.scores[i]),
                    bounding_box=BoundingBox(x=x, y=y, width=width, height=height),
                    image_id=request.image.id
                )
                results.append(result)
            
            processing_time = time.time() - start_time
            self._update_stats(True, processing_time)
            
            self.logger.debug(f"Processed request {request.request_id}: {len(results)} detections in {processing_time:.3f}s")
            
            return DetectionResponse(
                request_id=request.request_id,
                image_id=request.image.id,
                results=results,
                processing_time=processing_time,
                success=True
            )
            
        except Exception as e:
            processing_time = time.time() - start_time
            self._update_stats(False, processing_time)
            
            error_message = f"Detection failed: {str(e)}"
            self.logger.error(f"Request {request.request_id} failed: {error_message}")
            
            return DetectionResponse(
                request_id=request.request_id,
                image_id=request.image.id,
                results=[],
                processing_time=processing_time,
                success=False,
                error_message=error_message
            )
    
    def _process_batch(self, batch: List[DetectionRequest]) -> List[DetectionResponse]:
        """
        Process a batch of requests concurrently.
        
        Args:
            batch: List of detection requests
            
        Returns:
            List of detection responses
        """
        if not batch:
            return []
        
        self.logger.debug(f"Processing batch of {len(batch)} requests")
        
        executor = self._get_executor()
        responses = []
        
        # Submit all requests in the batch
        future_to_request = {
            executor.submit(self._process_single_request, request): request 
            for request in batch
        }
        
        # Collect results as they complete
        for future in as_completed(future_to_request, timeout=self.config.batch_config.timeout_seconds):
            try:
                response = future.result()
                responses.append(response)
            except Exception as e:
                request = future_to_request[future]
                self.logger.error(f"Batch processing error for request {request.request_id}: {e}")
                
                # Create error response
                error_response = DetectionResponse(
                    request_id=request.request_id,
                    image_id=request.image.id,
                    results=[],
                    processing_time=0.0,
                    success=False,
                    error_message=f"Batch processing error: {str(e)}"
                )
                responses.append(error_response)
        
        return responses
    
    def process_detections(
        self,
        requests: List[DetectionRequest],
        callback: Optional[Callable[[List[DetectionResponse]], None]] = None
    ) -> List[DetectionResponse]:
        """
        Process detection requests in batches.
        
        Args:
            requests: List of detection requests
            callback: Optional callback for each completed batch
            
        Returns:
            List of all detection responses
        """
        if not requests:
            return []
        
        self.logger.info(f"Processing {len(requests)} detection requests")
        
        all_responses = []
        batch_size = self.config.batch_config.batch_size
        
        # Process in batches
        for i in range(0, len(requests), batch_size):
            batch = requests[i:i + batch_size]
            batch_responses = self._process_batch(batch)
            all_responses.extend(batch_responses)
            
            # Call callback if provided
            if callback:
                try:
                    callback(batch_responses)
                except Exception as e:
                    self.logger.error(f"Callback error: {e}")
            
            self.logger.debug(f"Completed batch {i//batch_size + 1}/{(len(requests) + batch_size - 1)//batch_size}")
        
        success_count = sum(1 for r in all_responses if r.success)
        self.logger.info(f"Detection processing complete: {success_count}/{len(all_responses)} successful")
        
        return all_responses
    
    async def process_detections_async(
        self,
        requests: List[DetectionRequest],
        callback: Optional[Callable[[List[DetectionResponse]], None]] = None
    ) -> List[DetectionResponse]:
        """
        Process detection requests asynchronously.
        
        Args:
            requests: List of detection requests
            callback: Optional callback for each completed batch
            
        Returns:
            List of all detection responses
        """
        if not self.config.enable_async:
            # Fallback to synchronous processing
            return self.process_detections(requests, callback)
        
        # Run synchronous processing in thread pool to avoid blocking
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None, 
            self.process_detections, 
            requests, 
            callback
        )
    
    def create_detection_request(
        self,
        image: AnnotationImage,
        config: AnnotationConfig,
        dataset_id: UUID,
        request_id: Optional[str] = None
    ) -> DetectionRequest:
        """
        Helper method to create a detection request.
        
        Args:
            image: Annotation image
            config: Annotation configuration
            dataset_id: Dataset ID
            request_id: Optional request ID (generates one if None)
            
        Returns:
            DetectionRequest instance
        """
        if request_id is None:
            request_id = f"{dataset_id}_{image.id}_{int(time.time() * 1000)}"
        
        return DetectionRequest(
            request_id=request_id,
            image=image,
            config=config,
            dataset_id=dataset_id
        )
    
    def is_ready(self) -> bool:
        """
        Check if processor is ready to handle requests.
        
        Returns:
            True if ready, False otherwise
        """
        try:
            # Try to get model - this will create it if needed
            model = self._get_or_create_model(self.config.model_type)
            return model is not None
        except Exception as e:
            self.logger.error(f"Processor readiness check failed: {e}")
            return False
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get processing statistics.
        
        Returns:
            Dictionary with processing statistics
        """
        with self._stats_lock:
            stats = self._stats.copy()
            
        # Calculate derived metrics
        if stats['total_requests'] > 0:
            stats['success_rate'] = stats['successful_requests'] / stats['total_requests']
            stats['average_processing_time'] = stats['total_processing_time'] / stats['total_requests']
        else:
            stats['success_rate'] = 0.0
            stats['average_processing_time'] = 0.0
        
        return stats
    
    def cleanup(self) -> None:
        """Clean up resources"""
        self.logger.info("Cleaning up ZeroshotDetectionProcessor...")
        
        # Shutdown thread pool
        with self._executor_lock:
            if self._executor:
                self._executor.shutdown(wait=True)
                self._executor = None
        
        # Clean up models
        with self._model_cache_lock:
            for model in self._model_cache.values():
                if hasattr(model, '_cleanup'):
                    model._cleanup()
            self._model_cache.clear()
        
        self.logger.info("ZeroshotDetectionProcessor cleanup complete")
    
    def __enter__(self) -> 'ZeroshotDetectionProcessor':
        """Context manager entry"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Context manager exit with cleanup"""
        self.cleanup()