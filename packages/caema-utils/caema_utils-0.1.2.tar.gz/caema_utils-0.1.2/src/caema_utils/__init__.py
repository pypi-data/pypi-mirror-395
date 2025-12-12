"""
CAEMA Utils - System Dependency Manager
A collection of reusable Python modules for AI services.

Available modules:
- pose_estimation: AI-powered body pose analysis using YOLOv8
"""

__version__ = "0.1.2"
__author__ = "CAEMA Solutions"

from . import pose_estimation

__all__ = ["pose_estimation", "__version__"]
