# Sample Data Directory

This directory is for storing sample images to test the image classifier.

## Supported Image Formats

- JPEG (.jpg, .jpeg)
- PNG (.png)
- BMP (.bmp)
- GIF (.gif)
- TIFF (.tiff)

## Recommended Test Images

For best results with the ResNet50 model, try images containing:

### Animals
- Cats
- Dogs
- Birds
- Fish
- Horses
- Elephants

### Objects
- Cars
- Bicycles
- Airplanes
- Boats
- Furniture

### Nature
- Flowers
- Trees
- Mountains
- Beaches

## Image Requirements

- **Resolution**: Any resolution (will be automatically resized to 224x224)
- **Format**: RGB color images work best
- **Size**: Reasonable file sizes (< 50MB for performance)

## Adding Test Images

1. Create a subdirectory (e.g., `samples/`)
2. Add your test images
3. Run the application and select images from this directory

## Note

This directory is included in `.gitignore` to avoid committing large image files to the repository. Add your own test images locally.

## Sample Directory Structure

```
data/
├── README.md          # This file
├── samples/           # Your test images
│   ├── cat.jpg
│   ├── dog.png
│   └── bird.jpeg
└── results/           # Optional: save classification results
```
