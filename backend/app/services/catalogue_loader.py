import json
from pathlib import Path
from typing import List
from app.models import CatalogueItem

def load_catalogue(catalogue_path: str) -> List[CatalogueItem]:
    """
    Load catalogue items from JSON file.
    
    Args:
        catalogue_path: Path to catalogue.json
    
    Returns:
        List of CatalogueItem objects
    """
    if not Path(catalogue_path).exists():
        # Return empty list if catalogue doesn't exist yet
        return []
    
    try:
        with open(catalogue_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        items = [CatalogueItem(**item) for item in data.get('items', [])]
        return items
    
    except json.JSONDecodeError:
        raise ValueError(f"Catalogue file {catalogue_path} is not valid JSON")
    except Exception as e:
        raise Exception(f"Error loading catalogue: {str(e)}")

def save_catalogue(items: List[dict], catalogue_path: str) -> None:
    """
    Save catalogue items to JSON file.
    
    Args:
        items: List of item dictionaries
        catalogue_path: Path to save to
    """
    Path(catalogue_path).parent.mkdir(parents=True, exist_ok=True)
    
    with open(catalogue_path, 'w', encoding='utf-8') as f:
        json.dump({"items": items}, f, indent=2, ensure_ascii=False)
