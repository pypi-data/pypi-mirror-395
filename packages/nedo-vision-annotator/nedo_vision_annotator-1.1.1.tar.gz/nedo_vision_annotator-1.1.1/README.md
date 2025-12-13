# Nedo Vision Annotator Service

## Overview

Python service that automatically annotates dataset images using AI models. Listens to RabbitMQ for image processing tasks, runs inference using YOLO/RF-DETR models with GPU acceleration, and sends annotations back to the manager via gRPC.

## Features

- **Automated Annotation**: Process images from RabbitMQ queue automatically
- **Multi-Model Support**: YOLO and RF-DETR detection models
- **GPU Acceleration**: Automatic CUDA detection for faster inference
- **Batch Processing**: Efficient batch annotation submission
- **Local Storage**: SQLite-based annotation queue before sending
- **Authentication**: Token-based authentication with manager
- **Configuration Management**: Persistent configuration storage
- **Status Reporting**: Real-time status updates to manager

## Architecture

### Core Components

1. **Configuration Management** (`config/ConfigurationManager.py`)

   - SQLite-based key-value storage
   - Stores: server_host, server_port, token, annotator_id
   - Convenience methods for common config keys

2. **Database Management** (`database/`)

   - SQLAlchemy-based architecture with entity-repository pattern
   - Local annotation storage with pending queue
   - Entities: `DatasetAnnotation`
   - Repositories: `DatasetAnnotationRepository`
   - Session management with connection pooling

3. **AI Models** (`models/AIModel.py`)

   - AI model entity representation
   - Support for YOLO and RF-DETR models
   - Class management for object detection
   - Version tracking for model updates

4. **Detection** (`detection/`)

   - `BaseDetector`: Abstract base class for all detectors
   - `YOLODetector`: Ultralytics YOLO detection with GPU support
   - `RFDETRDetector`: RF-DETR detection with GPU support
   - Standardized output: `[{"label": str, "confidence": float, "bbox": [x1, y1, x2, y2]}]`
   - Normalized bounding boxes (0-1 range)

5. **Core Logic** (`core/`)

   - `DatasetManager`: Dataset synchronization and management
   - `ModelLoader`: AI model loading, caching, and version control

6. **Background Tasks** (`tasks/`)

   - `AnnotationProcessor`: Image download and detection processing
   - `AnnotationSender`: Batch annotation submission to manager
   - `MessageHandler`: RabbitMQ message routing and validation
   - `StatusReporter`: Periodic status updates

7. **Services** (`services/`)
   - `GrpcClientBase`: Base gRPC client with authentication
   - `AnnotatorGrpcClient`: Manager communication for datasets, images, and annotations
   - `RabbitMQConsumer`: Message queue consumer with reconnection logic

### Main Service (`annotator_service.py`)

- Entry point for the annotator service
- Manages service lifecycle (initialization, start, stop)
- Signal handling for graceful shutdown
- Configuration initialization and validation
- Coordinates all background tasks

### CLI (`cli.py`)

Command-line interface with the following arguments:

- `--token` (required): Authentication token for the annotator
- `--server-host`: Manager server host (default: be.vision.sindika.co.id)
- `--server-port`: gRPC port (default: 50051)
- `--storage-path`: Data storage path (default: data)
- `--batch-size`: Annotations per batch (default: 50)
- `--send-interval`: Send interval in seconds (default: 60)

## Installation

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install in development mode
pip install -e .
```

## Usage

```bash
# Run annotator service
nedo-vision-annotator --token YOUR_TOKEN --server-host localhost

# Or with Python module
python -m nedo_vision_annotator.cli --token YOUR_TOKEN

# With custom settings
nedo-vision-annotator \
  --token YOUR_TOKEN \
  --server-host localhost \
  --server-port 50051 \
  --batch-size 100 \
  --send-interval 30
```

## Dependencies

- **gRPC**: Communication with manager (grpcio, grpcio-tools, protobuf)
- **RabbitMQ**: Message queue (pika)
- **AI/ML**: Model inference (torch, torchvision, ultralytics, rfdetr<=1.2.0, opencv-python, numpy)
- **Database**: Local storage (sqlalchemy)
- **System**: Resource monitoring (psutil)

## gRPC Services

### AnnotatorService

The annotator uses the following gRPC methods:

- `GetConnectionInfo`: Fetch RabbitMQ connection details and annotator ID
- `GetDatasetList`: Get assigned datasets with AI model information
- `GetAIModelList`: List AI models assigned to annotator's datasets
- `DownloadAIModel`: Stream download AI model files
- `GetImage`: Download image file from storage
- `SendAnnotations`: Submit batch of annotations to manager
- `UpdateStatus`: Report annotator status (connected/disconnected)

## Data Flow

1. **Initialization**

   - Connect to manager via gRPC using authentication token
   - Fetch annotator ID and RabbitMQ connection information
   - Retrieve assigned datasets with AI model configurations
   - Download and load required AI models

2. **Processing Loop**

   - Listen to dedicated RabbitMQ queue for annotation requests
   - Receive message with dataset item ID and image path
   - Download image from storage via gRPC
   - Run inference using assigned AI model
   - Store annotations locally with normalized bounding boxes (0-1 range)
   - Batch annotations for efficient submission

3. **Annotation Submission**

   - Collect pending annotations up to batch size
   - Group annotations by dataset item
   - Send batch to manager via gRPC
   - Delete local annotations after successful submission
   - Retry on failure with exponential backoff

4. **Model Management**

   - Load AI models on demand when processing starts
   - Cache loaded models in memory for reuse
   - Monitor model versions and re-download on updates
   - Support for YOLO and RF-DETR model types

5. **Status Reporting**
   - Periodic status updates (connected/disconnected)
   - System metrics: CPU usage, temperature, RAM usage, latency
   - Automatic reconnection handling on network issues

## Configuration

The annotator stores configuration in SQLite database at `{storage_path}/config/config.db`:

- `server_host`: Manager server hostname
- `server_port`: Manager gRPC port
- `token`: Authentication token
- `annotator_id`: Unique annotator identifier (fetched from manager)

## Logging

Logs are written to stdout with the following format:

```
YYYY-MM-DD HH:MM:SS [LEVEL] Message
```

Log levels:

- ERROR: Critical errors and failures
- WARNING: Non-critical issues
- INFO: Important events and status changes
- DEBUG: Detailed debugging information (disabled by default)

## Error Handling

- **Authentication Failures**: Automatic shutdown on invalid token
- **Network Issues**: Automatic reconnection with exponential backoff
- **Model Loading Errors**: Logged and skipped, service continues
- **RabbitMQ Disconnection**: Automatic reconnection attempts
- **gRPC Errors**: Retry logic with timeout handling

## Performance

- **GPU Acceleration**: Automatic CUDA detection and usage
- **Batch Processing**: Configurable batch size for efficient submission
- **Connection Pooling**: Database connection pool for concurrent operations
- **Model Caching**: In-memory model cache to avoid reloading
- **Async Operations**: Background threads for non-blocking tasks
