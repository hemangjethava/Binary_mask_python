# ==============================================================================
# Author: Hemang Jethava
# Email: jethava007@gmail.com
# Date: 11-11-2024
# Description: This script reads jpg and png images from a folder, processes them to generate 
#              binary masks based on color thresholds, and saves the masks as PNG files.
#              The script also logs the number of pixels where all RGB channels 
#              exceed a threshold of 200.
# License: MIT License (or any license you're using)
# Version: 1.0
# ==============================================================================
# Required Libraries: 
#   - OpenCV (cv2)
#   - NumPy
#   - concurrent.futures (for parallel processing)
#   - logging (for logging details)

import cv2
import numpy as np
import os
import concurrent.futures
import logging

# Setup logging to log the count of pixels
logging.basicConfig(level=logging.INFO)

def process_image(image_path, output_dir):
	"""
    Processes an image to generate a binary mask where all three color channels 
    (R, G, B) are above the threshold of 200.

    Args:
    - image_path (str): Path to the input image.
    - output_dir (str): Directory where the mask will be saved.

    Returns:
    - mask_count (int): The number of pixels where the mask is "on" (255).
    - mask_filename (str): The filename where the mask image is saved.
    """
	try:
        # Read the image
		image = cv2.imread(image_path)
        
		if image is None:
			logging.warning(f"Failed to read image: {image_path}")
			return 0, None
        
		# Initialize an empty mask with the same height and width as the image
		mask = np.zeros(image.shape[:2], dtype=np.uint8)
		
		# Iterate over each pixel to check if all three channels are greater than 200
		for i in range(image.shape[0]):
			for j in range(image.shape[1]):
				# Check if R, G, B are all greater than 200
				if image[i, j, 0] > 200 and image[i, j, 1] > 200 and image[i, j, 2] > 200:
					mask[i, j] = 255  # Set the mask pixel to 255 if condition is met
		
		# Check if output directory exists, if not, create it
		if not os.path.exists(output_dir):
			os.makedirs(output_dir)
		
		# Create the mask filename (save to the outputs directory)
		mask_filename = os.path.join(output_dir, image_path.split('\\')[-1].split('.')[0] + "_mask.png")
		
		# Write the mask to a PNG file (lossless format)
		cv2.imwrite(mask_filename, mask)
		
		# Count the number of pixels where the mask is fully 'on' (255)
		mask_count = np.sum(mask == 255)
		
		# Log the count of pixels where the mask is fully 'on' for this image
		logging.info(f"Image: {image_path}, Mask pixels fully 'on': {mask_count}")
		
		return mask_count, mask_filename
    
	except Exception as e:
		logging.error(f"Error processing image {image_path}: {e}")
		return 0, None

def process_images_in_parallel(image_paths, output_dir):
	"""
	Processes a list of image files in parallel, generating binary masks for each image. 
	The function uses a thread pool to process images concurrently and logs the results, 
	including the number of pixels where the mask is fully 'on' (i.e., where all RGB channels are above 200).

	Args:
		image_paths (list of str): A list of file paths to the images that need to be processed.
		output_dir (str): The directory where the binary mask images will be saved.

	Returns:
		int: The total number of pixels where the mask is fully 'on' (i.e., all RGB channels > 200) 
			 across all processed images.

	Logs:
		- Logs the path of each processed mask image.
		- Logs the total number of pixels where the mask is fully 'on' across all images.
	"""
	total_mask_count = 0

	# Using ThreadPoolExecutor to process images in parallel
	with concurrent.futures.ThreadPoolExecutor() as executor:
		futures = [executor.submit(process_image, image_path, output_dir) for image_path in image_paths]
		
		for future in concurrent.futures.as_completed(futures):
			mask_count, mask_filename = future.result()
			if mask_filename:
				logging.info(f"Processed mask saved to {mask_filename}")
			total_mask_count += mask_count

	# Log the total number of pixels where the mask is fully 'on' across all images
	logging.info(f"Total pixels where mask is fully 'on' across all images: {total_mask_count}")
	return total_mask_count

if __name__ == "__main__":
	"""
	Main entry point for the script that processes a batch of images.

	This function does the following:
	1. Defines the directory containing the input images.
	2. Defines the directory where the output mask images will be saved.
	3. Collects all the image paths from the input directory.
	4. Processes the images in parallel to generate binary masks.
	5. Logs the total number of pixels where the mask is fully 'on' (all RGB channels > 200).

	This function does not take any arguments or return anything. It relies on the 
	'process_images_in_parallel' function to process the images and save the results.
	"""
	# The directory containing the JPG images
	image_dir = 'Online-test'

	# The output directory where the mask images will be saved
	output_dir = 'outputs'

	# Get a list of all jpg files in the directory
	image_paths = [os.path.join(image_dir, f) for f in os.listdir(image_dir) if f.lower().endswith('g')]

	# Process the images in parallel and log the total pixel count
	process_images_in_parallel(image_paths, output_dir)
