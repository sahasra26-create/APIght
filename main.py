from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="InKraft API", version="1.0.0")


origins = [
    "http://localhost:3000", # Common React port
    "http://localhost:5173", # Common Vite/React port
    "http://127.0.0.1:3000",
    "http://127.0.0.1:5173",
]


# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files
frontend_path = Path(__file__).parent.parent / "frontend"
app.mount("/static", StaticFiles(directory=str(frontend_path / "static")), name="static")

# Import AI services
from ai_services import (
    generate_brand_names,
    generate_marketing_content,
    analyze_sentiment,
    get_color_palette,
    chat_with_ai,
    generate_logo_prompt,
    generate_logo_image,
    unique_selling_points,
    analyze_competitors
)

# ─────────────────── ROUTES ───────────────────

@app.get("/")
async def root():
    return FileResponse(str(frontend_path / "index.html"))

@app.get("/{page}.html")
async def serve_page(page: str):
    file_path = frontend_path / f"{page}.html"
    if file_path.exists():
        return FileResponse(str(file_path))
    return FileResponse(str(frontend_path / "index.html"))

# Brand Names
@app.post("/api/generate-brand")
async def generate_brand_endpoint(request: dict):
    try:
        result = await generate_brand_names(
            request.get("keywords", ""),
            request.get("industry", "Technology"),
            request.get("tone", "Professional"),
            request.get("language", "en"),
        )
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Marketing Content
@app.post("/api/generate-content")
async def generate_content_endpoint(request: dict):
    try:
        result = await generate_marketing_content(
            request.get("brand_description", ""),
            request.get("tone", "Professional"),
            request.get("content_type", "product_description"),
            request.get("language", "en"),
        )
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Sentiment Analysis
@app.post("/api/analyze-sentiment")
async def analyze_sentiment_endpoint(request: dict):
    try:
        result = await analyze_sentiment(
            request.get("text", ""),
            request.get("brand_tone", "Professional"),
            request.get("language", "en")
        )
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Color Palette
@app.post("/api/get-colors")
async def get_colors_endpoint(request: dict):
    try:
        result = await get_color_palette(
            request.get("tone", "Professional"),
            request.get("industry", "Technology"),
            request.get("language", "en")
        )
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Chat
@app.post("/api/chat")
async def chat_endpoint(request: dict):
    try:
        result = await chat_with_ai(request.get("message", ""))
        return {"success": True, "data": {"content": result}}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Logo Prompt
@app.post("/api/generate-logo")
async def generate_logo_endpoint(request: dict):
    try:
        result = await generate_logo_prompt(
            request.get("brand_name", ""),
            request.get("industry", ""),
            request.get("keywords", ""),
            request.get("language", "en")
        )
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Logo Image (SDXL)
@app.post("/api/generate-logo-image")
async def generate_logo_image_endpoint(request: dict):
    try:
        result = await generate_logo_image(request.get("prompt", ""))
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
# Add this new route near your other @app.post routes
@app.post("/api/generate-usp")
async def generate_usp_endpoint(request: dict):
    try:
        description = request.get("description", "")
        industry = request.get("industry", "")
        language = request.get("language", "en")
        result = await unique_selling_points(description, industry, language)
        
        clean_result = result.replace("*", "")
        clean_result1 = clean_result.replace("#","")
        
        return {"success": True, "data": clean_result1}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
# Add this new route in main.py
@app.post("/api/analyze-competitors")
async def competitors_endpoint(request: dict):
    try:

        brand = request.get("brand_name", "My Brand")
        industry = request.get("industry", "General")
        competitors = request.get("competitors", "")
        language = request.get("language", "en")
        
        if not competitors:
            raise HTTPException(status_code=400, detail="Please provide at least one competitor.")
            
        result = await analyze_competitors(brand, industry, competitors, language)
        clean_result = result.replace("*", "")
        clean_result1 = clean_result.replace("#","")
        return {"success": True, "data": clean_result1}
        
    except Exception as e: 
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    print("\n" + "="*60)
    print("🚀  InKraft Backend Started!")
    print("="*60)
    print("🌐  API running at http://localhost:8000")
    print("📁  Frontend path:", frontend_path)
    print("="*60 + "\n")
    uvicorn.run(app, host="0.0.0.0", port=8000)
