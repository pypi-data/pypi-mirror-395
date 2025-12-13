from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Tuple, Union
from enum import Enum
from PIL import Image

import numpy as np
import torch

ImageSource = Union[str, Path, np.ndarray, Image.Image]
BoundingBox = Tuple[float, float, float, float]


@dataclass
class ModelConfig(ABC):
    """Abstract base class for model configuration."""
    device: str
    box_threshold: float
    text_threshold: float
    
    @abstractmethod
    def validate(self) -> None:
        """Validate configuration parameters."""
        pass

class DeviceType(Enum):
    """Supported device types."""
    CPU = "cpu"
    CUDA = "cuda"
    MPS = "mps"  # For Apple Silicon


@dataclass
class DetectionResult:
    """
    Type-safe container for detection results.
    
    Attributes:
        boxes: Bounding boxes in normalized xyxy format (N, 4)
        scores: Confidence scores (N,)
        labels: Predicted class labels (N,)
        image_shape: Original image shape (height, width)
    """
    boxes: torch.Tensor  # Shape: (N, 4)
    scores: torch.Tensor  # Shape: (N,)
    labels: List[str]  # Length: N
    image_shape: Tuple[int, int]  # (height, width)
    
    def __post_init__(self) -> None:
        """Validate detection result consistency."""
        n_boxes = len(self.boxes)
        if len(self.scores) != n_boxes:
            raise ValueError(
                f"Mismatch: {n_boxes} boxes but {len(self.scores)} scores"
            )
        if len(self.labels) != n_boxes:
            raise ValueError(
                f"Mismatch: {n_boxes} boxes but {len(self.labels)} labels"
            )
    
    def __len__(self) -> int:
        """Return number of detections."""
        return len(self.boxes)
    
    def to_dict(self) -> Dict[str, Union[torch.Tensor, List[str], Tuple[int, int]]]:
        """Convert to dictionary format."""
        return {
            "boxes": self.boxes,
            "scores": self.scores,
            "labels": self.labels,
            "image_shape": self.image_shape
        }
    
    def filter_by_score(self, threshold: float) -> 'DetectionResult':
        """
        Filter detections by confidence score.
        
        Args:
            threshold: Minimum confidence score
            
        Returns:
            New DetectionResult with filtered detections
        """
        mask = self.scores >= threshold
        return DetectionResult(
            boxes=self.boxes[mask],
            scores=self.scores[mask],
            labels=[label for label, keep in zip(self.labels, mask) if keep],
            image_shape=self.image_shape
        )
