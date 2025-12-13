# CAEMA Utils

A collection of reusable Python modules for AI services.

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Available Modules

| Module | Description | Status |
|--------|-------------|--------|
| `pose_estimation` | Body keypoint detection using YOLOv8 | Stable (v0.2.0) |

---

## Installation

### Step-by-Step Install (Recommended)

Run these commands **one by one**:

```bash
# Step 1: Install the package with all dependencies
pip install "caema-utils[all]"

# Step 2: Fix OpenCV for headless servers (Codespaces, Docker, cloud VMs)
pip uninstall opencv-python opencv-python-headless -y
pip install opencv-python-headless --force-reinstall --no-deps

# Step 3: Verify installation
pose-server --check
```

You should see: `All dependencies OK!`

### Quick Install (One Command)

```bash
pip install "caema-utils[all]" && pip uninstall opencv-python opencv-python-headless -y && pip install opencv-python-headless --force-reinstall --no-deps && pose-server --check
```

### Troubleshooting

If you see `libGL.so.1: cannot open shared object file` or `No module named 'cv2'`:
```bash
pip uninstall opencv-python opencv-python-headless -y
pip install opencv-python-headless --force-reinstall --no-deps
```

### From GitHub

```bash
pip install "caema-utils[all] @ git+https://github.com/msorozabal/Utils.git"
pip uninstall opencv-python opencv-python-headless -y
pip install opencv-python-headless --force-reinstall --no-deps
pose-server --check
```

---

## Pose Estimation Module

Body keypoint detection using YOLOv8.

### Features

- Detects 17 body keypoints (COCO format)
- Calculates angles between body segments
- Returns annotated images with skeleton overlay
- Multiple input formats: file path, bytes, numpy array
- Multiple output formats: bytes, base64, numpy array, file

### Quick Start

```python
from caema_utils.pose_estimation import PoseEstimator

# Initialize (downloads model on first run)
estimator = PoseEstimator(model_size="nano")

# Detect keypoints from file
result = estimator.analyze("photo.jpg")

if result['success']:
    print(f"Confidence: {result['confidence']:.1%}")
    print(f"Keypoints: {result['keypoints']}")
    print(f"Angles: {result['angles']}")

    # Save annotated image
    with open("output.png", "wb") as f:
        f.write(result['annotated_image_bytes'])
```

### Model Sizes

| Size | Model | Speed | Accuracy | Use Case |
|------|-------|-------|----------|----------|
| `nano` | yolov8n-pose | Fastest | Good | Real-time, mobile |
| `small` | yolov8s-pose | Fast | Better | Balanced |
| `medium` | yolov8m-pose | Medium | High | Production |
| `large` | yolov8l-pose | Slow | Higher | Quality-critical |
| `xlarge` | yolov8x-pose | Slowest | Highest | Research |

### API Reference

#### `PoseEstimator`

```python
class PoseEstimator:
    def __init__(self, model_size: str = "nano"):
        """
        Initialize pose estimator.

        Args:
            model_size: "nano", "small", "medium", "large", or "xlarge"
        """

    def analyze(
        self,
        image: Union[str, Path, bytes],
        output_format: str = "bytes",
        save_path: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Detect body keypoints from image.

        Args:
            image: Path to image file or image bytes
            output_format: "bytes", "base64", "array", or "file"
            save_path: If output_format="file", save path for annotated image

        Returns:
            {
                'success': bool,
                'keypoints': Dict[str, List[float]],  # name -> [x, y, confidence]
                'angles': Dict[str, float],  # angle_name -> degrees
                'confidence': float,  # 0-1
                'annotated_image_*': ...,  # Image in requested format
            }
        """
```

#### Response Structure

```python
{
    'success': True,
    'keypoints': {
        'nose': [256.5, 128.3, 0.95],
        'left_shoulder': [200.1, 180.2, 0.92],
        'right_shoulder': [312.8, 178.9, 0.93],
        # ... 17 keypoints total
    },
    'angles': {
        'neck_angle': 5.2,
        'shoulder_line_angle': 3.1,
        'hip_line_angle': 2.8,
        'torso_angle': 4.5,
        'left_elbow_angle': 165.3,
        'right_elbow_angle': 168.7,
        'left_knee_angle': 175.2,
        'right_knee_angle': 176.8,
    },
    'confidence': 0.93,
    'annotated_image_bytes': b'...',  # PNG image with skeleton overlay
}
```

