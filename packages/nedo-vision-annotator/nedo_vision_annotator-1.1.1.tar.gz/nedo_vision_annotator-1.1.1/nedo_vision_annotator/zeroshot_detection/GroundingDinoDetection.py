import logging
import os
import torch
import hashlib
import requests

from typing import List, Tuple, Optional, Union
from dataclasses import dataclass
from PIL import Image
from pathlib import Path
import numpy as np

from .ZeroShotDetection import ZeroShotDetection
from ..types.ZeroShotDetectionType import DetectionResult, ImageSource, ModelConfig

from dataclasses import dataclass

logger = logging.getLogger(__name__)


def _download_file(url: str, dst: Path) -> None:
    """Download a file from a URL to a destination path with logging."""
    logger.info(f"Downloading weights from {url} to {dst}")
    dst.parent.mkdir(parents=True, exist_ok=True)

    try:
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            total_length = r.headers.get("content-length")
            total = int(total_length) if total_length is not None else 0

            with open(dst, "wb") as f:
                downloaded = 0
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        if total > 0:
                            percent = downloaded * 100 / total
                            if downloaded % (1024 * 1024 * 10) == 0:
                                logger.debug(f"Downloading... {percent:.2f}%")
        logger.info("Download completed successfully.")
    except requests.RequestException as e:
        logger.error(f"Download failed: {e}")
        if dst.exists():
            os.remove(dst)
        raise


@dataclass
class GroundingDINOConfig(ModelConfig):
    """Configuration specific to Grounding DINO."""
    config_path: str = "groundingdino/config/GroundingDINO_SwinB_cfg.py"
    config_url: str = (
        "https://raw.githubusercontent.com/IDEA-Research/GroundingDINO/main/groundingdino/config/GroundingDINO_SwinB_cfg.py"
    )
    checkpoint_path: str = "groundingdino/weights/groundingdino_swinb_cogcoor.pth"
    checkpoint_url: str = (
        "https://github.com/IDEA-Research/GroundingDINO/releases/download/v0.1.0-alpha2/groundingdino_swinb_cogcoor.pth"
    )
    box_threshold: float = 0.35
    text_threshold: float = 0.25
    device: str = "cuda" if torch.cuda.is_available() else "cpu"

    def validate(self) -> None:
        """Validate Grounding DINO configuration."""
        ckpt_path = Path(self.checkpoint_path)
        cnfg_path = Path(self.config_path)

        if not cnfg_path.exists():
            logger.warning(
                f"Config file not found at {cnfg_path}. Initiating download..."
            )
            _download_file(self.config_url, cnfg_path)

        if not ckpt_path.exists():
            logger.warning(
                f"Checkpoint not found at {ckpt_path}. Initiating download..."
            )
            _download_file(self.checkpoint_url, ckpt_path)

        # Validate thresholds
        if not 0.0 <= self.box_threshold <= 1.0:
            raise ValueError(
                f"box_threshold must be in [0, 1], got {self.box_threshold}"
            )
        if not 0.0 <= self.text_threshold <= 1.0:
            raise ValueError(
                f"text_threshold must be in [0, 1], got {self.text_threshold}"
            )

        # Validate device
        if self.device == "cuda" and not torch.cuda.is_available():
            logger.warning("CUDA requested but not available, falling back to CPU")
            self.device = "cpu"


