"""
Type definitions for auto-annotation functionality
"""
from dataclasses import dataclass
from typing import List
from uuid import UUID


@dataclass
class AnnotationConfig:
    """Configuration for annotation detection"""
    class_name: str
    prompt_name: str
    threshold: float = 0.01  # Lowest possible threshold for test annotations


@dataclass
class AutoAnnotateAllConfig:
    """Configuration for auto annotate all with explicit threshold"""
    class_name: str
    prompt_name: str
    threshold: float


@dataclass
class AnnotationImage:
    """Image data for annotation"""
    id: UUID
    image_path: str


@dataclass
class TestAnnotationRequest:
    """Request structure for test annotation"""
    config: List[AnnotationConfig]
    images: List[AnnotationImage]


@dataclass
class AutoAnnotateAllRequest:
    """Request structure for annotate all"""
    config: List[AutoAnnotateAllConfig]


@dataclass
class TestAutoAnnotationMessage:
    """Message structure for test auto annotation request"""
    dataset_id: UUID
    request_id: UUID
    annotations: TestAnnotationRequest


@dataclass
class AutoAnnotateAllMessage:
    """Message structure for auto annotate all request"""
    dataset_id: UUID
    config: List[AutoAnnotateAllConfig]


@dataclass
class BoundingBox:
    """Bounding box coordinates"""
    x: float
    y: float
    width: float
    height: float


@dataclass
class AutoAnnotationResult:
    """Result of auto annotation for a single detection"""
    class_name: str
    confidence: float
    bounding_box: BoundingBox
    image_id: UUID


# Constants for RabbitMQ exchanges and queues
class AutoAnnotationConstants:
    """Constants for auto-annotation RabbitMQ configuration"""
    
    # Exchange names
    EXCHANGE_TEST_REQUEST = "nedo.autoannotation.request.test"
    EXCHANGE_TEST_RESPONSE = "nedo.autoannotation.response.test"
    EXCHANGE_ANNOTATE_ALL = "nedo.autoannotation.annotate.all"
    EXCHANGE_PROGRESS = "nedo.autoannotation.progress"
    
    # Queue names
    QUEUE_TEST_RESPONSE = "nedo.autoannotation.response.test.queue"
    
    # Exchange types
    EXCHANGE_TYPE_DIRECT = "direct"