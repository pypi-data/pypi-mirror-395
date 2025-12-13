"""
gRPC client for AnnotatorService
"""
import grpc
import logging
from typing import Optional, List, Dict
from .GrpcClientBase import GrpcClientBase
from . import AnnotatorService_pb2
from . import AnnotatorService_pb2_grpc


class AnnotatorGrpcClient(GrpcClientBase):
    """Client for AnnotatorService gRPC communication"""
    
    def __init__(self, server_host: str, server_port: int, token: str):
        super().__init__(server_host, server_port, token)
        self.logger = logging.getLogger(__name__)
    
    def get_connection_info(self) -> Optional[Dict]:
        """
        Get connection information including RabbitMQ details and annotator ID.
        
        Returns:
            dict: Connection info or None if failed
                {
                    'annotator_id': str,
                    'rabbitmq_host': str,
                    'rabbitmq_port': int,
                    'rabbitmq_username': str,
                    'rabbitmq_password': str
                }
        """
        try:
            channel = self.create_channel()
            stub = AnnotatorService_pb2_grpc.AnnotatorServiceStub(channel)
            
            request = AnnotatorService_pb2.GetAnnotatorConnectionInfoRequest(
                token=self.token
            )
            
            self.logger.info("📡 Fetching connection info from manager...")
            response = stub.GetConnectionInfo(request, metadata=self.get_metadata())
            
            if response.success:
                self.logger.info(f"✅ Connection info retrieved successfully")
                return {
                    'annotator_id': response.id if response.id else None,
                    'rabbitmq_host': response.rabbitmq_host,
                    'rabbitmq_port': response.rabbitmq_port,
                    'rabbitmq_username': response.rabbitmq_username,
                    'rabbitmq_password': response.rabbitmq_password
                }
            else:
                self.logger.error(f"❌ Failed to get connection info: {response.message}")
                return None
        except grpc.RpcError as e:
            self.handle_grpc_error(e, "GetConnectionInfo")
            return None
        except Exception as e:
            self.logger.error(f"❌ Unexpected error in GetConnectionInfo: {e}")
            return None
    
    def get_dataset_list(self) -> Optional[List[Dict]]:
        """
        Get list of datasets assigned to this annotator.
        
        Returns:
            list: List of dataset dicts or None if failed
                [{
                    'id': str,
                    'name': str,
                    'ai_model_id': str,
                    'ai_model_name': str,
                    'classes': List[str]
                }, ...]
        """
        try:
            channel = self.create_channel()
            stub = AnnotatorService_pb2_grpc.AnnotatorServiceStub(channel)
            
            request = AnnotatorService_pb2.GetDatasetListRequest(token=self.token)
            
            response = stub.GetDatasetList(request, metadata=self.get_metadata())
            
            if response.success:
                datasets = []
                for dataset in response.data:
                    datasets.append({
                        'id': dataset.id,
                        'name': dataset.name,
                        'ai_model_id': dataset.ai_model_id if dataset.ai_model_id else None,
                        'ai_model_name': dataset.ai_model_name if dataset.ai_model_name else None,
                        'classes': list(dataset.classes) if dataset.classes else []
                    })
                
                return datasets
            else:
                self.logger.error(f"❌ Failed to get dataset list: {response.message}")
                return None
        except grpc.RpcError as e:
            self.handle_grpc_error(e, "GetDatasetList")
            return None
        except Exception as e:
            self.logger.error(f"❌ Unexpected error in GetDatasetList: {e}")
            return None
    
    def get_image(self, file_path: str) -> Optional[bytes]:
        """
        Download image file from manager.
        
        Args:
            file_path: Path to the image file
            
        Returns:
            bytes: Image data or None if failed
        """
        try:
            channel = self.create_channel()
            stub = AnnotatorService_pb2_grpc.AnnotatorServiceStub(channel)
            
            request = AnnotatorService_pb2.GetImageRequest(
                token=self.token,
                file_path=file_path
            )
            
            self.logger.debug(f"📥 Downloading image: {file_path}")
            response = stub.GetImage(request, metadata=self.get_metadata())
            
            if response.success:
                self.logger.debug(f"✅ Image downloaded: {len(response.image_data)} bytes")
                return response.image_data
            else:
                self.logger.error(f"❌ Failed to download image: {response.message}")
                return None
        except grpc.RpcError as e:
            self.handle_grpc_error(e, "GetImage")
            return None
        except Exception as e:
            self.logger.error(f"❌ Unexpected error in GetImage: {e}")
            return None
    
    def send_annotations(
        self,
        items: List[Dict]
    ) -> Optional[Dict]:
        """
        Send batch of annotations for multiple dataset items to manager.
        
        Args:
            items: List of items with annotations
                [{
                    'dataset_item_id': str,
                    'annotations': [
                        {
                            'label': str,
                            'bbox': [x1, y1, x2, y2]
                        }, ...
                    ]
                }, ...]
        
        Returns:
            dict: Response with success status and counts, or None if failed
                {
                    'success': bool,
                    'message': str,
                    'items_processed': int,
                    'annotations_created': int
                }
        """
        try:
            channel = self.create_channel()
            stub = AnnotatorService_pb2_grpc.AnnotatorServiceStub(channel)
            
            # Convert items to proto format
            item_annotations = []
            total_annotations = 0
            
            for item in items:
                dataset_item_id = item['dataset_item_id']
                annotations = item['annotations']
                
                # Convert annotations to proto format
                annotation_data = []
                for ann in annotations:
                    annotation_data.append(
                        AnnotatorService_pb2.AnnotationData(
                            label=ann['label'],
                            bbox_x1=ann['bbox_x1'],
                            bbox_y1=ann['bbox_y1'],
                            bbox_x2=ann['bbox_x2'],
                            bbox_y2=ann['bbox_y2']
                        )
                    )
                    total_annotations += 1
                
                item_annotations.append(
                    AnnotatorService_pb2.DatasetItemAnnotations(
                        dataset_item_id=dataset_item_id,
                        annotations=annotation_data
                    )
                )
            
            request = AnnotatorService_pb2.SendAnnotationsRequest(
                token=self.token,
                items=item_annotations
            )
            
            self.logger.debug(f"📤 Sending {total_annotations} annotations for {len(items)} items")
            response = stub.SendAnnotations(request, metadata=self.get_metadata())
            
            if response.success:
                self.logger.info(
                    f"✅ Processed {response.items_processed} items, "
                    f"created {response.annotations_created} annotations"
                )
                return {
                    'success': True,
                    'message': response.message,
                    'items_processed': response.items_processed,
                    'annotations_created': response.annotations_created
                }
            else:
                self.logger.error(f"❌ Failed to send annotations: {response.message}")
                return {
                    'success': False,
                    'message': response.message,
                    'items_processed': 0,
                    'annotations_created': 0
                }
        except grpc.RpcError as e:
            self.handle_grpc_error(e, "SendAnnotations")
            return None
        except Exception as e:
            self.logger.error(f"❌ Unexpected error in SendAnnotations: {e}")
            return None
    
    def update_status(self, status_code: str) -> bool:
        """
        Update annotator status.
        
        Args:
            status_code: Status code ('connected' or 'disconnected')
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            import time
            channel = self.create_channel()
            stub = AnnotatorService_pb2_grpc.AnnotatorServiceStub(channel)
            
            request = AnnotatorService_pb2.UpdateAnnotatorStatusRequest(
                token=self.token,
                status_code=status_code,
                timestamp=int(time.time() * 1000)  # milliseconds
            )
            
            response = stub.UpdateStatus(request, metadata=self.get_metadata())
            
            if response.success:
                self.logger.debug(f"✅ Status updated to: {status_code}")
                return True
            else:
                self.logger.error(f"❌ Failed to update status: {response.message}")
                return False
        except grpc.RpcError as e:
            self.handle_grpc_error(e, "UpdateStatus")
            return False
        except Exception as e:
            self.logger.error(f"❌ Unexpected error in UpdateStatus: {e}")
            return False
    
    def get_ai_model_list(self) -> Optional[List[Dict]]:
        """
        Get list of AI models assigned to this annotator's datasets.
        
        Returns:
            list: List of AI model dicts or None if failed
                [{
                    'id': str,
                    'name': str,
                    'ai_model_type_code': str,
                    'version': str,
                    'file_path': str,
                    'classes': List[str]
                }, ...]
        """
        try:
            channel = self.create_channel()
            stub = AnnotatorService_pb2_grpc.AnnotatorServiceStub(channel)
            
            request = AnnotatorService_pb2.GetAnnotatorAIModelListRequest(token=self.token)
            
            response = stub.GetAIModelList(request, metadata=self.get_metadata())
            
            if response.success:
                models = []
                for model in response.data:
                    models.append({
                        'id': model.id,
                        'name': model.name,
                        'ai_model_type_code': model.ai_model_type_code,
                        'version': model.version,
                        'file_path': model.file_path,
                        'classes': list(model.classes) if model.classes else []
                    })
                
                return models
            else:
                self.logger.error(f"❌ Failed to get AI model list: {response.message}")
                return None
        except grpc.RpcError as e:
            self.handle_grpc_error(e, "GetAIModelList")
            return None
        except Exception as e:
            self.logger.error(f"❌ Unexpected error in GetAIModelList: {e}")
            return None
    
    def download_ai_model(self, ai_model_id: str, output_path: str) -> bool:
        """
        Download AI model file from manager.
        
        Args:
            ai_model_id: ID of the AI model to download
            output_path: Path where to save the model file
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            import os
            
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            channel = self.create_channel()
            stub = AnnotatorService_pb2_grpc.AnnotatorServiceStub(channel)
            
            request = AnnotatorService_pb2.DownloadAnnotatorAIModelRequest(
                token=self.token,
                ai_model_id=ai_model_id
            )
            
            self.logger.info(f"📥 Downloading AI model: {ai_model_id}")
            
            # Stream the file chunks
            chunk_count = 0
            bytes_received = 0
            with open(output_path, 'wb') as f:
                for response in stub.DownloadAIModel(request, metadata=self.get_metadata()):
                    if not response.success:
                        self.logger.error(f"❌ Download error: {response.message}")
                        # Remove partial file
                        if os.path.exists(output_path):
                            os.remove(output_path)
                        return False
                    
                    if response.chunk_data:
                        chunk_size = len(response.chunk_data)
                        f.write(response.chunk_data)
                        chunk_count += 1
                        bytes_received += chunk_size
                        if chunk_count % 100 == 0:  # Log progress every 100 chunks
                            self.logger.debug(f"📦 Downloaded {chunk_count} chunks ({bytes_received / 1024 / 1024:.2f} MB)")
            
            self.logger.info(f"✅ Model downloaded successfully: {output_path} ({bytes_received / 1024 / 1024:.2f} MB, {chunk_count} chunks)")
            return True
            
        except grpc.RpcError as e:
            self.handle_grpc_error(e, "DownloadAIModel")
            self.logger.error(f"❌ gRPC error details: status_code={e.code()}, details={e.details()}")
            # Remove partial file
            if os.path.exists(output_path):
                os.remove(output_path)
            return False
        except Exception as e:
            self.logger.error(f"❌ Unexpected error in DownloadAIModel: {e}")
            import traceback
            self.logger.error(traceback.format_exc())
            # Remove partial file
            if os.path.exists(output_path):
                os.remove(output_path)
            return False
