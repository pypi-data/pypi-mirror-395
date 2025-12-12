"""
FastAPI server for pose estimation.
Provides HTTP API for analyzing images and receiving annotated results.

Run with:
    uvicorn caema_utils.pose_estimation.server:app --reload --port 8005

Or use the CLI:
    pose-server
"""

import io
import sys
import base64
import logging
from typing import Optional
from fastapi import FastAPI, File, UploadFile, HTTPException, Query
from fastapi.responses import Response, JSONResponse

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("pose-server")

# Lazy import to avoid loading heavy dependencies at import time
_estimator = None
_init_error = None


def check_dependencies():
    """Check if all required dependencies are installed."""
    errors = []

    # Check cv2
    try:
        import cv2
        logger.info(f"OpenCV version: {cv2.__version__}")
    except ImportError as e:
        errors.append(f"opencv-python-headless not installed: {e}")

    # Check numpy
    try:
        import numpy as np
        logger.info(f"NumPy version: {np.__version__}")
    except ImportError as e:
        errors.append(f"numpy not installed: {e}")

    # Check ultralytics
    try:
        from ultralytics import YOLO
        logger.info("Ultralytics YOLO loaded successfully")
    except ImportError as e:
        errors.append(f"ultralytics not installed: {e}")
    except Exception as e:
        errors.append(f"ultralytics import error (likely opencv issue): {e}")

    return errors


def get_estimator():
    """Lazy load the pose estimator."""
    global _estimator, _init_error

    if _init_error:
        raise RuntimeError(_init_error)

    if _estimator is None:
        logger.info("Initializing PoseEstimator...")
        try:
            from .estimator import PoseEstimator
            _estimator = PoseEstimator(model_size="nano")
            logger.info("PoseEstimator initialized successfully")
        except ImportError as e:
            _init_error = f"Failed to import PoseEstimator: {e}. Make sure to run: pip uninstall opencv-python -y && pip install opencv-python-headless"
            logger.error(_init_error)
            raise RuntimeError(_init_error)
        except Exception as e:
            _init_error = f"Failed to initialize PoseEstimator: {e}"
            logger.error(_init_error)
            raise RuntimeError(_init_error)

    return _estimator


app = FastAPI(
    title="Pose Estimation API",
    description="AI-powered body pose analysis using YOLOv8",
    version="0.1.3",
    docs_url="/docs",
    redoc_url="/redoc",
)


@app.on_event("startup")
async def startup_event():
    """Check dependencies on startup."""
    logger.info("=" * 50)
    logger.info("Pose Estimation API Starting...")
    logger.info("=" * 50)

    errors = check_dependencies()
    if errors:
        logger.error("Dependency check failed:")
        for error in errors:
            logger.error(f"  - {error}")
        logger.error("")
        logger.error("To fix, run:")
        logger.error("  pip uninstall opencv-python -y && pip install opencv-python-headless")
    else:
        logger.info("All dependencies OK")

    logger.info("=" * 50)


@app.get("/")
async def root():
    """Root endpoint with API info."""
    return {
        "service": "Pose Estimation API",
        "version": "0.1.3",
        "endpoints": {
            "POST /analyze": "Analyze image and get JSON response with base64 annotated image",
            "POST /analyze/image": "Analyze image and get annotated image directly (PNG)",
            "POST /analyze/json-only": "Analyze image and get JSON only (no image)",
            "GET /health": "Health check endpoint",
            "GET /docs": "OpenAPI documentation",
        }
    }


@app.get("/health")
async def health():
    """Health check endpoint."""
    errors = check_dependencies()
    return {
        "status": "healthy" if not errors else "unhealthy",
        "service": "pose-estimation",
        "version": "0.1.3",
        "model_loaded": _estimator is not None,
        "dependencies_ok": len(errors) == 0,
        "errors": errors if errors else None
    }


@app.post("/analyze")
async def analyze_image(
    file: UploadFile = File(..., description="Image file to analyze (PNG, JPG, JPEG)"),
    include_image: bool = Query(True, description="Include base64 annotated image in response")
):
    """
    Analyze body posture from uploaded image.

    Returns JSON with:
    - keypoints: Detected body keypoints with coordinates and confidence
    - angles: Calculated biomechanical angles
    - confidence: Average detection confidence (0-1)
    - analysis: Text analysis of postural findings
    - annotated_image_base64: Base64-encoded annotated image (if include_image=True)
    """
    logger.info(f"POST /analyze - file: {file.filename}, content_type: {file.content_type}")

    # Validate file type
    allowed_types = {"image/png", "image/jpeg", "image/jpg"}
    if file.content_type not in allowed_types:
        logger.warning(f"Invalid file type: {file.content_type}")
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type: {file.content_type}. Allowed: {allowed_types}"
        )

    try:
        # Read file content
        content = await file.read()
        logger.info(f"Read {len(content)} bytes from {file.filename}")

        # Get estimator and analyze
        estimator = get_estimator()
        output_format = "base64" if include_image else "bytes"
        result = estimator.analyze(content, output_format=output_format)

        if not result['success']:
            logger.error(f"Analysis failed: {result.get('error')}")
            raise HTTPException(status_code=400, detail=result.get('error', 'Analysis failed'))

        logger.info(f"Analysis successful - confidence: {result['confidence']:.2f}")

        # Prepare response
        response = {
            "success": True,
            "filename": file.filename,
            "keypoints": result['keypoints'],
            "angles": result['angles'],
            "confidence": result['confidence'],
            "analysis": result['analysis'],
        }

        if include_image and 'annotated_image_base64' in result:
            response['annotated_image_base64'] = result['annotated_image_base64']

        return JSONResponse(content=response)

    except HTTPException:
        raise
    except RuntimeError as e:
        logger.error(f"Runtime error: {e}")
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail=f"Analysis error: {str(e)}")


