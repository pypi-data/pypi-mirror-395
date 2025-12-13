"""
Pose Estimation Module
Body keypoint detection using YOLOv8.

Usage:
    from caema_utils.pose_estimation import PoseEstimator

    # Initialize estimator
    estimator = PoseEstimator()

    # Detect keypoints from an image
    result = estimator.analyze("path/to/image.jpg")

    # Result contains: keypoints, angles, confidence, annotated_image_bytes
"""

from .estimator import PoseEstimator
from .models.analyzer import PoseAnalyzer

__all__ = ["PoseEstimator", "PoseAnalyzer"]
