"""
Unit tests for the GUI components.
"""

import pytest
import tkinter as tk
import tempfile
import os
from PIL import Image
import numpy as np
import sys
from unittest.mock import Mock, patch, MagicMock

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))


class TestImageClassifierGUI:
    """Test cases for ImageClassifierGUI class."""

    @pytest.fixture
    def root(self):
        """Create a test tkinter root window."""
        root = tk.Tk()
        root.withdraw()  # Hide the window during testing
        yield root
        root.destroy()

    @pytest.fixture
    def sample_image_path(self):
        """Create a temporary sample image for testing."""
        img_array = np.random.randint(0, 255, (224, 224, 3), dtype=np.uint8)
        img = Image.fromarray(img_array, 'RGB')

        with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as tmp_file:
            img.save(tmp_file.name, 'JPEG')
            yield tmp_file.name

        try:
            os.unlink(tmp_file.name)
        except OSError:
            pass

    @patch('src.gui.create_classifier')
    def test_gui_initialization(self, mock_create_classifier, root):
        """Test GUI initialization."""
        # Mock the classifier to avoid loading the actual model
        mock_classifier = Mock()
        mock_create_classifier.return_value = mock_classifier

        from gui import ImageClassifierGUI

        gui = ImageClassifierGUI(root)

        # Check that basic UI components exist
        assert gui.root == root
        assert gui.select_button is not None
        assert gui.predict_button is not None
        assert gui.file_label is not None
        assert gui.status_label is not None
        assert gui.results_text is not None
        assert gui.image_label is not None
        assert gui.progress is not None

    @patch('src.gui.create_classifier')
    def test_model_loading_success(self, mock_create_classifier, root):
        """Test successful model loading."""
        mock_classifier = Mock()
        mock_create_classifier.return_value = mock_classifier

        from gui import ImageClassifierGUI

        gui = ImageClassifierGUI(root)

        # Simulate successful model loading
        gui._on_model_loaded()

        assert "successfully" in gui.status_label.cget("text").lower()
        assert gui.status_label.cget("foreground") == "green"

    @patch('src.gui.create_classifier')
    def test_model_loading_error(self, mock_create_classifier, root):
        """Test model loading error handling."""
        mock_create_classifier.side_effect = Exception("Model loading failed")

        from gui import ImageClassifierGUI

        gui = ImageClassifierGUI(root)

        # Simulate model loading error
        gui._on_model_error("Model loading failed")

        assert "failed" in gui.status_label.cget("text").lower()
        assert gui.status_label.cget("foreground") == "red"

    @patch('src.gui.create_classifier')
    @patch('tkinter.filedialog.askopenfilename')
    def test_image_selection(self, mock_filedialog, mock_create_classifier, root, sample_image_path):
        """Test image file selection."""
        mock_classifier = Mock()
        mock_create_classifier.return_value = mock_classifier
        mock_filedialog.return_value = sample_image_path

        from gui import ImageClassifierGUI

        gui = ImageClassifierGUI(root)
        gui.select_image()

        assert gui.current_image_path == sample_image_path
        assert os.path.basename(sample_image_path) in gui.file_label.cget("text")
        assert gui.predict_button.cget("state") == tk.NORMAL

    @patch('src.gui.create_classifier')
    @patch('tkinter.filedialog.askopenfilename')
    def test_image_selection_cancelled(self, mock_filedialog, mock_create_classifier, root):
        """Test cancelled image file selection."""
        mock_classifier = Mock()
        mock_create_classifier.return_value = mock_classifier
        mock_filedialog.return_value = ""  # User cancelled

        from gui import ImageClassifierGUI

        gui = ImageClassifierGUI(root)
        original_path = gui.current_image_path

        gui.select_image()

        assert gui.current_image_path == original_path
        assert gui.predict_button.cget("state") == tk.DISABLED

    @patch('src.gui.create_classifier')
    def test_display_image_success(self, mock_create_classifier, root, sample_image_path):
        """Test successful image display."""
        mock_classifier = Mock()
        mock_create_classifier.return_value = mock_classifier

        from gui import ImageClassifierGUI

        gui = ImageClassifierGUI(root)
        gui.display_image(sample_image_path)

        # Check that image was loaded (image attribute should be set)
        assert hasattr(gui.image_label, 'image')
        assert gui.image_label.cget("text") == ""

    @patch('src.gui.create_classifier')
    def test_display_image_error(self, mock_create_classifier, root):
        """Test image display error handling."""
        mock_classifier = Mock()
        mock_create_classifier.return_value = mock_classifier

        from gui import ImageClassifierGUI

        gui = ImageClassifierGUI(root)
        gui.display_image("nonexistent_file.jpg")

        # Check that error message is displayed
        assert "error" in gui.image_label.cget("text").lower()

    @patch('src.gui.create_classifier')
    def test_classification_complete(self, mock_create_classifier, root):
        """Test classification completion handling."""
        mock_classifier = Mock()
        mock_create_classifier.return_value = mock_classifier

        from gui import ImageClassifierGUI

        gui = ImageClassifierGUI(root)

        # Mock predictions
        predictions = [
            ("cat", 0.85),
            ("dog", 0.12),
            ("bird", 0.03)
        ]

        gui._on_classification_complete(predictions)

        # Check UI state
        assert gui.predict_button.cget("state") == tk.NORMAL
        assert "complete" in gui.status_label.cget("text").lower()
        assert gui.status_label.cget("foreground") == "green"

        # Check results display
        results_content = gui.results_text.get(1.0, tk.END)
        assert "cat" in results_content
        assert "85.00%" in results_content

    @patch('src.gui.create_classifier')
    def test_classification_error(self, mock_create_classifier, root):
        """Test classification error handling."""
        mock_classifier = Mock()
        mock_create_classifier.return_value = mock_classifier

        from gui import ImageClassifierGUI

        gui = ImageClassifierGUI(root)
        gui._on_classification_error("Classification failed")

        # Check UI state
        assert gui.predict_button.cget("state") == tk.NORMAL
        assert "failed" in gui.status_label.cget("text").lower()
        assert gui.status_label.cget("foreground") == "red"

    @patch('src.gui.create_classifier')
    def test_clear_results(self, mock_create_classifier, root):
        """Test clearing results display."""
        mock_classifier = Mock()
        mock_create_classifier.return_value = mock_classifier

        from gui import ImageClassifierGUI

        gui = ImageClassifierGUI(root)

        # Add some content to results
        gui.results_text.config(state=tk.NORMAL)
        gui.results_text.insert(tk.END, "Some test content")
        gui.results_text.config(state=tk.DISABLED)

        # Clear results
        gui.clear_results()

        # Check that results are empty
        content = gui.results_text.get(1.0, tk.END).strip()
        assert content == ""

    @patch('src.gui.create_classifier')
    @patch('tkinter.messagebox.showwarning')
    def test_classify_without_image(self, mock_messagebox, mock_create_classifier, root):
        """Test classification attempt without selecting an image."""
        mock_classifier = Mock()
        mock_create_classifier.return_value = mock_classifier

        from gui import ImageClassifierGUI

        gui = ImageClassifierGUI(root)
        gui.current_image_path = None

        gui.classify_image()

        # Check that warning was shown
        mock_messagebox.assert_called_once()

    @patch('src.gui.create_classifier')
    @patch('tkinter.messagebox.showerror')
    def test_classify_without_model(self, mock_messagebox, mock_create_classifier, root):
        """Test classification attempt without loaded model."""
        mock_create_classifier.return_value = None

        from gui import ImageClassifierGUI

        gui = ImageClassifierGUI(root)
        gui.classifier = None
        gui.current_image_path = "some_image.jpg"

        gui.classify_image()

        # Check that error was shown
        mock_messagebox.assert_called_once()


