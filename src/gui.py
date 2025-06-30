"""
Tkinter GUI for PyTorch ResNet50 Image Classifier

This module provides a user-friendly graphical interface for image classification
using the ResNet50 model.
"""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import threading
import os
import logging
from .model import create_classifier

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ImageClassifierGUI:
    """
    Main GUI class for the image classifier application.
    """

    def __init__(self, root):
        """
        Initialize the GUI.

        Args:
            root (tk.Tk): Root tkinter window
        """
        self.root = root
        self.classifier = None
        self.current_image_path = None
        self.setup_ui()
        self.load_model()

    def setup_ui(self):
        """Set up the user interface components."""
        self.root.title("PyTorch ResNet50 Image Classifier")
        self.root.geometry("800x600")
        self.root.resizable(True, True)

        # Create main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)

        # Title label
        title_label = ttk.Label(
            main_frame,
            text="PyTorch ResNet50 Image Classifier",
            font=("Arial", 16, "bold")
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # Left panel for controls
        control_frame = ttk.LabelFrame(main_frame, text="Controls", padding="10")
        control_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))

        # File selection button
        self.select_button = ttk.Button(
            control_frame,
            text="Select Image",
            command=self.select_image,
            width=20
        )
        self.select_button.grid(row=0, column=0, pady=(0, 10), sticky=tk.W)

        # Selected file label
        self.file_label = ttk.Label(
            control_frame,
            text="No file selected",
            wraplength=200
        )
        self.file_label.grid(row=1, column=0, pady=(0, 10), sticky=tk.W)

        # Predict button
        self.predict_button = ttk.Button(
            control_frame,
            text="Classify Image",
            command=self.classify_image,
            width=20,
            state=tk.DISABLED
        )
        self.predict_button.grid(row=2, column=0, pady=(0, 20), sticky=tk.W)

        # Progress bar
        self.progress = ttk.Progressbar(
            control_frame,
            mode='indeterminate',
            length=200
        )
        self.progress.grid(row=3, column=0, pady=(0, 10), sticky=tk.W)

        # Status label
        self.status_label = ttk.Label(
            control_frame,
            text="Loading model...",
            foreground="blue"
        )
        self.status_label.grid(row=4, column=0, pady=(0, 10), sticky=tk.W)

        # Results frame
        results_frame = ttk.LabelFrame(control_frame, text="Predictions", padding="5")
        results_frame.grid(row=5, column=0, pady=(10, 0), sticky=(tk.W, tk.E, tk.N, tk.S))
        control_frame.rowconfigure(5, weight=1)

        # Results text widget with scrollbar
        text_frame = ttk.Frame(results_frame)
        text_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        results_frame.columnconfigure(0, weight=1)
        results_frame.rowconfigure(0, weight=1)

        self.results_text = tk.Text(
            text_frame,
            width=30,
            height=10,
            wrap=tk.WORD,
            state=tk.DISABLED
        )
        scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=self.results_text.yview)
        self.results_text.configure(yscrollcommand=scrollbar.set)

        self.results_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        text_frame.columnconfigure(0, weight=1)
        text_frame.rowconfigure(0, weight=1)

        # Right panel for image display
        image_frame = ttk.LabelFrame(main_frame, text="Image Preview", padding="10")
        image_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        image_frame.columnconfigure(0, weight=1)
        image_frame.rowconfigure(0, weight=1)

        # Image display label
        self.image_label = ttk.Label(
            image_frame,
            text="No image selected",
            anchor=tk.CENTER
        )
        self.image_label.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    def load_model(self):
        """Load the ResNet50 model in a separate thread."""
        def load_in_background():
            try:
                self.progress.start()
                self.classifier = create_classifier()
                self.root.after(0, self._on_model_loaded)
            except Exception as e:
                self.root.after(0, lambda: self._on_model_error(str(e)))

        thread = threading.Thread(target=load_in_background, daemon=True)
        thread.start()

    def _on_model_loaded(self):
        """Called when model loading is complete."""
        self.progress.stop()
        self.status_label.config(text="Model loaded successfully", foreground="green")
        logger.info("Model loaded successfully")

    def _on_model_error(self, error_msg):
        """Called when model loading fails."""
        self.progress.stop()
        self.status_label.config(text="Model loading failed", foreground="red")
        messagebox.showerror("Model Error", f"Failed to load model: {error_msg}")
        logger.error(f"Model loading failed: {error_msg}")

    def select_image(self):
        """Open file dialog to select an image."""
        file_types = [
            ("Image files", "*.jpg *.jpeg *.png *.bmp *.gif *.tiff"),
            ("JPEG files", "*.jpg *.jpeg"),
            ("PNG files", "*.png"),
            ("All files", "*.*")
        ]

        file_path = filedialog.askopenfilename(
            title="Select an image file",
            filetypes=file_types
        )

        if file_path:
            self.current_image_path = file_path
            self.file_label.config(text=f"Selected: {os.path.basename(file_path)}")
            self.predict_button.config(state=tk.NORMAL)
            self.display_image(file_path)
            self.clear_results()

    def display_image(self, image_path):
        """Display the selected image in the GUI."""
        try:
            # Load and resize image for display
            image = Image.open(image_path)

            # Calculate display size (max 400x400, maintain aspect ratio)
            max_size = (400, 400)
            image.thumbnail(max_size, Image.Resampling.LANCZOS)

            # Convert to PhotoImage
            photo = ImageTk.PhotoImage(image)

            # Update image label
            self.image_label.config(image=photo, text="")
            self.image_label.image = photo  # Keep a reference

        except Exception as e:
            self.image_label.config(text=f"Error loading image: {str(e)}")
            logger.error(f"Error displaying image: {e}")

    def classify_image(self):
        """Classify the selected image."""
        if not self.current_image_path:
            messagebox.showwarning("No Image", "Please select an image first.")
            return

        if not self.classifier:
            messagebox.showerror("Model Error", "Model is not loaded.")
            return

        # Run classification in background thread
        def classify_in_background():
            try:
                self.root.after(0, self._on_classification_start)
                predictions = self.classifier.predict(self.current_image_path, top_k=5)
                self.root.after(0, lambda: self._on_classification_complete(predictions))
            except Exception as e:
                self.root.after(0, lambda: self._on_classification_error(str(e)))

        thread = threading.Thread(target=classify_in_background, daemon=True)
        thread.start()

    def _on_classification_start(self):
        """Called when classification starts."""
        self.progress.start()
        self.predict_button.config(state=tk.DISABLED)
        self.status_label.config(text="Classifying...", foreground="blue")
        self.clear_results()

    def _on_classification_complete(self, predictions):
        """Called when classification is complete."""
        self.progress.stop()
        self.predict_button.config(state=tk.NORMAL)
        self.status_label.config(text="Classification complete", foreground="green")
        self.display_results(predictions)

    def _on_classification_error(self, error_msg):
        """Called when classification fails."""
        self.progress.stop()
        self.predict_button.config(state=tk.NORMAL)
        self.status_label.config(text="Classification failed", foreground="red")
        messagebox.showerror("Classification Error", f"Failed to classify image: {error_msg}")
        logger.error(f"Classification failed: {error_msg}")

    def display_results(self, predictions):
        """Display classification results."""
        self.results_text.config(state=tk.NORMAL)
        self.results_text.delete(1.0, tk.END)

        self.results_text.insert(tk.END, "Top 5 Predictions:\n\n")

        for i, (class_name, confidence) in enumerate(predictions, 1):
            confidence_percent = confidence * 100
            result_text = f"{i}. {class_name}\n   Confidence: {confidence_percent:.2f}%\n\n"
            self.results_text.insert(tk.END, result_text)

        self.results_text.config(state=tk.DISABLED)

    def clear_results(self):
        """Clear the results display."""
        self.results_text.config(state=tk.NORMAL)
        self.results_text.delete(1.0, tk.END)
        self.results_text.config(state=tk.DISABLED)


def main():
    """Main function to run the application."""
    try:
        root = tk.Tk()
        app = ImageClassifierGUI(root)
        root.mainloop()
    except Exception as e:
        logger.error(f"Application error: {e}")
        messagebox.showerror("Application Error", f"An error occurred: {e}")


if __name__ == "__main__":
    main()
