"""
YOLO Detector for object detection using Ultralytics YOLO
"""
import cv2
import logging
import os
import torch
from typing import List, Dict, Optional
from ultralytics import YOLO
from .BaseDetector import BaseDetector
from ..models.AIModel import AIModel


logging.getLogger("ultralytics").setLevel(logging.WARNING)


class YOLODetector(BaseDetector):
    """YOLO detector using Ultralytics library"""
    
    def __init__(self):
        self.model = None
        self.metadata: Optional[AIModel] = None
        self.logger = logging.getLogger(__name__)
        # Use GPU if available, otherwise CPU
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.logger.info(f"🖥️  YOLO will use device: {self.device}")
    
    def load_model(self, model_path: str, model_metadata: AIModel) -> bool:
        """
        Load YOLO model from file.
        
        Args:
            model_path: Path to YOLO model file
            model_metadata: AIModel metadata
            
        Returns:
            bool: True if successful, False otherwise
        """
        self.metadata = model_metadata
        
        # Check if file exists and has content
        if not os.path.isfile(model_path) or os.path.getsize(model_path) == 0:
            self.logger.error(f"❌ Model file not found or empty: {model_path}")
            self.model = None
            return False
        
        try:
            self.logger.info(f"📦 Loading YOLO model: {model_metadata.name}")
            self.model = YOLO(model_path)
            
            # Move model to GPU if available
            if self.device == "cuda":
                self.model.to(self.device)
                self.logger.info(f"🚀 Model moved to GPU")
            
            self.logger.info(f"✅ YOLO model loaded successfully on {self.device}")
            return True
        except Exception as e:
            self.logger.error(f"❌ Error loading YOLO model {model_metadata.name}: {e}")
            self.model = None
            return False
    
    def detect_objects(
        self,
        frame
    ) -> List[Dict]:
        """
        Detect objects in frame using YOLO.
        
        Args:
            frame: Image frame (numpy array, BGR format)
            
        Returns:
            List of detections with label, confidence, and bbox
        """
        if self.model is None:
            return []
        
        try:
            # Convert BGR to RGB
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.model(frame_rgb, verbose=False)
            
            # Get class names
            class_names = self.metadata.get_classes() if self.metadata else None
            if not class_names:
                class_names = self.model.names
            
            detections = []
            for box in results[0].boxes:
                class_id = int(box.cls)
                label = class_names[class_id] if class_names else str(class_id)
                confidence = float(box.conf)
                
                # Get bounding box coordinates [x1, y1, x2, y2]
                bbox = box.xyxy.tolist()[0]
                
                detections.append({
                    "label": label,
                    "confidence": confidence,
                    "bbox": bbox
                })
            
            return detections
        except Exception as e:
            self.logger.error(f"❌ Error during YOLO detection: {e}")
            return []
    
    def is_loaded(self) -> bool:
        """Check if model is loaded"""
        return self.model is not None
