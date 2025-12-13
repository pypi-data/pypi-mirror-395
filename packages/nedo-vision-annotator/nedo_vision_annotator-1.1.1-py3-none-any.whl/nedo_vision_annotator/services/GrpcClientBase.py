"""
Base gRPC client with authentication support
"""
import grpc
import logging
from typing import Optional, Callable


# Global authentication failure callback
_auth_failure_callback: Optional[Callable] = None


def set_auth_failure_callback(callback: Callable) -> None:
    """
    Set the global authentication failure callback.
    
    Args:
        callback: Function to call when authentication fails
    """
    global _auth_failure_callback
    _auth_failure_callback = callback


def get_auth_failure_callback() -> Optional[Callable]:
    """Get the global authentication failure callback"""
    return _auth_failure_callback


class GrpcClientBase:
    """
    Base class for gRPC clients with authentication and connection management.
    """
    
    def __init__(self, server_host: str, server_port: int, token: str):
        """
        Initialize gRPC client.
        
        Args:
            server_host: Manager server host
            server_port: Manager server gRPC port
            token: Authentication token
        """
        self.server_host = server_host
        self.server_port = server_port
        self.token = token
        self.logger = logging.getLogger(__name__)
        self._channel: Optional[grpc.Channel] = None
    
    def get_server_address(self) -> str:
        """Get the full server address"""
        return f"{self.server_host}:{self.server_port}"
    
    def create_channel(self) -> grpc.Channel:
        """
        Create and return a gRPC channel.
        
        Returns:
            grpc.Channel: Configured gRPC channel
        """
        if self._channel is None:
            address = self.get_server_address()
            self.logger.debug(f"Creating gRPC channel to {address}")
            
            # For production with SSL/TLS:
            # self._channel = grpc.secure_channel(
            #     address,
            #     grpc.ssl_channel_credentials()
            # )
            
            # For development without SSL:
            self._channel = grpc.insecure_channel(address)
        
        return self._channel
    
    def close_channel(self) -> None:
        """Close the gRPC channel"""
        if self._channel:
            self._channel.close()
            self._channel = None
            self.logger.debug("gRPC channel closed")
    
    def get_metadata(self) -> list:
        """
        Get metadata for gRPC calls (includes authentication token).
        
        Returns:
            list: Metadata tuples for gRPC call
        """
        return [('token', self.token)]
    
    def handle_grpc_error(self, e: grpc.RpcError, operation: str) -> None:
        """
        Handle gRPC errors and trigger callbacks.
        
        Args:
            e: gRPC error
            operation: Name of the operation that failed
        """
        if isinstance(e, grpc.RpcError):
            status_code = e.code()
            details = e.details()
            
            self.logger.error(f"❌ gRPC error in {operation}: {status_code} - {details}")
            
            # Check for authentication failure
            if status_code == grpc.StatusCode.UNAUTHENTICATED:
                self.logger.error("🔐 Authentication failed")
                callback = get_auth_failure_callback()
                if callback:
                    callback()
            elif status_code == grpc.StatusCode.UNAVAILABLE:
                self.logger.error(f"🔌 Server unavailable at {self.get_server_address()}")
            elif status_code == grpc.StatusCode.DEADLINE_EXCEEDED:
                self.logger.error(f"⏱️ Request timeout for {operation}")
            else:
                self.logger.error(f"❌ gRPC error: {status_code}")
        else:
            self.logger.error(f"❌ Unexpected error in {operation}: {e}")
    
    def __enter__(self):
        """Context manager entry"""
        self.create_channel()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close_channel()
