import cv2
import numpy as np
from sklearn.cluster import KMeans
from app.models import ExtractedFeatures, TextureFeatures, ShapeFeatures, ClothingHints
from app.services.image_preprocessing import create_analysis_regions

def extract_dominant_colors(image: np.ndarray, k: int = 5) -> list:
    """
    Extract dominant colors using KMeans clustering.
    
    Args:
        image: Input image (RGB format)
        k: Number of color clusters
    
    Returns:
        List of [r, g, b] dominant colors
    """
    # Reshape image to 2D array of pixels
    pixels = image.reshape(-1, 3).astype(np.float32)
    
    # Sample max 10,000 pixels for speed
    if len(pixels) > 10000:
        sample_indices = np.random.choice(len(pixels), 10000, replace=False)
        pixels = pixels[sample_indices]
    
    # Apply KMeans
    kmeans = KMeans(n_clusters=k, n_init=10, random_state=42)
    kmeans.fit(pixels)
    
    # Get cluster centers and convert to int
    colors = kmeans.cluster_centers_.astype(int).tolist()
    colors = [[int(c[0]), int(c[1]), int(c[2])] for c in colors]
    
    return colors

def extract_color_histogram(image: np.ndarray) -> list:
    """
    Extract HSV color histogram.
    
    Args:
        image: Input image (RGB format)
    
    Returns:
        Normalized histogram values
    """
    # Convert RGB to HSV
    hsv = cv2.cvtColor(image.astype(np.uint8), cv2.COLOR_RGB2HSV)
    
    # Calculate histogram for hue and saturation
    hist_h = cv2.calcHist([hsv], [0], None, [18], [0, 180])
    hist_s = cv2.calcHist([hsv], [1], None, [25], [0, 256])
    
    # Normalize
    hist_h = cv2.normalize(hist_h, hist_h).flatten().tolist()
    hist_s = cv2.normalize(hist_s, hist_s).flatten().tolist()
    
    # Combine
    histogram = hist_h + hist_s
    return histogram

def extract_texture_features(image: np.ndarray) -> TextureFeatures:
    """
    Extract texture-related features.
    
    Args:
        image: Input image
    
    Returns:
        TextureFeatures object
    """
    # Convert to grayscale
    gray = cv2.cvtColor(image.astype(np.uint8), cv2.COLOR_RGB2GRAY)
    
    # Edge detection
    edges = cv2.Canny(gray, 100, 200)
    edge_density = np.sum(edges > 0) / edges.size
    
    # Contrast (standard deviation)
    contrast = np.std(gray) / 255.0
    
    # Brightness (mean value)
    brightness = np.mean(gray) / 255.0
    
    # Saturation
    hsv = cv2.cvtColor(image.astype(np.uint8), cv2.COLOR_RGB2HSV)
    saturation = np.mean(hsv[:, :, 1]) / 255.0
    
    return TextureFeatures(
        edge_density=float(np.clip(edge_density, 0, 1)),
        contrast=float(np.clip(contrast, 0, 1)),
        brightness=float(np.clip(brightness, 0, 1)),
        saturation=float(np.clip(saturation, 0, 1))
    )

def extract_shape_features(image: np.ndarray) -> ShapeFeatures:
    """
    Extract shape-related features.
    
    Args:
        image: Input image
    
    Returns:
        ShapeFeatures object
    """
    height, width = image.shape[:2]
    
    # Convert to grayscale and threshold
    gray = cv2.cvtColor(image.astype(np.uint8), cv2.COLOR_RGB2GRAY)
    _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    
    # Find contours
    contours, _ = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    if not contours:
        return ShapeFeatures(aspect_ratio=1.0, coverage=0.0, vertical_edge_ratio=0.5)
    
    # Get largest contour
    largest_contour = max(contours, key=cv2.contourArea)
    area = cv2.contourArea(largest_contour)
    
    # Get bounding box
    x, y, w, h = cv2.boundingRect(largest_contour)
    
    # Aspect ratio
    aspect_ratio = h / (w + 1) if w > 0 else 1.0
    
    # Coverage
    coverage = area / (height * width)
    
    # Vertical edge ratio (approximate)
    edges = cv2.Canny(gray, 100, 200)
    vertical_edges = np.sum(np.abs(np.diff(edges, axis=1)) > 0)
    total_edges = np.sum(edges > 0) + 1
    vertical_edge_ratio = vertical_edges / total_edges
    
    return ShapeFeatures(
        aspect_ratio=float(aspect_ratio),
        coverage=float(np.clip(coverage, 0, 1)),
        vertical_edge_ratio=float(np.clip(vertical_edge_ratio, 0, 1))
    )

