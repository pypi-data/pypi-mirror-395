"""
Test Auto Annotation Handler - Handles test auto-annotation requests and responses
"""
import logging
import os
import tempfile
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Optional, Dict, List
from uuid import UUID

from ..services.RabbitMQConsumer import RabbitMQConsumer
from ..services.RabbitMQPublisher import RabbitMQPublisher, ExchangeConfig
from ..services.AnnotatorGrpcClient import AnnotatorGrpcClient
from ..types.AutoAnnotationTypes import (
    TestAutoAnnotationMessage,
    TestAnnotationRequest,
    AnnotationConfig,
    AnnotationImage,
    AutoAnnotationResult,
    AutoAnnotationConstants
)
from .ZeroshotDetectionProcessor import (
    DetectionProcessor, 
    DetectionRequest,
    DetectionResponse
)


class TestAutoAnnotationHandler:
    """
    Handles test auto-annotation requests from the manager service.
    Listens for test requests, processes them, and sends back results.
    """
    
    def __init__(
        self,
        rabbitmq_host: str,
        rabbitmq_port: int,
        rabbitmq_username: str,
        rabbitmq_password: str,
        annotator_id: str,
        annotator_client: AnnotatorGrpcClient,
        detection_processor: DetectionProcessor 
    ):
        """
        Initialize TestAutoAnnotationHandler.
        
        Args:
            rabbitmq_host: RabbitMQ host
            rabbitmq_port: RabbitMQ port
            rabbitmq_username: RabbitMQ username
            rabbitmq_password: RabbitMQ password
            annotator_id: Annotator ID for routing
            annotator_client: gRPC client for annotator operations
            detection_processor: Optional detection processor for dependency injection
        """
        self.rabbitmq_host = rabbitmq_host
        self.rabbitmq_port = rabbitmq_port
        self.rabbitmq_username = rabbitmq_username
        self.rabbitmq_password = rabbitmq_password
        self.annotator_id = annotator_id
        self.annotator_client = annotator_client
        self.logger = logging.getLogger(__name__)
        
        # Dependency injection for detection processor
        self.detection_processor = detection_processor
        
        self.is_running = False
        self.consumer: Optional[RabbitMQConsumer] = None
        self.publisher: Optional[RabbitMQPublisher] = None
    
    def setup(self) -> bool:
        """
        Setup RabbitMQ consumer and publisher for test auto-annotation.
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if not all([self.rabbitmq_host, self.rabbitmq_username, self.rabbitmq_password]):
                self.logger.error("❌ Missing RabbitMQ configuration")
                return False
            
            # Setup publisher for sending responses
            self.publisher = RabbitMQPublisher(
                host=self.rabbitmq_host,
                port=self.rabbitmq_port,
                username=self.rabbitmq_username,
                password=self.rabbitmq_password
            )
            
            # Connect publisher and declare response exchange
            if not self.publisher.connect():
                return False
            
            response_exchange = ExchangeConfig(
                name=AutoAnnotationConstants.EXCHANGE_TEST_RESPONSE,
                type=AutoAnnotationConstants.EXCHANGE_TYPE_DIRECT,
                durable=True,
                auto_delete=False
            )
            
            if not self.publisher.declare_exchange(response_exchange):
                return False
            
            # Setup consumer for test requests
            # Use annotator ID as routing key
            routing_key = str(self.annotator_id) if self.annotator_id else "default"
            
            self.logger.info(f"📡 Setting up test auto-annotation consumer with routing key: {routing_key}")
            
            self.consumer = RabbitMQConsumer(
                host=self.rabbitmq_host,
                port=self.rabbitmq_port,
                username=self.rabbitmq_username,
                password=self.rabbitmq_password,
                queue_name=f"test_auto_annotation_{self.annotator_id}",
                callback=self._on_test_request,
                exchange_name=AutoAnnotationConstants.EXCHANGE_TEST_REQUEST,
                routing_key=routing_key
            )
            
            self.logger.info("✅ Test auto-annotation handler setup completed")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Failed to setup test auto-annotation handler: {e}")
            import traceback
            self.logger.error(traceback.format_exc())
            return False
    
    def _on_test_request(self, message: Dict) -> None:
        """
        Handle incoming test auto-annotation request.
        
        Args:
            message: Raw message dictionary from RabbitMQ
        """
        try:
            self.logger.info(f"📨 Received test auto-annotation request")
            
            # Parse message into typed structure
            test_message = self._parse_test_message(message)
            if not test_message:
                self.logger.error("❌ Failed to parse test message")
                return
            
            self.logger.info(f"🔍 Processing test annotation for dataset {test_message.dataset_id} with {len(test_message.annotations.images)} image(s)")
            # Close gRPC clients
            
            # Process the test annotation request
            results = self._process_test_annotation(test_message)
            
            # Send response back to manager
            self._send_test_response(test_message.request_id, results)
            
        except Exception as e:
            self.logger.error(f"❌ Error processing test request: {e}")
            import traceback
            self.logger.error(traceback.format_exc())
    
    def _parse_test_message(self, message: Dict) -> Optional[TestAutoAnnotationMessage]:
        """
        Parse raw message into typed TestAutoAnnotationMessage.
        
        Args:
            message: Raw message dictionary
            
        Returns:
            TestAutoAnnotationMessage or None if parsing fails
        """
        try:
            # Extract main fields
            dataset_id = UUID(message['datasetId'])
            request_id = UUID(message['requestId'])
            annotations_data = message['annotations']
            
            # Parse annotation configs (no threshold in test mode - use default lowest value)
            config_list = []
            for config_data in annotations_data.get('config', []):
                config = AnnotationConfig(
                    class_name=config_data['className'],
                    prompt_name=config_data['promptName']
                    # threshold uses default 0.01 from dataclass
                )
                config_list.append(config)
            
            # Parse annotation images
            image_list = []
            for image_data in annotations_data.get('images', []):
                image = AnnotationImage(
                    id=UUID(image_data['id']),
                    image_path=image_data['imagePath']
                )
                image_list.append(image)
            
            # Create test annotation request
            test_request = TestAnnotationRequest(
                config=config_list,
                images=image_list
            )
            
            # Create full message
            return TestAutoAnnotationMessage(
                dataset_id=dataset_id,
                request_id=request_id,
                annotations=test_request
            )
            
        except Exception as e:
            self.logger.error(f"❌ Error parsing test message: {e}")
            return None
    
    def _process_test_annotation(self, message: TestAutoAnnotationMessage) -> List[AutoAnnotationResult]:
        """
        Process test annotation request and generate results using detection processor.
        
        Args:
            message: Parsed test annotation message
            
        Returns:
            List of annotation results
        """
        self.logger.info("🔄 Processing test annotation using zero-shot detection")
        
        try:
            # Check if processor is ready
            if not self.detection_processor.is_ready():
                self.logger.error("❌ Detection processor is not ready")
                return []
            
            # Step 1: Download all images concurrently (max 4 images, safe to download all at once)
            self.logger.info(f"📥 Downloading {len(message.annotations.images)} image(s) concurrently...")
            
            image_temp_files = {}  # Map image_id -> temp_file_path
            temp_files_to_cleanup = []
            
            def download_image(image: AnnotationImage) -> tuple:
                """Download a single image and create temp file"""
                try:
                    # Download image binary data
                    image_data = self.annotator_client.get_image(image.image_path)
                    if not image_data:
                        self.logger.warning(f"⚠️ Failed to download image: {image.image_path}")
                        return image.id, None
                    
                    # Create temporary file with proper extension
                    file_ext = os.path.splitext(image.image_path)[1] or '.jpg'
                    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=file_ext)
                    temp_file.write(image_data)
                    temp_file.close()
                    
                    return image.id, temp_file.name
                    
                except Exception as e:
                    self.logger.error(f"❌ Error downloading image {image.image_path}: {e}")
                    return image.id, None
            
            # Download all images concurrently using ThreadPoolExecutor
            with ThreadPoolExecutor(max_workers=4) as executor:
                # Submit all download tasks
                download_futures = {
                    executor.submit(download_image, image): image 
                    for image in message.annotations.images
                }
                
                # Collect results as they complete
                for future in as_completed(download_futures):
                    image_id, temp_file_path = future.result()
                    if temp_file_path:
                        image_temp_files[image_id] = temp_file_path
                        temp_files_to_cleanup.append(temp_file_path)
                    else:
                        self.logger.warning(f"⚠️ Failed to download image {image_id}")
            
            self.logger.info(f"✅ Downloaded {len(image_temp_files)}/{len(message.annotations.images)} image(s)")
            
            if not image_temp_files:
                self.logger.error("❌ No images downloaded successfully")
                return []
            
            # Step 2: Create detection requests for each image-config combination
            detection_requests = []
            for image in message.annotations.images:
                # Skip images that failed to download
                if image.id not in image_temp_files:
                    continue
                    
                # Create updated AnnotationImage with temp file path
                temp_image = AnnotationImage(
                    id=image.id,
                    image_path=image_temp_files[image.id]
                )
                
                for config in message.annotations.config:
                    request = DetectionRequest(
                        request_id=f"{message.request_id}_{image.id}_{config.class_name}",
                        image=temp_image,
                        config=config,
                        dataset_id=message.dataset_id
                    )
                    detection_requests.append(request)
            
            self.logger.info(f"🔍 Processing {len(detection_requests)} detection requests")
            
            # Step 3: Process all detection requests
            detection_responses = self.detection_processor.process_detections(
                requests=detection_requests,
                callback=self._on_batch_complete
            )
            
            # Step 4: Collect all results
            all_results = []
            for response in detection_responses:
                if response.success:
                    all_results.extend(response.results)
                else:
                    self.logger.warning(f"Detection failed for request {response.request_id}: {response.error_message}")
            
            # Step 5: Cleanup temporary files
            for temp_file in temp_files_to_cleanup:
                try:
                    os.unlink(temp_file)
                except Exception as e:
                    self.logger.debug(f"Failed to cleanup temp file {temp_file}: {e}")
            
            self.logger.info(f"✅ Generated {len(all_results)} detection result(s)")
            return all_results
            
        except Exception as e:
            self.logger.error(f"❌ Error in test annotation processing: {e}")
            import traceback
            self.logger.error(traceback.format_exc())
            return []
    
    def _on_batch_complete(self, responses: List[DetectionResponse]) -> None:
        """
        Callback for when a batch of detections is completed.
        
        Args:
            responses: List of detection responses in the completed batch
        """
        success_count = sum(1 for r in responses if r.success)
        self.logger.debug(f"📊 Batch completed: {success_count}/{len(responses)} successful")
    
    def _send_test_response(self, request_id: UUID, results: List[AutoAnnotationResult]) -> None:
        """
        Send test annotation results back to the manager.
        
        Args:
            request_id: Request ID for response routing
            results: List of annotation results
        """
        try:
            # Convert results to dictionary format
            results_data = []
            for result in results:
                # Ensure coordinates are within bounds [0, 1]
                x1 = max(0.0, min(1.0, result.bounding_box.x))
                y1 = max(0.0, min(1.0, result.bounding_box.y))
                x2 = max(0.0, min(1.0, result.bounding_box.x + result.bounding_box.width))
                y2 = max(0.0, min(1.0, result.bounding_box.y + result.bounding_box.height))
                
                result_dict = {
                    'classname': result.class_name,
                    'confidence': result.confidence,
                    'x1': x1,
                    'y1': y1,
                    'x2': x2,
                    'y2': y2,
                    'imageId': str(result.image_id)
                }
                results_data.append(result_dict)
            
            # Send response using request ID as routing key
            routing_key = str(request_id)
            
            success = self.publisher.publish_message(
                message=results_data,
                exchange_name=AutoAnnotationConstants.EXCHANGE_TEST_RESPONSE,
                routing_key=routing_key
            )
            
            if success:
                self.logger.info(f"📤 Sent test annotation response for request {request_id}")
            else:
                self.logger.error(f"❌ Failed to send test annotation response for request {request_id}")
                
        except Exception as e:
            self.logger.error(f"❌ Error sending test response: {e}")
            import traceback
            self.logger.error(traceback.format_exc())
    
    def start(self) -> bool:
        """
        Start the test auto-annotation handler.
        
        Returns:
            bool: True if started successfully, False otherwise
        """
        if self.is_running:
            self.logger.warning("⚠️ Test auto-annotation handler already running")
            return False
        
        try:
            self.logger.info("🚀 Starting test auto-annotation handler...")
            
            # Start consumer
            if not self.consumer.start():
                self.logger.error("❌ Failed to start test auto-annotation consumer")
                return False
            
            self.is_running = True
            self.logger.info("✅ Test auto-annotation handler started successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Failed to start test auto-annotation handler: {e}")
            import traceback
            self.logger.error(traceback.format_exc())
            return False
    
    def stop(self) -> None:
        """Stop the test auto-annotation handler"""
        if not self.is_running:
            return
        
        try:
            self.logger.info("🛑 Stopping test auto-annotation handler...")
            
            self.is_running = False
            
            # Stop consumer
            if self.consumer:
                self.consumer.stop()
            
            # Stop publisher (thread-safe shutdown)
            if self.publisher:
                self.publisher.stop()
            
            # Cleanup detection processor if we own it
            if hasattr(self.detection_processor, 'cleanup'):
                self.detection_processor.cleanup()
            
            self.logger.info("✅ Test auto-annotation handler stopped")
            
        except Exception as e:
            self.logger.error(f"❌ Error stopping test auto-annotation handler: {e}")
    
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
            self.consumer.is_connected() and
            self.publisher is not None and
            self.publisher.is_connected()
        )