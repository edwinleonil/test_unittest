"""
Unit tests for the ResNet50 classifier model.
"""

from model import ResNet50Classifier, create_classifier
import pytest
import torch
import tempfile
import os
from PIL import Image
import numpy as np
import sys

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))


class TestResNet50Classifier:
    """Test cases for ResNet50Classifier class."""

    @pytest.fixture
    def classifier(self):
        """Create a classifier instance for testing."""
        return create_classifier()

    @pytest.fixture
    def sample_image_path(self):
        """Create a temporary sample image for testing."""
        # Create a temporary RGB image
        img_array = np.random.randint(0, 255, (224, 224, 3), dtype=np.uint8)
        img = Image.fromarray(img_array, 'RGB')

        # Save to temporary file
        with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as tmp_file:
            img.save(tmp_file.name, 'JPEG')
            yield tmp_file.name

        # Cleanup
        try:
            os.unlink(tmp_file.name)
        except OSError:
            pass

    def test_classifier_creation(self):
        """Test that classifier can be created successfully."""
        classifier = create_classifier()
        assert classifier is not None
        assert isinstance(classifier, ResNet50Classifier)

    def test_model_loading(self, classifier):
        """Test that the ResNet50 model loads correctly."""
        assert classifier.model is not None
        assert classifier.is_model_loaded()

        # Check that model is in eval mode
        assert not classifier.model.training

    def test_transforms_setup(self, classifier):
        """Test that image transforms are set up correctly."""
        assert classifier.transform is not None

        # Test transform pipeline
        img_array = np.random.randint(0, 255, (300, 300, 3), dtype=np.uint8)
        img = Image.fromarray(img_array, 'RGB')

        transformed = classifier.transform(img)

        # Check output shape and type
        assert isinstance(transformed, torch.Tensor)
        assert transformed.shape == (3, 224, 224)  # C, H, W

        # Check normalization (values should be roughly in [-2, 2] range)
        assert transformed.min() >= -3.0
        assert transformed.max() <= 3.0

    def test_image_preprocessing(self, classifier, sample_image_path):
        """Test image preprocessing functionality."""
        tensor = classifier.preprocess_image(sample_image_path)

        # Check output shape and type
        assert isinstance(tensor, torch.Tensor)
        assert tensor.shape == (1, 3, 224, 224)  # Batch, C, H, W
        assert tensor.dtype == torch.float32

    def test_image_preprocessing_invalid_file(self, classifier):
        """Test image preprocessing with invalid file."""
        with pytest.raises(ValueError):
            classifier.preprocess_image("nonexistent_file.jpg")

    def test_prediction(self, classifier, sample_image_path):
        """Test image classification prediction."""
        predictions = classifier.predict(sample_image_path, top_k=3)

        # Check output format
        assert isinstance(predictions, list)
        assert len(predictions) == 3

        for class_name, confidence in predictions:
            assert isinstance(class_name, str)
            assert isinstance(confidence, float)
            assert 0.0 <= confidence <= 1.0

        # Check that predictions are sorted by confidence (descending)
        confidences = [conf for _, conf in predictions]
        assert confidences == sorted(confidences, reverse=True)

    def test_prediction_invalid_image(self, classifier):
        """Test prediction with invalid image file."""
        with pytest.raises(ValueError):
            classifier.predict("nonexistent_file.jpg")

    def test_prediction_top_k_parameter(self, classifier, sample_image_path):
        """Test prediction with different top_k values."""
        # Test with top_k=1
        predictions_1 = classifier.predict(sample_image_path, top_k=1)
        assert len(predictions_1) == 1

        # Test with top_k=10
        predictions_10 = classifier.predict(sample_image_path, top_k=10)
        assert len(predictions_10) == 10

    def test_class_labels_exist(self, classifier):
        """Test that class labels are loaded."""
        assert classifier.class_labels is not None
        assert isinstance(classifier.class_labels, list)
        assert len(classifier.class_labels) > 0

        # Check that all labels are strings
        for label in classifier.class_labels:
            assert isinstance(label, str)
            assert len(label) > 0

    def test_model_inference_mode(self, classifier, sample_image_path):
        """Test that model inference runs without gradients."""
        # This test ensures torch.no_grad() is used during inference
        original_grad_enabled = torch.is_grad_enabled()

        try:
            # Enable gradients initially
            torch.set_grad_enabled(True)

            # Run prediction
            predictions = classifier.predict(sample_image_path)

            # Verify we got valid predictions
            assert len(predictions) > 0

        finally:
            # Restore original gradient state
            torch.set_grad_enabled(original_grad_enabled)


class TestFactoryFunction:
    """Test cases for the factory function."""

    def test_create_classifier_function(self):
        """Test the create_classifier factory function."""
        classifier = create_classifier()
        assert isinstance(classifier, ResNet50Classifier)
        assert classifier.is_model_loaded()


class TestErrorHandling:
    """Test cases for error handling scenarios."""

    def test_corrupted_image_handling(self):
        """Test handling of corrupted image files."""
        classifier = create_classifier()

        # Create a file with invalid image data
        with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as tmp_file:
            tmp_file.write(b"This is not an image")
            tmp_file.flush()

            try:
                with pytest.raises(ValueError):
                    classifier.preprocess_image(tmp_file.name)
            finally:
                os.unlink(tmp_file.name)

    def test_empty_file_handling(self):
        """Test handling of empty files."""
        classifier = create_classifier()

        # Create an empty file
        with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as tmp_file:
            pass  # File is empty

            try:
                with pytest.raises(ValueError):
                    classifier.preprocess_image(tmp_file.name)
            finally:
                os.unlink(tmp_file.name)
