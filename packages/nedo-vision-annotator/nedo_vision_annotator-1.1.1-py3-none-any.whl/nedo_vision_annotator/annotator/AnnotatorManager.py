"""
Annotator Manager - Main coordinator for annotation workflow
"""
import os
import logging
from typing import Optional, Dict

from ..services.AnnotatorGrpcClient import AnnotatorGrpcClient
from ..services.AutoAnnotationGrpcClient import AutoAnnotationGrpcClient
from ..database import DatabaseSession, DatasetAnnotationRepository
from ..core.ModelLoader import ModelLoader
from ..core.DatasetManager import DatasetManager
from ..tasks.AnnotationProcessor import AnnotationProcessor
from ..tasks.AnnotationSender import AnnotationSender
from ..tasks.StatusReporter import StatusReporter
from ..tasks.MessageHandler import MessageHandler


class AnnotatorManager:
    def __init__(self, config: Dict):
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        self.server_host = config['server_host']
        self.server_port = int(config['server_port'])
        self.token = config['token']
        self.storage_path = config['storage_path']
        self.batch_size = config['batch_size']
        self.send_interval = config['send_interval']
        self.annotator_id = config.get('annotator_id')
        
        self.rabbitmq_host = config.get('rabbitmq_host')
        self.rabbitmq_port = int(config.get('rabbitmq_port', 5672))
        self.rabbitmq_username = config.get('rabbitmq_username')
        self.rabbitmq_password = config.get('rabbitmq_password')
        
        self.db_session: Optional[DatabaseSession] = None

        self.annotator_client: Optional[AnnotatorGrpcClient] = None
        self.auto_annotation_client: Optional[AutoAnnotationGrpcClient] = None
        
        self.model_loader: Optional[ModelLoader] = None
        self.dataset_manager: Optional[DatasetManager] = None
        self.annotation_processor: Optional[AnnotationProcessor] = None
        self.annotation_sender: Optional[AnnotationSender] = None
        self.status_reporter: Optional[StatusReporter] = None
        self.message_handler: Optional[MessageHandler] = None
        
        self.is_running = False
        
        self.logger.info("✅ AnnotatorManager initialized")
    
    def initialize(self) -> bool:
        try:
            self.logger.info("🚀 Initializing AnnotatorManager components...")
            
            db_path = os.path.join(self.storage_path, 'annotations.db')
            database_url = f"sqlite:///{db_path}"
            self.db_session = DatabaseSession(database_url)
            
            self.annotator_client = AnnotatorGrpcClient(
                self.server_host,
                self.server_port,
                self.token
            )
            
            self.auto_annotation_client = AutoAnnotationGrpcClient(
                self.server_host,
                self.server_port,
                self.token
            )
            
            models_dir = os.path.join(self.storage_path, 'models')
            
            self.model_loader = ModelLoader(self.annotator_client, models_dir)
            self.dataset_manager = DatasetManager(self.annotator_client)
            self.annotation_processor = AnnotationProcessor(
                self.annotator_client,
                self.db_session,
                self.dataset_manager,
                self.model_loader
            )
            self.annotation_sender = AnnotationSender(
                self.annotator_client,
                self.db_session,
                self.batch_size,
                self.send_interval
            )
            
            self.logger.info("📋 Fetching assigned datasets...")
            self.dataset_manager.fetch_datasets()
            
            # Preload models for all assigned datasets before starting to consume messages
            self.logger.info("📦 Preloading models for assigned datasets...")
            if not self._preload_models():
                self.logger.warning("⚠️ Some models failed to preload, but continuing...")
            
            self.message_handler = MessageHandler(
                self.rabbitmq_host,
                self.rabbitmq_port,
                self.rabbitmq_username,
                self.rabbitmq_password,
                self.annotator_id,
                self._on_annotation_request
            )
            
            if not self.message_handler.setup():
                return False
            
            # Initialize status reporter (after message handler setup)
            self.status_reporter = StatusReporter(
                self.annotator_client,
                self.message_handler.get_consumer()
            )
            
            self.logger.info("✅ AnnotatorManager initialized successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Failed to initialize AnnotatorManager: {e}")
            import traceback
            self.logger.error(traceback.format_exc())
            return False
    
    def _preload_models(self) -> bool:
        """
        Preload AI models for all assigned datasets before starting message consumption.
        This ensures models are downloaded and loaded before annotation requests arrive.
        
        Returns:
            bool: True if all models loaded successfully, False if any failed
        """
        try:
            datasets = self.dataset_manager.get_all_datasets()
            
            if not datasets:
                self.logger.info("ℹ️  No datasets assigned, skipping model preload")
                return True
            
            # Get unique AI model IDs from datasets
            model_ids = set()
            for dataset in datasets:
                ai_model_id = dataset.get('ai_model_id')
                if ai_model_id:
                    model_ids.add(ai_model_id)
            
            if not model_ids:
                self.logger.warning("⚠️ No AI models assigned to datasets")
                return True
            
            self.logger.info(f"📦 Preloading {len(model_ids)} unique model(s)...")
            
            all_success = True
            for model_id in model_ids:
                self.logger.info(f"⏳ Loading model: {model_id}")
                if self.model_loader.ensure_model_loaded(model_id):
                    self.logger.info(f"✅ Model ready: {model_id}")
                else:
                    self.logger.error(f"❌ Failed to load model: {model_id}")
                    all_success = False
            
            if all_success:
                self.logger.info("✅ All models preloaded successfully")
            else:
                self.logger.warning("⚠️ Some models failed to preload")
            
            return all_success
            
        except Exception as e:
            self.logger.error(f"❌ Error during model preload: {e}")
            import traceback
            self.logger.error(traceback.format_exc())
            return False
    
    def _on_annotation_request(self, message: Dict) -> None:
        """
        Callback for processing annotation requests from RabbitMQ.
        
        Args:
            message: Message dictionary with dataset_item_id, file_path, dataset_id
        """
        self.annotation_processor.process_annotation_request(
            dataset_item_id=message['dataset_item_id'],
            image_path=message['file_path'],
            dataset_id=message['dataset_id']
        )
    
    def start(self) -> bool:
        """
        Start the annotator manager.
        
        Returns:
            bool: True if started successfully, False otherwise
        """
        if self.is_running:
            self.logger.warning("⚠️ AnnotatorManager already running")
            return False
        
        try:
            self.logger.info("🚀 Starting AnnotatorManager...")
            
            # Start message handler (RabbitMQ consumer)
            if not self.message_handler.start():
                self.logger.error("❌ Failed to start message handler")
                return False
            
            self.is_running = True
            
            # Start all background services
            self.annotation_sender.start()
            self.status_reporter.start()
            self.dataset_manager.start_polling()
            
            # Report connected status
            self.status_reporter.report_status('connected')
            
            self.logger.info("✅ AnnotatorManager started successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Failed to start AnnotatorManager: {e}")
            import traceback
            self.logger.error(traceback.format_exc())
            return False
    
    def stop(self) -> None:
        """Stop the annotator manager"""
        if not self.is_running:
            return
        
        try:
            self.logger.info("🛑 Stopping AnnotatorManager...")
            
            # Report disconnected status
            if self.status_reporter:
                self.status_reporter.report_status('disconnected')
            
            self.is_running = False
            
            # Stop all background services
            if self.annotation_sender:
                self.annotation_sender.stop()
            
            if self.status_reporter:
                self.status_reporter.stop()
            
            if self.dataset_manager:
                self.dataset_manager.stop_polling()
            
            # Stop message handler (RabbitMQ consumer)
            if self.message_handler:
                self.message_handler.stop()
            
            # Close gRPC clients
            if self.annotator_client:
                self.annotator_client.close_channel()
            
            self.logger.info("✅ AnnotatorManager stopped")
            
        except Exception as e:
            self.logger.error(f"❌ Error stopping AnnotatorManager: {e}")
