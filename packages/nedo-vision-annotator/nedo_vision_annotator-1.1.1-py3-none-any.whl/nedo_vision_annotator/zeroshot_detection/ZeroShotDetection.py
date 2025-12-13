from abc import ABC, abstractmethod
import logging
from typing import List, Optional


from abc import ABC, abstractmethod
from pathlib import Path
from typing import List, Tuple, Optional, Union

import numpy as np
import torch

from nedo_vision_annotator.types.ZeroShotDetectionType import DetectionResult, ImageSource, ModelConfig

logger = logging.getLogger(__name__)

class ZeroShotDetection(ABC):
    """
    Abstract base class for zero-shot object detection models.
    
    This class defines the interface that all zero-shot detection
    implementations must follow.
    """
    
    def __init__(self, config: ModelConfig) -> None:
        """
        Initialize detector with configuration.
        
        Args:
            config: Model-specific configuration
        """
        self.config = config
        self.config.validate()
        self.model: Optional[torch.nn.Module] = None
    
    @abstractmethod
    def _load_model(self) -> None:
        """Load the detection model. Must be implemented by subclasses."""
        pass
    
    @abstractmethod
    def load_image(self, image_source: ImageSource) -> Tuple[np.ndarray, torch.Tensor]:
        """
        Load and preprocess image.
        
        Args:
            image_source: Image from various sources
            
        Returns:
            Tuple of (original_image, transformed_image_tensor)
        """
        pass
    
    @abstractmethod
    def predict(
        self,
        image: ImageSource,
        text_prompt: str,
        box_threshold: Optional[float] = None,
        text_threshold: Optional[float] = None
    ) -> DetectionResult:
        """
        Perform zero-shot object detection.
        
        Args:
            image: Image to process
            text_prompt: Text description of objects to detect
            box_threshold: Optional confidence threshold for boxes
            text_threshold: Optional confidence threshold for text matching
            
        Returns:
            DetectionResult containing boxes, scores, and labels
        """
        pass
    
    @abstractmethod
    def annotate_image(
        self,
        image: ImageSource,
        result: DetectionResult,
        output_path: Optional[Union[str, Path]] = None
    ) -> np.ndarray:
        """
        Annotate image with detection results.
        
        Args:
            image: Original image
            result: Detection results
            output_path: Optional path to save annotated image
            
        Returns:
            Annotated image as numpy array
        """
        pass
    
    def batch_predict(
        self,
        images: List[ImageSource],
        text_prompt: str,
        **kwargs
    ) -> List[DetectionResult]:
        """
        Process multiple images.
        
        Args:
            images: List of images to process
            text_prompt: Text prompt for detection
            **kwargs: Additional arguments passed to predict()
            
        Returns:
            List of DetectionResult objects
        """
        results: List[DetectionResult] = []
        
        for idx, image in enumerate(images):
            try:
                result = self.predict(image, text_prompt, **kwargs)
                results.append(result)
                logger.info(f"Processed image {idx + 1}/{len(images)}")
                
            except Exception as e:
                logger.error(f"Failed to process image {idx}: {e}")
                raise
        
        return results
    
    def __enter__(self) -> 'ZeroShotDetection':
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Context manager exit with cleanup."""
        self._cleanup()
    
    def _cleanup(self) -> None:
        """Cleanup resources. Can be overridden by subclasses."""
        if self.model is not None and self.config.device == "cuda":
            torch.cuda.empty_cache()
        logger.info("Detector cleanup completed")