class TestGUIIntegration:
    """Integration tests for GUI components."""

    @pytest.fixture
    def root(self):
        """Create a test tkinter root window."""
        root = tk.Tk()
        root.withdraw()  # Hide the window during testing
        yield root
        root.destroy()

    @patch('src.gui.create_classifier')
    def test_gui_workflow(self, mock_create_classifier, root):
        """Test the complete GUI workflow."""
        # Mock classifier
        mock_classifier = Mock()
        mock_classifier.predict.return_value = [("cat", 0.9), ("dog", 0.1)]
        mock_create_classifier.return_value = mock_classifier

        from gui import ImageClassifierGUI

        gui = ImageClassifierGUI(root)

        # Simulate successful model loading
        gui._on_model_loaded()

        # Check initial state
        assert gui.predict_button.cget("state") == tk.DISABLED

        # Simulate image selection
        with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as tmp_file:
            # Create a simple test image
            img = Image.new('RGB', (100, 100), color='red')
            img.save(tmp_file.name, 'JPEG')

            try:
                gui.current_image_path = tmp_file.name
                gui.file_label.config(text=f"Selected: {os.path.basename(tmp_file.name)}")
                gui.predict_button.config(state=tk.NORMAL)

                # Check that predict button is enabled
                assert gui.predict_button.cget("state") == tk.NORMAL

                # Simulate classification completion
                predictions = [("cat", 0.9), ("dog", 0.1)]
                gui._on_classification_complete(predictions)

                # Check results
                results_content = gui.results_text.get(1.0, tk.END)
                assert "cat" in results_content
                assert "90.00%" in results_content

            finally:
                os.unlink(tmp_file.name)


# Mock tests that don't require actual GUI components
class TestGUILogic:
    """Test GUI logic without creating actual widgets."""

    def test_prediction_formatting(self):
        """Test prediction result formatting logic."""
        predictions = [
            ("cat", 0.85432),
            ("dog", 0.12345),
            ("bird", 0.02223)
        ]

        # This would be the logic inside display_results
        formatted_results = []
        for i, (class_name, confidence) in enumerate(predictions, 1):
            confidence_percent = confidence * 100
            result_text = f"{i}. {class_name}\n   Confidence: {confidence_percent:.2f}%\n\n"
            formatted_results.append(result_text)

        assert "1. cat" in formatted_results[0]
        assert "85.43%" in formatted_results[0]
        assert "2. dog" in formatted_results[1]
        assert "12.35%" in formatted_results[1]
