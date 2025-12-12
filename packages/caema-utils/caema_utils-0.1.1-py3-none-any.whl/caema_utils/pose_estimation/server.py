"""
FastAPI server for pose estimation.
Provides HTTP API for analyzing images and receiving annotated results.

Run with:
    uvicorn caema_utils.pose_estimation.server:app --reload --port 8005

Or use the CLI:
    pose-server
"""

import io
import base64
from typing import Optional
from fastapi import FastAPI, File, UploadFile, HTTPException, Query
from fastapi.responses import Response, JSONResponse

# Lazy import to avoid loading heavy dependencies at import time
_estimator = None


def get_estimator():
    """Lazy load the pose estimator."""
    global _estimator
    if _estimator is None:
        from .estimator import PoseEstimator
        _estimator = PoseEstimator(model_size="nano")
    return _estimator


app = FastAPI(
    title="Pose Estimation API",
    description="AI-powered body pose analysis using YOLOv8",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)


@app.get("/")
async def root():
    """Root endpoint with API info."""
    return {
        "service": "Pose Estimation API",
        "version": "0.1.0",
        "endpoints": {
            "POST /analyze": "Analyze image and get JSON response with base64 annotated image",
            "POST /analyze/image": "Analyze image and get annotated image directly (PNG)",
            "GET /health": "Health check endpoint",
            "GET /docs": "OpenAPI documentation",
        }
    }


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "pose-estimation",
        "model_loaded": _estimator is not None
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

    Example with curl:
    ```bash
    curl -X POST "http://localhost:8005/analyze" \\
         -H "accept: application/json" \\
         -F "file=@photo.jpg"
    ```
    """
    # Validate file type
    allowed_types = {"image/png", "image/jpeg", "image/jpg"}
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type: {file.content_type}. Allowed: {allowed_types}"
        )

    try:
        # Read file content
        content = await file.read()

        # Get estimator and analyze
        estimator = get_estimator()
        output_format = "base64" if include_image else "bytes"
        result = estimator.analyze(content, output_format=output_format)

        if not result['success']:
            raise HTTPException(status_code=400, detail=result.get('error', 'Analysis failed'))

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
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis error: {str(e)}")


@app.post("/analyze/image")
async def analyze_image_direct(
    file: UploadFile = File(..., description="Image file to analyze (PNG, JPG, JPEG)")
):
    """
    Analyze body posture and return annotated image directly.

    Returns the annotated PNG image with skeleton overlay.
    Use this endpoint when you want to display the image directly.

    Example with curl:
    ```bash
    curl -X POST "http://localhost:8005/analyze/image" \\
         -F "file=@photo.jpg" \\
         --output annotated.png
    ```
    """
    # Validate file type
    allowed_types = {"image/png", "image/jpeg", "image/jpg"}
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type: {file.content_type}. Allowed: {allowed_types}"
        )

    try:
        content = await file.read()

        estimator = get_estimator()
        result = estimator.analyze(content, output_format="bytes")

        if not result['success']:
            raise HTTPException(status_code=400, detail=result.get('error', 'Analysis failed'))

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
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis error: {str(e)}")


@app.post("/analyze/json-only")
async def analyze_json_only(
    file: UploadFile = File(..., description="Image file to analyze (PNG, JPG, JPEG)")
):
    """
    Analyze body posture and return only JSON data (no image).

    Faster response as it doesn't include the base64 image.
    Use when you only need the keypoints and analysis data.

    Example with curl:
    ```bash
    curl -X POST "http://localhost:8005/analyze/json-only" \\
         -F "file=@photo.jpg"
    ```
    """
    allowed_types = {"image/png", "image/jpeg", "image/jpg"}
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type: {file.content_type}. Allowed: {allowed_types}"
        )

    try:
        content = await file.read()

        estimator = get_estimator()
        result = estimator.analyze(content, output_format="bytes")

        if not result['success']:
            raise HTTPException(status_code=400, detail=result.get('error', 'Analysis failed'))

        # Remove image from response
        result.pop('annotated_image_bytes', None)

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
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis error: {str(e)}")


def main():
    """Entry point for pose-server command."""
    import uvicorn
    import argparse

    parser = argparse.ArgumentParser(description="Pose Estimation API Server")
    parser.add_argument("--host", default="0.0.0.0", help="Host to bind (default: 0.0.0.0)")
    parser.add_argument("--port", type=int, default=8005, help="Port to bind (default: 8005)")
    parser.add_argument("--reload", action="store_true", help="Enable auto-reload")

    args = parser.parse_args()

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
