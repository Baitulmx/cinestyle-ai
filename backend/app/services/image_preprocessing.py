import cv2
import numpy as np
from pathlib import Path

def load_image(path: str) -> np.ndarray:
    """
    Load an image and convert from BGR to RGB.
    
    Args:
        path: Path to image file
    
    Returns:
        Image as numpy array in RGB format
    
    Raises:
        ValueError if image cannot be loaded
    """
    image = cv2.imread(path)
    
    if image is None:
        raise ValueError(f"Cannot load image from {path}")
    
    # Convert BGR to RGB (OpenCV uses BGR by default)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return image_rgb

def resize_image(image: np.ndarray, max_width: int = 600) -> np.ndarray:
    """
    Resize image to max width while maintaining aspect ratio.
    Does not upscale.
    
    Args:
        image: Input image as numpy array
        max_width: Maximum width in pixels
    
    Returns:
        Resized image
    """
    height, width = image.shape[:2]
    
    # If image is already smaller, return as is
    if width <= max_width:
        return image
    
    # Calculate scaling factor
    scale = max_width / width
    new_width = max_width
    new_height = int(height * scale)
    
    # Resize using OpenCV
    resized = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_AREA)
    return resized

def remove_background_simple(image: np.ndarray) -> np.ndarray:
    """
    Simple background removal by cropping central region.
    Assumes the main subject (outfit) is in the center.
    
    Args:
        image: Input image
    
    Returns:
        Cropped image focusing on central 70%
    """
    height, width = image.shape[:2]
    
    # Crop central 70% of image
    x_crop = int(width * 0.15)
    y_crop = int(height * 0.15)
    x_end = int(width * 0.85)
    y_end = int(height * 0.85)
    
    cropped = image[y_crop:y_end, x_crop:x_end]
    return cropped

def create_analysis_regions(image: np.ndarray) -> dict:
    """
    Split image into analysis regions.
    
    Args:
        image: Input image
    
    Returns:
        Dictionary with full, upper_body, lower_body, and centre regions
    """
    height, width = image.shape[:2]
    
    # Calculate region boundaries
    upper_start = int(height * 0.15)
    upper_end = int(height * 0.60)
    
    lower_start = int(height * 0.55)
    lower_end = int(height * 0.95)
    
    centre_x_start = int(width * 0.20)
    centre_x_end = int(width * 0.80)
    centre_y_start = int(height * 0.10)
    centre_y_end = int(height * 0.95)
    
    # Extract regions
    regions = {
        "full": image,
        "upper_body": image[upper_start:upper_end, :],
        "lower_body": image[lower_start:lower_end, :],
        "centre": image[centre_y_start:centre_y_end, centre_x_start:centre_x_end]
    }
    
    return regions
