"""
CAEMA Utils
A collection of reusable Python modules for AI services.

Available modules:
- pose_estimation: Body keypoint detection using YOLOv8
"""

__version__ = "0.2.0"
__author__ = "CAEMA Solutions"

from . import pose_estimation

__all__ = ["pose_estimation", "__version__"]
