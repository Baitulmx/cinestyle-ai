import numpy as np
from typing import List, Dict
from app.models import SimilarityScoreBreakdown

def euclidean_distance(color1: List[int], color2: List[int]) -> float:
    """
    Calculate Euclidean distance between two RGB colors.
    
    Args:
        color1: [r, g, b]
        color2: [r, g, b]
    
    Returns:
        Distance value
    """
    return np.sqrt(sum((c1 - c2) ** 2 for c1, c2 in zip(color1, color2)))

def color_similarity(input_colors: List[List[int]], item_colors: List[List[int]]) -> float:
    """
    Compare dominant colors between input and item.
    
    Args:
        input_colors: List of [r, g, b] from input image
        item_colors: List of [r, g, b] from catalogue item
    
    Returns:
        Similarity score 0-1
    """
    if not input_colors or not item_colors:
        return 0.5
    
    # Find closest color pair for each input color
    distances = []
    for input_color in input_colors:
        closest_distance = min(
            euclidean_distance(input_color, item_color)
            for item_color in item_colors
        )
        # Normalize distance (max distance is ~440 for RGB)
        similarity = 1 - (closest_distance / 440)
        distances.append(max(0, similarity))
    
    # Average similarity
    return float(np.mean(distances))

def histogram_similarity(input_hist: List[float], item_hist: List[float]) -> float:
    """
    Compare histograms using cosine similarity.
    
    Args:
        input_hist: Histogram from input image
        item_hist: Histogram from catalogue item
    
    Returns:
        Similarity score 0-1
    """
    if not input_hist or not item_hist:
        return 0.5
    
    # Pad to same length
    max_len = max(len(input_hist), len(item_hist))
    input_hist = input_hist + [0] * (max_len - len(input_hist))
    item_hist = item_hist + [0] * (max_len - len(item_hist))
    
    # Cosine similarity
    input_arr = np.array(input_hist)
    item_arr = np.array(item_hist)
    
    norm_input = np.linalg.norm(input_arr)
    norm_item = np.linalg.norm(item_arr)
    
    if norm_input == 0 or norm_item == 0:
        return 0.5
    
    cosine_sim = np.dot(input_arr, item_arr) / (norm_input * norm_item)
    return float(np.clip(cosine_sim, 0, 1))

def texture_similarity(input_texture: dict, item_texture: dict) -> float:
    """
    Compare texture features.
    
    Args:
        input_texture: Texture dict from input
        item_texture: Texture dict from item
    
    Returns:
        Similarity score 0-1
    """
    if not item_texture:
        return 0.5
    
    # Compare edge density and contrast
    edge_diff = abs(input_texture.get("edge_density", 0.15) - item_texture.get("edge_density", 0.15)) * 2
    contrast_diff = abs(input_texture.get("contrast", 0.3) - item_texture.get("contrast", 0.3)) * 2
    
    # Convert to similarity
    edge_sim = 1 - min(edge_diff, 1)
    contrast_sim = 1 - min(contrast_diff, 1)
    
    return float(0.5 * edge_sim + 0.5 * contrast_sim)

def shape_similarity(input_shape: dict, item_shape: dict) -> float:
    """
    Compare shape features.
    
    Args:
        input_shape: Shape dict from input
        item_shape: Shape dict from item
    
    Returns:
        Similarity score 0-1
    """
    if not item_shape:
        return 0.5
    
    # Compare aspect ratio and coverage
    input_aspect = input_shape.get("aspect_ratio", 1.5)
    item_aspect = item_shape.get("aspect_ratio", 1.5)
    
    input_coverage = input_shape.get("coverage", 0.6)
    item_coverage = item_shape.get("coverage", 0.6)
    
    # Normalize aspect ratio difference
    aspect_diff = abs(input_aspect - item_aspect) / max(input_aspect, item_aspect, 1)
    aspect_sim = 1 - min(aspect_diff, 1)
    
    # Compare coverage
    coverage_diff = abs(input_coverage - item_coverage)
    coverage_sim = 1 - coverage_diff
    
    return float(0.6 * aspect_sim + 0.4 * coverage_sim)

