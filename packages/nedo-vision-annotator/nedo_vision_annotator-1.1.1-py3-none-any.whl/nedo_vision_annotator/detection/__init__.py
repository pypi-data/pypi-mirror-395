"""
Detection module for object detection
"""
from .BaseDetector import BaseDetector
from .YOLODetector import YOLODetector
from .RFDETRDetector import RFDETRDetector, RFDETR_AVAILABLE

__all__ = ['BaseDetector', 'YOLODetector', 'RFDETRDetector', 'RFDETR_AVAILABLE']