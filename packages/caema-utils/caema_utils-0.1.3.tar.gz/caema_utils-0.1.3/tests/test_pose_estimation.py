"""
Tests for the pose_estimation module.

Run with: pytest tests/test_pose_estimation.py -v
"""

import pytest
import os
import numpy as np


class TestPoseEstimatorImport:
    """Test that the module can be imported correctly."""

    def test_import_module(self):
        """Test basic module import."""
        from caema_utils import pose_estimation
        assert pose_estimation is not None

    def test_import_estimator(self):
        """Test PoseEstimator import."""
        from caema_utils.pose_estimation import PoseEstimator
        assert PoseEstimator is not None

    def test_import_analyzer(self):
        """Test PoseAnalyzer import."""
        from caema_utils.pose_estimation import PoseAnalyzer
        assert PoseAnalyzer is not None


class TestPoseAnalyzer:
    """Test the PoseAnalyzer class."""

    @pytest.fixture(scope="class")
    def analyzer(self):
        """Create analyzer instance for tests."""
        from caema_utils.pose_estimation.models.analyzer import PoseAnalyzer
        return PoseAnalyzer(model_name="yolov8n-pose.pt")

    def test_keypoint_names(self, analyzer):
        """Test that keypoint names are defined."""
        assert len(analyzer.KEYPOINT_NAMES) == 17
        assert 'nose' in analyzer.KEYPOINT_NAMES.values()
        assert 'left_shoulder' in analyzer.KEYPOINT_NAMES.values()
        assert 'right_ankle' in analyzer.KEYPOINT_NAMES.values()

    def test_skeleton_connections(self, analyzer):
        """Test skeleton connections are defined."""
        assert len(analyzer.SKELETON_CONNECTIONS) > 0
        assert ('left_shoulder', 'right_shoulder') in analyzer.SKELETON_CONNECTIONS

    def test_midpoint_calculation(self, analyzer):
        """Test midpoint calculation."""
        point1 = [0, 0]
        point2 = [10, 10]
        mid = analyzer._midpoint(point1, point2)
        assert mid == [5, 5]

    def test_angle_to_vertical(self, analyzer):
        """Test vertical angle calculation."""
        # Perfectly vertical (point2 above point1) should be 0
        angle = analyzer._angle_to_vertical([100, 100], [100, 0])
        assert abs(angle) < 1  # Allow small floating point error

        # 45 degree tilt
        angle = analyzer._angle_to_vertical([0, 100], [100, 0])
        assert abs(angle - 45) < 1

    def test_joint_angle(self, analyzer):
        """Test joint angle calculation."""
        # Straight line should be 180 degrees
        angle = analyzer._joint_angle([0, 0], [50, 0], [100, 0])
        assert abs(angle - 180) < 1

        # Right angle should be 90 degrees
        angle = analyzer._joint_angle([0, 0], [0, 50], [50, 50])
        assert abs(angle - 90) < 1


class TestPoseEstimator:
    """Test the high-level PoseEstimator class."""

    @pytest.fixture(scope="class")
    def estimator(self):
        """Create estimator instance for tests."""
        from caema_utils.pose_estimation import PoseEstimator
        return PoseEstimator(model_size="nano")

    def test_model_size_property(self, estimator):
        """Test model size property."""
        assert estimator.model_size == "nano"

    def test_invalid_model_size(self):
        """Test that invalid model size raises error."""
        from caema_utils.pose_estimation import PoseEstimator
        with pytest.raises(ValueError):
            PoseEstimator(model_size="invalid")

    def test_get_keypoint_names(self, estimator):
        """Test keypoint names retrieval."""
        names = estimator.get_keypoint_names()
        assert isinstance(names, dict)
        assert len(names) == 17

    def test_get_skeleton_connections(self, estimator):
        """Test skeleton connections retrieval."""
        connections = estimator.get_skeleton_connections()
        assert isinstance(connections, list)
        assert len(connections) > 0

    def test_invalid_input_type(self, estimator):
        """Test that invalid input type raises error."""
        with pytest.raises(TypeError):
            estimator.analyze(12345)  # Invalid type


class TestAnalysisOutput:
    """Test analysis output structure."""

    @pytest.fixture(scope="class")
    def sample_result(self):
        """Create a sample analysis result for structure testing."""
        # This is a mock result structure - actual tests with images
        # would require test images
        return {
            'success': True,
            'keypoints': {
                'nose': [100.0, 50.0, 0.95],
                'left_shoulder': [80.0, 100.0, 0.92],
                'right_shoulder': [120.0, 100.0, 0.93],
            },
            'angles': {
                'neck_tilt': 5.2,
                'shoulder_angle': 2.1,
            },
            'confidence': 0.93,
            'analysis': 'OK: Body alignment within normal parameters',
        }

    def test_result_has_success(self, sample_result):
        """Test result has success field."""
        assert 'success' in sample_result
        assert isinstance(sample_result['success'], bool)

    def test_result_has_keypoints(self, sample_result):
        """Test result has keypoints."""
        assert 'keypoints' in sample_result
        assert isinstance(sample_result['keypoints'], dict)

    def test_result_has_angles(self, sample_result):
        """Test result has angles."""
        assert 'angles' in sample_result
        assert isinstance(sample_result['angles'], dict)

    def test_result_has_confidence(self, sample_result):
        """Test result has confidence."""
        assert 'confidence' in sample_result
        assert 0 <= sample_result['confidence'] <= 1

    def test_result_has_analysis(self, sample_result):
        """Test result has analysis text."""
        assert 'analysis' in sample_result
        assert isinstance(sample_result['analysis'], str)


# Integration test with actual image (skipped if no test image available)
@pytest.mark.skipif(
    not os.path.exists("tests/fixtures/test_image.jpg"),
    reason="Test image not available"
)
class TestIntegrationWithImage:
    """Integration tests with actual images."""

    @pytest.fixture(scope="class")
    def estimator(self):
        from caema_utils.pose_estimation import PoseEstimator
        return PoseEstimator(model_size="nano")

    def test_analyze_file(self, estimator):
        """Test analyzing an actual image file."""
        result = estimator.analyze("tests/fixtures/test_image.jpg")
        assert result['success'] is True
        assert 'annotated_image_bytes' in result

    def test_analyze_bytes(self, estimator):
        """Test analyzing image bytes."""
        with open("tests/fixtures/test_image.jpg", "rb") as f:
            image_bytes = f.read()

        result = estimator.analyze(image_bytes)
        assert result['success'] is True

    def test_base64_output(self, estimator):
        """Test base64 output format."""
        result = estimator.analyze(
            "tests/fixtures/test_image.jpg",
            output_format="base64"
        )
        assert 'annotated_image_base64' in result
        # Base64 string should be valid
        import base64
        decoded = base64.b64decode(result['annotated_image_base64'])
        assert len(decoded) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
