from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import os

from app.config import settings
from app.models import HealthResponse, ItemsResponse, AnalyzeResponse, RecommendationResponse, FilterOptions
from app.services.catalogue_loader import load_catalogue
from app.services.image_preprocessing import load_image, resize_image
from app.services.feature_extraction import extract_features
from app.services.similarity import final_similarity_score
from app.services.recommendation import recommend_items

# Initialize FastAPI app
app = FastAPI(title=settings.app_name, version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load catalogue once at startup
catalogue = load_catalogue(settings.catalogue_path)

# HEALTH CHECK

@app.get("/health", response_model=HealthResponse)
def health_check():
    """Health check endpoint."""
    return {
        "status": "ok",
        "message": "CineStyle AI backend is running"
    }

# CATALOGUE ENDPOINTS

@app.get("/items", response_model=ItemsResponse)
def get_items():
    """Get all catalogue items."""
    items = load_catalogue(settings.catalogue_path)
    return {
        "count": len(items),
        "items": items
    }

# IMAGE ANALYSIS ENDPOINTS

@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze_image(file: UploadFile = File(...)):
    """
    Analyze an uploaded outfit image.
    Extracts visual features: colours, texture, shape, style tags, and category hints.
    """
    try:
        # Validate file
        if not file.filename:
            raise HTTPException(status_code=400, detail="No file provided")
        
        # Check file extension
        file_ext = Path(file.filename).suffix.lstrip(".").lower()
        if file_ext not in settings.allowed_extensions:
            raise HTTPException(
                status_code=400,
                detail=f"File type .{file_ext} not supported. Allowed: {', '.join(settings.allowed_extensions)}"
            )
        
        # Save uploaded file
        file_path = settings.uploads_dir / file.filename
        contents = await file.read()
        with open(file_path, "wb") as f:
            f.write(contents)
        
        # Load and preprocess image
        image = load_image(str(file_path))
        image = resize_image(image, max_width=settings.max_image_width)
        
        # Extract features
        features = extract_features(image)
        features_dict = features.model_dump()
        
        return {
            "success": True,
            "features": features
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")

# RECOMMENDATION ENDPOINTS

@app.post("/recommend", response_model=RecommendationResponse)
async def recommend(
    features: dict,
    filters: FilterOptions
):
    """
    Get recommendations based on extracted features and filters.
    Use this when you've already analyzed an image and want to change filters.
    """
    try:
        items = load_catalogue(settings.catalogue_path)
        recommendations = recommend_items(features, filters, items)
        
        return {
            "success": True,
            "query_features": features,
            "filters_applied": filters,
            "count": len(recommendations),
            "recommendations": recommendations
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating recommendations: {str(e)}")

@app.post("/recommend-from-image", response_model=RecommendationResponse)
async def recommend_from_image(
    file: UploadFile = File(...),
    min_price: float = Form(0),
    max_price: float = Form(10000),
    style_tags: str = Form(""),
    categories: str = Form("")
):
    """
    Complete pipeline: upload image, analyze, and get recommendations.
    Simpler for frontend - single endpoint.
    """
    try:
        # Validate file
        if not file.filename:
            raise HTTPException(status_code=400, detail="No file provided")
        
        file_ext = Path(file.filename).suffix.lstrip(".").lower()
        if file_ext not in settings.allowed_extensions:
            raise HTTPException(
                status_code=400,
                detail=f"File type .{file_ext} not supported. Allowed: {', '.join(settings.allowed_extensions)}"
            )
        
        # Save file
        file_path = settings.uploads_dir / file.filename
        contents = await file.read()
        with open(file_path, "wb") as f:
            f.write(contents)
        
        # Preprocess image
        image = load_image(str(file_path))
        image = resize_image(image, max_width=settings.max_image_width)
        
        # Extract features
        features = extract_features(image)
        features_dict = features.model_dump()
        
        # Parse filter options
        style_tags_list = [tag.strip() for tag in style_tags.split(",") if tag.strip()]
        categories_list = [cat.strip() for cat in categories.split(",") if cat.strip()]
        
        filters = FilterOptions(
            min_price=min_price,
            max_price=max_price,
            style_tags=style_tags_list if style_tags_list else None,
            categories=categories_list if categories_list else None
        )
        
        # Get recommendations
        items = load_catalogue(settings.catalogue_path)
        recommendations = recommend_items(features_dict, filters, items)
        
        return {
            "success": True,
            "query_features": features,
            "filters_applied": filters,
            "count": len(recommendations),
            "recommendations": recommendations
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")

# ROOT ENDPOINT

@app.get("/")
def root():
    """Root endpoint with API info."""
    return {
        "message": "CineStyle AI - Outfit Recommender API",
        "endpoints": {
            "health": "/health",
            "items": "/items",
            "analyze": "/analyze (POST)",
            "recommend": "/recommend (POST)",
            "recommend_from_image": "/recommend-from-image (POST)"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
