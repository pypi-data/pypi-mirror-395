"""
CLI entry point for NEDO Vision Annotator Service
"""
import argparse
import sys
from .annotator_service import AnnotatorService


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="NEDO Vision Annotator Service - Automated annotation service"
    )
    
    parser.add_argument(
        "--server-host",
        type=str,
        default="be.vision.sindika.co.id",
        help="Manager server host (default: be.vision.sindika.co.id)",
    )
    
    parser.add_argument(
        "--server-port",
        type=int,
        default=50051,
        help="Manager server gRPC port (default: 50051)",
    )
    
    parser.add_argument(
        "--token",
        type=str,
        required=True,
        help="Authentication token for the annotator",
    )
    
    parser.add_argument(
        "--storage-path",
        type=str,
        default="data",
        help="Storage path for databases and files (default: data)",
    )
    
    parser.add_argument(
        "--batch-size",
        type=int,
        default=50,
        help="Number of annotations to batch before sending (default: 50)",
    )
    
    parser.add_argument(
        "--send-interval",
        type=int,
        default=60,
        help="Interval in seconds to send annotations (default: 60)",
    )
    
    
    parser.add_argument(
        "--annotate-all-batch-size",
        type=int,
        default=3,
        help="Batch size for auto annotate all requests (default: 3)",
    )
    
    
    parser.add_argument(
        "--annotate-all-grpc-batch-size",
        type=int,
        default=15,
        help="Batch size for auto annotate all requests (default: 15)",
    )
    
    args = parser.parse_args()
    
    # Create and run the annotator service
    service = AnnotatorService(
        server_host=args.server_host,
        server_port=args.server_port,
        token=args.token,
        storage_path=args.storage_path,
        batch_size=args.batch_size,
        send_interval=args.send_interval,
        annotate_all_batch_size=args.annotate_all_batch_size,
        annotate_all_grpc_batch_size=args.annotate_all_grpc_batch_size
    )
    
    try:
        service.start()
    except KeyboardInterrupt:
        print("\n🛑 [APP] Received interrupt signal. Shutting down...")
        service.stop()
    except Exception as e:
        print(f"❌ [APP] Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
