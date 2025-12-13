"""
Model Loader - Handles AI model loading and caching
"""
import os
import logging
from typing import Dict, Optional

from ..services.AnnotatorGrpcClient import AnnotatorGrpcClient
from ..models.AIModel import AIModel
from ..detection.YOLODetector import YOLODetector
from ..detection.RFDETRDetector import RFDETRDetector, RFDETR_AVAILABLE


class ModelLoader:
    """
    Manages AI model loading, caching, and detector instantiation.
    Supports multiple models with lazy loading and reuse.
    """
    
    def __init__(self, annotator_client: AnnotatorGrpcClient, models_dir: str):
        """
        Initialize ModelLoader.
        
        Args:
            annotator_client: gRPC client for annotator operations
            models_dir: Directory to store downloaded models
        """
        self.annotator_client = annotator_client
        self.models_dir = models_dir
        self.logger = logging.getLogger(__name__)
        
        # Model cache
        self.loaded_models: Dict[str, AIModel] = {}  # model_id -> AIModel
        self.loaded_detectors: Dict[str, any] = {}  # model_id -> Detector instance
        
        os.makedirs(self.models_dir, exist_ok=True)
    
    def ensure_model_loaded(self, ai_model_id: str) -> bool:
        """
        Ensure AI model is loaded and ready. Reuses existing models if already loaded.
        
        Args:
            ai_model_id: ID of the AI model
            
        Returns:
            bool: True if model is loaded, False otherwise
        """
        try:
            self.logger.info(f"📦 Loading AI model: {ai_model_id}")
            
            # Get model info from annotator service
            models = self.annotator_client.get_ai_model_list()
            if not models:
                self.logger.error("❌ Failed to fetch AI model list")
                return False
            
            # Find the model
            model_data = next((m for m in models if m['id'] == ai_model_id), None)
            if not model_data:
                self.logger.error(f"❌ Model not found: {ai_model_id}")
                return False
            
            # Create AIModel object from data
            model = AIModel(
                id=model_data['id'],
                name=model_data['name'],
                ai_model_type_code=model_data['ai_model_type_code'],
                version=model_data['version'],
                file_path=model_data['file_path'],
                classes=model_data['classes']
            )
            
            # Check if model file exists locally
            model_path = os.path.join(self.models_dir, model.file_path)
            need_download = False
            
            if not os.path.exists(model_path):
                need_download = True
                # Reduce verbosity
            else:
                # Check if version changed (compare with cached model)
                if ai_model_id in self.loaded_models:
                    cached_model = self.loaded_models[ai_model_id]
                    if cached_model.version != model.version:
                        need_download = True
                        self.logger.info(f"🔄 Model version changed ({cached_model.version} -> {model.version}), re-downloading")
                        # Clear old cached detector
                        if ai_model_id in self.loaded_detectors:
                            del self.loaded_detectors[ai_model_id]
                    else:
                        # Same version, check if already loaded and ready
                        if ai_model_id in self.loaded_detectors:
                            detector = self.loaded_detectors[ai_model_id]
                            if detector and detector.is_loaded():
                                self.logger.debug(f"♻️  Reusing already loaded model: {ai_model_id}")
                                return True
            
            # Download if needed
            if need_download:
                if not self.annotator_client.download_ai_model(ai_model_id, model_path):
                    self.logger.error(f"❌ Failed to download model: {model.name}")
                    return False
            
            # Create detector based on model type
            detector = self._create_detector(model)
            if not detector:
                return False
            
            # Load the model
            if not detector.load_model(model_path, model):
                self.logger.error(f"❌ Failed to load model: {model.name}")
                return False
            
            # Cache the model and detector
            self.loaded_models[ai_model_id] = model
            self.loaded_detectors[ai_model_id] = detector
            
            self.logger.info(f"✅ Model loaded: {model.name}")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Error loading model: {e}")
            import traceback
            self.logger.error(traceback.format_exc())
            return False
    
    def _create_detector(self, model: AIModel):
        """
        Create detector instance based on model type.
        
        Args:
            model: AIModel instance
            
        Returns:
            Detector instance or None if unsupported
        """
        if model.is_yolo_model():
            self.logger.info("🔧 Creating YOLO detector...")
            return YOLODetector()
        elif model.is_rfdetr_model():
            if not RFDETR_AVAILABLE:
                self.logger.error("❌ RF-DETR not available, please install it")
                return None
            self.logger.info("🔧 Creating RF-DETR detector...")
            return RFDETRDetector()
        else:
            self.logger.error(f"❌ Unsupported model type: {model.ai_model_type_code}")
            return None
    
    def get_detector(self, ai_model_id: str):
        """
        Get cached detector for a model.
        
        Args:
            ai_model_id: ID of the AI model
            
        Returns:
            Detector instance or None if not loaded
        """
        return self.loaded_detectors.get(ai_model_id)
