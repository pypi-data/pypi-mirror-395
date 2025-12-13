"""
Base detector abstract class for object detection
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Optional


class BaseDetector(ABC):
    """
    Abstract base class for all object detectors.
    """

    @abstractmethod
    def load_model(self, model_path: str, model_metadata) -> bool:
        """
        Load model from file path.
        
        Args:
            model_path: Path to model file
            model_metadata: AIModel metadata
            
        Returns:
            bool: True if successful, False otherwise
        """
        pass

    @abstractmethod
    def detect_objects(
        self,
        frame
    ) -> List[Dict]:
        """
        Detect objects in the input frame.
        
        Args:
            frame: Image/frame (numpy array)
            
        Returns:
            List of detections: [{"label": str, "confidence": float, "bbox": [x1, y1, x2, y2]}, ...]
        """
        pass
    
    @abstractmethod
    def is_loaded(self) -> bool:
        """Check if model is loaded and ready"""
        pass
