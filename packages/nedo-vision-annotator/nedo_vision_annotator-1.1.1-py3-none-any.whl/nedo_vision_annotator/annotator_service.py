"""
Main Annotator Service class
"""
import time
import signal
import sys
import logging
from typing import Optional

from .config.ConfigurationManager import ConfigurationManager
from .services.GrpcClientBase import set_auth_failure_callback
from .initializer.AppInitializer import AppInitializer
from .annotator.AnnotatorManager import AnnotatorManager
from .annotator.AutoAnnotationManager import AutoAnnotationManager


class AnnotatorService:
    """
    Main annotator service class that manages the annotator agent lifecycle.
    Listens to RabbitMQ for dataset images, runs inference, and sends annotations back via gRPC.
    """
    
    def __init__(
        self,
        server_host: str = "be.vision.sindika.co.id",
        server_port: int = 50051,
        token: str = None,
        storage_path: str = "data",
        batch_size: int = 50,
        send_interval: int = 60,
        annotate_all_batch_size: int = 3,
        annotate_all_grpc_batch_size: int = 15
    ):
        """
        Initialize the annotator service.
        
        Args:
            server_host: Manager server host
            server_port: Manager server gRPC port
            token: Authentication token for the annotator
            storage_path: Storage path for databases and files
            batch_size: Number of annotations to batch before sending
            send_interval: Interval in seconds to send annotations
        """
        self.logger = self._setup_logging()
        self.annotator_manager = None  # Optional[AnnotatorManager] = None
        self.auto_annotation_manager = None  # Optional[AutoAnnotationManager] = None
        self.running = False
        self.server_host = server_host
        self.server_port = server_port
        self.token = token
        self.storage_path = storage_path
        self.batch_size = batch_size
        self.send_interval = send_interval
        self.config = None
        self.auth_failure_detected = False
        self.annotate_all_batch_size = annotate_all_batch_size
        self.annotate_all_grpc_batch_size = annotate_all_grpc_batch_size
        
        # Register authentication failure callback
        set_auth_failure_callback(self._on_authentication_failure)
        
        # Setup signal handlers
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)

    def _on_authentication_failure(self):
        """Called when an authentication failure is detected."""
        if not self.auth_failure_detected:
            self.auth_failure_detected = True
            self.logger.error("🔑 [APP] Authentication failure detected. Shutting down service...")
            self.stop()

    def _setup_logging(self):
        """Configure logging settings."""
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s [%(levelname)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        # Only show warnings and errors
        logging.getLogger("sqlalchemy").setLevel(logging.WARNING)
        logging.getLogger("pika").setLevel(logging.WARNING)
        logging.getLogger("grpc").setLevel(logging.FATAL)
        
        return logging.getLogger(__name__)

    def _initialize_configuration(self):
        """Initialize the application configuration."""
        self.logger.info("🚀 [APP] Initializing annotator application...")

        config_manager = ConfigurationManager(self.storage_path)
        config = config_manager.get_all_configs()
        
        server_host = self.server_host
        self.logger.info(f"🌐 [APP] Using server host: {server_host}")

        if not config:
            self.logger.info("⚙️ [APP] Configuration not found. Performing first-time setup...")

            self.logger.info(f"🌐 [APP] Using Server Host: {server_host}")

            # Check if token is provided
            if not self.token:
                raise ValueError("Token is required for annotator initialization.")

            # Store initial configuration (annotator_id will come from gRPC connection)
            config_manager.set_server_host(server_host)
            config_manager.set_server_port(self.server_port)
            config_manager.set_token(self.token)
            
            # Register with manager via gRPC and get annotator ID
            self.logger.info("📡 Registering with manager...")
            conn_info = AppInitializer.initialize_connection(
                server_host,
                self.server_port,
                self.token,
                config_manager
            )
            
            if not conn_info:
                raise RuntimeError("Failed to register with manager")
            
            self.logger.info("✅ Initial configuration saved")

            # Get configuration
            config = config_manager.get_all_configs()
        else:
            # Check if configuration needs updates
            config_updated = False
            
            if config.get('server_host') != server_host:
                config_manager.set_server_host(server_host)
                config_updated = True
                self.logger.info(f"✅ [APP] Updated server host to: {server_host}")
            
            if str(config.get('server_port')) != str(self.server_port):
                config_manager.set_server_port(self.server_port)
                config_updated = True
                self.logger.info(f"✅ [APP] Updated server port to: {self.server_port}")
            
            if self.token and config.get('token') != self.token:
                config_manager.set_token(self.token)
                config_updated = True
                self.logger.info("✅ [APP] Updated authentication token")
            
            if config_updated:
                config = config_manager.get_all_configs()
                self.logger.info("✅ [APP] Configuration updated successfully")
            else:
                self.logger.info("✅ [APP] Configuration found. No changes needed.")
            
            # Fetch connection info from manager to update RabbitMQ details and verify connection
            self.logger.info("🔄 [APP] Checking for connection info updates...")
            token_to_use = self.token if self.token else config.get('token')
            if token_to_use:
                success = AppInitializer.update_connection_info(
                    server_host,
                    self.server_port,
                    token_to_use,
                    config_manager
                )
                if success:
                    config = config_manager.get_all_configs()
                else:
                    self.logger.warning("⚠️ [APP] Failed to update connection info")
            else:
                self.logger.warning("⚠️ [APP] No token available to fetch connection info updates")
        
        # Add runtime parameters to config
        config['batch_size'] = self.batch_size
        config['send_interval'] = self.send_interval
        config['storage_path'] = self.storage_path
        config['annotate_all.batch_size'] = self.annotate_all_batch_size
        config['annotate_all.grpc_batch_size'] = self.annotate_all_grpc_batch_size
        
        self.config_manager = config_manager
        
        return config

    def initialize(self) -> bool:
        """
        Initialize the annotator service components.
        
        Returns:
            bool: True if initialization successful, False otherwise
        """
        try:
            self.logger.info("📝 [APP] Annotator service initialization started")
            
            # Initialize configuration
            self.config = self._initialize_configuration()
            
            if not self.config:
                raise RuntimeError("Failed to initialize configuration")

            # Initialize AnnotatorManager
            self.annotator_manager = AnnotatorManager(self.config)
            
            if not self.annotator_manager.initialize():
                raise RuntimeError("Failed to initialize AnnotatorManager")

            # Initialize AutoAnnotationManager
            self.auto_annotation_manager = AutoAnnotationManager(self.config)
            
            if not self.auto_annotation_manager.initialize():
                raise RuntimeError("Failed to initialize AutoAnnotationManager")

            self.logger.info("✅ [APP] Annotator service initialization completed successfully")
            return True
        except Exception as e:
            self.logger.error(f"❌ [APP] Failed to initialize annotator service: {e}")
            import traceback
            self.logger.error(traceback.format_exc())
            return False
    
    def start(self):
        """Start the annotator service"""
        if not self.running:
            self.running = True
            
            self.logger.info("=" * 80)
            self.logger.info("📝 NEDO VISION ANNOTATOR SERVICE".center(80))
            self.logger.info("=" * 80)
            
            # Initialize the service
            if not self.initialize():
                self.logger.error("❌ [APP] Failed to initialize service. Exiting...")
                sys.exit(1)
            
            # Start the annotator manager
            if self.annotator_manager:
                self.logger.info("🚀 [APP] Starting annotator manager...")
                self.annotator_manager.start()
            
            # Start the auto annotation manager
            if self.auto_annotation_manager:
                self.logger.info("🚀 [APP] Starting auto annotation manager...")
                self.auto_annotation_manager.start()
            
            self.logger.info("✅ [APP] Annotator service started successfully")
            self.logger.info("=" * 80)
            
            # Keep the service running
            try:
                while self.running:
                    time.sleep(1)
            except KeyboardInterrupt:
                self.logger.info("\n🛑 [APP] Received interrupt signal")
                self.stop()
    
    def stop(self):
        """Stop the annotator service"""
        if self.running:
            self.running = False
            self.logger.info("🛑 [APP] Stopping annotator service...")
            
            # Stop the annotator manager
            if self.annotator_manager:
                self.annotator_manager.stop()
            
            # Stop the auto annotation manager
            if self.auto_annotation_manager:
                self.auto_annotation_manager.stop()
            
            self.logger.info("✅ [APP] Annotator service stopped")
    
    def _signal_handler(self, signum, frame):
        """Handle system signals for graceful shutdown"""
        self.logger.info(f"\n🛑 [APP] Received signal {signum}")
        self.stop()
        sys.exit(0)