---

## HTTP API Server

The module includes a built-in FastAPI server for HTTP access.

### Start the Server

```bash
# Check dependencies first
pose-server --check

# Start server (localhost only)
pose-server --port 8005

# Accept connections from other machines
pose-server --host 0.0.0.0 --port 8005

# With auto-reload for development
pose-server --host 0.0.0.0 --port 8005 --reload
```

### API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | API info |
| `/health` | GET | Health check |
| `/detect` | POST | Full detection (JSON + base64 image) |
| `/detect/image` | POST | Returns annotated image directly |
| `/detect/json-only` | POST | Detection without image |
| `/docs` | GET | OpenAPI documentation |

### curl Examples

```bash
# Health check
curl http://localhost:8005/health

# Full detection with annotated image (base64)
curl -X POST "http://localhost:8005/detect" \
     -H "accept: application/json" \
     -F "file=@photo.jpg"

# Get annotated image directly (save to file)
curl -X POST "http://localhost:8005/detect/image" \
     -F "file=@photo.jpg" \
     --output annotated.png

# JSON only (faster, no image)
curl -X POST "http://localhost:8005/detect/json-only" \
     -F "file=@photo.jpg"
```

### Response Example

```json
{
  "success": true,
  "filename": "photo.jpg",
  "keypoints": {
    "nose": [256.5, 128.3, 0.95],
    "left_shoulder": [200.1, 180.2, 0.92]
  },
  "angles": {
    "neck_angle": 5.2,
    "shoulder_line_angle": 3.1
  },
  "confidence": 0.93,
  "annotated_image_base64": "iVBORw0KGgoAAAANS..."
}
```

---

## Keypoint Reference

The module detects 17 body keypoints in COCO format:

| Index | Name | Description |
|-------|------|-------------|
| 0 | nose | Nose tip |
| 1 | left_eye | Left eye |
| 2 | right_eye | Right eye |
| 3 | left_ear | Left ear |
| 4 | right_ear | Right ear |
| 5 | left_shoulder | Left shoulder |
| 6 | right_shoulder | Right shoulder |
| 7 | left_elbow | Left elbow |
| 8 | right_elbow | Right elbow |
| 9 | left_wrist | Left wrist |
| 10 | right_wrist | Right wrist |
| 11 | left_hip | Left hip |
| 12 | right_hip | Right hip |
| 13 | left_knee | Left knee |
| 14 | right_knee | Right knee |
| 15 | left_ankle | Left ankle |
| 16 | right_ankle | Right ankle |

---

## Calculated Angles

| Angle | Description |
|-------|-------------|
| `neck_angle` | Angle of nose-to-mid-shoulder line relative to vertical |
| `shoulder_line_angle` | Angle of shoulder line relative to horizontal |
| `hip_line_angle` | Angle of hip line relative to horizontal |
| `torso_angle` | Angle of mid-shoulder-to-mid-hip line relative to vertical |
| `left_elbow_angle` | Angle at left elbow joint |
| `right_elbow_angle` | Angle at right elbow joint |
| `left_knee_angle` | Angle at left knee joint |
| `right_knee_angle` | Angle at right knee joint |

---

## Development

### Running Tests

```bash
# Install dev dependencies
pip install -e ".[all,dev]"

# Run tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=caema_utils --cov-report=term-missing
```

### Code Quality

```bash
# Format code
black src/ tests/

# Lint
ruff src/ tests/

# Type check
mypy src/
```

---

## Requirements

- Python 3.9+
- For pose estimation:
  - numpy < 2.0.0
  - ultralytics >= 8.1.0
  - opencv-python-headless >= 4.9.0
- For HTTP server:
  - fastapi >= 0.100.0
  - uvicorn >= 0.23.0
  - python-multipart >= 0.0.6

---

## License

MIT License - see [LICENSE](LICENSE) file.

---

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## Support

- Issues: [GitHub Issues](https://github.com/msorozabal/Utils/issues)
- Documentation: [GitHub Wiki](https://github.com/msorozabal/Utils/wiki)