def category_similarity(input_category: str, item_category: str) -> float:
    """
    Compare clothing categories.
    
    Args:
        input_category: Predicted category from input
        item_category: Category of catalogue item
    
    Returns:
        Similarity score 0-1
    """
    if input_category == item_category:
        return 1.0
    
    # Define related categories
    related = {
        "jacket": ["coat", "hoodie"],
        "coat": ["jacket", "hoodie"],
        "hoodie": ["jacket", "coat"],
        "trousers": ["jeans", "pants"],
        "jeans": ["trousers", "pants"],
        "pants": ["trousers", "jeans"],
        "shirt": ["t-shirt"],
        "t-shirt": ["shirt"],
        "shoes": ["boots", "sneakers"],
        "boots": ["shoes", "sneakers"],
        "sneakers": ["shoes", "boots"],
    }
    
    if item_category in related.get(input_category, []):
        return 0.7
    
    return 0.2

def style_tag_similarity(input_tags: List[str], item_tags: List[str]) -> float:
    """
    Compare style tags using Jaccard similarity.
    
    Args:
        input_tags: Style tags from input
        item_tags: Style tags from item
    
    Returns:
        Similarity score 0-1
    """
    if not input_tags or not item_tags:
        return 0.5
    
    input_set = set(input_tags)
    item_set = set(item_tags)
    
    if not input_set and not item_set:
        return 1.0
    
    intersection = len(input_set & item_set)
    union = len(input_set | item_set)
    
    if union == 0:
        return 0.0
    
    return float(intersection / union)

def final_similarity_score(input_features: dict, item: dict, weights: dict = None) -> dict:
    """
    Calculate final similarity score with breakdown.
    
    Args:
        input_features: Extracted features from input image
        item: Catalogue item
        weights: Score weights
    
    Returns:
        Dictionary with score and breakdown
    """
    if weights is None:
        weights = {
            "colour": 0.35,
            "histogram": 0.10,
            "texture": 0.15,
            "shape": 0.10,
            "category": 0.15,
            "style_tags": 0.15
        }
    
    # Extract input features
    input_colors = input_features.get("dominant_colors", [])
    input_hist = input_features.get("color_histogram", [])
    input_texture = input_features.get("texture", {})
    input_shape = input_features.get("shape", {})
    input_category = input_features.get("clothing_hints", {}).get("likely_category", "shirt")
    input_tags = input_features.get("style_tags", [])
    
    # Convert pydantic models to dicts if needed
    if hasattr(input_texture, "dict"):
        input_texture = input_texture.dict()
    if hasattr(input_shape, "dict"):
        input_shape = input_shape.dict()
    
    # Calculate individual similarities
    colour_sim = color_similarity(input_colors, item.get("dominant_colors", []))
    hist_sim = histogram_similarity(input_hist, item.get("color_histogram", []))
    texture_sim = texture_similarity(input_texture, item.get("texture", {}))
    shape_sim = shape_similarity(input_shape, item.get("shape", {}))
    category_sim = category_similarity(input_category, item.get("category", "shirt"))
    tags_sim = style_tag_similarity(input_tags, item.get("style_tags", []))
    
    # Calculate weighted final score
    final_score = (
        weights["colour"] * colour_sim +
        weights["histogram"] * hist_sim +
        weights["texture"] * texture_sim +
        weights["shape"] * shape_sim +
        weights["category"] * category_sim +
        weights["style_tags"] * tags_sim
    )
    
    # Generate reasons
    reasons = []
    
    if colour_sim > 0.75:
        reasons.append("Similar colour palette")
    
    if category_sim > 0.8:
        reasons.append(f"Matched {item.get('category', 'clothing')} category")
    elif category_sim > 0.6:
        reasons.append(f"Related {item.get('category', 'clothing')} category")
    
    if tags_sim > 0.5:
        matching_tags = set(input_tags) & set(item.get("style_tags", []))
        if matching_tags:
            tags_str = " and ".join(list(matching_tags)[:2])
            reasons.append(f"Shared {tags_str} style tags")
    
    if texture_sim > 0.7:
        reasons.append("Similar texture and contrast")
    
    if not reasons:
        reasons = ["Good overall match"]
    
    return {
        "score": float(final_score),
        "breakdown": SimilarityScoreBreakdown(
            colour=colour_sim,
            histogram=hist_sim,
            texture=texture_sim,
            shape=shape_sim,
            category=category_sim,
            style_tags=tags_sim
        ),
        "reasons": reasons
    }
