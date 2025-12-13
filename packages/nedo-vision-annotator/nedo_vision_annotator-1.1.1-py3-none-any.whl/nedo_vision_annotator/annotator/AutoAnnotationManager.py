"""
Auto Annotation Manager - Main coordinator for auto annotation workflow
"""
import logging
from typing import Optional, Dict

from ..services.AutoAnnotationGrpcClient import AutoAnnotationGrpcClient
from ..services.AnnotatorGrpcClient import AnnotatorGrpcClient
from ..tasks.TestAutoAnnotationHandler import TestAutoAnnotationHandler
from ..tasks.AutoAnnotateAllHandler import AutoAnnotateAllHandler
from ..tasks.ZeroshotDetectionProcessor import ZeroshotDetectionProcessor, ProcessorConfig


class AutoAnnotationManager:
    def __init__(self, config: Dict):
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        self.server_host = config['server_host']
        self.server_port = int(config['server_port'])
        self.token = config['token']
        self.annotator_id = config.get('annotator_id')
        
        self.rabbitmq_host = config.get('rabbitmq_host', 'localhost')
        self.rabbitmq_port = int(config.get('rabbitmq_port', 5672))
        self.rabbitmq_username = config.get('rabbitmq_username', 'guest')
        self.rabbitmq_password = config.get('rabbitmq_password', 'guest')
        
        self.auto_annotation_client: Optional[AutoAnnotationGrpcClient] = None
        self.annotator_client: Optional[AnnotatorGrpcClient] = None
        self.test_annotation_handler: Optional[TestAutoAnnotationHandler] = None
        self.annotate_all_handler: Optional[AutoAnnotateAllHandler] = None
        
        self.is_running = False
        
        self.logger.info("✅ AutoAnnotationManager initialized")
    
    def initialize(self) -> bool:
        try:
            self.logger.info("🚀 Initializing AutoAnnotationManager components...")
            
            # Initialize gRPC clients
            self.auto_annotation_client = AutoAnnotationGrpcClient(
                self.server_host,
                self.server_port,
                self.token
            )
            
            self.annotator_client = AnnotatorGrpcClient(
                self.server_host,
                self.server_port,
                self.token
            )
            
            # Initialize detection processor (shared between handlers)
            processor_config = self.config.get('detection_processor_config')
            detection_processor = ZeroshotDetectionProcessor(
                config=ProcessorConfig(**processor_config) if processor_config else ProcessorConfig(),
                logger=self.logger
            )
            
            # Initialize test auto-annotation handler
            self.test_annotation_handler = TestAutoAnnotationHandler(
                rabbitmq_host=self.rabbitmq_host,
                rabbitmq_port=self.rabbitmq_port,
                rabbitmq_username=self.rabbitmq_username,
                rabbitmq_password=self.rabbitmq_password,
                annotator_id=self.annotator_id,
                annotator_client=self.annotator_client,
                detection_processor=detection_processor
            )
            
            if not self.test_annotation_handler.setup():
                return False
            
            # Initialize auto annotate all handler
            batch_size = self.config.get('annotate_all.batch_size', 3)
            grpc_batch_size = self.config.get('annotate_all.grpc_batch_size', 15)
            
            self.annotate_all_handler = AutoAnnotateAllHandler(
                rabbitmq_host=self.rabbitmq_host,
                rabbitmq_port=self.rabbitmq_port,
                rabbitmq_username=self.rabbitmq_username,
                rabbitmq_password=self.rabbitmq_password,
                annotator_id=self.annotator_id,
                annotator_client=self.annotator_client,
                auto_annotation_client=self.auto_annotation_client,
                detection_processor=detection_processor,
                batch_size=batch_size,
                grpc_batch_size=grpc_batch_size
            )
            
            if not self.annotate_all_handler.setup():
                return False
            
            self.logger.info("✅ AutoAnnotationManager initialized successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Failed to initialize AutoAnnotationManager: {e}")
            import traceback
            self.logger.error(traceback.format_exc())
            return False
    
    
    def start(self) -> bool:
        """
        Start the auto annotation manager.
        
        Returns:
            bool: True if started successfully, False otherwise
        """
        if self.is_running:
            self.logger.warning("⚠️ AutoAnnotationManager already running")
            return False
        
        try:
            self.logger.info("🚀 Starting AutoAnnotationManager...")
            
            # Start test annotation handler
            if self.test_annotation_handler and not self.test_annotation_handler.start():
                self.logger.error("❌ Failed to start test annotation handler")
                return False
            
            # Start annotate all handler
            if self.annotate_all_handler and not self.annotate_all_handler.start():
                self.logger.error("❌ Failed to start annotate all handler")
                return False
            
            self.is_running = True
            
            self.logger.info("✅ AutoAnnotationManager started successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Failed to start AutoAnnotationManager: {e}")
            import traceback
            self.logger.error(traceback.format_exc())
            return False
    
    def stop(self) -> None:
        """Stop the auto annotation manager"""
        if not self.is_running:
            return
        
        try:
            self.logger.info("🛑 Stopping AutoAnnotationManager...")
            
            self.is_running = False
            
            # Stop handlers
            if self.test_annotation_handler:
                self.test_annotation_handler.stop()
            
            if self.annotate_all_handler:
                self.annotate_all_handler.stop()
            
            # Close gRPC clients
            if self.auto_annotation_client:
                self.auto_annotation_client.close_channel()
                
            if self.annotator_client:
                self.annotator_client.close_channel()
            
            self.logger.info("✅ AutoAnnotationManager stopped")
            
        except Exception as e:
            self.logger.error(f"❌ Error stopping AutoAnnotationManager: {e}")
    
    def get_processing_stats(self) -> Dict:
        """
        Get processing statistics from both handlers.
        
        Returns:
            Dictionary with processing statistics
        """
        stats = {}
        
        if self.test_annotation_handler:
            stats['test_annotation'] = self.test_annotation_handler.get_processor_stats()
            
        if self.annotate_all_handler:
            stats['annotate_all'] = self.annotate_all_handler.get_processor_stats()
            
        return stats
    
    def is_processing_ready(self) -> bool:
        """
        Check if the auto annotation manager is ready to process requests.
        
        Returns:
            True if ready, False otherwise
        """
        test_ready = (
            self.test_annotation_handler is not None and 
            self.test_annotation_handler.is_connected()
        )
        
        annotate_all_ready = (
            self.annotate_all_handler is not None and 
            self.annotate_all_handler.is_connected()
        )
        
        return self.is_running and test_ready and annotate_all_ready