class GroundingDINODetection(ZeroShotDetection):
    """
    Concrete implementation of zero-shot detection using Grounding DINO.

    This class provides a type-safe, production-ready implementation
    of the ZeroShotDetection interface using the Grounding DINO model.
    """

    def __init__(self, config: Optional[GroundingDINOConfig] = None) -> None:
        """
        Initialize Grounding DINO detector.

        Args:
            config: Grounding DINO configuration. Uses defaults if None.
        """
        if config is None:
            config = GroundingDINOConfig()

        super().__init__(config)
        self.config: GroundingDINOConfig
        self._load_model()

        logger.info(f"Grounding DINO initialized on {self.config.device}")

    def _load_model(self) -> None:
        """Load Grounding DINO model."""
        try:
            from groundingdino.util.inference import load_model

            self.model = load_model(
                self.config.config_path,
                self.config.checkpoint_path,
                device=self.config.device,
            )

            # Set model to evaluation mode
            if self.model is not None:
                self.model.eval()

            logger.info("Grounding DINO model loaded successfully")

        except ImportError as e:
            logger.error(
                "Failed to import GroundingDINO. "
                "Install with: pip install groundingdino"
            )
            raise
        except Exception as e:
            logger.error(f"Failed to load model: {e}")
            raise

    def load_image(self, image_source: ImageSource) -> Tuple[np.ndarray, torch.Tensor]:
        """
        Load and preprocess image for Grounding DINO.

        Args:
            image_source: Path to image, numpy array, or PIL Image

        Returns:
            Tuple of (original_image_np, transformed_image_tensor)
        """
        try:
            from groundingdino.util.inference import load_image as gd_load_image

            # Handle different input types with type checking
            processed_source: Union[str, Image.Image]

            if isinstance(image_source, (str, Path)):
                path_str = str(image_source)
                if not os.path.exists(path_str):
                    raise FileNotFoundError(f"Image not found: {path_str}")
                processed_source = path_str

            elif isinstance(image_source, np.ndarray):
                # Convert numpy array to PIL Image
                processed_source = Image.fromarray(image_source)

            elif isinstance(image_source, Image.Image):
                processed_source = image_source

            else:
                raise TypeError(
                    f"Unsupported image type: {type(image_source)}. "
                    f"Expected str, Path, np.ndarray, or PIL.Image"
                )

            # Load and transform
            image_np: np.ndarray
            image_tensor: torch.Tensor
            image_np, image_tensor = gd_load_image(processed_source)

            return image_np, image_tensor

        except Exception as e:
            logger.error(f"Failed to load image: {e}")
            raise

    def predict(
        self,
        image: ImageSource,
        text_prompt: str,
        box_threshold: Optional[float] = None,
        text_threshold: Optional[float] = None,
    ) -> DetectionResult:
        """
        Perform zero-shot object detection with Grounding DINO.

        Args:
            image: Image source
            text_prompt: Text description (e.g., "cat . dog . person")
            box_threshold: Confidence threshold for boxes
            text_threshold: Confidence threshold for text matching

        Returns:
            DetectionResult with type-safe detection data
        """
        if self.model is None:
            raise RuntimeError("Model not loaded. Call _load_model() first.")

        # Use provided thresholds or fall back to config
        box_thresh = (
            box_threshold if box_threshold is not None else self.config.box_threshold
        )
        text_thresh = (
            text_threshold if text_threshold is not None else self.config.text_threshold
        )

        try:
            from groundingdino.util.inference import predict as gd_predict

            # Load and preprocess image
            image_np, image_tensor = self.load_image(image)

            # Run inference with no gradient computation
            with torch.no_grad():
                boxes: torch.Tensor
                logits: torch.Tensor
                phrases: List[str]

                boxes, logits, phrases = gd_predict(
                    model=self.model,
                    image=image_tensor,
                    caption=text_prompt,
                    box_threshold=box_thresh,
                    text_threshold=text_thresh,
                    device=self.config.device,
                )

            # Create type-safe result
            result = DetectionResult(
                boxes=boxes,
                scores=logits,
                labels=phrases,
                image_shape=(image_np.shape[0], image_np.shape[1]),
            )

            logger.info(f"Detected {len(result)} objects")
            return result

        except Exception as e:
            logger.error(f"Prediction failed: {e}")
            raise

    def annotate_image(
        self,
        image: ImageSource,
        result: DetectionResult,
        output_path: Optional[Union[str, Path]] = None,
    ) -> np.ndarray:
        """
        Annotate image with Grounding DINO predictions.

        Args:
            image: Original image
            result: Detection results from predict()
            output_path: Optional path to save annotated image

        Returns:
            Annotated image as numpy array
        """
        try:
            from groundingdino.util.inference import annotate as gd_annotate

            # Load image if path provided
            image_np: np.ndarray
            if isinstance(image, (str, Path)):
                image_np, _ = self.load_image(image)
            elif isinstance(image, np.ndarray):
                image_np = image
            elif isinstance(image, Image.Image):
                image_np = np.array(image)
            else:
                raise TypeError(f"Unsupported image type: {type(image)}")

            # Annotate with type-safe data
            annotated_image: np.ndarray = gd_annotate(
                image_source=image_np,
                boxes=result.boxes.cpu(),
                logits=result.scores.cpu(),
                phrases=result.labels,
            )

            # Save if output path provided
            if output_path is not None:
                output_str = str(output_path)
                Image.fromarray(annotated_image).save(output_str)
                logger.info(f"Saved annotated image to {output_str}")

            return annotated_image

        except Exception as e:
            logger.error(f"Annotation failed: {e}")
            raise
