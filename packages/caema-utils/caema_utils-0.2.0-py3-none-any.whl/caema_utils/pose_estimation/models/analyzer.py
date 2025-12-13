"""
Pose Analyzer Module
Detects body keypoints and calculates angles using YOLOv8.
"""

import math
from typing import Dict, List, Tuple, Optional, Any
import numpy as np

try:
    import cv2
except ImportError:
    cv2 = None

try:
    from ultralytics import YOLO
except ImportError:
    YOLO = None


class PoseAnalyzer:
    """Body keypoint detector using YOLOv8-pose model."""

    # COCO format keypoint indices
    KEYPOINT_NAMES = {
        0: 'nose',
        1: 'left_eye',
        2: 'right_eye',
        3: 'left_ear',
        4: 'right_ear',
        5: 'left_shoulder',
        6: 'right_shoulder',
        7: 'left_elbow',
        8: 'right_elbow',
        9: 'left_wrist',
        10: 'right_wrist',
        11: 'left_hip',
        12: 'right_hip',
        13: 'left_knee',
        14: 'right_knee',
        15: 'left_ankle',
        16: 'right_ankle'
    }

    # Skeleton connections for drawing
    SKELETON_CONNECTIONS = [
        ('nose', 'left_eye'), ('nose', 'right_eye'),
        ('left_eye', 'left_ear'), ('right_eye', 'right_ear'),
        ('left_shoulder', 'right_shoulder'),
        ('left_shoulder', 'left_elbow'), ('left_elbow', 'left_wrist'),
        ('right_shoulder', 'right_elbow'), ('right_elbow', 'right_wrist'),
        ('left_shoulder', 'left_hip'), ('right_shoulder', 'right_hip'),
        ('left_hip', 'right_hip'),
        ('left_hip', 'left_knee'), ('left_knee', 'left_ankle'),
        ('right_hip', 'right_knee'), ('right_knee', 'right_ankle')
    ]

    def __init__(self, model_name: str = 'yolov8n-pose.pt'):
        """
        Initialize the pose analyzer.

        Args:
            model_name: Name of the YOLO model to use.
                       Options: yolov8n-pose.pt, yolov8s-pose.pt, yolov8m-pose.pt
        """
        if YOLO is None:
            raise ImportError(
                "ultralytics is required for pose estimation. "
                "Install with: pip install ultralytics"
            )
        if cv2 is None:
            raise ImportError(
                "opencv-python is required for pose estimation. "
                "Install with: pip install opencv-python-headless"
            )

        self.model_name = model_name
        self._load_model()

    def _load_model(self):
        """Load the YOLO model with PyTorch 2.6+ compatibility."""
        import torch

        # Save original torch.load
        _original_torch_load = torch.load

        # Patch for PyTorch 2.6+ compatibility
        def _patched_torch_load(*args, **kwargs):
            kwargs['weights_only'] = False
            return _original_torch_load(*args, **kwargs)

        torch.load = _patched_torch_load

        try:
            self.model = YOLO(self.model_name)
        finally:
            torch.load = _original_torch_load

    def analyze_image(self, image_path: str) -> Dict[str, Any]:
        """
        Analyze an image file and detect keypoints.

        Args:
            image_path: Path to the image file.

        Returns:
            Dictionary with keypoints, angles, and annotated image path.
        """
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"Could not load image: {image_path}")

        return self._analyze_image_array(image, output_path=image_path.replace('.', '_analyzed.'))

    def analyze_bytes(self, image_bytes: bytes) -> Dict[str, Any]:
        """
        Analyze image from bytes.

        Args:
            image_bytes: Image as bytes (e.g., from file upload).

        Returns:
            Dictionary with keypoints, angles, and annotated image bytes.
        """
        # Decode bytes to numpy array
        nparr = np.frombuffer(image_bytes, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if image is None:
            raise ValueError("Could not decode image from bytes")

        return self._analyze_image_array(image, return_bytes=True)

    def analyze_numpy(self, image: np.ndarray) -> Dict[str, Any]:
        """
        Analyze image from numpy array.

        Args:
            image: Image as numpy array (BGR format).

        Returns:
            Dictionary with keypoints, angles, and annotated image.
        """
        return self._analyze_image_array(image, return_array=True)

    def _analyze_image_array(
        self,
        image: np.ndarray,
        output_path: Optional[str] = None,
        return_bytes: bool = False,
        return_array: bool = False
    ) -> Dict[str, Any]:
        """Internal method to analyze image array."""
        # Detect pose
        results = self.model(image, verbose=False)

        if len(results) == 0 or len(results[0].keypoints) == 0:
            return {
                'success': False,
                'error': 'No person detected in the image'
            }

        # Extract keypoints from first detected person
        keypoints_data = results[0].keypoints[0]
        keypoints = self._extract_keypoints(keypoints_data)

        # Calculate angles
        angles = self._calculate_angles(keypoints)

        # Create annotated visualization
        annotated_image = self._draw_pose(image.copy(), keypoints)

        # Prepare result
        result = {
            'success': True,
            'keypoints': keypoints,
            'angles': angles,
            'confidence': float(np.mean([kp[2] for kp in keypoints.values()])),
        }

        # Handle output format
        if output_path:
            cv2.imwrite(output_path, annotated_image)
            result['annotated_image_path'] = output_path
        elif return_bytes:
            _, buffer = cv2.imencode('.png', annotated_image)
            result['annotated_image_bytes'] = buffer.tobytes()
        elif return_array:
            result['annotated_image'] = annotated_image

        return result

    def _extract_keypoints(self, keypoints_data) -> Dict[str, List[float]]:
        """Extract keypoints as dictionary."""
        keypoints = {}

        xy = keypoints_data.xy[0].cpu().numpy()
        conf = keypoints_data.conf[0].cpu().numpy() if hasattr(keypoints_data, 'conf') else None

        for idx, name in self.KEYPOINT_NAMES.items():
            if idx < len(xy):
                x, y = xy[idx]
                confidence = conf[idx] if conf is not None else 1.0
                keypoints[name] = [float(x), float(y), float(confidence)]

        return keypoints

    def _calculate_angles(self, keypoints: Dict[str, List[float]]) -> Dict[str, float]:
        """Calculate angles between body segments."""
        angles = {}

        # Neck angle (nose to mid-shoulder relative to vertical)
        if all(k in keypoints for k in ['nose', 'left_shoulder', 'right_shoulder']):
            nose = keypoints['nose'][:2]
            mid_shoulder = self._midpoint(
                keypoints['left_shoulder'][:2],
                keypoints['right_shoulder'][:2]
            )
            angles['neck_angle'] = self._angle_to_vertical(nose, mid_shoulder)

        # Shoulder line angle (relative to horizontal)
        if 'left_shoulder' in keypoints and 'right_shoulder' in keypoints:
            angles['shoulder_line_angle'] = self._line_angle(
                keypoints['left_shoulder'][:2],
                keypoints['right_shoulder'][:2]
            )

        # Hip line angle (relative to horizontal)
        if 'left_hip' in keypoints and 'right_hip' in keypoints:
            angles['hip_line_angle'] = self._line_angle(
                keypoints['left_hip'][:2],
                keypoints['right_hip'][:2]
            )

        # Torso angle (mid-shoulder to mid-hip relative to vertical)
        if all(k in keypoints for k in ['left_shoulder', 'right_shoulder', 'left_hip', 'right_hip']):
            mid_shoulder = self._midpoint(
                keypoints['left_shoulder'][:2],
                keypoints['right_shoulder'][:2]
            )
            mid_hip = self._midpoint(
                keypoints['left_hip'][:2],
                keypoints['right_hip'][:2]
            )
            angles['torso_angle'] = self._angle_to_vertical(mid_shoulder, mid_hip)

        # Elbow angles
        for side in ['left', 'right']:
            if all(f'{side}_{part}' in keypoints for part in ['shoulder', 'elbow', 'wrist']):
                angle = self._joint_angle(
                    keypoints[f'{side}_shoulder'][:2],
                    keypoints[f'{side}_elbow'][:2],
                    keypoints[f'{side}_wrist'][:2]
                )
                angles[f'{side}_elbow_angle'] = angle

        # Knee angles
        for side in ['left', 'right']:
            if all(f'{side}_{part}' in keypoints for part in ['hip', 'knee', 'ankle']):
                angle = self._joint_angle(
                    keypoints[f'{side}_hip'][:2],
                    keypoints[f'{side}_knee'][:2],
                    keypoints[f'{side}_ankle'][:2]
                )
                angles[f'{side}_knee_angle'] = angle

        return angles

    def _angle_to_vertical(self, point1: List[float], point2: List[float]) -> float:
        """Calculate angle of a line relative to vertical (in degrees)."""
        dx = point1[0] - point2[0]
        dy = point1[1] - point2[1]
        angle = math.degrees(math.atan2(dx, dy))
        return abs(angle)

    def _line_angle(self, left: List[float], right: List[float]) -> float:
        """Calculate angle of a line relative to horizontal (in degrees)."""
        dx = right[0] - left[0]
        dy = right[1] - left[1]
        angle = math.degrees(math.atan2(dy, dx))
        return abs(angle)

    def _joint_angle(
        self,
        point1: List[float],
        point2: List[float],
        point3: List[float]
    ) -> float:
        """Calculate angle at a joint (point2) between two segments (in degrees)."""
        v1 = np.array([point1[0] - point2[0], point1[1] - point2[1]])
        v2 = np.array([point3[0] - point2[0], point3[1] - point2[1]])

        cos_angle = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2) + 1e-6)
        angle = math.degrees(math.acos(np.clip(cos_angle, -1.0, 1.0)))

        return angle

    def _midpoint(self, point1: List[float], point2: List[float]) -> List[float]:
        """Calculate midpoint between two points."""
        return [(point1[0] + point2[0]) / 2, (point1[1] + point2[1]) / 2]

    def _draw_pose(
        self,
        image: np.ndarray,
        keypoints: Dict[str, List[float]],
        line_color: Tuple[int, int, int] = (0, 255, 0),
        point_color: Tuple[int, int, int] = (0, 0, 255),
        line_thickness: int = 2,
        point_radius: int = 5,
        confidence_threshold: float = 0.5
    ) -> np.ndarray:
        """Draw skeleton and keypoints on image."""
        # Draw connections
        for start, end in self.SKELETON_CONNECTIONS:
            if start in keypoints and end in keypoints:
                if keypoints[start][2] > confidence_threshold and keypoints[end][2] > confidence_threshold:
                    pt1 = (int(keypoints[start][0]), int(keypoints[start][1]))
                    pt2 = (int(keypoints[end][0]), int(keypoints[end][1]))
                    cv2.line(image, pt1, pt2, line_color, line_thickness)

        # Draw keypoints
        for name, (x, y, conf) in keypoints.items():
            if conf > confidence_threshold:
                cv2.circle(image, (int(x), int(y)), point_radius, point_color, -1)

        return image
