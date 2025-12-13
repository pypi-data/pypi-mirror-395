"""
RabbitMQ consumer for receiving dataset image processing messages
"""
import pika
import json
import logging
import threading
import time
from typing import Optional, Callable, Dict


# Suppress pika's shutdown-related error logs (known race condition in pika with Python 3.13)
class PikaShutdownFilter(logging.Filter):
    """Filter to suppress harmless pika shutdown errors"""
    def filter(self, record):
        if record.levelno == logging.ERROR:
            # Suppress "pop from an empty deque" errors during shutdown
            if "pop from an empty deque" in str(record.getMessage()):
                return False
            # Suppress unexpected frame/connection errors during shutdown
            if "Unexpected frame" in str(record.getMessage()):
                return False
            if "connection_lost" in str(record.getMessage()):
                return False
            if "Unexpected connection close" in str(record.getMessage()):
                return False
        return True


class RabbitMQConsumer:
    """
    RabbitMQ consumer that listens for dataset image processing messages.
    Automatically reconnects on connection failure.
    """
    
    def __init__(
        self,
        host: str,
        port: int,
        username: str,
        password: str,
        queue_name: str,
        callback: Callable[[Dict], None],
        exchange_name: str = None,
        routing_key: str = None
    ):
        """
        Initialize RabbitMQ consumer.
        
        Args:
            host: RabbitMQ server host
            port: RabbitMQ server port
            username: RabbitMQ username
            password: RabbitMQ password
            queue_name: Queue name to consume from
            callback: Function to call when message received
                      Signature: callback(message_dict)
            exchange_name: Exchange name to bind to (optional)
            routing_key: Routing key for binding (optional)
        """
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.queue_name = queue_name
        self.callback = callback
        self.exchange_name = exchange_name
        self.routing_key = routing_key
        self.logger = logging.getLogger(__name__)
        
        # Apply shutdown error filter to pika loggers
        shutdown_filter = PikaShutdownFilter()
        for logger_name in ['pika.adapters.utils.io_services_utils', 'pika.adapters.base_connection', 'pika.channel']:
            pika_logger = logging.getLogger(logger_name)
            pika_logger.addFilter(shutdown_filter)
        
        self.connection: Optional[pika.BlockingConnection] = None
        self.channel: Optional[pika.channel.Channel] = None
        self.consumer_tag: Optional[str] = None
        self.is_running = False
        self.should_reconnect = False
        self.reconnect_delay = 5  # seconds
        
        # Thread for consuming messages
        self.consumer_thread: Optional[threading.Thread] = None
    
    def connect(self) -> bool:
        """
        Establish connection to RabbitMQ server.
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            self.logger.info(f"🔌 Connecting to RabbitMQ at {self.host}:{self.port}...")
            
            # Create credentials
            credentials = pika.PlainCredentials(self.username, self.password)
            
            # Create connection parameters
            parameters = pika.ConnectionParameters(
                host=self.host,
                port=self.port,
                credentials=credentials,
                heartbeat=600,  # 10 minutes
                blocked_connection_timeout=300  # 5 minutes
            )
            
            # Establish connection
            self.connection = pika.BlockingConnection(parameters)
            self.channel = self.connection.channel()
            
            # Declare exchange if provided
            if self.exchange_name:
                self.channel.exchange_declare(
                    exchange=self.exchange_name,
                    exchange_type='direct',
                    durable=True
                )
            
            # Declare queue (idempotent)
            self.channel.queue_declare(queue=self.queue_name, durable=True)
            
            # Bind queue to exchange if both are provided
            if self.exchange_name and self.routing_key:
                self.channel.queue_bind(
                    queue=self.queue_name,
                    exchange=self.exchange_name,
                    routing_key=self.routing_key
                )
                self.logger.info(f"🔗 Bound queue '{self.queue_name}' to exchange '{self.exchange_name}' with routing key '{self.routing_key}'")
            
            # Set QoS to process one message at a time
            self.channel.basic_qos(prefetch_count=1)
            
            self.logger.info(f"✅ Connected to RabbitMQ, listening on queue: {self.queue_name}")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Failed to connect to RabbitMQ: {e}")
            return False
    
    def disconnect(self) -> None:
        """Close connection to RabbitMQ"""
        try:
            if self.channel and not self.channel.is_closed:
                # Cancel consumer first to prevent race condition
                try:
                    self.channel.cancel()
                except Exception:
                    pass  # Ignore cancel errors during shutdown
                
                try:
                    self.channel.close()
                except Exception:
                    pass  # Ignore close errors during shutdown
                    
            if self.connection and not self.connection.is_closed:
                try:
                    self.connection.close()
                except Exception:
                    pass  # Ignore close errors during shutdown
                    
            self.logger.info("🔌 Disconnected from RabbitMQ")
        except Exception as e:
            # Log but don't raise - this is expected during shutdown
            self.logger.debug(f"Disconnect cleanup: {e}")
    
    def _on_message(self, channel, method, properties, body):
        """
        Callback when message is received from RabbitMQ.
        
        Args:
            channel: Channel object
            method: Method frame
            properties: Properties
            body: Message body (bytes)
        """
        try:
            # Parse JSON message
            message_str = body.decode('utf-8')
            message = json.loads(message_str)
            
            self.logger.debug(f"📨 Received message: {message}")
            
            # Call user callback
            self.callback(message)
            
            # Acknowledge message
            channel.basic_ack(delivery_tag=method.delivery_tag)
            self.logger.debug(f"✅ Message acknowledged")
            
        except json.JSONDecodeError as e:
            self.logger.error(f"❌ Failed to parse message JSON: {e}")
            # Reject message and don't requeue (invalid format)
            channel.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
        except Exception as e:
            self.logger.error(f"❌ Error processing message: {e}")
            # Reject message and requeue for retry
            channel.basic_nack(delivery_tag=method.delivery_tag, requeue=True)
    
    def _consume_loop(self) -> None:
        """Main consume loop that runs in a separate thread"""
        while self.is_running:
            try:
                if not self.connection or self.connection.is_closed:
                    self.logger.info("🔄 Connection lost, reconnecting...")
                    if not self.connect():
                        self.logger.error(f"❌ Reconnection failed, retrying in {self.reconnect_delay}s...")
                        time.sleep(self.reconnect_delay)
                        continue
                
                # Start consuming
                self.logger.info("👂 Starting to consume messages...")
                self.consumer_tag = self.channel.basic_consume(
                    queue=self.queue_name,
                    on_message_callback=self._on_message,
                    auto_ack=False
                )
                
                # Process messages (blocking)
                self.channel.start_consuming()
                
            except pika.exceptions.AMQPConnectionError as e:
                self.logger.error(f"❌ AMQP Connection error: {e}")
                if self.is_running:
                    self.logger.info(f"🔄 Reconnecting in {self.reconnect_delay}s...")
                    time.sleep(self.reconnect_delay)
            except pika.exceptions.ChannelClosedByBroker as e:
                self.logger.error(f"❌ Channel closed by broker: {e}")
                if self.is_running:
                    self.logger.info(f"🔄 Reconnecting in {self.reconnect_delay}s...")
                    time.sleep(self.reconnect_delay)
            except Exception as e:
                self.logger.error(f"❌ Unexpected error in consume loop: {e}")
                if self.is_running:
                    self.logger.info(f"🔄 Reconnecting in {self.reconnect_delay}s...")
                    time.sleep(self.reconnect_delay)
    
    def start(self) -> bool:
        """
        Start consuming messages in a separate thread.
        
        Returns:
            bool: True if started successfully, False otherwise
        """
        if self.is_running:
            self.logger.warning("⚠️ Consumer already running")
            return False
        
        # Connect first
        if not self.connect():
            return False
        
        self.is_running = True
        
        # Start consumer thread
        self.consumer_thread = threading.Thread(
            target=self._consume_loop,
            daemon=True,
            name="RabbitMQConsumer"
        )
        self.consumer_thread.start()
        
        self.logger.info("✅ RabbitMQ consumer started")
        return True
    
    def stop(self) -> None:
        """Stop consuming messages and close connection"""
        if not self.is_running:
            return
        
        self.logger.info("🛑 Stopping RabbitMQ consumer...")
        self.is_running = False
        
        try:
            # Stop consuming first (this will cause the consumer loop to exit)
            if self.channel and not self.channel.is_closed:
                try:
                    self.channel.stop_consuming()
                except Exception as e:
                    self.logger.debug(f"stop_consuming() error (expected during shutdown): {e}")
            
            # Wait for thread to finish consuming
            if self.consumer_thread and self.consumer_thread.is_alive():
                self.consumer_thread.join(timeout=5)
            
            # Now disconnect (after consumer loop has exited)
            self.disconnect()
            
            self.logger.info("✅ RabbitMQ consumer stopped")
        except Exception as e:
            self.logger.error(f"❌ Error stopping consumer: {e}")
    
    def is_connected(self) -> bool:
        """Check if connected to RabbitMQ"""
        return (
            self.connection is not None and 
            not self.connection.is_closed and
            self.channel is not None and
            not self.channel.is_closed
        )
