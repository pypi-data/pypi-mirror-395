"""
Dataset Annotation Repository
"""
import logging
from typing import List, Optional
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from ..entities.DatasetAnnotation import DatasetAnnotation
from ..session import DatabaseSession


class DatasetAnnotationRepository:
    def __init__(self, db_session: DatabaseSession = None):
        self.db_session = db_session
        self.logger = logging.getLogger(__name__)
    
    def _get_session(self) -> Session:
        return self.db_session.get_session() if self.db_session else DatabaseSession().get_session()
    
    def create(self, dataset_item_id: str, dataset_id: str, annotations: List[dict]) -> DatasetAnnotation:
        session = self._get_session()
        annotation = DatasetAnnotation(
            dataset_item_id=dataset_item_id,
            dataset_id=dataset_id,
            status='pending'
        )
        annotation.set_annotations(annotations)
        
        session.add(annotation)
        session.commit()
        session.refresh(annotation)
        
        return annotation
    
    def get_by_id(self, annotation_id: int) -> Optional[DatasetAnnotation]:
        session = self._get_session()
        return session.query(DatasetAnnotation).filter(
            DatasetAnnotation.id == annotation_id
        ).first()
    
    def get_pending(self, limit: Optional[int] = None) -> List[DatasetAnnotation]:
        session = self._get_session()
        query = session.query(DatasetAnnotation).filter(
            DatasetAnnotation.status == 'pending'
        ).order_by(DatasetAnnotation.created_at)
        
        if limit:
            query = query.limit(limit)
        
        return query.all()
    
    def count_pending(self) -> int:
        session = self._get_session()
        return session.query(DatasetAnnotation).filter(
            DatasetAnnotation.status == 'pending'
        ).count()
    
    def count_by_status(self, status: str) -> int:
        session = self._get_session()
        return session.query(DatasetAnnotation).filter(
            DatasetAnnotation.status == status
        ).count()
    
    def mark_as_sent(self, annotation_ids: List[int]) -> int:
        session = self._get_session()
        updated = session.query(DatasetAnnotation).filter(
            DatasetAnnotation.id.in_(annotation_ids)
        ).update(
            {'status': 'sent', 'sent_at': datetime.utcnow()},
            synchronize_session=False
        )
        session.commit()
        return updated
    
    def delete_by_ids(self, annotation_ids: List[int]) -> int:
        session = self._get_session()
        deleted = session.query(DatasetAnnotation).filter(
            DatasetAnnotation.id.in_(annotation_ids)
        ).delete(synchronize_session=False)
        session.commit()
        return deleted
    
    def delete_sent(self, older_than_days: int = 7) -> int:
        session = self._get_session()
        cutoff_date = datetime.utcnow() - timedelta(days=older_than_days)
        deleted = session.query(DatasetAnnotation).filter(
            DatasetAnnotation.status == 'sent',
            DatasetAnnotation.sent_at < cutoff_date
        ).delete(synchronize_session=False)
        session.commit()
        return deleted
    
    def get_all(self, limit: Optional[int] = None) -> List[DatasetAnnotation]:
        session = self._get_session()
        query = session.query(DatasetAnnotation).order_by(
            DatasetAnnotation.created_at.desc()
        )
        if limit:
            query = query.limit(limit)
        return query.all()
