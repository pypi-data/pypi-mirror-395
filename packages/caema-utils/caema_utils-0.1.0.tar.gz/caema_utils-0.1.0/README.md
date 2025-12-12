# CAEMA Utils

**System Dependency Manager** - A collection of reusable Python modules for AI services.

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Available Modules

| Module | Description | Status |
|--------|-------------|--------|
| `pose_estimation` | AI-powered body pose analysis using YOLOv8 | Stable |

---

## Installation

### From GitHub (Recommended)

```bash
# Install with pose estimation dependencies
pip install "caema-utils[pose] @ git+https://github.com/caema-solutions/Utils.git"

# Install with all dependencies (pose + server)
pip install "caema-utils[all] @ git+https://github.com/caema-solutions/Utils.git"

# Install core only (no heavy dependencies)
pip install git+https://github.com/caema-solutions/Utils.git
```

### For Development

```bash
git clone https://github.com/msorozabal/Utils.git
cd Utils
pip install -e ".[all,dev]"
```

---

## Pose Estimation Module

AI-powered body pose analysis using YOLOv8 for biomechanical evaluation.

### Features

- Detects 17 body keypoints (COCO format)
- Calculates biomechanical angles (neck, shoulders, spine, knees, etc.)
- Generates text analysis of postural findings
- Returns annotated images with skeleton overlay
- Multiple input formats: file path, bytes, numpy array
- Multiple output formats: bytes, base64, numpy array, file

### Quick Start

```python
from caema_utils.pose_estimation import PoseEstimator

# Initialize (downloads model on first run)
estimator = PoseEstimator(model_size="nano")

# Analyze from file
result = estimator.analyze("photo.jpg")

if result['success']:
    print(f"Confidence: {result['confidence']:.1%}")
    print(f"Analysis:\n{result['analysis']}")

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
        Analyze body posture from image.

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
                'analysis': str,  # Text analysis
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
        'neck_tilt': 5.2,
        'shoulder_angle': 3.1,
        'hip_angle': 2.8,
        'spine_angle': 4.5,
        'left_elbow': 165.3,
        'right_elbow': 168.7,
        'left_knee': 175.2,
        'right_knee': 176.8,
    },
    'confidence': 0.93,
    'analysis': 'OK: Body alignment within normal parameters\nOK: No significant postural deviations detected',
    'annotated_image_bytes': b'...',  # PNG image with skeleton overlay
}
```

---

## HTTP API Server

The module includes a built-in FastAPI server for HTTP access.

### Start the Server

```bash
# After installation
pose-server --port 8005

# Or with uvicorn directly
uvicorn caema_utils.pose_estimation.server:app --port 8005
```

### API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | API info |
| `/health` | GET | Health check |
| `/analyze` | POST | Full analysis (JSON + base64 image) |
| `/analyze/image` | POST | Returns annotated image directly |
| `/analyze/json-only` | POST | Analysis without image |
| `/docs` | GET | OpenAPI documentation |

### curl Examples

```bash
# Full analysis with annotated image (base64)
curl -X POST "http://localhost:8005/analyze" \
     -H "accept: application/json" \
     -F "file=@photo.jpg"

# Get annotated image directly (save to file)
curl -X POST "http://localhost:8005/analyze/image" \
     -F "file=@photo.jpg" \
     --output annotated.png

# JSON only (faster, no image)
curl -X POST "http://localhost:8005/analyze/json-only" \
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
    "neck_tilt": 5.2,
    "shoulder_angle": 3.1
  },
  "confidence": 0.93,
  "analysis": "OK: Body alignment within normal parameters",
  "annotated_image_base64": "iVBORw0KGgoAAAANS..."
}
```

---

## Integration Examples

### FastAPI Integration

```python
from fastapi import FastAPI, File, UploadFile
from caema_utils.pose_estimation import PoseEstimator

app = FastAPI()
estimator = PoseEstimator(model_size="nano")

@app.post("/api/analyze")
async def analyze(file: UploadFile = File(...)):
    content = await file.read()
    result = estimator.analyze(content, output_format="base64")
    return result
```

### Flask Integration

```python
from flask import Flask, request, jsonify
from caema_utils.pose_estimation import PoseEstimator

app = Flask(__name__)
estimator = PoseEstimator(model_size="nano")

@app.route('/analyze', methods=['POST'])
def analyze():
    file = request.files['image']
    result = estimator.analyze(file.read())
    return jsonify(result)
```

### Async Usage

```python
import asyncio
from concurrent.futures import ThreadPoolExecutor
from caema_utils.pose_estimation import PoseEstimator

estimator = PoseEstimator()
executor = ThreadPoolExecutor(max_workers=4)

async def analyze_async(image_bytes):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(
        executor,
        estimator.analyze,
        image_bytes
    )
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

| Angle | Description | Normal Range |
|-------|-------------|--------------|
| `neck_tilt` | Head tilt from vertical | < 10° |
| `shoulder_angle` | Shoulder level asymmetry | < 5° |
| `hip_angle` | Hip level asymmetry | < 5° |
| `spine_angle` | Spinal lateral deviation | < 8° |
| `left_elbow` | Left elbow flexion | 0-180° |
| `right_elbow` | Right elbow flexion | 0-180° |
| `left_knee` | Left knee flexion | 160-190° |
| `right_knee` | Right knee flexion | 160-190° |

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
