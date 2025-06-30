"""
PyTorch ResNet50 Image Classifier Module

This module provides functionality for loading a pre-trained ResNet50 model
and performing image classification with proper preprocessing.
"""

import torch
import torchvision.models as models
import torchvision.transforms as transforms
from PIL import Image
import torch.nn.functional as F
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ResNet50Classifier:
    """
    A wrapper class for PyTorch ResNet50 model with image preprocessing
    and classification functionality.
    """

    def __init__(self):
        """Initialize the ResNet50 classifier."""
        self.model = None
        self.transform = None
        self.class_labels = None
        self._setup_model()
        self._setup_transforms()
        self._load_imagenet_labels()

    def _setup_model(self):
        """Load and configure the pre-trained ResNet50 model."""
        try:
            logger.info("Loading pre-trained ResNet50 model...")
            self.model = models.resnet50(weights=models.ResNet50_Weights.IMAGENET1K_V1)
            self.model.eval()  # Set to evaluation mode
            logger.info("Model loaded successfully")
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            raise

    def _setup_transforms(self):
        """Set up image preprocessing transforms."""
        # Standard ImageNet preprocessing
        self.transform = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225]
            )
        ])

    def _load_imagenet_labels(self):
        """Load ImageNet class labels."""
        # Simplified subset of ImageNet classes for demonstration
        # In a real application, you might load this from a file
        self.class_labels = [
            "tench", "goldfish", "great white shark", "tiger shark",
            "hammerhead", "electric ray", "stingray", "cock", "hen",
            "ostrich", "brambling", "goldfinch", "house finch",
            "junco", "indigo bunting", "robin", "bulbul", "jay",
            "magpie", "chickadee", "water ouzel", "kite", "bald eagle",
            "vulture", "great grey owl", "European fire salamander",
            "common newt", "eft", "spotted salamander", "axolotl"
        ]
        # Note: This is just a sample. The full ImageNet has 1000 classes.
        # For a complete implementation, load from imagenet_classes.txt

    def preprocess_image(self, image_path):
        """
        Preprocess an image for ResNet50 input.

        Args:
            image_path (str): Path to the image file

        Returns:
            torch.Tensor: Preprocessed image tensor

        Raises:
            ValueError: If image cannot be loaded or processed
        """
        try:
            # Load image
            image = Image.open(image_path).convert('RGB')

            # Apply transforms
            image_tensor = self.transform(image)

            # Add batch dimension
            image_tensor = image_tensor.unsqueeze(0)

            return image_tensor

        except Exception as e:
            logger.error(f"Error preprocessing image {image_path}: {e}")
            raise ValueError(f"Cannot process image: {e}")

    def predict(self, image_path, top_k=5):
        """
        Perform image classification on a single image.

        Args:
            image_path (str): Path to the image file
            top_k (int): Number of top predictions to return

        Returns:
            list: List of tuples (class_name, confidence_score)

        Raises:
            ValueError: If prediction fails
        """
        try:
            # Preprocess image
            image_tensor = self.preprocess_image(image_path)

            # Perform inference
            with torch.no_grad():
                outputs = self.model(image_tensor)
                probabilities = F.softmax(outputs, dim=1)

                # Get top-k predictions
                top_prob, top_class = torch.topk(probabilities, top_k)

                # Convert to human-readable format
                predictions = []
                for i in range(top_k):
                    class_idx = top_class[0][i].item()
                    confidence = top_prob[0][i].item()

                    # Use class label if available, otherwise use index
                    if class_idx < len(self.class_labels):
                        class_name = self.class_labels[class_idx]
                    else:
                        class_name = f"Class_{class_idx}"

                    predictions.append((class_name, confidence))

                return predictions

        except Exception as e:
            logger.error(f"Error during prediction: {e}")
            raise ValueError(f"Prediction failed: {e}")

    def is_model_loaded(self):
        """Check if the model is properly loaded."""
        return self.model is not None


def create_classifier():
    """
    Factory function to create a ResNet50Classifier instance.

    Returns:
        ResNet50Classifier: Initialized classifier instance
    """
    return ResNet50Classifier()