def predict_clothing_category(image: np.ndarray, regions: dict) -> ClothingHints:
    """
    Rule-based prediction of clothing category.
    
    Args:
        image: Full image
        regions: Dictionary of image regions
    
    Returns:
        ClothingHints with likely category and confidence
    """
    # Extract texture features from different regions
    upper_texture = extract_texture_features(regions["upper_body"])
    lower_texture = extract_texture_features(regions["lower_body"])
    full_texture = extract_texture_features(image)
    
    # Extract shape features
    shape = extract_shape_features(image)
    
    # Rule-based logic
    confidence = 0.6
    category = "shirt"
    
    # High dark coverage + high edge density = jacket/coat
    if full_texture.brightness < 0.35 and upper_texture.edge_density > 0.22:
        category = "jacket"
        confidence = 0.75
    
    # High saturation and low texture = t-shirt
    elif full_texture.saturation > 0.50 and full_texture.edge_density < 0.15:
        category = "t-shirt"
        confidence = 0.65
    
    # High vertical ratio + medium aspect ratio = trousers
    elif shape.vertical_edge_ratio > 0.45 and 0.8 < shape.aspect_ratio < 2.5:
        category = "trousers"
        confidence = 0.70
    
    # Dark + high contrast + structured = formal
    elif full_texture.brightness < 0.40 and full_texture.contrast > 0.35:
        category = "jacket"
        confidence = 0.72
    
    # Very dark = could be jacket/hoodie
    elif full_texture.brightness < 0.25:
        category = "jacket"
        confidence = 0.65
    
    return ClothingHints(
        likely_category=category,
        confidence=float(np.clip(confidence, 0, 1))
    )

def predict_style_tags(texture: TextureFeatures, brightness: float, saturation: float) -> list:
    """
    Rule-based prediction of style tags.
    
    Args:
        texture: Texture features
        brightness: Image brightness (0-1)
        saturation: Image saturation (0-1)
    
    Returns:
        List of style tags
    """
    tags = []
    
    # Dark
    if brightness < 0.35:
        tags.append("dark")
    
    # Minimalist
    if saturation < 0.25 and brightness > 0.45:
        tags.append("minimalist")
    
    # Edgy
    if texture.edge_density > 0.25 and brightness < 0.45:
        tags.append("edgy")
    
    # Formal
    if tags.count("dark") > 0 and texture.contrast > 0.30:
        if "edgy" not in tags:
            tags.append("formal")
    
    # Casual
    if saturation > 0.50:
        tags.append("casual")
    
    # Professional
    if brightness > 0.45 and saturation < 0.35 and texture.contrast > 0.25:
        tags.append("professional")
    
    # Vintage (brownish tones)
    if brightness > 0.40 and brightness < 0.65 and saturation > 0.20 and saturation < 0.45:
        tags.append("vintage")
    
    # Ensure we have at least 2 tags
    if not tags:
        tags = ["casual", "modern"]
    
    return list(set(tags))[:4]  # Return max 4 unique tags

def extract_features(image: np.ndarray) -> ExtractedFeatures:
    """
    Complete feature extraction pipeline.
    
    Args:
        image: Input image (RGB format)
    
    Returns:
        ExtractedFeatures object with all extracted features
    """
    # Ensure image is in correct format
    if image.dtype != np.uint8:
        image = (image * 255).astype(np.uint8)
    
    # Extract dominant colors
    dominant_colors = extract_dominant_colors(image, k=5)
    
    # Extract color histogram
    color_histogram = extract_color_histogram(image)
    
    # Extract texture
    texture = extract_texture_features(image)
    
    # Extract shape
    shape = extract_shape_features(image)
    
    # Create regions for analysis
    regions = create_analysis_regions(image)
    
    # Predict category
    clothing_hints = predict_clothing_category(image, regions)
    
    # Predict style tags
    style_tags = predict_style_tags(texture, texture.brightness, texture.saturation)
    
    # Generate explanation
    explanation = []
    
    if texture.brightness < 0.35:
        explanation.append("Dominant dark colours detected")
    elif texture.brightness > 0.65:
        explanation.append("Bright, light colour palette detected")
    
    if texture.edge_density > 0.25:
        explanation.append("Structured silhouette with visible edges")
    elif texture.edge_density < 0.10:
        explanation.append("Smooth, minimalist silhouette")
    
    if texture.saturation > 0.50:
        explanation.append("High colour saturation suggests casual style")
    
    if shape.vertical_edge_ratio > 0.50:
        explanation.append("Vertical proportion suggests fitted silhouette")
    
    explanation.append(f"Predicted category: {clothing_hints.likely_category}")
    
    return ExtractedFeatures(
        dominant_colors=dominant_colors,
        color_histogram=color_histogram,
        texture=texture,
        shape=shape,
        clothing_hints=clothing_hints,
        style_tags=style_tags,
        explanation=explanation
    )
