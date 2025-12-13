"""
Status Reporter - Handles periodic status reporting to manager
"""
import logging
import threading
import time
from typing import Optional

from ..services.AnnotatorGrpcClient import AnnotatorGrpcClient
from ..services.RabbitMQConsumer import RabbitMQConsumer


class StatusReporter:
    """
    Periodically reports annotator status to manager.
    """
    
    def __init__(
        self,
        annotator_client: AnnotatorGrpcClient,
        rabbitmq_consumer: RabbitMQConsumer,
        report_interval: int = 30
    ):
        """
        Initialize StatusReporter.
        
        Args:
            annotator_client: gRPC client for annotator operations
            rabbitmq_consumer: RabbitMQ consumer for connection status
            report_interval: Interval between status reports in seconds (default: 30)
        """
        self.annotator_client = annotator_client
        self.rabbitmq_consumer = rabbitmq_consumer
        self.report_interval = report_interval
        self.logger = logging.getLogger(__name__)
        
        # Threading
        self.is_running = False
        self.reporter_thread: Optional[threading.Thread] = None
    
    def start(self) -> None:
        """Start background reporter thread"""
        if self.is_running:
            self.logger.warning("⚠️ Status reporter already running")
            return
        
        self.is_running = True
        self.reporter_thread = threading.Thread(
            target=self._reporter_loop,
            daemon=True,
            name="StatusReporter"
        )
        self.reporter_thread.start()
        # Reduce startup logging
    
    def stop(self) -> None:
        """Stop background reporter thread"""
        if not self.is_running:
            return
        
        self.is_running = False
        if self.reporter_thread and self.reporter_thread.is_alive():
            self.reporter_thread.join(timeout=5)
        
        # Reduce shutdown logging
    
    def report_status(self, status: str) -> None:
        """
        Report status immediately.
        
        Args:
            status: Status code ('connected' or 'disconnected')
        """
        try:
            self.annotator_client.update_status(status)
            self.logger.debug(f"📊 Status reported: {status}")
        except Exception as e:
            self.logger.error(f"❌ Error reporting status: {e}")
    
    def _reporter_loop(self) -> None:
        """Background thread that reports status to manager"""
        while self.is_running:
            try:
                # Report status every interval
                time.sleep(self.report_interval)
                
                # Determine status based on RabbitMQ connection
                if self.rabbitmq_consumer and self.rabbitmq_consumer.is_connected():
                    status = 'connected'
                else:
                    status = 'disconnected'
                
                # Send status update
                self.report_status(status)
                
            except Exception as e:
                self.logger.error(f"❌ Error in status reporter loop: {e}")
