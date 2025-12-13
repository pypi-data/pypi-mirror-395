"""
Auto Annotate All Handler - Handles auto-annotation requests for entire datasets
"""
import io
import logging
import os
import tempfile
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Optional, Dict, List
from uuid import UUID
from PIL import Image

from nedo_vision_annotator.services.AutoAnnotation_pb2 import DatasetItemResponse

from ..services.RabbitMQConsumer import RabbitMQConsumer
from ..services.RabbitMQPublisher import RabbitMQPublisher, ExchangeConfig
from ..services.AnnotatorGrpcClient import AnnotatorGrpcClient
from ..services.AutoAnnotationGrpcClient import AutoAnnotationGrpcClient, AutoAnnotationResultRequest
from ..types.AutoAnnotationTypes import (
    AutoAnnotateAllMessage,
    AutoAnnotateAllConfig,
    AutoAnnotationConstants
)
from .ZeroshotDetectionProcessor import (
    DetectionProcessor, 
    DetectionRequest,
    DetectionResponse
)


class AutoAnnotateAllHandler:
    """
    Handles auto-annotation requests for entire datasets.
    Processes all images in a dataset using zero-shot detection.
    """
    
    def __init__(
        self,
        rabbitmq_host: str,
        rabbitmq_port: int,
        rabbitmq_username: str,
        rabbitmq_password: str,
        annotator_id: Optional[str],
        annotator_client: AnnotatorGrpcClient,
        auto_annotation_client: AutoAnnotationGrpcClient,
        detection_processor: DetectionProcessor = None,
        batch_size: int = 3,  # Smaller batches for more frequent progress updates
        grpc_batch_size: int = 15
    ):
        """
        Initialize AutoAnnotateAllHandler.
        
        Args:
            rabbitmq_host: RabbitMQ host
            rabbitmq_port: RabbitMQ port
            rabbitmq_username: RabbitMQ username
            rabbitmq_password: RabbitMQ password
            annotator_id: Annotator ID for routing
            annotator_client: gRPC client for annotator operations
            auto_annotation_client: gRPC client for auto annotation operations
            detection_processor: Optional detection processor for dependency injection
            batch_size: Number of images to process in parallel
            grpc_batch_size: Number of results to send to backend in each gRPC call
        """
        self.rabbitmq_host = rabbitmq_host
        self.rabbitmq_port = rabbitmq_port
        self.rabbitmq_username = rabbitmq_username
        self.rabbitmq_password = rabbitmq_password
        self.annotator_id = annotator_id
        self.annotator_client = annotator_client
        self.auto_annotation_client = auto_annotation_client
        self.batch_size = batch_size
        self.grpc_batch_size = grpc_batch_size
        self.logger = logging.getLogger(__name__)
        
        # Dependency injection for detection processor
        self.detection_processor = detection_processor
        
        self.is_running = False
        self.consumer: Optional[RabbitMQConsumer] = None
        self.progress_publisher: Optional[RabbitMQPublisher] = None
    
    def setup(self) -> bool:
        """
        Setup RabbitMQ consumer for auto annotate all requests.
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if not all([self.rabbitmq_host, self.rabbitmq_username, self.rabbitmq_password]):
                self.logger.error("❌ Missing RabbitMQ configuration")
                return False
            
            # Check if detection processor is ready
            if not self.detection_processor.is_ready():
                self.logger.error("❌ Detection processor is not ready")
                return False
            
            # Setup consumer for annotate all requests
            # Use annotator ID as routing key
            routing_key = str(self.annotator_id) if self.annotator_id else "default"
            
            self.logger.info(f"📡 Setting up auto annotate all consumer with routing key: {routing_key}")
            
            self.consumer = RabbitMQConsumer(
                host=self.rabbitmq_host,
                port=self.rabbitmq_port,
                username=self.rabbitmq_username,
                password=self.rabbitmq_password,
                queue_name=f"auto_annotate_all_{self.annotator_id}",
                callback=self._on_annotate_all_request,
                exchange_name=AutoAnnotationConstants.EXCHANGE_ANNOTATE_ALL,
                routing_key=routing_key
            )
            
            # Setup progress publisher for web progress tracking
            self.progress_publisher = RabbitMQPublisher(
                host=self.rabbitmq_host,
                port=self.rabbitmq_port,
                username=self.rabbitmq_username,
                password=self.rabbitmq_password
            )
            
            if not self.progress_publisher.connect():
                self.logger.error("❌ Failed to connect progress publisher")
                return False
            
            # Declare progress exchange
            progress_exchange = ExchangeConfig(
                name=AutoAnnotationConstants.EXCHANGE_PROGRESS,
                type="topic",
                durable=True,
                auto_delete=False
            )
            
            if not self.progress_publisher.declare_exchange(progress_exchange):
                self.logger.error("❌ Failed to declare progress exchange")
                return False
            
            self.logger.info("✅ Auto annotate all handler setup completed")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Failed to setup auto annotate all handler: {e}")
            import traceback
            self.logger.error(traceback.format_exc())
            return False
    
    def _on_annotate_all_request(self, message: Dict) -> None:
        """
        Handle incoming auto annotate all request.
        
        Args:
            message: Raw message dictionary from RabbitMQ
        """
        try:
            self.logger.info(f"📨 Received auto annotate all request")
            
            # Parse message into typed structure
            annotate_message = self._parse_annotate_all_message(message)
            if not annotate_message:
                self.logger.error("❌ Failed to parse annotate all message")
                return
            
            self.logger.info(f"🔍 Processing auto annotation for dataset {annotate_message.dataset_id} with {len(annotate_message.config)} config(s)")
            
            # Process the auto annotation request
            self._process_annotate_all(annotate_message)
            
        except Exception as e:
            self.logger.error(f"❌ Error processing annotate all request: {e}")
            import traceback
            self.logger.error(traceback.format_exc())
    
    def _parse_annotate_all_message(self, message: Dict) -> Optional[AutoAnnotateAllMessage]:
        """
        Parse raw message into typed AutoAnnotateAllMessage.
        
        Args:
            message: Raw message dictionary
            
        Returns:
            AutoAnnotateAllMessage or None if parsing fails
        """
        try:
            # Extract main fields
            dataset_id = UUID(message['datasetId'])
            
            # Parse annotation configs with thresholds
            config_list = []
            for config_data in message.get('config', []):
                config = AutoAnnotateAllConfig(
                    class_name=config_data['className'],
                    prompt_name=config_data['promptName'],
                    threshold=float(config_data['threshold'])
                )
                config_list.append(config)
            
            # Create message
            return AutoAnnotateAllMessage(
                dataset_id=dataset_id,
                config=config_list
            )
            
        except Exception as e:
            self.logger.error(f"❌ Error parsing annotate all message: {e}")
            return None
    
    def _publish_progress(self, dataset_id: UUID, total_processed: int, total_images: int, status: str = "processing") -> None:
        """
        Publish progress update to RabbitMQ for web progress tracking.
        
        Args:
            dataset_id: Dataset ID being processed
            total_processed: Number of images processed so far
            total_images: Total number of images to process
            status: Current status (processing, completed, failed)
        """
        try:
            if not self.progress_publisher:
                return
            
            progress_data = {
                "datasetId": str(dataset_id),
                "totalProcessed": total_processed,
                "totalImages": total_images,
                "progress": round((total_processed / total_images) * 100, 2) if total_images > 0 else 0,
                "status": status,
                "timestamp": int(time.time() * 1000),  # milliseconds
                "annotatorId": self.annotator_id
            }
            
            # Use dataset ID as routing key for topic-based routing
            routing_key = f"dataset.{dataset_id}.progress"
            
            success = self.progress_publisher.publish_message(
                message=progress_data,
                exchange_name=AutoAnnotationConstants.EXCHANGE_PROGRESS,
                routing_key=routing_key
            )
            
            if success:
                self.logger.debug(f"📊 Published progress: {total_processed}/{total_images} ({progress_data['progress']}%)")
            else:
                self.logger.warning(f"⚠️ Failed to publish progress update")
                
        except Exception as e:
            self.logger.error(f"❌ Error publishing progress: {e}")
    
    def _process_annotate_all(self, message: AutoAnnotateAllMessage) -> None:
        """
        Process auto annotate all request.
        
        Args:
            message: Parsed auto annotate all message
        """
        try:
            # Step 1: Get dataset items from backend via gRPC
            self.logger.info("📋 Fetching dataset items from backend...")
            dataset_items = self.auto_annotation_client.get_dataset_items(str(message.dataset_id))
            
            if not dataset_items:
                self.logger.error("❌ No dataset items found or failed to fetch")
                return
            
            self.logger.info(f"📊 Found {len(dataset_items)} dataset items to process")
            
            # Publish initial progress (0%)
            self._publish_progress(message.dataset_id, 0, len(dataset_items))
            
            # Step 2: Process images in batches
            total_processed = 0
            total_results = 0
            result_batch = []
            
            # Process in chunks of batch_size
            for i in range(0, len(dataset_items), self.batch_size):
                batch_items = dataset_items[i:i + self.batch_size]
                
                self.logger.info(f"🔄 Processing batch {i//self.batch_size + 1}/{(len(dataset_items) + self.batch_size - 1)//self.batch_size}")
                
                # Create detection requests for this batch
                detection_requests = []
                temp_files = []  # Keep track of temp files to clean up
                
                # Download images concurrently within this batch
                item_temp_files = {}  # Map item_id -> temp_file_path
                
                def download_batch_image(item: DatasetItemResponse) -> tuple:
                    """Download a single image and create temp file for batch processing"""
                    try:
                        # Download image binary data
                        image_data = self.annotator_client.get_image(item.file_path)
                        if not image_data:
                            self.logger.warning(f"⚠️ Failed to download image: {item.file_path}")
                            return item.id, None
                        
                        # Create temporary file with proper extension
                        file_ext = os.path.splitext(item.file_path)[1] or '.jpg'
                        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=file_ext)
                        temp_file.write(image_data)
                        temp_file.close()
                        
                        return item.id, temp_file.name
                        
                    except Exception as e:
                        self.logger.error(f"❌ Error downloading batch image {item.file_path}: {e}")
                        return item.id, None
                
                # Download all images in this batch concurrently
                with ThreadPoolExecutor(max_workers=self.batch_size) as executor:
                    # Submit all download tasks for this batch
                    download_futures = {
                        executor.submit(download_batch_image, item): item 
                        for item in batch_items
                    }
                    
                    # Collect results as they complete
                    for future in as_completed(download_futures):
                        item_id, temp_file_path = future.result()
                        if temp_file_path:
                            item_temp_files[item_id] = temp_file_path
                            temp_files.append(temp_file_path)
                        else:
                            self.logger.warning(f"⚠️ Failed to download image for item {item_id}")
                
                # Create detection requests for successfully downloaded images
                for item in batch_items:
                    # Skip items that failed to download
                    if item.id not in item_temp_files:
                        continue
                    
                    temp_file_path = item_temp_files[item.id]
                    
                    # Create detection requests for each config
                    for config in message.config:
                        # Convert to AnnotationImage format
                        from ..types.AutoAnnotationTypes import AnnotationImage
                        annotation_image = AnnotationImage(
                            id=UUID(item.id),
                            image_path=temp_file_path  # Use temporary file path
                        )
                        
                        # Convert AutoAnnotateAllConfig to AnnotationConfig
                        from ..types.AutoAnnotationTypes import AnnotationConfig
                        annotation_config = AnnotationConfig(
                            class_name=config.class_name,
                            prompt_name=config.prompt_name,
                            threshold=config.threshold
                        )
                        
                        request = DetectionRequest(
                            request_id=f"{message.dataset_id}_{item.id}_{config.class_name}",
                            image=annotation_image,
                            config=annotation_config,
                            dataset_id=message.dataset_id
                        )
                        detection_requests.append(request)
                
                # Process detection requests CONCURRENTLY
                # Note: ZeroshotDetectionProcessor runs all detections in this batch 
                # in parallel using ThreadPoolExecutor - not sequential!
                if detection_requests:
                    detection_responses = self.detection_processor.process_detections(
                        requests=detection_requests,
                        callback=self._on_detection_batch_complete
                    )
                    
                    # Convert responses to gRPC format and accumulate
                    for response in detection_responses:
                        if response.success:
                            for result in response.results:
                                # Convert from (x, y, width, height) to (x1, y1, x2, y2) format as percentages
                                x1 = result.bounding_box.x
                                y1 = result.bounding_box.y
                                x2 = result.bounding_box.x + result.bounding_box.width
                                y2 = result.bounding_box.y + result.bounding_box.height
                                
                                # Ensure coordinates stay within bounds
                                x1 = max(0.0, min(1.0, x1))
                                y1 = max(0.0, min(1.0, y1))
                                x2 = max(0.0, min(1.0, x2))
                                y2 = max(0.0, min(1.0, y2))
                                
                                grpc_result = AutoAnnotationResultRequest(
                                    dataset_item_id=str(result.image_id),
                                    bboxx1=x1,
                                    bboxy1=y1,
                                    bboxx2=x2,
                                    bboxy2=y2,
                                    class_name=result.class_name
                                )
                                result_batch.append(grpc_result)
                                total_results += 1
                        else:
                            self.logger.warning(f"⚠️ Detection failed for {response.request_id}: {response.error_message}")
                
                total_processed += len(batch_items)
                
                # Send results to backend in chunks
                if len(result_batch) >= self.grpc_batch_size:
                    self._send_results_to_backend(result_batch[:self.grpc_batch_size])
                    result_batch = result_batch[self.grpc_batch_size:]
                
                # Clean up temporary files
                for temp_file in temp_files:
                    try:
                        os.unlink(temp_file)
                    except Exception as e:
                        self.logger.debug(f"Failed to cleanup temp file {temp_file}: {e}")
                
                # Publish progress update after each batch
                self._publish_progress(message.dataset_id, total_processed, len(dataset_items))
                
                self.logger.info(f"📊 Batch complete: {total_processed}/{len(dataset_items)} items processed, {total_results} results generated")
            
            # Send remaining results
            if result_batch:
                self._send_results_to_backend(result_batch)
            
            # Publish final completion progress (100%)
            self._publish_progress(message.dataset_id, total_processed, len(dataset_items))
            
            self.logger.info(f"✅ Auto annotate all completed: {total_processed} items processed, {total_results} total results")
            
        except Exception as e:
            self.logger.error(f"❌ Error in auto annotate all processing: {e}")
            import traceback
            self.logger.error(traceback.format_exc())
    
    def _send_results_to_backend(self, results: List[AutoAnnotationResultRequest]) -> None:
        """
        Send annotation results to backend via gRPC.
        
        Args:
            results: List of annotation results to send
        """
        try:
            self.logger.debug(f"📤 Sending {len(results)} results to backend...")
            
            success = self.auto_annotation_client.save_annotation_result(results)
            
            if success:
                self.logger.debug(f"✅ Successfully sent {len(results)} results to backend")
            else:
                self.logger.error(f"❌ Failed to send {len(results)} results to backend")
                
        except Exception as e:
            self.logger.error(f"❌ Error sending results to backend: {e}")
    
    def _on_detection_batch_complete(self, responses: List[DetectionResponse]) -> None:
        """
        Callback for when a batch of detections is completed.
        
        Args:
            responses: List of detection responses in the completed batch
        """
        success_count = sum(1 for r in responses if r.success)
        self.logger.debug(f"📊 Detection batch completed: {success_count}/{len(responses)} successful")
    
    def start(self) -> bool:
        """
        Start the auto annotate all handler.
        
        Returns:
            bool: True if started successfully, False otherwise
        """
        if self.is_running:
            self.logger.warning("⚠️ Auto annotate all handler already running")
            return False
        
        try:
            self.logger.info("🚀 Starting auto annotate all handler...")
            
            # Start consumer
            if not self.consumer.start():
                self.logger.error("❌ Failed to start auto annotate all consumer")
                return False
            
            self.is_running = True
            self.logger.info("✅ Auto annotate all handler started successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Failed to start auto annotate all handler: {e}")
            import traceback
            self.logger.error(traceback.format_exc())
            return False
    
    def stop(self) -> None:
        """Stop the auto annotate all handler"""
        if not self.is_running:
            return
        
        try:
            self.logger.info("🛑 Stopping auto annotate all handler...")
            
            self.is_running = False
            
            # Stop consumer
            if self.consumer:
                self.consumer.stop()
            
            # Stop progress publisher (thread-safe shutdown)
            if self.progress_publisher:
                self.progress_publisher.stop()
            
            # Cleanup detection processor if we own it
            if hasattr(self.detection_processor, 'cleanup'):
                self.detection_processor.cleanup()
            
            self.logger.info("✅ Auto annotate all handler stopped")
            
        except Exception as e:
            self.logger.error(f"❌ Error stopping auto annotate all handler: {e}")
    
    def get_processor_stats(self) -> Dict:
        """
        Get statistics from the detection processor.
        
        Returns:
            Dictionary with processor statistics
        """
        if hasattr(self.detection_processor, 'get_stats'):
            return self.detection_processor.get_stats()
        return {}
    
    def is_connected(self) -> bool:
        """Check if handler is connected and ready"""
        return (
            self.is_running and
            self.consumer is not None and
            self.consumer.is_connected()
        )