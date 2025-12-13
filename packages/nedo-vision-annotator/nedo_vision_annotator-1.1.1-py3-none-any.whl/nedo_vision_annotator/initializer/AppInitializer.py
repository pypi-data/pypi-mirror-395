"""
Application initializer for annotator service
"""
import logging
from typing import Optional, Dict
from ..services.AnnotatorGrpcClient import AnnotatorGrpcClient
from ..config.ConfigurationManager import ConfigurationManager


class AppInitializer:
    """
    Handles initial connection setup and configuration with the manager.
    """
    
    @staticmethod
    def initialize_connection(
        server_host: str,
        server_port: int,
        token: str,
        config_manager: ConfigurationManager
    ) -> Optional[Dict]:
        """
        Initialize connection with manager and fetch configuration.
        
        Args:
            server_host: Manager server host
            server_port: Manager server gRPC port
            token: Authentication token
            config_manager: Configuration manager instance
            
        Returns:
            dict: Connection info including annotator_id and RabbitMQ details, or None if failed
        """
        logger = logging.getLogger(__name__)
        
        try:
            logger.info("🔌 Initializing connection with manager...")
            
            # Create gRPC client
            client = AnnotatorGrpcClient(server_host, server_port, token)
            
            # Fetch connection info
            conn_info = client.get_connection_info()
            
            if not conn_info:
                logger.error("❌ Failed to get connection info from manager")
                return None
            
            # Store annotator ID if provided
            if conn_info.get('annotator_id'):
                config_manager.set_annotator_id(conn_info['annotator_id'])
                logger.info(f"✅ Annotator ID: {conn_info['annotator_id']}")
            else:
                logger.warning("⚠️ No annotator ID received from manager")
            
            # Store RabbitMQ connection details
            config_manager.set_config('rabbitmq_host', conn_info['rabbitmq_host'])
            config_manager.set_config('rabbitmq_port', str(conn_info['rabbitmq_port']))
            config_manager.set_config('rabbitmq_username', conn_info['rabbitmq_username'])
            config_manager.set_config('rabbitmq_password', conn_info['rabbitmq_password'])
            
            logger.info(f"✅ RabbitMQ: {conn_info['rabbitmq_host']}:{conn_info['rabbitmq_port']}")
            logger.info("✅ Connection initialized successfully")
            
            # Close the client
            client.close_channel()
            
            return conn_info
            
        except Exception as e:
            logger.error(f"❌ Failed to initialize connection: {e}")
            import traceback
            logger.error(traceback.format_exc())
            return None
    
    @staticmethod
    def update_connection_info(
        server_host: str,
        server_port: int,
        token: str,
        config_manager: ConfigurationManager
    ) -> bool:
        """
        Update connection information from manager.
        
        Args:
            server_host: Manager server host
            server_port: Manager server gRPC port
            token: Authentication token
            config_manager: Configuration manager instance
            
        Returns:
            bool: True if successful, False otherwise
        """
        logger = logging.getLogger(__name__)
        
        try:
            logger.info("🔄 Updating connection info...")
            
            conn_info = AppInitializer.initialize_connection(
                server_host,
                server_port,
                token,
                config_manager
            )
            
            return conn_info is not None
            
        except Exception as e:
            logger.error(f"❌ Failed to update connection info: {e}")
            return False
