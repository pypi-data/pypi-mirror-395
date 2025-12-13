"""
gRPC client for AutoAnnotation
"""
from dataclasses import dataclass
import grpc
import logging
from typing import List
from .GrpcClientBase import GrpcClientBase
from . import AutoAnnotation_pb2
from . import AutoAnnotation_pb2_grpc


@dataclass
class DatasetItemResponse:
    id: str
    dataset_id: str
    file_path: str
    
@dataclass
class AutoAnnotationResultRequest:
    dataset_item_id: str
    bboxx1: float
    bboxy1: float
    bboxx2: float
    bboxy2: float
    class_name: str

class AutoAnnotationGrpcClient(GrpcClientBase):
    def __init__(self, server_host: str, server_port: int, token: str):
        super().__init__(server_host, server_port, token)
        self.logger = logging.getLogger(__name__)

    def get_dataset_items(self, dataset_id: str):
        try:
            channel = self.create_channel()
            stub = AutoAnnotation_pb2_grpc.AutoAnnotationResultServiceStub(channel)
            
            request = AutoAnnotation_pb2.GetDatasetItemsRequest(
                token=self.token,
                dataset_id=dataset_id
            )
            
            response = stub.GetDatasetItems(request, metadata=self.get_metadata())
            
            if response.success:
                response.data
                return [ 
                    DatasetItemResponse( 
                        id=item.id, 
                        dataset_id=item.dataset_id, 
                        file_path=item.file_path) 
                    for item in response.data 
                ]
            else:
                self.logger.error(f"❌ Failed to get connection info: {response.message}")
                return None
        except grpc.RpcError as e:
            self.handle_grpc_error(e, "GetConnectionInfo")
            return None
        except Exception as e:
            self.logger.error(f"❌ Unexpected error in GetConnectionInfo: {e}")
            return None
    
    def save_annotation_result(self, results: list[AutoAnnotationResultRequest]):
        try:
            channel = self.create_channel()
            stub = AutoAnnotation_pb2_grpc.AutoAnnotationResultServiceStub(channel)
            
            request = AutoAnnotation_pb2.SaveAnnotationResultRequest(
                token=self.token,
                data=[
                    AutoAnnotation_pb2.AutoAnnotationResultRequest(
                        dataset_item_id=result.dataset_item_id,
                        bboxx1=result.bboxx1,
                        bboxy1=result.bboxy1,
                        bboxx2=result.bboxx2,
                        bboxy2=result.bboxy2,
                        class_name=result.class_name,
                    ) for result in results
                ]
            )
            
            response = stub.SaveAnnotationResult(request, metadata=self.get_metadata())
            
            if response.success:
                return True
            else:
                self.logger.error(f"❌ Failed to get connection info: {response.message}")
                return None
        except grpc.RpcError as e:
            self.handle_grpc_error(e, "GetConnectionInfo")
            return None
        except Exception as e:
            self.logger.error(f"❌ Unexpected error in GetConnectionInfo: {e}")
            return None
    