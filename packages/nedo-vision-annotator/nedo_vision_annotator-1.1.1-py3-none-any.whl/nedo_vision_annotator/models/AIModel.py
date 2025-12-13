"""
AI Model entity for the annotator service
"""
import json
from typing import List, Optional


class AIModel:
    """
    AI Model entity representing a downloaded model for annotation.
    Simplified version adapted from worker core.
    """
    
    def __init__(
        self,
        id: str,
        name: str,
        ai_model_type_code: str,
        version: str,
        file_path: str,
        classes: Optional[List[str]] = None
    ):
        self.id = id
        self.name = name
        self.ai_model_type_code = ai_model_type_code
        self.version = version
        self.file_path = file_path
        self._classes = classes or []
    
    def get_classes(self) -> List[str]:
        """Get list of class names"""
        return self._classes
    
    def set_classes(self, classes: List[str]) -> None:
        """Set list of class names"""
        self._classes = classes
    
    def is_yolo_model(self) -> bool:
        """Check if this is a YOLO model"""
        return self.ai_model_type_code.lower() == 'yolo'
    
    def is_rfdetr_model(self) -> bool:
        """Check if this is an RF-DETR model"""
        return self.ai_model_type_code.lower() == 'rf_detr'
    
    def __repr__(self):
        return (
            f"<AIModel(id={self.id}, name={self.name}, type={self.ai_model_type_code}, "
            f"version={self.version})>"
        )
    
    def __str__(self):
        return (
            f"AIModel(id={self.id}, name={self.name}, type={self.ai_model_type_code}, "
            f"version={self.version})"
        )
    
    @classmethod
    def from_grpc_response(cls, grpc_model):
        """
        Create AIModel instance from gRPC AIModelResponse.
        
        Args:
            grpc_model: AIModelResponse from gRPC
            
        Returns:
            AIModel instance
        """
        return cls(
            id=grpc_model.id,
            name=grpc_model.name,
            ai_model_type_code=grpc_model.ai_model_type_code,
            version=grpc_model.version,
            file_path=grpc_model.file_path,
            classes=list(grpc_model.classes) if grpc_model.classes else []
        )
