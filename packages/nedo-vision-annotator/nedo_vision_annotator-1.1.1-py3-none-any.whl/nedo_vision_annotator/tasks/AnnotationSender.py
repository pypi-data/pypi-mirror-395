"""
Annotation Sender - Handles batch sending of annotations to manager
"""
import logging
import threading
import time
from typing import Optional

from ..services.AnnotatorGrpcClient import AnnotatorGrpcClient
from ..database import DatabaseSession, DatasetAnnotationRepository


class AnnotationSender:
    def __init__(
        self,
        annotator_client: AnnotatorGrpcClient,
        db_session: DatabaseSession,
        batch_size: int,
        send_interval: int
    ):
        self.annotator_client = annotator_client
        self.db_session = db_session
        self.batch_size = batch_size
        self.send_interval = send_interval
        self.logger = logging.getLogger(__name__)
        
        self.is_running = False
        self.sender_thread: Optional[threading.Thread] = None
    
    def start(self) -> None:
        """Start background sender thread"""
        if self.is_running:
            self.logger.warning("⚠️ Annotation sender already running")
            return
        
        self.is_running = True
        self.sender_thread = threading.Thread(
            target=self._sender_loop,
            daemon=True,
            name="AnnotationSender"
        )
        self.sender_thread.start()
        # Reduce startup logging
    
    def stop(self) -> None:
        """Stop background sender thread"""
        if not self.is_running:
            return
        
        self.is_running = False
        if self.sender_thread and self.sender_thread.is_alive():
            self.sender_thread.join(timeout=5)
        
        # Reduce shutdown logging
    
    def _sender_loop(self) -> None:
        while self.is_running:
            try:
                time.sleep(self.send_interval)
                
                repo = DatasetAnnotationRepository(self.db_session)
                pending = repo.get_pending(limit=self.batch_size)
                
                if not pending:
                    self.logger.debug("No pending annotations to send")
                    continue
                
                grouped = {}
                for ann_obj in pending:
                    ann = ann_obj.to_dict()
                    item_id = ann['dataset_item_id']
                    if item_id not in grouped:
                        grouped[item_id] = {
                            'dataset_item_id': item_id,
                            'annotations': [],
                            'ids': []
                        }
                    grouped[item_id]['annotations'].extend(ann['annotations'])
                    grouped[item_id]['ids'].append(ann['id'])
                
                items_to_send = [{
                    'dataset_item_id': v['dataset_item_id'],
                    'annotations': v['annotations']
                } for v in grouped.values()]
                
                all_ann_ids = [id for v in grouped.values() for id in v['ids']]
                
                try:
                    result = self.annotator_client.send_annotations(items_to_send)
                    
                    if result and result['success']:
                        repo.delete_by_ids(all_ann_ids)
                        self.logger.info(
                            f"✅ Batch sent: "
                            f"{result['items_processed']} items, "
                            f"{result['annotations_created']} annotations created"
                        )
                    else:
                        self.logger.error(f"❌ Failed to send batch: {result['message'] if result else 'Unknown error'}")
                
                except Exception as e:
                    self.logger.error(f"❌ Error sending batch: {e}")
                
            except Exception as e:
                self.logger.error(f"❌ Error in annotation sender loop: {e}")
