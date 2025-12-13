"""
RF-DETR Detector for object detection
"""
import cv2
import logging
import os
import torch
from typing import List, Dict, Optional

try:
    from rfdetr import RFDETRNano, RFDETRSmall, RFDETRMedium, RFDETRBase, RFDETRLarge
    RFDETR_AVAILABLE = True
except ImportError:
    RFDETR_AVAILABLE = False
    RFDETRNano = RFDETRSmall = RFDETRMedium = RFDETRBase = RFDETRLarge = None

from .BaseDetector import BaseDetector
from ..models.AIModel import AIModel


logging.getLogger("ultralytics").setLevel(logging.WARNING)


class RFDETRDetector(BaseDetector):
    """RF-DETR detector for object detection"""
    
    def __init__(self):
        if not RFDETR_AVAILABLE:
            raise ImportError(
                "RF-DETR is required but not installed. Install it with:\n"
                "pip install 'rfdetr<=1.2.0'\n"
                "See the documentation for more details."
            )
        self.model = None
        self.metadata: Optional[AIModel] = None
        self.logger = logging.getLogger(__name__)
        # Use GPU if available, otherwise CPU
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        # Reduce device logging
    
    def _detect_model_variant(self, model_path: str):
        """
        Automatically detect the correct RF-DETR variant by trying to load the weights.
        Returns the appropriate RF-DETR model or None if all attempts fail.
        """
        variants = [
            ("Nano", RFDETRNano),
            ("Small", RFDETRSmall),
            ("Medium", RFDETRMedium),
            ("Base", RFDETRBase),
            ("Large", RFDETRLarge)
        ]
        
        for variant_name, variant_class in variants:
            try:
                self.logger.debug(f"🔍 Trying RF-DETR {variant_name} variant...")
                temp_model = variant_class(pretrain_weights=model_path)
                self.logger.info(f"✅ Successfully loaded RF-DETR {variant_name} variant")
                return temp_model, variant_name
            except Exception as e:
                # Only log at debug level to avoid cluttering logs
                self.logger.debug(f"RF-DETR {variant_name} variant failed: {e}")
                continue
        
        return None, None
    
    def load_model(self, model_path: str, model_metadata: AIModel) -> bool:
        """
        Load RF-DETR model from file.
        
        Args:
            model_path: Path to RF-DETR model file
            model_metadata: AIModel metadata
            
        Returns:
            bool: True if successful, False otherwise
        """
        self.metadata = model_metadata
        
        if not os.path.isfile(model_path) or os.path.getsize(model_path) == 0:
            self.logger.error(f"❌ Model file not found or empty: {model_path}")
            self.model = None
            return False
        
        try:
            loaded_model, variant_name = self._detect_model_variant(model_path)
            
            if loaded_model is None:
                self.logger.error(f"❌ Could not load model with any RF-DETR variant")
                self.model = None
                return False
            
            self.model = loaded_model
            self.model.optimize_for_inference()
            self.logger.info(f"✅ Loaded {model_metadata.name} using RF-DETR {variant_name}")
            return True
        except Exception as e:
            self.logger.error(f"❌ Error loading RFDETR model {model_metadata.name}: {e}")
            self.model = None
            return False
    
    def detect_objects(
        self,
        frame
    ) -> List[Dict]:
        """
        Detect objects in frame using RF-DETR.
        
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
            results = self.model.predict(frame_rgb, confidence_threshold=0.0)
            
            # Get class names
            class_names = self.metadata.get_classes() if self.metadata else None
            if not class_names:
                class_names = getattr(self.model, "class_names", None)
            
            detections = []
            for class_id, conf, xyxy in zip(results.class_id, results.confidence, results.xyxy):
                label = class_names[class_id - 1] if class_names else str(class_id)
                
                detections.append({
                    "label": label,
                    "confidence": float(conf),
                    "bbox": xyxy.tolist() if hasattr(xyxy, 'tolist') else list(xyxy)
                })
            
            return detections
        except Exception as e:
            self.logger.error(f"❌ Error during RF-DETR detection: {e}")
            return []
    
    def is_loaded(self) -> bool:
        """Check if model is loaded"""
        return self.model is not None
