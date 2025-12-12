"""
PoseEstimator - High-level interface for pose estimation.
This is the main class users will interact with.
"""

import io
import base64
from typing import Dict, Any, Optional, Union
from pathlib import Path

from .models.analyzer import PoseAnalyzer


class PoseEstimator:
    """
    High-level interface for body pose estimation and analysis.

    This class provides a simple API for analyzing body posture from images.
    It handles image loading, pose detection, biomechanical analysis, and
    returns annotated images with detected keypoints.

    Example:
        >>> from caema_utils.pose_estimation import PoseEstimator
        >>> estimator = PoseEstimator()
        >>> result = estimator.analyze("photo.jpg")
        >>> print(result['analysis'])
        >>> result['annotated_image_bytes']  # PNG bytes with skeleton overlay
    """

    def __init__(self, model_size: str = "nano"):
        """
        Initialize the pose estimator.

        Args:
            model_size: Size of the YOLO model to use.
                       Options: "nano" (fastest), "small", "medium", "large", "xlarge"
                       Default is "nano" for best speed/accuracy balance.
        """
        model_map = {
            "nano": "yolov8n-pose.pt",
            "small": "yolov8s-pose.pt",
            "medium": "yolov8m-pose.pt",
            "large": "yolov8l-pose.pt",
            "xlarge": "yolov8x-pose.pt",
        }

        if model_size not in model_map:
            raise ValueError(
                f"Invalid model_size: {model_size}. "
                f"Options: {list(model_map.keys())}"
            )

        self._analyzer = PoseAnalyzer(model_name=model_map[model_size])
        self._model_size = model_size

    @property
    def model_size(self) -> str:
        """Get the current model size."""
        return self._model_size

    def analyze(
        self,
        image: Union[str, Path, bytes],
        output_format: str = "bytes",
        save_path: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Analyze body posture from an image.

        Args:
            image: Image to analyze. Can be:
                   - str/Path: Path to image file
                   - bytes: Image bytes (e.g., from HTTP request)
            output_format: Format for annotated image output.
                          Options: "bytes" (default), "base64", "array", "file"
            save_path: If output_format is "file", save annotated image here.

        Returns:
            Dictionary with:
                - success (bool): Whether analysis succeeded
                - keypoints (dict): Detected body keypoints with coordinates
                - angles (dict): Calculated biomechanical angles
                - confidence (float): Average detection confidence (0-1)
                - analysis (str): Text analysis of postural findings
                - annotated_image_* : Annotated image in requested format
                - error (str): Error message if success is False

        Example:
            >>> result = estimator.analyze("photo.jpg")
            >>> if result['success']:
            ...     print(f"Confidence: {result['confidence']:.1%}")
            ...     print(result['analysis'])
            ...     # Save annotated image
            ...     with open("output.png", "wb") as f:
            ...         f.write(result['annotated_image_bytes'])
        """
        # Handle different input types
        if isinstance(image, (str, Path)):
            return self._analyze_file(str(image), output_format, save_path)
        elif isinstance(image, bytes):
            return self._analyze_bytes(image, output_format, save_path)
        else:
            raise TypeError(
                f"image must be str, Path, or bytes, got {type(image).__name__}"
            )

    def _analyze_file(
        self,
        file_path: str,
        output_format: str,
        save_path: Optional[str]
    ) -> Dict[str, Any]:
        """Analyze image from file path."""
        # Read file as bytes
        with open(file_path, "rb") as f:
            image_bytes = f.read()

        return self._analyze_bytes(image_bytes, output_format, save_path)

    def _analyze_bytes(
        self,
        image_bytes: bytes,
        output_format: str,
        save_path: Optional[str]
    ) -> Dict[str, Any]:
        """Analyze image from bytes."""
        # Get raw result with bytes output
        result = self._analyzer.analyze_bytes(image_bytes)

        if not result['success']:
            return result

        # Convert annotated image to requested format
        annotated_bytes = result.pop('annotated_image_bytes', None)

        if output_format == "bytes":
            result['annotated_image_bytes'] = annotated_bytes
        elif output_format == "base64":
            if annotated_bytes:
                result['annotated_image_base64'] = base64.b64encode(annotated_bytes).decode('utf-8')
        elif output_format == "array":
            import numpy as np
            import cv2
            if annotated_bytes:
                nparr = np.frombuffer(annotated_bytes, np.uint8)
                result['annotated_image_array'] = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        elif output_format == "file":
            if save_path and annotated_bytes:
                with open(save_path, "wb") as f:
                    f.write(annotated_bytes)
                result['annotated_image_path'] = save_path
        else:
            raise ValueError(
                f"Invalid output_format: {output_format}. "
                "Options: bytes, base64, array, file"
            )

        return result

    def analyze_and_save(
        self,
        image: Union[str, Path, bytes],
        output_path: str
    ) -> Dict[str, Any]:
        """
        Analyze image and save annotated result to file.

        Convenience method that calls analyze() with file output.

        Args:
            image: Image to analyze (path or bytes).
            output_path: Path to save annotated image.

        Returns:
            Analysis result dictionary with 'annotated_image_path'.
        """
        return self.analyze(image, output_format="file", save_path=output_path)

    def get_keypoint_names(self) -> Dict[int, str]:
        """Get mapping of keypoint indices to names."""
        return self._analyzer.KEYPOINT_NAMES.copy()

    def get_skeleton_connections(self) -> list:
        """Get list of skeleton connection pairs."""
        return list(self._analyzer.SKELETON_CONNECTIONS)


# Convenience function for one-off analysis
def analyze_pose(
    image: Union[str, Path, bytes],
    model_size: str = "nano",
    output_format: str = "bytes"
) -> Dict[str, Any]:
    """
    Convenience function for quick pose analysis.

    Creates a PoseEstimator instance and analyzes the image.
    For multiple images, create a PoseEstimator instance directly
    to avoid reloading the model each time.

    Args:
        image: Image to analyze (path or bytes).
        model_size: YOLO model size (nano, small, medium, large, xlarge).
        output_format: Output format for annotated image.

    Returns:
        Analysis result dictionary.

    Example:
        >>> from caema_utils.pose_estimation import analyze_pose
        >>> result = analyze_pose("photo.jpg")
        >>> print(result['analysis'])
    """
    estimator = PoseEstimator(model_size=model_size)
    return estimator.analyze(image, output_format=output_format)
