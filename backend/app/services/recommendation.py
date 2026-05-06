from typing import List, Dict
from app.models import RecommendationResult, FilterOptions
from app.services.similarity import final_similarity_score

def recommend_items(
    input_features: dict,
    filters: FilterOptions,
    catalogue: List[Dict],
    top_k: int = 12
) -> List[RecommendationResult]:
    """
    Generate ranked recommendations based on features and filters.
    
    Args:
        input_features: Extracted features from input image
        filters: User-specified filters (price, category, style tags)
        catalogue: List of catalogue items
        top_k: Number of recommendations to return
    
    Returns:
        List of RecommendationResult objects, sorted by score descending
    """
    
    # Apply hard filters
    filtered_items = []
    
    for item in catalogue:
        # Price filter
        if item.price < filters.min_price or item.price > filters.max_price:
            continue
        
        # Category filter
        if filters.categories:
            if item.category not in filters.categories:
                continue
        
        # Style tag filter
        if filters.style_tags:
            item_tags = set(item.style_tags)
            filter_tags = set(filters.style_tags)
            if not (item_tags & filter_tags):  # No intersection
                continue
        
        filtered_items.append(item)
    
    # Score remaining items
    scored_items = []
    
    for item in filtered_items:
        # Convert item to dict format for similarity function
        item_dict = item.dict()
        
        # Calculate similarity
        similarity_result = final_similarity_score(input_features, item_dict)
        
        # Create recommendation result
        recommendation = RecommendationResult(
            id=item.id,
            name=item.name,
            price=item.price,
            currency=item.currency,
            category=item.category,
            image=item.image,
            link=item.link,
            style_tags=item.style_tags,
            score=similarity_result["score"],
            score_breakdown=similarity_result["breakdown"],
            reasons=similarity_result["reasons"]
        )
        
        scored_items.append(recommendation)
    
    # Sort by score descending
    scored_items.sort(key=lambda x: x.score, reverse=True)
    
    # Return top k
    return scored_items[:top_k]