@app.post("/analyze/image")
async def analyze_image_direct(
    file: UploadFile = File(..., description="Image file to analyze (PNG, JPG, JPEG)")
):
    """
    Analyze body posture and return annotated image directly.

    Returns the annotated PNG image with skeleton overlay.
    """
    logger.info(f"POST /analyze/image - file: {file.filename}, content_type: {file.content_type}")

    # Validate file type
    allowed_types = {"image/png", "image/jpeg", "image/jpg"}
    if file.content_type not in allowed_types:
        logger.warning(f"Invalid file type: {file.content_type}")
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type: {file.content_type}. Allowed: {allowed_types}"
        )

    try:
        content = await file.read()
        logger.info(f"Read {len(content)} bytes from {file.filename}")

        estimator = get_estimator()
        result = estimator.analyze(content, output_format="bytes")

        if not result['success']:
            logger.error(f"Analysis failed: {result.get('error')}")
            raise HTTPException(status_code=400, detail=result.get('error', 'Analysis failed'))

        logger.info(f"Analysis successful - returning annotated image")

        return Response(
            content=result['annotated_image_bytes'],
            media_type="image/png",
            headers={
                "Content-Disposition": f'inline; filename="annotated_{file.filename}"',
                "X-Confidence": str(result['confidence']),
                "X-Keypoints-Count": str(len(result['keypoints'])),
            }
        )

    except HTTPException:
        raise
    except RuntimeError as e:
        logger.error(f"Runtime error: {e}")
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail=f"Analysis error: {str(e)}")


@app.post("/analyze/json-only")
async def analyze_json_only(
    file: UploadFile = File(..., description="Image file to analyze (PNG, JPG, JPEG)")
):
    """
    Analyze body posture and return only JSON data (no image).

    Faster response as it doesn't include the base64 image.
    """
    logger.info(f"POST /analyze/json-only - file: {file.filename}, content_type: {file.content_type}")

    allowed_types = {"image/png", "image/jpeg", "image/jpg"}
    if file.content_type not in allowed_types:
        logger.warning(f"Invalid file type: {file.content_type}")
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type: {file.content_type}. Allowed: {allowed_types}"
        )

    try:
        content = await file.read()
        logger.info(f"Read {len(content)} bytes from {file.filename}")

        estimator = get_estimator()
        result = estimator.analyze(content, output_format="bytes")

        if not result['success']:
            logger.error(f"Analysis failed: {result.get('error')}")
            raise HTTPException(status_code=400, detail=result.get('error', 'Analysis failed'))

        logger.info(f"Analysis successful - confidence: {result['confidence']:.2f}")

        return JSONResponse(content={
            "success": True,
            "filename": file.filename,
            "keypoints": result['keypoints'],
            "angles": result['angles'],
            "confidence": result['confidence'],
            "analysis": result['analysis'],
        })

    except HTTPException:
        raise
    except RuntimeError as e:
        logger.error(f"Runtime error: {e}")
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail=f"Analysis error: {str(e)}")


def main():
    """Entry point for pose-server command."""
    import uvicorn
    import argparse

    parser = argparse.ArgumentParser(description="Pose Estimation API Server")
    parser.add_argument("--host", default="0.0.0.0", help="Host to bind (default: 0.0.0.0)")
    parser.add_argument("--port", type=int, default=8005, help="Port to bind (default: 8005)")
    parser.add_argument("--reload", action="store_true", help="Enable auto-reload")
    parser.add_argument("--check", action="store_true", help="Check dependencies and exit")

    args = parser.parse_args()

    # Check dependencies mode
    if args.check:
        print("Checking dependencies...")
        errors = check_dependencies()
        if errors:
            print("\nERRORS FOUND:")
            for error in errors:
                print(f"  - {error}")
            print("\nTo fix, run:")
            print("  pip uninstall opencv-python -y && pip install opencv-python-headless")
            sys.exit(1)
        else:
            print("All dependencies OK!")
            sys.exit(0)

    print(f"Starting Pose Estimation API on http://{args.host}:{args.port}")
    print(f"Documentation available at http://{args.host}:{args.port}/docs")

    uvicorn.run(
        "caema_utils.pose_estimation.server:app",
        host=args.host,
        port=args.port,
        reload=args.reload
    )


if __name__ == "__main__":
    main()
