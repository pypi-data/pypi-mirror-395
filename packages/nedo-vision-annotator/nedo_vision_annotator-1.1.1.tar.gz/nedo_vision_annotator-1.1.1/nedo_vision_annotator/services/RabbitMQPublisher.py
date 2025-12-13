"""
RabbitMQ publisher for sending messages - Thread-safe, long-lived connection
"""
import pika
import json
import logging
import threading
from typing import Optional, Dict, Any, Callable
from dataclasses import dataclass
from queue import Queue, Empty
from concurrent.futures import Future


@dataclass
class ExchangeConfig:
    """Configuration for RabbitMQ exchange"""
    name: str
    type: str = 'direct'
    durable: bool = True
    auto_delete: bool = False


@dataclass
class QueueConfig:
    """Configuration for RabbitMQ queue"""
    name: str
    durable: bool = True
    auto_delete: bool = False
    exclusive: bool = False


class RabbitMQPublisher(threading.Thread):
    """
    Thread-safe RabbitMQ publisher for sending messages to exchanges and queues.
    Runs in its own thread and uses add_callback_threadsafe for thread-safe publishing.
    Supports both simple publishing and request-response patterns.
    """
    
    def __init__(
        self,
        host: str,
        port: int,
        username: str,
        password: str
    ):
        """
        Initialize RabbitMQ publisher.
        
        Args:
            host: RabbitMQ server host
            port: RabbitMQ server port
            username: RabbitMQ username
            password: RabbitMQ password
        """
        super().__init__()
        self.daemon = True
        self.name = "RabbitMQPublisher"
        
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.logger = logging.getLogger(__name__)
        
        self.connection: Optional[pika.BlockingConnection] = None
        self.channel: Optional[pika.channel.Channel] = None
        
        self._is_running = False
        self._is_connected = False
        self._connect_event = threading.Event()
        self._stop_event = threading.Event()
        
        # Queue for pending operations (exchanges, queues to declare)
        self._pending_operations: Queue = Queue()
    
    def connect(self) -> bool:
        """
        Establish connection to RabbitMQ server.
        This starts the publisher thread which maintains the connection.
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if self._is_running:
                return self._is_connected
            
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
            
            self._is_connected = True
            self._is_running = True
            self._connect_event.set()
            
            # Start the publisher thread
            self.start()
            
            self.logger.info("✅ Connected to RabbitMQ for publishing (thread-safe mode)")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Failed to connect to RabbitMQ: {e}")
            self._is_connected = False
            return False
    
    def run(self):
        """
        Main thread loop - processes data events to maintain connection.
        This keeps the connection alive and processes any pending callbacks.
        """
        self.logger.debug("🔄 RabbitMQ publisher thread started")
        
        while self._is_running and not self._stop_event.is_set():
            try:
                if self.connection and self.connection.is_open:
                    # Process data events with timeout - this handles heartbeats
                    # and any callbacks scheduled via add_callback_threadsafe
                    self.connection.process_data_events(time_limit=1)
                else:
                    # Connection lost, try to reconnect
                    self._is_connected = False
                    self.logger.warning("⚠️ RabbitMQ connection lost, attempting to reconnect...")
                    self._reconnect()
                    
            except Exception as e:
                self.logger.error(f"❌ Error in publisher thread: {e}")
                self._is_connected = False
                # Brief pause before attempting reconnect
                self._stop_event.wait(timeout=5)
                if not self._stop_event.is_set():
                    self._reconnect()
        
        self.logger.debug("🛑 RabbitMQ publisher thread stopped")
    
    def _reconnect(self) -> bool:
        """
        Attempt to reconnect to RabbitMQ.
        
        Returns:
            bool: True if reconnection successful
        """
        try:
            # Close existing connection if any
            self._close_connection()
            
            # Create new connection
            credentials = pika.PlainCredentials(self.username, self.password)
            parameters = pika.ConnectionParameters(
                host=self.host,
                port=self.port,
                credentials=credentials,
                heartbeat=600,
                blocked_connection_timeout=300
            )
            
            self.connection = pika.BlockingConnection(parameters)
            self.channel = self.connection.channel()
            
            self._is_connected = True
            self.logger.info("✅ Reconnected to RabbitMQ")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Failed to reconnect to RabbitMQ: {e}")
            self._is_connected = False
            return False
    
    def _close_connection(self) -> None:
        """Close existing connection safely"""
        try:
            if self.channel and self.channel.is_open:
                self.channel.close()
        except Exception:
            pass
        
        try:
            if self.connection and self.connection.is_open:
                self.connection.close()
        except Exception:
            pass
        
        self.channel = None
        self.connection = None
    
    def disconnect(self) -> None:
        """Close connection to RabbitMQ and stop the thread"""
        self.stop()
    
    def stop(self) -> None:
        """Stop the publisher thread and close connection"""
        self.logger.info("🛑 Stopping RabbitMQ publisher...")
        
        self._is_running = False
        self._stop_event.set()
        
        # Wait for thread to finish processing
        if self.connection and self.connection.is_open:
            try:
                self.connection.process_data_events(time_limit=1)
            except Exception:
                pass
        
        self._close_connection()
        self._is_connected = False
        
        self.logger.info("🔌 Disconnected from RabbitMQ")
    
    def _declare_exchange_internal(self, exchange_config: ExchangeConfig) -> bool:
        """
        Internal method to declare exchange (called from publisher thread).
        
        Args:
            exchange_config: Exchange configuration
            
        Returns:
            bool: True if successful
        """
        try:
            if not self.channel or self.channel.is_closed:
                return False
            
            self.channel.exchange_declare(
                exchange=exchange_config.name,
                exchange_type=exchange_config.type,
                durable=exchange_config.durable,
                auto_delete=exchange_config.auto_delete
            )
            
            self.logger.debug(f"📢 Declared exchange: {exchange_config.name}")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Failed to declare exchange {exchange_config.name}: {e}")
            return False
    
    def declare_exchange(self, exchange_config: ExchangeConfig) -> bool:
        """
        Declare an exchange (thread-safe).
        
        Args:
            exchange_config: Exchange configuration
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not self._is_connected:
            return False
        
        # If called from the publisher thread, execute directly
        if threading.current_thread() == self:
            return self._declare_exchange_internal(exchange_config)
        
        # Otherwise, schedule via callback
        result_future: Future = Future()
        
        def _do_declare():
            try:
                success = self._declare_exchange_internal(exchange_config)
                result_future.set_result(success)
            except Exception as e:
                result_future.set_exception(e)
        
        try:
            self.connection.add_callback_threadsafe(_do_declare)
            return result_future.result(timeout=10)
        except Exception as e:
            self.logger.error(f"❌ Failed to declare exchange {exchange_config.name}: {e}")
            return False
    
    def _declare_queue_internal(self, queue_config: QueueConfig) -> bool:
        """
        Internal method to declare queue (called from publisher thread).
        
        Args:
            queue_config: Queue configuration
            
        Returns:
            bool: True if successful
        """
        try:
            if not self.channel or self.channel.is_closed:
                return False
            
            self.channel.queue_declare(
                queue=queue_config.name,
                durable=queue_config.durable,
                auto_delete=queue_config.auto_delete,
                exclusive=queue_config.exclusive
            )
            
            self.logger.debug(f"📝 Declared queue: {queue_config.name}")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Failed to declare queue {queue_config.name}: {e}")
            return False
    
    def declare_queue(self, queue_config: QueueConfig) -> bool:
        """
        Declare a queue (thread-safe).
        
        Args:
            queue_config: Queue configuration
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not self._is_connected:
            return False
        
        # If called from the publisher thread, execute directly
        if threading.current_thread() == self:
            return self._declare_queue_internal(queue_config)
        
        # Otherwise, schedule via callback
        result_future: Future = Future()
        
        def _do_declare():
            try:
                success = self._declare_queue_internal(queue_config)
                result_future.set_result(success)
            except Exception as e:
                result_future.set_exception(e)
        
        try:
            self.connection.add_callback_threadsafe(_do_declare)
            return result_future.result(timeout=10)
        except Exception as e:
            self.logger.error(f"❌ Failed to declare queue {queue_config.name}: {e}")
            return False
    
    def _bind_queue_internal(self, queue_name: str, exchange_name: str, routing_key: str) -> bool:
        """
        Internal method to bind queue (called from publisher thread).
        
        Args:
            queue_name: Name of the queue to bind
            exchange_name: Name of the exchange to bind to
            routing_key: Routing key for binding
            
        Returns:
            bool: True if successful
        """
        try:
            if not self.channel or self.channel.is_closed:
                return False
            
            self.channel.queue_bind(
                queue=queue_name,
                exchange=exchange_name,
                routing_key=routing_key
            )
            
            self.logger.debug(f"🔗 Bound queue '{queue_name}' to exchange '{exchange_name}' with routing key '{routing_key}'")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Failed to bind queue {queue_name} to exchange {exchange_name}: {e}")
            return False
    
    def bind_queue(self, queue_name: str, exchange_name: str, routing_key: str) -> bool:
        """
        Bind a queue to an exchange with a routing key (thread-safe).
        
        Args:
            queue_name: Name of the queue to bind
            exchange_name: Name of the exchange to bind to
            routing_key: Routing key for binding
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not self._is_connected:
            return False
        
        # If called from the publisher thread, execute directly
        if threading.current_thread() == self:
            return self._bind_queue_internal(queue_name, exchange_name, routing_key)
        
        # Otherwise, schedule via callback
        result_future: Future = Future()
        
        def _do_bind():
            try:
                success = self._bind_queue_internal(queue_name, exchange_name, routing_key)
                result_future.set_result(success)
            except Exception as e:
                result_future.set_exception(e)
        
        try:
            self.connection.add_callback_threadsafe(_do_bind)
            return result_future.result(timeout=10)
        except Exception as e:
            self.logger.error(f"❌ Failed to bind queue {queue_name} to exchange {exchange_name}: {e}")
            return False
    
    def _publish_internal(
        self,
        message_body: str,
        exchange_name: str,
        routing_key: str,
        properties: pika.BasicProperties
    ) -> bool:
        """
        Internal publish method (called from publisher thread).
        
        Args:
            message_body: Serialized message body
            exchange_name: Exchange to publish to
            routing_key: Routing key for message
            properties: Message properties
            
        Returns:
            bool: True if successful
        """
        try:
            if not self.channel or self.channel.is_closed:
                self.logger.error("❌ Channel is closed, cannot publish")
                return False
            
            self.channel.basic_publish(
                exchange=exchange_name,
                routing_key=routing_key,
                body=message_body,
                properties=properties
            )
            
            self.logger.debug(f"📤 Published message to exchange '{exchange_name}' with routing key '{routing_key}'")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Failed to publish message: {e}")
            return False
    
    def publish_message(
        self,
        message: Dict[str, Any],
        exchange_name: str,
        routing_key: str,
        properties: Optional[pika.BasicProperties] = None
    ) -> bool:
        """
        Publish a message to an exchange (thread-safe).
        Uses add_callback_threadsafe to safely publish from any thread.
        
        Args:
            message: Message dictionary to send
            exchange_name: Exchange to publish to
            routing_key: Routing key for message
            properties: Optional message properties
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not self._is_connected or not self.connection:
            self.logger.error("❌ Not connected to RabbitMQ")
            return False
        
        try:
            # Serialize message to JSON
            message_body = json.dumps(message, default=str)
            
            # Set default properties if none provided
            if properties is None:
                properties = pika.BasicProperties(
                    delivery_mode=2,  # Make message persistent
                    content_type='application/json'
                )
            
            # If called from the publisher thread, execute directly
            if threading.current_thread() == self:
                return self._publish_internal(message_body, exchange_name, routing_key, properties)
            
            # Otherwise, schedule via callback for thread safety
            result_future: Future = Future()
            
            def _do_publish():
                try:
                    success = self._publish_internal(message_body, exchange_name, routing_key, properties)
                    result_future.set_result(success)
                except Exception as e:
                    result_future.set_exception(e)
            
            self.connection.add_callback_threadsafe(_do_publish)
            
            # Wait for result with timeout
            return result_future.result(timeout=10)
            
        except Exception as e:
            self.logger.error(f"❌ Failed to publish message: {e}")
            return False
    
    def publish_message_async(
        self,
        message: Dict[str, Any],
        exchange_name: str,
        routing_key: str,
        properties: Optional[pika.BasicProperties] = None,
        callback: Optional[Callable[[bool], None]] = None
    ) -> None:
        """
        Publish a message asynchronously (fire-and-forget with optional callback).
        
        Args:
            message: Message dictionary to send
            exchange_name: Exchange to publish to
            routing_key: Routing key for message
            properties: Optional message properties
            callback: Optional callback called with success status
        """
        if not self._is_connected or not self.connection:
            self.logger.error("❌ Not connected to RabbitMQ")
            if callback:
                callback(False)
            return
        
        try:
            # Serialize message to JSON
            message_body = json.dumps(message, default=str)
            
            # Set default properties if none provided
            if properties is None:
                properties = pika.BasicProperties(
                    delivery_mode=2,
                    content_type='application/json'
                )
            
            def _do_publish():
                try:
                    success = self._publish_internal(message_body, exchange_name, routing_key, properties)
                    if callback:
                        callback(success)
                except Exception as e:
                    self.logger.error(f"❌ Async publish failed: {e}")
                    if callback:
                        callback(False)
            
            self.connection.add_callback_threadsafe(_do_publish)
            
        except Exception as e:
            self.logger.error(f"❌ Failed to schedule async publish: {e}")
            if callback:
                callback(False)
    
    def is_connected(self) -> bool:
        """Check if connected to RabbitMQ"""
        return (
            self._is_connected and
            self._is_running and
            self.connection is not None and 
            self.connection.is_open and
            self.channel is not None and
            self.channel.is_open
        )
    
    def __enter__(self):
        """Context manager entry"""
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.stop()