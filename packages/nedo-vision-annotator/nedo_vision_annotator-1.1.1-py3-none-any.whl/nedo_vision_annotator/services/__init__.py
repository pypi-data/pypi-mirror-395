"""
Service modules for gRPC and RabbitMQ communication
"""
from .GrpcClientBase import GrpcClientBase, set_auth_failure_callback, get_auth_failure_callback
from .AnnotatorGrpcClient import AnnotatorGrpcClient
from .AutoAnnotationGrpcClient import AutoAnnotationGrpcClient
from .RabbitMQConsumer import RabbitMQConsumer

__all__ = [
    'GrpcClientBase',
    'set_auth_failure_callback',
    'get_auth_failure_callback',
    'AnnotatorGrpcClient',
    'AutoAnnotationGrpcClient',
    'RabbitMQConsumer'
]

