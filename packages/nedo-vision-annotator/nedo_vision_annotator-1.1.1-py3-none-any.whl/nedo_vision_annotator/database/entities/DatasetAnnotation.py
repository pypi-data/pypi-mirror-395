from sqlalchemy import Column, String, Integer, DateTime, Text
from sqlalchemy.sql import func
import json

from ..base import Base


class DatasetAnnotation(Base):
    __tablename__ = "dataset_annotations"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    dataset_item_id = Column(String(36), nullable=False, index=True)
    dataset_id = Column(String(36), nullable=False, index=True)
    annotations = Column(Text, nullable=False)
    status = Column(String(20), default='pending', index=True)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    sent_at = Column(DateTime, nullable=True)
    
    def get_annotations(self):
        return json.loads(self.annotations) if self.annotations else []
    
    def set_annotations(self, annotations_list):
        self.annotations = json.dumps(annotations_list)
    
    def to_dict(self):
        return {
            'id': self.id,
            'dataset_item_id': self.dataset_item_id,
            'dataset_id': self.dataset_id,
            'annotations': self.get_annotations(),
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'sent_at': self.sent_at.isoformat() if self.sent_at else None
        }
    
    def __repr__(self):
        return f"<DatasetAnnotation(id={self.id}, dataset_item_id={self.dataset_item_id}, dataset_id={self.dataset_id}, status={self.status})>"
