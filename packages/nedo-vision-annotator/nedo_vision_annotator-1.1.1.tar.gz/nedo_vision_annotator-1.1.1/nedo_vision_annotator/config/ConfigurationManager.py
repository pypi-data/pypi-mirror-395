"""
Configuration management for the annotator service
"""
import os
import sqlite3
import logging
from typing import Optional, Dict, Any


logger = logging.getLogger(__name__)


class ConfigurationManager:
    """Manages annotator configuration using SQLite database"""
    
    def __init__(self, storage_path: str):
        """
        Initialize configuration manager.
        
        Args:
            storage_path: Directory path for storing configuration database
        """
        self.storage_path = storage_path
        self.db_path = os.path.join(storage_path, 'config.db')
        self._initialize_database()
    
    def _initialize_database(self) -> None:
        """Initialize the configuration database and create tables if needed"""
        try:
            # Create storage directory if it doesn't exist
            os.makedirs(self.storage_path, exist_ok=True)
            
            # Create database and table
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS configuration (
                    key TEXT PRIMARY KEY,
                    value TEXT NOT NULL,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            conn.commit()
            conn.close()
            
            logger.info(f"📁 Configuration database initialized at: {self.db_path}")
        except Exception as e:
            logger.error(f"❌ Failed to initialize configuration database: {e}")
            raise
    
    def get_config(self, key: str) -> Optional[str]:
        """
        Get configuration value by key.
        
        Args:
            key: Configuration key
            
        Returns:
            str: Configuration value or None if not found
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('SELECT value FROM configuration WHERE key = ?', (key,))
            result = cursor.fetchone()
            
            conn.close()
            
            return result[0] if result else None
        except Exception as e:
            logger.error(f"❌ Failed to get config '{key}': {e}")
            return None
    
    def set_config(self, key: str, value: str) -> bool:
        """
        Set configuration value.
        
        Args:
            key: Configuration key
            value: Configuration value
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT OR REPLACE INTO configuration (key, value, updated_at)
                VALUES (?, ?, CURRENT_TIMESTAMP)
            ''', (key, value))
            
            conn.commit()
            conn.close()
            
            logger.debug(f"✅ Config set: {key} = {value[:50]}..." if len(value) > 50 else f"✅ Config set: {key} = {value}")
            return True
        except Exception as e:
            logger.error(f"❌ Failed to set config '{key}': {e}")
            return False
    
    def get_all_configs(self) -> Dict[str, str]:
        """
        Get all configuration key-value pairs.
        
        Returns:
            dict: Dictionary of all configurations
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('SELECT key, value FROM configuration')
            results = cursor.fetchall()
            
            conn.close()
            
            return {key: value for key, value in results}
        except Exception as e:
            logger.error(f"❌ Failed to get all configs: {e}")
            return {}
    
    def delete_config(self, key: str) -> bool:
        """
        Delete configuration by key.
        
        Args:
            key: Configuration key to delete
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('DELETE FROM configuration WHERE key = ?', (key,))
            
            conn.commit()
            conn.close()
            
            logger.debug(f"🗑️ Config deleted: {key}")
            return True
        except Exception as e:
            logger.error(f"❌ Failed to delete config '{key}': {e}")
            return False
    
    def config_exists(self, key: str) -> bool:
        """
        Check if configuration key exists.
        
        Args:
            key: Configuration key
            
        Returns:
            bool: True if exists, False otherwise
        """
        return self.get_config(key) is not None
    
    # Convenience methods for common configuration keys
    
    def get_server_host(self) -> Optional[str]:
        """Get server host from configuration"""
        return self.get_config('server_host')
    
    def set_server_host(self, host: str) -> bool:
        """Set server host in configuration"""
        return self.set_config('server_host', host)
    
    def get_server_port(self) -> Optional[int]:
        """Get server port from configuration"""
        port = self.get_config('server_port')
        return int(port) if port else None
    
    def set_server_port(self, port: int) -> bool:
        """Set server port in configuration"""
        return self.set_config('server_port', str(port))
    
    def get_token(self) -> Optional[str]:
        """Get authentication token from configuration"""
        return self.get_config('token')
    
    def set_token(self, token: str) -> bool:
        """Set authentication token in configuration"""
        return self.set_config('token', token)
    
    def get_annotator_id(self) -> Optional[str]:
        """Get annotator ID from configuration"""
        return self.get_config('annotator_id')
    
    def set_annotator_id(self, annotator_id: str) -> bool:
        """Set annotator ID in configuration"""
        return self.set_config('annotator_id', annotator_id)
