# Image Masking Creation Script | Binary Mask Generation

## Author
- **Name**: Hemang Jethava  
- **Date**: 11-11-2024

## Description
This Python script reads images (JPG or PNG) from a specified folder, processes them to generate binary masks based on color thresholds, and saves the resulting masks as PNG files. The script checks if all RGB color channels of a pixel exceed the threshold of 200, marking it as part of the mask (255 value). The script also logs the number of pixels where all RGB channels exceed the threshold across all processed images.

### Features:
- Process images in parallel for faster execution.
- Generate binary masks where all three RGB color channels are above 200.
- Save the generated masks as PNG files (lossless format).
- Log the number of "fully on" pixels (where all RGB channels exceed 200).

## Requirements

Before running the script, make sure you have the following dependencies installed:

- OpenCV (`cv2`) - for image processing.
- NumPy - for handling arrays and matrix operations.
- `concurrent.futures` - for parallel processing.
- `logging` - for logging the number of pixels.

To install required libraries, you can use pip:

```bash
pip install opencv-python numpy
