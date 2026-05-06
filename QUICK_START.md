# CineStyle AI - Quick Reference Guide

## Start the Application (30 seconds)

### Windows
```
Double-click run_all.bat
```

### macOS/Linux
```bash
cd backend && python -m uvicorn app.main:app --reload &
cd frontend && npm run dev
```

## Access Points

| Service | URL | Purpose |
|---------|-----|---------|
| **Frontend** | http://localhost:5173 | Web UI |
| **Backend** | http://localhost:8000 | API Server |
| **API Docs** | http://localhost:8000/docs | Swagger Documentation |
| **Health** | http://localhost:8000/health | Status Check |

## 📸 How to Use

1. **Upload** → Drag image or click to browse
2. **Analyze** → System extracts features (2-5 seconds)
3. **Filter** → Adjust budget, category, style (optional)
4. **Shop** → Click "View Item" on recommendations

## Frontend Features

### Components Ready to Use
- ✅ Image upload with drag-drop
- ✅ Real-time recommendations
- ✅ Dynamic filtering
- ✅ Mobile responsive
- ✅ Error handling
- ✅ Loading states
- ✅ Modern UI with gradients
- ✅ Example outfit gallery

### Styling
- Framework: **Tailwind CSS**
- Colors: Indigo, Purple, Pink gradients
- Icons: Emojis for visual appeal
- Animations: Smooth transitions and hovers

---

## 🔧 Backend Features

### Endpoints
```
POST /recommend-from-image
  ├─ Takes: Image file, filters
  └─ Returns: Top 12 recommendations

POST /analyze
  ├─ Takes: Image file
  └─ Returns: Extracted features

GET /items
  ├─ Takes: None
  └─ Returns: All catalogue items

GET /health
  ├─ Takes: None
  └─ Returns: Status OK

GET /docs
  ├─ Takes: None
  └─ Returns: Swagger UI
```

### Image Analysis Pipeline
```
Upload → Load → Resize → Extract:
  ├─ Dominant Colors (KMeans, 5 colors)
  ├─ Color Histogram (HSV 18+25 bins)
  ├─ Texture Features (edges, contrast, saturation)
  ├─ Shape Features (aspect ratio, coverage)
  ├─ Category Hints (clothing type prediction)
  └─ Style Tags (formal, casual, vintage, etc.)
```

### Similarity Scoring
```
Final Score = 
  35% × Color_Similarity +
  10% × Histogram_Similarity +
  15% × Texture_Similarity +
  10% × Shape_Similarity +
  15% × Category_Match +
  15% × StyleTags_Match
```

### Configuration
- ⚙️ Environment variables ready
- ⚙️ Easy customization points
- ⚙️ Batch script for quick start
- ⚙️ Production ready structure

---

## Troubleshooting

### Issue: "Backend is not available"
**Solution:** Run backend manually
```bash
cd backend
python -m uvicorn app.main:app --reload
```

### Issue: npm command not found
**Solution:** Install Node.js from https://nodejs.org

### Issue: Python not found
**Solution:** 
- Install Python 3.12+
- Add to PATH
- Use `python3` if needed

### Issue: Port already in use
**Solution:** 
```bash
# Kill process using port 8000
lsof -ti:8000 | xargs kill -9

# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

---

## Security Notes

 **For Development Only**
- CORS allows all origins
- File upload has no auth
- No rate limiting
- Debug mode enabled

For production:
- [ ] Restrict CORS origins
- [ ] Add authentication
- [ ] Add rate limiting
- [ ] Disable debug mode
- [ ] Use HTTPS
- [ ] Add input validation

---

## File Structure Quick Guide

```
cinestyle-ai/
├── backend/                    # Python/FastAPI backend
│   ├── app/
│   │   ├── main.py            # API endpoints
│   │   ├── models.py          # Data schemas
│   │   ├── config.py          # Settings
│   │   ├── services/          # Business logic
│   │   └── data/catalogue.json # Products DB
│   └── requirements.txt        # Dependencies
│
├── frontend/                   # React/Vite frontend
│   ├── src/
│   │   ├── App.jsx            # Main component
│   │   ├── components/        # React components
│   │   ├── api/api.js         # API client
│   │   └── styles/main.css    # Styles
│   ├── package.json           # NPM config
│   └── vite.config.js         # Build config
│
├── README.md                   # Full documentation
├── IMPROVEMENTS.md             # Detailed improvements
├── QUICK_START.md              # This file
└── run_all.bat                # Quick start script
```

---

## Performance Tips

### Frontend
- Disable animations if slow: Remove `hover:scale-105` from components
- Clear cache: Ctrl+Shift+Delete
- Hard refresh: Ctrl+Shift+R

### Backend
- Optimize image size: Reduce max_image_width in config
- Reduce K-Means clusters: Change kmeans_clusters: 3 (from 5)
- Profile performance: `python -m cProfile -s cumtime`

### Database
- Add caching for catalogue
- Index products by category
- Pre-compute feature vectors

## Learning Resources

### How It Works
1. **Feature Extraction** → `app/services/feature_extraction.py`
2. **Similarity** → `app/services/similarity.py`
3. **Recommendations** → `app/services/recommendation.py`
4. **Frontend** → `src/App.jsx`

### Customization Ideas
- [ ] Add user accounts
- [ ] Save favorites
- [ ] Social sharing
- [ ] AR try-on integration
- [ ] Real-time price updates
- [ ] Influencer partnerships
- [ ] Style quiz integration

---

## Deployment Checklist

- [ ] Build frontend: `npm run build`
- [ ] Test production build: `npm run preview`
- [ ] Set environment variables
- [ ] Disable debug mode
- [ ] Enable HTTPS
- [ ] Add authentication
- [ ] Set up monitoring
- [ ] Configure CDN
- [ ] Add logging
- [ ] Set up backups
- [ ] Performance testing
- [ ] Security audit

---

## Support

### Getting Help
1. Check README.md first
2. Review IMPROVEMENTS.md
3. Check error messages in browser console
4. Check backend logs in terminal
5. Review API docs at `/docs`

### Common Errors
- **"Cannot read property 'slice' of undefined"** → Image upload failed
- **"TypeError: Cannot read property 'items'"** → Backend not responding
- **"CORS error"** → Backend CORS issue (should be fixed)

---

**Status**: ✅ Ready to Use
**Last Updated**: April 2026
**Version**: 1.0
