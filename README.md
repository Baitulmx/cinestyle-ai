# CineStyle AI – Outfit Recommender

## 1. What the Software Does
CineStyle AI is a web application that analyzes an outfit image and recommends similar real world clothing items using a custom, explainable feature extraction and similarity matching algorithm.

---

## 2. Overview
CineStyle AI is designed to help users find clothing inspired by outfits from films and TV. The system:

1. Accepts uploaded outfit images or example selections  
2. Extracts visual features (colour, texture, shape, style)  
3. Compares them with a curated catalogue  
4. Ranks similar clothing items  
5. Displays recommendations with explanations  
6. Allows filtering by price, category, and style  

---

## 3. Core Features
- Image upload (drag & drop or click)
- Example outfit buttons
- Feature extraction:
  - Dominant colours
  - Texture metrics
  - Shape characteristics
  - Style tags
- Recommendation system with similarity scoring
- Match explanation per item
- Filtering system:
  - Budget
  - Category
  - Style tags

---

# USER GUIDE

## Step 1 – Requirements
Make sure you have installed:
- Python 3.12
- Node.js 18+
- npm

---

## Step 2 – Running the System

### Option A (Windows)
Double click:
    run_all.bat

This starts:
- Backend → http://localhost:8000 and http://localhost:8000/docs
- Frontend → http://localhost:5173  

---

### Option B (Manual Setup)

#### Backend
    cd backend
    python -m venv venv
    venv\Scripts\activate
    pip install -r requirements.txt
    python -m uvicorn app.main:app --reload

Backend runs at:
    http://localhost:8000 and http://localhost:8000/docs

---

#### Frontend (new terminal)
    cd frontend
    npm install
    npm run dev

Frontend runs at:
    http://localhost:5173

---

## Step 3 – Using the Application

1. Open:
    http://localhost:5173

2. Upload an image:
   - Drag & drop  
   - Click “Select Image”  
   - Or use example buttons  

3. Wait for processing

4. View results:
   - Recommended clothing items  
   - Match percentage  
   - Explanation of similarity  

5. Adjust filters:
   - Budget slider  
   - Category  
   - Style tags  

---

## Step 4 – Example Inputs
- Any outfit image (e.g. jacket, jeans, full outfit)
- Built-in example buttons

---

## Step 5 – Example Output
Each recommendation includes:
- Product name
- Price
- Category
- Match percentage
- Explanation (e.g. similar colours, matching style)
- Link to retailer

---

## 1. Tech Stack

Backend:
- FastAPI
- OpenCV
- NumPy
- scikit-learn
- Pydantic

Frontend:
- React
- Vite
- Tailwind CSS
- Axios

---

## 2. Dataset Used
- backend/app/data/catalogue.json
- ~60 clothing items
- Includes name, category, price, style tags, features

---

## 3. API Endpoints
- GET /health  
- GET /items  
- POST /analyze  
- POST /recommend  
- POST /recommend-from-image  

---

## 4. How It Works
1. Image uploaded  
2. Features extracted (colour, texture, shape, style)  
3. Compared with catalogue  
4. Similarity score calculated  
5. Top matches returned  

---

## 5. Known Limitations
- Static dataset (not real store data)  
- Placeholder links/images  
- No external APIs  
- Rule based system (no deep learning model)  
- Category detection is approximate  

---

## 6. Why Not CLIP?
CLIP was not used because:
- Too heavy for project scope  
- Requires large dependencies  
- Less explainable  

A custom algorithm was used for:
- Transparency  
- Simplicity  
- Faster performance  

---

## 7. Testing Checklist
- Upload valid image  
- Upload invalid file  
- Use example buttons  
- Apply filters  
- Check recommendations update  
- Verify loading/error states  

---

## 8. Project Structure
cinestyle-ai/
- backend/
- frontend/
- README.md
- run_all.bat