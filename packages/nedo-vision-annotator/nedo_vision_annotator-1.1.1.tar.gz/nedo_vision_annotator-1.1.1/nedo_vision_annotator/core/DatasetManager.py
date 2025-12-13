"""
Dataset Manager - Handles dataset fetching and caching
"""
import logging
import threading
import time
from typing import Dict, Optional

from ..services.AnnotatorGrpcClient import AnnotatorGrpcClient


class DatasetManager:
    """
    Manages dataset information with periodic polling for updates.
    """
    
    def __init__(self, annotator_client: AnnotatorGrpcClient):
        """
        Initialize DatasetManager.
        
        Args:
            annotator_client: gRPC client for annotator operations
        """
        self.annotator_client = annotator_client
        self.logger = logging.getLogger(__name__)
        
        # Datasets cache
        self.datasets: Dict[str, Dict] = {}
        
        # Polling
        self.is_running = False
        self.poller_thread: Optional[threading.Thread] = None
    
    def fetch_datasets(self) -> None:
        """Fetch and cache datasets from manager"""
        try:
            datasets = self.annotator_client.get_dataset_list()
            
            if not datasets:
                if self.datasets:
                    self.logger.warning("⚠️ No datasets assigned to this annotator")
                    self.datasets.clear()
                return
            
            # Update datasets cache
            old_dataset_ids = set(self.datasets.keys())
            new_dataset_ids = set()
            has_changes = False
            
            for dataset in datasets:
                dataset_id = dataset['id']
                new_dataset_ids.add(dataset_id)
                
                # Check if this is a new dataset or updated
                if dataset_id not in self.datasets:
                    self.logger.info(f"➕ New dataset: {dataset['name']} (Model: {dataset.get('ai_model_name', 'None')})")
                    has_changes = True
                elif self.datasets[dataset_id].get('ai_model_id') != dataset.get('ai_model_id'):
                    self.logger.info(f"🔄 Dataset updated: {dataset['name']} (Model: {dataset.get('ai_model_name', 'None')})")
                    has_changes = True
                
                self.datasets[dataset_id] = dataset
            
            # Check for removed datasets
            removed_ids = old_dataset_ids - new_dataset_ids
            for dataset_id in removed_ids:
                dataset_name = self.datasets[dataset_id].get('name', dataset_id)
                self.logger.info(f"➖ Dataset removed: {dataset_name}")
                has_changes = True
                del self.datasets[dataset_id]
            
            if has_changes:
                self.logger.info(f"📦 Total datasets: {len(self.datasets)}")
            
        except Exception as e:
            self.logger.error(f"❌ Error fetching datasets: {e}")
    
    def get_dataset(self, dataset_id: str) -> Optional[Dict]:
        """
        Get dataset by ID.
        
        Args:
            dataset_id: Dataset ID
            
        Returns:
            Dataset dict or None if not found
        """
        return self.datasets.get(dataset_id)
    
    def get_all_datasets(self):
        """
        Get all cached datasets.
        
        Returns:
            List of dataset dicts
        """
        return list(self.datasets.values())
    
    def start_polling(self, interval: int = 60) -> None:
        """
        Start background polling for dataset updates.
        
        Args:
            interval: Polling interval in seconds (default: 60)
        """
        if self.is_running:
            self.logger.warning("⚠️ Dataset polling already running")
            return
        
        self.running = True
        self.poll_thread = threading.Thread(target=self._poller_loop, daemon=True, args=(interval,))
        self.poll_thread.start()
        # Reduce startup logging
    
    def stop_polling(self) -> None:
        """Stop background polling"""
        if not self.is_running:
            return
        
        self.is_running = False
        if self.poller_thread and self.poller_thread.is_alive():
            self.poller_thread.join(timeout=5)
        
        # Reduce shutdown logging
    
    def _poller_loop(self, interval: int) -> None:
        """Background thread that polls for dataset updates"""
        while self.is_running:
            try:
                time.sleep(interval)
                self.fetch_datasets()
            except Exception as e:
                self.logger.error(f"❌ Error in dataset poller loop: {e}")
