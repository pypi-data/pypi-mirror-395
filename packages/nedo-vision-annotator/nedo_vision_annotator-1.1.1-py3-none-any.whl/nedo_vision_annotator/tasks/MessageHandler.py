"""
Message Handler - Handles RabbitMQ setup and message routing
"""
import logging
from typing import Dict, Callable, Optional

from ..services.RabbitMQConsumer import RabbitMQConsumer


class MessageHandler:
    """
    Manages RabbitMQ consumer setup and message routing.
    """
    
    def __init__(
        self,
        rabbitmq_host: str,
        rabbitmq_port: int,
        rabbitmq_username: str,
        rabbitmq_password: str,
        annotator_id: Optional[str],
        message_callback: Callable[[Dict], None]
    ):
        """
        Initialize MessageHandler.
        
        Args:
            rabbitmq_host: RabbitMQ host
            rabbitmq_port: RabbitMQ port
            rabbitmq_username: RabbitMQ username
            rabbitmq_password: RabbitMQ password
            annotator_id: Annotator ID for queue naming
            message_callback: Callback function for processing messages
        """
        self.rabbitmq_host = rabbitmq_host
        self.rabbitmq_port = rabbitmq_port
        self.rabbitmq_username = rabbitmq_username
        self.rabbitmq_password = rabbitmq_password
        self.annotator_id = annotator_id
        self.message_callback = message_callback
        self.logger = logging.getLogger(__name__)
        
        self.rabbitmq_consumer: Optional[RabbitMQConsumer] = None
    
    def setup(self) -> bool:
        """
        Setup RabbitMQ consumer.
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if not all([self.rabbitmq_host, self.rabbitmq_username, self.rabbitmq_password]):
                self.logger.error("❌ Missing RabbitMQ configuration")
                return False
            
            # Queue name is annotator-specific
            queue_name = f"annotator_{self.annotator_id}" if self.annotator_id else "annotator_default"
            
            # Exchange and routing key for dataset frame messages
            exchange_name = "nedo.dataset.frame.response"
            routing_key = str(self.annotator_id) if self.annotator_id else "default"
            
            self.logger.info(f"📡 Setting up RabbitMQ consumer for queue: {queue_name}")
            
            self.rabbitmq_consumer = RabbitMQConsumer(
                host=self.rabbitmq_host,
                port=self.rabbitmq_port,
                username=self.rabbitmq_username,
                password=self.rabbitmq_password,
                queue_name=queue_name,
                callback=self._on_message,
                exchange_name=exchange_name,
                routing_key=routing_key
            )
            
            return True
        except Exception as e:
            self.logger.error(f"❌ Failed to setup RabbitMQ: {e}")
            return False
    
    def _on_message(self, message: Dict) -> None:
        """
        Internal callback when RabbitMQ message is received.
        
        Args:
            message: Message dictionary
        """
        try:
            # Reduce verbosity - only log errors
            
            # Validate message (using snake_case from backend serialization)
            required_fields = ['dataset_item_id', 'file_path', 'dataset_id']
            if not all(field in message for field in required_fields):
                self.logger.error(f"❌ Invalid message format: {message}")
                return
            
            # Route to callback
            self.message_callback(message)
            
        except Exception as e:
            self.logger.error(f"❌ Error processing RabbitMQ message: {e}")
            import traceback
            self.logger.error(traceback.format_exc())
    
    def start(self) -> bool:
        """
        Start RabbitMQ consumer.
        
        Returns:
            bool: True if started successfully, False otherwise
        """
        if not self.rabbitmq_consumer:
            self.logger.error("❌ RabbitMQ consumer not setup")
            return False
        
        return self.rabbitmq_consumer.start()
    
    def stop(self) -> None:
        """Stop RabbitMQ consumer"""
        if self.rabbitmq_consumer:
            self.rabbitmq_consumer.stop()
    
    def get_consumer(self) -> Optional[RabbitMQConsumer]:
        """
        Get RabbitMQ consumer instance.
        
        Returns:
            RabbitMQConsumer instance or None
        """
        return self.rabbitmq_consumer
