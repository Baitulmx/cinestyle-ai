from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any

class DominantColor(BaseModel):
    """RGB color representation."""
    r: int = Field(..., ge=0, le=255)
    g: int = Field(..., ge=0, le=255)
    b: int = Field(..., ge=0, le=255)

class TextureFeatures(BaseModel):
    """Texture-related features extracted from image."""
    edge_density: float = Field(..., ge=0, le=1)
    contrast: float = Field(..., ge=0, le=1)
    brightness: float = Field(..., ge=0, le=1)
    saturation: float = Field(..., ge=0, le=1)

class ShapeFeatures(BaseModel):
    """Shape-related features extracted from image."""
    aspect_ratio: float
    coverage: float = Field(..., ge=0, le=1)
    vertical_edge_ratio: float = Field(..., ge=0, le=1)

class ClothingHints(BaseModel):
    """Rule-based clothing category predictions."""
    likely_category: str
    confidence: float = Field(..., ge=0, le=1)

class ExtractedFeatures(BaseModel):
    """Complete extracted features from an image."""
    dominant_colors: List[List[int]]
    color_histogram: List[float]
    texture: TextureFeatures
    shape: ShapeFeatures
    clothing_hints: ClothingHints
    style_tags: List[str]
    explanation: List[str]

class SimilarityScoreBreakdown(BaseModel):
    """Detailed breakdown of similarity scoring."""
    colour: float = Field(..., ge=0, le=1)
    histogram: float = Field(..., ge=0, le=1)
    texture: float = Field(..., ge=0, le=1)
    shape: float = Field(..., ge=0, le=1)
    category: float = Field(..., ge=0, le=1)
    style_tags: float = Field(..., ge=0, le=1)

class CatalogueItem(BaseModel):
    """A clothing item in the catalogue."""
    id: str
    name: str
    category: str
    price: float
    currency: str = "GBP"
    retailer: str
    link: str
    image: str
    style_tags: List[str]
    dominant_colors: Optional[List[List[int]]] = None
    texture: Optional[Dict[str, float]] = None
    shape: Optional[Dict[str, float]] = None

class RecommendationResult(BaseModel):
    """A single recommendation with scoring details."""
    id: str
    name: str
    price: float
    currency: str
    category: str
    image: str
    link: str
    style_tags: List[str]
    score: float = Field(..., ge=0, le=1)
    score_breakdown: SimilarityScoreBreakdown
    reasons: List[str]

class FilterOptions(BaseModel):
    """User-provided filters for recommendations."""
    min_price: float = 0
    max_price: float = 10000
    style_tags: Optional[List[str]] = None
    categories: Optional[List[str]] = None

class RecommendationResponse(BaseModel):
    """Response from the recommendation endpoint."""
    success: bool
    query_features: Optional[ExtractedFeatures] = None
    filters_applied: FilterOptions
    count: int
    recommendations: List[RecommendationResult]

class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    message: str

class ItemsResponse(BaseModel):
    """Response containing all catalogue items."""
    count: int
    items: List[CatalogueItem]

class AnalyzeResponse(BaseModel):
    """Response from the analyze endpoint."""
    success: bool
    features: ExtractedFeatures
