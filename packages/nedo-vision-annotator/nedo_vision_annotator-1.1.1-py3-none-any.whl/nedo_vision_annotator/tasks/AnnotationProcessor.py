"""
Annotation Processor - Handles image processing and annotation detection
"""
import cv2
import logging
import numpy as np
from typing import Dict

from ..services.AnnotatorGrpcClient import AnnotatorGrpcClient
from ..database import DatabaseSession, DatasetAnnotationRepository
from ..core.DatasetManager import DatasetManager
from ..core.ModelLoader import ModelLoader


class AnnotationProcessor:
    def __init__(
        self,
        annotator_client: AnnotatorGrpcClient,
        db_session: DatabaseSession,
        dataset_manager: DatasetManager,
        model_loader: ModelLoader
    ):
        self.annotator_client = annotator_client
        self.db_session = db_session
        self.dataset_manager = dataset_manager
        self.model_loader = model_loader
        self.logger = logging.getLogger(__name__)
    
    def process_annotation_request(
        self,
        dataset_item_id: str,
        image_path: str,
        dataset_id: str
    ) -> None:
        """
        Process annotation request for a single image.
        
        Args:
            dataset_item_id: ID of the dataset item
            image_path: Path to the image file
            dataset_id: ID of the dataset
        """
        try:
            # Get dataset info
            dataset = self.dataset_manager.get_dataset(dataset_id)
            if not dataset:
                self.logger.error(f"❌ Unknown dataset: {dataset_id}")
                return
            
            # Load model if needed
            ai_model_id = dataset.get('ai_model_id')
            if not ai_model_id:
                self.logger.warning(f"⚠️ No AI model assigned to dataset: {dataset['name']}")
                return
            
            if not self.model_loader.ensure_model_loaded(ai_model_id):
                self.logger.error(f"❌ Failed to load model for dataset: {dataset['name']}")
                return
            
            # Get the detector for this model
            detector = self.model_loader.get_detector(ai_model_id)
            if not detector:
                self.logger.error(f"❌ Detector not found for model: {ai_model_id}")
                return
            
            # Download image
            image_data = self.annotator_client.get_image(image_path)
            
            if not image_data:
                self.logger.error(f"❌ Failed to download image: {image_path}")
                return
            
            # Convert bytes to numpy array
            nparr = np.frombuffer(image_data, np.uint8)
            image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            
            if image is None:
                self.logger.error(f"❌ Failed to decode image: {image_path}")
                return
            
            # Run detection
            detections = detector.detect_objects(image)
            
            if detections:
                self.logger.info(f"✅ Processed: {len(detections)} objects found")
                # Get image dimensions for normalization
                img_height, img_width = image.shape[:2]
                
                annotations = []
                for detection in detections:
                    bbox = detection['bbox']
                    # Normalize bbox coordinates to 0-1 range
                    annotations.append({
                        'label': detection['label'],
                        'bbox_x1': float(bbox[0]) / img_width,
                        'bbox_y1': float(bbox[1]) / img_height,
                        'bbox_x2': float(bbox[2]) / img_width,
                        'bbox_y2': float(bbox[3]) / img_height
                    })
                
                repo = DatasetAnnotationRepository(self.db_session)
                repo.create(
                    dataset_item_id=dataset_item_id,
                    dataset_id=dataset_id,
                    annotations=annotations
                )
            
        except Exception as e:
            self.logger.error(f"❌ Error processing annotation request: {e}")
            import traceback
            self.logger.error(traceback.format_exc())
