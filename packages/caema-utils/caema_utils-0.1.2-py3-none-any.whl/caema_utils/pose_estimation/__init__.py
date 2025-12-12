"""
Pose Estimation Module
AI-powered body pose analysis using YOLOv8 for biomechanical evaluation.

Usage:
    from caema_utils.pose_estimation import PoseEstimator

    # Initialize estimator
    estimator = PoseEstimator()

    # Analyze an image
    result = estimator.analyze("path/to/image.jpg")

    # Or analyze bytes directly
    result = estimator.analyze_bytes(image_bytes)
"""

from .estimator import PoseEstimator
from .models.analyzer import PoseAnalyzer

__all__ = ["PoseEstimator", "PoseAnalyzer"]
