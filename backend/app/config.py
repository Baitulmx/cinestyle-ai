from pydantic_settings import BaseSettings
import os
from pathlib import Path
# Configuration and settings for the application
class Settings(BaseSettings):
    """Application settings and configuration."""
    
    # App
    app_name: str = "CineStyle AI"
    debug: bool = True
    
    # Paths
    base_dir: Path = Path(__file__).parent.parent
    uploads_dir: Path = base_dir / "uploads"
    data_dir: Path = Path(__file__).parent / "data"
    catalogue_path: Path = data_dir / "catalogue.json"
    
    # Image processing
    max_image_width: int = 600
    allowed_extensions: list = ["jpg", "jpeg", "png", "webp"]
    
    # Feature extraction
    kmeans_clusters: int = 5
    edge_detection_threshold: float = 0.25
    
    # Similarity scoring weights
    similarity_weights: dict = {
        "colour": 0.35,
        "histogram": 0.10,
        "texture": 0.15,
        "shape": 0.10,
        "category": 0.15,
        "style_tags": 0.15
    }
    
    # Recommendation
    default_top_k: int = 12
    
    class Config:
        env_file = ".env"

settings = Settings()

# Ensure directories exist
settings.uploads_dir.mkdir(parents=True, exist_ok=True)
settings.data_dir.mkdir(parents=True, exist_ok=True)
